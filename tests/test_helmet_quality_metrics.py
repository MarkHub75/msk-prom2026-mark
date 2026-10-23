import unittest
from ml.quality.helmet.metrics import evaluate_dataset


def image(coverage='complete',gt=None,split='val',group='scene1'):
    return {'image_id':'a','group_id':group,'split':split,'class_coverage':{'helmet':coverage,'bare_head':'unknown'},'annotations':gt if gt is not None else [{'class_name':'helmet','bbox_xyxy':[0,0,10,10]}],'ignore_regions':[]}


def pred(score=.9,box=None,cls='helmet'):return {'class_name':cls,'score':score,'bbox_xyxy':box or [0,0,10,10]}


class HelmetMetricsTests(unittest.TestCase):
    def test_perfect_and_duplicate_prediction_ap_score_order(self):
        r=evaluate_dataset({'images':[image()]},{'a':[pred(.9),pred(.8)]})['classes']['helmet']
        self.assertEqual((r['tp'],r['fp'],r['fn']),(1,1,0));self.assertEqual(r['precision'],.5);self.assertEqual(r['recall'],1);self.assertEqual(r['ap50'],1)
        self.assertAlmostEqual(r['f1'],2/3)

    def test_partial_annotations_do_not_create_false_positives_or_ap(self):
        r=evaluate_dataset({'images':[image('partial')]},{'a':[pred(),pred(.8,[20,20,30,30])]})['classes']['helmet']
        self.assertIsNone(r['precision']);self.assertIsNone(r['ap50']);self.assertEqual(r['fp'],0);self.assertEqual(r['partial_known_recall'],1)

    def test_unknown_ignored_and_missed_gt(self):
        i=image();i['ignore_regions']=[{'bbox_xyxy':[20,20,40,40],'reason':'occluded head','class_name':None}]
        r=evaluate_dataset({'images':[i]},{'a':[pred(.9,[25,25,35,35])]})['classes']['helmet']
        self.assertEqual((r['tp'],r['fp'],r['fn'],r['ignored_predictions']),(0,0,1,1));self.assertEqual(r['ap50'],0)

    def test_regular_gt_wins_before_unknown_ignore(self):
        i=image();i['ignore_regions']=[{'bbox_xyxy':[0,0,10,10]}]
        r=evaluate_dataset({'images':[i]},{'a':[pred()]})['classes']['helmet'];self.assertEqual(r['tp'],1)

    def test_empty_gt_ap_undefined_not_zero(self):
        r=evaluate_dataset({'images':[image(gt=[])]},{'a':[pred()]});self.assertIsNone(r['macro_ap50']);self.assertEqual(r['classes']['helmet']['fp'],1)

    def test_final_test_guard_and_group_leakage(self):
        with self.assertRaises(ValueError):evaluate_dataset({'images':[image(split='test')]},{'a':[]})
        b=image(split='train');b['image_id']='b'
        with self.assertRaises(ValueError):evaluate_dataset({'images':[image(),b]},{'a':[],'b':[]})

    def test_invalid_prediction_and_missing_inference_not_counted_as_miss(self):
        with self.assertRaises(ValueError):evaluate_dataset({'images':[image()]},{})
        with self.assertRaises(ValueError):evaluate_dataset({'images':[image()]},{'a':[pred(float('nan'))]})

    def test_score_floor_and_iou_distinguish_ap_thresholds(self):
        r=evaluate_dataset({'images':[image()]},{'a':[pred(.2,[1,0,11,10])]})['classes']['helmet']
        self.assertEqual(r['fn'],1);self.assertEqual(r['ap50'],1);self.assertLess(r['map50_95'],1)


if __name__=='__main__':unittest.main()
