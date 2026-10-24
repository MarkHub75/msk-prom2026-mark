import hashlib
import io
from pathlib import Path
import tempfile
import unittest
import json
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4
import zipfile
from ml.pipeline import upload_bootstrap as module


class UploadBootstrapTest(unittest.TestCase):
    def fixture(self,root):
        project=root/'project';out=root/'artifacts'
        for name in ('ml/linq/upload_agent.py','ml/pipeline/stage_program.py'):
            p=project/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('# fixture source\n')
        (project/'private.env').write_text('PRIVATE_TEST_CONTENT')
        return out,module.build(project,out)

    def test_two_reviewed_files_only_owned_names_and_pinned_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            out,(info,payload)=self.fixture(Path(tmp))
            self.assertFalse(info['published']);self.assertEqual(info['namespace_owner'],'matvey')
            self.assertEqual(hashlib.sha256(payload).hexdigest(),info['bootstrap_sha256'])
            with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                self.assertEqual(set(archive.namelist()),{'matvey_upload_agent.py','matvey_stage_program.py'})
                self.assertNotIn(b'PRIVATE_TEST_CONTENT',b''.join(archive.read(n) for n in archive.namelist()))
            source=(out/module.CELL).read_text();compile(source,'bootstrap-cell','exec')
            self.assertIn(info['bootstrap_sha256'],source);self.assertIn('headers[TARGET_URI_ATTR_NAME]',source)
            self.assertIn('dir=_matvey_cache',source);self.assertIn('OMP_NUM_THREADS',source)
            self.assertIn('cv2.setNumThreads(1)',source);self.assertIn('options.intra_op_num_threads, options.inter_op_num_threads = 2, 1',source)
            self.assertNotIn('LINQ_AMQP_PASSWORD',source);self.assertNotIn('mosprom_upload_agent',source)
            self.assertNotIn('torch_resnet50_b1_o5_h1m.tpu',source)
            with self.assertRaises(FileExistsError):module.build(Path(tmp)/'project',out)

    def test_foreign_queue_rejected_before_credentials_or_connection(self):
        with patch.object(module,'_environment_parameters') as private:
            with self.assertRaises(ValueError):module.publish({'bootstrap_queue':'captain_queue'},b'')
        private.assert_not_called()

    def test_ambiguous_own_publication_is_not_repeated(self):
        blob=b'fixture'
        info={'bootstrap_queue':'matvey_bootstrap_'+str(uuid4()),'upload_queue':'matvey_upload_'+str(uuid4()),
            'namespace_owner':'matvey','bootstrap_sha256':hashlib.sha256(blob).hexdigest(),
            'published':False,'publication_state':'UNKNOWN_REVIEW_OWN_QUEUE'}
        with patch.object(module,'_environment_parameters') as private:
            with self.assertRaisesRegex(ValueError,'possibly published'):module.publish(info,blob)
        private.assert_not_called()

    def test_confirmed_publication_reloads_state_and_blocks_stale_second_caller(self):
        with tempfile.TemporaryDirectory() as tmp:
            out,(info,payload)=self.fixture(Path(tmp));calls=[]
            def send(**kwargs):
                self.assertEqual(json.loads((out/module.METADATA).read_text())['publication_state'],'PUBLISHING_UNKNOWN')
                calls.append(kwargs);return None
            channel=SimpleNamespace(queue_declare=lambda **kw:None,confirm_delivery=lambda:None,basic_publish=send)
            connection=SimpleNamespace(channel=lambda:channel,close=lambda:None)
            with patch('pika.BlockingConnection',return_value=connection),patch.object(module,'_environment_parameters',return_value=object()),patch.object(module,'_connection_parameters',return_value=object()):
                result=module.publish(info,payload,out)
                self.assertTrue(result['published'])
                with self.assertRaisesRegex(ValueError,'possibly published'):module.publish(info,payload,out)
            self.assertEqual(len(calls),1)

    def test_negative_publish_confirmation_remains_ambiguous(self):
        with tempfile.TemporaryDirectory() as tmp:
            out,(info,payload)=self.fixture(Path(tmp))
            channel=SimpleNamespace(queue_declare=lambda **kw:None,confirm_delivery=lambda:None,basic_publish=lambda **kw:False)
            connection=SimpleNamespace(channel=lambda:channel,close=lambda:None)
            with patch('pika.BlockingConnection',return_value=connection),patch.object(module,'_environment_parameters',return_value=object()),patch.object(module,'_connection_parameters',return_value=object()):
                result=module.publish(info,payload,out)
            self.assertFalse(result['published']);self.assertEqual(result['publication_state'],'UNKNOWN_REVIEW_OWN_QUEUE')
