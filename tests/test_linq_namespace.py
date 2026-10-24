import unittest
from unittest.mock import patch
import test_linq_amqp as fixtures
from ml.linq import amqp, upload_agent
from ml.linq.namespace import check_program_uri, check_reply_queue, reply_queue


class NamespaceTransportTests(unittest.TestCase):
    def setUp(self): fixtures.AmqpTransportTests.setUp(self)

    def test_unsafe_uri_rejected_before_connection_or_publish(self):
        for uri in [
            'file:///auto/cache/fixture/baseline/matvey_helmet.tpu?raw=False',
            'file:///auto/cache/foreign/matvey/matvey_helmet.tpu?raw=False',
            'file:///auto/cache/fixture/matvey/../mosprom_x_cut_ap9999.tpu?raw=False',
            'file:///auto/cache/fixture/matvey/mosprom_x_cut_ap9999.tpu?raw=False',
            'file:///auto/cache/fixture/matvey/matvey_%2e%2e.tpu?raw=False',
            'file:///auto/cache/fixture/helmet-v1.tpu?raw=False',
        ]:
            self.runner.program = uri
            with self.assertRaises(amqp.AmqpError) as error: self.runner(self.inputs)
            self.assertEqual(error.exception.details['code'], 'owned_namespace_required')
        self.assertEqual(self.parameters, [])
        self.assertEqual(self.channel.published, [])
        self.assertEqual(self.channel.deleted, [])

    def test_foreign_reply_factory_rejected_before_network(self):
        self.binding.reply_queue_factory = lambda request_id: 'notebook_' + request_id[:8]
        with self.assertRaises(amqp.AmqpError): self.runner(self.inputs)
        self.assertEqual(self.parameters, [])

    def test_unexpected_broker_queue_is_never_read_or_deleted(self):
        from types import SimpleNamespace
        self.channel.queue_declare = lambda **kwargs: SimpleNamespace(method=SimpleNamespace(queue='foreign'))
        with self.assertRaises(amqp.AmqpError): self.runner(self.inputs)
        self.assertEqual(self.channel.published, [])
        self.assertEqual(self.channel.deleted, [])
        self.assertEqual(self.channel.get_count, 0)

    def test_legacy_owned_receive_requires_exact_reviewed_uuid(self):
        self.channel.publish_error = True
        with self.assertRaises(amqp.AmqpError): self.runner(self.inputs)
        request_id = self.runner.last_response['request_id']
        self.runner.journal.update(request_id, reply_queue='notebook_' + request_id[:8])
        self.channel.publish_error = False
        unreviewed = amqp.AmqpRunner(self.binding, journal_dir=self.journal_dir)
        with self.assertRaises(amqp.AmqpError): unreviewed.reconcile(request_id)
        self.assertEqual(len(self.parameters), 1)
        self.assertEqual(self.channel.get_count, 0)
        reviewed = amqp.AmqpRunner(self.binding, journal_dir=self.journal_dir,
                                  legacy_request_ids=[request_id])
        reviewed.reconcile(request_id)
        self.assertEqual(reviewed.last_response['journal_state'], 'COMPLETED')
        self.assertEqual(len(self.channel.published), 1)

    def test_foreign_direct_upload_queue_blocked(self):
        self.runner.purpose='model_upload';self.runner.program='helmet'
        self.binding.request_exchange='';self.binding.request_routing_key='notebook_upload_foreign'
        with self.assertRaises(amqp.AmqpError): self.runner(self.inputs)
        self.assertEqual(self.parameters, [])


