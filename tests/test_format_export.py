"""Package-export boundary tests with explicitly fake modules, no vendor claims."""
import importlib.util
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import zipfile
from ml.pipeline.export_linq_format import export_package

class FormatExportTest(unittest.TestCase):
    def test_permission_checked_before_module_access(self):
        with patch('importlib.util.find_spec') as find:
            with self.assertRaises(PermissionError):export_package('unused.zip')
            find.assert_not_called()

    def test_exports_one_module_and_sanitized_metadata_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);site=root/'site';site.mkdir()
            module=site/'tpu_pycloud_format.py'
            module.write_text('class PyTask: pass\ndef serialize(value): pass\ndef deserialize(data): pass\n')
            (site/'unrelated.env').write_text('excluded fixture')
            spec=importlib.util.spec_from_file_location('tpu_pycloud_format',module)
            package=types.SimpleNamespace(PyTask=lambda task_id:None,serialize=lambda obj:None,deserialize=lambda data:None)
            dist=types.SimpleNamespace(version='0.0.1',requires=['numpy @ https://private.invalid/path'])
            with patch('importlib.util.find_spec',return_value=spec),patch('importlib.metadata.distribution',return_value=dist),patch('importlib.metadata.version',return_value='1.26.4'),patch('importlib.import_module',return_value=package):
                result=export_package(root/'transfer.zip',authorized_by_organizers=True,expected_site=site)
            self.assertEqual(result['status'],'EXPORTED')
            with zipfile.ZipFile(root/'transfer.zip') as archive:
                self.assertNotIn('unrelated.env',archive.namelist())
                manifest=json.loads(archive.read('SOURCE.json'))
                self.assertEqual(manifest['version'],'0.0.1')
                self.assertFalse(manifest['notebook_or_credentials_exported'])
                self.assertNotIn('private.invalid',archive.read('tpu_pycloud_format-0.0.1.dist-info/METADATA').decode())
                self.assertEqual(manifest['api']['serialize'][0]['name'],'obj')

    def test_wrong_version_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);module=root/'tpu_pycloud_format.py';module.write_text('')
            spec=importlib.util.spec_from_file_location('tpu_pycloud_format',module)
            with patch('importlib.util.find_spec',return_value=spec),patch('importlib.metadata.distribution',return_value=types.SimpleNamespace(version='0.0.2')):
                with self.assertRaises(ValueError):export_package(root/'out.zip',authorized_by_organizers=True,expected_site=root)
