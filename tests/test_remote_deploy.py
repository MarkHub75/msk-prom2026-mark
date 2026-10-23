import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
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
            with patch.object(module,'ARTIFACTS',root),patch.dict(module.PROFILES,{'helmet':('helmet-v1','helmet-v1.tpu',sha)}),patch.object(module,'_environment_parameters',return_value=object()),patch.object(module,'official_binding',return_value=SimpleNamespace()),patch.object(module,'AmqpRunner',Runner):
                with self.assertRaises(AmqpError) as raised:
                    module.upload_program('helmet',{'upload_queue':'notebook_upload_'+'a'*32})
                self.assertEqual(raised.exception.details['code'],'jupyter_upload_agent_not_ready')
            self.assertFalse((root/'linq-rpc/helmet/staging-receipt.json').exists())

    def test_wrong_remote_hash_never_produces_staging_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);blob,sha=self.setup_program(root)
            class Runner:
                def __init__(self,*args,**kwargs):self.last_response={'request_id':'unit-only','remote_completion':'response_received'}
                def __call__(self,inputs):
                    self_input=inputs['program_bytes'];assert self_input.tobytes()==blob
                    return {'sha256':np.zeros(32,np.uint8),'byte_count':np.array([len(blob)],np.int64)}
            with patch.object(module,'ARTIFACTS',root),patch.dict(module.PROFILES,{'helmet':('helmet-v1','helmet-v1.tpu',sha)}),patch.object(module,'_environment_parameters',return_value=object()),patch.object(module,'official_binding',return_value=SimpleNamespace()),patch.object(module,'AmqpRunner',Runner):
                with self.assertRaises(ValueError):module.upload_program('helmet',{'upload_queue':'notebook_upload_'+'a'*32})
            self.assertFalse((root/'linq-rpc/helmet/staging-receipt.json').exists())

    def test_unreviewed_local_bytes_stop_before_connection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.setup_program(root)
            with patch.object(module,'ARTIFACTS',root),patch.object(module,'_environment_parameters') as params:
                with self.assertRaises(ValueError):module.upload_program('helmet',{'upload_queue':'notebook_upload_'+'a'*32})
                params.assert_not_called()
