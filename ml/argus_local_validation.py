"""Real local-ONNX job through frozen Argus, in a new isolated app directory.

No source patches, fake inference, external artifacts injected into the cache,
network listeners, remote TPU calls, or writes to the captain's application.
"""
import argparse
import asyncio
import json
import os
from pathlib import Path
import shutil
import sys
import time

from ml.argus_replay import digest, write_json
from ml.pipeline.video_clock import FilePTS


async def run(root, output_name, source_override=None, source_sha256=None, broadcast_seconds=None):
    import yaml
    root = Path(root).resolve()
    if not root.is_relative_to(Path('/workspace/artifacts')):
        raise ValueError('isolated local test must be outside Git')
    original = root / 'argus_snapshot_f6b5358a'
    receipt = json.loads((original / 'MATVEY_SNAPSHOT.json').read_text())
    if not output_name.replace('_', '').isalnum():
        raise ValueError('simple output directory name required')
    app = root / output_name
    app.mkdir(exist_ok=False)
    for rel, expected in receipt['files'].items():
        source, target = original / rel, app / rel
        if digest(source) != expected:
            raise ValueError('frozen application snapshot changed')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    with (app / 'config/models.yaml').open() as stream:
        registry = yaml.safe_load(stream)
    additions = yaml.safe_load((root / 'models/matvey_registry_additions.local.yaml').read_text())['models']
    existing = {(m['id'], m['version']) for m in registry['models']}
    if any((m['id'], m['version']) in existing for m in additions):
        raise ValueError('model ref collision')
    registry['models'].extend(additions)
    (app / 'config/models.yaml').write_text(yaml.safe_dump(registry, sort_keys=False))
    override = yaml.safe_load((root / 'models/matvey_pipeline.local.yaml').read_text())
    override |= {'data_dir': str(app / 'app_data'), 'local': {'threads': 1},
                 'broadcast': {'autostart': False, 'loop_default': False}, 'delivery': {'webhooks': []}}
    (app / 'config/user.yaml').write_text(yaml.safe_dump(override, sort_keys=False))
    # Unpack only expected model files from the previously verified model kit.
    import tarfile
    with tarfile.open(root / 'models/matvey_safewatch_delivery_v2.tar.gz') as archive:
        for member in archive.getmembers():
            name = Path(member.name)
            if name.is_absolute() or '..' in name.parts or member.issym() or member.islnk():
                raise ValueError('unexpected model archive path')
        archive.extractall(app, filter='data')
    for source in (root / 'models/coco_reference').rglob('*'):
        if source.is_file():
            target = app / source.relative_to(root / 'models/coco_reference')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    metadata = json.loads((root / 'models/MODEL_REGISTRY.json').read_text())
    for record in metadata['models']:
        model = record['model']
        for field in ['local_onnx', 'linq_tail']:
            rel = model.get(field)
            if not rel or (app / rel).exists():
                continue
            item = next(f for f in record['files'] if Path(f['path']).name == Path(rel).name)
            model_source = Path(item['path'])
            if not model_source.is_file() and item.get('bundle_relative_path'):
                model_source = root / item['bundle_relative_path']
            if digest(model_source) != item['sha256']:
                raise ValueError('registered model bytes differ')
            target = app / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(model_source, target)
    # The kit also contains registry templates; restore the deliberately local-only config.
    (app / 'config/models.yaml').write_text(yaml.safe_dump(registry, sort_keys=False))
    (app / 'config/user.yaml').write_text(yaml.safe_dump(override, sort_keys=False))
    os.environ['INFERENCE_BACKEND'], os.environ['SAFEWATCH_FAKE'] = 'local', '0'
    sys.path.insert(0, str(app / 'src'))
    from safewatch import config, services, store
    from safewatch.types import SectorIn, CameraIn, BroadcastIn
    import cv2
    cv2.setNumThreads(1)
    settings = config.get_settings()
    if settings.inference_backend != 'local' or settings.fake or settings.data_dir != app / 'app_data' or settings.delivery.webhooks:
        raise ValueError('local job isolation failed')
    sector = services.sector_create(SectorIn(name='Matvey isolated ML validation'), 'admin')
    source = Path(source_override) if source_override else root / 'scenes/S01_3_tr45/original.mp4'
    expected_source = source_sha256 if source_override else '2020127242e62532028e5f2a4947d0611c97dd0b7f68b5c52e8fe813b07e0dbf'
    camera = services.camera_create(CameraIn(sector_id=sector.id, name=source.stem[:70] + ' replay'), 'admin')
    if digest(source) != expected_source:
        raise ValueError('source identity mismatch')
    started = time.perf_counter()
    imported = services.video_import(camera.id, source)
    job = await services.run_next_job()
    if job is None or job.status != 'done':
        write_json(app / 'failed_job.json', None if job is None else job.model_dump(mode='json'))
        raise ValueError('actual local Argus job failed; see failed_job.json')
    wall = time.perf_counter() - started
    write_json(app / 'job.json', job.model_dump(mode='json'))
    analysis = services.video_analysis(imported.video.id)
    write_json(app / 'analysis.json', analysis.model_dump(mode='json'))
    episodes = [dict(r) for r in store.all('SELECT * FROM episodes')]
    evidence = [dict(r) for r in store.all('SELECT * FROM evidence')]
    artifacts = [dict(r) for r in store.all('SELECT * FROM artifacts')]
    source_clock = FilePTS(source)
    summaries, model_calls = [], 0
    for artifact in artifacts:
        file = settings.data_dir / artifact['path']
        rows = [json.loads(x) for x in file.read_text().splitlines()]
        for row in rows:
            if abs(row['ts_ms'] - source_clock.at(row['frame_idx'])) > .051:
                raise ValueError('actual app PTS differ from original encoded PTS')
        summary = json.loads(file.with_suffix('.summary.json').read_text())
        summaries.append({'model_id': artifact['model_id'], 'model_version': artifact['model_version'],
            'file': str(file.relative_to(app)), 'sha256': digest(file), 'summary': summary,
            'processed_frame_indices': [r['frame_idx'] for r in rows],
            'missing_frame_indices': [i for i in range(len(source_clock.times)) if i not in {r['frame_idx'] for r in rows}]})
        model_calls += len(rows)
    # A regular finite broadcast advances on the real clock; no clock mock.
    services.broadcast_start(camera.id, BroadcastIn(video_id=imported.video.id, loop=False), 'admin')
    start_broadcast = time.perf_counter()
    playback_seconds = broadcast_seconds if broadcast_seconds is not None else len(source_clock.times) * .001 * (source_clock.times[1] - source_clock.times[0]) + .2
    if not 0 < playback_seconds <= 60:
        raise ValueError('bounded local broadcast must be at most60seconds')
    while time.perf_counter() - start_broadcast < playback_seconds:
        services.broadcast_tick()
        await asyncio.sleep(.05)
    services.broadcast_tick()
    events = [dict(r) for r in store.all('SELECT * FROM events')]
    details = [services.event_detail(e['id'], 'operator').model_dump(mode='json') for e in events]
    for ev in evidence:
        if digest(settings.data_dir / ev['path']) != ev['sha256']:
            raise ValueError('persisted evidence hash differs')
    write_json(app / 'events.json', events)
    write_json(app / 'event_details.json', details)
    write_json(app / 'episodes.json', episodes)
    write_json(app / 'evidence.json', evidence)
    write_json(app / 'artifacts.json', summaries)
    # In-process ASGI requests use the actual routes, with no server/listener or lifespan worker.
    import httpx
    from safewatch.api import create_app
    responses = []
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=create_app(settings)), base_url='http://isolated-argus') as client:
        for endpoint in ['/api/events'] + ['/api/events/' + str(e['id']) for e in events]:
            response = await client.get(endpoint, headers={'X-Role': 'operator'})
            responses.append({'path': endpoint, 'status_code': response.status_code, 'body': response.json()})
            if response.status_code != 200:
                raise ValueError('actual Argus event API read failed')
    write_json(app / 'api_readbacks.json', responses)
    # Verify no application code or default rules changed during the test.
    unchanged = {rel: expected for rel, expected in receipt['files'].items() if rel not in {'config/models.yaml'}}
    if any(digest(app / rel) != expected for rel, expected in unchanged.items()):
        raise ValueError('frozen code/default rule file changed')
    report = {'status': 'PASS_REAL_LOCAL_ARGUS_JOB', 'argus_revision': receipt['source_commit'],
        'source_sha256': expected_source, 'source_frames': len(source_clock.times), 'model_calls': model_calls,
        'backend': 'ONNXRUNTIME_CPU', 'fake': False, 'gpu_calls': 0, 'tpu_calls': 0,
        'original_pts_verified': True, 'app_job_wall_seconds': wall,
        'neural_frame_census_by_model': summaries, 'episodes': len(episodes), 'events': len(events),
        'evidence': len(evidence), 'event_api_readbacks': 'PASS', 'ui_visual_test': 'NOT_RUN',
        'production_application_modified': False, 'external_artifacts_injected': False,
        'source_patches': 0, 'network_listeners': 0, 'external_delivery_channels': 0,
        'gt_event_metrics': 'NOT_MEASURED', 'event_predictions_are_not_verified_violations': True,
        'database': str(settings.data_dir / 'safewatch.db'),
        'only_changed_application_files': ['config/models.yaml (append)', 'config/user.yaml (new isolated config)']}
    store.conn().execute('PRAGMA wal_checkpoint(TRUNCATE)')
    store.conn().close()
    write_json(app / 'validation.json', report)
    print(json.dumps({k: report[k] for k in ['status', 'model_calls', 'episodes', 'events', 'evidence', 'app_job_wall_seconds']}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default='/workspace/artifacts/matvey-final-20261025')
    parser.add_argument('--output-name', default='local_app_validation_v1')
    parser.add_argument('--source', type=Path)
    parser.add_argument('--source-sha256')
    parser.add_argument('--broadcast-seconds', type=float)
    args = parser.parse_args()
    if bool(args.source) != bool(args.source_sha256):
        parser.error('explicit source requires its pinned SHA256')
    asyncio.run(run(args.root, args.output_name, args.source, args.source_sha256, args.broadcast_seconds))


if __name__ == '__main__':
    main()
