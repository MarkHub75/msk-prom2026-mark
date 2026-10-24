"""Synthetic CAVIAR-scope and running-only invariants, not measured quality."""
from copy import deepcopy
import unittest
import json
import tempfile
from pathlib import Path
from ml.quality.temporal.caviar import associate,_label,evaluate_saved,digest
from ml.quality.temporal.running_zone import RunningZonePrototype
from test_temporal_quality_running_zone import batch,person,kinds


def running(**extra):
    return {'running_only':True,'camera_id':'synthetic-camera','image_size':[1000,600],
        'speed_units':'image_diagonals_per_second','speed_threshold':.2,
        'speed_confirm_ms':1000,'min_score':.5,'keypoint_score':.5,'max_gap_ms':750,**extra}


class CaviarContracts(unittest.TestCase):
    def test_literal_visible_scope_only(self):
        for state in ('active','inactive'):
            self.assertIsNone(_label({'appearance':'visible','movement_values':[state]}))
        for appearance in ('appear','disappear','occluded'):
            self.assertIsNone(_label({'appearance':appearance,'movement_values':['running']}))
        self.assertIsNone(_label({'appearance':'visible','movement_values':['running','walking']}))
        self.assertEqual(_label({'appearance':'visible','movement_values':['walking']}),'walking')

    def test_class_aware_unique_bidirectional_iou(self):
        source=[{'bbox_xyxy_original':[0,0,20,40]}]
        p=[{'class_name':'person','bbox_xyxy':[0,0,20,40]}]
        self.assertEqual(associate(source,p),{0:0})
        self.assertEqual(associate(source+source,p),{})
        self.assertEqual(associate(source,p+p),{})
        self.assertEqual(associate(source,[{**p[0],'class_name':'car'}]),{})
        self.assertEqual(associate(source,[{**p[0],'bbox_xyxy':[30,0,50,40]}]),{})

    def test_running_only_needs_no_polygon_and_emits_no_zone_diagnostics(self):
        e=RunningZonePrototype(running(speed_units='pixels_per_second',speed_threshold=100))
        out=[]
        for t,x in ((0,100),(500,160),(1000,220),(1500,280),(2000,340)):out+=kinds(e.update(batch(t,x)))
        self.assertEqual(out,['fast_motion_candidate'])
        with self.assertRaises(ValueError):RunningZonePrototype(running(allowed_direction_xy=[1,0]))

    def test_bodyheight_proxy_fixed_threshold_and_no_zone_mode(self):
        e=RunningZonePrototype(running(speed_units='body_heights_per_second',speed_threshold=1.5))
        # 160px/.5s /200px height =1.6 bodyheights/s; tracking boxes
        # move too far at .5s, so use100ms samples to preserve unique tracks.
        out=[]
        for t in range(0,1201,100):out+=kinds(e.update(batch(t,100+t*.32)))
        self.assertEqual(out,['fast_motion_candidate'])
        slow=RunningZonePrototype(running(speed_units='body_heights_per_second',speed_threshold=1.5))
        for t in range(0,1201,100):self.assertEqual(kinds(slow.update(batch(t,100+t*.2))),[])
        with self.assertRaises(ValueError):RunningZonePrototype(running(running_only=False))

    def test_bbox_anchor_is_running_only_observed_and_truncation_resets(self):
        e=RunningZonePrototype(running(motion_anchor='observed_bbox_center'))
        p=person(100,kp=0)
        self.assertEqual(e._anchor(p),[100,200])
        for box in ([0,10,20,30],[10,0,20,30],[10,10,1000,30],[10,10,20,600]):
            truncated=deepcopy(p);truncated['bbox_xyxy']=box
            self.assertIsNone(e._anchor(truncated))
        p['visibility']='unknown';self.assertIsNone(e._anchor(p))
        with self.assertRaises(ValueError):RunningZonePrototype(running(running_only=False,motion_anchor='observed_bbox_center'))
        e=RunningZonePrototype(running(motion_anchor='observed_bbox_center',speed_units='pixels_per_second',speed_threshold=100))
        for t in (0,200,400):e.update(batch(t,100+t*.12))
        b=batch(600,172);b['detections'][0]['bbox_xyxy'][0]=0;e.update(b)
        for t in (800,1000,1200,1400,1600):self.assertEqual(kinds(e.update(batch(t,100+t*.12))),[])

    def _saved_fixture(self,root,scope='walking',missing=False):
        refs=[];observations=[]
        for f in range(0,36,5):
            t=f*40;p=person(100+f*4)
            objects=[] if scope is None else [{'track_id':'source-actor','appearance':'visible','movement_values':[scope],'bbox_xyxy_original':p['bbox_xyxy']}]
            refs.append({'sequence':'synthetic-camera','frame_id_from_source_filename':f,'width':1000,'height':600,'source_objects':objects})
            b=batch(t,100+f*4,frame_id=f)
            if missing:b['detections']=[]
            observations.append({'video_id':'synthetic-camera','batch':b})
        ref=root/'frame_annotations.jsonl';ref.write_text(''.join(json.dumps(r)+'\n' for r in refs))
        obs=root/'observations.jsonl';obs.write_text(''.join(json.dumps(r)+'\n' for r in observations))
        protocol={'hashes':{str(ref):digest(ref)},'baseline':running(speed_units='pixels_per_second',speed_threshold=50),
            'episodes':[] if scope is None else [{'episode_id':'source-episode','source':'synthetic-camera','actor':'source-actor','label':scope,'start_frame':0,'end_frame_exclusive':36,'left_censored':True,'right_censored':True}]}
        path=root/'protocol.json';path.write_text(json.dumps(protocol));return path,obs

    def test_saved_evaluation_scope_unknown_is_not_unboxed_false_positive(self):
        for scope in ('walking',None):
            with tempfile.TemporaryDirectory() as d:
                root=Path(d);p,o=self._saved_fixture(root,scope)
                r=evaluate_saved(p,o,root/'output')
                self.assertEqual(r['episode_metrics']['fp'],int(scope=='walking'))
                self.assertEqual(r['unknown_prediction_episodes'],int(scope is None))
                self.assertEqual(r['source_running_episodes'],0)

    def test_missing_model_does_not_remove_positive_truth_or_unrun_frames(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,o=self._saved_fixture(root,'running',missing=True)
            r=evaluate_saved(p,o,root/'output')
            self.assertEqual(r['episode_metrics']['fn'],1)
            self.assertEqual(r['frame_metrics']['fn'],8)
            self.assertEqual(r['actor_window_coverage'][0]['matched_person_frames'],0)
            lines=o.read_text().splitlines();o.write_text('\n'.join(lines[:-1])+'\n')
            with self.assertRaisesRegex(ValueError,'incomplete'):evaluate_saved(p,o,root/'partial')

    def test_gap_low_confidence_and_missing_ankles_reset_running_confirmation(self):
        for issue in ('gap','ankles','score'):
            e=RunningZonePrototype(running(speed_units='pixels_per_second',speed_threshold=100))
            for t in (0,200,400):e.update(batch(t,100+t*.12))
            b=batch(600,172)
            if issue=='gap':b['status']='gap';b['detections']=[]
            if issue=='ankles':b['detections'][0]['keypoints'][15][2]=.49
            if issue=='score':b['detections'][0]['score']=.49
            e.update(b)
            for t in (800,1000,1200,1400,1600):self.assertEqual(kinds(e.update(batch(t,100+t*.12))),[])

if __name__=='__main__':unittest.main()
