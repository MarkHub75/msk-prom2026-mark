"""Frozen development-video diagnostic using one loaded SDK CPU graph.

No TPU, GPU, training or service transport. Does not score event ground truth.
"""
import argparse
import csv
import hashlib
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import time
from uuid import uuid4
from .compile import sha256


def decoder_command(video):
    # Rawvideo has no timestamps. Disable CFR duplication so each pipe frame
    # corresponds exactly to one selected original source index.
    return ['ffmpeg', '-v', 'error', '-threads', '2', '-noautorotate',
            '-i', video['media_path'], '-vf', 'select=not(mod(n\\,15))', '-filter_threads', '2',
            '-threads', '2', '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1']


def pin_selection(reference_path, manifest_path, compile_dir):
    reference = json.loads(Path(reference_path).read_text())
    manifest = json.loads(Path(manifest_path).read_text())
    compiled = Path(compile_dir)
    report = json.loads((compiled / 'compile-report.json').read_text())
    if (report['compile_status'] != 'PASS' or manifest['decoder'] != 'split_pose_v8'
            or report['source_onnx_sha256'] != manifest['artifacts']['onnx']['sha256']):
        raise ValueError('reviewed split pose source graph required')
    media = reference['media']
    if len(media) != 20 or len({v['video_id'] for v in media}) != 20:
        raise ValueError('exact frozen UR20 development set required')
    videos = []
    for video in media:
        if video['split'] not in ('validation', 'development') or video['fps'] != 30:
            raise ValueError('only frozen thirty-FPS development media accepted')
        if sha256(video['media_path']) != video['media_sha256'] or sha256(video['annotation_path']) != video['annotation_sha256']:
            raise ValueError('media/annotation hash drift')
        with Path(video['annotation_path']).open() as file:
            rows = list(csv.DictReader(file))
        if len(rows) != video['frame_count']:
            raise ValueError('source frame count differs')
        previous = -1
        for index, row in enumerate(rows):
            pts = float(row['video_pts_ms'])
            if int(row['source_frame_id']) != index + 1 or not previous < pts < video['duration_ms']:
                raise ValueError('invalid source identity or PTS')
            previous = pts
        selected = [dict(rows[i], source_frame_index=i) for i in range(0, len(rows), 15)]
        if any(float(b['video_pts_ms'])-float(a['video_pts_ms']) >= 750 for a,b in zip(selected, selected[1:])):
            raise ValueError('sampling gap violates unchanged behavior continuity')
        videos.append({'video_id': video['video_id'], 'media_sha256': video['media_sha256'],
                       'annotation_sha256': video['annotation_sha256'], 'group_id': video['group_id'],
                       'selected_frames': selected})
    return reference, manifest, {
        'reference_sha256': sha256(reference_path), 'model_manifest_sha256': sha256(manifest_path),
        'compiler_artifacts_sha256': {name: sha256(compiled / name) for name in
            ['quantized.qm.onnx', 'scales.json', 'compile-report.json', 'optimized.onnx']},
        'source_onnx_sha256': report['source_onnx_sha256'],
        'sampling': 'every fifteenth zero-based source frame, stride=15,start=0, 2FPS, original annotation video_pts_ms',
        'selected_frame_count': sum(len(v['selected_frames']) for v in videos), 'videos': videos}


def verify_decoders(reference, selection):
    """Count and pin every selected RGB frame before loading a neural graph."""
    for video, selected in zip(reference['media'], selection['videos']):
        decoded = subprocess.run(decoder_command(video), capture_output=True, check=True, timeout=30)
        frame_bytes = video['width'] * video['height'] * 3
        if len(decoded.stdout) != frame_bytes * len(selected['selected_frames']):
            raise ValueError('selected decoder output count differs from exact source index selection')
        for i, row in enumerate(selected['selected_frames']):
            row['decoded_rgb_sha256'] = hashlib.sha256(decoded.stdout[i*frame_bytes:(i+1)*frame_bytes]).hexdigest()
    selection['decoder_check'] = 'ALL_SELECTED_RGB_HASHES_AND_COUNTS_VERIFIED_BEFORE_NEURAL_INFERENCE'


