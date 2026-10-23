import math
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import numpy as np

import test_linq_amqp as fixtures
from ml.linq import amqp
from ml.linq.backend import safe_transport


class PhaseTimingAndDropTests(unittest.TestCase):
    def setUp(self):fixtures.AmqpTransportTests.setUp(self)

    def test_finite_disjoint_phase_timings_on_initial_request(self):
        self.runner(self.inputs)
        timings=self.runner.last_response['timings']
        self.assertEqual(set(timings),set(amqp.TIMING_KEYS))
        for value in timings.values():self.assertTrue(math.isfinite(value) and value>=0)
        for key in amqp.TIMING_KEYS:self.assertGreater(timings[key],0)
        self.assertLessEqual(sum(value for key,value in timings.items() if key!='total_ms'),timings['total_ms'])
        self.assertEqual(self.runner.last_response['latency_kind'],'initial_call')

    def test_cache_is_distinct_and_does_not_report_network_phases(self):
        self.runner(self.inputs);request_id=self.runner.last_response['request_id']
        offline=amqp.AmqpRunner(None,journal_dir=self.journal_dir)
        offline.reconcile(request_id)
        self.assertEqual(offline.last_response['latency_kind'],'cached_response')
        for key in amqp.TIMING_KEYS:
            if key!='total_ms':self.assertEqual(offline.last_response['timings'][key],0)
        self.assertGreaterEqual(offline.last_response['timings']['total_ms'],0)
        self.assertEqual(len(self.channel.published),1)

    def test_serialize_failure_has_timing_but_no_publish_phase(self):
        self.fmt.serialize=lambda task:(_ for _ in ()).throw(ValueError('sensitive-marker'))
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        timings=self.runner.last_response['timings']
        self.assertGreater(timings['serialize_ms'],0)
        self.assertEqual(timings['publish_confirm_ms'],0)
        self.assertEqual(timings['response_wait_ms'],0)
        self.assertEqual(self.runner.last_response['journal_state'],'NOT_SUBMITTED')

    def test_connection_closed_after_confirm_reconciles_late_reply_once(self):
        original_publish=self.channel.basic_publish
        def close_after_confirm(**kwargs):
            confirmed=original_publish(**kwargs)
            self.connection.close()
            return confirmed
        self.channel.basic_publish=close_after_confirm
        self.channel.basic_get=lambda **kwargs:(_ for _ in ()).throw(ConnectionError('client connection is closed'))
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        record=self.runner.journal.load(request_id)
        self.assertEqual(record['state'],'UNKNOWN')
        self.assertTrue(record['broker_confirmed'])
        self.assertTrue(self.runner.last_response['publish_confirmed'])
        self.assertEqual(self.channel.deleted,[])
        properties=self.channel.published[0]['properties']
        late=fixtures.FakeChannel()
        late.basic_get=lambda **kwargs:(SimpleNamespace(delivery_tag=9),properties,b'late-response-fixture')
        late.basic_publish=lambda **kwargs:self.fail('reconnect cannot republish')
        late.queue_declare=lambda **kwargs:self.fail('reconnect cannot redeclare reply queue')
        connection=fixtures.FakeConnection(late)
        self.pika.BlockingConnection=lambda parameters:connection
        resumed=amqp.AmqpRunner(self.binding,journal_dir=self.journal_dir,timeout=1)
        outputs=resumed.reconcile(request_id)
        np.testing.assert_allclose(outputs['495'],[[.2,.8]])
        self.assertEqual(resumed.last_response['request_id'],request_id)
        self.assertEqual(resumed.last_response['response_id'],request_id)
        self.assertEqual(resumed.last_response['latency_kind'],'recovery_only')
        self.assertEqual(resumed.last_response['timings']['publish_confirm_ms'],0)
        self.assertEqual(resumed.last_response['timings']['serialize_ms'],0)
        self.assertEqual(len(self.channel.published),1)
        self.assertEqual(late.acked,[{'delivery_tag':9}])
        self.assertEqual(connection.closed,1)
        # A duplicate logical recovery is cached, never another network operation.
        self.pika.BlockingConnection=lambda parameters:self.fail('completed cache cannot reconnect')
        resumed.reconcile(request_id)
        self.assertEqual(resumed.last_response['latency_kind'],'cached_response')

    def test_foreign_late_reply_on_reconnect_is_preserved_not_acked(self):
        self.channel.publish_error=True
        with self.assertRaises(amqp.AmqpError):self.runner(self.inputs)
        request_id=self.runner.last_response['request_id']
        foreign=fixtures.FakeChannel()
        foreign.basic_get=lambda **kwargs:(SimpleNamespace(delivery_tag=11),
            SimpleNamespace(headers={'tpu_pycloud_message_id':'foreign-invalid-id'}),b'foreign')
        self.pika.BlockingConnection=lambda parameters:fixtures.FakeConnection(foreign)
        resumed=amqp.AmqpRunner(self.binding,journal_dir=self.journal_dir,timeout=1)
        with self.assertRaises(amqp.AmqpError):resumed.reconcile(request_id)
        self.assertEqual(self.runner.journal.load(request_id)['state'],'UNKNOWN')
        self.assertEqual(foreign.acked,[])
        self.assertEqual(foreign.deleted,[])
        self.assertEqual(foreign.published,[])
        self.assertEqual(len(self.channel.published),1)

    def test_typed_phase_allowlist_rejects_nonfinite_and_ignores_unknown_metadata(self):
        timings={key:1.25 for key in amqp.TIMING_KEYS}
        timings['password']='never-export-marker'
        result=safe_transport({'timings':timings})
        self.assertEqual(result['timings'],{key:1.25 for key in amqp.TIMING_KEYS})
        for key in amqp.TIMING_KEYS:
            for bad in [float('nan'),float('inf'),-1,True,'private-marker']:
                with self.subTest(key=key,bad=type(bad).__name__),self.assertRaises(ValueError):
                    safe_transport({'timings':{key:bad}})


if __name__=='__main__':unittest.main()
