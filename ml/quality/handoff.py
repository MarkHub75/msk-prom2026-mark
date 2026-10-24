"""Verify an immutable, scoped dataset handoff before any model experiment.

This is consumer-side integrity/role verification, not a substitute for the Data
Orchestrator's source/label/rights audit. READY for annotation does not imply
READY for event-quality measurement, training or independent final evaluation.
"""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

SCHEMA = 'mosprom-dataset-handoff-v1'
SPLITS = {'train', 'calibration', 'validation', 'development', 'test', 'quarantine'}
DEFAULT_ROOTS = ('/workspace/datasets', '/workspace/artifacts',
                 '/workspace/project/Deep-Research', '/workspace/agents/data-audit/docs/data-audit')


class HandoffError(ValueError):
    pass


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _digest(value):
    return isinstance(value, str) and len(value)==64 and all(c in '0123456789abcdef' for c in value)


def verify_manifest(manifest, *, allowed_roots=DEFAULT_ROOTS):
    if manifest.get('schema_version') != SCHEMA or manifest.get('status') != 'READY':
        raise HandoffError('dataset snapshot must have supported schema and explicit READY')
    if not isinstance(manifest.get('version'), str) or not manifest['version']:
        raise HandoffError('immutable dataset version required')
    if not manifest.get('producer') or not manifest.get('consumer_verification_scope'):
        raise HandoffError('producer identity and consumer verification boundary required')
    roots = [Path(p).resolve() for p in allowed_roots]
    datasets = manifest.get('datasets', [])
    if not datasets or len({d['dataset_id'] for d in datasets}) != len(datasets):
        raise HandoffError('unique nonempty dataset inventory required')
    groups, sources = {}, {}
    for dataset in datasets:
        if (dataset.get('split') not in SPLITS or not dataset.get('rights_scope')
                or not dataset.get('annotation_scope') or not dataset.get('capabilities')):
            raise HandoffError('explicit split, rights, annotation scope and capabilities required')
        if dataset['split']=='quarantine' and set(dataset['capabilities'])-{'metadata_inspection'}:
            raise HandoffError('quarantined media cannot be used for a model experiment')
        assets = dataset.get('assets')
        if not isinstance(assets, list) or not assets:
            raise HandoffError('asset census required')
        seen = set()
        for asset in assets:
            path = Path(asset.get('path', ''))
            if not path.is_absolute() or not _digest(asset.get('sha256')) or type(asset.get('bytes')) is not int:
                raise HandoffError('absolute path, exact bytes and SHA256 required')
            resolved = path.resolve()
            if not any(resolved.is_relative_to(root) for root in roots):
                raise HandoffError('asset outside approved data/provenance roots')
            if str(resolved) in seen:
                raise HandoffError('duplicate asset path')
            seen.add(str(resolved))
            before = path.stat()
            if not path.is_file() or before.st_size != asset['bytes'] or sha256(path) != asset['sha256']:
                raise HandoffError('asset bytes or SHA256 changed')
            after = path.stat()
            if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
                raise HandoffError('asset changed during verification')
            # Metadata/annotation files may legitimately describe several splits.
            if asset.get('role') in ('media', 'calibration_tensor'):
                group = asset.get('group_id')
                if not isinstance(group, str) or not group:
                    raise HandoffError('source group required for model inputs')
                for mapping, key in ((groups, group), (sources, asset['sha256'])):
                    if key in mapping and mapping[key] != dataset['split']:
                        raise HandoffError('source or group leaks across declared splits')
                    mapping[key] = dataset['split']
    return manifest


def load_ready(path, *, dataset_id, capability, allow_test=False, allowed_roots=DEFAULT_ROOTS):
    manifest = json.loads(Path(path).read_text())
    verify_manifest(manifest, allowed_roots=allowed_roots)
    found = [d for d in manifest['datasets'] if d['dataset_id']==dataset_id]
    if len(found)!=1 or capability not in found[0]['capabilities']:
        raise HandoffError('requested dataset capability is not READY')
    dataset = found[0]
    if dataset['split']=='test' and capability not in ('annotation', 'metadata_inspection') and not allow_test:
        raise HandoffError('sealed final test requires explicit final-evaluation gate')
    return manifest, dataset


def publish_snapshot(manifest, destination, *, allowed_roots=DEFAULT_ROOTS):
    """Publish only verified READY bytes; never overwrite another producer."""
    value = deepcopy(manifest)
    verify_manifest(value, allowed_roots=allowed_roots)
    value['consumer_verified_utc'] = datetime.now(timezone.utc).isoformat()
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation prevents silently replacing a producer's active version.
    with target.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')
    return value


def load_producer_ready(pointer, *, dataset_id, allowed_use,
                        releases_root='/workspace/datasets/research/releases'):
    """Consume the Data Orchestrator's existing release schema without rewriting it.

    The exact allowed-use string is mandatory. A research/import release cannot
    silently become training, independent validation or exhaustive event GT.
    """
    pointer = Path(pointer)
    catalog = json.loads(pointer.read_text())
    if catalog.get('schema_version') != 'dataset-handoff-v1':
        raise HandoffError('unsupported producer handoff schema')
    rows = [d for d in catalog.get('datasets', []) if d.get('dataset_id')==dataset_id]
    if len(rows)!=1 or rows[0].get('status')!='READY':
        raise HandoffError('producer dataset is not READY')
    entry=rows[0]
    root=Path(entry['absolute_path']).resolve()
    if not root.is_relative_to(Path(releases_root).resolve()):
        raise HandoffError('producer release outside approved immutable root')
    manifest_path=Path(entry['manifest_path'])
    if manifest_path.resolve()!=root/'manifest.json' or sha256(manifest_path)!=entry['manifest_sha256']:
        raise HandoffError('producer manifest checksum or location changed')
    manifest=json.loads(manifest_path.read_text())
    if (manifest.get('schema_version')!='dataset-release-v1' or manifest.get('status')!='READY'
            or manifest.get('immutable') is not True or manifest.get('dataset_id')!=dataset_id
            or manifest.get('version')!=entry['version']):
        raise HandoffError('producer release identity/immutability mismatch')
    if allowed_use not in entry.get('allowed_uses',[]) or allowed_use not in manifest.get('allowed_uses',[]):
        raise HandoffError('requested use is not approved by producer')
    for relative,spec in manifest.get('files',{}).items():
        path=root/relative
        if (not path.resolve().is_relative_to(root) or path.stat().st_size!=spec['bytes']
                or sha256(path)!=spec['sha256']):
            raise HandoffError('producer asset checksum/path changed')
    for key,name in [('class_map_path','class_map.json'),('split_manifest_path','split_manifest.json')]:
        if Path(entry[key]).resolve()!=root/name or name not in manifest['files']:
            raise HandoffError('producer class/split metadata not pinned')
    # The checksums registry is itself derived; compare to manifest-pinned records.
    if json.loads(Path(entry['checksums_path']).read_text())!=manifest['files']:
        raise HandoffError('producer checksum registry differs from pinned manifest')
    return manifest, {'pointer_sha256':sha256(pointer),'manifest_sha256':entry['manifest_sha256'],
                      'allowed_use':allowed_use,'verification':'READ_ONLY_HASH_AND_SCOPE_VALIDATION'}
