import json
from pathlib import Path
import tempfile
import unittest
import numpy as np

from ml.linq.candidate import prepare_candidate
from ml.linq.compile import sha256
from ml.linq.quality_audit import compare_arrays, load_arrays, pose_scores, helmet_comparison
from ml.linq.simulate import simulate


class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.onnx = self.root / 'model.onnx'
        self.onnx.write_bytes(b'reviewed-export-fixture-not-real-model')
        self.model = self.root / 'model.json'
        self.model.write_text(json.dumps({'model_id': 'fixture', 'input': {
            'name': 'images', 'dtype': 'float32', 'shape': [1, 3, 2, 2]},
            'artifacts': {'onnx': {'sha256': sha256(self.onnx)}}}))
        sample = self.root / 'sample.npz'
        np.savez(sample, images=np.ones((1, 3, 2, 2), dtype=np.float32))
        self.data = {'reserved_groups': ['test-camera'], 'reserved_source_sha256': ['b' * 64],
                     'samples': [{'path': 'sample.npz', 'sha256': sha256(sample),
                                  'source_group': 'train-camera', 'source_sha256': 'a' * 64,
                                  'split': 'calibration'}]}
        self.manifest = self.root / 'calibration.json'

    def run_prepare(self):
        self.manifest.write_text(json.dumps(self.data))
        return prepare_candidate(self.onnx, self.model, self.manifest, self.root / 'candidate')

    def test_prepare_numeric_corpus_without_compiling(self):
        result = self.run_prepare()
        self.assertEqual(result['linq_status'], 'NOT_RUN')
        self.assertEqual(result['status'], 'PREPARED_NOT_COMPILED')
        self.assertEqual(result['tensor_bytes'], 48)
        self.assertEqual(result['calibration_statistics']['channel_mean'], [1, 1, 1])
        self.assertEqual(result['calibration_statistics']['channel_std'], [0, 0, 0])
        self.assertFalse((self.root / 'candidate' / 'model.tpu').exists())

    def test_reserved_group_and_source_are_rejected_before_writes(self):
        for key, value in [('source_group', 'test-camera'), ('source_sha256', 'b' * 64)]:
            original = self.data['samples'][0][key]
            self.data['samples'][0][key] = value
            with self.assertRaises(ValueError): self.run_prepare()
            self.assertFalse((self.root / 'candidate').exists())
            self.data['samples'][0][key] = original

    def test_holdout_and_duplicate_are_rejected(self):
        self.data['samples'][0]['split'] = 'val'
        with self.assertRaises(ValueError): self.run_prepare()
        self.data['samples'][0]['split'] = 'train'
        self.data['samples'].append(dict(self.data['samples'][0]))
        with self.assertRaises(ValueError): self.run_prepare()

    def test_hash_drift_and_overwrite_rejected(self):
        self.onnx.write_bytes(b'drift')
        with self.assertRaises(ValueError): self.run_prepare()
        (self.root / 'candidate').mkdir()
        with self.assertRaises(ValueError): self.run_prepare()

    def test_numeric_nonfinite_and_wrong_names_rejected(self):
        for arrays in [{'images': np.full((1, 3, 2, 2), np.nan, np.float32)},
                       {'wrong': np.zeros((1, 3, 2, 2), np.float32)}]:
            np.savez(self.root / 'sample.npz', **arrays)
            self.data['samples'][0]['sha256'] = sha256(self.root / 'sample.npz')
            with self.assertRaises(ValueError): self.run_prepare()
            self.assertFalse((self.root / 'candidate').exists())


class NumericAuditTests(unittest.TestCase):
    def test_helmet_box_gate_excludes_unselected_background(self):
        reference = np.zeros((1, 6, 2), np.float32)
        actual = reference.copy()
        reference[0, 5, 0] = actual[0, 5, 0] = .6
        actual[0, 0, 1] = 20
        result = helmet_comparison({'output0': reference}, {'output0': actual})
        self.assertTrue(result['class_scores_exact_equal'])
        self.assertEqual(result['box_xywh_max_abs_input_pixels'], 20)
        self.assertEqual(result['selected_anchor_count'], 1)
        self.assertEqual(result['selected_box_xywh_max_abs_input_pixels'], 0)

    def test_simulation_rejects_unbounded_threads_before_sdk_import(self):
        for threads in (0, 5, True, 1.5):
            with self.assertRaises(ValueError):
                simulate('unused', 'unused', 'unused', 'unused', 'unused', num_threads=threads)

    def test_name_and_dtype_mismatch_cannot_be_inferred_from_shape(self):
        reference = {'a': np.zeros((1, 2), np.float32)}
        with self.assertRaises(ValueError): compare_arrays(reference, {'b': reference['a']})
        with self.assertRaises(ValueError): compare_arrays(reference, {'a': reference['a'].astype(np.float64)})
        self.assertTrue(compare_arrays(reference, reference)['a']['exact_equal'])

    def test_global_keypoint_max_does_not_establish_person_quality(self):
        result = pose_scores({'/model.22/Sigmoid_output_0': np.array([[[.1, .2]]], np.float32),
                              '/model.22/Sigmoid_1_output_0': np.array([[[[.99, .01]]]], np.float32)})
        self.assertEqual(result['person_anchors_ge_025'], 0)
        self.assertEqual(result['top_anchor_keypoints_ge_05'], 0)
        self.assertGreater(result['global_keypoint_max'], .98)

    def test_pickle_inputs_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'bad.npz'
            np.savez(path, secret=np.array([{}], dtype=object))
            with self.assertRaises(ValueError): load_arrays(path)


if __name__ == '__main__': unittest.main()
