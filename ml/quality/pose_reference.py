"""Bounded native reference on source-PTS videos; NOT a TPU execution witness.

Keep this diagnostic separate from hardware and independent-test quality. All
media/weights are verified before importing the GPU backend. The existing codec
and BehaviorEngine are reused unchanged. Partial outputs retain RUNNING/FAILED
status and must not be presented as completed evaluation.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import fcntl
import json
from pathlib import Path
import time
from uuid import uuid4, uuid5, UUID

from ml.detection.export import sha256


def inspect_inputs(reference_path, model_manifest, weights, *, max_frames=10000):
    reference = json.loads(Path(reference_path).read_text())
    manifest = json.loads(Path(model_manifest).read_text())
    if manifest['decoder'] != 'split_pose_v8':
        raise ValueError('only the reviewed split-pose architecture is accepted')
    if sha256(weights) != manifest['artifacts']['weights']['sha256']:
        raise ValueError('weights hash differs from export manifest')
    media = reference['media']
    total = sum(v['frame_count'] for v in media)
    if not media or not 1 <= total <= max_frames:
        raise ValueError('frame budget exceeded or empty reference')
    seen = set()
    for video in media:
        if video['split'] not in ('validation', 'development'):
            raise ValueError('this development runner must not open final test')
        if video['video_id'] in seen:
            raise ValueError('duplicate video id')
        seen.add(video['video_id'])
        if sha256(video['media_path']) != video['media_sha256']:
            raise ValueError('media digest changed')
        if sha256(video['annotation_path']) != video['annotation_sha256']:
            raise ValueError('source frame annotations changed')
        with Path(video['annotation_path']).open() as stream:
            rows = list(csv.DictReader(stream))
        if len(rows) != video['frame_count']:
            raise ValueError('annotation/media frame count mismatch')
        previous = -1.0
        for index, row in enumerate(rows):
            pts = float(row['video_pts_ms'])
            if int(row['source_frame_id']) != index + 1 or not previous < pts < video['duration_ms']:
                raise ValueError('invalid source frame identity or PTS')
            previous = pts
    return reference, manifest


def run(reference_path, model_manifest, weights, output, *, device='cuda:0',
        gpu_lock='/workspace/artifacts/quality/gpu.lock', max_frames=10000):
    reference, manifest = inspect_inputs(reference_path, model_manifest, weights,
                                         max_frames=max_frames)
    root = Path(output)
    if root.exists():
        raise ValueError('fresh output required; completed evidence is immutable')
    lock_path = Path(gpu_lock); lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        import cv2
        import torch
        from ml.behavior.engine import BehaviorEngine, DEFAULTS
        from ml.detection.codec import preprocess, decode
        from ml.detection.reference import NativeReferenceBackend
        torch.set_num_threads(2)
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
        root.mkdir(parents=True, exist_ok=False)
        run_id = str(uuid4())
        config = {'status': 'RUNNING', 'run_id': run_id,
                  'backend': 'pytorch', 'linq_status': 'NOT_RUN',
                  'reference_sha256': sha256(reference_path),
                  'model_manifest_sha256': sha256(model_manifest),
                  'weights_sha256': sha256(weights), 'device': device,
                  'behavior': DEFAULTS, 'sampling': 'all source frames at original PTS',
                  'scope': 'development diagnostic; source labels are not automatically incident GT',
                  'videos': []}
        def checkpoint():
            (root/'run.json').write_text(json.dumps(config, indent=2, allow_nan=False)+'\n')
        checkpoint(); started = time.perf_counter(); cap = None
        try:
            backend = NativeReferenceBackend(weights, manifest, device)
            with (root/'observations.jsonl').open('w') as observations, (root/'events.jsonl').open('w') as events:
                for video in reference['media']:
                    engine = BehaviorEngine()
                    with Path(video['annotation_path']).open() as stream:
                        rows = list(csv.DictReader(stream))
                    cap = cv2.VideoCapture(video['media_path'])
                    if not cap.isOpened():
                        raise ValueError('cannot decode verified source video')
                    calls_ms = []; visible_people = 0; posture_counts = {}; clip_events = []
                    epoch = f'{run_id}/{video["video_id"]}'
                    for index, row in enumerate(rows):
                        ok, bgr = cap.read()
                        if not ok:
                            raise ValueError('video ended before source frame reference')
                        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
                        tensor, transform = preprocess(rgb, manifest)
                        request_id = str(uuid5(UUID(run_id), f'{video["video_id"]}/{index}'))
                        result = backend.infer({'request_id': request_id, 'model_id': manifest['model_id'],
                                                'inputs': {manifest['input']['name']: tensor}})
                        detections = decode(result['outputs'], manifest, transform)
                        batch = {'schema_version': '1.0', 'camera_id': video['video_id'],
                                 'stream_epoch': epoch, 'frame_id': index,
                                 'media_time_ms': float(row['video_pts_ms']),
                                 'image_size': [rgb.shape[1], rgb.shape[0]], 'status': 'ok',
                                 'detections': detections, 'backend': 'pytorch',
                                 'model_id': manifest['model_id'], 'request_id': request_id,
                                 'ingested_at': datetime.now(timezone.utc).isoformat()}
                        mutations = engine.update(batch)
                        for event in mutations:
                            event['evaluation_video_id'] = video['video_id']
                            events.write(json.dumps(event, allow_nan=False)+'\n')
                        clip_events.extend(mutations)
                        person = [v for v in detections if v['class_name']=='person' and v['score'] >= DEFAULTS['min_score']]
                        postures = [engine._posture(v) for v in person]
                        visible_people += bool(person)
                        for value in postures:
                            posture_counts[value] = posture_counts.get(value, 0)+1
                        calls_ms.append(result['timings']['roundtrip_ms'])
                        observations.write(json.dumps({'video_id': video['video_id'], 'batch': batch,
                            'source_state': row['state'], 'postures': postures,
                            'timing_ms': calls_ms[-1]}, allow_nan=False)+'\n')
                    if cap.read()[0]:
                        raise ValueError('video contains more frames than source reference')
                    cap.release(); cap = None
                    observations.flush(); events.flush()
                    config['videos'].append({'video_id': video['video_id'], 'frame_count': len(rows),
                        'frames_with_people_at_behavior_threshold': visible_people,
                        'postures': posture_counts, 'event_mutations': len(clip_events),
                        'neural_call_total_ms': sum(calls_ms),
                        'neural_call_mean_ms': sum(calls_ms)/len(calls_ms)})
                    checkpoint()
            config.update(status='COMPLETED', wall_seconds=time.perf_counter()-started)
            checkpoint()
        except Exception as exc:
            config.update(status='FAILED', failure_type=type(exc).__name__)
            checkpoint()
            raise
        finally:
            if cap is not None:
                cap.release()
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', required=True); parser.add_argument('--manifest', required=True)
    parser.add_argument('--weights', required=True); parser.add_argument('--output', required=True)
    parser.add_argument('--device', default='cuda:0'); parser.add_argument('--max-frames', type=int, default=10000)
    args = parser.parse_args()
    print(json.dumps(run(args.reference, args.manifest, args.weights, args.output,
                         device=args.device, max_frames=args.max_frames), indent=2))


if __name__ == '__main__':
    main()