class NamespacePureTests(unittest.TestCase):
    def test_old_video_name_cannot_submit_even_with_reviewed_hash(self):
        import hashlib
        from pathlib import Path
        import tempfile
        from ml.linq import video
        from ml.linq.backend import PendingRequestError
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);program=root/'program.tpu';program.write_bytes(b'fixture')
            digest=hashlib.sha256(b'fixture').hexdigest()
            manifest={'model_id':'helmet-v1','program_name':'helmet-v1.tpu',
                'program_sha256':digest,'program_path':str(program),
                'rpc_state_dir':str(root/'rpc/helmet-v1'),'journal_dir':str(root/'requests'),
                'format_source_manifest':'unused','inputs':[{'name':'images','shape':[1,1],'dtype':'float32'}],
                'outputs':[{'name':'output0','shape':[1,1],'dtype':'float32'}]}
            import numpy as np
            with patch.dict(video._MODELS,{'helmet-v1':('matvey_helmet-v1.tpu',digest)}), \
                 patch.dict('os.environ',{'LINQ_LOGIN':'fixture'}), \
                 patch.object(video.DurableVideoRunner,'_binding') as binding:
                runner=video.DurableVideoRunner(manifest)
                with self.assertRaises(PendingRequestError):
                    runner({'images':np.zeros((1,1),np.float32)},
                           {'request_id':'epoch:0:helmet-v1','model_id':'helmet-v1','program_sha256':digest})
                binding.assert_not_called()

    def test_protected_upload_filename_never_creates_source_file(self):
        import hashlib
        import numpy as np
        from types import SimpleNamespace
        blob = b'fixture-program'
        fmt = SimpleNamespace(deserialize=lambda body: ({'program_bytes': np.frombuffer(blob,np.uint8)},(),{'status_code':0}))
        for name in ['mosprom_captain_cut_ap9999.tpu', 'matvey_../foreign.tpu']:
            with patch.dict(upload_agent._MODELS, {'helmet': (name,hashlib.sha256(blob).hexdigest())}), \
                 patch.object(upload_agent,'_cache_namespace',return_value=__import__('pathlib').Path('/auto/cache/fixture/matvey')), \
                 patch.object(upload_agent.tempfile,'TemporaryDirectory') as temporary:
                with self.assertRaises(upload_agent.UploadError):
                    upload_agent._stage_payload(fmt,b'body','/auto/cache/fixture/matvey','helmet',lambda:None)
                temporary.assert_not_called()

    def test_upload_symlink_escape_rejected_before_temp_files_or_thread(self):
        from pathlib import Path
        with patch.object(Path,'resolve',return_value=Path('/auto/cache/fixture/baseline')), \
             patch.object(upload_agent.tempfile,'TemporaryDirectory') as temporary, \
             patch.object(upload_agent.threading,'Thread') as thread:
            with self.assertRaises(upload_agent.UploadError):
                upload_agent.UploadAgent(None,'/auto/cache/fixture/matvey',
                    'matvey_upload_00000000-0000-0000-0000-000000000001',lambda:None)
            temporary.assert_not_called();thread.assert_not_called()

    def test_owned_uri_and_full_uuid_queue(self):
        value='00000000-0000-0000-0000-000000000001'
        self.assertEqual(check_reply_queue(reply_queue(value),value), 'matvey_reply_'+value)
        with self.assertRaises(ValueError): check_reply_queue('matvey_reply_foreign',value)
        check_program_uri('file:///auto/cache/fixture/matvey/matvey_helmet-v1.tpu?raw=False','fixture')

    def test_upload_foreign_cache_or_queue_rejected_without_thread(self):
        with patch.object(upload_agent.threading, 'Thread') as thread:
            for cache in ['/auto/cache/fixture', '/auto/cache/fixture/baseline', '/tmp/matvey',
                          '/auto/cache/fixture/matvey/../baseline']:
                with self.assertRaises(upload_agent.UploadError):
                    upload_agent.UploadAgent(None,cache,'matvey_upload_00000000-0000-0000-0000-000000000001',lambda:None)
            with self.assertRaises(upload_agent.UploadError):
                upload_agent.UploadAgent(None,'/auto/cache/fixture/matvey','foreign',lambda:None)
            thread.assert_not_called()


if __name__ == '__main__': unittest.main()
