import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from ml.pipeline.upload_bootstrap import build

class UploadBootstrapTest(unittest.TestCase):
    def test_two_reviewed_files_only_and_pinned_code_cell(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);project=root/'project';out=root/'artifacts'
            for name in ('ml/linq/upload_agent.py','ml/pipeline/stage_program.py'):
                p=project/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('# fixture source\n')
            (project/'private.env').write_text('PRIVATE_TEST_CONTENT')
            info,payload=build(project,out)
            self.assertFalse(info['published'])
            self.assertEqual(hashlib.sha256(payload).hexdigest(),info['bootstrap_sha256'])
            with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                self.assertEqual(set(archive.namelist()),{'upload_agent.py','stage_program.py'})
                self.assertNotIn(b'PRIVATE_TEST_CONTENT',b''.join(archive.read(n) for n in archive.namelist()))
            source=(out/'start_jupyter_upload.py').read_text()
            compile(source,'bootstrap-cell','exec')
            self.assertIn(info['bootstrap_sha256'],source)
            self.assertIn('headers[TARGET_URI_ATTR_NAME]',source)
            self.assertNotIn('LINQ_AMQP_PASSWORD',source)
            with self.assertRaises(FileExistsError):build(project,out)
