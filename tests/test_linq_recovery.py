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
