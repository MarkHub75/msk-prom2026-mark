"""Synthetic runnable scenario coverage; not neural or factory quality."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from ml.scenarios.rules import motion,machinery,barriers,fall
from ml.scenarios.common import validate_finding

ROOT=Path(__file__).resolve().parents[1]
ZONE=[[0,0],[700,0],[700,600],[0,600]]


def config(scenario):return json.loads((ROOT/f'configs/scenarios/{scenario}.json').read_text())
def person(x=200):
    points=[[0,0,0] for _ in range(17)];points[15]=[x-10,290,.9];points[16]=[x+10,290,.9]
    return {'class_name':'person','detection_id':'p1','score':.9,'bbox_xyxy':[x-30,100,x+30,300],
        'keypoints':points,'track_key':'c/e/0/1','previous':None,'dt_ms':None}


def context():
    return {'batch':{'schema_version':'1.0','camera_id':'c','stream_epoch':'e','frame_id':5,'media_time_ms':1000,
        'image_size':[1000,600],'status':'ok','backend':'synthetic-test','detections':[],
        'scenario_context':{'facts':[],'coverage':{}}},'people':[person()],'objects':[],'legacy_events':[]}


def addfact(ctx,name,value,key=None,**changes):
    row={'track_key':key or ctx['people'][0]['track_key'],'name':name,'value':value,'score':.95,
        'source':'explicit-synthetic-test','frame_id':ctx['batch']['frame_id'],'media_time_ms':ctx['batch']['media_time_ms'],**changes}
    ctx['batch']['scenario_context']['facts'].append(row);return row


def byrule(rows):return {r['subrule']:r for r in rows}

def moving_object(x=230,old_x=210):
    obj={'class_name':'forklift','detection_id':'o1','object_key':'c/e/object/1','score':.9,'bbox_xyxy':[x,200,x+80,330],'dt_ms':500}
    obj['previous']={'class_name':'forklift','score':.9,'bbox_xyxy':[old_x,200,old_x+80,330]} if old_x is not None else None
    return obj


class MotionTests(unittest.TestCase):
    def policy(self):
        c=config('01');c['abrupt_movement'].update(work_zone=ZONE,geometry_revision='synthetic-v1',policy_source='explicit-synthetic-test');return c

    def test_running_positive_negative_and_missing_not_speed_inferred(self):
        ctx=context();c=self.policy();self.assertEqual(byrule(motion.evaluate(ctx,c))['running']['verdict'],'UNKNOWN')
        f=addfact(ctx,'running_action',True);self.assertEqual(byrule(motion.evaluate(ctx,c))['running']['verdict'],'POSITIVE')
        f['value']=False;self.assertEqual(byrule(motion.evaluate(ctx,c))['running']['verdict'],'NEGATIVE')

    def test_abrupt_zone_proxy_distinct_from_running(self):
        ctx=context();p=ctx['people'][0];p['previous']=person(50);p['dt_ms']=500
        rows=byrule(motion.evaluate(ctx,self.policy()))
        self.assertEqual(rows['abrupt_in_machinery_zone']['verdict'],'POSITIVE')
        self.assertTrue(rows['abrupt_in_machinery_zone']['attributes']['apparent_motion_only'])
        self.assertEqual(rows['running']['verdict'],'UNKNOWN')
        p['previous']=person(195)
        self.assertEqual(byrule(motion.evaluate(ctx,self.policy()))['abrupt_in_machinery_zone']['verdict'],'NEGATIVE')

    def test_missing_policy_gap_feet_and_outside(self):
        ctx=context();self.assertEqual(byrule(motion.evaluate(ctx,config('01')))['abrupt_in_machinery_zone']['verdict'],'BLOCKED')
        c=self.policy();self.assertEqual(byrule(motion.evaluate(ctx,c))['abrupt_in_machinery_zone']['verdict'],'UNKNOWN')
        p=ctx['people'][0];p['previous']=person(50);p['dt_ms']=1000
        self.assertEqual(byrule(motion.evaluate(ctx,c))['abrupt_in_machinery_zone']['verdict'],'UNKNOWN')
        p['dt_ms']=500;p['keypoints'][15][2]=.49
        self.assertEqual(byrule(motion.evaluate(ctx,c))['abrupt_in_machinery_zone']['verdict'],'UNKNOWN')
        ctx['people']=[person(900)]
        self.assertEqual(byrule(motion.evaluate(ctx,c))['abrupt_in_machinery_zone']['verdict'],'NEGATIVE')

    def test_stale_duplicated_or_low_confidence_action_abstains(self):
        for change in ({'frame_id':4},{'media_time_ms':999},{'source':''},{'score':.49}):
            ctx=context();addfact(ctx,'running_action',True,**change)
            self.assertEqual(byrule(motion.evaluate(ctx,self.policy()))['running']['verdict'],'UNKNOWN')
        ctx=context();addfact(ctx,'running_action',True);addfact(ctx,'running_action',False)
        self.assertEqual(byrule(motion.evaluate(ctx,self.policy()))['running']['verdict'],'UNKNOWN')

    def test_degenerate_or_wrong_image_geometry_is_blocked(self):
        for polygon in ([[0,0],[1,1],[2,2]],[[0,0],[2000,0],[0,600]]):
            ctx=context();c=self.policy();c['abrupt_movement']['work_zone']=polygon
            self.assertEqual(byrule(motion.evaluate(ctx,c))['abrupt_in_machinery_zone']['verdict'],'BLOCKED')

    def test_uncalibrated_metres_per_second_not_accepted(self):
        ctx=context();ctx['people'][0].update(previous=person(50),dt_ms=500);c=self.policy();c['abrupt_movement']['speed_units']='metres_per_second'
        self.assertEqual(byrule(motion.evaluate(ctx,c))['abrupt_in_machinery_zone']['verdict'],'BLOCKED')


class MachineryTests(unittest.TestCase):
    def policy(self):
        c=config('02');c['proximity']['policy_source']='explicit-synthetic-test';return c

    def test_moving_near_positive_stationary_and_far_negative(self):
        ctx=context();obj=moving_object();ctx['objects']=[obj]
        self.assertEqual(machinery.evaluate(ctx,self.policy())[0]['verdict'],'POSITIVE')
        obj['previous']=deepcopy(obj);obj['previous']['previous']=None
        self.assertEqual(machinery.evaluate(ctx,self.policy())[0]['verdict'],'NEGATIVE')
        ctx['objects']=[moving_object(900,880)]
        self.assertEqual(machinery.evaluate(ctx,self.policy())[0]['verdict'],'NEGATIVE')

    def test_first_sample_unknown_sourced_operation_can_supply_moving_state(self):
        ctx=context();ctx['objects']=[moving_object(old_x=None)]
        self.assertEqual(machinery.evaluate(ctx,self.policy())[0]['verdict'],'UNKNOWN')
        f=addfact(ctx,'moving_state',True,key=ctx['objects'][0]['object_key'])
        self.assertEqual(machinery.evaluate(ctx,self.policy())[0]['verdict'],'POSITIVE')
        f['value']=False;self.assertEqual(machinery.evaluate(ctx,self.policy())[0]['verdict'],'NEGATIVE')

    def test_no_missing_detection_negative_without_complete_coverage(self):
        ctx=context();self.assertEqual(machinery.evaluate(ctx,self.policy())[0]['verdict'],'UNKNOWN')
        ctx['batch']['scenario_context']['coverage']={k:'complete' for k in self.policy()['machine_classes']}
        self.assertEqual(machinery.evaluate(ctx,self.policy())[0]['verdict'],'NEGATIVE')

    def test_unconfigured_policy_and_stale_motion_gap_abstain(self):
        ctx=context();ctx['objects']=[moving_object()]
        self.assertEqual(machinery.evaluate(ctx,config('02'))[0]['verdict'],'BLOCKED')
        ctx['objects'][0]['dt_ms']=1000
        self.assertEqual(machinery.evaluate(ctx,self.policy())[0]['verdict'],'UNKNOWN')

    def test_multiple_objects_aggregate_one_finding_and_do_not_mask_unknown(self):
        ctx=context();unknown=moving_object(900,None);unknown['object_key']='other'
        ctx['objects']=[unknown,moving_object()];r=machinery.evaluate(ctx,self.policy())
        self.assertEqual(len(r),1);self.assertEqual(r[0]['verdict'],'POSITIVE');self.assertEqual(r[0]['attributes']['objects_evaluated'],2)
        ctx['objects']=[unknown,moving_object(900,880)]
        self.assertEqual(machinery.evaluate(ctx,self.policy())[0]['verdict'],'UNKNOWN')


class BarrierTests(unittest.TestCase):
    def policy(self):
        c=config('05')
        for name in barriers.SPECS:c[name].update(polygon=ZONE,barrier_id=name+'-1',geometry_revision='synthetic-v1',policy_source='explicit-synthetic-test')
        return c

    def value(self,name):
        action,evidence=barriers.SPECS[name]
        return {action:True,'barrier_id':name+'-1',**{k:True for k in evidence}}

    def test_each_distinct_subrule_positive_negative_insufficient(self):
        for name,(action,evidence) in barriers.SPECS.items():
            ctx=context();c=self.policy()
            self.assertEqual(byrule(barriers.evaluate(ctx,c))[name]['verdict'],'UNKNOWN')
            value=self.value(name);f=addfact(ctx,name,value)
            self.assertEqual(byrule(barriers.evaluate(ctx,c))[name]['verdict'],'POSITIVE')
            value[action]=False;self.assertEqual(byrule(barriers.evaluate(ctx,c))[name]['verdict'],'NEGATIVE')
            value[action]=True;value[evidence[0]]=False
            self.assertEqual(byrule(barriers.evaluate(ctx,c))[name]['verdict'],'UNKNOWN')

    def test_line_crossing_overlap_cannot_prove_climbing_or_underpass(self):
        ctx=context();p=ctx['people'][0];p.update(previous=person(900),dt_ms=500)
        for r in barriers.evaluate(ctx,self.policy()):self.assertEqual(r['verdict'],'UNKNOWN')

    def test_unconfigured_policy_is_blocked_and_other_barrier_fact_unknown(self):
        ctx=context()
        for r in barriers.evaluate(ctx,config('05')):self.assertEqual(r['verdict'],'BLOCKED')
        value=self.value('under_conveyor');value['barrier_id']='different';addfact(ctx,'under_conveyor',value)
        self.assertEqual(byrule(barriers.evaluate(ctx,self.policy()))['under_conveyor']['verdict'],'UNKNOWN')

    def test_invalid_region_is_blocked_not_a_safe_negative(self):
        ctx=context();c=self.policy()
        for name in barriers.SPECS:c[name]['polygon']=[[0,0],[1,1],[2,2]]
        self.assertTrue(all(r['verdict']=='BLOCKED' for r in barriers.evaluate(ctx,c)))

    def test_outside_declared_region_and_unobservable_feet(self):
        ctx=context();ctx['people']=[person(900)]
        self.assertTrue(all(r['verdict']=='NEGATIVE' for r in barriers.evaluate(ctx,self.policy())))
        ctx['people'][0]['keypoints'][15][2]=.49
        self.assertTrue(all(r['verdict']=='UNKNOWN' for r in barriers.evaluate(ctx,self.policy())))


class FallWrapperTests(unittest.TestCase):
    def event(self,kind='suspected_fall',**changes):
        return {'event_id':'legacy-uuid','revision':1,'track_key':'c/e/0/1','camera_id':'c','stream_epoch':'e','type':kind,'state':'open',**changes}

    def test_only_matching_legacy_event_positive_no_new_posture_classifier(self):
        for kind in ('suspected_fall','prolonged_lying'):
            ctx=context();ctx['legacy_events']=[self.event(kind)];addfact(ctx,'floor_observed',True)
            r=byrule(fall.evaluate(ctx,config('07')))
            self.assertEqual(r[kind]['verdict'],'POSITIVE');self.assertEqual(r[kind]['attributes']['legacy_event_id'],'legacy-uuid')
            self.assertFalse(r[kind]['attributes']['medical_diagnosis'])
            self.assertEqual(r['immobility_observed']['verdict'],'UNKNOWN')
        ctx=context();self.assertTrue(all(r['verdict']=='UNKNOWN' for r in fall.evaluate(ctx,config('07'))))

    def test_wrong_track_camera_epoch_cannot_inherit_event(self):
        for change in ({'track_key':'other'},{'camera_id':'other'},{'stream_epoch':'old'}):
            ctx=context();ctx['legacy_events']=[self.event(**change)]
            self.assertTrue(all(r['verdict']=='UNKNOWN' for r in fall.evaluate(ctx,config('07'))))

    def test_immobility_attribute_is_observable_not_unconsciousness(self):
        ctx=context();ctx['legacy_events']=[self.event(attributes={'immobility_observed':True,'immobility_since_media_ms':100,'immobility_confirmed_media_ms':1000})];addfact(ctx,'floor_observed',True)
        r=byrule(fall.evaluate(ctx,config('07')))['immobility_observed']
        self.assertEqual(r['verdict'],'POSITIVE');self.assertFalse(r['attributes']['medical_diagnosis'])
        self.assertEqual(r['attributes']['consciousness_status'],'NOT_DETERMINABLE_FROM_VISUAL_STATE')
        self.assertEqual(r['attributes']['immobility_since_media_ms'],100)
        self.assertEqual(r['attributes']['immobility_confirmed_media_ms'],1000)

    def test_lying_floor_required_unknown_bed_negative_and_current_fact_positive(self):
        ctx=context();ctx['legacy_events']=[self.event('prolonged_lying',attributes={'immobility_observed':True})]
        for name in ('prolonged_lying','immobility_observed'):
            self.assertEqual(byrule(fall.evaluate(ctx,config('07')))[name]['verdict'],'UNKNOWN')
        f=addfact(ctx,'floor_observed',False)
        for name in ('prolonged_lying','immobility_observed'):
            self.assertEqual(byrule(fall.evaluate(ctx,config('07')))[name]['verdict'],'NEGATIVE')
        f['value']=True
        for name in ('prolonged_lying','immobility_observed'):
            self.assertEqual(byrule(fall.evaluate(ctx,config('07')))[name]['verdict'],'POSITIVE')
        f['frame_id']=4
        self.assertEqual(byrule(fall.evaluate(ctx,config('07')))['prolonged_lying']['verdict'],'UNKNOWN')

    def test_suspected_fall_does_not_require_floor_or_assert_floor_lying(self):
        ctx=context();ctx['legacy_events']=[self.event()]
        rows=byrule(fall.evaluate(ctx,config('07')))
        self.assertEqual(rows['suspected_fall']['verdict'],'POSITIVE')
        self.assertEqual(rows['prolonged_lying']['verdict'],'UNKNOWN')
        self.assertEqual(rows['immobility_observed']['verdict'],'UNKNOWN')

    def test_floor_geometry_requires_source_revision_and_current_center(self):
        ctx=context();ctx['legacy_events']=[self.event('prolonged_lying')];c=config('07');c['floor_polygon']=ZONE
        self.assertEqual(byrule(fall.evaluate(ctx,c))['prolonged_lying']['verdict'],'UNKNOWN')
        c.update(floor_policy_source='explicit-synthetic-test',geometry_revision='floor-v1')
        self.assertEqual(byrule(fall.evaluate(ctx,c))['prolonged_lying']['verdict'],'POSITIVE')
        ctx['people']=[person(900)]
        self.assertEqual(byrule(fall.evaluate(ctx,c))['prolonged_lying']['verdict'],'NEGATIVE')

    def test_shared_upright_negative_unknown_pose_abstains_without_legacy(self):
        ctx=context();ctx['people'][0]['posture']='upright'
        self.assertTrue(all(r['verdict']=='NEGATIVE' for r in fall.evaluate(ctx,config('07'))))
        ctx['people'][0]['posture']='unknown'
        self.assertTrue(all(r['verdict']=='UNKNOWN' for r in fall.evaluate(ctx,config('07'))))

    def test_closed_upright_negative_and_interrupted_unknown(self):
        ctx=context();ctx['legacy_events']=[self.event(state='closed',close_reason='observed_upright')]
        self.assertEqual(byrule(fall.evaluate(ctx,config('07')))['suspected_fall']['verdict'],'NEGATIVE')
        ctx['legacy_events'][0]['state']='interrupted'
        self.assertEqual(byrule(fall.evaluate(ctx,config('07')))['suspected_fall']['verdict'],'UNKNOWN')

    def test_latest_legacy_revision_and_exact_finding_keys(self):
        ctx=context();ctx['legacy_events']=[self.event(),self.event(revision=2,state='closed',close_reason='observed_upright')]
        rows=fall.evaluate(ctx,config('07'))
        self.assertEqual(byrule(rows)['suspected_fall']['verdict'],'NEGATIVE')
        for module,sc in ((motion,'01'),(machinery,'02'),(barriers,'05'),(fall,'07')):
            for row in module.evaluate(ctx,config(sc)):
                validate_finding(row)
                self.assertEqual(set(row),{'scenario_id','subrule','track_key','verdict','reason','score','attributes'})

if __name__=='__main__':unittest.main()
