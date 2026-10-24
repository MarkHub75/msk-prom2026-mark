import unittest
import numpy as np
from ml.quality.edf_reference import degrade,project,hit_bounds,summarize

class EdfReferenceTests(unittest.TestCase):
    def test_grid_restored_but_information_removed(self):
        rgb=np.zeros((9,11,3),np.uint8);rgb[::2,::2]=255
        out=degrade(rgb)
        self.assertEqual(out.shape,rgb.shape);self.assertEqual(out.dtype,np.uint8)
        self.assertFalse(np.array_equal(rgb,out));np.testing.assert_array_equal(out,degrade(rgb))
    def test_native_frame_origin_keeps_one_frame_uncertainty(self):
        w=project({'start_frame':3,'end_frame':5},[0,33,67,100,133,167])
        self.assertEqual((w['start_ms'],w['last_ms']),(67,133))
        self.assertEqual(hit_bounds(40,45,w),(False,True))
        self.assertEqual(hit_bounds(100,100,w),(True,True))
        self.assertEqual(hit_bounds(180,190,w),(False,False))
    def test_lying_never_becomes_source_fall_and_unknown_never_false_positive(self):
        w=project({'start_frame':3,'end_frame':5,'video_path':'/data/one.mp4','native_event_ordinal':1},[0,33,67,100,133,167])
        obs=[{'eligible_persons':1,'unknown_postures':1,'full_torsos':0}]
        lying={'event_id':'lying','type':'prolonged_lying','camera_id':'one','start_media_ms':67,'confirmed_media_ms':100}
        fall={'event_id':'fall','type':'suspected_fall','camera_id':'one','start_media_ms':300,'confirmed_media_ms':400}
        r=summarize(obs,[lying,fall],[w]);self.assertEqual(r['support_hit_coverage_upper'],0)
        self.assertEqual(r['precision'],'NOT_MEASURABLE');self.assertEqual(r['posture_unknown_rate_of_eligible_detections'],1)
    def test_revisions_do_not_count_as_duplicate_episodes(self):
        w=project({'start_frame':3,'end_frame':5,'video_path':'/data/one.mp4','native_event_ordinal':1},[0,33,67,100,133,167])
        e={'event_id':'fall','type':'suspected_fall','camera_id':'one','start_media_ms':67,'confirmed_media_ms':100}
        r=summarize([], [e,dict(e,state='closed')],[w]);self.assertEqual(r['unique_suspected_fall_episodes'],1)
        self.assertEqual(r['possible_duplicate_additional_episodes'],0)
