import unittest
import numpy as np
from ml.detection.codec import preprocess,decode
from ml.scenarios.experiments.person_roi import tiles,proposals,global_nms,observation_metrics

class PersonRoiTests(unittest.TestCase):
    def test_fixed_corner_tiles_and_half_up_bounds(self):
        self.assertEqual(tiles(384,288),[(0,0,230,173),(154,0,384,173),(0,115,230,288),(154,115,384,288)])
        self.assertEqual(tiles(101,99),[(0,0,61,59),(40,0,101,59),(0,40,61,99),(40,40,101,99)])
    def test_decode_parity_without_neural_math_then_original_offset(self):
        m={'decoder':'split_pose_v8','classes':['person'],'input':{'shape':[1,3,640,640],'dtype':'float32'},'split_outputs':{'boxes':'b','class_scores':'s','keypoint_xy':'xy','keypoint_scores':'c'},'thresholds':{'confidence':.25,'iou':.45,'max_detections':300}}
        _,t=preprocess(np.zeros((320,640,3),np.uint8),m)
        o={'b':np.array([[[100],[200],[40],[40]]],np.float32),'s':np.array([[[.9]]],np.float32),'xy':np.full((1,17,2,1),100,np.float32),'c':np.full((1,17,1,1),.8,np.float32)}
        a=global_nms(proposals(o,m,t,(0,0)));self.assertEqual(a,decode(o,m,t))
        b=proposals(o,m,t,(50,25))[0];np.testing.assert_allclose(b['bbox_xyxy'],np.array(a[0]['bbox_xyxy'])+[50,25,50,25])
        np.testing.assert_allclose(np.array(b['keypoints'])[:,:2],np.array(a[0]['keypoints'])[:,:2]+[50,25])
    def test_global_overlap_deduplicates_one_person(self):
        a={'class_name':'person','score':.9,'bbox_xyxy':[10,10,30,50],'keypoints':[[20,20,.9]]*17};b=dict(a,score=.8,bbox_xyxy=[11,10,31,50]);self.assertEqual(len(global_nms([a,b])),1)
    def test_source_partial_unknown_and_out_of_bounds_strata(self):
        objects=[{'track_id':'a','appearance':'visible','movement_values':['running'],'bbox_xyxy_original':[-10,0,10,20]}, {'track_id':'b','appearance':'visible','movement_values':['active'],'bbox_xyxy_original':[40,0,60,20]}]
        ref={'source_objects':objects,'width':100,'height':100,'canonical_frame_time_ms':0,'sha256':'same'}
        obs={'video_id':'s','input_sha256':'same','batch':{'camera_id':'s','frame_id':0,'status':'ok','image_size':[100,100],'media_time_ms':0,'detections':[{'class_name':'person','score':.9,'bbox_xyxy':[0,0,10,20]}]}}
        r=observation_metrics({('s',0):ref},[obs]);self.assertEqual(r['running']['out_of_bounds'],{'matched':1,'total':1,'recall':1.0});self.assertEqual(r['counts']['source_actor_frames_excluded_unknown_other'],1)
        with self.assertRaises(ValueError):observation_metrics({('s',0):ref},[])
