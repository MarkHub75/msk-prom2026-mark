"""Synthetic offline motion/geometry contracts, not Running/Zone accuracy."""
from copy import deepcopy
import unittest
from ml.quality.temporal.running_zone import RunningZonePrototype


def config(**changes):
    return {'camera_id':'synthetic-camera','image_size':[1000,600],
            'geometry_revision':'synthetic-geometry-v1','polygon_provenance':'synthetic test polygon; no safety policy',
            'polygon_xy':[[150,200],[350,200],[350,400],[150,400]],
            'speed_units':'pixels_per_second','speed_threshold':100,'speed_confirm_ms':1000,
            'allowed_direction_xy':[1,0],**changes}


def person(x,score=.99,kp=.99):
    points=[[0,0,0] for _ in range(17)]
    points[5]=[x-20,140,.99];points[6]=[x+20,140,.99]
    points[11]=[x-20,220,.99];points[12]=[x+20,220,.99]
    points[15]=[x-10,290,kp];points[16]=[x+10,290,kp]
    return {'detection_id':'synthetic-person','class_name':'person','score':score,
            'bbox_xyxy':[x-30,100,x+30,300],'keypoints':points}


def batch(t,x,**changes):
    return {'schema_version':'1.0','camera_id':'synthetic-camera','stream_epoch':'e1',
            'frame_id':t,'media_time_ms':t,'image_size':[1000,600],'status':'ok',
            'backend':'synthetic-test','detections':[person(x)],**changes}


def kinds(value):return [d['kind'] for d in value['diagnostics']]


