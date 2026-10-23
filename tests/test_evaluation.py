import unittest
from ml.pipeline.evaluation import evaluate

class EvaluationTest(unittest.TestCase):
    def test_revisions_do_not_inflate_tp_and_late_is_not_timely(self):
        gt=[dict(camera_id='c',stream_epoch='s',type='missing_helmet',start_media_ms=0,end_media_ms=10000),
            dict(camera_id='c',stream_epoch='s',type='missing_helmet',start_media_ms=20000,end_media_ms=30000)]
        event=dict(gt[0],event_id='1',revision=1,confirmed_media_ms=2000)
        revision=dict(event,revision=2)
        late=dict(gt[1],event_id='2',revision=1,confirmed_media_ms=26000)
        score=evaluate(gt,[event,revision,late])
        self.assertEqual((score['tp'],score['fp'],score['fn']),(1,1,1))
        self.assertEqual(score['precision'],.5)
        self.assertFalse(score['delivery_latency_measured'])

    def test_empty_denominators_are_unknown(self):
        score=evaluate([],[])
        self.assertIsNone(score['precision'])
        self.assertIsNone(score['recall'])
