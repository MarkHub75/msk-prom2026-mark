"""Prepare an isolated, leakage-checked PTQ candidate; never promotes a model.

Input JSON has samples [{path, sha256, source_group, source_sha256, split}],
reserved_groups and reserved_source_sha256 arrays covering validation AND test.
Each path is an already reviewed, inference-preprocessed named numeric NPZ.
This provenance declaration cannot independently establish the truth of a split.
No SDK import or model execution occurs unless --compile is explicitly supplied.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from .compile import sha256


def prepare_candidate(onnx, model_manifest, calibration_manifest, output_dir,
                      *, max_samples=64):
    """Validate all inputs before creating a fresh directory or allocating corpus."""
    out = Path(output_dir)
    if out.exists():
        raise ValueError('candidate output must not exist; baseline reuse forbidden')
    if not 1 <= max_samples <= 128:
        raise ValueError('bounded sample budget must be 1..128')
    manifest_path = Path(calibration_manifest)
    data = json.loads(manifest_path.read_text())
    model = json.loads(Path(model_manifest).read_text())
    if sha256(onnx) != model['artifacts']['onnx']['sha256']:
        raise ValueError('ONNX hash differs from reviewed export manifest')
    samples = data['samples']
    if not isinstance(samples, list) or not 1 <= len(samples) <= max_samples:
        raise ValueError('calibration corpus outside approved sample budget')
    reserved = set(data['reserved_groups'])
    reserved_hashes = set(data['reserved_source_sha256'])
    spec = model['input']
    if len(spec['shape']) != 4 or spec['shape'][:2] != [1, 3] or spec.get('layout', 'NCHW') != 'NCHW':
        raise ValueError('candidate preparation requires reviewed batch-one RGB NCHW model')
    arrays, seen, sample_statistics = [], set(), []
    channel_sum = np.zeros(3, dtype=np.float64)
    channel_square_sum = np.zeros(3, dtype=np.float64)
    for sample in samples:
        if sample['split'] not in ('train', 'calibration'):
            raise ValueError('validation/test/unspecified data forbidden for calibration')
        group, source_hash = sample['source_group'], sample['source_sha256']
        if not isinstance(group, str) or not group or group in reserved:
            raise ValueError('missing or reserved source group')
        if (not isinstance(source_hash, str) or len(source_hash) != 64 or
                any(c not in '0123456789abcdef' for c in source_hash) or
                source_hash in reserved_hashes):
            raise ValueError('invalid or reserved source hash')
        path = Path(sample['path'])
        if not path.is_absolute():
            path = manifest_path.parent / path
        digest = sha256(path)
        if digest != sample['sha256'] or digest in seen:
            raise ValueError('sample hash mismatch or exact duplicate calibration tensor')
        seen.add(digest)
        with np.load(path, allow_pickle=False) as archive:
            if archive.files != [spec['name']]:
                raise ValueError('sample must contain exactly the named model input')
            value = archive[spec['name']]
            if (list(value.shape) != spec['shape'] or
                    value.dtype != np.dtype(spec['dtype']) or
                    not np.isfinite(value).all()):
                raise ValueError('sample shape/dtype/nonfinite mismatch')
            if value.min() < 0 or value.max() > 1:
                raise ValueError('reviewed RGB /255 input range must be 0..1')
            channel_sum += value.sum(axis=(0, 2, 3), dtype=np.float64)
            channel_square_sum += np.square(value, dtype=np.float64).sum(axis=(0, 2, 3))
            sample_statistics.append({'source_group': group, 'tensor_sha256': digest,
                                      'min': float(value.min()), 'max': float(value.max()),
                                      'mean': float(value.mean(dtype=np.float64))})
            arrays.append(np.ascontiguousarray(value))
    corpus = np.concatenate(arrays, axis=0)
    out.mkdir(parents=True, exist_ok=False)
    np.savez(out / 'calibration.npz', **{spec['name']: corpus})
    pixels_per_channel = corpus.shape[0] * corpus.shape[2] * corpus.shape[3]
    channel_mean = channel_sum / pixels_per_channel
    channel_std = np.sqrt(np.maximum(channel_square_sum / pixels_per_channel - channel_mean ** 2, 0))
    report = {
        'status': 'PREPARED_NOT_COMPILED', 'model_id': model['model_id'],
        'source_onnx_sha256': sha256(onnx),
        'model_manifest_sha256': sha256(model_manifest),
        'calibration_manifest_sha256': sha256(calibration_manifest),
        'calibration_sha256': sha256(out / 'calibration.npz'),
        'sample_count': len(samples), 'source_group_count': len({s['source_group'] for s in samples}),
        'tensor_bytes': int(corpus.nbytes),
        'calibration_statistics': {'channel_order': 'RGB', 'channel_mean': channel_mean.tolist(),
                                   'channel_std': channel_std.tolist(), 'samples': sample_statistics,
                                   'interpretation': 'numeric coverage only; no labels/task-quality metrics'},
        'split_verification': 'DECLARED_GROUP_AND_SOURCE_HASH_DISJOINT',
        'near_duplicate_review': data.get('near_duplicate_review', 'NOT_PROVIDED'),
        'quantization_options': 'existing compile_model calibrate_torch defaults; no percentile sweep',
        'linq_status': 'NOT_RUN', 'quality_status': 'NOT_EVALUATED',
        'promotion': 'FORBIDDEN_WITHOUT_PAIRED_INDEPENDENT_QUALITY_AND_LINQ_PASS',
    }
    (out / 'candidate.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--onnx', required=True)
    parser.add_argument('--model-manifest', required=True)
    parser.add_argument('--calibration-manifest', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--max-samples', type=int, default=64)
    parser.add_argument('--compile', action='store_true', help='only after explicit resource allocation')
    args = parser.parse_args()
    report = prepare_candidate(args.onnx, args.model_manifest, args.calibration_manifest,
                               args.output, max_samples=args.max_samples)
    if args.compile:
        from .compile import compile_model
        result = compile_model(args.onnx, Path(args.output) / 'calibration.npz',
                               Path(args.output) / 'compile', report['model_id'], 'O1')
        report['compile_status'] = result['compile_status']
    print(json.dumps(report, indent=2))
    if report.get('compile_status') == 'FAIL':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
