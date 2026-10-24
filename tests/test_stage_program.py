import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from ml.pipeline import stage_program as module


class StageProgramTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.cache_root=self.root/'auto/cache'
        self.parent=self.cache_root/'fixture_account';self.parent.mkdir(parents=True)
        self.cache=self.parent/'matvey';self.cache.mkdir()
        self.source=self.cache/'matvey_source.tpu';self.source.write_bytes(b'mocked program bytes')
        self.sha=hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.patches=patch.multiple(module,CACHE_ROOT=self.cache_root,PROGRAM_SHA256=self.sha)
        self.patches.start();self.addCleanup(self.patches.stop)

    def stage(self,*args,**kwargs):
        return module.stage(self.cache,*args,owner_login='fixture_account',**kwargs)

    def test_owned_namespace_idempotent_bytes_without_stock_lookup(self):
        first=self.stage(self.source);second=self.stage(self.source)
        self.assertEqual(first['status'],'STAGED');self.assertEqual(second['status'],'ALREADY_STAGED_IDENTICAL')
        self.assertEqual((self.cache/module.PROGRAM_NAME).read_bytes(),self.source.read_bytes())
        self.assertEqual(first['namespace_owner'],'matvey');self.assertTrue(first['program_path_namespace_verified'])
        self.assertNotIn(str(self.cache),str(first))

    def test_never_create_a_guessed_namespace(self):
        with self.assertRaises(ValueError):module.stage(self.root/'absent',self.source,owner_login='fixture_account')
        self.assertFalse((self.root/'absent').exists())

    def test_never_replace_other_program(self):
        target=self.cache/module.PROGRAM_NAME;target.write_bytes(b'other')
        with self.assertRaises(FileExistsError):self.stage(self.source)
        self.assertEqual(target.read_bytes(),b'other')

    def test_wrong_source_rejected_without_target(self):
        with patch.object(module,'PROGRAM_SHA256','0'*64),self.assertRaises(ValueError):self.stage(self.source)
        self.assertFalse((self.cache/module.PROGRAM_NAME).exists())

    def test_matvey_symlink_escape_rejected_before_source_read(self):
        other=self.parent/'baseline';other.mkdir();self.source.unlink();self.cache.rmdir();self.cache.symlink_to(other)
        with patch.object(module,'file_hash') as reader,self.assertRaises(ValueError):self.stage(self.cache/'matvey_source.tpu')
        reader.assert_not_called();self.assertEqual(list(other.iterdir()),[])

    def test_foreign_account_or_root_cache_rejected_before_write(self):
        for directory in (self.parent,self.cache_root/'other'/'matvey'):
            with self.assertRaises(ValueError):module.stage(directory,self.source,owner_login='fixture_account')
        self.assertFalse((self.cache/module.PROGRAM_NAME).exists())

    def test_protected_program_name_and_outside_source_rejected(self):
        with patch.object(module,'PROGRAM_NAME','mosprom_captain_cut_ap9999.tpu'),self.assertRaises(ValueError):self.stage(self.source)
        other=self.root/'matvey_outside.tpu';other.write_bytes(self.source.read_bytes())
        with self.assertRaises(ValueError):self.stage(other)
        self.assertFalse((self.cache/module.PROGRAM_NAME).exists())

    def test_only_explicit_own_directory_can_be_prepared(self):
        self.source.unlink();self.cache.rmdir()
        directory=module.owned_cache_directory(self.cache,'fixture_account',create=True)
        self.assertEqual(directory,self.cache);self.assertTrue(directory.is_dir())
