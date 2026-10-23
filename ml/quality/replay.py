"""Score host-rule hypotheses against immutable saved neural observations.

No inference or data acquisition. Sampling amendments are explicit and preserve
original PTS. Whole-clip evaluation requires a caller-supplied completed video
census; unrun videos are never silently counted as false negatives.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import time

from ml.behavior import BehaviorEngine
from ml.detection.export import sha256
from ml.quality.temporal.evaluation import evaluate


def replay(observations, truth, output, *, evaluated_videos, rules=None,
           stride=1, camera_to_video=None):
    if type(stride) is not int or stride < 1:
        raise ValueError('positive integer source-frame stride required')
    root = Path(output)
    if root.exists():
        raise ValueError('fresh output required to preserve experiment evidence')
    config = rules or {}
    engine = BehaviorEngine(config)
    gt = json.loads(Path(truth).read_text())
    if gt.get('final_test') or any(v.get('split') not in ('validation','development') for v in gt['videos']):
        raise ValueError('hypothesis replay must not open final test')
    census = set(evaluated_videos)
    if len(census) != len(evaluated_videos):
        raise ValueError('duplicate evaluated video')
    mapping = camera_to_video or {}
    envelopes = []; counts = Counter(); per_video = Counter(); seen = set()
    started = time.perf_counter()
    root.mkdir(parents=True, exist_ok=False)
    with Path(observations).open() as stream, (root/'predictions.jsonl').open('w') as result:
        for line in stream:
            row = json.loads(line)
            batch = row.get('batch', row)
            video = row.get('video_id') or mapping.get(batch['camera_id'])
            if video not in census:
                raise ValueError('observation outside completed video census')
            if batch['frame_id'] % stride and batch['status']=='ok':
                continue
            identity = (video, batch['frame_id'], batch['status'])
            if identity in seen:
                raise ValueError('duplicate source observation')
            seen.add(identity); per_video[video] += 1
            mutations = engine.update(batch)
            for event in mutations:
                envelope = {'video_id': video, 'event': event}
                envelopes.append(envelope)
                result.write(json.dumps(envelope, allow_nan=False)+'\n')
            if batch['status'] != 'ok':
                counts['explicit_gaps'] += 1
                continue
            counts['sampled_frames'] += 1
            persons = [d for d in batch['detections'] if d['class_name']=='person'
                       and d['score']>=engine.config['min_score']]
            if not persons:
                counts['frames_without_person_above_behavior_threshold'] += 1
            elif all(engine._posture(d)=='unknown' for d in persons):
                counts['frames_with_person_but_all_postures_unknown'] += 1
    if set(per_video) != census:
        raise ValueError('completed video census has no matching observations')
    report = evaluate(gt, envelopes, evaluated_video_ids=evaluated_videos,
                      allow_source_reference=True)
    report['replay'] = {'rules': engine.config, 'stride': stride,
        'observation_sha256': sha256(observations), 'truth_sha256': sha256(truth),
        'per_video_observations': dict(per_video), 'counts': dict(counts),
        'execution': 'saved-neural-observations-only; NO_NEW_NEURAL_REQUESTS',
        'wall_seconds': time.perf_counter()-started}
    (root/'metrics.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--observations', required=True); parser.add_argument('--truth', required=True)
    parser.add_argument('--output', required=True); parser.add_argument('--evaluated-videos', required=True)
    parser.add_argument('--rules'); parser.add_argument('--stride', type=int, default=1)
    parser.add_argument('--camera-to-video')
    args = parser.parse_args()
    read = lambda path: json.loads(Path(path).read_text())
    result = replay(args.observations, args.truth, args.output,
                    evaluated_videos=read(args.evaluated_videos),
                    rules=read(args.rules) if args.rules else None, stride=args.stride,
                    camera_to_video=read(args.camera_to_video) if args.camera_to_video else None)
    print(json.dumps({'per_type': result['per_type'], 'replay': result['replay']}, indent=2))


if __name__=='__main__':
    main()