class RunningZonePrototypeTests(unittest.TestCase):
    def test_requires_explicit_image_plane_policy_not_metres_or_unnamed_zone(self):
        for change in ({'speed_units':'metres_per_second'}, {'speed_threshold':None},
                       {'polygon_provenance':''},{'polygon_xy':[[0,0],[1,1],[2,2]]}):
            with self.assertRaises(ValueError):RunningZonePrototype(config(**change))

    def test_observed_outside_to_inside_entry_once_while_inside(self):
        p=RunningZonePrototype(config())
        self.assertEqual(p.update(batch(0,100))['diagnostics'],[])
        first=p.update(batch(500,200));self.assertIn('observed_polygon_entry',kinds(first))
        self.assertEqual(first['diagnostics'][0]['crossing_time_bounds_ms'],[0,500])
        self.assertFalse(first['diagnostics'][0]['physical_intrusion_claim'])
        for t in (1000,1500,2000):self.assertNotIn('observed_polygon_entry',kinds(p.update(batch(t,200))))

    def test_first_seen_inside_is_left_censored_not_entry(self):
        result=RunningZonePrototype(config()).update(batch(0,200))
        self.assertNotIn('observed_polygon_entry',kinds(result))
        self.assertEqual(result['unknowns'][0]['reason'],'inside_at_first_observation_entry_unknown')

    def test_gap_before_inside_cannot_invent_crossing_or_fast_motion(self):
        p=RunningZonePrototype(config());p.update(batch(0,100))
        result=p.update(batch(1000,200))
        self.assertNotIn('observed_polygon_entry',kinds(result))
        self.assertNotIn('fast_motion_candidate',kinds(result))
        self.assertIn('observation_gap_reset',[v['reason'] for v in result['unknowns']])

    def test_low_confidence_person_breaks_motion_and_entry_history(self):
        p=RunningZonePrototype(config());p.update(batch(0,100))
        result=p.update(batch(500,150,detections=[person(150,score=.2)]))
        self.assertEqual(result['diagnostics'],[])
        result=p.update(batch(1000,200))
        self.assertNotIn('observed_polygon_entry',kinds(result))

    def test_unobserved_ankles_do_not_fall_back_to_bbox_or_old_point(self):
        p=RunningZonePrototype(config());p.update(batch(0,100))
        result=p.update(batch(500,200,detections=[person(200,kp=.49)]))
        self.assertEqual(result['diagnostics'],[])
        self.assertEqual(result['unknowns'][0]['reason'],'insufficient_ankle_observability')
        self.assertNotIn('observed_polygon_entry',kinds(p.update(batch(1000,220))))

    def test_fast_motion_proxy_requires_continuous_duration_and_does_not_repeat(self):
        p=RunningZonePrototype(config());events=[]
        for t,x in [(0,100),(500,160),(1000,220),(1500,280),(2000,340)]:
            result=p.update(batch(t,x));events.extend(d for d in result['diagnostics'] if d['kind']=='fast_motion_candidate')
        self.assertEqual(len(events),1)
        self.assertAlmostEqual(events[0]['speed'],120)
        self.assertEqual(events[0]['units'],'pixels_per_second')
        self.assertEqual(events[0]['confirmed_media_ms'],1500)
        self.assertIn('not gait/running recognition',events[0]['interpretation'])

    def test_speed_normalization_is_explicit_image_diagonal(self):
        p=RunningZonePrototype(config(speed_units='image_diagonals_per_second',speed_threshold=.05,speed_confirm_ms=0))
        p.update(batch(0,100));result=p.update(batch(500,160))
        event=next(d for d in result['diagnostics'] if d['kind']=='fast_motion_candidate')
        self.assertAlmostEqual(event['speed'],120/(1000**2+600**2)**.5)

    def test_against_direction_uses_current_observed_motion_and_deduplicates(self):
        p=RunningZonePrototype(config());p.update(batch(0,300))
        first=p.update(batch(500,250));second=p.update(batch(1000,200))
        self.assertIn('motion_against_configured_direction',kinds(first))
        self.assertNotIn('motion_against_configured_direction',kinds(second))
        self.assertEqual(first['diagnostics'][0]['cosine'],-1)

    def test_outside_to_outside_chord_does_not_claim_observed_entry(self):
        p=RunningZonePrototype(config(polygon_xy=[[145,200],[155,200],[155,400],[145,400]]))
        p.update(batch(0,100));result=p.update(batch(500,200))
        self.assertNotIn('observed_polygon_entry',kinds(result))
        self.assertIn('unobserved_path_may_cross_polygon',[v['reason'] for v in result['unknowns']])

    def test_boundary_abstention_breaks_unobserved_crossing_chain(self):
        p=RunningZonePrototype(config());p.update(batch(0,100))
        edge=p.update(batch(500,150));self.assertIn('polygon_boundary_uncertain',[v['reason'] for v in edge['unknowns']])
        self.assertNotIn('observed_polygon_entry',kinds(p.update(batch(1000,200))))

    def test_camera_size_mismatch_and_retired_epoch_cannot_borrow_geometry(self):
        p=RunningZonePrototype(config());p.update(batch(0,100))
        with self.assertRaises(ValueError):p.update(batch(500,200,camera_id='other'))
        with self.assertRaises(ValueError):p.update(batch(500,200,image_size=[2000,1200]))
        result=p.update(batch(0,200,stream_epoch='e2'))
        self.assertNotIn('observed_polygon_entry',kinds(result))
        result=p.update(batch(500,200))
        self.assertEqual(result['ignored_reason'],'late_or_duplicate_source_observation')

    def test_wall_processing_duration_is_not_media_motion_time(self):
        p=RunningZonePrototype(config(speed_confirm_ms=0));p.update(batch(0,100,frame_cycle_ms=20000))
        result=p.update(batch(500,160,frame_cycle_ms=21000))
        event=next(d for d in result['diagnostics'] if d['kind']=='fast_motion_candidate')
        self.assertAlmostEqual(event['speed'],120)
        self.assertEqual(result['status'],'UNVALIDATED_PROTOTYPE')
        self.assertTrue(result['not_an_external_event'])
        self.assertEqual(result['production_running_zone'],'NOT_IMPLEMENTED')
        self.assertEqual(result['physical_calibration'],'NONE')

    def test_ambiguous_overlapping_people_do_not_pool_motion(self):
        p=RunningZonePrototype(config(speed_confirm_ms=0))
        first=p.update(batch(0,100,detections=[person(100),person(100)]))
        self.assertEqual(first['diagnostics'],[])
        result=p.update(batch(500,160,detections=[person(160),person(160)]))
        self.assertEqual(result['diagnostics'],[])


if __name__=='__main__':unittest.main()
