"""Source-scoped detector recall on full saved CAVIAR playback scenes.

Uses the already-audited actor matcher, no new inference or negative invention.
Unlabelled areas and unmatched predictions stay UNKNOWN. This is neither an
event evaluation nor an independent industrial benchmark.
"""
from collections import Counter
import json
from pathlib import Path

from ml.argus_replay import digest, write_json
from ml.quality.temporal.caviar import associate, _label


def evaluate(root):
    root = Path(root)
    intake = json.loads((root / 'matvey_inputs_v1.json').read_text())
    src = Path('/workspace/datasets/research/releases/caviar-running-walking-source3/v1-20261024/frame_annotations.jsonl')
    expected = 'bf9d1a2d2e26ba0602122f46275de1eb1054ae83922762a006d8e04be8d52fae'
    if digest(src) != expected:
        raise ValueError('published actor annotation changed')
    refs = {(r['sequence'], r['frame_index0']): r for r in
            (json.loads(x) for x in src.read_text().splitlines())}
    results, details = [], []
    for sid, sequence in [('S01_caviar_run', 'Fight_RunAway1'), ('S01_caviar_walk', 'Walk1')]:
        scene = root / 'new_full_scenes' / sid
        meta = json.loads((scene / 'matvey_scene.json').read_text())
        rows = [json.loads(x) for x in (scene / 'matvey_detections.jsonl').read_text().splitlines()]
        producer = next(s['producer_scene'] for s in intake['scenes'] if s['scene_id'] == sid)
        if producer['full_length_mp4']['sha256'] != meta['source_sha256']:
            raise ValueError('playback source identity changed')
        for mid in ['coco-reference-yolov8n', 'pose-split-v1']:
            counts, unknown = Counter(), 0
            for row in rows:
                ref = refs[(sequence, row['frame_index'])]
                if [ref['width'], ref['height']] != row['image_size'] or abs(row['original_pts_ms'] - ref['canonical_frame_time_ms']) > 1e-8:
                    raise ValueError('source GT geometry/projected clock differ')
                model = next(m for m in row['models'] if m['model_id'] == mid)
                predictions = [{'class_name': d['class_name'], 'bbox_xyxy': d['bbox_xyxy']}
                               for d in model['detections'] if d['class_name'] == 'person']
                matches = associate(ref['source_objects'], predictions)
                unknown += len(predictions) - len(set(matches.values()))
                for i, obj in enumerate(ref['source_objects']):
                    label = _label(obj)
                    if label is None:
                        continue
                    counts[label + '_known_gt_actor_frames'] += 1
                    counts[label + '_matched_person_actor_frames'] += int(i in matches)
                    details.append({'scene_id': sid, 'frame_index': row['frame_index'],
                        'original_pts_ms': row['original_pts_ms'], 'model_id': mid,
                        'source_actor': obj['track_id'], 'source_gait': label,
                        'matched_person_at_IoU05': i in matches})
            metrics = dict(counts)
            for label in ['walking', 'running']:
                denominator = counts[label + '_known_gt_actor_frames']
                metrics[label + '_known_positive_person_recall'] = counts[label + '_matched_person_actor_frames'] / denominator if denominator else None
            results.append({'scene_id': sid, 'sequence': sequence, 'model_id': mid,
                'source_sha256': meta['source_sha256'], 'metrics': metrics,
                'unmatched_person_proposals_unknown': unknown,
                'precision': None, 'event_precision_recall_f1': 'NOT_MEASURED',
                'independent_test': False, 'target_industrial_quality': 'NOT_MEASURED',
                'scope': 'person localization on visible source walking/running actor boxes; NOT gait classification accuracy',
                'matching': 'existing unique bidirectional IoU>=0.5, ambiguity unmatched; every decoded frame',
                'source_video': 'full lossy source-JPEG MP4 reconstruction; nominal25FPS projection, not capture PTS',
                'missing_annotations_are_negative': False})
    write_json(root / 'SOURCE_SCOPED_DETECTOR_METRICS.json', {
        'schema': 'matvey-source-scoped-detector-recall-v1', 'results': results,
        'annotation_path': str(src), 'annotation_sha256': expected,
        'new_neural_calls': 0, 'source_gt_provenance': 'SOURCE_ANNOTATION, development only'})
    write_json(root / 'source_actor_match_details.json', details)
    return results


if __name__ == '__main__':
    result = evaluate('/workspace/artifacts/matvey-final-20261025')
    print(json.dumps(result, indent=2))
