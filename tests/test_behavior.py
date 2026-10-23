import json
import unittest
from ml.behavior import BehaviorEngine
from ml.contracts import validate_event


def person(lying=False, x=100, points=True):
    k=[[0,0,0] for _ in range(17)]
    if lying:
        box=[x,100,x+200,180]
        k[0]=[x+20,130,.99]
        k[5]=[x+40,120,.99];k[6]=[x+40,150,.99]
        k[11]=[x+120,120,.99];k[12]=[x+120,150,.99]
    else:
        box=[x,0,x+80,200]
        k[0]=[x+40,20,.99]
        k[5]=[x+20,50,.99];k[6]=[x+60,50,.99]
        k[11]=[x+20,130,.99];k[12]=[x+60,130,.99]
    return dict(detection_id='p',class_name='person',score=.99,bbox_xyxy=box,keypoints=k if points else None)


def head(kind='bare_head',x=100):
    return dict(detection_id='h',class_name=kind,score=.99,bbox_xyxy=[x+20,5,x+60,40],keypoints=None)


def batch(t,ds,epoch='e1',camera='c1'):
    return dict(schema_version='1.0',camera_id=camera,stream_epoch=epoch,frame_id=t,
                media_time_ms=t,image_size=[1000,800],request_id=str(t),model_id='test',
                backend='linq',status='ok',detections=ds)


