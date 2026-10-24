import copy
import unittest

from ml.scene_packs import validate_records


class ScenePackValidationTests(unittest.TestCase):
    def setUp(self):
        self.meta = {'original_frames': 2, 'processed_frames': 2, 'device': 'cuda:0',
                     'model_specs': [{'model_id': 'pose-split-v1', 'class_map': {'0': 'person'},
                                      'source_class_map': {'0': 'person'}}]}
        self.rows = []
        for index, pts in enumerate([39.028, 79.028]):
            self.rows.append({'frame_index': index, 'original_pts_ms': pts, 'image_size': [320, 240],
                'backend': 'PYTORCH_CUDA', 'models': [{'model_id': 'pose-split-v1', 'detections': [{
                    'class_id': 0, 'class_name': 'person', 'source_class_name': 'person',
                    'confidence': .7, 'bbox_xyxy': [10, 20, 100, 200],
                    'pose_coco17': [[50, 60, .8] for _ in range(17)]}]}]})

    def validate(self):
        validate_records(self.meta, self.rows)

    def test_nonzero_original_pts_origin_preserved(self):
        self.validate()
        self.assertEqual(self.rows[0]['original_pts_ms'], 39.028)

    def test_missing_frame_is_not_complete_scene(self):
        self.rows.pop()
        with self.assertRaisesRegex(ValueError, 'frame census'):
            self.validate()

    def test_duplicate_frame_or_pts_rejected(self):
        for key in ('frame_index', 'original_pts_ms'):
            rows = copy.deepcopy(self.rows)
            rows[1][key] = rows[0][key]
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'chronological'):
                validate_records(self.meta, rows)

    def test_boolean_frame_index_is_not_original_ordinal_zero(self):
        self.rows[0]['frame_index'] = False
        with self.assertRaisesRegex(ValueError, 'chronological'):
            self.validate()

    def test_gpu_rows_cannot_claim_linq(self):
        self.rows[0]['backend'] = 'linq'
        with self.assertRaisesRegex(ValueError, 'provenance'):
            self.validate()

    def test_missing_model_result_is_not_a_processed_frame_for_all_models(self):
        self.rows[0]['models'] = []
        with self.assertRaisesRegex(ValueError, 'model census'):
            self.validate()

    def test_empty_detections_are_still_real_processed_observations(self):
        self.rows[0]['models'][0]['detections'] = []
        self.validate()

    def test_product_class_alias_requires_consistent_numeric_id(self):
        self.rows[0]['models'][0]['detections'][0]['class_name'] = 'truck'
        with self.assertRaisesRegex(ValueError, 'class mapping'):
            self.validate()

    def test_pose_or_box_corruption_rejected(self):
        for change in [{'pose_coco17': [[0, 0, .8]] * 16}, {'bbox_xyxy': [0, 0, 400, 300]},
                       {'confidence': float('nan')}]:
            rows = copy.deepcopy(self.rows)
            rows[0]['models'][0]['detections'][0].update(change)
            with self.subTest(change=list(change)), self.assertRaises(ValueError):
                validate_records(self.meta, rows)
