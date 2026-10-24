"""Scenario01: sourced running and apparent abrupt movement are distinct."""
from math import hypot,isfinite
from ml.scenarios.common import finding,foot,inside,fact


def _geometry(policy,batch):
    poly=policy.get('work_zone');w,h=batch['image_size']
    if not isinstance(poly,list) or len(poly)<3 or not all(isinstance(p,list) and len(p)==2 and all(type(v) in (int,float) and isfinite(v) for v in p) and 0<=p[0]<=w and 0<=p[1]<=h for p in poly):return False
    if abs(sum(poly[i-1][0]*p[1]-p[0]*poly[i-1][1] for i,p in enumerate(poly)))<1e-8:return False
    return all(isinstance(policy.get(k),str) and bool(policy[k]) for k in ('geometry_revision','policy_source'))


def evaluate(ctx,config):
    out=[];batch=ctx['batch'];w,h=batch['image_size'];minimum=config.get('min_score',.5)
    for p in ctx.get('people',[]):
        key=p['track_key'];action=fact(ctx,key,'running_action')
        if p.get('score',0)<minimum:
            out.extend(finding('01',s,key,'UNKNOWN','person_below_required_confidence') for s in ('running','abrupt_in_machinery_zone'));continue
        if not action or action.get('score',0)<config.get('min_fact_score',.5) or type(action.get('value')) is not bool:
            out.append(finding('01','running',key,'UNKNOWN','sourced_running_action_unavailable'))
        else:
            out.append(finding('01','running',key,'POSITIVE' if action['value'] else 'NEGATIVE','sourced_running_action',action['score'],{'source':action['source'],'validated_model_claim':False}))
        policy=config.get('abrupt_movement',{});zone=policy.get('work_zone')
        if not _geometry(policy,batch):
            out.append(finding('01','abrupt_in_machinery_zone',key,'BLOCKED','machinery_work_zone_policy_unconfigured'));continue
        anchor=foot(p,minimum)
        if anchor is None:
            out.append(finding('01','abrupt_in_machinery_zone',key,'UNKNOWN','current_foot_unobservable'));continue
        if not inside(anchor,zone):
            out.append(finding('01','abrupt_in_machinery_zone',key,'NEGATIVE','outside_declared_machinery_work_zone'));continue
        previous=p.get('previous');dt=p.get('dt_ms')
        old=foot(previous,minimum) if previous and previous.get('score',0)>=minimum else None
        if old is None or type(dt) not in (int,float) or not isfinite(dt) or not 0<dt<=policy.get('max_gap_ms',750):
            out.append(finding('01','abrupt_in_machinery_zone',key,'UNKNOWN','insufficient_consecutive_observed_feet'));continue
        units=policy.get('speed_units');threshold=policy.get('speed_threshold')
        if units not in ('pixels_per_second','image_diagonals_per_second') or type(threshold) not in (int,float) or not isfinite(threshold) or threshold<=0:
            out.append(finding('01','abrupt_in_machinery_zone',key,'BLOCKED','explicit_image_plane_speed_policy_required'));continue
        speed=hypot(anchor[0]-old[0],anchor[1]-old[1])/(dt/1000)
        if units=='image_diagonals_per_second':speed/=hypot(w,h)
        out.append(finding('01','abrupt_in_machinery_zone',key,'POSITIVE' if speed>=threshold else 'NEGATIVE','configured_apparent_motion_proxy',float(min(p['score'],previous['score'])),
            {'speed':speed,'speed_units':units,'threshold':threshold,'geometry_revision':policy['geometry_revision'],'policy_source':policy['policy_source'],'apparent_motion_only':True,'validated_gait':False,'physical_speed':False}))
    return out
