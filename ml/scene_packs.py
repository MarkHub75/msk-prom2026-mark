"""Complete local neural video scenes, with encoded PTS and separate TPU evidence.

No Argus rules/events. Original MP4 is copied unchanged; every decoded source
frame is forwarded through each selected existing model. No interpolation.
"""
import argparse
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
import fcntl
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

import numpy as np

from ml.detection import NativeReferenceBackend, preprocess, decode
from ml.pipeline.video_clock import FilePTS
from ml.quality.handoff import sha256


ROOT = Path('/workspace/artifacts/matvey-scene-packs-20261024')
MODEL_SOURCES = [
    ('pose-split-v1', Path('/workspace/artifacts/detection/pose-split/manifest.json'),
     Path('/workspace/artifacts/detection/pose-split/weights.pt'), 'c6fa93dd1ee4a2c18c900a45c1d864a1c6f7aba75d84f91648a30b7fb641d212'),
    ('helmet-v1', Path('/workspace/artifacts/detection/helmet/manifest.json'),
     Path('/workspace/artifacts/detection/helmet/weights.pt'), '05ed3a517485292d42d6eb6c9be3987ea51cd162e04807d2741eadcac8a19e6c'),
    ('coco-reference-yolov8n', Path('/workspace/artifacts/safewatch-delivery/coco-reference-local-v1-source/manifest.json'),
     Path('/workspace/artifacts/safewatch-delivery/reference/yolov8n.pt'), 'f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36'),
]


def save(path, data):
    from ml.linq.journal import atomic_json
    atomic_json(path, data)


def selected_scenes():
    screen = json.loads(Path('/workspace/artifacts/matvey-scenarios/video-screen-v1/report.json').read_text())
    by_id = {row['video_id']: row for row in screen['videos']}
    scenes = []
    for sid, video in [('S02', '7_te4'), ('S04', '5_tr19'), ('S01', '3_tr45'), ('S02', '7_tr15'), ('S04', '6_tr15')]:
        row = by_id[video]
        scenes.append({'scene_id': sid + '_' + video, 'scenario_id': sid, 'source': row['source_path'],
                       'source_sha256': row['source_sha256'], 'prior_note': row['visual_note'],
                       'rights': 'Mendeley CC BY4.0; DOI10.17632/xjmtb22pff.1; retain attribution'})
    scenes.insert(0, {'scene_id': 'S07_urfall01', 'scenario_id': 'S07',
        'source': '/workspace/datasets/quality/temporal/processed/urfall/fall-01-cam0-rgb.mp4',
        'source_sha256': 'ad08c42886c274c03876a68fb7f2be3b065c951d7202847317d126c61bb1d760',
        'prior_note': 'Laboratory fall reference; historical TPU source fall was missed by old rules. No rules run here.',
        'rights': 'URFall academic NC-SA scope; pre-existing lossy RGB-crop preview, unchanged during export'})
    scenes.append({'scene_id': 'S07_urfall06', 'scenario_id': 'S07',
        'source': '/workspace/datasets/quality/temporal/processed/urfall/fall-06-cam0-rgb.mp4',
        'source_sha256': '8e867b39f72f239e61c04f6cd1857c8abf760725af4f5d5767e7c5204f730f64',
        'prior_note': 'Laboratory source fall reference; previously observable native fall transition, not industrial GT.',
        'rights': 'URFall academic NC-SA scope; pre-existing lossy RGB-crop preview, unchanged during export'})
    return scenes


def load_scene_catalog(path):
    """Pinned, already-published intake only; this performs no source discovery."""
    data = json.loads(Path(path).read_text())
    if data.get('schema') != 'MATVEY_PINNED_SCENE_INPUTS_V1' or not data.get('scenes'):
        raise ValueError('versioned pinned scene input catalog required')
    producer = data['producer']
    if sha256(producer['path']) != producer['sha256']:
        raise ValueError('published producer manifest changed')
    ids = []
    for scene in data['scenes']:
        ids.append(scene['scene_id'])
        if (not scene['scene_id'].replace('_', '').isalnum() or not scene.get('rights')
                or sha256(scene['source']) != scene['source_sha256']):
            raise ValueError('pinned source bytes/rights/scene ID required')
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate input scene IDs')
    return data['scenes']


