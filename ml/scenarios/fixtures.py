"""Clearly labelled synthetic rule acceptance; no video/model accuracy claim."""
from copy import deepcopy
from ml.behavior.scenarios import _person
from .engine import load_config


def build_case(scenario_id,variant='positive'):
    if scenario_id not in {f'{i:02d}' for i in range(1,9)} or variant not in ('positive','negative','unknown'):
        raise ValueError('explicit scenario/fixture variant required')
    config=load_config();config['behavior']={}
    cid='SYNTHETIC-'+scenario_id+'-'+variant;epoch='SYNTHETIC-EPOCH';key=cid+'/'+epoch+'/1/1'
    config.update(camera_id=cid,image_size=[640,480])
    zone=[[0,0],[640,0],[640,480],[0,480]];outside=[[500,300],[630,300],[630,470],[500,470]]
    module=config['modules'][scenario_id];module['temporal']={'confirm_ms':1000,'min_observations':2}
    if scenario_id=='02':module['proximity']['policy_source']='SYNTHETIC_NOT_SITE_POLICY'
    if scenario_id=='04':module.update(policy_declared=True,policy_source='SYNTHETIC_NOT_SITE_POLICY',allowed_fire_zones=[outside],allowed_smoking_zones=[outside])
    if scenario_id=='05':module['fence_climb'].update(barrier_id='SYNTHETIC-FENCE',polygon=zone,geometry_revision='synthetic-v1',policy_source='SYNTHETIC_NOT_SITE_POLICY')
    if scenario_id=='06':module.update(height_policy_declared=True,height_zone_source='SYNTHETIC_NOT_SITE_SURVEY',elevated_work_zones=[zone])
    if scenario_id=='07':module.update(floor_polygon=zone,floor_policy_source='SYNTHETIC_NOT_SITE_SURVEY',geometry_revision='synthetic-v1')
    if scenario_id=='08':module.update(cargo_policy_declared=True,policy_source='SYNTHETIC_NOT_SITE_POLICY',forbidden_carry_zones=[zone])
    result=[]
    for index,t in enumerate(range(0,6501,500)):
        lying=scenario_id=='07' and variant=='positive' and t>=1000
        p=_person(lying=lying,x=40)
        if not lying:
            p['keypoints'][9]=[80,45,.99];p['keypoints'][10]=[85,45,.99]
            p['keypoints'][15]=[65,195,.99];p['keypoints'][16]=[95,195,.99]
        if scenario_id=='07' and variant=='unknown':p['keypoints']=None
        batch={'schema_version':'1.0','camera_id':cid,'stream_epoch':epoch,'frame_id':index,'media_time_ms':t,
               'image_size':[640,480],'status':'ok','detections':[p],'backend':'synthetic-test',
               'fixture_origin':'MANUALLY_CONSTRUCTED_OBSERVATIONS_NO_NEURAL_INFERENCE',
               'scenario_context':{'coverage':{'phone':'complete','cigarette':'complete','flame':'complete','harness':'complete','cargo':'complete'},'facts':[]}}
        def obj(cls,name,box):batch['detections'].append({'class_name':cls,'score':.99,'bbox_xyxy':box,'object_key':name})
        def fact(name,value,owner=key):
            batch['scenario_context']['facts'].append({'track_key':owner,'name':name,'value':value,'score':.99,
                'source':'explicit-synthetic-test-not-model-output','frame_id':index,'media_time_ms':t})
        yes=variant=='positive'
        if scenario_id=='01':fact('running_action',yes)
        if scenario_id=='02':obj('machine','fixture-machine',[130,110,190,230]);fact('moving_state',yes,'fixture-machine')
        if scenario_id=='03':
            obj('phone','fixture-phone',[75,38,86,49]);fact('moving_observed',yes);fact('operating_equipment',False)
            fact('phone_use_observed',yes);fact('phone_object_key','fixture-phone')
        if scenario_id=='04':
            obj('flame','fixture-fire',[75,38,86,49]);fact('open_flame_observed',yes,'fixture-fire');fact('flame_not_steam_or_reflection',True,'fixture-fire')
        if scenario_id=='05':fact('fence_climb',{'climbing':yes,'barrier_id':'SYNTHETIC-FENCE','height_or_pose_evidence':True})
        if scenario_id=='06':
            fact('working_observed',True);fact('harness_area_visible',True);fact('harness_state','absent' if yes else 'present')
            if variant=='negative':fact('harness_usage','in_use')
        if scenario_id=='08':obj('cargo','fixture-load',[90,65,125,120]);fact('carrying_observed',yes);fact('carried_object_key','fixture-load')
        if variant=='unknown':batch['scenario_context']['facts']=[]
        result.append(batch)
    return deepcopy(config),result
