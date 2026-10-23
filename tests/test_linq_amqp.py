from contextlib import redirect_stdout
from dataclasses import dataclass
import importlib.metadata
import io
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from ml.linq import amqp


@dataclass
class FakeTask:
    data: object


class FakeClock:
    def __init__(self):self.value=0
    def __call__(self):self.value+=.01;return self.value


class FakeChannel:
    def __init__(self):
        self.published=[];self.acked=[];self.bindings=[];self.get_count=0;self.deleted=[];self.delete_error=False
        self.timeout=False;self.mismatch=False;self.publish_error=False
    def queue_declare(self,**kwargs):
        self.queue_config=kwargs
        return SimpleNamespace(method=SimpleNamespace(queue=kwargs['queue'] or 'exclusive-fixture'))
    def queue_bind(self,**kwargs):self.bindings.append(kwargs)
    def queue_delete(self,**kwargs):
        self.deleted.append(kwargs)
        if self.delete_error:raise RuntimeError("private-delete-marker")
    def confirm_delivery(self):pass
    def basic_publish(self,**kwargs):
        self.published.append(kwargs)
        if self.publish_error:raise ConnectionError('private-password-marker')
        return True
    def basic_get(self,**kwargs):
        self.get_count+=1
        if self.timeout:return None,None,None
        properties=self.published[0]['properties']
        if self.mismatch:properties=SimpleNamespace(headers={'tpu_pycloud_message_id':'wrong'})
        return SimpleNamespace(delivery_tag=3),properties,b'response-fixture'
    def basic_ack(self,**kwargs):self.acked.append(kwargs)


class FakeConnection:
    def __init__(self,channel):self.the_channel=channel;self.closed=0
    def channel(self):return self.the_channel
    def process_data_events(self,**kwargs):pass
    def close(self):self.closed+=1


