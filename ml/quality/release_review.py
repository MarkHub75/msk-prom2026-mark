"""Local evidence ledger for a frozen ML checkpoint; never promotes a model.

No training, inference, network calls or credential files are used. A valid hash
and a historical status-0 capture do not imply independent model quality or new
Matvey placement. Unknown qualification formats require human/scientific review.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
from uuid import UUID

from ml.pipeline.capture_review import review_capture
from ml.pipeline.capture_recovery import save_json


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def regular_owned_file(path, root):
    path, root = Path(path), Path(root).resolve()
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root):
        raise ValueError('artifact missing, symlinked or outside approved local root')
    # Do not silently follow a symlinked directory to an alternate artifact.
    if path.absolute() != path.resolve():
        raise ValueError('noncanonical artifact path')
    return path


def check_artifact(spec, root):
    expected = spec.get('sha256')
    if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
        raise ValueError('exact file SHA256 required')
    path = regular_owned_file(spec['path'], root)
    if 'bytes' in spec and (type(spec['bytes']) is not int or spec['bytes'] != path.stat().st_size):
        raise ValueError('artifact byte count mismatch')
    if digest(path) != expected:
        raise ValueError('artifact checksum mismatch')
    return {'sha256': expected, 'bytes': path.stat().st_size}


def check_runtime(model, root):
    location = Path(model['actual_linq']['initial_capture'])
    capture = json.loads(regular_owned_file(location / 'capture.json', root).read_text())
    response = json.loads(regular_owned_file(location / 'response.json', root).read_text())
    request = response.get('request_id')
    if not isinstance(request, str) or str(UUID(request)) != request:
        raise ValueError('canonical captured request UUID required')
    if (type(response.get('status_code')) is not int or response['status_code'] != 0
            or response.get('response_id') != request or response.get('status') != 'completed'
            or response.get('remote_completion') != 'response_received'
            or capture.get('status') != 'completed' or capture.get('model_id') != model['model_id']
            or capture.get('journal_request_id') != request):
        raise ValueError('correlated historical completion evidence required')
    for name in ('inputs.npz', 'outputs.npz'):
        regular_owned_file(location / name, root)
    result = review_capture(location, expected_program_sha256=model['artifacts']['tpu']['sha256'])
    if result.get('status') != 'CAPTURE_INTEGRITY_VALID':
        raise ValueError('capture integrity review failed')
    return {'request_id': request, 'status_code': 0, 'integrity': result['status'],
            'hardware_attestation': 'NOT_ESTABLISHED_BY_LOCAL_REVIEW',
            'scope': 'HISTORICAL_EXECUTION_ONLY_NOT_QUALITY_OR_NEW_PLACEMENT'}


def review(manifest_path, *, project_root='/workspace/project', artifacts_root='/workspace/artifacts'):
    project, artifacts = Path(project_root).resolve(), Path(artifacts_root).resolve()
    path = regular_owned_file(manifest_path, project)
    manifest = json.loads(path.read_text())
    checks, errors = {}, []
    def run(key, fn):
        try:
            checks[key] = {'status': 'PASS', 'evidence': fn()}
        except Exception as error:
            # Paths/content/worker error text may contain private data; report only type.
            checks[key] = {'status': 'FAIL', 'error_type': type(error).__name__}
            errors.append(key)

    models = manifest.get('models', [])
    if not models or len({m.get('model_id') for m in models}) != len(models):
        errors.append('unique_models_required')
    for model in models:
        identity = model['model_id']
        for kind in ('weights', 'onnx', 'tpu', 'export_manifest'):
            run(identity + ':' + kind, lambda m=model, k=kind: check_artifact(m['artifacts'][k], artifacts))
        run(identity + ':historical_runtime', lambda m=model: check_runtime(m, artifacts))
    for index, candidate in enumerate(manifest.get('candidates', [])):
        run('retained_candidate:' + str(index), lambda c=candidate: check_artifact(
            {'path': c['program'], 'sha256': c['program_sha256'], **({'bytes': c['bytes']} if 'bytes' in c else {})}, artifacts))
    for name, expected in manifest.get('components', {}).items():
        def component(n=name, sha=expected):
            p = Path(n)
            if p.is_absolute() or p.parts[0] not in ('ml', 'scripts'):
                raise ValueError('component outside ML code scope')
            return check_artifact({'path': str(project / p), 'sha256': sha}, project)
        run('component:' + name, component)

    # These gates are intentionally distinct from byte integrity and software tests.
    # The checkpoint format has no independent-evaluation acceptance object. Never
    # upgrade it based on free-text stage labels or a test count.
    gates = {
        'independent_quality': {'status': 'BLOCKED', 'reason': 'NO_REVIEWED_INDEPENDENT_ACCEPTANCE_IN_CHECKPOINT_FORMAT',
                                'declared_final_test': manifest.get('final_test_status', 'UNKNOWN')},
        'new_matvey_placement': {'status': 'NOT_VERIFIED',
                                 'reason': 'HISTORICAL_CAPTURE_DOES_NOT_ATTEST_NEW_NAMESPACE'},
        'external_backup': {'status': 'DECLARED_VERIFIED_NOT_RECHECKED' if manifest.get('off_vast_backup', {}).get('external_copy_verified') is True else 'NOT_VERIFIED',
                             'scope': 'manifest declaration only; no remote storage contacted'},
    }
    if any(m.get('new_remote_placement_verified') is True for m in models):
        # No future placement evidence can be guessed from a boolean alone.
        gates['new_matvey_placement']['status'] = 'REQUIRES_EVIDENCE_REVIEW'
    return {'schema_version': 'mosprom-ml-checkpoint-review-v1', 'manifest_sha256': digest(path),
            'reviewer_sha256': digest(Path(__file__).resolve()),
            'integrity_status': 'PASS' if not errors else 'FAIL', 'failed_checks': errors,
            'checks': checks, 'gates': gates, 'quality_release': 'NOT_QUALIFIED',
            'new_neural_calls': 0, 'new_remote_calls': 0,
            'scope': 'local checkpoint integrity and evidence ledger; no automatic promotion'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', default='/workspace/project/ml/RELEASE_MANIFEST.json')
    parser.add_argument('--output', required=True, help='new outside-Git report file; existing evidence is not overwritten')
    parser.add_argument('--integrity-only', action='store_true', help='exit0 on byte/runtime integrity, retaining blocked quality gates')
    args = parser.parse_args()
    output = Path(args.output)
    if not output.resolve().is_relative_to(Path('/workspace/artifacts')):
        parser.error('review outputs must remain under /workspace/artifacts, outside Git')
    if output.exists():
        parser.error('use a new output file; existing review must not be overwritten')
    output.parent.mkdir(parents=True, exist_ok=True)
    result = review(args.manifest)
    save_json(output, result)
    print(json.dumps({key: result[key] for key in ('integrity_status', 'quality_release', 'new_neural_calls', 'new_remote_calls')}))
    return 1 if result['integrity_status'] != 'PASS' else (0 if args.integrity_only else 2)


if __name__ == '__main__':
    raise SystemExit(main())
