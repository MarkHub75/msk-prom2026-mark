"""Explicit synthetic fixtures; tests establish rules, not detector accuracy."""
import copy,json,unittest
from pathlib import Path
from ml.scenarios.rules import phone,fire_smoking,height,cargo

ZONE=[[0,0],[200,0],[200,250],[0,250]]
OUTSIDE=[[300,0],[400,0],[400,250],[300,250]]


def person():
    k=[[50,50,.99] for _ in range(17)];k[9]=[50,55,.99];k[10]=[60,55,.99];k[15]=[40,200,.99];k[16]=[60,200,.99]
    return {'detection_id':'person','class_name':'person','score':.99,'bbox_xyxy':[0,0,100,210],'keypoints':k,'track_key':'p','previous':None,'dt_ms':None}


def obj(cls,key,box=None):
    return {'detection_id':key,'object_key':key,'class_name':cls,'score':.99,'bbox_xyxy':box or [45,45,55,55],'keypoints':None,'previous':None,'dt_ms':None}


def context(objects=None,values=None,coverage=None):
    facts=[{'track_key':key,'name':name,'value':value,'score':.99,'source':'synthetic_explicit_fixture','frame_id':7,'media_time_ms':1000} for key,name,value in values or []]
    return {'batch':{'schema_version':'1.0','camera_id':'fixture','stream_epoch':'epoch','frame_id':7,'media_time_ms':1000,'image_size':[640,480],'request_id':'r7','model_id':'synthetic','backend':'synthetic-test','status':'ok','detections':[], 'scenario_context':{'coverage':coverage or {'phone':'complete','flame':'complete','cigarette':'complete','harness':'complete','cargo':'complete'},'facts':facts}},'people':[person()],'objects':objects or [],'legacy_events':[]}


def config(n):return json.loads((Path(__file__).resolve().parents[1]/'configs/scenarios'/f'{n}.json').read_text())

