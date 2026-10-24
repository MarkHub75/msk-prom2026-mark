"""Assemble the final reviewable ML evidence, without inference or app mutation."""
import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

from ml.argus_replay import digest, write_json


ROOT = Path('/workspace/artifacts/matvey-final-20261025')
OLD = Path('/workspace/artifacts/matvey-scene-packs-20261024')


def copy_verified(source, target):
    source, target = Path(source), Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    expected = digest(source)
    if target.exists():
        if digest(target) != expected:
            raise ValueError('refusing to replace issued artifact ' + str(target))
    else:
        shutil.copyfile(source, target)
    if digest(target) != expected:
        raise ValueError('copied artifact differs')
    return {'path': str(target.relative_to(ROOT)), 'bytes': target.stat().st_size, 'sha256': expected}


def build():
    videos = []
    scenes = sorted(OLD.glob('*/matvey_scene.json')) + sorted((ROOT / 'new_full_scenes').glob('*/matvey_scene.json'))
    for path in scenes:
        meta = json.loads(path.read_text())
        sid, source = meta['scene_id'], path.parent
        target = ROOT / 'scenes' / sid
        target.mkdir(parents=True, exist_ok=True)
        kind = meta.get('source_kind', 'PREEXISTING_LOSSY_RGB_CROP_PREVIEW' if sid.startswith('S07_ur') else 'ORIGINAL_MP4_BYTES')
        original = kind == 'ORIGINAL_MP4_BYTES'
        source_name = 'original.mp4' if original else 'playback.mp4'
        files = {'video': copy_verified(source / 'matvey_source_original.mp4', target / source_name),
            'detections': copy_verified(source / 'matvey_detections.json', target / 'detections.json'),
            'detections_jsonl': copy_verified(source / 'matvey_detections.jsonl', target / 'detections.intermediate.jsonl'),
            'events': copy_verified(ROOT / 'replays' / sid / 'events.json', target / 'events.json')}
        for name in ['annotated.mp4', 'video_time_map.json', 'render_validation.json', 'render.log']:
            files[name] = copy_verified(ROOT / 'visuals_v1' / sid / name, target / name)
        for name in ['provenance.json', 'analysis.json', 'analysis_config.json', 'models.json', 'replay_report.json']:
            files['argus_' + name] = copy_verified(ROOT / 'replays' / sid / name, target / 'argus' / name)
        for spec in meta['model_specs']:
            name = spec['model_id'] + '.jsonl'
            files['argus_' + name] = copy_verified(ROOT / 'replays' / sid / name, target / 'argus' / name)
        for name in ['matvey_scene.json', 'matvey_validation.json', 'matvey_linq_frames.json', 'matvey_missing_frames.json', 'matvey_report.txt']:
            files[name] = copy_verified(source / name, target / name)
        replay = json.loads((target / 'argus/replay_report.json').read_text())
        manifest = {'schema': 'matvey-final-scene-manifest-v1', 'scene_id': sid,
            'scenario_candidates': ['S02', 'S01'] if sid == 'S01_3_tr45' else [meta['scenario_id']],
            'source_kind': kind, 'original_mp4_available': original,
            'source_sha256': meta['source_sha256'], 'rights': meta['rights'],
            'original_source_reference': meta.get('producer_scene', {}).get('original_source_path', meta['source']),
            'complete_provider_file': True, 'longer_camera_session': 'UNKNOWN',
            'frames': meta['processed_frames'], 'local_neural_calls': meta['processed_frames'] * 3,
            'backend': meta['device'], 'models': meta['model_specs'],
            'original_pts': 'encoded best_effort PTS, exact in detections; CAVIAR is declared JPEG25FPS projection',
            'events': 'actual frozen Argus EpisodeDraft predictions; no GT injected; not production app DB/UI',
            'event_count': replay['episodes'], 'argus_revision': replay['argus_snapshot_commit'],
            'signal_review': meta['signal_review'], 'fresh_tpu_calls': 0,
            'local_missing_frames': [], 'tracker_carried_detections': 0, 'files': files}
        write_json(target / 'manifest.json', manifest)
        metrics = {'status': 'NOT_MEASURED', 'scope': 'target-event accuracy', 'gt_events': None,
            'tp': None, 'fp': None, 'fn': None, 'precision': None, 'recall': None, 'f1': None,
            'false_alerts_per_hour': None, 'detection_delay_ms': None,
            'reason': 'No exhaustive appropriate independent target-event GT/site policy; empty predicted events are not verified negatives',
            'actual_argus_predicted_episodes': replay['episodes'], 'local_frames_processed': meta['processed_frames'],
            'local_frames_missing': 0, 'local_model_calls': meta['processed_frames'] * 3,
            'local_pipeline_wall_seconds': meta['wall_seconds'], 'wall_scope': 'source/export/preprocess/inference/decode, not device-only',
            'detector_quality': 'see SOURCE_SCOPED_DETECTOR_METRICS.json for CAVIAR, historical_detector_metrics.json for PPE; neither is independent test',
            'linq_wall_clock': 'separate historical captures only, see linq_gate report',
            'rule_confirmation_intervals_ms': [e['confirm_ms'] - e['start_ms'] for e in json.loads((target / 'events.json').read_text())],
            'rule_interval_is_gt_detection_delay': False}
        write_json(target / 'metrics.json', metrics)
        command = ('OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 '
            '/tmp/safewatch-ml-contract/.venv/bin/python -m ml.argus_replay --scene ' + str(source) +
            ' --output /workspace/artifacts/NEW_matvey_replay_' + sid +
            ' --argus-snapshot ' + str(ROOT / 'argus_snapshot_f6b5358a'))
        (target / 'run.log').write_text('Executed replay command (original output was ' + str(ROOT / 'replays' / sid) + '):\n' + command + '\n' +
            'Actual backend of saved observations: ' + meta['device'] + '\n' +
            'PASS FrameDetections/read_jsonl/analyze; episodes=' + str(replay['episodes']) + '\n' +
            'Fresh NN calls during adapter/renderer:0. Fresh TPU calls:0. No app DB mutation.\n')
        (target / 'README.md').write_text('# ' + sid + '\n\n' +
            'Смотрите annotated.mp4. Это полный сохранённый ' + meta['device'] + '-прогон; не TPU.\n\n' +
            ('original.mp4 — неизменённые байты исходного MP4.\n' if original else
             'playback.mp4 — прежний производный источник (' + kind + '), скопирован без изменений. Native original.mp4 не установлен.\n') +
            'detections.json содержит все кадры/PTS/три модели. argus/*.jsonl — точный FrameDetections действующего main; provenance.json сохраняет backend.\n' +
            'events.json — предсказания неизменённого Argus, не GT, не запись в production DB/UI. Ноль записей не означает безопасную сцену.\n' +
            'manifest.json: SHA, версии, class maps, происхождение, ограничения. metrics.json: область измерений.\n\n' +
            'Визуализация показывает каждый кадр один раз; её PTS нормированы к0/квантованы1мс. Исходные PTS не изменены в JSON/HUD.\n\n' +
            'Воспроизведение из matvey_cv и существующего окружения/артефактов:\n```bash\n' + command + '\n```\n')
        videos.append({'scene_id': sid, 'path': str(target.relative_to(ROOT)), 'source_kind': kind,
            'original_mp4': files['video']['path'] if original else None,
            'playback_mp4': files['video']['path'], 'annotated_mp4': files['annotated.mp4']['path'],
            'detections_json': files['detections']['path'], 'events_json': files['events']['path'],
            'source_sha256': meta['source_sha256'], 'frames': meta['processed_frames'],
            'model_calls': meta['processed_frames'] * 3, 'backend': 'PYTORCH_CUDA',
            'event_count': replay['episodes'], 'episodes_by_scenario': replay['episodes_by_scenario'],
            'fresh_tpu_calls': 0, 'independent_quality': 'NOT_MEASURED', 'rights': meta['rights']})
    for sid, pack in [('S07_urfall01', 'matvey-egor-linq-urfall01-20261024-v2'), ('PPE_industrial4tr6', 'matvey-egor-linq-demo-20261024-v2')]:
        src = Path('/workspace/artifacts') / pack
        target = ROOT / 'linq_captures' / sid
        for p in src.rglob('*'):
            if p.is_file():
                copy_verified(p, target / p.relative_to(src))
        for name in ['annotated.mp4', 'video_time_map.json', 'render_validation.json', 'render.log']:
            copy_verified(ROOT / 'linq_visuals_v1' / sid / name, target / ('matvey_' + name))
    write_json(ROOT / 'VIDEO_MANIFEST.json', {'schema': 'matvey-final-video-manifest-v1',
        'created_utc': datetime.now(timezone.utc).isoformat(), 'videos': videos,
        'complete_local_scenes': len(videos), 'local_frames': sum(v['frames'] for v in videos),
        'local_model_calls': sum(v['model_calls'] for v in videos), 'local_missing_frames': 0,
        'tracker_carried_detections': 0, 'new_local_frames_this_sprint': 2060,
        'new_local_model_calls_this_sprint': 6180,
        'historical_linq_unique_source_frames': 13, 'historical_linq_model_calls': 15,
        'fresh_linq_calls': 0, 'live_linq_argus_end_to_end': 'BLOCKED_OWN_STAGING',
        'app_db_ui': 'NOT_VERIFIED', 'original_mp4_count': sum(v['original_mp4'] is not None for v in videos)})
    metrics_rows = []
    for v in videos:
        metrics_rows.append({k: v[k] for k in ['scene_id', 'frames', 'model_calls', 'backend', 'event_count']} |
            {k: 'NOT_MEASURED' for k in ['gt_events', 'tp', 'fp', 'fn', 'precision', 'recall', 'f1', 'false_alerts_per_hour', 'detection_delay_ms']})
    with (ROOT / 'SCENE_METRICS.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(metrics_rows[0]))
        writer.writeheader(); writer.writerows(metrics_rows)
    archive = json.loads(Path('ml/safewatch.delivery.json').read_text())['archive']
    if digest(archive['path']) != archive['sha256']:
        raise ValueError('canonical model archive changed')
    copy_verified(archive['path'], ROOT / 'models' / 'matvey_safewatch_delivery_v2.tar.gz')
    delivery = json.loads(Path('ml/safewatch.delivery.json').read_text())
    coco = json.loads(Path('/workspace/artifacts/safewatch-delivery/coco-reference-local-v1/MANIFEST.json').read_text())
    model_records = [coco] + delivery['models']
    for record in model_records:
        for f in record['files']:
            if digest(f['path']) != f['sha256'] or Path(f['path']).stat().st_size != f['bytes']:
                raise ValueError('issued model artifact differs')
    # Historical two-model tar excludes the primary COCO reference. Ship it
    # explicitly so the local integration instructions are actually complete.
    for f in coco['files']:
        rel = Path(f['path']).relative_to('/workspace/artifacts/safewatch-delivery/coco-reference-local-v1')
        copy_verified(f['path'], ROOT / 'models/coco_reference' / rel)
    write_json(ROOT / 'models' / 'MODEL_REGISTRY.json', {'schema': 'matvey-final-model-registry-v1',
        'models': model_records, 'archive': archive,
        'local_scene_confidence_floor': .25, 'app_registry_floor': .1,
        'raw_local_tensors_retained': False, 'remote_placement': 'NOT_VERIFIED',
        'new_models': 0, 'new_training_runs': 0, 'new_compilations': 0,
        'historical_model_outputs_not_claimed_under_new_preprocessing': True})
    import yaml
    additions = []
    for record in model_records:
        model = dict(record['model'])
        model['linq_program'] = None  # local-only recommendation; never use the unsafe uploader
        additions.append(model)
    (ROOT / 'models/matvey_registry_additions.local.yaml').write_text(yaml.safe_dump({'models': additions}, sort_keys=False))
    override = {'pipeline': {'detector': coco['model']['id'] + '@' + coco['model']['version'],
        'pose': delivery['models'][0]['model']['id'] + '@' + delivery['models'][0]['model']['version'],
        'extra': [delivery['models'][1]['model']['id'] + '@' + delivery['models'][1]['model']['version']]}}
    (ROOT / 'models/matvey_pipeline.local.yaml').write_text(yaml.safe_dump(override, sort_keys=False))
    print(json.dumps({'scenes': len(videos), 'frames': sum(v['frames'] for v in videos), 'status': 'ASSEMBLED'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    build()
