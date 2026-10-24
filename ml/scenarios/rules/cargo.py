"""08: owned carried load against explicit observable site policy only."""
from ml.scenarios.common import finding,foot,inside,fact,covered


def evaluate(context,config):
    out=[];minimum=config.get('min_evidence_score',.5)
    zones=config.get('forbidden_carry_zones',[]);face_rule=config.get('forbid_face_obstruction') is True
    for person in context['people']:
        key=person['track_key']
        def emit(v,r,s=None,a=None):out.append(finding('08','unsafe_cargo_carrying',key,v,r,s,a))
        if config.get('cargo_policy_declared') is not True or not config.get('policy_source') or not (zones or face_rule):
            emit('BLOCKED','explicit_observable_carrying_policy_required');continue
        if not covered(context,config.get('cargo_class','cargo')):emit('BLOCKED','cargo_detector_coverage_unavailable');continue
        def observed(name):
            f=fact(context,key,name)
            return f if f and f['score']>=minimum else None
        carrying=observed('carrying_observed');own=observed('carried_object_key')
        if carrying and carrying['value'] is False:emit('NEGATIVE','sourced_not_carrying');continue
        if not carrying or carrying['value'] is not True or not own or not isinstance(own['value'],str):emit('UNKNOWN','observable_carrying_and_load_ownership_required');continue
        loads=[o for o in context['objects'] if o['class_name']==config.get('cargo_class','cargo') and o['object_key']==own['value'] and o['score']>=minimum]
        if len(loads)!=1:emit('UNKNOWN','owned_load_not_uniquely_observed');continue
        violations=[];unresolved=[]
        if zones:
            location=foot(person,min_score=minimum)
            if location is None:unresolved.append('carry_zone_location_unobservable')
            elif any(inside(location,p) for p in zones):violations.append('forbidden_carry_zone')
        if face_rule:
            visible=observed('face_load_relation_observable');obstructed=observed('face_obstructed_by_load')
            if not visible or visible['value'] is not True or not obstructed or type(obstructed['value']) is not bool:unresolved.append('face_obstruction_unresolved')
            elif obstructed['value'] is True:violations.append('observed_face_obstruction')
        if violations:
            emit('POSITIVE','owned_load_violates_explicit_site_policy',float(min(carrying['score'],own['score'],loads[0]['score'])),{'object_key':loads[0]['object_key'],'violations':violations,'unresolved_other_checks':unresolved,'policy_source':config['policy_source'],'prototype_policy':True})
        elif unresolved:emit('UNKNOWN','carrying_policy_checks_not_fully_observable',a={'unresolved':unresolved})
        else:emit('NEGATIVE','observed_owned_load_complies_with_configured_checks')
    return out
