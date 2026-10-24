"""Scenario02: observed moving machinery/transport and declared proximity."""
from math import hypot,isfinite
from ml.scenarios.common import finding,center,foot,fact,covered


def _movement(ctx,obj,config):
    state=fact(ctx,obj['object_key'],'moving_state')
    if state and state.get('score',0)>=config.get('min_fact_score',.5) and type(state.get('value')) is bool:
        return state['value'],'sourced_moving_state',state['score']
    previous=obj.get('previous');dt=obj.get('dt_ms')
    if not previous or previous.get('score',0)<config.get('min_score',.5) or type(dt) not in (int,float) or not isfinite(dt) or not 0<dt<=config.get('max_gap_ms',750):return None,'moving_state_unobservable',None
    threshold=config.get('moving_min_image_diagonals_per_second')
    if type(threshold) not in (int,float) or not isfinite(threshold) or threshold<=0:return None,'moving_policy_unconfigured',None
    a,b=center(obj['bbox_xyxy']),center(previous['bbox_xyxy']);w,h=ctx['batch']['image_size']
    speed=hypot(a[0]-b[0],a[1]-b[1])/(dt/1000)/hypot(w,h)
    return speed>=threshold,'observed_object_translation',float(min(obj['score'],previous['score']))


def evaluate(ctx,config):
    out=[];classes=config.get('machine_classes',[]);minimum=config.get('min_score',.5)
    objects=[o for o in ctx.get('objects',[]) if o.get('class_name') in classes and o.get('score',0)>=minimum]
    policy=config.get('proximity',{})
    for p in ctx.get('people',[]):
        key=p['track_key'];anchor=foot(p,minimum)
        if p.get('score',0)<minimum or anchor is None:
            out.append(finding('02','moving_machine_proximity',key,'UNKNOWN','person_or_foot_unobservable'));continue
        if not objects:
            complete=bool(classes) and all(covered(ctx,c) for c in classes)
            out.append(finding('02','moving_machine_proximity',key,'NEGATIVE' if complete else 'UNKNOWN','complete_machine_absence' if complete else 'machine_observation_coverage_unknown'));continue
        if not policy.get('policy_source') or policy.get('units') not in ('pixels','body_heights') or type(policy.get('threshold')) not in (int,float) or not isfinite(policy['threshold']) or policy['threshold']<=0:
            out.append(finding('02','moving_machine_proximity',key,'BLOCKED','declared_view_plane_proximity_policy_required'));continue
        pairs=[]
        for obj in objects:
            moving,reason,score=_movement(ctx,obj,config)
            attrs={'object_key':obj['object_key'],'movement_basis':reason,'policy_source':policy['policy_source'],'distance_units':policy['units'],'physical_distance':False}
            if moving is None:
                pairs.append(finding('02','moving_machine_proximity',key,'UNKNOWN',reason,attributes=attrs));continue
            if not moving:
                pairs.append(finding('02','moving_machine_proximity',key,'NEGATIVE','object_not_observed_moving',score,attrs));continue
            box=obj['bbox_xyxy'];distance=hypot(max(box[0]-anchor[0],0,anchor[0]-box[2]),max(box[1]-anchor[1],0,anchor[1]-box[3]))
            if policy['units']=='body_heights':distance/=max(1,p['bbox_xyxy'][3]-p['bbox_xyxy'][1])
            attrs.update(distance=distance,threshold=policy['threshold'])
            pairs.append(finding('02','moving_machine_proximity',key,'POSITIVE' if distance<=policy['threshold'] else 'NEGATIVE','configured_projected_proximity',float(min(p['score'],score)),attrs))
        chosen=next((r for r in pairs if r['verdict']=='POSITIVE'),None) or next((r for r in pairs if r['verdict']=='UNKNOWN'),None) or pairs[0]
        chosen['attributes']={**chosen['attributes'],'pairs':[r['attributes'] for r in pairs],'objects_evaluated':len(pairs)}
        out.append(chosen)
    return out