class AmqpTransportTests(unittest.TestCase):
    def setUp(self):
        self.journal_tmp=tempfile.TemporaryDirectory();self.addCleanup(self.journal_tmp.cleanup)
        self.journal_dir=self.journal_tmp.name
        self.channel=FakeChannel();self.connection=FakeConnection(self.channel);self.parameters=[]
        self.inputs={'input.1':np.ones((1,2),dtype=np.float32)}
        self.response=({'495':np.array([[.2,.8]],dtype=np.float32)},(),
                       {'status_code':0,'error_message':'private-worker-error-marker'})
        self.fmt=SimpleNamespace(PyTask=FakeTask,serialize=lambda task:b'official-fixture',
            deserialize=lambda body:self.response,MESSAGE_ID_ATTR_NAME='tpu_pycloud_message_id',
            RESPONSE_ROUTING_KEYS_ATTR_NAME='response_routing_keys',TARGET_URI_ATTR_NAME='uri')
        def connect(parameters):self.parameters.append(parameters);return self.connection
        self.pika=SimpleNamespace(BlockingConnection=connect,
            BasicProperties=lambda **kwargs:SimpleNamespace(**kwargs))
        self.addCleanup(patch.stopall)
        patch.object(amqp,'_load_format',return_value=self.fmt).start()
        patch('ml.linq.amqp.importlib.import_module',side_effect=lambda name:self.pika if name=='pika' else self.fmt).start()
        patch.object(amqp,'monotonic',new=FakeClock()).start()
        self.original=SimpleNamespace(host='unlogged-host',port=5672,credentials='private-credential-marker')
        self.binding=amqp.official_binding(self.original,request_exchange='explicit-request-exchange',
            request_routing_key='explicit-worker-key',reply_exchange='explicit-reply-exchange',
            output_names=['495'])
        self.runner=amqp.AmqpRunner(self.binding,'file:///explicit/program.tpu?raw=False',timeout=1,journal_dir=self.journal_dir)

    def test_official_headers_tuple_and_one_publish_close(self):
        output=self.runner(self.inputs)
        self.assertEqual(list(output),['495'])
        self.assertEqual(len(self.channel.published),1)
        publish=self.channel.published[0]
        self.assertEqual(publish['exchange'],'explicit-request-exchange')
        self.assertEqual(publish['routing_key'],'explicit-worker-key')
        self.assertTrue(publish['mandatory'])
        headers=publish['properties'].headers
        self.assertEqual(headers['tpu_pycloud_message_id'],self.runner.last_response['request_id'])
        self.assertEqual(json.loads(headers['response_routing_keys']),['exclusive-fixture'])
        self.assertEqual(headers['uri'],'file:///explicit/program.tpu?raw=False')
        self.assertEqual(self.channel.queue_config,dict(queue='',durable=False,exclusive=False,auto_delete=True))
        self.assertEqual(self.channel.bindings,[dict(queue='exclusive-fixture',exchange='explicit-reply-exchange',routing_key='exclusive-fixture')])
        self.assertEqual(self.connection.closed,1)
        self.assertEqual(self.runner.last_response['status_code'],0)
        self.assertEqual(self.runner.last_response['response_id'],self.runner.last_response['request_id'])
        self.assertEqual(self.channel.deleted,[{'queue':'exclusive-fixture'}])
        self.assertNotIn('private-worker-error-marker',json.dumps(self.runner.last_response))
        self.assertNotIn('uri',json.dumps(self.runner.last_response))

    def test_id_mismatch_stops_no_retry_and_closes(self):
        self.channel.mismatch=True
        with self.assertRaises(amqp.AmqpError) as error:self.runner(self.inputs)
        self.assertEqual(error.exception.details['code'],'response_id_mismatch')
        self.assertIsNone(self.runner.last_response['response_id'])
        self.assertEqual(len(self.channel.published),1)
        self.assertEqual(self.connection.closed,1)
        self.assertEqual(self.channel.acked,[])

    def test_timeout_leaves_remote_unknown_and_closes(self):
        self.channel.timeout=True
        with self.assertRaises(amqp.AmqpError) as error:self.runner(self.inputs)
        self.assertEqual(error.exception.details['code'],'response_timeout')
        self.assertEqual(self.runner.last_response['remote_completion'],'unknown')
        self.assertEqual(self.channel.deleted,[])
        self.assertEqual(self.runner.last_response['reply_queue_cleanup'],'retained_for_recovery')
        self.assertEqual(len(self.channel.published),1)
        self.assertEqual(self.connection.closed,1)

    def test_nonzero_status_no_outputs_or_worker_error_dump(self):
        self.response[2]['status_code']=17
        with self.assertRaises(amqp.AmqpError) as error:self.runner(self.inputs)
        self.assertEqual(error.exception.details['status_code'],17)
        self.assertEqual(self.runner.last_response['journal_state'],'SERVICE_FAILED')
        self.assertEqual(self.channel.acked,[{'delivery_tag':3}])
        self.assertEqual(self.connection.closed,1)
        self.assertEqual(self.runner.last_response['service_error'],'private-worker-error-marker')

    def test_serialization_failure_closes_before_publish(self):
        def fail(task):raise RuntimeError('private-codec-marker')
        self.fmt.serialize=fail
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        self.assertEqual(self.channel.published,[])
        self.assertEqual(self.connection.closed,1)
        self.assertEqual(self.runner.last_response['error']['phase'],'serialize_request')
        self.assertNotIn('private-codec-marker',json.dumps(self.runner.last_response))

    def test_publish_exception_is_one_ambiguous_attempt(self):
        self.channel.publish_error=True
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        self.assertEqual(len(self.channel.published),1)
        self.assertEqual(self.runner.last_response['remote_completion'],'unknown')
        self.assertTrue(self.runner.last_response['publish_attempted'])
        self.assertFalse(self.runner.last_response['publish_confirmed'])
        self.assertEqual(self.connection.closed,1)
        self.assertNotIn('private-password-marker',json.dumps(self.runner.last_response))

    def test_copied_parameters_have_bounded_timeouts_no_retries(self):
        self.runner(self.inputs)
        params=self.parameters[0]
        self.assertEqual((params.host,params.port),('127.0.0.1',15672))
        self.assertEqual((params.connection_attempts,params.retry_delay),(1,0))
        self.assertTrue(0<params.socket_timeout<=1)
        self.assertTrue(0<params.stack_timeout<=1)
        self.assertTrue(0<params.blocked_connection_timeout<=1)
        self.assertEqual(self.original.host,'unlogged-host')
        self.assertFalse(hasattr(self.original,'socket_timeout'))

    def test_missing_format_never_connects(self):
        with patch.object(amqp,'_load_format',side_effect=amqp.AmqpError('official_format_missing','load_format')):
            with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        self.assertEqual(self.parameters,[])
        self.assertEqual(self.runner.last_response['next_action'],'provide_exact_official_tpu_pycloud_format_0_0_1')

    def test_wrong_target_never_connects(self):
        runner=amqp.AmqpRunner(self.binding,'explicit-uri',host='remote-host',journal_dir=self.journal_dir)
        with self.assertRaises(amqp.AmqpError):runner(self.inputs)
        self.assertEqual(self.parameters,[])

    def test_nonfinite_outputs_rejected(self):
        self.response[0]['495'][:]=np.inf
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        self.assertEqual(self.connection.closed,1)
        self.assertEqual(self.runner.last_response['status'],'failed')

    def test_invalid_task_type_never_serialized(self):
        self.binding.task_factory=lambda *args:{'not':'official PyTask'}
        with self.assertRaises(amqp.AmqpError) as error:self.runner(self.inputs)
        self.assertEqual(error.exception.details['code'],'task_factory_must_return_official_pytask')
        self.assertEqual(self.channel.published,[])
        self.assertEqual(self.connection.closed,1)

    def test_default_reply_exchange_explicit_no_bind(self):
        binding=amqp.official_binding(self.original,request_exchange='',request_routing_key='explicit',
                                     reply_exchange='',output_names=['495'])
        amqp.AmqpRunner(binding,'explicit-uri',journal_dir=self.journal_dir)(self.inputs)
        self.assertEqual(self.channel.bindings,[])


    def test_explicit_stock_queue_name_factory(self):
        self.binding.reply_queue_factory=lambda request_id:'notebook_'+request_id[:8]
        self.runner(self.inputs)
        self.assertEqual(self.channel.queue_config['queue'],'notebook_'+self.runner.last_response['request_id'][:8])
        self.assertFalse(self.channel.queue_config['exclusive'])

    def test_service_error_sanitizes_known_password_and_uri_auth(self):
        self.original.credentials=SimpleNamespace(password='super-private-value')
        self.response[2]['status_code']=2
        self.response[2]['error_message']='missing program.tpu super-private-value https://user:other-secret@host/path token=hidden-value'
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        text=self.runner.last_response['service_error']
        self.assertIn('missing program.tpu',text)
        for secret in ['super-private-value','other-secret','hidden-value']:
            self.assertNotIn(secret,text)
        self.assertLessEqual(len(text),1024)


    def test_cleanup_failure_never_prevents_connection_close(self):
        self.channel.delete_error=True
        self.runner(self.inputs)
        self.assertEqual(self.connection.closed,1)
        self.assertEqual(self.runner.last_response['reply_queue_cleanup'],'failed')
        self.assertNotIn('private-delete-marker',json.dumps(self.runner.last_response))

    def test_actual_mismatching_uuid_is_recorded_before_rejection(self):
        from uuid import uuid4
        actual=str(uuid4())
        self.binding.get_response_id=lambda response,properties:actual
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        self.assertEqual(self.runner.last_response['response_id'],actual)
        self.assertEqual(self.connection.closed,1)


