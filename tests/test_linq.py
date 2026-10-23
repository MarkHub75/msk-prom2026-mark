import unittest
from unittest.mock import patch
import numpy as np
from ml.linq import LinQBackend, TensorSpec
from ml.linq.preflight import check


def manifest():
    return {"model_id":"test-v1","program_sha256":"a"*64,
            "inputs":[{"name":"image","shape":[1,2],"dtype":"float32"}],
            "outputs":[{"name":"scores","shape":[1,2],"dtype":"float32"}]}


def request(array=None):
    return {"request_id":"req-1","model_id":"test-v1",
            "inputs":{"image":np.ones((1,2),dtype=np.float32) if array is None else array}}


class LinQTests(unittest.TestCase):
    def test_missing_runner_never_falls_back(self):
        r=LinQBackend(manifest()).infer(request())
        self.assertEqual(r["error"]["code"],"linq_unavailable")
        self.assertEqual(r["outputs"],{})
        self.assertFalse(r["execution_verified"])

    def test_copies_output_and_correlates(self):
        source=np.array([[.1,.9]],dtype=np.float32)
        backend=LinQBackend(manifest(),lambda inputs,meta:{"scores":source})
        r=backend.infer(request()); source[:]=0
        self.assertEqual(r["status"],"ok")
        self.assertEqual(r["request_id"],"req-1")
        np.testing.assert_allclose(r["outputs"]["scores"],[[.1,.9]])
        self.assertFalse(r["execution_verified"])

    def test_rejects_bad_inputs_before_call(self):
        called=[]
        backend=LinQBackend(manifest(),lambda *args:called.append(1))
        for a in [np.ones((1,2),dtype=np.float64),np.ones((2,1),dtype=np.float32),
                  np.array([[np.nan,0]],dtype=np.float32),
                  np.ones((1,4),dtype=np.float32)[:,::2]]:
            with self.subTest(shape=a.shape,dtype=a.dtype):
                self.assertEqual(backend.infer(request(a))["error"]["code"],"contract_error")
        self.assertEqual(called,[])

    def test_request_model_and_names(self):
        backend=LinQBackend(manifest(),lambda *args:{})
        r=request();r['model_id']='wrong'
        self.assertEqual(backend.infer(r)['status'],'error')
        r=request();r['inputs']['extra']=r['inputs']['image']
        self.assertEqual(backend.infer(r)['status'],'error')

    def test_bad_output_rejected(self):
        for out in [{}, {'scores':np.zeros((1,2),dtype=np.int8)}, {'scores':np.full((1,2),np.inf,dtype=np.float32)}]:
            r=LinQBackend(manifest(),lambda *args:out).infer(request())
            self.assertEqual(r['status'],'error')
            self.assertEqual(r['outputs'],{})

    def test_runner_error_does_not_leak_message(self):
        def runner(*args):raise RuntimeError('password=do-not-expose')
        r=LinQBackend(manifest(),runner).infer(request())
        self.assertEqual(r['error']['code'],'runner_error')
        self.assertNotIn('do-not-expose',str(r))

    def test_witness_correlation_and_allowlist(self):
        def runner(inputs,meta):
            return {'outputs':{'scores':inputs['image']},'execution_witness':{
                **meta,'device_kind':'linq_tpu','completed':True,'token':'hidden'}}
        r=LinQBackend(manifest(),runner).infer(request())
        self.assertEqual(r['status'],'ok')
        self.assertNotIn('token',r['execution_witness'])
        self.assertFalse(r['execution_verified'])
        def mismatched(inputs,meta):
            return {'outputs':{'scores':inputs['image']},'execution_witness':{
                **meta,'request_id':'wrong','device_kind':'linq_tpu','completed':True}}
        self.assertEqual(LinQBackend(manifest(),mismatched).infer(request())['status'],'error')

    def test_invalid_specs(self):
        for shape in [[0,2],[-1,2],[None,2],[True,2]]:
            with self.assertRaises(ValueError):TensorSpec.parse({'name':'x','shape':shape,'dtype':'float32'})
        with self.assertRaises(ValueError):TensorSpec.parse({'name':'x','shape':[1],'dtype':'object'})

    def test_preflight_cannot_claim_hardware(self):
        with patch('ml.linq.preflight.socket.getaddrinfo',side_effect=OSError), \
             patch('ml.linq.preflight.socket.create_connection',side_effect=OSError), \
             patch('ml.linq.preflight.urllib.request.build_opener') as opener:
            opener.return_value.open.side_effect=OSError
            report=check(timeout=.01)
        self.assertFalse(report['hardware_inference_confirmed'])
        self.assertEqual({x['name']:x['status'] for x in report['checks']}['own_model_tpu'],'not_run')



class LocalRunnerTests(unittest.TestCase):
    def test_official_run_api_and_resource_lifetime(self):
        import hashlib, tempfile, types
        from pathlib import Path
        from contextlib import contextmanager
        from ml.linq.local import LocalPytpuRunner
        actions=[]
        @contextmanager
        def context(name,value):
            actions.append('open-'+name)
            try:yield value
            finally:actions.append('close-'+name)
        inf=types.SimpleNamespace(run=lambda inputs:{'scores':inputs['image']})
        program=types.SimpleNamespace(inference=lambda:context('inference',inf))
        device=types.SimpleNamespace(load=lambda path:context('program',program))
        fake=types.SimpleNamespace(Device=types.SimpleNamespace(
            list_devices=lambda:['/dev/tpu0'],open=lambda path:context('device',device)))
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'test.tpu';path.write_bytes(b'fake-test-program')
            digest=hashlib.sha256(path.read_bytes()).hexdigest()
            m=manifest();m['program_sha256']=digest
            with patch('ml.linq.local.importlib.import_module',return_value=fake):
                with LocalPytpuRunner(path,digest) as runner:
                    r=LinQBackend(m,runner).infer(request())
                    self.assertEqual(r['status'],'ok')
                    self.assertTrue(r['execution_witness']['completed'])
                    self.assertFalse(r['execution_verified'])
            self.assertEqual(actions,['open-device','open-program','open-inference',
                                      'close-inference','close-program','close-device'])
            np.testing.assert_equal(r['outputs']['scores'],[[1,1]])

    def test_program_hash_checked_before_runtime(self):
        import tempfile
        from pathlib import Path
        from ml.linq.local import LocalPytpuRunner
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'test.tpu';path.write_bytes(b'fake')
            with self.assertRaises(ValueError):
                with LocalPytpuRunner(path,'0'*64):pass


if __name__=='__main__':unittest.main()
