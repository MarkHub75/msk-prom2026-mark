"""Consume COMPLETE pinned Training video outputs for the existing scene/replay path.

No neural inference. Checks every source RGB/input tensor/raw output and decodes
once from raw using the unmodified Argus helper. It never fills missing frames.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

import numpy as np

from ml.argus_replay import digest, frame_record, write_json
from ml.pipeline.video_clock import FilePTS


PREPROCESS = 'OPENCV_INTER_LINEAR_RGB_LETTERBOX_PAD114_FLOAT32_DIVIDE_255'


def pinned(item):
    path = Path(item['path'])
    if digest(path) != item['sha256'] or ('bytes' in item and path.stat().st_size != item['bytes']):
        raise ValueError('producer artifact changed: ' + str(path))
    return path


def consume(entry, output, snapshot):
    import cv2
    cv2.setNumThreads(1)
    if entry['status'] != 'COMPLETE_BOTH_MODELS':
        raise ValueError('completed model census required')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    source = pinned(entry['source_mp4'])
    shutil.copyfile(source, output / 'matvey_source_original.mp4')
    io_path = Path(snapshot) / 'tools/linq/yolo_io.py'
    if digest(io_path) != '175fedb53f3a41b3da24e4f78245506fc665b5818b90ae90f732adb2ac826a40':
        raise ValueError('unreviewed Argus preprocessing/decoder')
    module_spec = importlib.util.spec_from_file_location('matvey_consumer_pinned_yolo_io', io_path)
    io = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(io)
    clock = FilePTS(source)
    if len(clock.times) != entry['frames']:
        raise ValueError('source frame census differs')
    models = []
    origins = {m['backend'] for m in entry['models']}
    if len(origins) != 1 or not origins <= {'PYTORCH_CUDA', 'PYTORCH_CPU', 'ONNXRUNTIME_CPU'}:
        raise ValueError('one explicit real backend required for this full scene')
    backend = next(iter(origins))
    for model in entry['models']:
        pinned(model['weights'])
        pred, result_path, start = (pinned(model[k]) for k in ['predictions', 'result', 'start'])
        result = json.loads(result_path.read_text())
        if result['status'] != 'COMPLETE' or result['not_inferred_frames'] or result['inferred_frames'] != len(clock.times):
            raise ValueError('partial producer run cannot be called complete')
        values = [json.loads(x) for x in pred.read_text().splitlines()]
        if [r['frame_index0'] for r in values] != list(range(len(clock.times))):
            raise ValueError('missing or duplicate neural frame')
        identity = {k: model[k] for k in ['role', 'model_id', 'model_version', 'weights', 'class_map', 'confidence', 'iou', 'max_det', 'input_size']}
        sha = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
        spec = {'model_id': model['model_id'], 'version': model['model_version'],
            'role': model['role'], 'weights_sha256': model['weights']['sha256'],
            'manifest_sha256': sha, 'class_map': model['class_map'], 'classes': model['class_map'],
            'source_class_map': model['class_map'],
            'thresholds': {'confidence': model['confidence'], 'iou': model['iou'], 'max_detections': model['max_det']},
            'decoder': 'Argus_frozen_yolo_io', 'preprocessing': PREPROCESS,
            'keypoint_coordinate_policy': 'ARGUS_UNCLAMPED_PREDICTIONS',
            'producer_predictions': model['predictions'], 'raw_output_root': model['raw_root']}
        models.append((model, values, spec))
    cap, rows, counts, checked, max_difference = cv2.VideoCapture(str(source)), [], Counter(), 0, 0.0
    try:
        for i in range(len(clock.times)):
            ok, bgr = cap.read()
            if not ok:
                raise ValueError('source video ended early')
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            rgb_sha = hashlib.sha256(rgb.tobytes()).hexdigest()
            row = {'frame_index': i, 'original_pts_ms': clock.at(i), 'image_size': [rgb.shape[1], rgb.shape[0]],
                'rgb_sha256': rgb_sha, 'backend': backend, 'models': []}
            for model, values, spec in models:
                item = values[i]
                if (item['source_sha256'] != entry['source_mp4']['sha256'] or item['encoded_pts_ms'] != clock.at(i)
                    or item['backend'].upper() != backend or item['neural_inferred'] is not True
                    or item['model_version'] != model['model_version'] or item['source_rgb_sha256'] != rgb_sha):
                    raise ValueError('actual neural source/frame/model provenance differs')
                tensor, transform = io.preprocess(rgb, model['input_size'])
                transform = json.loads(json.dumps(transform))
                if hashlib.sha256(tensor.tobytes()).hexdigest() != item['input_sha256'] or transform != item['letterbox']:
                    raise ValueError('actual neural input hash/transform differs')
                raw_path = Path(model['raw_root']) / f'matvey_{i:06d}.npz'
                if raw_path.name != Path(item['raw_file']).name or digest(raw_path) != item['raw_sha256']:
                    raise ValueError('raw neural file hash differs')
                with np.load(raw_path, allow_pickle=False) as z:
                    raw = z['decoded']
                    if int(z['frame_index0']) != i or float(z['encoded_pts_ms']) != clock.at(i) or list(raw.shape) != item['raw_shape'] or raw.dtype != np.float32 or not np.isfinite(raw).all():
                        raise ValueError('raw numeric shape/frame/PTS differs')
                pose = model['role'] == 'pose'
                decoded = io.postprocess(raw, transform, model['confidence'], model['iou'],
                    nc=1 if pose else len(model['class_map']), kpt_shape=(17, 3) if pose else None,
                    classes=model.get('product_class_ids'), max_det=model['max_det'])
                expected = item['detections']
                if len(decoded) != len(expected):
                    raise ValueError('raw decoder count differs from saved predictions')
                exported = []
                for actual, saved in zip(decoded, expected):
                    if actual['cls'] != saved['cls'] or model['class_map'][str(saved['cls'])] != saved['name']:
                        raise ValueError('class map/ID differs')
                    for key in ['score', 'bbox_xyxy'] + (['kpts'] if pose else []):
                        delta = float(np.max(np.abs(np.asarray(actual[key]) - np.asarray(saved[key]))))
                        max_difference = max(max_difference, delta)
                        if delta > .011:
                            raise ValueError('numeric decoder drift exceeds serialized rounding')
                    exported.append({'class_id': saved['cls'], 'source_class_name': saved['name'],
                        'class_name': saved['name'], 'confidence': saved['score'], 'bbox_xyxy': saved['bbox_xyxy'],
                        'pose_coco17': saved.get('kpts')})
                    counts[model['model_id'] + ':' + saved['name']] += 1
                value = {'model_id': model['model_id'], 'version': model['model_version'],
                    'detections': exported, 'original_transform': transform, 'input_sha256': item['input_sha256'],
                    'raw_output_file': str(raw_path), 'raw_output_sha256': item['raw_sha256']}
                frame_record(row, value, allow_outside_keypoints=True)
                row['models'].append(value)
                checked += 1
            rows.append(row)
        if cap.read()[0]:
            raise ValueError('unreported source frames remain')
    finally:
        cap.release()
    meta = {'scene_id': entry['scene_id'], 'scenario_id': 'S07' if entry['scene_id'].startswith(('ur-', 'S07')) else 'S04',
        'source': str(source), 'source_sha256': entry['source_mp4']['sha256'], 'source_file': 'matvey_source_original.mp4',
        'source_kind': entry['source_kind'], 'rights': entry['rights'], 'source_original': entry['source_original'],
        'original_frames': len(rows), 'processed_frames': len(rows), 'model_specs': [m[2] for m in models],
        'device': 'cuda:0' if backend == 'PYTORCH_CUDA' else 'cpu', 'backend': backend,
        'status': 'COMPLETE_TRAINING_NEURAL_IMPORT', 'preprocessing': PREPROCESS,
        'detected_object_counts': dict(counts), 'source_clip_labels': entry.get('source_clip_labels', []),
        'GT': entry.get('GT'), 'fresh_linq_calls': 0, 'linq_processed_frame_indices': [],
        'no_interpolation': True, 'signal_review': {'available': 'actual full-frame trained/pretrained model outputs',
            'absent': 'independent industrial event GT and site permission policy',
            'cannot_confirm': 'site-specific violation, medical state or independent event accuracy'}}
    write_json(output / 'matvey_scene.json', meta)
    with (output / 'matvey_detections.jsonl').open('x') as stream:
        stream.writelines(json.dumps(x, allow_nan=False) + '\n' for x in rows)
    write_json(output / 'matvey_detections.json', {'format': 'MATVEY_SCENE_INTERMEDIATE_NOT_ARGUS_FINAL',
        'source_sha256': meta['source_sha256'], 'model_specs': meta['model_specs'], 'frames': rows,
        'frame_count': len(rows), 'no_interpolation': True, 'inference_backend': backend})
    report = {'status': 'PASS_TRAINING_SOURCE_INPUT_RAW_DECODER_IMPORT', 'frames': len(rows),
        'model_observations': checked, 'max_saved_vs_frozen_decoder_abs_difference': max_difference,
        'new_neural_calls': 0, 'source_rgbs_and_input_hashes_all_checked': True,
        'raw_files_and_encoded_pts_all_checked': True, 'event_GT': 'NOT_MEASURED'}
    write_json(output / 'matvey_validation.json', report)
    print(json.dumps({'scene': entry['scene_id'], **report}), flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--index', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--argus-snapshot', type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.index.read_text())
    for entry in data['scenes']:
        destination = args.output / entry['scene_id']
        if (destination / 'matvey_validation.json').exists():
            continue
        consume(entry, destination, args.argus_snapshot)


if __name__ == '__main__':
    main()