def run(scene_ids=None, scenes_override=None):
    import cv2
    import torch
    cv2.setNumThreads(1)
    torch.set_num_threads(2)
    ROOT.mkdir(parents=True, exist_ok=True)
    lock = Path('/workspace/artifacts/quality/gpu.lock').open('a')
    device, allocation = 'cpu', 'CPU_SELECTED'
    try:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            active = subprocess.check_output(['nvidia-smi', '--query-compute-apps=pid', '--format=csv,noheader,nounits'], text=True).strip()
            if not active and torch.cuda.is_available():
                device, allocation = 'cuda:0', 'ROOT_ALLOCATED_FREE_GPU_WITH_LOCK'
            else:
                fcntl.flock(lock, fcntl.LOCK_UN)
        except BlockingIOError:
            allocation = 'CPU_GPU_LOCK_HELD_BY_ANOTHER_JOB'
        save(ROOT / 'matvey_compute.json', {'device': device, 'allocation': allocation,
             'checked_utc': datetime.now(timezone.utc).isoformat(), 'threads': 2, 'opencv_threads': 1})
        models = []
        for mid, manifest_path, weights, expected in MODEL_SOURCES:
            if sha256(weights) != expected:
                raise ValueError('pinned existing checkpoint changed')
            manifest = json.loads(manifest_path.read_text())
            models.append((manifest, NativeReferenceBackend(weights, manifest, device=device),
                           {'model_id': mid, 'version': 'v1-existing-checkpoint', 'weights_sha256': expected,
                            'manifest_sha256': sha256(manifest_path), 'classes': dict(enumerate(manifest['classes'])),
                            'source_class_map': dict(enumerate(manifest['classes'])),
                            'class_map': {i: ('no_helmet' if name == 'bare_head' else name)
                                          for i, name in enumerate(manifest['classes'])},
                            'thresholds': manifest['thresholds'], 'decoder': manifest['decoder']}))
        scenes = selected_scenes() if scenes_override is None else scenes_override
        if scene_ids:
            scenes = [s for s in scenes if s['scene_id'] in scene_ids]
        for scene in scenes:
            directory = ROOT / scene['scene_id']
            if (directory / 'matvey_validation.json').exists():
                continue
            directory.mkdir(exist_ok=False)
            if sha256(scene['source']) != scene['source_sha256']:
                raise ValueError('source bytes changed')
            original = directory / 'matvey_source_original.mp4'
            shutil.copyfile(scene['source'], original)
            clock, counts = FilePTS(original), Counter()
            cap, index, started = cv2.VideoCapture(str(original)), 0, time.perf_counter()
            rows = directory / 'matvey_detections.jsonl'
            with rows.open('x') as stream:
                while True:
                    ok, bgr = cap.read()
                    if not ok:
                        break
                    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
                    row = {'frame_index': index, 'original_pts_ms': clock.at(index),
                           'image_size': [rgb.shape[1], rgb.shape[0]],
                           'rgb_sha256': hashlib.sha256(rgb.tobytes(order='C')).hexdigest(),
                           'backend': 'PYTORCH_CUDA' if device.startswith('cuda') else 'PYTORCH_CPU', 'models': []}
                    for manifest, backend, spec in models:
                        tensor, transform = preprocess(rgb, manifest)
                        result = backend.infer({'model_id': manifest['model_id'],
                            'request_id': scene['scene_id'] + ':' + str(index) + ':' + manifest['model_id'],
                            'inputs': {manifest['input']['name']: tensor}})
                        detections = decode(result['outputs'], manifest, transform)
                        exported = []
                        for detection in detections:
                            name = detection['class_name']
                            exported.append({'class_id': manifest['classes'].index(name),
                                'source_class_name': name, 'class_name': 'no_helmet' if name == 'bare_head' else name,
                                'confidence': detection['score'], 'bbox_xyxy': detection['bbox_xyxy'],
                                'pose_coco17': detection.get('keypoints')})
                            counts[manifest['model_id'] + ':' + name] += 1
                        row['models'].append({'model_id': manifest['model_id'], 'version': spec['version'],
                             'detections': exported, 'original_transform': asdict(transform),
                             'input_sha256': hashlib.sha256(tensor.tobytes()).hexdigest(),
                             'inference_timings_ms': result['timings']})
                    stream.write(json.dumps(row, allow_nan=False) + '\n')
                    index += 1
            cap.release()
            if index != len(clock.times) or sha256(original) != scene['source_sha256']:
                raise ValueError('complete source frame/byte census mismatch')
            linq = []
            if scene['scene_id'] == 'S07_urfall01':
                source = Path('/workspace/artifacts/matvey-egor-linq-urfall01-20261024-v2')
                shutil.copytree(source, directory / 'matvey_separate_historical_linq_capture')
                linq = list(range(0, 151, 15))
            save(directory / 'matvey_linq_frames.json', {'frame_indices': linq, 'origin': 'HISTORICAL_REAL_CAPTURE' if linq else 'NONE',
                 'new_linq_calls': 0, 'same_source_sha256_required': scene['source_sha256']})
            save(directory / 'matvey_missing_frames.json', {'local_inference_missing_frame_indices': [],
                 'linq_missing_frame_indices': [i for i in range(index) if i not in linq],
                 'interpolation_performed': False})
            limitations = ['No Argus rules/events or final Argus schema.', 'No independent event GT or violation decision.',
                 'COCO reference has no qualified forklift/action/fire/smoke/cigarette/harness/manual-cargo specialist.',
                 'Missing detections are not negatives. GPU/CPU outputs are not LinQ outputs.',
                 'PIL RGB letterbox preprocessing; raw output tensors not retained for local frames, decoded results retained.']
            save(directory / 'matvey_scene.json', {**scene, 'source_file': original.name,
                 'status': 'COMPLETE_LOCAL_ALL_FRAMES', 'format': 'INTERMEDIATE_NOT_ARGUS_FINAL',
                 'device': device, 'processed_frames': index, 'original_frames': len(clock.times),
                 'model_specs': [spec for _, _, spec in models], 'detected_object_counts': dict(counts),
                 'wall_seconds': time.perf_counter() - started, 'linq_processed_frame_indices': linq,
                 'limitations': limitations, 'raw_local_tensors_retained': False})
            with rows.open() as stream:
                parsed = [json.loads(line) for line in stream]
            if [r['frame_index'] for r in parsed] != list(range(index)) or any(r['original_pts_ms'] != clock.at(i) for i, r in enumerate(parsed)):
                raise ValueError('saved frame/PTS coverage check failed')
            save(directory / 'matvey_validation.json', {'status': 'PASS_COMPLETE_LOCAL_FRAME_COVERAGE',
                 'frames': index, 'model_calls': index * len(models), 'source_sha256': sha256(original),
                 'detections_sha256': sha256(rows), 'pts_basis': 'ENCODED_BEST_EFFORT_PTS',
                 'model_backend': device, 'not_linq': True, 'no_interpolation': True})
            report = 'Scene ' + scene['scene_id'] + '\n' + scene['prior_note'] + '\n\nObserved neural object counts:\n' + json.dumps(dict(counts), indent=2) + '\n\nCannot confirm:\n' + '\n'.join(limitations) + '\n'
            (directory / 'matvey_report.txt').write_text(report)
            finalize_scene(directory)
            refresh_manifest()
            print(json.dumps({'scene': scene['scene_id'], 'status': 'COMPLETE', 'frames': index, 'device': device}), flush=True)
    finally:
        fcntl.flock(lock, fcntl.LOCK_UN)
        lock.close()


