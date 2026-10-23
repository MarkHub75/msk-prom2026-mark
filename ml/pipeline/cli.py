"""CLI keeps replay/native/linq execution modes explicit."""
import argparse
import importlib
import json
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
    sink = HttpEventSink(args.backend_url, os.environ.get('MOSPROM_BACKEND_TOKEN'),
                         evidence_base_url=args.evidence_base_url) if args.backend_url else None
    return Pipeline(BehaviorEngine(config), outbox, args.state_dir, sink)


def run_video(args, pipeline):
    import cv2
    import numpy as np
    from datetime import datetime, timezone
    from ml.detection import preprocess, decode
    manifests = [json.loads(Path(path).read_text()) for path in args.manifest]
    backends = []
    for manifest in manifests:
        if args.backend == 'native':
            from ml.detection import NativeReferenceBackend
            weights = manifest.get('weights_path') or manifest.get('weights', {}).get('path')
            if not weights:
                raise ValueError('native manifest requires weights_path')
            backends.append(NativeReferenceBackend(weights, manifest, device=args.device))
        else:
            from ml.linq import LinQBackend
            backends.append(LinQBackend(manifest, runner=load_object(args.linq_runner) if args.linq_runner else None))
    cap = cv2.VideoCapture(int(args.source) if args.source.isdigit() else args.source)
    if not cap.isOpened():
        raise ValueError('video source unavailable')
    epoch, frame_id, last_sample = str(uuid4()), -1, -float('inf')
    live = args.live
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not live and (not np.isfinite(fps) or fps <= 0):
        raise ValueError('file video has no valid FPS/timebase')
    start = time.monotonic()
    live_source = LatestFrameSource(cap) if live else None
    latencies, events_count, processed, failures = [], 0, 0, 0
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
            if media_ms - last_sample < 1000 / args.sample_fps:
                continue
            last_sample = media_ms
            if not live and args.realtime:
                delay = media_ms / 1000 - (time.monotonic() - start)
                if delay > 0:
                    time.sleep(delay)
            if not live:
                observed = time.monotonic()
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            detections, model_ids, errors = [], [], []
            for manifest, backend in zip(manifests, backends):
                tensor, transform = preprocess(rgb, manifest)
                model_id = manifest.get('model_id', manifest.get('id', 'unversioned'))
                model_ids.append(model_id)
                result = backend.infer({'request_id': f'{epoch}:{frame_id}:{model_id}', 'model_id': model_id,
                                         'inputs': {manifest['input'].get('name', 'images'): tensor}})
                if result['status'] != 'ok':
                    errors.append(model_id)
                    continue
                detections.extend(decode(result['outputs'], manifest, transform))
            for idx, d in enumerate(detections):
                d['detection_id'] = f'{frame_id}:{idx}'
            elapsed_ms = (time.monotonic() - observed) * 1000
            stale = live and elapsed_ms > args.max_age_ms
            batch = {'schema_version': '1.0', 'camera_id': args.camera_id, 'stream_epoch': epoch,
                     'frame_id': frame_id, 'media_time_ms': media_ms, 'image_size': [rgb.shape[1], rgb.shape[0]],
                     'ingested_at': datetime.now(timezone.utc).isoformat(), 'request_id': f'{epoch}:{frame_id}',
                     'model_id': '+'.join(model_ids), 'model_ids': model_ids, 'backend': args.backend,
                     'status': 'gap' if errors or stale else 'ok', 'detections': [] if errors or stale else detections}
            mutations = pipeline.process(batch, rgb if batch['status'] == 'ok' else None)
            processed += 1
            failures += int(batch['status'] != 'ok')
            events_count += len(mutations)
            latencies.append(elapsed_ms)
            for event in mutations:
                print(json.dumps(event, allow_nan=False))
        return {'execution_backend': args.backend, 'processed_frames': processed, 'failed_or_stale_frames': failures,
                'event_mutations': events_count, 'frame_cycle_p50_ms': float(np.percentile(latencies, 50)) if latencies else None,
                'frame_cycle_p95_ms': float(np.percentile(latencies, 95)) if latencies else None,
                'wall_seconds': time.monotonic() - start, **pipeline.outbox.counts()}
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
    video.add_argument('--linq-runner', help='Approved SDK bridge callable module:name')
    video.add_argument('--sample-fps', type=float, default=5)
    video.add_argument('--max-age-ms', type=float, default=2000)
    video.add_argument('--max-frames', type=int, default=0)
    video.add_argument('--live', action='store_true', help='Live source uses monotonic receive timestamps')
    video.add_argument('--realtime', action='store_true', help='Pace file playback by media time')
    args = parser.parse_args(argv)
    if args.command == 'video' and (args.sample_fps <= 0 or args.max_age_ms <= 0 or args.max_frames < 0):
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
    finally:
        pipeline.outbox.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        # Avoid printing SDK/HTTP exception messages that may contain secrets.
        print(f'ML worker failed: {type(exc).__name__}; inspect local inputs and runbook', file=sys.stderr)
        sys.exit(1)
