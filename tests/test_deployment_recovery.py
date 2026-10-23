import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from uuid import uuid4

import numpy as np
from ml.linq.notebook import capture_call
from ml.pipeline.capture_recovery import complete_capture
from ml.pipeline.runtime_lock import deployment_lock


class DeploymentRecoveryTest(unittest.TestCase):
    def fixture(self, root):
        program = root / "fixture.tpu"
        program.write_bytes(b"not a hardware fixture")
        directory = root / "capture"
        def interrupted(inputs):
            raise ConnectionError("fixture connection lost")
        capture_call(interrupted, inputs={"images": np.ones((1, 2), np.float32)},
                     output_names=["output0"], program_path=program,
                     output_dir=directory, model_id="fixture")
        request_id = str(uuid4())
        (directory / "request-pointer.json").write_text(json.dumps({"journal_request_id": request_id}))
        response = {"request_id": request_id, "response_id": request_id,
                    "status_code": 0, "remote_completion": "response_received"}
        outputs = {"output0": np.array([[0.25, 0.75]], np.float32)}
        return directory, response, outputs

    def test_single_orchestrator_lock_released_on_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "deployment.lock"
            with self.assertRaisesRegex(ValueError, "fixture"):
                with deployment_lock(path):
                    with self.assertRaises(RuntimeError):
                        with deployment_lock(path):
                            self.fail("concurrent orchestrator acquired the lock")
                    raise ValueError("fixture")
            with deployment_lock(path):
                pass

    def test_reply_persisted_after_interruption_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory, response, outputs = self.fixture(Path(temporary))
            self.assertEqual(complete_capture(directory, outputs, response)["status"], "CAPTURE_INTEGRITY_VALID")
            first = (directory / "outputs.npz").read_bytes()
            complete_capture(directory, outputs, response)
            self.assertEqual(first, (directory / "outputs.npz").read_bytes())

    def test_foreign_request_or_changed_inputs_cannot_finish_capture(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory, response, outputs = self.fixture(Path(temporary))
            response["response_id"] = str(uuid4())
            with self.assertRaises(ValueError):
                complete_capture(directory, outputs, response)
            response["response_id"] = response["request_id"]
            (directory / "inputs.npz").write_bytes(b"corrupted input")
            with self.assertRaises(ValueError):
                complete_capture(directory, outputs, response)
            self.assertFalse((directory / "outputs.npz").exists())

    def test_crash_after_output_save_resumes_without_overwriting(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory, response, outputs = self.fixture(Path(temporary))
            with patch("ml.pipeline.capture_recovery.save_json", side_effect=OSError("disk fixture")):
                with self.assertRaises(OSError):
                    complete_capture(directory, outputs, response)
            first = (directory / "outputs.npz").read_bytes()
            complete_capture(directory, outputs, response)
            self.assertEqual(first, (directory / "outputs.npz").read_bytes())
            with self.assertRaises(ValueError):
                complete_capture(directory, {"output0": outputs["output0"] + 1}, response)
