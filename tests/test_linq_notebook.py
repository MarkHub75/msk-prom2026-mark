import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from ml.linq.notebook import capture_call, ExpectedClass


class NotebookCaptureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.program = self.root / 'program.tpu'
        self.program.write_bytes(b'fixture-not-a-real-tpu-program')
        self.dest = self.root / 'capture'
        self.calls = 0

    def invoke(self, arrays):
        self.calls += 1
        return {'runtime/output': arrays['images'].copy()}

    def run_capture(self, **changes):
        options = {'inputs': {'images': np.array([[1., 2.]], dtype=np.float32)},
                   'output_names': ['runtime/output'], 'program_path': self.program,
                   'output_dir': self.dest, 'model_id': 'fixture-v1'}
        options.update(changes)
        return capture_call(options.pop('run', self.invoke), **options)

    def test_once_named_arrays_hashes_and_explicit_mapping(self):
        result = self.run_capture(placement_attested=True,
            runtime_to_reference={'runtime/output': 'reference/output'})
        self.assertEqual(self.calls, 1)
        self.assertEqual(result['status'], 'completed')
        self.assertTrue(result['call_completed'])
        self.assertFalse(result['hardware_placement']['independently_verified'])
        self.assertEqual(result['hardware_placement']['basis'], 'user_supplied_runtime_attestation')
        self.assertEqual(result['program']['sha256'], hashlib.sha256(self.program.read_bytes()).hexdigest())
        for name in ['inputs', 'outputs']:
            file=self.dest / (name+'.npz')
            self.assertEqual(result['artifacts'][name]['sha256'], hashlib.sha256(file.read_bytes()).hexdigest())
            with np.load(file, allow_pickle=False) as data:
                self.assertEqual(set(data.files), {'images'} if name=='inputs' else {'runtime/output'})
        self.assertEqual(json.loads((self.dest/'capture.json').read_text()), result)
        self.assertNotIn(str(self.root), json.dumps(result))
        self.assertGreaterEqual(result['timings']['call_ms'], 0)

    def test_no_success_or_completion_before_supplied_call(self):
        def invoke(arrays):
            before=json.loads((self.dest/'capture.json').read_text())
            self.assertEqual(before['status'], 'pending_call')
            self.assertFalse(before['call_completed'])
            self.assertNotIn('outputs', before['artifacts'])
            return self.invoke(arrays)
        self.assertEqual(self.run_capture(run=invoke)['status'], 'completed')
        self.assertEqual(self.calls, 1)

    def test_input_copy_survives_callback_mutation(self):
        original=np.array([[1,2]],dtype=np.int32)
        def invoke(arrays):
            arrays['images'][:]=9
            return self.invoke(arrays)
        result=self.run_capture(run=invoke, inputs={'images':original})
        self.assertEqual(result['status'], 'completed')
        np.testing.assert_equal(original, [[1,2]])
        with np.load(self.dest/'inputs.npz',allow_pickle=False) as data:
            np.testing.assert_equal(data['images'], [[1,2]])

    def test_invalid_inputs_never_invoke(self):
        for value in [np.array(['auth-secret']), np.array([object()]),
                      np.array([[np.nan]],dtype=np.float32), np.array([],dtype=np.float32)]:
            result=self.run_capture(inputs={'images':value})
            self.assertEqual(result['status'], 'failed')
            self.assertFalse(result['call_started'])
        self.assertEqual(self.calls, 0)
        self.assertFalse(self.dest.exists())

    def test_output_dtype_preserved_and_spec_asserted(self):
        result=self.run_capture(output_specs={'runtime/output': {'shape':[1,2], 'dtype':'float64'}})
        self.assertEqual(result['status'], 'failed')
        self.assertTrue(result['call_completed'])
        self.assertFalse((self.dest/'outputs.npz').exists())
        self.assertEqual(result['error']['phase'], 'validate_outputs')

    def test_input_dtype_mismatch_never_calls(self):
        result=self.run_capture(input_specs={'images':{'shape':[1,2],'dtype':'int8'}})
        self.assertEqual(result['status'],'failed')
        self.assertEqual(self.calls,0)

    def test_no_extra_runtime_metadata_or_secret_error_text(self):
        def invoke(arrays):
            return {'runtime/output':arrays['images'], 'session':{'password':'never-write-this'}}
        result=self.run_capture(run=invoke)
        self.assertEqual(result['status'],'failed')
        report=(self.dest/'capture.json').read_text()
        self.assertNotIn('never-write-this',report)
        self.assertNotIn('session',report)
        self.assertFalse((self.dest/'outputs.npz').exists())

    def test_callable_failure_is_not_retried_and_message_is_not_saved(self):
        def invoke(arrays):
            self.calls+=1
            raise RuntimeError('password=never-write-this; cookie=private')
        result=self.run_capture(run=invoke)
        self.assertEqual(self.calls,1)
        self.assertEqual(result['status'],'failed')
        self.assertFalse(result['call_completed'])
        self.assertEqual(result['error'],{'phase':'invoke_supplied_call','exception_type':'RuntimeError'})
        self.assertNotIn('never-write-this',json.dumps(result))
        self.assertNotIn('private',(self.dest/'capture.json').read_text())

    def test_existing_capture_never_overwritten_or_called(self):
        self.dest.mkdir(); (self.dest/'capture.json').write_text('original')
        result=self.run_capture()
        self.assertEqual(result['status'],'failed')
        self.assertEqual(self.calls,0)
        self.assertEqual((self.dest/'capture.json').read_text(),'original')

    def test_classification_is_opt_in_axis_and_offset_explicit(self):
        result=self.run_capture(expected_class=ExpectedClass('runtime/output',2,axis=1,class_offset=1))
        self.assertEqual(result['status'],'completed')
        self.assertEqual(result['checks']['expected_class']['observed'],2)
        self.assertEqual(result['checks']['expected_class']['status'],'PASS')

    def test_wrong_expected_class_is_not_success(self):
        result=self.run_capture(expected_class=ExpectedClass('runtime/output',257,axis=1,class_offset=0))
        self.assertEqual(result['status'],'validation_failed')
        self.assertTrue(result['call_completed'])
        self.assertEqual(result['checks']['expected_class']['status'],'FAIL')
        self.assertTrue((self.dest/'outputs.npz').exists())

    def test_default_claims_no_hardware_and_no_class_check(self):
        result=self.run_capture()
        self.assertEqual(result['hardware_placement']['claimed_device'],'unverified')
        self.assertNotIn('expected_class',result['checks'])
        self.assertNotIn('execution_verified',result)

    def test_mapping_must_be_exact_and_one_to_one(self):
        for mapping in [{}, {'other':'output'}, {'runtime/output':'bad name with spaces'}]:
            result=self.run_capture(runtime_to_reference=mapping)
            self.assertEqual(result['status'],'failed')
            self.assertEqual(self.calls,0)

    def test_transform_allowlist_no_arbitrary_metadata(self):
        result=self.run_capture(original_transform={'cookie':'never-write-this'})
        self.assertEqual(result['status'],'failed')
        self.assertNotIn('never-write-this',json.dumps(result))
        self.assertEqual(self.calls,0)

    def test_exact_numeric_transform_saved(self):
        transform=dict(original_width=1920,original_height=1080,input_width=640,input_height=640,
                       resized_width=640,resized_height=360,left=0,top=140)
        result=self.run_capture(original_transform=transform)
        self.assertEqual(result['original_transform'],transform)

    def test_nonfinite_output_fails_without_writing_tensor(self):
        result=self.run_capture(run=lambda arrays:{'runtime/output':np.array([np.inf])})
        self.assertEqual(result['status'],'failed')
        self.assertFalse((self.dest/'outputs.npz').exists())

    def test_byte_budget_rejects_before_call(self):
        result=self.run_capture(max_bytes=1)
        self.assertEqual(result['status'],'failed')
        self.assertEqual(self.calls,0)


if __name__=='__main__':unittest.main()