def refresh_manifest():
    entries = []
    for path in sorted(ROOT.glob('*/matvey_scene.json')):
        d = json.loads(path.read_text())
        entries.append({'scene_id': d['scene_id'], 'scenario_id': d['scenario_id'], 'path': str(path.parent),
                        'status': d['status'], 'frames': d['processed_frames'], 'device': d['device'],
                        'linq_frames': d['linq_processed_frame_indices'], 'source_sha256': d['source_sha256'],
                        'original_mp4': str(path.parent / 'matvey_source_original.mp4'),
                        'detections_json': str(path.parent / 'matvey_detections.json'),
                        'detections_jsonl': str(path.parent / 'matvey_detections.jsonl'),
                        'linq_frame_list': str(path.parent / 'matvey_linq_frames.json'),
                        'missing_frame_list': str(path.parent / 'matvey_missing_frames.json'),
                        'verification': str(path.parent / 'matvey_validation.json'),
                        'technical_report': str(path.parent / 'matvey_report.txt'),
                        'target_event_quality': 'NOT_QUALIFIED',
                        'signal_review': d.get('signal_review')})
    extras = {name: str(ROOT / filename) for name, filename in {
        'readme': 'matvey_README.md', 'independent_review': 'matvey_independent_review_v2.json',
        'linq_readiness': 'matvey_linq_readiness.json', 'checkpoint_zip': 'matvey_best_three_v1.zip',
        'optional_S08_status': 'S08_BLOCKED/matvey_status.json'}.items() if (ROOT / filename).is_file()}
    save(ROOT / 'matvey_manifest.json', {'schema': 'MATVEY_SCENE_PACK_CATALOG_V1',
         'updated_utc': datetime.now(timezone.utc).isoformat(), 'scenes': entries,
         'total_complete_scenes': len(entries), 'total_complete_local_frames': sum(e['frames'] for e in entries),
         'total_local_model_calls': sum(e['frames'] for e in entries) * len(MODEL_SOURCES),
         'files': extras, 'new_linq_calls': 0, 'final_argus_contract': 'PENDING',
         'S08': 'BLOCKED_NO_CONFIRMED_MANUAL_CARGO_SOURCE_OR_SPECIALIST_MODEL',
         'fresh_linq': 'BLOCKED_OWN_STAGING_AND_JUPYTER_CAPABILITY_ABSENT'})


