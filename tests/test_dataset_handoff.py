import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from ml.quality.handoff import HandoffError, load_ready, load_producer_ready, publish_snapshot, verify_manifest


class DatasetHandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.source=self.root/'frame.bin';self.source.write_bytes(b'fixture media')
        self.asset={'path':str(self.source),'bytes':self.source.stat().st_size,
            'sha256':hashlib.sha256(self.source.read_bytes()).hexdigest(),'role':'media','group_id':'camera-a'}
        self.dataset={'dataset_id':'fixture','split':'validation','rights_scope':'SYNTHETIC_FIXTURE',
            'annotation_scope':'unknown','capabilities':['annotation'],'assets':[self.asset]}
        self.manifest={'schema_version':'mosprom-dataset-handoff-v1','status':'READY','version':'v1',
            'producer':{'id':'fixture'},'consumer_verification_scope':'checksum fixture', 'datasets':[self.dataset]}

    def verify(self):return verify_manifest(self.manifest,allowed_roots=[self.root])

    def test_ready_does_not_grant_unavailable_event_gt(self):
        p=self.root/'ready.json';publish_snapshot(self.manifest,p,allowed_roots=[self.root])
        load_ready(p,dataset_id='fixture',capability='annotation',allowed_roots=[self.root])
        with self.assertRaisesRegex(HandoffError,'capability'):
            load_ready(p,dataset_id='fixture',capability='event_quality',allowed_roots=[self.root])

    def test_mutated_source_rejected(self):
        self.source.write_bytes(b'changed media')
        with self.assertRaisesRegex(HandoffError,'changed'):self.verify()

    def test_source_group_leak_rejected(self):
        other=copy.deepcopy(self.dataset);other.update(dataset_id='test',split='test')
        self.manifest['datasets'].append(other)
        with self.assertRaisesRegex(HandoffError,'leaks'):self.verify()

    def test_training_prohibited_while_downloading(self):
        self.manifest['status']='DOWNLOADING'
        with self.assertRaisesRegex(HandoffError,'READY'):self.verify()

    def test_no_overwrite_or_untrusted_path(self):
        p=self.root/'ready.json';publish_snapshot(self.manifest,p,allowed_roots=[self.root])
        with self.assertRaises(FileExistsError):publish_snapshot(self.manifest,p,allowed_roots=[self.root])
        self.asset['path']='/etc/passwd'
        with self.assertRaisesRegex(HandoffError,'approved'):self.verify()

    def test_sealed_test_never_silently_becomes_validation(self):
        self.dataset.update(split='test',capabilities=['annotation','inference'])
        p=self.root/'ready.json';p.write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(HandoffError,'sealed'):
            load_ready(p,dataset_id='fixture',capability='inference',allowed_roots=[self.root])

    def producer_fixture(self):
        release=self.root/'release';release.mkdir()
        for name in ('class_map.json','split_manifest.json'):(release/name).write_text('{}')
        files={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in release.iterdir()}
        (release/'checksums.json').write_text(json.dumps(files))
        m={'schema_version':'dataset-release-v1','status':'READY','immutable':True,'dataset_id':'producer',
            'version':'v1','files':files,'allowed_uses':['annotation QA']}
        p=release/'manifest.json';p.write_text(json.dumps(m))
        entry={'dataset_id':'producer','version':'v1','status':'READY','absolute_path':str(release),
            'manifest_path':str(p),'manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
            'allowed_uses':['annotation QA'],'class_map_path':str(release/'class_map.json'),
            'split_manifest_path':str(release/'split_manifest.json'),'checksums_path':str(release/'checksums.json')}
        pointer=self.root/'producer-ready.json';pointer.write_text(json.dumps({'schema_version':'dataset-handoff-v1','datasets':[entry]}))
        return pointer,release

    def test_producer_diagnostic_permission_does_not_become_training(self):
        p,_=self.producer_fixture()
        load_producer_ready(p,dataset_id='producer',allowed_use='annotation QA',releases_root=self.root)
        with self.assertRaisesRegex(HandoffError,'not approved'):
            load_producer_ready(p,dataset_id='producer',allowed_use='training',releases_root=self.root)

    def test_producer_split_bytes_checked_before_consumption(self):
        p,release=self.producer_fixture();(release/'split_manifest.json').write_text('{"test":[]}')
        with self.assertRaisesRegex(HandoffError,'checksum'):
            load_producer_ready(p,dataset_id='producer',allowed_use='annotation QA',releases_root=self.root)
