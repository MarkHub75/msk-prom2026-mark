import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4
import tempfile
import unittest
from unittest.mock import patch
import numpy as np

from ml.linq import video
from ml.linq.amqp import AmqpError
from ml.linq.backend import LinQBackend, PendingRequestError, TerminalRequestError
from ml.linq.journal import RequestJournal, atomic_json, TERMINAL


class DurableVideoTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'run';self.program=Path(self.tmp.name)/'fixture.tpu'
        self.program.write_bytes(b'test-program-not-hardware')
        self.digest=hashlib.sha256(self.program.read_bytes()).hexdigest()
        self.addCleanup(patch.stopall)
        patch.dict(video._MODELS,{'helmet-v1':('matvey_helmet-v1.tpu',self.digest),
                                 'pose-split-v1':('matvey_pose-split-v1.tpu',self.digest)}).start()
        patch.dict('os.environ',{'LINQ_LOGIN':'unit-test-account'}).start()
        patch.object(video,'_environment_parameters',return_value=object()).start()
        patch.object(video,'official_binding',side_effect=lambda *a,**k:SimpleNamespace(output_names=k['output_names'])).start()
        self.publishes=0;self.reconciles=0;self.mode='success';self.resolve=False
        owner=self
        class RpcFixture:
            def __init__(self,binding=None,program=None,*,journal_dir,timeout=60,purpose='inference',capture_dir=None):
                self.binding,self.program=binding,program
                self.store=RequestJournal(journal_dir);self.context=Path(capture_dir) if capture_dir else None
                self.purpose=purpose;self.last_response=None
            def summary(self,request_id,cached=False,reconcile=False):
                record=self.store.load(request_id)
                self.last_response={'request_id':request_id,'response_id':record.get('response_id'),
                    'status_code':record.get('status_code'),'journal_state':record['state'],
                    'remote_completion':'response_received' if record['state'] in TERMINAL else
                        'not_submitted' if record['state']=='NOT_SUBMITTED' else 'unknown',
                    'journal_path':str(self.store.path(request_id)),
                    'cached_response':cached,'reconcile_only':reconcile,'timings':{'total_ms':10.0}}
            def __call__(self,inputs):
                request_id=str(uuid4())
                self.store.create(request_id,purpose=self.purpose,
                    program_uri_sha256=hashlib.sha256(self.program.encode()).hexdigest(),inputs=inputs,
                    output_names=self.binding.output_names,capture_dir=self.context,
                    reply_queue='notebook_'+request_id[:8])
                atomic_json(self.context/'request-pointer.json',{'schema_version':'1.0',
                    'journal_request_id':request_id,'journal_path':str(self.store.path(request_id)),'purpose':'inference'})
                if owner.mode=='not_submitted':
                    self.summary(request_id);raise AmqpError('broker_unavailable','open_connection')
                self.store.update(request_id,'SUBMITTING');owner.publishes+=1
                self.store.update(request_id,'ACCEPTED',broker_confirmed=True)
                if owner.mode=='unknown':
                    self.store.update(request_id,'UNKNOWN');self.summary(request_id)
                    raise AmqpError('response_timeout','wait_response')
                if owner.mode=='service_failed':
                    self.store.complete(request_id,{},status_code=3,response_id=request_id)
                    self.summary(request_id);raise AmqpError('service_reported_failure','check_status',status_code=3)
                outputs={name:np.array([[.2,.8]],dtype=np.float32) for name in self.binding.output_names}
                self.store.complete(request_id,outputs,status_code=0,response_id=request_id)
                self.summary(request_id);return outputs
            def reconcile(self,request_id):
                owner.reconciles+=1
                record=self.store.recover(request_id);cached=record['state'] in TERMINAL
                if not cached:
                    if not owner.resolve:
                        self.summary(request_id,reconcile=True);raise AmqpError('response_timeout','wait_response')
                    outputs={name:np.array([[.2,.8]],dtype=np.float32) for name in record['output_names']}
                    self.store.complete(request_id,outputs,status_code=0,response_id=request_id)
                    record=self.store.load(request_id)
                self.summary(request_id,cached=cached,reconcile=True)
                if record['state']=='SERVICE_FAILED':
                    raise AmqpError('service_reported_failure','cached_response',status_code=record['status_code'])
                return self.store.outputs(request_id)
        patch.object(video,'AmqpRunner',RpcFixture).start()
        self.inputs={'images':np.array([[1.,2.]],dtype=np.float32)}

    def manifest(self,model='helmet-v1'):
        return {'model_id':model,'program_name':video._MODELS[model][0],'program_path':str(self.program),
            'program_sha256':self.digest,'rpc_state_dir':str(self.root/'rpc'/model),
            'journal_dir':str(self.root/'requests'),'format_source_manifest':'explicit-format-audit.json',
            'timeout':60,'inputs':[{'name':'images','shape':[1,2],'dtype':'float32'}],
            'outputs':[{'name':'output0','shape':[1,2],'dtype':'float32'}]}

    def metadata(self,frame=1,model='helmet-v1'):
        return {'request_id':f'epoch:{frame}:{model}','model_id':model,'program_sha256':self.digest}

    def context(self,frame=1,model='helmet-v1'):
        key=hashlib.sha256(self.metadata(frame,model)['request_id'].encode()).hexdigest()
        return self.root/'rpc'/model/key

    def test_success_correlates_logical_witness_and_distinct_transport_uuid(self):
        runner=video.create_runner(self.manifest())
        result=runner(self.inputs,self.metadata())
        self.assertEqual(self.publishes,1)
        self.assertEqual(result['execution_witness']['request_id'],'epoch:1:helmet-v1')
        provenance=result['transport_provenance']
        self.assertNotEqual(provenance['request_id'],'epoch:1:helmet-v1')
        self.assertEqual(provenance['request_id'],provenance['response_id'])
        self.assertEqual(provenance['journal_state'],'COMPLETED')
        self.assertEqual(provenance['latency_kind'],'initial_call')
        text=(self.context()/'logical.json').read_text()
        self.assertNotIn('unit-test-account',text)
        self.assertNotIn('file://',text)

    def test_duplicate_and_restart_use_cache_without_runtime_credentials(self):
        video.create_runner(self.manifest())(self.inputs,self.metadata())
        with patch.object(video,'_environment_parameters',side_effect=AssertionError('no auth read')):
            result=video.create_runner(self.manifest())(self.inputs,self.metadata())
        self.assertEqual(self.publishes,1)
        self.assertEqual(self.reconciles,1)
        self.assertTrue(result['transport_provenance']['cached_response'])
        self.assertEqual(result['transport_provenance']['latency_kind'],'cached_response')

    def test_changed_inputs_or_model_hash_rejected_without_reconcile_or_publish(self):
        runner=video.create_runner(self.manifest());runner(self.inputs,self.metadata())
        with self.assertRaises(ValueError):runner({'images':np.array([[1.,3.]],dtype=np.float32)},self.metadata())
        bad=self.metadata();bad['program_sha256']='f'*64
        with self.assertRaises(ValueError):runner(self.inputs,bad)
        self.assertEqual(self.publishes,1);self.assertEqual(self.reconciles,0)

    def test_unknown_is_receive_only_across_restart_until_resolved(self):
        self.mode='unknown'
        with self.assertRaises(PendingRequestError) as error:
            video.create_runner(self.manifest())(self.inputs,self.metadata())
        self.assertEqual(error.exception.code,'linq_pending')
        with self.assertRaises(PendingRequestError):
            video.create_runner(self.manifest())(self.inputs,self.metadata())
        self.assertEqual(self.publishes,1)
        self.resolve=True
        result=video.create_runner(self.manifest())(self.inputs,self.metadata())
        self.assertEqual(self.publishes,1)
        self.assertEqual(result['transport_provenance']['journal_state'],'COMPLETED')
        self.assertEqual(result['transport_provenance']['latency_kind'],'recovery_only')

    def test_definite_not_submitted_archives_attempt_then_safe_fresh_uuid(self):
        self.mode='not_submitted'
        with self.assertRaises(PendingRequestError) as error:
            video.create_runner(self.manifest())(self.inputs,self.metadata())
        self.assertEqual(error.exception.code,'linq_not_submitted')
        old=json.loads((self.context()/'request-pointer.json').read_text())['journal_request_id']
        self.assertEqual(self.publishes,0)
        self.mode='success'
        video.create_runner(self.manifest())(self.inputs,self.metadata())
        new=json.loads((self.context()/'request-pointer.json').read_text())['journal_request_id']
        self.assertNotEqual(old,new)
        self.assertTrue((self.context()/'attempts'/(old+'.json')).is_file())
        self.assertEqual(RequestJournal(self.root/'requests').load(old)['state'],'NOT_SUBMITTED')
        self.assertEqual(self.publishes,1)

    def test_unknown_blocks_fresh_other_model_across_run(self):
        self.mode='unknown'
        with self.assertRaises(PendingRequestError):video.create_runner(self.manifest())(self.inputs,self.metadata())
        self.mode='success'
        with self.assertRaises(PendingRequestError):
            video.create_runner(self.manifest('pose-split-v1'))(self.inputs,self.metadata(model='pose-split-v1'))
        self.assertEqual(self.publishes,1)

    def test_cached_model_remains_readable_while_other_model_is_unknown(self):
        video.create_runner(self.manifest())(self.inputs,self.metadata())
        self.mode='unknown'
        with self.assertRaises(PendingRequestError):
            video.create_runner(self.manifest('pose-split-v1'))(self.inputs,self.metadata(model='pose-split-v1'))
        cached=video.create_runner(self.manifest())(self.inputs,self.metadata())
        self.assertTrue(cached['transport_provenance']['cached_response'])
        self.assertEqual(self.publishes,2)

    def test_terminal_service_failure_never_republished(self):
        self.mode='service_failed'
        for _ in range(2):
            with self.assertRaises(TerminalRequestError):
                video.create_runner(self.manifest())(self.inputs,self.metadata())
        self.assertEqual(self.publishes,1)

    def test_missing_credentials_on_unknown_still_reports_unknown_not_unsent(self):
        self.mode='unknown'
        with self.assertRaises(PendingRequestError):video.create_runner(self.manifest())(self.inputs,self.metadata())
        with patch.object(video,'_environment_parameters',side_effect=AmqpError('unavailable','configuration')):
            with self.assertRaises(PendingRequestError) as error:
                video.create_runner(self.manifest())(self.inputs,self.metadata())
        self.assertEqual(error.exception.code,'linq_pending')
        self.assertEqual(error.exception.transport_provenance['journal_state'],'UNKNOWN')
        self.assertEqual(self.publishes,1)

    def test_shared_run_lock_across_model_factories(self):
        first=video.create_runner(self.manifest())
        other=video.create_runner(self.manifest('pose-split-v1'))
        with first._lock():
            with self.assertRaises(PendingRequestError) as error:
                other(self.inputs,self.metadata(model='pose-split-v1'))
        self.assertEqual(error.exception.code,'linq_busy')
        self.assertEqual(self.publishes,0)

    def test_backend_preserves_provenance_and_pending_terminal_distinction(self):
        manifest=self.manifest();backend=LinQBackend(manifest,video.create_runner(manifest))
        request={**self.metadata(),'inputs':self.inputs}
        self.mode='unknown'
        result=backend.infer(request)
        self.assertEqual(result['status'],'pending')
        self.assertEqual(result['error']['code'],'linq_pending')
        self.assertEqual(result['transport_provenance']['journal_state'],'UNKNOWN')
        self.assertEqual(result['outputs'],{})
        self.resolve=True
        result=backend.infer(request)
        self.assertEqual(result['status'],'ok')
        self.assertEqual(result['execution_witness']['request_id'],request['request_id'])
        self.assertFalse(result['execution_verified'])
        self.assertEqual(result['transport_provenance']['status_code'],0)

    def test_backend_service_failure_is_explicit_terminal_error(self):
        manifest=self.manifest();self.mode='service_failed'
        result=LinQBackend(manifest,video.create_runner(manifest)).infer({**self.metadata(),'inputs':self.inputs})
        self.assertEqual(result['status'],'error')
        self.assertEqual(result['error']['code'],'linq_service_failed')
        self.assertEqual(result['transport_provenance']['status_code'],3)

    def test_unreviewed_program_and_bad_state_path_rejected(self):
        manifest=self.manifest();manifest['program_name']='arbitrary.tpu'
        with self.assertRaises(ValueError):video.create_runner(manifest)
        manifest=self.manifest();manifest['rpc_state_dir']=str(self.root/'different'/'helmet-v1')
        with self.assertRaises(ValueError):video.create_runner(manifest)


if __name__=='__main__':unittest.main()
