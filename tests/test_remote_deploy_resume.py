import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from uuid import uuid4

import numpy as np
from ml.linq.amqp import AmqpError
from ml.linq.journal import RequestJournal
from ml.linq.notebook import capture_call
from ml.pipeline import remote_deploy as module


class DeploymentResumeTest(unittest.TestCase):
    def test_recovery_latency_is_not_reported_as_original_roundtrip(self):
        self.assertEqual(module.response_latency({'timings': {'total_ms': 120}}),
            {'roundtrip_ms': 120, 'recovery_ms': None, 'latency_kind': 'full_amqp_call'})
        self.assertEqual(module.response_latency({'reconcile_only': True, 'timings': {'total_ms': 2}}),
            {'roundtrip_ms': None, 'recovery_ms': 2, 'latency_kind': 'recovery_only'})

    def test_durable_terminal_reply_resumes_offline_and_rejects_changed_context(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            program = root / 'fixture.tpu'
            program.write_bytes(b'fixture')
            directory = root / 'linq-rpc/helmet-001'
            inputs = {'images': np.ones((1, 2), np.float32)}
            def interrupted(values):
                raise ConnectionError('fixture')
            capture = capture_call(interrupted, inputs=inputs, output_names=['output0'],
                program_path=program, output_dir=directory, model_id='helmet-v1')
            store = RequestJournal(root / 'linq-rpc/requests')
            request_id = str(uuid4())
            store.create(request_id, purpose='inference', program_uri_sha256='0' * 64,
                inputs=inputs, output_names=['output0'], capture_dir=directory,
                capture_id=capture['capture_id'])
            store.update(request_id, 'SUBMITTING')
            store.complete(request_id, {'output0': np.ones((1, 1), np.float32)},
                status_code=0, response_id=request_id)
            (directory / 'request-pointer.json').write_text(json.dumps({
                'schema_version': '1.0', 'journal_request_id': request_id,
                'journal_path': str(store.path(request_id)), 'purpose': 'inference'}))
            with patch.object(module, 'ARTIFACTS', root), patch.object(module, '_environment_parameters') as credentials:
                with store.lock(request_id):
                    with self.assertRaises(BlockingIOError):
                        module.resume_operation(directory, 'inference', ['output0'], 60)
                values, response = module.resume_operation(directory, 'inference', ['output0'], 60)
                self.assertEqual(response['response_id'], request_id)
                self.assertTrue(response['cached_response'])
                np.testing.assert_equal(values['output0'], [[1]])
                credentials.assert_not_called()
                capture['capture_id'] = str(uuid4())
                (directory / 'capture.json').write_text(json.dumps(capture))
                with self.assertRaisesRegex(ValueError, 'original durable request'):
                    module.resume_operation(directory, 'inference', ['output0'], 60)

    def fixture(self, root):
        blob = b"reviewed local fixture"
        sha = hashlib.sha256(blob).hexdigest()
        compiled = root / "linq-sdk/helmet-compile"
        compiled.mkdir(parents=True)
        (compiled / "model.tpu").write_bytes(blob)
        (compiled / "compile-report.json").write_text(json.dumps({"outputs": [{"name": "output0"}]}))
        stock = root / "linq-rpc/resnet50-001"
        stock.mkdir(parents=True)
        (stock / "resnet-check.json").write_text(json.dumps({"status": "PASS", "status_code": 0}))
        capture = root / "linq-rpc/helmet-001"
        capture.mkdir()
        (capture / "capture.json").write_text(json.dumps({
            "model_id": "helmet-v1", "program": {"sha256": sha}, "status": "completed"}))
        (capture / "response.json").write_text('{}')
        return blob, sha, capture

    def test_completed_model_uses_local_result_without_credentials_or_network(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, sha, _ = self.fixture(root)
            with patch.object(module, "ARTIFACTS", root), patch.dict(module.PROFILES, {"helmet": ("helmet-v1", "helmet-v1.tpu", sha)}), patch.object(module, "verify_model", return_value={"status": "PASS"}), patch.object(module, "_environment_parameters") as credentials, patch.object(module, "upload_program") as upload, patch.object(module, "amqp_main") as publish:
                self.assertEqual(module.run("helmet", root / "missing-bridge"), 0)
                credentials.assert_not_called()
                upload.assert_not_called()
                publish.assert_not_called()

    def test_unknown_request_only_reconciles_and_cannot_publish_again(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, sha, capture = self.fixture(root)
            report = json.loads((capture / "capture.json").read_text())
            report["status"] = "failed"
            (capture / "capture.json").write_text(json.dumps(report))
            with patch.object(module, "ARTIFACTS", root), patch.dict(module.PROFILES, {"helmet": ("helmet-v1", "helmet-v1.tpu", sha)}), patch.object(module, "resume_operation", side_effect=AmqpError("response_timeout", "reconcile")) as receive, patch.object(module, "upload_program") as upload, patch.object(module, "amqp_main") as publish:
                with self.assertRaises(AmqpError):
                    module.run("helmet", root / "missing-bridge")
                receive.assert_called_once_with(capture, "inference", ["output0"], 60)
                upload.assert_not_called()
                publish.assert_not_called()
                self.assertTrue(capture.exists())

    def test_upload_receipt_recovered_without_second_upload(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            blob, sha, _ = self.fixture(root)
            state = root / "linq-rpc/helmet"
            state.mkdir()
            (state / "request-pointer.json").write_text("{}")
            result = {"sha256": np.frombuffer(bytes.fromhex(sha), np.uint8),
                      "byte_count": np.array([len(blob)], np.int64)}
            response = {"request_id": str(uuid4()), "remote_completion": "response_received"}
            with patch.object(module, "ARTIFACTS", root), patch.dict(module.PROFILES, {"helmet": ("helmet-v1", "helmet-v1.tpu", sha)}), patch.object(module, "resume_operation", return_value=(result, response)), patch.object(module, "_submit_upload") as submit:
                receipt = module.upload_program("helmet", {})
                self.assertEqual(receipt["upload_request_id"], response["request_id"])
                submit.assert_not_called()

    def test_legacy_ambiguous_upload_requires_manual_completion_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, sha, _ = self.fixture(root)
            state = root / "linq-rpc/helmet"
            state.mkdir()
            (state / "upload-response.json").write_text(json.dumps({"publish_attempted": True}))
            with patch.object(module, "ARTIFACTS", root), patch.dict(module.PROFILES, {"helmet": ("helmet-v1", "helmet-v1.tpu", sha)}), patch.object(module, "_submit_upload") as submit:
                with self.assertRaisesRegex(ValueError, "legacy upload"):
                    module.upload_program("helmet", {})
                submit.assert_not_called()