def run(reference_path, manifest_path, compile_dir, output, *, budget_seconds=600, frozen_selection=None):
    if not 0 < budget_seconds <= 600:
        raise ValueError('allocated budget must be positive and at most600seconds')
    out = Path(output)
    if out.exists(): raise ValueError('fresh immutable output directory required')
    reference, manifest, selection = pin_selection(reference_path, manifest_path, compile_dir)
    # Limit this owned process and its decoder children, not system configuration.
    affinity = sorted(os.sched_getaffinity(0))[:2]
    os.sched_setaffinity(0, affinity)
    from ml.behavior.engine import BehaviorEngine, DEFAULTS
    verify_decoders(reference, selection)
    if frozen_selection is not None:
        frozen = json.loads(Path(frozen_selection).read_text())
        for key in ('reference_sha256', 'model_manifest_sha256', 'source_onnx_sha256',
                    'sampling', 'selected_frame_count', 'videos', 'decoder_check'):
            if selection[key] != frozen[key]:
                raise ValueError('paired input selection differs from frozen protocol')
    out.mkdir(parents=True, exist_ok=False)
    (out / 'selection.json').write_text(json.dumps(selection, indent=2) + '\n')
    config = {'status': 'RUNNING', 'run_id': str(uuid4()), 'backend': 'vendor_quantized_CPU_reference_NOT_HARDWARE',
        'linq_status': 'NOT_RUN', 'device': 'cpu', 'cpu_affinity': affinity, 'threads': 2,
        'selection_sha256': sha256(out / 'selection.json'), 'behavior': DEFAULTS,
        'hypothesis': 'candidate event recall increases without FP increase; scoring external on frozen development GT',
        'budget_seconds': budget_seconds, 'videos': [], 'completed_calls': 0,
        'scope': 'all UR20 development; never independent final test; no promotion from numeric closeness'}
    def checkpoint():
        (out / 'run.json').write_text(json.dumps(config, indent=2, allow_nan=False) + '\n')
    checkpoint(); started = time.monotonic(); decoder = None
    try:
        import numpy as np
        import torch
        torch.set_num_threads(2); torch.set_num_interop_threads(1)
        from ml.detection.codec import preprocess, decode
        from .quantized_reference import QuantizedReferenceBackend
        folder = Path(compile_dir)
        backend = QuantizedReferenceBackend(folder / 'quantized.qm.onnx', folder / 'scales.json', folder / 'compile-report.json')
        config['graph_load_seconds'] = time.monotonic() - started
        with (out / 'observations.jsonl').open('x') as observations, (out / 'events.jsonl').open('x') as events:
            for video, selected in zip(reference['media'], selection['videos']):
                engine = BehaviorEngine(); call_times = []; people_frames = 0; posture_counts = {}; event_count = 0
                frame_bytes = video['width'] * video['height'] * 3
                decoder = subprocess.Popen(decoder_command(video),
                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                for row in selected['selected_frames']:
                    if time.monotonic() - started >= budget_seconds: raise TimeoutError('allocated CPU run budget exhausted')
                    raw = decoder.stdout.read(frame_bytes)
                    if len(raw) != frame_bytes: raise ValueError('verified source decode ended early')
                    if hashlib.sha256(raw).hexdigest() != row['decoded_rgb_sha256']:
                        raise ValueError('sampled RGB differs from pre-neural pinned frame')
                    rgb = np.frombuffer(raw, np.uint8).reshape(video['height'], video['width'], 3)
                    tensor, transform = preprocess(rgb, manifest)
                    call_start = time.perf_counter()
                    outputs = backend.infer({manifest['input']['name']: tensor})
                    call_ms = (time.perf_counter() - call_start) * 1000
                    detections = decode(outputs, manifest, transform)
                    batch = {'schema_version': '1.0', 'camera_id': video['video_id'],
                        'stream_epoch': config['run_id'] + '/' + video['video_id'],
                        'frame_id': row['source_frame_index'], 'media_time_ms': float(row['video_pts_ms']),
                        'image_size': [video['width'], video['height']], 'status': 'ok', 'detections': detections,
                        'backend': config['backend'], 'model_id': manifest['model_id'],
                        'request_id': f"{config['run_id']}:{video['video_id']}:{row['source_frame_index']}",
                        'ingested_at': datetime.now(timezone.utc).isoformat()}
                    mutations = engine.update(batch)
                    for event in mutations:
                        event['evaluation_video_id'] = video['video_id']; events.write(json.dumps(event, allow_nan=False) + '\n')
                    event_count += len(mutations)
                    people = [v for v in detections if v['class_name'] == 'person' and v['score'] >= DEFAULTS['min_score']]
                    postures = [engine._posture(v) for v in people]
                    people_frames += bool(people)
                    for posture in postures: posture_counts[posture] = posture_counts.get(posture, 0) + 1
                    observations.write(json.dumps({'video_id': video['video_id'], 'batch': batch,
                        'source_state': row['state'], 'postures': postures, 'timing_ms': call_ms,
                        'original_transform': transform.__dict__}, allow_nan=False) + '\n')
                    call_times.append(call_ms); config['completed_calls'] += 1
                if decoder.stdout.read(1): raise ValueError('decoder produced unexpected extra sampled frame')
                if decoder.wait(timeout=10) != 0: raise ValueError('decoder failed')
                decoder.stdout.close(); decoder = None
                observations.flush(); events.flush()
                config['videos'].append({'video_id': video['video_id'], 'frame_count': len(call_times),
                    'frames_with_people_at_behavior_threshold': people_frames, 'postures': posture_counts,
                    'event_mutations': event_count, 'neural_call_total_ms': sum(call_times),
                    'neural_call_mean_ms': sum(call_times) / len(call_times)})
                checkpoint()
        if config['completed_calls'] != selection['selected_frame_count']: raise ValueError('incomplete selected corpus')
        config.update(status='COMPLETED', wall_seconds=time.monotonic() - started); checkpoint()
    except BaseException as exc:
        config.update(status='FAILED', failure_type=type(exc).__name__, wall_seconds=time.monotonic() - started)
        checkpoint(); raise
    finally:
        if decoder is not None:
            if decoder.poll() is None: decoder.kill()
            decoder.wait(timeout=10)
            if decoder.stdout is not None: decoder.stdout.close()
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['reference', 'manifest', 'compile-dir', 'output']: parser.add_argument('--' + name, required=True)
    parser.add_argument('--budget-seconds', type=float, default=600)
    parser.add_argument('--frozen-selection', help='paired source/PTS/RGB selection; compiler hashes may differ')
    args = parser.parse_args()
    result = run(args.reference, args.manifest, args.compile_dir, args.output,
                 budget_seconds=args.budget_seconds, frozen_selection=args.frozen_selection)
    print(json.dumps({'status': result['status'], 'completed_calls': result['completed_calls'], 'wall_seconds': result['wall_seconds']}))


if __name__ == '__main__': main()
