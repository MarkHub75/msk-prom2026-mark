import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
from uuid import uuid4
import unittest
from unittest.mock import patch
import numpy as np
from ml.pipeline import remote_deploy as module
from ml.linq.amqp import AmqpError

class RemoteDeploymentTest(unittest.TestCase):
    def setup_program(self,root):
        file=root/'linq-sdk/helmet-compile/model.tpu';file.parent.mkdir(parents=True)
        blob=b'explicit upload test fixture';file.write_bytes(blob)
        return blob,hashlib.sha256(blob).hexdigest()

    def test_inactive_jupyter_agent_prevents_upload_and_inference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);blob,sha=self.setup_program(root)
            class Runner:
                def __init__(self,binding,*args,**kwargs):self.binding=binding
                def __call__(self,inputs):
                    channel=SimpleNamespace(queue_declare=lambda **kwargs:SimpleNamespace(method=SimpleNamespace(consumer_count=0)))
                    self.binding.reply_setup(channel,'notebook_fixture','request-fixture')
                    raise AssertionError('upload must not proceed without an active consumer')
            with patch.dict(module.os.environ,{'LINQ_LOGIN':'private_test_owner'}),patch.object(module,'ARTIFACTS',root),patch.dict(module.PROFILES,{'helmet':('helmet-v1','matvey_helmet-v1.tpu',sha)}),patch.object(module,'_environment_parameters',return_value=object()),patch.object(module,'official_binding',return_value=SimpleNamespace()),patch.object(module,'AmqpRunner',Runner):
                with self.assertRaises(AmqpError) as raised:
                    module.upload_program('helmet',{'namespace_owner':'matvey','upload_queue':'matvey_upload_'+str(uuid4())})
                self.assertEqual(raised.exception.details['code'],'jupyter_upload_agent_not_ready')
            self.assertFalse((root/'linq-rpc/matvey_helmet_staging_v1/staging-receipt.json').exists())

    def test_wrong_remote_hash_never_produces_staging_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);blob,sha=self.setup_program(root)
            class Runner:
                def __init__(self,*args,**kwargs):self.last_response={'request_id':'unit-only','remote_completion':'response_received'}
                def __call__(self,inputs):
                    self_input=inputs['program_bytes'];assert self_input.tobytes()==blob
                    return {'sha256':np.zeros(32,np.uint8),'byte_count':np.array([len(blob)],np.int64)}
            with patch.dict(module.os.environ,{'LINQ_LOGIN':'private_test_owner'}),patch.object(module,'ARTIFACTS',root),patch.dict(module.PROFILES,{'helmet':('helmet-v1','matvey_helmet-v1.tpu',sha)}),patch.object(module,'_environment_parameters',return_value=object()),patch.object(module,'official_binding',return_value=SimpleNamespace()),patch.object(module,'AmqpRunner',Runner):
                with self.assertRaises(ValueError):module.upload_program('helmet',{'namespace_owner':'matvey','upload_queue':'matvey_upload_'+str(uuid4())})
            self.assertFalse((root/'linq-rpc/matvey_helmet_staging_v1/staging-receipt.json').exists())

    def test_unreviewed_local_bytes_stop_before_connection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.setup_program(root)
            with patch.dict(module.os.environ,{'LINQ_LOGIN':'private_test_owner'}),patch.object(module,'ARTIFACTS',root),patch.object(module,'_environment_parameters') as params:
                with self.assertRaises(ValueError):module.upload_program('helmet',{'namespace_owner':'matvey','upload_queue':'matvey_upload_'+str(uuid4())})
                params.assert_not_called()

    def test_foreign_upload_queue_stops_before_private_config(self):
        with patch.object(module,'_environment_parameters') as private:
            with self.assertRaises(ValueError):
                module._submit_upload('helmet',{'namespace_owner':'matvey','upload_queue':'captain_queue'},b'x',Path('/unused'),60)
        private.assert_not_called()

    def test_owned_queue_uses_default_full_uuid_reply_and_runtime_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);blob,sha=self.setup_program(root)
            seen={}
            def binding(*args,**kwargs):
                seen.update(kwargs);return SimpleNamespace()
            class Runner:
                def __init__(self,*args,**kwargs):
                    self.last_response={'request_id':str(uuid4()),'remote_completion':'response_received'}
                def __call__(self,inputs):
                    return {'sha256':np.frombuffer(bytes.fromhex(sha),np.uint8),'byte_count':np.array([len(blob)],np.int64)}
            with patch.dict(module.os.environ,{'LINQ_LOGIN':'private_test_owner'}),patch.object(module,'ARTIFACTS',root),patch.dict(module.PROFILES,{'helmet':('helmet-v1','matvey_helmet-v1.tpu',sha)}),patch.object(module,'_environment_parameters',return_value=object()),patch.object(module,'official_binding',side_effect=binding),patch.object(module,'AmqpRunner',Runner):
                receipt=module.upload_program('helmet',{'namespace_owner':'matvey','upload_queue':'matvey_upload_'+str(uuid4())})
            self.assertNotIn('reply_queue_factory',seen)
            self.assertEqual(seen['owner_login'],'private_test_owner')
            self.assertEqual(receipt['program_name'],'matvey_helmet-v1.tpu')
            self.assertTrue(receipt['program_path_namespace_verified'])
            self.assertNotIn('private_test_owner',json.dumps(receipt))

    def test_legacy_receipt_cannot_prove_owned_staging(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);blob,sha=self.setup_program(root)
            state=root/'linq-rpc/matvey_helmet_staging_v1';state.mkdir(parents=True)
            (state/'staging-receipt.json').write_text(json.dumps({'status':'STAGED','model_id':'helmet-v1','program_name':'helmet-v1.tpu','program_sha256':sha,'bytes':len(blob)}))
            with patch.object(module,'ARTIFACTS',root),patch.dict(module.PROFILES,{'helmet':('helmet-v1','matvey_helmet-v1.tpu',sha)}),patch.object(module,'_environment_parameters') as private:
                with self.assertRaises(ValueError):module.upload_program('helmet',{})
            private.assert_not_called()

    def test_completed_historical_capture_is_reviewed_offline_without_stock_or_private_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);out=root/'linq-rpc/helmet-001';out.mkdir(parents=True)
            (out/'capture.json').write_text(json.dumps({'model_id':'helmet-v1','status':'completed','program':{'sha256':module.PROFILES['helmet'][2]}}))
            (out/'response.json').write_text('{}')
            with patch.object(module,'ARTIFACTS',root),patch.object(module,'verify_model',return_value={'status':'PASS'}) as verify,patch.object(module,'_environment_parameters') as private:
                self.assertEqual(module._run('helmet','/unused',60),0)
                verify.assert_called_once_with('helmet',out)
            private.assert_not_called()
