"""Scenario07 wraps own-track existing events, never diagnoses consciousness."""
from math import isfinite
from ml.scenarios.common import finding,fact,center,inside


def _floor(ctx,person,config):
    observed=fact(ctx,person['track_key'],'floor_observed')
    if observed and observed.get('score',0)>=config.get('min_fact_score',.5) and type(observed.get('value')) is bool:
        return observed['value'],'current_sourced_floor_observation',{'floor_source':observed['source'],'floor_score':observed['score']}
    poly=config.get('floor_polygon');w,h=ctx['batch']['image_size']
    valid=isinstance(poly,list) and len(poly)>=3 and all(isinstance(p,list) and len(p)==2 and all(type(v) in (int,float) and isfinite(v) for v in p) and 0<=p[0]<=w and 0<=p[1]<=h for p in poly)
    if valid:valid=abs(sum(poly[i-1][0]*p[1]-p[0]*poly[i-1][1] for i,p in enumerate(poly)))>1e-8
    if not valid or not all(isinstance(config.get(k),str) and config[k] for k in ('floor_policy_source','geometry_revision')):
        return None,'floor_observation_or_policy_unavailable',{}
    if person.get('score',0)<config.get('min_score',.5):return None,'current_person_below_floor_geometry_confidence',{}
    return inside(center(person['bbox_xyxy']),poly),'declared_floor_geometry',{'floor_policy_source':config['floor_policy_source'],'floor_geometry_revision':config['geometry_revision']}


def evaluate(ctx,config):
    out=[];batch=ctx['batch']
    for person in ctx.get('people',[]):
        key=person['track_key']
        own=[e for e in ctx.get('legacy_events',[]) if e.get('track_key')==key and e.get('camera_id')==batch['camera_id'] and e.get('stream_epoch')==batch['stream_epoch'] and e.get('type') in ('suspected_fall','prolonged_lying')]
        for subrule in ('suspected_fall','prolonged_lying','immobility_observed'):
            relevant=own if subrule=='immobility_observed' else [e for e in own if e['type']==subrule]
            event=max(relevant,key=lambda e:e.get('revision',0)) if relevant else None
            attrs={'medical_diagnosis':False,'consciousness_status':'NOT_DETERMINABLE_FROM_VISUAL_STATE'}
            if not event:
                upright=person.get('posture')=='upright' and person.get('score',0)>=config.get('min_score',.5)
                out.append(finding('07',subrule,key,'NEGATIVE' if upright else 'UNKNOWN','shared_observed_upright' if upright else 'no_matching_legacy_observation',attributes=attrs));continue
            attrs.update(legacy_event_id=event['event_id'],legacy_revision=event['revision'],legacy_type=event['type'],legacy_state=event['state'],legacy_start_media_ms=event.get('start_media_ms'),legacy_confirmed_media_ms=event.get('confirmed_media_ms'))
            if event['state']=='closed' and event.get('close_reason')=='observed_upright':
                out.append(finding('07',subrule,key,'NEGATIVE','legacy_observed_upright_closure',attributes=attrs));continue
            if event['state']!='open':
                out.append(finding('07',subrule,key,'UNKNOWN','legacy_episode_not_open',attributes=attrs));continue
            if subrule=='immobility_observed' and event.get('attributes',{}).get('immobility_observed') is not True:
                out.append(finding('07',subrule,key,'UNKNOWN','visible_keypoint_immobility_not_confirmed',attributes=attrs));continue
            if subrule in ('prolonged_lying','immobility_observed'):
                on_floor,reason,floor_attrs=_floor(ctx,person,config);attrs.update(floor_attrs)
                if on_floor is not True:
                    out.append(finding('07',subrule,key,'NEGATIVE' if on_floor is False else 'UNKNOWN','observed_not_on_floor' if on_floor is False else reason,attributes=attrs));continue
                attrs['floor_observed']=True
            if subrule=='immobility_observed':
                attrs['immobility_observed']=True
                for name in ('immobility_since_media_ms','immobility_confirmed_media_ms'):
                    if name in event.get('attributes',{}):attrs[name]=event['attributes'][name]
            out.append(finding('07',subrule,key,'POSITIVE','legacy_confirmed_observable_state',attributes=attrs))
    return out