class BehaviorTests(unittest.TestCase):
    def test_positive_helmet_and_no_repeat(self):
        e=BehaviorEngine();out=[]
        for t in range(0,6001,500):out+=e.update(batch(t,[person(),head()]))
        self.assertEqual(len(out),1)
        self.assertEqual(out[0]['type'],'missing_helmet')
        validate_event(out[0])
        self.assertEqual(out[0]['confirmed_media_ms'],2000)

    def test_absence_is_not_violation(self):
        e=BehaviorEngine()
        for t in range(0,4001,500):self.assertEqual(e.update(batch(t,[person()])),[])

    def test_unobserved_head_unknown(self):
        e=BehaviorEngine()
        for t in range(0,4001,500):self.assertEqual(e.update(batch(t,[person(points=False),head()])),[])

    def test_conflicting_helmet_unknown(self):
        e=BehaviorEngine()
        for t in range(0,4001,500):self.assertEqual(e.update(batch(t,[person(),head(),head('helmet')])),[])

    def test_shared_head_ambiguous(self):
        e=BehaviorEngine()
        for t in range(0,4001,500):self.assertEqual(e.update(batch(t,[person(),person(x=110),head()])),[])

    def test_unknown_breaks_confirmation(self):
        e=BehaviorEngine()
        for t in (0,500,1000):self.assertEqual(e.update(batch(t,[person(),head()])),[])
        e.update(batch(1500,[person()]))
        for t in (2000,2500,3000,3500):self.assertEqual(e.update(batch(t,[person(),head()])),[])
        self.assertEqual(len(e.update(batch(4000,[person(),head()]))),1)

    def test_gap_breaks_pending_and_interrupts_active(self):
        e=BehaviorEngine()
        for t in range(0,2001,500):out=e.update(batch(t,[person(),head()]))
        event_id=out[0]['event_id']
        out=e.on_gap(dict(camera_id='c1',stream_epoch='e1',media_time_ms=2500))
        self.assertEqual(out[0]['event_id'],event_id)
        self.assertEqual(out[0]['state'],'interrupted')
        self.assertEqual(out[0]['revision'],2)
        self.assertEqual(e.update(batch(3000,[person(),head()])),[])

    def test_long_gap_cannot_accumulate_dwell(self):
        e=BehaviorEngine()
        e.update(batch(0,[person(),head()]))
        self.assertEqual(e.update(batch(4000,[person(),head()])),[])

    def test_late_frame_does_not_reset_candidate(self):
        e=BehaviorEngine()
        for t in (0,500,1000):e.update(batch(t,[person(),head()]))
        self.assertEqual(e.update(batch(750,[person(),head('helmet')])),[])
        e.update(batch(1500,[person(),head()]))
        self.assertEqual(len(e.update(batch(2000,[person(),head()]))),1)

    def test_stream_epoch_reset_and_retired_epoch(self):
        e=BehaviorEngine()
        for t in (0,500,1000,1500,2000):out=e.update(batch(t,[person(),head()]))
        old=out[0]['track_key']
        out=e.update(batch(0,[person(),head()],epoch='e2'))
        self.assertGreaterEqual(out[0]['end_media_ms'], out[0]['confirmed_media_ms'])
        self.assertEqual(out[0]['state'],'interrupted')
        self.assertEqual(e.update(batch(2500,[person(),head()],epoch='e1')),[])
        for t in (500,1000,1500,2000):out=e.update(batch(t,[person(),head()],epoch='e2'))
        self.assertNotEqual(out[0]['track_key'],old)

    def test_lying_from_start_not_fall(self):
        e=BehaviorEngine();out=[]
        for t in range(0,5001,500):out+=e.update(batch(t,[person(True)]))
        self.assertEqual([v['type'] for v in out],['prolonged_lying'])
        self.assertEqual(out[0]['confirmed_media_ms'],3000)

    def test_transition_fall_and_no_second_lying(self):
        e=BehaviorEngine();out=[]
        e.update(batch(0,[person()]))
        for t in range(500,5001,500):out+=e.update(batch(t,[person(True)]))
        self.assertEqual([v['type'] for v in out],['suspected_fall'])
        self.assertEqual(out[0]['confirmed_media_ms'],1500)

    def test_recovery_closes_and_suppresses_repeat(self):
        e=BehaviorEngine()
        e.update(batch(0,[person()]))
        for t in (500,1000,1500):out=e.update(batch(t,[person(True)]))
        eid=out[0]['event_id']
        out=e.update(batch(2000,[person()]))
        self.assertEqual((out[0]['event_id'],out[0]['state']),(eid,'closed'))
        for t in (2500,3000,3500,4000):self.assertEqual(e.update(batch(t,[person(True)])),[])

    def test_missing_keypoints_not_lying(self):
        e=BehaviorEngine()
        for t in range(0,5001,500):self.assertEqual(e.update(batch(t,[person(True,points=False)])),[])

    def test_camera_independence(self):
        e=BehaviorEngine()
        for t in range(0,2001,500):
            a=e.update(batch(t,[person(),head()],camera='a'))
            b=e.update(batch(t,[person(),head('helmet')],camera='b'))
        self.assertEqual(len(a),1);self.assertEqual(b,[])

    def test_compliance_closes_but_no_renotify(self):
        e=BehaviorEngine()
        for t in range(0,2001,500):e.update(batch(t,[person(),head()]))
        out=e.update(batch(2500,[person(),head('helmet')]))
        self.assertEqual(out[0]['state'],'closed')
        for t in range(3000,6001,500):self.assertEqual(e.update(batch(t,[person(),head()])),[])

    def test_checkpoint_restores_uuid_and_suppression(self):
        e=BehaviorEngine()
        for t in range(0,2001,500):out=e.update(batch(t,[person(),head()]))
        eid=out[0]['event_id']
        state=json.loads(json.dumps(e.export_state()))
        restored=BehaviorEngine();restored.restore_state(state)
        self.assertEqual(restored.update(batch(2500,[person(),head()])),[])
        out=restored.update(batch(3000,[person(),head('helmet')]))
        self.assertEqual(out[0]['event_id'],eid)
        self.assertEqual(out[0]['revision'],2)

    def test_checkpoint_config_change_rejected(self):
        state=BehaviorEngine().export_state()
        with self.assertRaises(ValueError):BehaviorEngine({'confirm_helmet_ms':1000}).restore_state(state)

    def test_valid_empty_breaks_candidate(self):
        e=BehaviorEngine()
        for t in (0,500,1000):e.update(batch(t,[person(),head()]))
        e.update(batch(1500,[]))
        self.assertEqual(e.update(batch(2000,[person(),head()])),[])

    def test_floor_polygon_rejects_lying_elsewhere(self):
        e=BehaviorEngine({'floor_polygon':[[500,500],[700,500],[700,700],[500,700]]})
        for t in range(0,4001,500):self.assertEqual(e.update(batch(t,[person(True)])),[])

