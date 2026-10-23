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

if __name__=='__main__':unittest.main()
