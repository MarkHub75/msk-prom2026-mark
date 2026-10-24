"""Synthetic policy safety contracts; not model accuracy."""
from copy import deepcopy
import unittest
from ml.behavior import BehaviorEngine
from test_behavior import person,batch


def partial(lying=False):
    p=person(lying)
    p['keypoints'][6][2]=.49
    p['keypoints'][12][2]=.49
    return p


class PartialTorsoTests(unittest.TestCase):
    def test_opt_in_only_and_same_side_required(self):
        p=partial();self.assertEqual(BehaviorEngine()._posture(p),'unknown')
        e=BehaviorEngine({'allow_partial_torso_pair':True})
        self.assertEqual(e._posture(p),'upright')
        p['keypoints'][11][2]=.49;p['keypoints'][12][2]=.99
        self.assertEqual(e._posture(p),'unknown')
        with self.assertRaises(ValueError):BehaviorEngine({'allow_partial_torso_pair':1})

    def test_right_side_and_existing_geometry_floor_gates(self):
        e=BehaviorEngine({'allow_partial_torso_pair':True})
        p=person(True);p['keypoints'][5][2]=0;p['keypoints'][11][2]=0
        self.assertEqual(e._posture(p),'lying')
        p['bbox_xyxy']=[100,0,180,200];self.assertEqual(e._posture(p),'unknown')
        p=partial(True);p['keypoints'][11][:2]=[141,121]
        self.assertEqual(e._posture(p),'unknown')
        p=partial(True)
        floor=BehaviorEngine({'allow_partial_torso_pair':True,'floor_polygon':[[0,0],[10,0],[10,10],[0,10]]})
        self.assertEqual(floor._posture(p),'unknown')

    def test_all_four_conflict_does_not_choose_convenient_side(self):
        p=person(True);p['keypoints'][12][:2]=[60,150]
        # Opposite side displacements cancel: average torso is too short.
        self.assertEqual(BehaviorEngine()._posture(p),'unknown')
        self.assertEqual(BehaviorEngine({'allow_partial_torso_pair':True})._posture(p),'unknown')

    def test_partial_lying_no_repeat_and_no_immobility_from_hidden_torso(self):
        e=BehaviorEngine({'allow_partial_torso_pair':True});out=[]
        for t in range(0,8501,500):
            p=partial(True)
            for i in (7,8,9,10,13,14,15,16):p['keypoints'][i]=[150+i,140,.99]
            out.extend(deepcopy(e.update(batch(t,[p]))))
        self.assertEqual(len(out),1)
        self.assertEqual(out[0]['type'],'prolonged_lying')
        self.assertFalse(out[0].get('attributes',{}).get('immobility_observed',False))

    def test_observed_partial_transition_can_confirm_single_fall(self):
        e=BehaviorEngine({'allow_partial_torso_pair':True});out=[]
        e.update(batch(0,[partial()]))
        for t in range(500,7001,500):out.extend(deepcopy(e.update(batch(t,[partial(True)]))))
        self.assertEqual([v['type'] for v in out],['suspected_fall'])

    def test_gap_and_unknown_break_confirmation(self):
        for gap in (True,False):
            e=BehaviorEngine({'allow_partial_torso_pair':True});out=[]
            for t in (0,500,1000,1500):out+=e.update(batch(t,[partial(True)]))
            b=batch(2000,[])
            if gap:b['status']='gap'
            out+=e.update(b)
            for t in (2500,3000,3500,4000,4500):out+=e.update(batch(t,[partial(True)]))
            self.assertFalse(any(v['state']=='open' for v in out))


if __name__=='__main__':unittest.main()
