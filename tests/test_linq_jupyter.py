import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from ml.linq.jupyter import CaseError, capture_case, prepare_case, require_success_status, _CASES


class PortableCaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.calls = 0
        self.dest = self.root / 'captured'
        self.program = b'mock-program-not-tpu-evidence'
        self.digest = hashlib.sha256(self.program).hexdigest()
        self.addCleanup(patch.stopall)
        patch.dict(_CASES, {'helmet': {**_CASES['helmet'], 'program_sha256': self.digest}}).start()
        self.directory = self.root/'models'/'helmet'
        self.directory.mkdir(parents=True)
        self.manifest = {
            'model_id':'helmet-v1','decoder':'detect_v8','classes':['helmet','bare_head'],
            'nms_in_graph':False,
            'input':{'name':'images','shape':[1,3,2,2],'dtype':'float32','layout':'NCHW'},
            'output_name':'output0','artifacts':{'onnx':{'sha256':'b'*64}}}
        self.compiled = {'model_id':'helmet-v1','compile_status':'PASS',
            'program_sha256':self.digest,'source_onnx_sha256':'b'*64,
            'runtime_abi_verified':False,
            'inputs':[{'name':'images','shape':[1,3,2,2],'dtype':'float32'}],
            'outputs':[{'name':'output0','shape':[1,6,1],'dtype':'float32'}]}
        self.transform = {'original_width':2,'original_height':2,'input_width':2,'input_height':2,
                          'resized_width':2,'resized_height':2,'left':0,'top':0}
        self.write_json('manifest.json', self.manifest)
        self.write_json('compile-report.json', self.compiled)
        self.write_json('capture-transform.json', {'original_transform':self.transform})
        (self.directory/'model.tpu').write_bytes(self.program)
        np.savez(self.directory/'inputs.npz', images=np.ones((1,3,2,2),dtype=np.float32))
        np.savez(self.directory/'golden-outputs.npz', output0=np.ones((1,6,1),dtype=np.float32))

    def write_json(self, name, value):
        (self.directory/name).write_text(json.dumps(value))

    def invoke(self, inputs):
        self.calls += 1
        return {'output0':np.ones((1,6,1),dtype=np.float32)}

    def capture(self, **kwargs):
        return capture_case(self.root, 'helmet', self.invoke, self.dest, **kwargs)

    def test_prepare_owned_numeric_case_and_never_upgrade_abi(self):
        self.compiled['runtime_abi_verified']=True
        self.write_json('compile-report.json',self.compiled)
        case=prepare_case(self.root,'helmet')
        self.assertFalse(case['runtime_abi_verified'])
        self.assertEqual(case['program_sha256'],self.digest)
        self.assertEqual(case['input_specs']['images'],{'shape':[1,3,2,2],'dtype':'float32'})
        self.assertEqual(case['original_transform'],self.transform)
        case['inputs']['images'][:]=9
        fresh=prepare_case(self.root,'helmet')
        np.testing.assert_equal(fresh['inputs']['images'],np.ones((1,3,2,2)))
        self.assertEqual(self.calls,0)

    def test_default_requires_verified_abi_or_explicit_diagnostic(self):
        with self.assertRaises(CaseError):self.capture()
        self.assertEqual(self.calls,0)
        self.assertFalse(self.dest.exists())

    def test_diagnostic_captures_once_without_hardware_or_abi_claim(self):
        result=self.capture(diagnostic_only=True)
        self.assertEqual(result['status'],'completed')
        self.assertEqual(self.calls,1)
        self.assertTrue(result['case_config']['diagnostic_only'])
        self.assertFalse(result['case_config']['runtime_abi_verified_attested'])
        self.assertFalse(result['hardware_placement']['independently_verified'])
        self.assertEqual(result['case_config']['output_spec_policy'],'observed_numeric_only')
        self.assertEqual(json.loads((self.dest/'capture.json').read_text()),result)

    def test_explicit_name_maps_no_shape_guessing(self):
        def invoke(inputs):
            self.calls+=1
            self.assertEqual(set(inputs),{'runtime_images'})
            return {'runtime_scores':np.ones((1,6,1),dtype=np.float32)}
        result=capture_case(self.root,'helmet',invoke,self.dest,diagnostic_only=True,
            input_map={'runtime_images':'images'},output_map={'runtime_scores':'output0'})
        self.assertEqual(result['status'],'completed')
        self.assertEqual(result['runtime_to_reference'],{'runtime_scores':'output0'})
        with np.load(self.dest/'inputs.npz',allow_pickle=False) as data:
            self.assertEqual(data.files,['runtime_images'])
        with np.load(self.dest/'outputs.npz',allow_pickle=False) as data:
            self.assertEqual(data.files,['runtime_scores'])

    def test_diagnostic_keeps_observed_dtype_shape_for_review(self):
        result=capture_case(self.root,'helmet',lambda inputs:{'output0':np.ones((1,7,2),dtype=np.float64)},
                            self.dest,diagnostic_only=True)
        self.assertEqual(result['status'],'completed')
        self.assertEqual(result['outputs']['output0']['dtype'],'float64')
        self.assertEqual(result['outputs']['output0']['shape'],[1,7,2])

    def test_strict_attested_abi_asserts_output_specs(self):
        result=capture_case(self.root,'helmet',lambda inputs:{'output0':np.ones((1,7,2),dtype=np.float64)},
                            self.dest,runtime_abi_verified=True)
        self.assertEqual(result['status'],'failed')
        self.assertTrue(result['call_completed'])
        self.assertFalse((self.dest/'outputs.npz').exists())

    def test_diagnostic_can_assert_explicit_observed_specs(self):
        result=self.capture(diagnostic_only=True,
            runtime_output_specs={'output0':{'shape':[1,6,1],'dtype':'float64'}})
        self.assertEqual(result['status'],'failed')
        self.assertEqual(self.calls,1)

    def test_invalid_maps_and_specs_do_not_call_runtime(self):
        for kwargs in [dict(input_map={'wrong':'not_images'}),
                       dict(output_map={'wrong':'not_output0'}),
                       dict(runtime_input_specs={'images':{'shape':[1,3,2,2],'dtype':'int8'}}),
                       dict(runtime_output_specs={'output0':{'name':'renamed','shape':[1,6,1],'dtype':'float32'}})]:
            with self.subTest(kwargs=kwargs),self.assertRaises((CaseError,ValueError)):
                self.capture(diagnostic_only=True,**kwargs)
        self.assertEqual(self.calls,0)

    def test_program_tampering_is_rejected_even_if_report_rehashed(self):
        (self.directory/'model.tpu').write_bytes(b'tampered')
        self.compiled['program_sha256']=hashlib.sha256(b'tampered').hexdigest()
        self.write_json('compile-report.json',self.compiled)
        with self.assertRaises(CaseError):self.capture(diagnostic_only=True)
        self.assertEqual(self.calls,0)

    def test_graph_hash_classmap_and_transform_consistency(self):
        self.manifest['artifacts']['onnx']['sha256']='c'*64
        self.write_json('manifest.json',self.manifest)
        with self.assertRaises(CaseError):prepare_case(self.root,'helmet')
        self.manifest['artifacts']['onnx']['sha256']='b'*64
        self.manifest['classes']=['bare_head','helmet']
        self.write_json('manifest.json',self.manifest)
        with self.assertRaises(CaseError):prepare_case(self.root,'helmet')
        self.manifest['classes']=['helmet','bare_head']
        self.write_json('manifest.json',self.manifest)
        self.transform['input_width']=3
        self.write_json('capture-transform.json',{'original_transform':self.transform})
        with self.assertRaises(CaseError):prepare_case(self.root,'helmet')

    def test_numeric_npz_only_and_exact_golden_specs(self):
        np.savez(self.directory/'golden-outputs.npz',output0=np.array(['credential-marker']))
        with self.assertRaises(CaseError) as caught:prepare_case(self.root,'helmet')
        self.assertNotIn('credential-marker',str(caught.exception))
        np.savez(self.directory/'golden-outputs.npz',output0=np.ones((1,6,1),dtype=np.float64))
        with self.assertRaises(CaseError):prepare_case(self.root,'helmet')

    def test_unknown_case_and_external_symlink_rejected(self):
        with self.assertRaises(CaseError):prepare_case(self.root,'../private')
        external=self.root/'external-program';external.write_bytes(self.program)
        (self.directory/'model.tpu').unlink()
        (self.directory/'model.tpu').symlink_to(external)
        with self.assertRaises(CaseError):prepare_case(self.root,'helmet')

    def test_actual_extracted_status_guard_no_response_assumptions(self):
        require_success_status(0)
        require_success_status(np.int64(0))
        require_success_status(200,success=200)
        for value in [1,True,'0',{'status_code':0},(0,[])]:
            with self.assertRaises(CaseError):require_success_status(value)
        def failing(inputs):
            self.calls+=1
            require_success_status(3)
            return {'output0':np.ones((1,6,1),dtype=np.float32)}
        result=capture_case(self.root,'helmet',failing,self.dest,diagnostic_only=True)
        self.assertEqual(result['status'],'failed')
        self.assertFalse(result['call_completed'])
        self.assertEqual(self.calls,1)
        self.assertFalse((self.dest/'outputs.npz').exists())

    def test_missing_file_no_runtime_call_and_no_private_paths_in_error(self):
        (self.directory/'inputs.npz').unlink()
        with self.assertRaises(CaseError) as caught:self.capture(diagnostic_only=True)
        self.assertNotIn(str(self.root),str(caught.exception))
        self.assertEqual(self.calls,0)


if __name__=='__main__':unittest.main()
