"""Read-only numeric baseline audit. No inference, SDK import, broker or credentials.

Run with --artifacts /workspace/artifacts --output <fresh audit.json>.
Saved simulation is compared only when its reference tensors are available.
Metrics are numerical diagnostics, never precision/recall or labelled quality.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from .compile import sha256


def load_arrays(path):
    with np.load(path, allow_pickle=False) as data:
        result = {key: data[key] for key in data.files}
    if not result or any(x.dtype.kind not in 'fiu' or not np.isfinite(x).all() for x in result.values()):
        raise ValueError('expected finite named numeric arrays')
    return result


def tensor_summary(arrays):
    return {key: {'shape': list(value.shape), 'dtype': str(value.dtype),
                  'min': float(value.min()), 'max': float(value.max())}
            for key, value in arrays.items()}


def compare_arrays(reference, actual):
    if set(reference) != set(actual):
        raise ValueError('exact output names required; no shape-based renaming')
    result = {}
    for key, ref in reference.items():
        value = actual[key]
        if ref.shape != value.shape or ref.dtype != value.dtype:
            raise ValueError('shape/dtype mismatch')
        delta = np.abs(value.astype(np.float64) - ref.astype(np.float64))
        result[key] = {'mean_abs_diff': float(delta.mean()), 'max_abs_diff': float(delta.max()),
                       'exact_equal': bool(np.array_equal(ref, value))}
    return result


def pose_scores(arrays):
    cls = arrays['/model.22/Sigmoid_output_0'].reshape(-1)
    kpt = arrays['/model.22/Sigmoid_1_output_0'][0, :, 0, :]
    index = int(cls.argmax())
    return {'person_max': float(cls[index]), 'person_anchors_ge_025': int((cls >= .25).sum()),
            'person_anchors_ge_05': int((cls >= .5).sum()), 'top_person_anchor': index,
            'top_anchor_keypoints_ge_05': int((kpt[:, index] >= .5).sum()),
            'top_anchor_keypoint_confidences': kpt[:, index].tolist(),
            'global_keypoint_max': float(kpt.max()), 'global_keypoint_min': float(kpt.min())}


def audit(artifacts):
    root = Path(artifacts)
    result = {'scope': 'saved numeric evidence only; no labelled task-quality claim',
              'baseline': {}, 'industrial': []}
    for model in ('helmet', 'pose-split'):
        folder = root / 'detection' / model
        manifest = json.loads((folder / 'manifest.json').read_text())
        compiled = root / 'linq-sdk' / (model + '-compile')
        report = json.loads((compiled / 'compile-report.json').read_text())
        hashes = {name: sha256(folder / name) for name in ('weights.pt', 'weights.onnx')}
        hashes['model.tpu'] = sha256(compiled / 'model.tpu')
        expected = {'weights.pt': manifest['artifacts']['weights']['sha256'],
                    'weights.onnx': manifest['artifacts']['onnx']['sha256'],
                    'model.tpu': report['program_sha256']}
        if hashes != expected:
            raise ValueError('baseline artifact hash drift')
        calibration = root / 'linq-sdk' / 'calibration-smoke.npz'
        if sha256(calibration) != report['calibration_sha256']:
            raise ValueError('baseline calibration hash drift')
        capture = root / 'linq-rpc' / (model + '-001')
        result['baseline'][model] = {
            'hashes': hashes, 'model_id': manifest['model_id'],
            'compiler_artifact_sha256': {name: sha256(compiled / name) for name in
                ('optimized.onnx', 'quantized.qm.onnx', 'thresholds.json', 'scales.json', 'compile-report.json')},
            'input': manifest['input'], 'outputs': report['outputs'],
            'preprocessing': 'RGB, bilinear letterbox 114, NCHW float32 /255; inverse original transform once',
            'thresholds': manifest['thresholds'], 'compile_preset': report['preset'],
            'compile_target': report['target'], 'calibration_sha256': sha256(calibration),
            'calibration': tensor_summary(load_arrays(calibration)),
            'calibration_independence': 'NOT_VERIFIED_ONE_BUS_IMAGE',
            'hardware_capture_sha256': sha256(capture / 'outputs.npz'),
            'hardware_outputs': tensor_summary(load_arrays(capture / 'outputs.npz')),
        }
        if model == 'pose-split':
            result['baseline'][model]['bus_pose_scores'] = pose_scores(load_arrays(capture / 'outputs.npz'))
            bus = compiled / 'simulation'
            result['baseline'][model]['bus_native_pose_scores'] = pose_scores(load_arrays(bus / 'simulation-reference.npz'))
            result['baseline'][model]['bus_simulation_pose_scores'] = pose_scores(load_arrays(bus / 'simulation-output.npz'))
    for run in ('industrial-001', 'industrial-002'):
        for path in sorted((root / 'video-mvp' / run / 'requests').glob('*/request.json')):
            journal = json.loads(path.read_text())
            if journal.get('state') != 'COMPLETED':
                continue
            outputs = load_arrays(path.parent / 'response.npz')
            entry = {'run': run, 'request_id': path.parent.name,
                     'input_sha256': sha256(path.parent / 'inputs.npz'),
                     'response_sha256': sha256(path.parent / 'response.npz'),
                     'status_code': journal['status_code'], 'outputs': tensor_summary(outputs)}
            if '/model.22/Sigmoid_output_0' in outputs:
                entry['pose_scores'] = pose_scores(outputs)
                sim = root / 'quality' / 'linq' / 'numerical-audit' / path.parent.name
                if (sim / 'simulation-reference.npz').exists():
                    reference = load_arrays(sim / 'simulation-reference.npz')
                    quantized = load_arrays(sim / 'simulation-output.npz')
                    entry['native_pose_scores'] = pose_scores(reference)
                    entry['simulation_pose_scores'] = pose_scores(quantized)
                    entry['native_vs_hardware'] = compare_arrays(reference, outputs)
                    entry['native_vs_simulation'] = compare_arrays(reference, quantized)
                    entry['simulation_vs_hardware'] = compare_arrays(quantized, outputs)
                    boxes = '/model.22/Mul_2_output_0'
                    scores = '/model.22/Sigmoid_output_0'
                    selected = (reference[scores][0, 0] >= .25) | (quantized[scores][0, 0] >= .25)
                    delta = np.abs(quantized[boxes] - outputs[boxes])
                    entry['simulation_vs_hardware_boxes'] = {
                        'differing_elements': int((delta > 0).sum()),
                        'selected_anchor_definition': 'union of native/simulated class score >=0.25; no NMS or GT',
                        'selected_anchor_count': int(selected.sum()),
                        'selected_anchor_max_abs_diff': float(delta[:, :, selected].max()) if selected.any() else None,
                    }
            result['industrial'].append(entry)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifacts', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    report = audit(args.artifacts)
    with Path(args.output).open('x') as file:
        json.dump(report, file, indent=2)
        file.write('\n')


if __name__ == '__main__':
    main()
