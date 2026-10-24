import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from uuid import uuid4

from ml.quality import release_review as module


class CheckpointReviewTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.project = self.root / 'project'; self.project.mkdir()
        self.artifacts = self.root / 'artifacts'; self.artifacts.mkdir()
        self.capture = self.artifacts / 'capture'; self.capture.mkdir()
        self.request = str(uuid4())
        self.model = {'model_id': 'SYNTHETIC_TEST_FIXTURE_NOT_LINQ', 'artifacts': {},
                      'actual_linq': {'initial_capture': str(self.capture)}}
        for kind in ('weights', 'onnx', 'tpu', 'export_manifest'):
            p = self.artifacts / kind; p.write_bytes(b'non-neural-test-fixture')
            self.model['artifacts'][kind] = {'path': str(p), 'sha256': module.digest(p), 'bytes': p.stat().st_size}
        self.response = {'request_id': self.request, 'response_id': self.request, 'status': 'completed',
                         'status_code': 0, 'remote_completion': 'response_received'}
        self.captured = {'status': 'completed', 'model_id': self.model['model_id'], 'journal_request_id': self.request}
        for name in ('inputs.npz', 'outputs.npz'):
            (self.capture / name).write_bytes(b'not-a-real-capture-mocked-review-only')
        self.manifest = {'models': [self.model], 'components': {}, 'candidates': [],
                         'software_tests': {'last_completed': 999999, 'status': 'PASS'},
                         'final_test_status': 'NOT_RUN'}
        self.path = self.project / 'manifest.json'

    def run_review(self):
        (self.capture / 'capture.json').write_text(json.dumps(self.captured))
        (self.capture / 'response.json').write_text(json.dumps(self.response))
        self.path.write_text(json.dumps(self.manifest))
        with patch.object(module, 'review_capture', return_value={'status': 'CAPTURE_INTEGRITY_VALID'}):
            return module.review(self.path, project_root=self.project, artifacts_root=self.artifacts)

    def test_many_software_checks_and_matching_hashes_cannot_qualify_independent_quality(self):
        report = self.run_review()
        self.assertEqual(report['integrity_status'], 'PASS')
        self.assertEqual(report['quality_release'], 'NOT_QUALIFIED')
        self.assertEqual(report['gates']['independent_quality']['status'], 'BLOCKED')
        self.assertEqual(report['gates']['new_matvey_placement']['status'], 'NOT_VERIFIED')
        self.assertEqual(report['new_remote_calls'], 0)

    def test_tampered_selected_model_cannot_pass_even_with_good_runtime_record(self):
        Path(self.model['artifacts']['tpu']['path']).write_bytes(b'tampered')
        report = self.run_review()
        self.assertEqual(report['integrity_status'], 'FAIL')
        self.assertIn(self.model['model_id'] + ':tpu', report['failed_checks'])

    def test_symlink_escape_stops_before_reading_a_foreign_file(self):
        foreign = self.root / 'foreign-secret'; foreign.write_bytes(b'PRIVATE_FIXTURE')
        target = Path(self.model['artifacts']['weights']['path']); target.unlink(); target.symlink_to(foreign)
        report = self.run_review()
        self.assertEqual(report['integrity_status'], 'FAIL')
        self.assertNotIn('PRIVATE_FIXTURE', json.dumps(report))

    def test_bool_status_and_wrong_request_are_not_historical_success(self):
        self.response['status_code'] = False
        self.assertEqual(self.run_review()['integrity_status'], 'FAIL')
        self.response['status_code'] = 0; self.response['response_id'] = str(uuid4())
        self.assertEqual(self.run_review()['integrity_status'], 'FAIL')

    def test_component_change_is_not_hidden_by_unchanged_weights(self):
        code = self.project / 'ml' / 'fixture.py'; code.parent.mkdir(); code.write_text('before')
        self.manifest['components']['ml/fixture.py'] = module.digest(code)
        code.write_text('after')
        self.assertIn('component:ml/fixture.py', self.run_review()['failed_checks'])

    def test_placement_or_backup_boolean_cannot_become_verified_execution(self):
        self.model['new_remote_placement_verified'] = True
        self.manifest['off_vast_backup'] = {'external_copy_verified': True}
        report = self.run_review()
        self.assertEqual(report['quality_release'], 'NOT_QUALIFIED')
        self.assertEqual(report['gates']['new_matvey_placement']['status'], 'REQUIRES_EVIDENCE_REVIEW')
        self.assertEqual(report['gates']['external_backup']['status'], 'DECLARED_VERIFIED_NOT_RECHECKED')

    def test_corrupt_retained_candidate_is_reported_without_selecting_it(self):
        self.manifest['candidates'] = [{'program': str(self.artifacts / 'missing.tpu'), 'program_sha256': '0' * 64}]
        report = self.run_review()
        self.assertEqual(report['integrity_status'], 'FAIL')
        self.assertIn('retained_candidate:0', report['failed_checks'])
