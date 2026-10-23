import unittest
import numpy as np
from ml.quality.helmet.tiles import tile_bounds,merge_tile_detections,infer_tiled,compare_policy


class TileTests(unittest.TestCase):
    def test_explicit_odd_dimension_geometry_covers_original(self):
        self.assertEqual(tile_bounds(101,99),[(0,0,61,59),(40,0,101,59),(0,40,61,99),(40,40,101,99)])
        for width,height in [(2,2),(101,99),(1920,1080)]:
            bounds=tile_bounds(width,height);coverage=np.zeros((height,width),np.uint8)
            for x,y,x2,y2 in bounds:coverage[y:y2,x:x2]+=1
            self.assertTrue((coverage>=1).all());self.assertEqual(len(bounds),4)
        with self.assertRaises(ValueError):tile_bounds(1,2)

    def test_source_coordinate_restoration_and_global_dedup_class_aware(self):
        parts=[]
        for index,bounds in enumerate(tile_bounds(100,100)):
            x,y,_,_=bounds
            parts.append((bounds,[{'class_name':'bare_head','score':.9-index*.1,'bbox_xyxy':[45-x,45-y,55-x,55-y],'keypoints':None}]))
        parts[0][1].append({'class_name':'helmet','score':.8,'bbox_xyxy':[45,45,55,55],'keypoints':None})
        result=merge_tile_detections(parts,(100,100))
        self.assertEqual(len(result),2)
        self.assertEqual(result[0]['bbox_xyxy'],[45,45,55,55]);self.assertEqual(result[0]['class_name'],'bare_head')
        self.assertEqual({i['class_name'] for i in result},{'helmet','bare_head'})

    def test_invalid_tile_boxes_and_empty_predictions(self):
        self.assertEqual(merge_tile_detections([(tile_bounds(10,10)[0],[])],(10,10)),[])
        with self.assertRaises(ValueError):merge_tile_detections([((0,0,6,6),[{'class_name':'helmet','score':.9,'bbox_xyxy':[0,0,8,8]}])],(10,10))

    def test_exactly_four_calls_no_fullframe_gt_or_local_suppression(self):
        class Fake:
            def __init__(self):self.requests=[]
            def infer(self,request):
                self.requests.append(request)
                # Same-class duplicate anchors must survive tile-local decoding;
                # the final existing NMS suppresses them in original pixels.
                raw=np.array([[[320,320],[320,320],[100,100],[100,100],[.1,.1],[.9,.8]]],np.float32)
                return {'status':'ok','outputs':{'output0':raw}}
        manifest={'model_id':'helmet-v1','decoder':'detect_v8','classes':['helmet','bare_head'],'input':{'name':'images','shape':[1,3,640,640],'dtype':'float32','layout':'NCHW'},'output_name':'output0','thresholds':{'confidence':.25,'iou':.45,'max_detections':300}}
        backend=Fake();d,t,metadata=infer_tiled(np.zeros((100,100,3),np.uint8),manifest,backend)
        self.assertEqual(len(backend.requests),4);self.assertEqual(len(metadata),4)
        self.assertTrue(all(m['decoded_candidates_before_global_nms']==2 for m in metadata))
        self.assertEqual(len(d),4);self.assertTrue(all(0<=c<=100 for item in d for c in item['bbox_xyxy']))
        self.assertIn('four_nn_calls_ms',t)
        self.assertEqual(manifest['thresholds']['confidence'],.25)

    def test_recalls_gate_rejects_candidate_that_loses_gt(self):
        data={'images':[{'image_id':'a','group_id':'g','split':'val','annotations':[{'class_name':'helmet','bbox_xyxy':[0,0,10,10]}],'class_coverage':{'helmet':'complete','bare_head':'unknown'}}]}
        b={'a':[{'class_name':'helmet','bbox_xyxy':[0,0,10,10],'score':.9}]}
        r=compare_policy(data,b,{'a':[]})
        self.assertEqual(r['status'],'REJECTED_VALIDATION');self.assertFalse(r['recall_guards']['helmet']['pass'])


if __name__=='__main__':unittest.main()
