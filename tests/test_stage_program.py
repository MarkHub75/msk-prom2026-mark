import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from ml.pipeline import stage_program as module

class StageProgramTest(unittest.TestCase):
    def fixture(self,root):
        cache=root/'cache';cache.mkdir();(cache/module.STOCK_NAME).write_bytes(b'stock fixture')
        source=root/'program.tpu';source.write_bytes(b'mocked program bytes')
        return cache,source,hashlib.sha256(source.read_bytes()).hexdigest()

    def test_selected_existing_namespace_and_idempotent_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cache,source,sha=self.fixture(root)
            with patch.object(module,'PROGRAM_SHA256',sha):
                first=module.stage(cache,source);second=module.stage(cache,source)
            self.assertEqual(first['status'],'STAGED')
            self.assertEqual(second['status'],'ALREADY_STAGED_IDENTICAL')
            self.assertEqual((cache/module.PROGRAM_NAME).read_bytes(),source.read_bytes())
            self.assertNotIn(str(cache),str(first))

    def test_never_create_a_guessed_namespace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaises(FileNotFoundError):module.stage(root/'absent',root/'program.tpu')
            self.assertFalse((root/'absent').exists())

    def test_never_replace_other_program(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cache,source,sha=self.fixture(root)
            target=cache/module.PROGRAM_NAME;target.write_bytes(b'other')
            with patch.object(module,'PROGRAM_SHA256',sha),self.assertRaises(FileExistsError):module.stage(cache,source)
            self.assertEqual(target.read_bytes(),b'other')

    def test_wrong_source_rejected_without_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cache,source,_=self.fixture(root)
            with self.assertRaises(ValueError):module.stage(cache,source)
            self.assertFalse((cache/module.PROGRAM_NAME).exists())
