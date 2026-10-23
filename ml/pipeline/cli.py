"""CLI keeps replay/native/linq execution modes explicit."""
import argparse
import importlib
import json
import math
import os
import sys
import time
from pathlib import Path
from uuid import uuid4
from ml.pipeline.delivery import Outbox, HttpEventSink
from ml.pipeline.runner import Pipeline, read_jsonl
from ml.pipeline.ingress import LatestFrameSource


def load_object(spec):
    module, name = spec.split(':', 1)
    return getattr(importlib.import_module(module), name)


def build_pipeline(args):
    from ml.behavior import BehaviorEngine
    config = json.loads(Path(args.rules).read_text()) if args.rules else None
    outbox = Outbox(Path(args.state_dir) / 'events.sqlite')
    token=None if getattr(args,'sink_kind','external')=='local-test' else os.environ.get('MOSPROM_BACKEND_TOKEN')
    sink = HttpEventSink(args.backend_url, token,
                         evidence_base_url=args.evidence_base_url) if args.backend_url else None
    return Pipeline(BehaviorEngine(config), outbox, args.state_dir, sink)


def run_video(args, pipeline):
    from contextlib import ExitStack
    with ExitStack() as stack:
        return _run_video(args, pipeline, stack)


def _run_video(args, pipeline, stack):
    import cv2
    import numpy as np
    from datetime import datetime, timezone
    from ml.detection import preprocess, decode
    manifests = [json.loads(Path(path).read_text()) for path in args.manifest]
    backends = []
    for manifest, manifest_path in zip(manifests, args.manifest):
        if args.backend == 'native':
            from ml.detection import NativeReferenceBackend
            import torch
            torch.backends.cuda.matmul.allow_tf32 = False
            torch.backends.cudnn.allow_tf32 = False
            weights = manifest.get('weights_path') or manifest.get('weights', {}).get('path')
            if not weights and manifest.get('artifacts', {}).get('weights', {}).get('file'):
                weights = Path(manifest_path).resolve().parent / manifest['artifacts']['weights']['file']
            if not weights:
                raise ValueError('native manifest requires weights_path')
            backends.append(NativeReferenceBackend(weights, manifest, device=args.device))
        else:
            from ml.linq import LinQBackend
            effective = {**manifest, **manifest.get('linq', {})}
            effective.update(rpc_state_dir=str(Path(args.state_dir).resolve()/'rpc'/effective['model_id']),
                journal_dir=str(Path(args.state_dir).resolve()/'requests'),
                format_source_manifest=args.linq_format_source_manifest,timeout=args.linq_timeout)
            if not effective.get('runtime_abi_verified'):
                raise ValueError('LinQ runtime ABI must be verified before video execution')
            if args.linq_runner_factory:
                runner = load_object(args.linq_runner_factory)(effective)
                if hasattr(runner, '__enter__'):
                    runner = stack.enter_context(runner)
            else:
                from ml.linq.local import LocalPytpuRunner
                program = effective.get('program_path')
                if not program:
                    raise ValueError('LinQ manifest requires program_path')
                if not Path(program).is_absolute():
                    program = Path(manifest_path).resolve().parent / program
                runner = stack.enter_context(LocalPytpuRunner(program, effective['program_sha256']))
            backends.append(LinQBackend(effective, runner=runner))
    cap = cv2.VideoCapture(int(args.source) if args.source.isdigit() else args.source)
    if not cap.isOpened():
        raise ValueError('video source unavailable')
    epoch, frame_id, last_sample = str(uuid4()), -1, -float('inf')
    live = args.live
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not live and (not np.isfinite(fps) or fps <= 0):
        raise ValueError('file video has no valid FPS/timebase')
    if args.backend=='linq' and not live:
        from ml.pipeline.file_video import run_file_video
        try:return run_file_video(args,pipeline,cap,manifests,backends,fps)
        finally:cap.release()
    start = time.monotonic()
    live_source = LatestFrameSource(cap) if live else None
    latencies, events_count, processed, failures = [], 0, 0, 0
    last_batch = None
    try:
        while not args.max_frames or processed < args.max_frames:
            if live_source:
                item = live_source.read()
                if item is None:
                    break
                frame_id, media_ms, observed, bgr = item
            else:
                ok, bgr = cap.read()
                if not ok:
                    break
                frame_id += 1
                media_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
            # File PTS must advance; reject broken timestamps rather than fabricate transition timing.
            if not live and frame_id and media_ms <= previous_pts:
                raise ValueError('video timestamps do not advance')
            previous_pts = media_ms
            if media_ms - last_sample + 1e-6 < 1000 / args.sample_fps:
                continue
            last_sample = media_ms
            if not live and args.realtime:
                delay = media_ms / 1000 - (time.monotonic() - start)
                if delay > 0:
                    time.sleep(delay)
            if not live:
                observed = time.monotonic()
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            detections, model_ids, errors, execution_records = [], [], [], []
            for manifest, backend in zip(manifests, backends):
                tensor, transform = preprocess(rgb, manifest)
                model_id = manifest.get('model_id', manifest.get('id', 'unversioned'))
                model_ids.append(model_id)
                input_name = manifest['input'].get('name', 'images')
                input_name = manifest.get('linq', {}).get('input_map', {}).get(input_name, input_name) if args.backend == 'linq' else input_name
                result = backend.infer({'request_id': f'{epoch}:{frame_id}:{model_id}', 'model_id': model_id,
                                         'inputs': {input_name: tensor}})
                execution_records.append({'request_id': result.get('request_id'), 'model_id': model_id,
                    'backend': result.get('backend'), 'status': result['status'],
                    'program_sha256': manifest.get('linq', {}).get('program_sha256') if args.backend == 'linq' else None,
                    'execution_witness': result.get('execution_witness'), 'execution_verified': result.get('execution_verified', False)})
                if result['status'] != 'ok':
                    errors.append(model_id)
                    continue
                outputs = result['outputs']
                if args.backend == 'linq':
                    mapping = manifest.get('linq', {}).get('output_map', {})
                    outputs = {mapping.get(name, name): value for name, value in outputs.items()}
                detections.extend(decode(outputs, manifest, transform))
            for idx, d in enumerate(detections):
                d['detection_id'] = f'{frame_id}:{idx}'
            elapsed_ms = (time.monotonic() - observed) * 1000
            stale = live and elapsed_ms > args.max_age_ms
            batch = {'schema_version': '1.0', 'camera_id': args.camera_id, 'stream_epoch': epoch,
                     'frame_id': frame_id, 'media_time_ms': media_ms, 'image_size': [rgb.shape[1], rgb.shape[0]],
                     'ingested_at': datetime.now(timezone.utc).isoformat(), 'request_id': f'{epoch}:{frame_id}',
                     'model_id': '+'.join(model_ids), 'model_ids': model_ids, 'backend': args.backend,
                     'execution_records': execution_records,
                     'status': 'gap' if errors or stale else 'ok', 'detections': [] if errors or stale else detections}
            last_batch = batch
            mutations = pipeline.process(batch, rgb if batch['status'] == 'ok' else None)
            processed += 1
            failures += int(batch['status'] != 'ok')
            events_count += len(mutations)
            latencies.append(elapsed_ms)
            for event in mutations:
                print(json.dumps(event, allow_nan=False))
        if last_batch is not None:
            gap = {**last_batch, 'frame_id': last_batch['frame_id'] + 1, 'media_time_ms': last_batch['media_time_ms'] + .001, 'status': 'gap', 'detections': [], 'reason': 'source_ended'}
            for event in pipeline.process(gap):
                print(json.dumps(event, allow_nan=False))
                events_count += 1
        return {'execution_backend': args.backend, 'processed_frames': processed, 'failed_or_stale_frames': failures,
                'event_mutations': events_count, 'frame_cycle_p50_ms': float(np.percentile(latencies, 50)) if latencies else None,
                'frame_cycle_p95_ms': float(np.percentile(latencies, 95)) if latencies else None,
                'wall_seconds': time.monotonic() - start, **pipeline.outbox.counts()}
    except Exception:
        if last_batch is not None:
            gap = {**last_batch, 'frame_id': last_batch['frame_id'] + 1,
                   'media_time_ms': last_batch['media_time_ms'] + .001,
                   'status': 'gap', 'detections': [], 'reason': 'worker_error'}
            try:
                for event in pipeline.process(gap):
                    print(json.dumps(event, allow_nan=False))
            except Exception:
                pass
        raise
    finally:
        if live_source:
            live_source.close()
        else:
            cap.release()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', default='runtime')
    parser.add_argument('--rules')
    parser.add_argument('--backend-url', help='Full event endpoint URL')
    parser.add_argument('--evidence-base-url', help='Receiver-accessible URL mapping state-dir contents')
    parser.add_argument('--sink-kind',choices=['external','local-test'],default='external')
    sub = parser.add_subparsers(dest='command', required=True)
    replay = sub.add_parser('replay', help='Replay observation JSONL; does not run neural inference')
    replay.add_argument('--input', required=True)
    sub.add_parser('dispatch', help='Retry pending outbox deliveries')
    video = sub.add_parser('video')
    video.add_argument('--source', required=True)
    video.add_argument('--camera-id', default='cam-01')
    video.add_argument('--manifest', action='append', required=True)
    video.add_argument('--backend', choices=['native', 'linq'], required=True)
    video.add_argument('--device', default='cpu')
    video.add_argument('--linq-runner-factory', help='Per-program approved SDK bridge factory module:name')
    video.add_argument('--linq-timeout',type=float,default=60)
    video.add_argument('--linq-format-source-manifest',default='/workspace/artifacts/linq-rpc/format-source.json')
    video.add_argument('--start-ms',type=float,default=0,help='File window start in original media milliseconds')
    video.add_argument('--end-ms',type=float,help='File window end in original media milliseconds')
    video.add_argument('--source-kind',choices=['real-video','repeated-image-fixture'],default='real-video')
    video.add_argument('--sample-fps', type=float, default=5)
    video.add_argument('--max-age-ms', type=float, default=2000)
    video.add_argument('--max-frames', type=int, default=0)
    video.add_argument('--live', action='store_true', help='Live source uses monotonic receive timestamps')
    video.add_argument('--realtime', action='store_true', help='Pace file playback by media time')
    args = parser.parse_args(argv)
    if args.command == 'video' and (not all(math.isfinite(v) for v in (args.sample_fps,args.max_age_ms,args.linq_timeout,args.start_ms)) or args.end_ms is not None and not math.isfinite(args.end_ms) or args.sample_fps <= 0 or args.max_age_ms <= 0 or args.max_frames < 0 or args.linq_timeout<=0 or args.start_ms<0 or args.end_ms is not None and args.end_ms<=args.start_ms):
        parser.error('invalid sampling/freshness limits')
    pipeline = build_pipeline(args)
    try:
        if args.command == 'replay':
            count = 0
            for batch in read_jsonl(args.input):
                for event in pipeline.process(batch):
                    print(json.dumps(event, allow_nan=False))
                    count += 1
            summary = {'mode': 'observation_replay', 'event_mutations': count, **pipeline.outbox.counts()}
        elif args.command == 'dispatch':
            if pipeline.sink is None:
                parser.error('dispatch requires --backend-url')
            summary = {'sent': pipeline.outbox.dispatch(pipeline.sink), **pipeline.outbox.counts()}
        else:
            summary = run_video(args, pipeline)
        print(json.dumps(summary, allow_nan=False), file=sys.stderr)
        if summary.get('status')=='WAITING_FOR_LINQ':raise SystemExit(3)
        if args.command == 'video' and (summary['processed_frames'] == 0 or summary['failed_or_stale_frames'] == summary['processed_frames']):
            raise SystemExit(2)
    finally:
        pipeline.outbox.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        # Avoid printing SDK/HTTP exception messages that may contain secrets.
        print(f'ML worker failed: {type(exc).__name__}; inspect local inputs and runbook', file=sys.stderr)
        sys.exit(1)
