"""Host-policy experiments cannot silently consume holdout or unrun clips."""
import json
from pathlib import Path
import tempfile
import unittest

from ml.quality.replay import replay


class ReplayCoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.gt = {'schema_version':'temporal-episode-gt-v1','final_test':False,
            'quality_level':'source-reference-diagnostic','scope':'EXPLICIT_TEST_FIXTURE',
            'episodes':[], 'videos':[{'video_id':'a','media_sha256':'a'*64,
                'group_id':'camera-a','split':'validation','duration_ms':1000,
                'known_windows':[{'start_ms':0,'end_ms':1000}], 'unknown_windows':[]} ]}
        self.truth = self.root/'truth.json'
        self.source = self.root/'observations.jsonl'
        self.batch = {'schema_version':'1.0','camera_id':'camera','stream_epoch':'epoch',
            'frame_id':0,'media_time_ms':0,'image_size':[320,240],
            'status':'ok','detections':[], 'backend':'pytorch'}
        self.output = self.root/'result'

    def call(self, census=None):
        self.truth.write_text(json.dumps(self.gt))
        return replay(self.source,self.truth,self.output,evaluated_videos=census or ['a'])

    def test_missing_video_is_not_silently_scored_as_evaluated(self):
        self.source.write_text('')
        with self.assertRaisesRegex(ValueError,'no matching observations'):
            self.call()
        self.assertFalse((self.output/'metrics.json').exists())

    def test_preserve_empty_detection_as_unknown_observation(self):
        self.source.write_text(json.dumps({'video_id':'a','batch':self.batch})+'\n')
        report=self.call()
        self.assertEqual(report['replay']['counts']['frames_without_person_above_behavior_threshold'],1)
        self.assertEqual(report['per_type']['suspected_fall']['adjudicable_predictions'],0)
        self.assertIn('NO_NEW_NEURAL_REQUESTS',report['replay']['execution'])

    def test_final_test_rejected_before_writing_results(self):
        self.gt['final_test']=True;self.source.write_text('')
        with self.assertRaisesRegex(ValueError,'final test'):
            self.call()
        self.assertFalse(self.output.exists())
