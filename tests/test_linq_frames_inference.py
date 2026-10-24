import hashlib
from dataclasses import asdict
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from uuid import uuid4

import numpy as np

from ml.linq_frames import preflight_manifest, run, load_completed_result
from ml.linq.journal import RequestJournal, tensor_metadata
from ml.detection import preprocess, decode
from ml.video_handoff import model_detection


class UploadStore:
    def __init__(self, record, outputs):
        self.record, self.arrays = record, outputs

    def load(self, request_id):
        return self.record

    def outputs(self, request_id):
        return self.arrays


class LinqFramesInferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.program = self.root / 'matvey_fixture.tpu'
        self.program.write_bytes(b'not executable; tests never submit')
        self.sha = hashlib.sha256(self.program.read_bytes()).hexdigest()
        self.uid = str(uuid4())
        self.receipt = {'status': 'STAGED', 'namespace_owner': 'matvey', 'model_id': 'fixture-v1',
                        'program_name': 'matvey_fixture.tpu', 'program_sha256': self.sha,
                        'bytes': self.program.stat().st_size, 'program_path_namespace_verified': True,
                        'remote_completion': 'response_received', 'upload_request_id': self.uid}
        self.receipt_path = self.root / 'receipt.json'
        self.receipt_path.write_text(json.dumps(self.receipt))
        self.manifest = {'model_id': 'fixture-v1', 'linq': {'program_name': 'matvey_fixture.tpu',
                         'program_sha256': self.sha, 'program_path': str(self.program), 'runtime_abi_verified': True},
                         'matvey_staging_receipt': str(self.receipt_path)}
        self.path = self.root / 'manifest.json'
        self.path.write_text(json.dumps(self.manifest))
        (self.root / 'fixture-verified.json').write_text(json.dumps(self.manifest))
        baseline = patch('ml.linq_frames.BASELINE', self.root)
        baseline.start()
        self.addCleanup(baseline.stop)
        self.profile = patch.dict('ml.linq_frames.PROFILES', {'fixture-v1': ('fixture', 'matvey_fixture.tpu', self.sha)})
        self.profile.start()
        self.addCleanup(self.profile.stop)
        self.record = {'state': 'COMPLETED', 'purpose': 'model_upload', 'status_code': 0,
                       'response_id': self.uid, 'reply_queue': 'matvey_reply_' + self.uid}
        self.outputs = {'sha256': np.frombuffer(bytes.fromhex(self.sha), np.uint8),
                        'byte_count': np.array([self.program.stat().st_size], np.int64)}

    def preflight(self):
        with patch('ml.linq_frames.RequestJournal', return_value=UploadStore(self.record, self.outputs)):
            return preflight_manifest(self.path, upload_journal=self.root)

    def test_numeric_own_upload_proof_required_and_accepted(self):
        self.assertEqual(self.preflight()['model_id'], 'fixture-v1')

    def test_legacy_name_rejected_before_upload_or_runner(self):
        self.manifest['linq']['program_name'] = 'fixture-v1.tpu'
        self.path.write_text(json.dumps(self.manifest))
        with patch('ml.linq_frames.RequestJournal') as store, self.assertRaises(ValueError):
            preflight_manifest(self.path)
        store.assert_not_called()

    def test_missing_receipt_rejected_without_remote_client(self):
        self.receipt_path.unlink()
        with patch('ml.linq_frames.DurableVideoRunner') as runner, self.assertRaisesRegex(ValueError, 'receipt missing'):
            preflight_manifest(self.path)
        runner.assert_not_called()

    def test_changed_tensor_abi_rejected_before_upload_or_runner(self):
        self.manifest['linq']['outputs'] = [{'name': 'unreviewed', 'shape': [1], 'dtype': 'float32'}]
        self.path.write_text(json.dumps(self.manifest))
        with patch('ml.linq_frames.RequestJournal') as store, self.assertRaisesRegex(ValueError, 'tensor ABI'):
            preflight_manifest(self.path)
        store.assert_not_called()

    def test_forged_staging_boolean_cannot_replace_numeric_upload_digest(self):
        self.outputs['sha256'] = np.zeros(32, np.uint8)
        with self.assertRaisesRegex(ValueError, 'hash/byte-count'):
            self.preflight()

    def test_unknown_upload_or_uncorrelated_receipt_blocks_inference(self):
        for change in [{'state': 'UNKNOWN'}, {'response_id': str(uuid4())}, {'status_code': False},
                       {'reply_queue': 'notebook_legacy'}]:
            original = self.record.copy()
            self.record.update(change)
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, 'correlated'):
                self.preflight()
            self.record = original

    def test_bound_is_checked_before_reading_source_or_submitting(self):
        with patch('ml.linq_frames.DurableVideoRunner') as runner, self.assertRaisesRegex(ValueError, 'maximum24'):
            run(self.root / 'absent.mp4', '0' * 64, ['a', 'b'], list(range(13)), self.root / 'out')
        runner.assert_not_called()

    def cached_fixture(self):
        manifest = dict(self.manifest, input={'shape': [1, 3, 8, 8], 'layout': 'NCHW', 'dtype': 'float32'},
                        decoder='detect_v8', classes=['helmet', 'bare_head'])
        tensor, transform = preprocess(np.zeros((8, 8, 3), np.uint8), manifest)
        arrays = {'output0': np.array([[[4], [4], [4], [4], [.8], [.1]]], np.float32)}
        logical_id = 'fixture-source:0:fixture-v1'
        context = self.root / 'rpc/fixture-v1' / hashlib.sha256(logical_id.encode()).hexdigest()
        context.mkdir(parents=True)
        store = RequestJournal(self.root / 'requests')
        store.create(self.uid, purpose='inference', program_uri_sha256='0' * 64,
                     inputs={'images': tensor}, output_names=['output0'])
        store.update(self.uid, 'SUBMITTING')
        store.complete(self.uid, arrays, status_code=0, response_id=self.uid)
        (context / 'request-pointer.json').write_text(json.dumps({'journal_request_id': self.uid}))
        (context / 'logical.json').write_text(json.dumps({'model_id': 'fixture-v1',
            'program_sha256': self.sha, 'logical_request_id': logical_id,
            'inputs': tensor_metadata({'images': tensor})}))
        value = {'model_id': 'fixture-v1', 'program_sha256': self.sha,
                 'original_transform': asdict(transform), 'transport_provenance': {'request_id': self.uid},
                 'detections': [model_detection(d, manifest['classes']) for d in decode(arrays, manifest, transform)]}
        path = self.root / 'frame.json'
        path.write_text(json.dumps({'source_rgb_sha256': 'f' * 64, 'result': value}))
        return path, manifest, tensor, transform, logical_id, value

    def test_completed_result_revalidated_from_numeric_journal_without_runner(self):
        path, manifest, tensor, transform, logical_id, value = self.cached_fixture()
        with patch('ml.linq_frames.DurableVideoRunner') as runner:
            self.assertEqual(load_completed_result(path, manifest, tensor, transform, 'f' * 64,
                                                   logical_id, self.root), value)
        runner.assert_not_called()

    def test_tampered_cached_confidence_rejected_instead_of_reused(self):
        path, manifest, tensor, transform, logical_id, value = self.cached_fixture()
        value['detections'][0]['confidence'] = .99
        path.write_text(json.dumps({'source_rgb_sha256': 'f' * 64, 'result': value}))
        with self.assertRaisesRegex(ValueError, 'differ from completed'):
            load_completed_result(path, manifest, tensor, transform, 'f' * 64, logical_id, self.root)
