"""06: declared elevated work plus explicitly observable harness state."""
from ml.scenarios.common import finding,foot,inside,fact,covered


def evaluate(context,config):
    out=[];minimum=config.get('min_evidence_score',.5)
    for person in context['people']:
        key=person['track_key']
        def emit(v,r,s=None,a=None):out.append(finding('06','work_at_height_without_harness',key,v,r,s,a))
        if config.get('height_policy_declared') is not True or not config.get('height_zone_source') or not config.get('elevated_work_zones'):
            emit('BLOCKED','elevated_work_area_not_declared');continue
        location=foot(person,min_score=minimum)
        if location is None:emit('UNKNOWN','height_zone_foot_position_unobservable');continue
        if not any(inside(location,p) for p in config['elevated_work_zones']):emit('NEGATIVE','outside_declared_elevated_work_area');continue
        def observed(name):
            f=fact(context,key,name)
            return f if f and f['score']>=minimum else None
        work=observed('working_observed')
        if work and work['value'] is False:emit('NEGATIVE','sourced_not_working');continue
        if not work or work['value'] is not True:emit('UNKNOWN','working_state_unresolved');continue
        visibility=observed('harness_area_visible');state=observed('harness_state');absent=observed('harness_absent')
        if not state and not absent:
            emit('UNKNOWN' if covered(context,config.get('harness_class','harness')) else 'BLOCKED','harness_absence_is_not_a_detection');continue
        if not visibility or visibility['value'] is not True:emit('UNKNOWN','harness_area_not_observable');continue
        present=state and state['value']=='present';missing=state and state['value']=='absent' or absent and absent['value'] is True
        if present and missing:emit('UNKNOWN','conflicting_harness_facts');continue
        if present:emit('NEGATIVE','positively_observed_harness_present',float(state['score']));continue
        if not missing:emit('UNKNOWN','harness_state_unresolved');continue
        score=min(work['score'],visibility['score'],state['score'] if state and state['value']=='absent' else absent['score'])
        emit('POSITIVE','observed_work_in_declared_height_area_with_visible_harness_absent',float(score),{'height_zone_source':config['height_zone_source'],'location':list(location),'prototype_policy':True})
    return out
