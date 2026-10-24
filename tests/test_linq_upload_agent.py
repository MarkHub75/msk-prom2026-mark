from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import tempfile
import threading
from types import SimpleNamespace
from uuid import uuid4
import unittest
from unittest.mock import Mock, patch

import numpy as np
from ml.linq import upload_agent as ua


@dataclass
class TaskFixture:
    data: object
    status_code: int = 0
    error_message: str = ''


class FormatFixture:
    PyTask=TaskFixture
    MESSAGE_ID_ATTR_NAME='tpu_pycloud_message_id'
    RESPONSE_ROUTING_KEYS_ATTR_NAME='response_routing_keys'
    TARGET_URI_ATTR_NAME='uri'
    def __init__(self,data):self.decoded=(data,(),{'status_code':0});self.replies=[]
    def deserialize(self,body):return self.decoded
    def serialize(self,task):self.replies.append(task);return b'mock-response-only'


class ChannelFixture:
    def __init__(self):self.published=[];self.acked=[];self.deleted=[];self.publish_failure=False
    def basic_publish(self,**kwargs):
        self.published.append(kwargs)
        if self.publish_failure:raise ConnectionError('credential-marker-must-not-escape')
    def basic_ack(self,**kwargs):self.acked.append(kwargs)
    def queue_declare(self,**kwargs):self.declared=kwargs
    def basic_qos(self,**kwargs):self.qos=kwargs
    def basic_consume(self,**kwargs):self.consumer=kwargs
    def queue_delete(self,**kwargs):self.deleted.append(kwargs)