def still_person(wrist_shift=0):
    p=person(True)
    for i,xy in {7:(150,120),8:(150,150),9:(180+wrist_shift,120),
                 10:(180,150),13:(240,120),14:(240,150),15:(270,120),16:(270,150)}.items():
        p["keypoints"][i]=[*xy,.99]
    return p


class ImmobilityTests(unittest.TestCase):
    def test_still_keypoints_update_existing_incident_once(self):
        e=BehaviorEngine();out=[]
        for t in range(0,6501,500):out+=e.update(batch(t,[still_person()]))
        self.assertEqual(len(out),2)
        self.assertEqual([v["revision"] for v in out],[1,2])
        self.assertEqual(out[0]["event_id"],out[1]["event_id"])
        self.assertTrue(out[1]["attributes"]["immobility_observed"])
        self.assertEqual(out[1]["attributes"]["immobility_confirmed_media_ms"],3500)
        self.assertNotIn("attributes",out[0])

    def test_single_moving_wrist_not_hidden_by_other_still_points(self):
        e=BehaviorEngine();out=[]
        for i,t in enumerate(range(0,6501,500)):
            out+=e.update(batch(t,[still_person(20 if i%2 else 0)]))
        self.assertEqual(len(out),1)
        self.assertNotIn("attributes",out[0])

    def test_not_enough_observed_points_unknown(self):
        e=BehaviorEngine();out=[]
        for t in range(0,6501,500):out+=e.update(batch(t,[person(True)]))
        self.assertEqual(len(out),1)
        self.assertNotIn("attributes",out[0])

    def test_movement_restarts_confirmation(self):
        e=BehaviorEngine();out=[]
        for t in range(0,3001,500):out+=e.update(batch(t,[still_person()]))
        out+=e.update(batch(3500,[still_person(30)]))
        out+=e.update(batch(4000,[still_person()]))
        for t in range(4500,7001,500):
            mutations=e.update(batch(t,[still_person()]))
            self.assertEqual(mutations,[])
        mutations=e.update(batch(7500,[still_person()]))
        self.assertTrue(mutations[0]["attributes"]["immobility_observed"])

    def test_unknown_visibility_restarts_confirmation(self):
        e=BehaviorEngine()
        for t in range(0,3001,500):e.update(batch(t,[still_person()]))
        self.assertEqual(e.update(batch(3500,[person(True)])),[])
        for t in range(4000,7001,500):self.assertEqual(e.update(batch(t,[still_person()])),[])
        self.assertTrue(e.update(batch(7500,[still_person()]))[0]["attributes"]["immobility_observed"])

    def test_explicit_gap_breaks_motion_window(self):
        e=BehaviorEngine()
        for t in range(0,3001,500):e.update(batch(t,[still_person()]))
        self.assertEqual(e.on_gap(dict(camera_id="c1",media_time_ms=3500))[0]["state"],"interrupted")
        new=[]
        for t in range(4000,7001,500):new+=e.update(batch(t,[still_person()]))
        self.assertEqual(len(new),1)
        self.assertNotIn("attributes",new[0])
        self.assertTrue(e.update(batch(7500,[still_person()]))[0]["attributes"]["immobility_observed"])

    def test_checkpoint_preserves_motion_window_and_no_repeat(self):
        e=BehaviorEngine()
        for t in range(0,3001,500):out=e.update(batch(t,[still_person()]))
        eid=out[0]["event_id"]
        r=BehaviorEngine();r.restore_state(json.loads(json.dumps(e.export_state())))
        out=r.update(batch(3500,[still_person()]))
        self.assertEqual((out[0]["event_id"],out[0]["revision"]),(eid,2))
        restored=BehaviorEngine();restored.restore_state(json.loads(json.dumps(r.export_state())))
        for t in range(4000,7001,500):self.assertEqual(restored.update(batch(t,[still_person()])),[])


if __name__=='__main__':unittest.main()