def finalize_scene(directory):
    directory = Path(directory)
    meta = json.loads((directory / 'matvey_scene.json').read_text())
    rows = [json.loads(line) for line in (directory / 'matvey_detections.jsonl').read_text().splitlines()]
    for spec in meta['model_specs']:
        spec['source_class_map'] = spec['classes']
        spec['class_map'] = {key: ('no_helmet' if name == 'bare_head' else name)
                             for key, name in spec['classes'].items()}
        spec['role'] = {'pose-split-v1': 'pose', 'helmet-v1': 'extra', 'coco-reference-yolov8n': 'detector'}[spec['model_id']]
        spec['class_map_scope'] = 'numeric source IDs preserved; only bare_head -> no_helmet product alias'
    for index, row in enumerate(rows):
        if row['frame_index'] != index or len(row['models']) != len(meta['model_specs']):
            raise ValueError('saved frame/model census mismatch')
        for model, spec in zip(row['models'], meta['model_specs']):
            if model['model_id'] != spec['model_id']:
                raise ValueError('saved model order mismatch')
            for d in model['detections']:
                if spec['class_map'][str(d['class_id'])] != d['class_name']:
                    raise ValueError('class ID/name mapping mismatch')
                if d['pose_coco17'] is not None and len(d['pose_coco17']) != 17:
                    raise ValueError('COCO17 pose required')
    signals = {
        'S02': {'available': 'person, generic COCO vehicle proposals and poses over all frames',
                'absent': 'qualified forklift-specific model, metric distance and danger policy',
                'cannot_confirm': 'unsafe approach; COCO car/bus/truck/suitcase overlap may be misclassification'},
        'S07': {'available': 'person bbox/COCO17 sequence over a source fall reference',
                'absent': 'qualified temporal classifier and independent floor/episode GT',
                'cannot_confirm': 'fall event acceptance, prolonged lying, unconsciousness; PPE detections in indoor scene may be false positives'},
        'S04': {'available': 'people/poses and scene context in previously screened haze footage',
                'absent': 'fire/smoke/cigarette specialist inference; these classes NOT_EVALUATED',
                'cannot_confirm': 'haze origin, smoking/open flame or violation; equipment COCO labels may be wrong'},
        'S01': {'available': 'person/pose and generic vehicle context over every frame',
                'absent': 'qualified running action head and actor-level gait GT',
                'cannot_confirm': 'running versus walking; this is a context scene, not a positive running demonstration'},
        'PPE': {'available': 'helmet/no_helmet proposals, people and poses on the complete source timeline',
                'absent': 'exhaustive video PPE GT and Argus PPE rule',
                'cannot_confirm': 'site-specific PPE violations, head/person ownership or independent accuracy'},
    }
    meta['signal_review'] = meta.get('input_signal_review', signals[meta['scenario_id']])
    meta['signal_review']['method'] = 'model-output census plus prior source screen; no new event GT'
    save(directory / 'matvey_scene.json', meta)
    save(directory / 'matvey_detections.json', {'format': 'MATVEY_SCENE_INTERMEDIATE_NOT_ARGUS_FINAL',
         'source_sha256': meta['source_sha256'], 'source_file': 'matvey_source_original.mp4',
         'inference_backend': meta['device'], 'frame_count': len(rows), 'model_specs': meta['model_specs'],
         'no_interpolation': True, 'frames': rows})
    validation = json.loads((directory / 'matvey_validation.json').read_text())
    validation['class_map_and_pose_validation'] = 'PASS'
    validation['json_sha256'] = sha256(directory / 'matvey_detections.json')
    save(directory / 'matvey_validation.json', validation)
    indices = meta['linq_processed_frame_indices']
    per_model = {s['model_id']: (indices if s['model_id'] == 'pose-split-v1' else []) for s in meta['model_specs']}
    save(directory / 'matvey_linq_frames.json', {'per_model': per_model, 'frame_indices': indices,
         'origin': 'HISTORICAL_REAL_CAPTURE' if indices else 'NONE', 'fresh_linq_calls': 0,
         'same_source_sha256': meta['source_sha256'], 'all_local_rows_are_gpu_or_cpu': True})
    save(directory / 'matvey_missing_frames.json', {'local_inference_missing_frame_indices': [],
         'linq_missing_frame_indices': [i for i in range(len(rows)) if i not in indices],
         'per_model_linq_missing': {mid: [i for i in range(len(rows)) if i not in chosen] for mid, chosen in per_model.items()},
         'interpolation_performed': False})
    with (directory / 'matvey_report.txt').open('a') as stream:
        stream.write('\nTarget signal review:\n' + json.dumps(meta['signal_review'], indent=2) +
                     '\nCounts are per-frame proposals, not unique objects, GT or accepted events.\n')


