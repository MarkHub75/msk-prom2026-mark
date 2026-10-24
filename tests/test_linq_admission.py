import json
from pathlib import Path
import select
import subprocess
import sys
import unittest
from unittest.mock import patch
from uuid import uuid4
import test_linq_amqp as fixtures
from ml.linq import amqp
from ml.linq.admission import MatveyAdmission
import ml.linq.admission as admission_module


class GlobalAdmissionTests(unittest.TestCase):
    def setUp(self): fixtures.AmqpTransportTests.setUp(self)

    def other_runner(self):
        return amqp.AmqpRunner(self.binding,self.runner.program,
                              journal_dir=Path(self.journal_dir)/'second-run',timeout=1)

    def test_pointer_durable_before_connection_and_no_credentials(self):
        original=self.pika.BlockingConnection
        observed=[]
        def connect(parameters):
            pointer=json.loads(self.runner.admission.pointer.read_text())
            self.assertEqual(set(pointer),{'schema_version','request_id','journal_path'})
            self.assertEqual(pointer['request_id'],self.runner.last_response['request_id'])
            self.assertEqual(Path(pointer['journal_path']),self.runner.journal.path(pointer['request_id'])/'request.json')
            self.assertEqual(self.runner.journal.load(pointer['request_id'])['state'],'NOT_SUBMITTED')
            observed.append(True)
            return original(parameters)
        self.pika.BlockingConnection=connect
        self.runner(self.inputs)
        self.assertEqual(observed,[True])
        self.assertFalse(self.runner.admission.pointer.exists())
        self.assertTrue((self.runner.admission.directory/'.lock').exists())

    def test_unknown_survives_restart_and_blocks_different_journal_until_same_uuid_reconciled(self):
        self.channel.publish_error=True
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        pointer=self.runner.admission.pointer.read_bytes()
        other=self.other_runner()
        with self.assertRaises(amqp.AmqpError) as error:other(self.inputs)
        self.assertEqual(error.exception.details['code'],'matvey_pending_request_requires_reconcile')
        self.assertEqual(len(self.channel.published),1)
        self.assertEqual(len(self.parameters),1)
        self.assertEqual(self.runner.admission.pointer.read_bytes(),pointer)
        self.channel.publish_error=False
        recovered=amqp.AmqpRunner(self.binding,journal_dir=self.journal_dir,timeout=1)
        recovered.reconcile(request_id)
        self.assertFalse(recovered.admission.pointer.exists())
        self.assertEqual(len(self.channel.published),1)  # receive-only
        get=self.channel.basic_get
        def latest(**kwargs):
            method,properties,body=get(**kwargs)
            return method,self.channel.published[-1]['properties'],body
        self.channel.basic_get=latest
        other(self.inputs)
        self.assertEqual(len(self.channel.published),2)

    def test_before_publish_failure_releases_only_durable_not_submitted(self):
        self.pika.BlockingConnection=lambda params: (_ for _ in ()).throw(ConnectionError('fixture'))
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        self.assertEqual(self.runner.journal.load(self.runner.last_response['request_id'])['state'],'NOT_SUBMITTED')
        self.assertFalse(self.runner.admission.pointer.exists())

    def test_process_death_at_publish_keeps_submitting_fence(self):
        def crash(**kwargs):
            self.channel.published.append(kwargs)
            raise SystemExit('simulated process loss')
        self.channel.basic_publish=crash
        with self.assertRaises(SystemExit):self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        self.assertEqual(self.runner.journal.load(request_id)['state'],'SUBMITTING')
        self.assertTrue(self.runner.admission.pointer.exists())
        with self.assertRaises(amqp.AmqpError):self.other_runner()(self.inputs)
        self.assertEqual(len(self.channel.published),1)

    def test_correlated_service_failure_releases_fence_without_republication(self):
        self.response[2]['status_code']=3
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        self.assertEqual(self.runner.journal.load(self.runner.last_response['request_id'])['state'],'SERVICE_FAILED')
        self.assertFalse(self.runner.admission.pointer.exists())

    def test_cross_process_global_flock_blocks_before_any_connection(self):
        directory=self.runner.admission.directory
        code=('from ml.linq.admission import MatveyAdmission; import sys\n'
              'with MatveyAdmission(sys.argv[1]).session():\n'
              ' print("ready",flush=True)\n'
              ' sys.stdin.read(1)\n')
        child=subprocess.Popen([sys.executable,'-c',code,str(directory)],stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            self.assertTrue(select.select([child.stdout],[],[],5)[0])
            self.assertEqual(child.stdout.readline(),b'ready\n')
            with self.assertRaises(amqp.AmqpError) as error:self.other_runner()(self.inputs)
            self.assertEqual(error.exception.details['code'],'matvey_admission_busy')
            self.assertEqual(self.parameters,[])
        finally:
            if child.poll() is None:
                child.stdin.write(b'x');child.stdin.flush()
            child.communicate(timeout=5)
        self.assertEqual(child.returncode,0)

    def test_cached_terminal_is_offline_even_while_global_lock_held(self):
        self.runner(self.inputs);request_id=self.runner.last_response['request_id']
        offline=amqp.AmqpRunner(None,journal_dir=self.journal_dir)
        with MatveyAdmission(self.runner.admission.directory).session(), \
             patch.object(offline,'_open',side_effect=AssertionError('must remain offline')):
            offline.reconcile(request_id)
        self.assertTrue(offline.last_response['cached_response'])

    def test_corrupt_terminal_response_and_failed_fsync_do_not_release(self):
        self.runner(self.inputs);request_id=self.runner.last_response['request_id']
        admission=self.runner.admission
        with admission.session():admission.claim(self.runner.journal,request_id)
        # Restore a terminal fence as if the previous process stopped before cleanup.
        pointer={'schema_version':'1.0','request_id':request_id,
                 'journal_path':str(self.runner.journal.path(request_id)/'request.json')}
        from ml.linq.journal import atomic_json
        atomic_json(admission.pointer,pointer)
        with patch.object(admission_module,'fsync_directory',side_effect=OSError('fsync fixture')):
            self.assertFalse(admission._safe(pointer))
        self.assertTrue(admission.pointer.exists())
        (self.runner.journal.path(request_id)/'response.npz').write_bytes(b'corrupt')
        with self.assertRaises(amqp.AmqpError):self.other_runner()(self.inputs)
        self.assertTrue(admission.pointer.exists())
        self.assertEqual(len(self.channel.published),1)


if __name__=='__main__':unittest.main()