class UploadProtocolTests(unittest.TestCase):
    def setUp(self):
        self.blob=bytes(range(32));self.digest=hashlib.sha256(self.blob).hexdigest()
        self.addCleanup(patch.stopall)
        patch.dict(ua._MODELS,{'helmet':('matvey_helmet-v1.tpu',self.digest),
                              'pose-split':('matvey_pose-split-v1.tpu',self.digest)}).start()
        self.fmt=FormatFixture({'program_bytes':np.frombuffer(self.blob,dtype=np.uint8)})
        self.pika=SimpleNamespace(BasicProperties=lambda **kwargs:SimpleNamespace(**kwargs))
        self.channel=ChannelFixture();self.request_id=str(uuid4())
        self.headers={'tpu_pycloud_message_id':self.request_id,
                      'response_routing_keys':json.dumps(['matvey_reply_'+self.request_id]),'uri':'helmet'}
        self.stage=Mock(side_effect=self.stage_valid)
        self.agent=ua.UploadAgent(SimpleNamespace(),'/auto/cache/fixture/matvey',
                                  'matvey_upload_'+str(uuid4()),self.stage)

    def stage_valid(self,cache,source,*,model):
        self.assertEqual(Path(source).read_bytes(),self.blob)
        self.assertEqual(Path(cache),Path('/auto/cache/fixture/matvey'))
        name,digest=ua._MODELS[model]
        return {'status':'STAGED','program_name':name,'program_sha256':digest,
                'namespace_owner':'matvey','program_path_namespace_verified':True,
                'worker_visibility':'NOT_VERIFIED_UNTIL_REQUEST'}

    def consume(self,body=b'body-fixture'):
        self.agent._consume(self.fmt,self.pika,self.channel,SimpleNamespace(delivery_tag=7),
                            SimpleNamespace(headers=self.headers),body)
        self.assertEqual(self.channel.acked,[{'delivery_tag':7}])

    def test_success_numeric_receipt_official_id_and_default_exchange(self):
        self.consume()
        self.stage.assert_called_once()
        receipt=self.fmt.replies[0]
        self.assertEqual(receipt.status_code,0)
        self.assertEqual(set(receipt.data),{'sha256','byte_count'})
        self.assertEqual(receipt.data['sha256'].dtype,np.dtype('uint8'))
        self.assertEqual(receipt.data['sha256'].shape,(32,))
        self.assertEqual(receipt.data['sha256'].tobytes().hex(),self.digest)
        self.assertEqual(receipt.data['byte_count'].dtype,np.dtype('int64'))
        np.testing.assert_equal(receipt.data['byte_count'],[32])
        published=self.channel.published[0]
        self.assertEqual(published['exchange'],'')
        self.assertEqual(published['routing_key'],'matvey_reply_'+self.request_id)
        self.assertEqual(published['properties'].headers,{'tpu_pycloud_message_id':self.request_id})
        self.assertEqual(receipt.error_message,'')

    def test_pose_split_fixed_name_and_digest(self):
        self.headers['uri']='pose-split'
        self.consume()
        self.assertEqual(self.stage.call_args.kwargs,{'model':'pose-split'})
        self.assertEqual(self.fmt.replies[0].status_code,0)

    def test_model_paths_and_unknown_headers_rejected_without_writes(self):
        self.headers['uri']='file:///arbitrary/private/target'
        with patch.object(ua.tempfile,'TemporaryDirectory') as temp:
            self.consume();temp.assert_not_called()
        self.stage.assert_not_called()
        self.assertEqual(self.fmt.replies[0].error_message,'INVALID_MODEL')
        self.assertNotIn('arbitrary',str(self.fmt.replies))

    def test_unknown_header_does_not_get_copied_into_reply(self):
        self.headers['private']='private-value-marker'
        with patch.object(ua.tempfile,'TemporaryDirectory') as temp:
            self.consume();temp.assert_not_called()
        self.assertEqual(self.fmt.replies[0].error_message,'UNKNOWN_HEADERS')
        self.assertNotIn('private-value-marker',str(self.fmt.replies))

    def test_callback_must_be_single_generated_matching_notebook_queue(self):
        self.headers['response_routing_keys']=json.dumps(['arbitrary_queue'])
        with patch.object(ua.tempfile,'TemporaryDirectory') as temp:
            self.consume();temp.assert_not_called()
        self.assertEqual(self.channel.published,[])
        self.stage.assert_not_called()

    def test_invalid_id_no_reply_to_unverified_target(self):
        self.headers['tpu_pycloud_message_id']='not-a-uuid'
        self.consume()
        self.assertEqual(self.channel.published,[])
        self.stage.assert_not_called()

    def test_hash_rejection_has_no_filesystem_writes(self):
        self.fmt.decoded=({'program_bytes':np.zeros(32,dtype=np.uint8)},(),{'status_code':0})
        with patch.object(ua.tempfile,'TemporaryDirectory') as temp:
            self.consume();temp.assert_not_called()
        self.assertEqual(self.fmt.replies[0].error_message,'PROGRAM_HASH_MISMATCH')
        self.stage.assert_not_called()

    def test_bounds_unknown_fields_dtype_and_metadata(self):
        variants=[({'program_bytes':np.ones(2,dtype=object)},()),
                  ({'program_bytes':np.array([np.nan],dtype=np.float32)},()),
                  ({'program_bytes':np.zeros((2,2),dtype=np.uint8)},()),
                  ({'program_bytes':np.zeros(0,dtype=np.uint8)},()),
                  ({'program_bytes':np.zeros(33,dtype=np.uint8)},()),
                  ({'program_bytes':np.zeros(2,dtype=np.uint8),'path':'arbitrary'},()),
                  ({'program_bytes':np.zeros(2,dtype=np.uint8)},({'private':'metadata'},))]
        for data,metadata in variants:
            with self.subTest(dtype=type(data['program_bytes'])):
                self.agent._messages=0
                fmt=FormatFixture(data);fmt.decoded=(data,metadata,{'status_code':0})
                ch=ChannelFixture()
                with patch.object(ua,'MAX_PROGRAM_BYTES',32),patch.object(ua.tempfile,'TemporaryDirectory') as temp:
                    self.agent._consume(fmt,self.pika,ch,SimpleNamespace(delivery_tag=7),
                                        SimpleNamespace(headers=self.headers),b'body')
                    temp.assert_not_called()
                self.assertNotEqual(fmt.replies[0].status_code,0)
                self.assertEqual(ch.acked,[{'delivery_tag':7}])
        self.stage.assert_not_called()
        self.assertEqual(ua.MAX_PROGRAM_BYTES,8*1024*1024)

    def test_wrong_stage_receipt_never_reports_success(self):
        self.stage.side_effect=None
        self.stage.return_value={'status':'STAGED','program_name':'wrong.tpu',
                                 'program_sha256':self.digest,
                                 'namespace_owner':'matvey','program_path_namespace_verified':True}
        self.consume()
        self.assertEqual(self.fmt.replies[0].error_message,'INVALID_STAGE_RECEIPT')
        self.assertNotEqual(self.fmt.replies[0].status_code,0)

    def test_stage_exception_is_stable_code_no_path_or_credentials(self):
        self.stage.side_effect=FileExistsError('secret-path-and-credential-marker')
        self.consume()
        self.assertEqual(self.fmt.replies[0].error_message,'STAGE_FAILED')
        self.assertEqual(self.agent.last_error_type,'FileExistsError')
        self.assertNotIn('secret-path',str(self.fmt.replies))

    def test_reply_publish_failure_still_acknowledges_once_no_retry(self):
        self.channel.publish_failure=True
        self.consume()
        self.assertEqual(len(self.channel.published),1)
        self.assertEqual(self.agent.last_error_type,'ConnectionError')

    def test_only_uuid_upload_queue_namespace(self):
        for name in ['input','tpu.direct','notebook_other','notebook_upload_not-uuid','../target']:
            with self.assertRaises(ua.UploadError):
                ua.UploadAgent(SimpleNamespace(),'/auto/cache/fixture/matvey',name,self.stage)


    def test_message_limit_never_stages_extra_messages(self):
        self.agent._messages=ua.MAX_MESSAGES
        self.consume()
        self.stage.assert_not_called()
        self.assertEqual(self.channel.published,[])
        self.assertTrue(self.agent._stop.is_set())

    def test_unknown_worker_fields_rejected_without_writes(self):
        self.fmt.decoded[2]['private-field']='private-value'
        with patch.object(ua.tempfile,'TemporaryDirectory') as temp:
            self.consume();temp.assert_not_called()
        self.assertEqual(self.fmt.replies[0].error_message,'UNKNOWN_TASK_FIELDS')
        self.stage.assert_not_called()


