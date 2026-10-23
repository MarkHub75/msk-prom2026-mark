"""Meaningful evaluator contracts on SYNTHETIC_FIXTURE, never real accuracy."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from ml.quality.temporal.motion_evaluation import evaluate,wrap_prototype_result

EXAMPLES=Path(__file__).resolve().parents[1]/'ml/quality/temporal/examples'

def fixture():
    gt=json.loads((EXAMPLES/'motion_gt.synthetic.json').read_text())
    preds=[json.loads(v) for v in (EXAMPLES/'motion_predictions.synthetic.jsonl').read_text().splitlines()]
    return gt,preds


def score(gt,preds,**kwargs):
    return evaluate(gt,preds,['synthetic-clip-1'],allow_experimental_running_proxy=True,**kwargs)


class MotionEpisodeTests(unittest.TestCase):
    def test_synthetic_fixture_is_labelled_not_real_quality(self):
        gt,p=fixture();r=score(gt,p)
        self.assertEqual(r['artifact_kind'],'SYNTHETIC_FIXTURE')
        self.assertFalse(r['real_quality_claim']);self.assertFalse(r['public_event_schema_changed'])
        for scenario in ('running','zone_entry'):
            self.assertEqual(r['per_type'][scenario]['point']['tp'],1)

    def test_real_reference_requires_valid_source_hash(self):
        for value in (None, '', 'a'*63, 'A'*64, 'z'*64):
            gt,p=fixture();gt['artifact_kind']='INDEPENDENT_REFERENCE'
            gt['scenes'][0]['source_sha256']=value
            with self.assertRaisesRegex(ValueError,'SHA256'):score(gt,p)
        gt,p=fixture();gt['artifact_kind']='INDEPENDENT_REFERENCE'
        gt['scenes'][0].pop('source_sha256')
        with self.assertRaisesRegex(ValueError,'SHA256'):score(gt,p)
        gt['scenes'][0]['source_sha256']='a'*64
        self.assertFalse(score(gt,p)['real_quality_claim'])

    def test_running_proxy_requires_explicit_acknowledgement(self):
        gt,p=fixture();r=evaluate(gt,p,['synthetic-clip-1'])
        self.assertEqual(r['per_type']['running']['status'],'NOT_EVALUATED')
        self.assertIsNone(r['per_type']['running']['recall'])
        self.assertEqual(r['status'],'PARTIALLY_EVALUATED')

    def test_no_scene_truth_or_missing_episode_list_is_not_zero_accuracy(self):
        gt,p=fixture()
        for missing in ({'scenes':[]}, {k:v for k,v in gt.items() if k!='episodes'}):
            r=evaluate(missing,[],[])
            self.assertEqual(r['status'],'NOT_EVALUATED')
            self.assertIsNone(r['per_type']['zone_entry']['fn'])

    def test_missing_polygon_or_incomplete_scope_coverage_is_not_scored(self):
        gt,p=fixture();gt['scenes'][0]['zones']=[]
        self.assertEqual(score(gt,p)['per_type']['zone_entry']['status'],'NOT_EVALUATED')
        gt,p=fixture();gt['scenes'][0]['coverage'][0]['windows'][0]['end_ms']=3999
        self.assertEqual(score(gt,p)['per_type']['running']['status'],'NOT_EVALUATED')
        gt,p=fixture();gt['scenes'][0]['episode_annotations_complete_for']=[]
        self.assertEqual(score(gt,p)['status'],'NOT_EVALUATED')

    def test_repeated_logical_diagnostic_counts_once_distinct_duplicate_counts_fp(self):
        gt,p=fixture();repeat={**p[0],'confirmed_media_ms':1800}
        r=score(gt,[*p,repeat]);self.assertEqual(r['repeated_diagnostic_rows_coalesced'],1)
        self.assertEqual(r['per_type']['running']['point']['fp'],0)
        extra={**p[0],'prediction_episode_id':'different-logical-episode'}
        r=score(gt,[*p,extra]);self.assertEqual(r['per_type']['running']['point']['fp'],1)
        self.assertEqual(r['per_type']['running']['point']['precision'],.5)

    def test_unknown_gt_is_separate_and_model_gap_does_not_hide_missed_gt(self):
        gt,p=fixture();gt['scenes'][0]['coverage'][0]['windows']=[
            {'start_ms':0,'end_ms':1400,'observability':'known'},
            {'start_ms':1400,'end_ms':1600,'observability':'unknown'},
            {'start_ms':1600,'end_ms':4000,'observability':'known'}]
        r=score(gt,p)['per_type']['running']
        self.assertEqual(len(r['unknown_predictions']),1)
        self.assertEqual(r['point']['fn'],1);self.assertIsNone(r['point']['precision'])
        gt,p=fixture();gap={k:v for k,v in p[0].items() if k in ('source_id','camera_id','source_epoch','group_id','config_version','mapping_version')}
        gap.update(record_kind='gap',media_time_ms=1500)
        r=score(gt,[gap])
        self.assertEqual(r['gap_records'],1)
        self.assertEqual(r['per_type']['running']['point']['fn'],1)
        self.assertEqual(r['per_type']['running']['point']['f1'],0)

    def test_wrong_known_actor_or_known_zone_is_fp_not_a_match(self):
        for scenario in ('running','zone_entry'):
            gt,p=fixture();index=0 if scenario=='running' else 1
            p[index].update(actor_id='actor-B',track_key='synthetic-camera/synthetic-epoch/1/2')
            point=score(gt,p)['per_type'][scenario]['point']
            self.assertEqual((point['tp'],point['fp'],point['fn']),(0,1,1))
        gt,p=fixture();p[1]['zone_id']='zone-B'
        point=score(gt,p)['per_type']['zone_entry']['point']
        self.assertEqual((point['tp'],point['fp'],point['fn']),(0,1,1))

    def test_claimed_actor_disagrees_with_verified_track_binding_is_false(self):
        gt,p=fixture();p[0]['actor_id']='actor-B'
        r=score(gt,p)['per_type']['running']
        self.assertEqual(r['wrong_actor_binding_predictions'],1)
        self.assertEqual(r['point']['fp'],1)

    def test_unresolved_actor_binding_and_polygon_revision_are_unknown(self):
        gt,p=fixture();p[0]['track_key']='unresolved';p[1]['geometry_revision']='wrong-version'
        r=score(gt,p)
        for scenario in ('running','zone_entry'):
            self.assertEqual(len(r['per_type'][scenario]['unknown_predictions']),1)
            self.assertIsNone(r['per_type'][scenario]['point']['precision'])

    def test_unrun_clip_is_not_counted_as_model_miss(self):
        gt,p=fixture();r=evaluate(gt,[],[],allow_experimental_running_proxy=True)
        self.assertEqual(r['unrun_source_ids'],['synthetic-clip-1'])
        self.assertEqual(r['status'],'NOT_EVALUATED')
        self.assertIsNone(r['per_type']['running']['fn'])

    def test_partial_evaluated_census_leaves_second_annotated_clip_unrun(self):
        gt,p=fixture();second=deepcopy(gt['scenes'][0]);second['source_id']='synthetic-clip-2'
        second['source_epoch']='second-epoch';gt['scenes'].append(second)
        for e in list(gt['episodes']):
            gt['episodes'].append({**e,'episode_id':e['episode_id']+'-second','source_id':'synthetic-clip-2'})
        r=score(gt,p)
        self.assertEqual(r['unrun_source_ids'],['synthetic-clip-2'])
        self.assertEqual(r['per_type']['running']['truth_episodes'],1)
        self.assertEqual(r['per_type']['running']['point']['fn'],0)

    def test_censored_or_unknown_episode_does_not_become_false_assertion(self):
        for change in ({'left_censored':True},{'observability':'unknown'}):
            gt,p=fixture();gt['episodes'][0].update(change)
            r=score(gt,p)['per_type']['running']
            self.assertEqual(r['truth_episodes'],0)
            self.assertEqual(len(r['unknown_predictions']),1)

    def test_onset_uncertainty_does_not_pick_midpoint(self):
        gt,p=fixture();p[0]['confirmed_media_ms']=750
        r=score(gt,p)['per_type']['running']
        self.assertEqual((r['lower']['tp'],r['upper']['tp']),(0,1));self.assertIsNone(r['point'])

    def test_config_lineage_or_episode_identity_changes_are_rejected(self):
        for key in ('camera_id','source_epoch','group_id','config_version','mapping_version'):
            gt,p=fixture();p[0][key]='changed'
            with self.assertRaises(ValueError):score(gt,p)
        gt,p=fixture();wrong={**p[0],'track_key':'other-track'}
        with self.assertRaises(ValueError):score(gt,[*p,wrong])

    def test_wrapper_requires_explicit_mapping_and_does_not_guess_actor_or_zone(self):
        raw={'camera_id':'synthetic-camera','stream_epoch':'synthetic-epoch','geometry_revision':'g1','media_time_ms':2000,
             'diagnostics':[{'kind':'observed_polygon_entry','track_key':'t','start_media_ms':1500,'confirmed_media_ms':2000}],
             'unknowns':[{'reason':'observation_gap_reset'}]}
        args={'source_id':'v','group_id':'g','config_version':'c','mapping_version':'m','actor_by_track':{'t':'A'},'zone_id':'zone'}
        a=wrap_prototype_result(raw,**args);b=wrap_prototype_result(raw,**args)
        self.assertEqual(a,b);self.assertEqual(a[0]['actor_id'],'A');self.assertEqual(a[1]['record_kind'],'gap')
        with self.assertRaises(ValueError):wrap_prototype_result(raw,**{**args,'zone_id':None})


if __name__=='__main__':unittest.main()
