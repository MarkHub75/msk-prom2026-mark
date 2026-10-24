"""Scenario05: three evidence-specific interactions; overlap is not climbing."""
from math import isfinite
from ml.scenarios.common import finding,foot,inside,fact

SPECS={'fence_climb':('climbing',('height_or_pose_evidence',)),
       'under_conveyor':('under',('pose_evidence','operation_evidence')),
       'under_suspended_load':('under',('pose_evidence','suspended_operation_evidence'))}


def _geometry(policy,batch):
    poly=policy.get('polygon');w,h=batch['image_size']
    if not isinstance(poly,list) or len(poly)<3 or not all(isinstance(p,list) and len(p)==2 and all(type(v) in (int,float) and isfinite(v) for v in p) and 0<=p[0]<=w and 0<=p[1]<=h for p in poly):return False
    if abs(sum(poly[i-1][0]*p[1]-p[0]*poly[i-1][1] for i,p in enumerate(poly)))<1e-8:return False
    return all(isinstance(policy.get(k),str) and bool(policy[k]) for k in ('barrier_id','geometry_revision','policy_source'))


def evaluate(ctx,config):
    out=[];minimum=config.get('min_score',.5)
    for p in ctx.get('people',[]):
        key=p['track_key'];anchor=foot(p,minimum)
        for subrule,(action,evidence) in SPECS.items():
            policy=config.get(subrule,{})
            attrs={'interaction':subrule,'geometry_revision':policy.get('geometry_revision'),'not_inferred_from_line_crossing':True}
            if p.get('score',0)<minimum or anchor is None:
                out.append(finding('05',subrule,key,'UNKNOWN','person_foot_unobservable',attributes=attrs));continue
            if not _geometry(policy,ctx['batch']):
                out.append(finding('05',subrule,key,'BLOCKED','interaction_geometry_policy_unconfigured',attributes=attrs));continue
            if not inside(anchor,policy['polygon']):
                out.append(finding('05',subrule,key,'NEGATIVE','outside_declared_interaction_region',attributes=attrs));continue
            observed=fact(ctx,key,subrule);value=observed.get('value') if observed else None
            if not observed or observed.get('score',0)<config.get('min_fact_score',.5) or not isinstance(value,dict) or value.get('barrier_id')!=policy['barrier_id'] or type(value.get(action)) is not bool:
                out.append(finding('05',subrule,key,'UNKNOWN','sourced_interaction_unavailable',attributes=attrs));continue
            if not value[action]:
                out.append(finding('05',subrule,key,'NEGATIVE','sourced_action_absent',observed['score'],attrs));continue
            if not all(value.get(name) is True for name in evidence):
                out.append(finding('05',subrule,key,'UNKNOWN','required_height_pose_operation_evidence_missing',attributes=attrs));continue
            attrs.update(source=observed['source'],barrier_id=policy['barrier_id'],policy_source=policy['policy_source'],evidence={name:True for name in evidence})
            out.append(finding('05',subrule,key,'POSITIVE','sourced_interaction_with_declared_geometry',observed['score'],attrs))
    return out
