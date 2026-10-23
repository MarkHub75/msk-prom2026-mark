"""Mock call capture -> integrity review -> CV comparator; no TPU claim."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from ml.linq.notebook import capture_call
from ml.pipeline.capture_review import review_capture
from ml.detection.compare_capture import compare_captures,load_numeric_npz

class CaptureIntegrationTest(unittest.TestCase):
    def capture(self,root):
        program=root/'mock-program.tpu';program.write_bytes(b'mock-only-not-a-TPU-program')
        count=[]
        def run(inputs):
            count.append(1)
            return {'runtime_scores':inputs['images']*2}
        report=capture_call(run,inputs={'images':np.array([[.2,.4]],np.float32)},
            output_names=['runtime_scores'],program_path=program,output_dir=root/'capture',
            model_id='mock-reference',runtime_to_reference={'runtime_scores':'scores'})
        self.assertEqual(count,[1]);self.assertEqual(report['status'],'completed')
        return report,hashlib.sha256(program.read_bytes()).hexdigest()

    def test_capture_review_and_compare_preserve_honest_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);capture,sha=self.capture(root)
            reviewed=review_capture(root/'capture',sha)
            self.assertEqual(reviewed['status'],'CAPTURE_INTEGRITY_VALID')
            self.assertFalse(capture['hardware_placement']['independently_verified'])
            compared=compare_captures({'scores':np.array([[.4,.8]],np.float32)},
                load_numeric_npz(root/'capture'/'outputs.npz'),metadata=capture)
            self.assertTrue(compared['outputs']['scores']['exact_equal'])
            self.assertEqual(compared['hardware_execution'],'NOT_ESTABLISHED_BY_COMPARISON')

    def test_modified_artifact_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.capture(root)
            np.savez(root/'capture'/'outputs.npz',runtime_scores=np.array([[1,2]],np.float32))
            with self.assertRaises(ValueError):review_capture(root/'capture')

    def test_self_consistent_wrong_tensor_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);capture,_=self.capture(root)
            capture['outputs']['runtime_scores']['shape']=[2,1]
            (root/'capture'/'capture.json').write_text(json.dumps(capture))
            with self.assertRaises(ValueError):review_capture(root/'capture')

    def test_expected_program_mismatch_or_failed_call_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);capture,_=self.capture(root)
            with self.assertRaises(ValueError):review_capture(root/'capture','0'*64)
            capture['status']='failed'
            (root/'capture'/'capture.json').write_text(json.dumps(capture))
            with self.assertRaises(ValueError):review_capture(root/'capture')
