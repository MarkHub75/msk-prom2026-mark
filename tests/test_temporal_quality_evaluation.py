"""Finite reference scoring fixtures, not measured human-action accuracy."""
from copy import deepcopy
import unittest
from ml.quality.temporal.evaluation import evaluate


def truth():
    return {'schema_version':'temporal-episode-gt-v1','quality_level':'source-reference-diagnostic',
            'fully_exhaustive_independent_human_review':False,'scope':'unit fixture',
            'final_test':False,'videos':[{'video_id':'v','duration_ms':1000,
                'group_id':'g','split':'validation','media_sha256':'a'*64,
                'known_windows':[{'start_ms':0,'end_ms':1000}], 'unknown_windows':[]}],
            'episodes':[{'episode_id':'fall','video_id':'v','type':'suspected_fall',
                'onset_lower_ms':100,'onset_upper_ms':200,'end_ms':1000,
                'left_censored':False,'right_censored':True}],
            'not_implemented':['running','zone_intrusion']}


def predicted(t,event_id='event',revision=1,kind='suspected_fall'):
    return {'video_id':'v','event':{'schema_version':'1.0','event_id':event_id,'revision':revision,
        'camera_id':'camera','stream_epoch':'epoch','track_key':'camera/epoch/1/1',
        'type':kind,'state':'open','start_media_ms':0,'confirmed_media_ms':t,
        'evidence':{'status':'unavailable','snapshot_ref':None,'clip_ref':None}}}


def score(gt,preds,vids=None,**kwargs):
    return evaluate(gt,preds,['v'] if vids is None else vids,allow_source_reference=True,**kwargs)


class TemporalEpisodeScoringTests(unittest.TestCase):
    def test_partial_source_reference_needs_explicit_acknowledgement(self):
        with self.assertRaises(ValueError):evaluate(truth(),[],['v'])

    def test_uncertain_onset_reports_bounds_not_midpoint_tp(self):
        result=score(truth(),[predicted(150)])['per_type']['suspected_fall']
        self.assertEqual(result['lower']['tp'],0)
        self.assertEqual(result['upper']['tp'],1)
        self.assertIsNone(result['point'])

    def test_after_entire_support_is_definite_one_tp(self):
        result=score(truth(),[predicted(250)])['per_type']['suspected_fall']['point']
        self.assertEqual((result['tp'],result['fp'],result['fn']),(1,0,0))
        self.assertEqual((result['precision'],result['recall'],result['f1']),(1,1,1))

    def test_unknown_reference_window_is_not_fp_and_is_reported(self):
        gt=truth();gt['videos'][0].update(known_windows=[{'start_ms':0,'end_ms':250},{'start_ms':300,'end_ms':1000}],unknown_windows=[{'start_ms':250,'end_ms':300}])
        result=score(gt,[predicted(275)])
        self.assertEqual(result['unknown_predictions'],1)
        self.assertEqual(result['source_unknown_ms'],50)
        self.assertIsNone(result['per_type']['suspected_fall']['point']['precision'])
        self.assertEqual(result['per_type']['suspected_fall']['point']['recall'],0)

    def test_revisions_count_once_distinct_duplicate_incident_counts_false(self):
        result=score(truth(),[predicted(250),predicted(250,revision=2),predicted(300,event_id='duplicate')])
        self.assertEqual(result['revision_rows_deduplicated'],1)
        point=result['per_type']['suspected_fall']['point']
        self.assertEqual((point['tp'],point['fp'],point['fn']),(1,1,0))
        self.assertEqual(point['precision'],.5)

    def test_deadline_respects_entire_onset_support(self):
        result=score(truth(),[predicted(250)],deadline_ms=100)['per_type']['suspected_fall']
        self.assertEqual((result['lower']['tp'],result['upper']['tp']),(0,1))
        result=score(truth(),[predicted(350)],deadline_ms=100)['per_type']['suspected_fall']
        self.assertEqual(result['point']['tp'],0)

    def test_maximum_matching_does_not_lose_second_valid_episode(self):
        gt=truth();gt['episodes'][0].update(onset_lower_ms=0,onset_upper_ms=0)
        gt['episodes'].append({**gt['episodes'][0],'episode_id':'second','onset_lower_ms':100,'onset_upper_ms':100,'end_ms':300})
        point=score(gt,[predicted(200),predicted(800,event_id='late')],deadline_ms=1000)['per_type']['suspected_fall']['point']
        self.assertEqual(point['tp'],2)

    def test_no_positive_lying_truth_has_undefined_recall(self):
        result=score(truth(),[predicted(250,kind='prolonged_lying')])['per_type']['prolonged_lying']['point']
        self.assertEqual(result['fp'],1)
        self.assertIsNone(result['recall']);self.assertIsNone(result['f1'])

    def test_unrun_videos_are_not_false_negatives(self):
        result=score(truth(),[],vids=[])
        self.assertEqual(result['unrun_videos'],['v'])
        self.assertEqual(result['per_type']['suspected_fall']['truth_episodes'],0)
        self.assertIsNone(result['per_type']['suspected_fall']['point']['recall'])

    def test_left_censored_truth_is_unresolved_not_false_prediction(self):
        gt=truth();gt['episodes'][0].update(onset_lower_ms=0,onset_upper_ms=0,left_censored=True)
        result=score(gt,[predicted(250)])
        self.assertEqual(result['left_censored_gt_excluded'],1)
        self.assertEqual(result['unknown_predictions'],1)

    def test_invalid_coverage_and_nonfinite_deadline_rejected(self):
        gt=truth();gt['videos'][0]['known_windows'][0]['start_ms']=1
        with self.assertRaises(ValueError):score(gt,[])
        with self.assertRaises(ValueError):score(truth(),[],deadline_ms=float('nan'))

    def test_uuid_cannot_move_between_truth_types_or_confirmation_times(self):
        with self.assertRaises(ValueError):score(truth(),[predicted(250),predicted(300,revision=2)])


if __name__=='__main__':unittest.main()