class FormatAndConfigTests(unittest.TestCase):
    def test_wrong_format_version_rejected(self):
        with patch('ml.linq.amqp.importlib.metadata.version',return_value='0.0.2'), \
             patch('ml.linq.amqp.importlib.import_module') as imported:
            with self.assertRaises(amqp.AmqpError) as error:amqp._load_format()
        self.assertEqual(error.exception.details['code'],'official_format_wrong_version')
        imported.assert_not_called()

    def test_missing_format_cli_action_error_before_loading_binding(self):
        stream=io.StringIO()
        with patch('ml.linq.amqp.importlib.metadata.version',side_effect=importlib.metadata.PackageNotFoundError), \
             patch('ml.linq.amqp._load_binding') as binding, redirect_stdout(stream):
            code=amqp.main(['--binding','nonexistent:factory','--program','explicit-uri',
                '--input-npz','no-file','--output-dir','no-output'])
        self.assertEqual(code,1)
        binding.assert_not_called()
        value=json.loads(stream.getvalue())
        self.assertEqual(value['error']['code'],'official_format_missing')
        self.assertIn('next_action',value)

    def test_private_config_allowlist_and_no_echo(self):
        calls=[]
        fake=SimpleNamespace(PlainCredentials=lambda u,p:('private',u,p),
            ConnectionParameters=lambda **kw:calls.append(kw) or SimpleNamespace(**kw))
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'private.json'
            path.write_text(json.dumps({'username':'configured-user','password':'private-password-marker','virtual_host':'configured-vhost'}))
            with patch('ml.linq.amqp.importlib.import_module',return_value=fake):
                params=amqp._environment_parameters(path)
            self.assertEqual(params.virtual_host,'configured-vhost')
            self.assertEqual(params.credentials[2],'private-password-marker')
            path.write_text(json.dumps({'username':'configured-user','password':'private-password-marker','virtual_host':'configured-vhost','unapproved':'private-extra-marker'}))
            with self.assertRaises(amqp.AmqpError) as error:amqp._environment_parameters(path)
            self.assertNotIn('private-password-marker',str(error.exception))
            self.assertNotIn('private-extra-marker',json.dumps(error.exception.details))

    def test_no_default_credentials(self):
        with patch.dict('os.environ',{},clear=True):
            with self.assertRaises(amqp.AmqpError) as error:amqp._environment_parameters()
        self.assertEqual(error.exception.details['code'],'explicit_broker_credentials_and_vhost_required')


if __name__=='__main__':unittest.main()