class UploadLifecycleTests(unittest.TestCase):
    def test_ready_stop_copied_parameters_and_thread_owned_close(self):
        fmt=FormatFixture({});channel=ChannelFixture()
        closed=[];params=[]
        class Connection:
            def channel(self):return channel
            def process_data_events(self,time_limit):threading.Event().wait(min(time_limit,.01))
            def add_callback_threadsafe(self,callback):pass
            def close(self):closed.append(threading.get_ident())
        connection=Connection()
        fake_pika=SimpleNamespace(BlockingConnection=lambda value:params.append(value) or connection)
        original=SimpleNamespace(host='original-host',credentials='not-exported')
        imports=lambda name:fmt if name=='tpu_pycloud_format' else fake_pika
        with patch.object(ua.importlib,'import_module',side_effect=imports):
            handle=ua.start_agent(original,'/auto/cache/fixture/matvey','matvey_upload_'+str(uuid4()),lambda *a,**k:None)
            self.assertTrue(handle.wait_ready(1))
            self.assertTrue(handle.is_ready)
            self.assertTrue(handle.stop(1))
            self.assertFalse(handle.is_ready)
        self.assertEqual(len(closed),1)
        self.assertNotEqual(closed[0],threading.get_ident())
        self.assertEqual(params[0].connection_attempts,1)
        self.assertFalse(hasattr(original,'connection_attempts'))
        self.assertEqual(channel.qos,{'prefetch_count':1})
        self.assertFalse(channel.consumer['auto_ack'])
        self.assertTrue(channel.declared['auto_delete'])
        self.assertEqual(channel.deleted,[{'queue':channel.declared['queue']}])

    def test_startup_failure_reports_type_only(self):
        with patch.object(ua.importlib,'import_module',side_effect=ImportError('private-marker')):
            handle=ua.start_agent(SimpleNamespace(),'/auto/cache/fixture/matvey','matvey_upload_'+str(uuid4()),lambda *a,**k:None)
            self.assertFalse(handle.wait_ready(1))
            self.assertTrue(handle.stop(1))
        self.assertEqual(handle.last_error_type,'ImportError')
        self.assertNotIn('private-marker',str(handle.last_error_type))


if __name__=='__main__':unittest.main()
