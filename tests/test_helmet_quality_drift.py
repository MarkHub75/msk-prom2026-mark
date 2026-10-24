import unittest
from ml.quality.helmet.drift_audit import audit_predictions,evidence_for_gt


def prediction(cls='helmet',score=.9,box=None):
    return {'class_name':cls,'score':score,'bbox_xyxy':box or [0,0,10,10]}

class DriftAuditTests(unittest.TestCase):
    def dataset(self,coverage='complete',ignores=None):
        return {'images':[{'image_id':'i','group_id':'g','split':'val','class_coverage':{'helmet':coverage,'bare_head':'complete'},
                          'annotations':[{'class_name':'helmet','bbox_xyxy':[0,0,10,10]}],'ignore_regions':ignores or []}]}
    def test_recovered_gt_can_offset_lost_gt_and_must_not_be_hidden(self):
        d=self.dataset();d['images'][0]['annotations'].append({'class_name':'helmet','bbox_xyxy':[20,0,30,10]})
        a={'i':[prediction()]};b={'i':[prediction(box=[20,0,30,10])]}
        r=audit_predictions(d,{'native':a,'baseline_ptq':b});t=r['pair_summary']['native_to_baseline_ptq']['helmet']['primary_complete_gt_transitions']
        self.assertEqual(t,{'TP->FN':1,'FN->TP':1});self.assertEqual(r['metrics']['native']['classes']['helmet']['tp'],1)
    def test_partial_unmatched_and_ignore_region_never_false_positive(self):
        p={'i':[prediction(),prediction(box=[30,0,40,10])]}
        partial=audit_predictions(self.dataset('partial'),{'native':p})
        self.assertEqual(partial['false_positives'],[]);self.assertEqual(partial['metrics']['native']['classes']['helmet']['partial_known_tp'],1)
        ignored=audit_predictions(self.dataset(ignores=[{'bbox_xyxy':[30,0,40,10]}]),{'native':p})
        self.assertEqual(ignored['false_positives'],[])
    def test_score_localization_and_other_class_evidence_not_retuning(self):
        gt={'class_name':'helmet','bbox_xyxy':[0,0,10,10]}
        self.assertEqual(evidence_for_gt(gt,[prediction(score=.2)])['unmatched_diagnostic'],'SAVED_SAME_CLASS_OVERLAP_BELOW_PRIMARY_SCORE')
        self.assertIn('OTHER_CLASS',evidence_for_gt(gt,[prediction('bare_head')])['unmatched_diagnostic'])
        self.assertIn('LOCALIZATION',evidence_for_gt(gt,[prediction(box=[7,0,17,10])])['unmatched_diagnostic'])
    def test_duplicate_and_unknown_do_not_redefine_matching(self):
        d=self.dataset();p={'i':[prediction(),prediction(score=.8)]};r=audit_predictions(d,{'native':p})
        self.assertEqual(len(r['false_positives']),1);self.assertEqual(r['false_positives'][0]['diagnostic'],'DUPLICATE_GT_OVERLAP_CANDIDATE')
        r=audit_predictions(self.dataset('unknown'),{'native':p});self.assertEqual(r['false_positives'],[])
        self.assertEqual(r['per_gt'][0]['variants']['native']['state'],'NOT_SCORED_UNKNOWN')
    def test_fp_correspondence_exposes_turnover_not_just_net_count(self):
        d=self.dataset();a={'i':[prediction(box=[30,0,40,10])]};b={'i':[prediction(box=[60,0,70,10])]}
        r=audit_predictions(d,{'native':a,'baseline_ptq':b})
        self.assertEqual(r['fp_pairs']['native_to_baseline_ptq']['counts'],{'SOURCE_FP_WITHOUT_SAME_CLASS_FP_COUNTERPART':1,'TARGET_FP_WITHOUT_SAME_CLASS_FP_COUNTERPART':1})
    def test_missing_prediction_frame_is_error(self):
        with self.assertRaises(ValueError):audit_predictions(self.dataset(),{'native':{}})
