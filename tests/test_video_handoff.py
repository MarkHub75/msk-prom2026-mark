import copy
import unittest

from ml.video_handoff import model_detection, verified_completed_request


class FakeJournal:
    def __init__(self, record):
        self.record = record

    def load(self, request_id):
        return self.record

    def outputs(self, request_id):
        return {'selected_numeric_tensor': 'fixture only'}


class VideoHandoffTests(unittest.TestCase):
    def setUp(self):
        self.uid = '6691fdc1-af48-4a67-b2c3-d7a9b0a943b9'
        self.record = {'state': 'COMPLETED', 'purpose': 'inference', 'status_code': 0,
                       'response_id': self.uid}
        self.execution = {'status': 'ok', 'backend': 'linq', 'transport_provenance': {
            'response_id': self.uid, 'status_code': 0, 'remote_completion': 'response_received'}}

    def test_completed_correlated_capture_can_be_exported(self):
        record, outputs = verified_completed_request(FakeJournal(self.record), self.uid, self.execution)
        self.assertEqual(record, self.record)
        self.assertIn('selected_numeric_tensor', outputs)

    def test_unknown_failure_and_boolean_status_never_become_tpu_success(self):
        for key, value in [('state', 'UNKNOWN'), ('purpose', 'model_upload'), ('status_code', False),
                           ('status_code', 1), ('response_id', 'different')]:
            record = dict(self.record, **{key: value})
            with self.subTest(key=key, value=value), self.assertRaisesRegex(ValueError, 'correlated'):
                verified_completed_request(FakeJournal(record), self.uid, self.execution)

    def test_uncorrelated_observation_cannot_borrow_a_valid_capture(self):
        execution = copy.deepcopy(self.execution)
        execution['transport_provenance']['response_id'] = 'different'
        with self.assertRaisesRegex(ValueError, 'correlated'):
            verified_completed_request(FakeJournal(self.record), self.uid, execution)

    def test_boolean_observation_status_is_not_integer_zero(self):
        execution = copy.deepcopy(self.execution)
        execution['transport_provenance']['status_code'] = False
        with self.assertRaisesRegex(ValueError, 'correlated'):
            verified_completed_request(FakeJournal(self.record), self.uid, execution)

    def test_product_class_alias_preserves_source_label_and_numeric_id(self):
        detection = {'class_name': 'bare_head', 'score': .33, 'bbox_xyxy': [0, 1, 2, 3], 'keypoints': None}
        mapped = model_detection(detection, ['helmet', 'bare_head'])
        self.assertEqual(mapped['class_id'], 1)
        self.assertEqual(mapped['class_name'], 'no_helmet')
        self.assertEqual(mapped['source_class_name'], 'bare_head')
        self.assertEqual(mapped['bbox_xyxy'], detection['bbox_xyxy'])
