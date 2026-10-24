import copy
import unittest

from ml.argus_replay import fingerprint, frame_record


class ArgusReplayTests(unittest.TestCase):
    def setUp(self):
        self.row = {'frame_index': 3, 'original_pts_ms': 39.028,
                    'image_size': [320, 240]}
        self.model = {'detections': [{'class_id': 0, 'class_name': 'person',
            'confidence': .7, 'bbox_xyxy': [1, 2, 30, 40],
            'pose_coco17': [[10, 20, .6] for _ in range(17)]}]}

    def test_numeric_values_and_nonzero_pts_preserved_without_mutating_input(self):
        before = copy.deepcopy(self.model)
        result = frame_record(self.row, self.model)
        self.assertEqual(result['ts_ms'], 39.028)
        self.assertEqual(result['frame_idx'], 3)
        self.assertEqual(result['detections'][0]['kpts'], self.model['detections'][0]['pose_coco17'])
        self.assertEqual(before, self.model)

    def test_empty_inferred_frame_remains_a_real_empty_record(self):
        self.assertEqual(frame_record(self.row, {'detections': []})['detections'], [])

    def test_bool_ordinal_and_nonfinite_pts_rejected(self):
        for value in [True, -1, 3.0]:
            with self.assertRaises(ValueError):
                frame_record(dict(self.row, frame_index=value), self.model)
        for value in [float('nan'), float('inf'), True, -1]:
            with self.assertRaises(ValueError):
                frame_record(dict(self.row, original_pts_ms=value), self.model)

    def test_corrupt_confidence_bbox_and_keypoints_rejected(self):
        for key, value in [('confidence', 1.01), ('confidence', True),
                           ('bbox_xyxy', [1, 2, 321, 40]),
                           ('pose_coco17', [[1, 2, .5]] * 16),
                           ('pose_coco17', [[1, 2, float('nan')]] * 17)]:
            model = copy.deepcopy(self.model)
            model['detections'][0][key] = value
            with self.assertRaises(ValueError):
                frame_record(self.row, model)

    def test_model_bytes_classes_threshold_preprocessing_and_backend_invalidate_identity(self):
        spec = {'weights_sha256': 'a' * 64, 'classes': {'0': 'person'},
                'thresholds': {'confidence': .25}}
        base = fingerprint(spec, 'PYTORCH_CUDA', 'PIL')
        for replacement in [dict(spec, weights_sha256='b' * 64),
                            dict(spec, classes={'0': 'helmet'}),
                            dict(spec, thresholds={'confidence': .1})]:
            self.assertNotEqual(base, fingerprint(replacement, 'PYTORCH_CUDA', 'PIL'))
        self.assertNotEqual(base, fingerprint(spec, 'LINQ_HISTORICAL_REAL_SERVICE_OUTPUTS', 'PIL'))
        self.assertNotEqual(base, fingerprint(spec, 'PYTORCH_CUDA', 'OPENCV'))


if __name__ == '__main__':
    unittest.main()