def validate_records(meta, rows):
    if len(rows) != meta['original_frames'] or len(rows) != meta['processed_frames']:
        raise ValueError('full source frame census required')
    previous = -1
    for index, row in enumerate(rows):
        if (type(row['frame_index']) is not int or row['frame_index'] != index
                or type(row['original_pts_ms']) not in (int, float) or not np.isfinite(row['original_pts_ms'])
                or row['original_pts_ms'] < 0 or row['original_pts_ms'] <= previous):
            raise ValueError('chronological original frame/PTS required')
        previous = row['original_pts_ms']
        if row['backend'] != ('PYTORCH_CUDA' if meta['device'].startswith('cuda') else 'PYTORCH_CPU'):
            raise ValueError('local execution provenance mismatch')
        if [m['model_id'] for m in row['models']] != [s['model_id'] for s in meta['model_specs']]:
            raise ValueError('per-frame model census mismatch')
        width, height = row['image_size']
        for model, spec in zip(row['models'], meta['model_specs']):
            for d in model['detections']:
                key = str(d['class_id'])
                if (type(d['class_id']) is not int or spec['class_map'].get(key) != d['class_name']
                        or spec['source_class_map'].get(key) != d['source_class_name']):
                    raise ValueError('source/product class mapping mismatch')
                score = d['confidence']
                box = d['bbox_xyxy']
                if (type(score) not in (int, float) or not np.isfinite(score) or not 0 <= score <= 1
                        or len(box) != 4 or any(type(v) not in (int, float) for v in box) or not np.isfinite(box).all()
                        or not 0 <= box[0] <= box[2] <= width or not 0 <= box[1] <= box[3] <= height):
                    raise ValueError('confidence or original-pixel box invalid')
                kp = d['pose_coco17']
                if kp is not None:
                    points = np.asarray(kp)
                    if (points.shape != (17, 3) or not np.isfinite(points).all()
                            or any(type(v) not in (int, float) for point in kp for v in point)
                            or (points[:, 2] < 0).any() or (points[:, 2] > 1).any()
                            or (points[:, 0] < 0).any() or (points[:, 0] > width).any()
                            or (points[:, 1] < 0).any() or (points[:, 1] > height).any()):
                        raise ValueError('finite COCO17 confidence triples required')


