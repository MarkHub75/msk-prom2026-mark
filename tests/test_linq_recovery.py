import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from uuid import uuid4

import numpy as np
import test_linq_amqp as fixtures
from ml.linq import amqp
from ml.linq.journal import RequestJournal


class RequestRecoveryTests(unittest.TestCase):
    def setUp(self):fixtures.AmqpTransportTests.setUp(self)

    def test_response_fsynced_and_terminal_before_ack(self):
        observed=[]
        def acknowledge(**kwargs):
            request_id=self.runner.last_response['request_id']
            journal=RequestJournal(self.journal_dir)
            record=journal.load(request_id)
            self.assertEqual(record['state'],'COMPLETED')
            np.testing.assert_allclose(journal.outputs(request_id)['495'],[[.2,.8]])
            observed.append(True)
        self.channel.basic_ack=acknowledge
        self.runner(self.inputs)
        self.assertEqual(observed,[True])

    def test_publish_loss_unknown_retains_queue_and_no_retry(self):
        self.channel.publish_error=True
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        record=RequestJournal(self.journal_dir).load(request_id)
        self.assertEqual(record['state'],'UNKNOWN')
        self.assertEqual(self.channel.deleted,[])
        self.assertEqual(len(self.channel.published),1)
        self.assertEqual(self.connection.closed,1)

    def test_cached_completed_reconcile_without_binding_or_network(self):
        self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        offline=amqp.AmqpRunner(None,journal_dir=self.journal_dir)
        with patch.object(amqp,'_load_format',side_effect=AssertionError('must not import network deps')):
            outputs=offline.reconcile(request_id)
            again=offline.reconcile(request_id)
        np.testing.assert_equal(outputs['495'],again['495'])
        self.assertTrue(offline.last_response['cached_response'])
        self.assertEqual(offline.last_response['status_code'],0)
        self.assertEqual(len(self.channel.published),1)

    def test_capture_and_upload_context_pointers_exist_before_network_and_survive_save(self):
        from ml.linq.notebook import capture_call
        context=Path(self.journal_dir)/'capture'
        program=Path(self.journal_dir)/'fixture.tpu';program.write_bytes(b'test-program')
        self.runner.capture_dir=context
        original=self.pika.BlockingConnection
        checked=[]
        def connect(parameters):
            pointer=json.loads((context/'request-pointer.json').read_text())
            capture=json.loads((context/'capture.json').read_text())
            self.assertEqual(pointer['journal_request_id'],self.runner.last_response['request_id'])
            self.assertEqual(capture['journal_request_id'],pointer['journal_request_id'])
            record=self.runner.journal.load(pointer['journal_request_id'])
            self.assertEqual(record['state'],'NOT_SUBMITTED')
            self.assertEqual(record['capture_id'],capture['capture_id'])
            checked.append(True)
            return original(parameters)
        self.pika.BlockingConnection=connect
        result=capture_call(self.runner,inputs=self.inputs,output_names=['495'],
            program_path=program,output_dir=context,model_id='mock-model')
        self.assertEqual(result['status'],'completed')
        self.assertEqual(checked,[True])
        self.assertEqual(result['journal_request_id'],self.runner.last_response['request_id'])
        saved=json.loads((context/'capture.json').read_text())
        self.assertEqual(saved['journal_request_id'],result['journal_request_id'])

    def test_upload_context_without_capture_json_gets_durable_pointer(self):
        context=Path(self.journal_dir)/'upload-context'
        self.runner.capture_dir=context;self.runner.purpose='model_upload'
        self.runner(self.inputs)
        pointer=json.loads((context/'request-pointer.json').read_text())
        self.assertEqual(pointer['purpose'],'model_upload')
        record=self.runner.journal.load(pointer['journal_request_id'])
        self.assertEqual(record['capture_dir'],str(context.resolve()))
        self.assertFalse((context/'capture.json').exists())

    def test_cli_offline_cache_does_not_need_credentials_format_or_program(self):
        from contextlib import redirect_stdout
        from io import StringIO
        self.runner(self.inputs)
        request_id=self.runner.last_response['request_id'];output=StringIO()
        with patch.object(amqp,'_load_format',side_effect=AssertionError('network dependency must not load')), \
             patch.object(amqp,'_environment_parameters',side_effect=AssertionError('must not read credentials')), \
             redirect_stdout(output):
            code=amqp.main(['--reconcile',request_id,'--journal-dir',self.journal_dir])
        self.assertEqual(code,0)
        value=json.loads(output.getvalue())
        self.assertTrue(value['response']['cached_response'])
        self.assertEqual(len(self.channel.published),1)

    def test_pending_reconcile_receives_without_any_publish_or_queue_declare(self):
        self.channel.publish_error=True
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        self.channel.publish_error=False
        self.channel.queue_declare=lambda **kwargs:self.fail('reconcile must not declare any queue')
        self.channel.basic_publish=lambda **kwargs:self.fail('reconcile must never publish')
        recovered=amqp.AmqpRunner(self.binding,journal_dir=self.journal_dir,timeout=1)
        outputs=recovered.reconcile(request_id)
        np.testing.assert_allclose(outputs['495'],[[.2,.8]])
        self.assertEqual(recovered.last_response['journal_state'],'COMPLETED')

    def test_crash_at_publish_leaves_submitting_then_restart_recovers_only(self):
        def crash(**kwargs):
            self.channel.published.append(kwargs)
            raise SystemExit('simulated process death')
        self.channel.basic_publish=crash
        with self.assertRaises(SystemExit):self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        self.assertEqual(self.runner.journal.load(request_id)['state'],'SUBMITTING')
        self.assertEqual(self.channel.deleted,[])
        self.channel.basic_publish=lambda **kwargs:self.fail('no republish on restart')
        recovered=amqp.AmqpRunner(self.binding,journal_dir=self.journal_dir,timeout=1)
        recovered.reconcile(request_id)
        self.assertEqual(recovered.last_response['journal_state'],'COMPLETED')
        self.assertEqual(len(self.channel.published),1)

    def test_crash_after_broker_confirmation_before_accepted_commit(self):
        update=self.runner.journal.update
        def crash(request_id,state=None,**fields):
            if state=='ACCEPTED':raise SystemExit('simulated crash before journal accepted commit')
            return update(request_id,state,**fields)
        self.runner.journal.update=crash
        with self.assertRaises(SystemExit):self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        self.assertEqual(self.runner.journal.load(request_id)['state'],'SUBMITTING')
        self.assertEqual(len(self.channel.published),1)
        self.assertEqual(self.channel.deleted,[])
        recovered=amqp.AmqpRunner(self.binding,journal_dir=self.journal_dir,timeout=1)
        recovered.reconcile(request_id)
        self.assertEqual(recovered.last_response['journal_state'],'COMPLETED')

    def test_network_loss_before_publish_stays_not_submitted_and_cleans_queue(self):
        self.fmt.serialize=lambda task:(_ for _ in ()).throw(ConnectionError('private-error-marker'))
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        record=self.runner.journal.load(request_id)
        self.assertEqual(record['state'],'NOT_SUBMITTED')
        self.assertEqual(self.channel.published,[])
        self.assertEqual(self.channel.deleted,[{'queue':'exclusive-fixture'}])
        self.assertNotIn('private-error-marker',json.dumps(record))

    def test_response_commit_failure_does_not_ack_or_delete_queue(self):
        self.runner.journal.complete=lambda *args,**kwargs:(_ for _ in ()).throw(OSError('disk-private-marker'))
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        self.assertEqual(self.runner.journal.load(request_id)['state'],'UNKNOWN')
        self.assertEqual(self.channel.acked,[])
        self.assertEqual(self.channel.deleted,[])
        self.assertEqual(self.connection.closed,1)

    def test_ack_loss_preserves_completed_response_without_resubmission(self):
        def lost_ack(**kwargs):raise ConnectionError('private-ack-marker')
        self.channel.basic_ack=lost_ack
        outputs=self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        self.assertEqual(self.runner.journal.load(request_id)['state'],'COMPLETED')
        self.assertEqual(self.runner.last_response['ack_error_type'],'ConnectionError')
        cached=amqp.AmqpRunner(None,journal_dir=self.journal_dir).reconcile(request_id)
        np.testing.assert_equal(cached['495'],outputs['495'])
        self.assertEqual(len(self.channel.published),1)

    def test_foreign_id_is_not_acked_or_deleted_and_journal_remains_unknown(self):
        self.channel.mismatch=True
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        self.assertEqual(self.runner.journal.load(request_id)['state'],'UNKNOWN')
        self.assertEqual(self.channel.acked,[])
        self.assertEqual(self.channel.deleted,[])
        self.assertEqual(self.connection.closed,1)

    def test_service_failure_durable_before_ack_and_cached_offline(self):
        self.response[2]['status_code']=7
        def acknowledge(**kwargs):
            request_id=self.runner.last_response['request_id']
            self.assertEqual(self.runner.journal.load(request_id)['state'],'SERVICE_FAILED')
        self.channel.basic_ack=acknowledge
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        offline=amqp.AmqpRunner(None,journal_dir=self.journal_dir)
        with patch.object(amqp,'_load_format',side_effect=AssertionError('no network')):
            with self.assertRaises(amqp.AmqpError) as error:offline.reconcile(request_id)
        self.assertEqual(error.exception.details['status_code'],7)
        self.assertEqual(offline.last_response['journal_state'],'SERVICE_FAILED')

    def test_journal_excludes_uri_auth_and_worker_error_strings(self):
        self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        value=(self.runner.journal.path(request_id)/'request.json').read_text()
        for secret in ['file:///explicit','unlogged-host','private-credential-marker','private-worker-error-marker']:
            self.assertNotIn(secret,value)
        record=json.loads(value)
        self.assertEqual(len(record['program_uri_sha256']),64)
        self.assertEqual(record['input_artifact']['file'],'inputs.npz')