class ObjectScenarioTests(unittest.TestCase):
    def test_phone_positive_requires_activity_ownership_use_and_geometry(self):
        values=[('p','moving_observed',True),('p','phone_use_observed',True),('p','phone_object_key','phone1')]
        c=context([obj('phone','phone1')],values)
        self.assertEqual(phone.evaluate(c,config('03'))[0]['verdict'],'POSITIVE')
        c['objects'][0]['bbox_xyxy']=[500,300,520,320]
        self.assertEqual(phone.evaluate(c,config('03'))[0]['verdict'],'UNKNOWN')
    def test_phone_presence_alone_or_stale_fact_cannot_confirm(self):
        c=context([obj('phone','phone1')]);self.assertEqual(phone.evaluate(c,config('03'))[0]['verdict'],'UNKNOWN')
        c=context([obj('phone','phone1')],[('p','moving_observed',True),('p','phone_use_observed',True),('p','phone_object_key','phone1')]);c['batch']['scenario_context']['facts'][-1]['frame_id']=6
        self.assertEqual(phone.evaluate(c,config('03'))[0]['verdict'],'UNKNOWN')
        c['batch']['scenario_context']['coverage']={};self.assertEqual(phone.evaluate(c,config('03'))[0]['verdict'],'BLOCKED')
    def test_phone_explicit_negative_activity(self):
        c=context(values=[('p','moving_observed',False),('p','operating_equipment',False)])
        self.assertEqual(phone.evaluate(c,config('03'))[0]['verdict'],'NEGATIVE')
    def fire_config(self):return dict(config('04'),policy_declared=True,policy_source='synthetic_site_policy',allowed_fire_zones=[OUTSIDE],allowed_smoking_zones=[OUTSIDE])
    def test_fire_distinct_positive_allowed_negative_steam_unknown(self):
        values=[('flame1','open_flame_observed',True),('flame1','flame_not_steam_or_reflection',True)]
        c=context([obj('flame','flame1')],values);cfg=self.fire_config()
        r=[x for x in fire_smoking.evaluate(c,cfg) if x['subrule'].startswith('open_fire')][0];self.assertEqual(r['verdict'],'POSITIVE')
        cfg['allowed_fire_zones']=[ZONE];self.assertEqual(fire_smoking.evaluate(c,cfg)[0]['verdict'],'NEGATIVE')
        c=context([obj('steam','steam1')]);self.assertEqual(fire_smoking.evaluate(c,self.fire_config())[0]['verdict'],'UNKNOWN')
        self.assertEqual(fire_smoking.evaluate(c,config('04'))[0]['verdict'],'BLOCKED')
    def test_smoking_not_cigarette_presence(self):
        c=context([obj('cigarette','cig1')]);cfg=self.fire_config()
        def smoke(c,cfg):return next(x for x in fire_smoking.evaluate(c,cfg) if x['subrule'].startswith('smoking'))
        self.assertEqual(smoke(c,cfg)['verdict'],'UNKNOWN')
        c=context([obj('cigarette','cig1')],[('p','smoking_observed',True),('p','smoking_gesture_observed',True),('p','cigarette_object_key','cig1')])
        self.assertEqual(smoke(c,cfg)['verdict'],'POSITIVE');cfg['allowed_smoking_zones']=[ZONE];self.assertEqual(smoke(c,cfg)['verdict'],'NEGATIVE')
        c['people'][0]['keypoints']=None;self.assertEqual(smoke(c,self.fire_config())['verdict'],'UNKNOWN')
    def height_config(self):return dict(config('06'),height_policy_declared=True,height_zone_source='synthetic_survey',elevated_work_zones=[ZONE])
    def test_height_explicit_absence_present_and_missing(self):
        cfg=self.height_config();values=[('p','working_observed',True),('p','harness_area_visible',True),('p','harness_state','absent')]
        c=context(values=values);self.assertEqual(height.evaluate(c,cfg)[0]['verdict'],'POSITIVE')
        c['batch']['scenario_context']['facts'][-1]['value']='present';self.assertEqual(height.evaluate(c,cfg)[0]['verdict'],'NEGATIVE')
        c=context(values=values[:2]);self.assertEqual(height.evaluate(c,cfg)[0]['verdict'],'UNKNOWN')
        self.assertEqual(height.evaluate(c,config('06'))[0]['verdict'],'BLOCKED')
        c['batch']['scenario_context']['coverage']={};self.assertEqual(height.evaluate(c,cfg)[0]['verdict'],'BLOCKED')
    def test_height_occlusion_or_conflicting_state_cannot_confirm(self):
        values=[('p','working_observed',True),('p','harness_area_visible',False),('p','harness_state','absent')]
        c=context(values=values);self.assertEqual(height.evaluate(c,self.height_config())[0]['verdict'],'UNKNOWN')
        c=context(values=[('p','working_observed',True),('p','harness_area_visible',True),('p','harness_state','present'),('p','harness_absent',True)])
        self.assertEqual(height.evaluate(c,self.height_config())[0]['verdict'],'UNKNOWN')
    def cargo_config(self,face=False):return dict(config('08'),cargo_policy_declared=True,policy_source='synthetic_policy',forbidden_carry_zones=[] if face else [ZONE],forbid_face_obstruction=face)
    def cargo_context(self,extra=None):return context([obj('cargo','load')],[('p','carrying_observed',True),('p','carried_object_key','load')]+(extra or []))
    def test_cargo_forbidden_zone_positive_and_policy_negative(self):
        c=self.cargo_context();cfg=self.cargo_config();self.assertEqual(cargo.evaluate(c,cfg)[0]['verdict'],'POSITIVE')
        cfg['forbidden_carry_zones']=[OUTSIDE];self.assertEqual(cargo.evaluate(c,cfg)[0]['verdict'],'NEGATIVE')
        self.assertEqual(cargo.evaluate(c,config('08'))[0]['verdict'],'BLOCKED')
        self.assertEqual(cargo.evaluate(context([obj('cargo','load')]),self.cargo_config())[0]['verdict'],'UNKNOWN')
    def test_cargo_face_obstruction_sourced_not_weight_inference(self):
        cfg=self.cargo_config(face=True);c=self.cargo_context([('p','face_load_relation_observable',True),('p','face_obstructed_by_load',True)])
        self.assertEqual(cargo.evaluate(c,cfg)[0]['verdict'],'POSITIVE')
        c['batch']['scenario_context']['facts'][-1]['value']=False;self.assertEqual(cargo.evaluate(c,cfg)[0]['verdict'],'NEGATIVE')
        self.assertEqual(cargo.evaluate(self.cargo_context(),cfg)[0]['verdict'],'UNKNOWN')
    def test_low_score_and_unviewable_phone_cannot_confirm(self):
        c=context([obj('phone','phone1')],[('p','moving_observed',True),('p','phone_use_observed',True),('p','phone_object_key','phone1')])
        c['people'][0]['keypoints']=None;self.assertEqual(phone.evaluate(c,config('03'))[0]['verdict'],'UNKNOWN')
        c=context([obj('flame','fire')],[('fire','open_flame_observed',True),('fire','flame_not_steam_or_reflection',True)])
        c['objects'][0]['score']=.1;self.assertEqual(fire_smoking.evaluate(c,self.fire_config())[0]['verdict'],'UNKNOWN')
    def test_rules_are_pure_and_outputs_do_not_depend_on_legacy_event_mutations(self):
        c=context();before=copy.deepcopy(c)
        for module,n in [(phone,'03'),(fire_smoking,'04'),(height,'06'),(cargo,'08')]:
            cfg=config(n);cfg_before=copy.deepcopy(cfg);first=module.evaluate(c,cfg)
            self.assertEqual(c,before);self.assertEqual(cfg,cfg_before);self.assertEqual(first,module.evaluate(c,cfg))
    def test_all_findings_exact_contract(self):
        for module,n in [(phone,'03'),(fire_smoking,'04'),(height,'06'),(cargo,'08')]:
            for finding in module.evaluate(context(),config(n)):
                self.assertEqual(set(finding),{'scenario_id','subrule','track_key','verdict','reason','score','attributes'})
                self.assertEqual(finding['scenario_id'],n)