def verify_scene(directory):
    """Independent full RGB/PTS/input audit; no new model or remote call."""
    import cv2
    cv2.setNumThreads(1)
    directory = Path(directory)
    meta = json.loads((directory / 'matvey_scene.json').read_text())
    rows = [json.loads(line) for line in (directory / 'matvey_detections.jsonl').read_text().splitlines()]
    combined = json.loads((directory / 'matvey_detections.json').read_text())
    if combined['frames'] != rows or combined['model_specs'] != meta['model_specs']:
        raise ValueError('JSON/JSONL/metadata representations differ')
    validate_records(meta, rows)
    source = directory / 'matvey_source_original.mp4'
    if sha256(source) != meta['source_sha256']:
        raise ValueError('original MP4 bytes changed')
    clock = FilePTS(source)
    if len(clock.times) != len(rows):
        raise ValueError('encoded frame census differs')
    manifests = {}
    for mid, path, weights, expected in MODEL_SOURCES:
        spec = next(s for s in meta['model_specs'] if s['model_id'] == mid)
        if spec['weights_sha256'] != expected or sha256(weights) != expected or sha256(path) != spec['manifest_sha256']:
            raise ValueError('model provenance hash mismatch')
        manifests[mid] = json.loads(path.read_text())
    cap, count = cv2.VideoCapture(str(source)), 0
    try:
        for row in rows:
            ok, bgr = cap.read()
            if not ok:
                raise ValueError('source ended before saved records')
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            if (row['original_pts_ms'] != clock.at(count)
                    or row['rgb_sha256'] != hashlib.sha256(rgb.tobytes(order='C')).hexdigest()
                    or row['image_size'] != [rgb.shape[1], rgb.shape[0]]):
                raise ValueError('source frame/RGB/encoded-PTS binding mismatch')
            inputs = {}
            for model in row['models']:
                manifest = manifests[model['model_id']]
                identity = json.dumps([manifest['input'], manifest.get('padding_value', 114)], sort_keys=True)
                if identity not in inputs:
                    tensor, transform = preprocess(rgb, manifest)
                    inputs[identity] = hashlib.sha256(tensor.tobytes()).hexdigest(), asdict(transform)
                if inputs[identity] != (model['input_sha256'], model['original_transform']):
                    raise ValueError('actual input tensor/transform binding mismatch')
            count += 1
        if cap.read()[0]:
            raise ValueError('unreported source frames remain')
    finally:
        cap.release()
    linq = json.loads((directory / 'matvey_linq_frames.json').read_text())
    missing = json.loads((directory / 'matvey_missing_frames.json').read_text())
    if missing['local_inference_missing_frame_indices'] != [] or missing['interpolation_performed'] is not False:
        raise ValueError('local complete/no-interpolation declarations differ')
    for mid, indices in linq['per_model'].items():
        if missing['per_model_linq_missing'][mid] != [i for i in range(count) if i not in indices]:
            raise ValueError('LinQ missing-frame census mismatch')
    historical = None
    if linq['frame_indices']:
        from ml.video_handoff import verify_export
        historical = verify_export(directory / 'matvey_separate_historical_linq_capture')
        if json.loads((directory / 'matvey_separate_historical_linq_capture/matvey_linq_frames.intermediate.json').read_text())['source']['sha256'] != meta['source_sha256']:
            raise ValueError('LinQ evidence belongs to another source')
    return {'scene_id': meta['scene_id'], 'status': 'PASS_INDEPENDENT_COMPLETE_SOURCE_AUDIT',
            'frames': count, 'model_results': count * len(meta['model_specs']), 'device': meta['device'],
            'source_sha256': meta['source_sha256'], 'json_sha256': sha256(directory / 'matvey_detections.json'),
            'historical_linq_review': historical, 'new_neural_calls': 0, 'new_remote_calls': 0,
            'independent_event_quality': 'NOT_EVALUATED'}


def main():
    global ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--scene', action='append')
    parser.add_argument('--scene-catalog', help='pinned existing producer scenes, no acquisition')
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--review-output')
    args = parser.parse_args()
    ROOT = Path(args.root).resolve()
    if not ROOT.is_relative_to(Path('/workspace/artifacts')):
        parser.error('media and predictions must stay outside Git under artifacts')
    if args.verify_only:
        output = Path(args.review_output) if args.review_output else ROOT / 'matvey_independent_review_v1.json'
        if not output.resolve().is_relative_to(Path('/workspace/artifacts')):
            parser.error('verification reports stay outside Git under artifacts')
        if output.exists():
            parser.error('use a new review output; old evidence is preserved')
        reports = [verify_scene(p.parent) for p in sorted(ROOT.glob('*/matvey_validation.json'))]
        if not reports:
            parser.error('no completed scene packs to verify')
        with output.open('x') as stream:
            json.dump({'status': 'PASS', 'scenes': reports, 'new_neural_calls': 0, 'new_remote_calls': 0}, stream, indent=2)
            stream.write('\n')
        print(json.dumps({'status': 'PASS', 'scenes': len(reports), 'frames': sum(r['frames'] for r in reports)}))
        return
    run(args.scene, load_scene_catalog(args.scene_catalog) if args.scene_catalog else None)


if __name__ == '__main__':
    main()
