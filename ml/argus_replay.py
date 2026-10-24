"""Offline adapter to a pinned, unmodified Argus analysis snapshot.

Uses Argus FrameDetections/ModelSpec, read_jsonl and analyze directly. Never
inserts an external artifact into an app database or submits a LinQ request.
Backend provenance travels in a sidecar because FrameDetections has no such
fields. A mixed replay never becomes a live TPU end-to-end claim.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

from ml.pipeline.video_clock import FilePTS


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                    allow_nan=False) + '\n')


def fingerprint(spec, backend, preprocessing):
    """Include the inputs Argus's current cache key itself omits."""
    identity = {'model': spec, 'backend': backend, 'preprocessing': preprocessing,
                'adapter': 'matvey-argus-frame-adapter-v1'}
    return hashlib.sha256(json.dumps(identity, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def frame_record(row, model, *, allow_outside_keypoints=False):
    """Lossless numeric mapping; never invent a detection for a missing frame."""
    idx, pts = row['frame_index'], row['original_pts_ms']
    if type(idx) is not int or idx < 0 or type(pts) not in (int, float) or not math.isfinite(pts) or pts < 0:
        raise ValueError('invalid source ordinal/PTS')
    out = []
    for d in model['detections']:
        cls, score, box, pose = d['class_id'], d['confidence'], d['bbox_xyxy'], d.get('pose_coco17')
        if type(cls) is not int or cls < 0 or type(score) not in (float, int) or not math.isfinite(score) or not 0 <= score <= 1:
            raise ValueError('invalid class/confidence')
        if len(box) != 4 or any(type(x) not in (int, float) or not math.isfinite(x) for x in box) or box[0] > box[2] or box[1] > box[3]:
            raise ValueError('invalid bbox')
        width, height = row['image_size']
        if not 0 <= box[0] <= box[2] <= width or not 0 <= box[1] <= box[3] <= height:
            raise ValueError('bbox outside original image')
        if pose is not None and (len(pose) != 17 or any(len(p) != 3 or any(type(x) not in (int, float) or not math.isfinite(x) for x in p) or not 0 <= p[2] <= 1 or (not allow_outside_keypoints and (not 0 <= p[0] <= width or not 0 <= p[1] <= height)) for p in pose)):
            raise ValueError('invalid COCO17')
        out.append({'cls': cls, 'name': d['class_name'], 'score': score,
                    'bbox_xyxy': box, 'kpts': pose})
    return {'frame_idx': idx, 'ts_ms': pts, 'detections': out}


def snapshot_import(snapshot):
    snapshot = Path(snapshot).resolve()
    receipt = json.loads((snapshot / 'MATVEY_SNAPSHOT.json').read_text())
    for rel, expected in receipt['files'].items():
        if digest(snapshot / rel) != expected:
            raise ValueError('Argus snapshot file changed: ' + rel)
    sys.path.insert(0, str(snapshot / 'src'))
    from safewatch import config
    if Path(config.ROOT).resolve() != snapshot:
        raise ValueError('unexpected application import location')
    if (snapshot / '.env').exists() or (snapshot / 'config/user.yaml').exists():
        raise ValueError('replay requires pristine snapshot config, no runtime credentials')
    return receipt


def argus_tpu_decoder(snapshot):
    """Return the actual app tail + postprocess, using saved numeric replies."""
    import importlib.util
    import numpy as np
    import onnxruntime as ort
    module_spec = importlib.util.spec_from_file_location('matvey_frozen_argus_yolo_io',
        Path(snapshot) / 'tools/linq/yolo_io.py')
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    delivery = json.loads((Path(__file__).parent / 'safewatch.delivery.json').read_text())
    sessions, proof = {}, []
    opts = ort.SessionOptions()
    opts.intra_op_num_threads = opts.inter_op_num_threads = 1
    for item in delivery['models']:
        mid = 'pose-split-v1' if item['model']['task'] == 'pose' else 'helmet-v1'
        tail = next(f for f in item['files'] if f['path'].endswith('_tail.onnx'))
        program = next(f for f in item['files'] if f['path'].endswith('.tpu'))
        if digest(tail['path']) != tail['sha256'] or digest(program['path']) != program['sha256']:
            raise ValueError('pinned Argus tail/program changed')
        sessions[mid] = ort.InferenceSession(tail['path'], sess_options=opts, providers=['CPUExecutionProvider']), tail, program

    def decode(pack, row, model):
        session, tail, program = sessions[model['model_id']]
        numeric = (Path(pack) / model['numeric_directory']).resolve()
        if not numeric.is_relative_to(Path(pack).resolve()):
            raise ValueError('numeric reply path outside capture')
        execution = json.loads((numeric / 'matvey_completion_receipt.json').read_text())
        if execution != model['execution'] or execution['request_id'] != execution['response_id'] or execution['status_code'] != 0 or execution['journal_state'] != 'COMPLETED' or execution['program_sha256'] != program['sha256']:
            raise ValueError('uncorrelated/noncompleted TPU reply')
        with np.load(numeric / 'response.npz', allow_pickle=False) as z:
            outputs = {name: z[name].copy() for name in z.files}
        if set(outputs) != set(execution['output_tensors']):
            raise ValueError('TPU tensor names differ')
        for name, array in outputs.items():
            expected = execution['output_tensors'][name]
            if (list(array.shape) != expected['shape'] or str(array.dtype) != expected['dtype'] or array.nbytes != expected['nbytes'] or hashlib.sha256(array.tobytes()).hexdigest() != expected['sha256'] or not np.isfinite(array).all()):
                raise ValueError('TPU tensor identity differs')
        values = session.run(None, {i.name: outputs[i.name] for i in session.get_inputs()})[0]
        transform = model['original_transform']
        w, h = row['image_size']
        metadata = {'scale': min(transform['input_width'] / w, transform['input_height'] / h),
                    'pad': (transform['left'], transform['top']), 'orig_hw': (h, w), 'size': 640}
        pose = model['model_id'] == 'pose-split-v1'
        thresholds = model['decoder_thresholds']
        dets = module.postprocess(values, metadata, conf=thresholds['confidence'], iou=thresholds['iou'],
            nc=1 if pose else 2, kpt_shape=(17, 3) if pose else None, max_det=thresholds['max_detections'])
        proof.append({'frame_index': row['frame_index'], 'original_pts_ms': row['original_pts_ms'],
            'model_id': model['model_id'], 'request_id': execution['request_id'],
            'response_id': execution['response_id'], 'status_code': 0,
            'program_sha256': program['sha256'], 'tail_sha256': tail['sha256'],
            'numeric_output_file_sha256': digest(numeric / 'response.npz'),
            'tail_output_shape': list(values.shape), 'detections': len(dets),
            'postprocess': 'unmodified frozen tools/linq/yolo_io.py; bbox rounded0.1px/keypoints0.01; no second NMS',
            'new_cnn_or_tpu_calls': 0})
        return {'frame_idx': row['frame_index'], 'ts_ms': row['original_pts_ms'], 'detections': dets}
    return decode, proof


def replay(scene, output, snapshot, historical=None, decode_tpu=False):
    receipt = snapshot_import(snapshot)
    from safewatch import rules, media, config as app_config
    from safewatch.analysis.pipeline import analyze
    from safewatch.inference.artifacts import read_jsonl, cache_key
    from safewatch.types import ModelSpec, AnalysisConfig
    import cv2
    cv2.setNumThreads(1)
    scene, output = Path(scene), Path(output)
    meta = json.loads((scene / 'matvey_scene.json').read_text())
    source = scene / 'matvey_source_original.mp4'
    if digest(source) != meta['source_sha256']:
        raise ValueError('source bytes changed')
    rows = [json.loads(x) for x in (scene / 'matvey_detections.jsonl').read_text().splitlines()]
    clock = FilePTS(source)
    if len(rows) != len(clock.times) or [r['frame_index'] for r in rows] != list(range(len(rows))):
        raise ValueError('incomplete source timeline')
    if any(r['original_pts_ms'] != clock.at(r['frame_index']) for r in rows):
        raise ValueError('source PTS differs')
    history = None
    actual_decoder, decoder_proof = argus_tpu_decoder(snapshot) if decode_tpu else (None, [])
    if decode_tpu and not historical:
        raise ValueError('Argus TPU decoder needs a real saved capture')
    if historical:
        history = json.loads((Path(historical) / 'matvey_linq_frames.intermediate.json').read_text())
        if history['source']['sha256'] != meta['source_sha256']:
            raise ValueError('TPU capture belongs to another video')
        indices = [r['frame_index'] for r in history['frames']]
        if indices != sorted(set(indices)) or not indices:
            raise ValueError('invalid TPU frame census')
        selected = [rows[i] for i in indices]
    else:
        selected = rows
    output.mkdir(parents=True, exist_ok=False)
    specs, records, provenance, cache_review = {}, {}, [], []
    for spec in meta['model_specs']:
        mid = spec['model_id']
        historical_models = {r['frame_index']: next((m for m in r['models'] if m['model_id'] == mid), None)
                             for r in history['frames']} if history else {}
        use_tpu = bool(historical_models) and all(historical_models.values())
        backend = 'LINQ_HISTORICAL_REAL_SERVICE_OUTPUTS' if use_tpu else selected[0]['backend']
        pre = spec.get('preprocessing', meta.get('preprocessing',
            'PIL_BILINEAR_RGB_LETTERBOX_PAD114_FLOAT32_MULTIPLY_1_OVER_255'))
        fp_spec = dict(spec)
        if use_tpu:
            fp_spec['historical_program_sha256'] = next(iter(historical_models.values()))['program_sha256']
        fp_spec['consumer_decode'] = 'frozen_argus_raw_tail_postprocess' if use_tpu and decode_tpu else 'lossless_saved_decoded_values'
        fp = fingerprint(fp_spec, backend, pre)
        role = spec['role']
        model = ModelSpec(id='matvey-replay-' + mid, version='640-replay-v1-' + fp[:16],
            task='pose' if role == 'pose' else 'detect', input_size=640,
            conf=spec['thresholds']['confidence'], iou=spec['thresholds']['iou'],
            classes={int(k): v for k, v in spec['class_map'].items()},
            linq_program=None, linq_tail=None, local_onnx=None)
        if role == 'detector' and list(model.classes) != list(range(80)):
            raise ValueError('primary detector must preserve COCO80 ABI')
        path = output / (mid + '.jsonl')
        with path.open('x') as stream:
            for row in selected:
                local = next(m for m in row['models'] if m['model_id'] == mid)
                item = historical_models[row['frame_index']] if use_tpu else local
                if use_tpu:
                    old_row = next(r for r in history['frames'] if r['frame_index'] == row['frame_index'])
                    if old_row['original_pts_ms'] != row['original_pts_ms'] or old_row['source_rgb_sha256'] != row['rgb_sha256']:
                        raise ValueError('TPU source frame identity differs')
                converted = actual_decoder(historical, row, item) if use_tpu and actual_decoder else frame_record(
                    row, item, allow_outside_keypoints=spec.get('keypoint_coordinate_policy') == 'ARGUS_UNCLAMPED_PREDICTIONS')
                for d in converted['detections']:
                    if use_tpu and actual_decoder:
                        # App resolves names from ModelSpec; worker emits numeric strings.
                        if d['cls'] not in model.classes:
                            raise ValueError('unknown consumer class ID')
                    elif model.classes.get(d['cls']) != d['name']:
                        raise ValueError('consumer class map differs')
                stream.write(json.dumps(converted, allow_nan=False) + '\n')
                provenance.append({'frame_index': row['frame_index'], 'original_pts_ms': row['original_pts_ms'],
                    'model_id': mid, 'argus_ref': model.id + '@' + model.version, 'backend': backend,
                    'neural_observation': True, 'tracker_propagation': False,
                    'source_rgb_sha256': row['rgb_sha256'], 'identity_fingerprint': fp,
                    'preprocessing': pre,
                    'program_sha256': item.get('program_sha256') if use_tpu else None})
        frames = read_jsonl(path, len(selected))
        if [f.frame_idx for f in frames] != [r['frame_index'] for r in selected]:
            raise ValueError('Argus reader frame identity mismatch')
        records[mid], specs[mid] = frames, model
        newer = model.model_copy(update={'version': model.version + '-changed'})
        old_key = cache_key(meta['source_sha256'], model, 1, 'local', False)
        new_key = cache_key(meta['source_sha256'], newer, 1, 'local', False)
        if old_key == new_key:
            raise ValueError('version change did not invalidate cache')
        cache_review.append({'model_id': mid, 'fingerprint': fp, 'cache_key': old_key,
            'changed_version_cache_key': new_key, 'different': True,
            'cache_not_injected': True, 'backend_key_for_schema_test_only': 'local'})
    dims = selected[0]['image_size']
    probe = media.probe_video(source)
    if probe is None:
        raise ValueError('Argus source probe failed')
    # Argus wants duration relative to its epoch. Preserve encoded PTS in records;
    # include any nonzero start offset in the analysis horizon.
    end = round(clock.times[-1] + (clock.times[-1] - clock.times[-2] if len(clock.times) > 1 else 1))
    step = selected[1]['frame_index'] - selected[0]['frame_index'] if len(selected) > 1 else 1
    config = AnalysisConfig(width=dims[0], height=dims[1], fps=probe.fps, step=step,
        duration_ms=end, calibration=None, zones=[], rules={},
        class_conf=app_config.get_settings().class_conf,
        active_classes=sorted({name for m in specs.values() for name in m.classes.values()}))
    primary = next(s['model_id'] for s in meta['model_specs'] if s['role'] == 'detector')
    pose_id = next((s['model_id'] for s in meta['model_specs'] if s['role'] == 'pose'), None)
    extras = [(specs[s['model_id']], records[s['model_id']]) for s in meta['model_specs'] if s['role'] == 'extra']
    result = analyze(records[primary], records[pose_id] if pose_id else None, source, config,
                     specs[pose_id] if pose_id else None, specs[primary], extras)
    write_json(output / 'events.json', [e.model_dump(mode='json') for e in result.episodes])
    write_json(output / 'analysis.json', result.model_dump(mode='json'))
    write_json(output / 'analysis_config.json', config.model_dump(mode='json'))
    write_json(output / 'models.json', {k: v.model_dump(mode='json') for k, v in specs.items()})
    write_json(output / 'tpu_tail_decoder_proof.json', decoder_proof)
    write_json(output / 'provenance.json', {'source_sha256': meta['source_sha256'], 'observations': provenance,
        'fresh_tpu_calls': 0, 'fresh_nn_calls': 0, 'argus_snapshot': receipt['source_commit'],
        'application_database_write': False, 'live_end_to_end': False,
        'origin': 'MIXED_SAVED_TPU_AND_LOCAL_REPLAY' if history else 'SAVED_LOCAL_REPLAY',
        'neural_missing_indices': [i for i in range(len(rows)) if i not in {r['frame_index'] for r in selected}],
        'no_interpolation': True, 'preprocessing_equals_current_argus': all(
            p['preprocessing'] == 'OPENCV_INTER_LINEAR_RGB_LETTERBOX_PAD114_FLOAT32_DIVIDE_255'
            for p in provenance),
        'events_are_predictions_not_gt': True})
    report = {'status': 'PASS_ISOLATED_ARGUS_REPLAY', 'source_scene': str(scene),
        'source_sha256': meta['source_sha256'], 'frames': len(selected), 'original_frames': len(rows),
        'episodes': len(result.episodes), 'episodes_by_scenario': {s: sum(e.scenario == s for e in result.episodes) for s in sorted({e.scenario for e in result.episodes})},
        'argus_scenarios': [m.model_dump(mode='json') for m in rules.scenario_metas(config.active_classes)],
        'argus_snapshot_commit': receipt['source_commit'], 'cache_review': cache_review,
        'source_pts_preserved': True, 'argus_rule_time_rounding_ms': 'Python round(original_pts_ms)',
        'zones': 'NONE_NO_INVENTED_SITE_POLICY', 'calibration': 'NONE',
        'live_end_to_end': False, 'app_db_or_ui_verified': False,
        'historical_capture': str(historical) if historical else None,
        'saved_tpu_tail_and_argus_postprocess_calls': len(decoder_proof),
        'event_quality': 'NOT_MEASURED_NO_EXHAUSTIVE_TARGET_GT'}
    write_json(output / 'replay_report.json', report)
    print(json.dumps({k: report[k] for k in ['status', 'frames', 'episodes', 'episodes_by_scenario']}, ensure_ascii=False))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scene', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--argus-snapshot', required=True, type=Path)
    parser.add_argument('--historical-capture', type=Path)
    parser.add_argument('--decode-tpu-with-argus', action='store_true')
    args = parser.parse_args()
    replay(args.scene, args.output, args.argus_snapshot, args.historical_capture, args.decode_tpu_with_argus)


if __name__ == '__main__':
    main()
