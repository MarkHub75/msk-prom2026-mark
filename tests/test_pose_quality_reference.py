"""Source-clock and holdout protection without opening a GPU or a video."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from ml.quality.pose_reference import inspect_inputs


class PoseReferenceGuards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.weights = self.root/'weights.pt'; self.weights.write_bytes(b'fixture-only')
        self.media = self.root/'video.mp4'; self.media.write_bytes(b'not-a-real-video-fixture')
        self.annotations = self.root/'frames.csv'
        self.annotations.write_text('source_frame_id,video_pts_ms\n1,0\n2,41.667\n')
        self.manifest = self.root/'model.json'
        self.manifest.write_text(json.dumps({'decoder':'split_pose_v8', 'artifacts':{
            'weights':{'sha256':self.digest(self.weights)}}}))
        self.video = {'video_id':'fixture', 'split':'validation','media_path':str(self.media),
            'media_sha256':self.digest(self.media), 'annotation_path':str(self.annotations),
            'annotation_sha256':self.digest(self.annotations),'frame_count':2,'duration_ms':83.333}
        self.reference = self.root/'reference.json'

    @staticmethod
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def inspect(self):
        self.reference.write_text(json.dumps({'media':[self.video]}))
        return inspect_inputs(self.reference, self.manifest, self.weights)

    def test_sealed_test_rejected_before_heavy_backend(self):
        self.video['split'] = 'test'
        with self.assertRaisesRegex(ValueError, 'final test'):
            self.inspect()

    def test_source_clock_preserved_and_frame_identity_checked(self):
        self.assertEqual(self.inspect()[0]['media'][0]['frame_count'], 2)
        self.annotations.write_text('source_frame_id,video_pts_ms\n1,0\n3,41.667\n')
        self.video['annotation_sha256'] = self.digest(self.annotations)
        with self.assertRaisesRegex(ValueError, 'identity or PTS'):
            self.inspect()

    def test_changed_media_rejected_even_if_path_unchanged(self):
        self.media.write_bytes(b'replaced-fixture')
        with self.assertRaisesRegex(ValueError, 'media digest'):
            self.inspect()
