"""06: declared elevated work plus explicitly observable harness presence AND usage."""
from ml.scenarios.common import finding,foot,inside,fact,covered


def evaluate(context,config):
    out=[];minimum=config.get('min_evidence_score',.5)
    for person in context['people']:
        key=person['track_key']
        def emit(v,r,s=None,a=None):out.append(finding('06','work_at_height_without_harness',key,v,r,s,a))
        if person['score']<minimum:emit('UNKNOWN','person_detection_below_evidence_score');continue
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
        visibility=observed('harness_area_visible');state=observed('harness_state');absent=observed('harness_absent');usage=observed('harness_usage')
        if not state and not absent and not usage:
            emit('UNKNOWN' if covered(context,config.get('harness_class','harness')) else 'BLOCKED','harness_absence_is_not_a_detection');continue
        if not visibility or visibility['value'] is not True:emit('UNKNOWN','harness_area_not_observable');continue
        if state and state['value']=='absent' and absent and absent['value'] is False:
            emit('UNKNOWN','conflicting_harness_facts');continue
        present=state and state['value']=='present';missing=state and state['value']=='absent' or absent and absent['value'] is True
        in_use=usage and usage['value']=='in_use'
        not_in_use=usage and usage['value']=='not_in_use'
        if present and missing or missing and in_use:emit('UNKNOWN','conflicting_harness_facts');continue
        attributes={'height_zone_source':config['height_zone_source'],'location':list(location),'prototype_policy':True}
        scores=[float(person['score']),work['score'],visibility['score']]
        if missing:
            scores.append(state['score'] if state and state['value']=='absent' else absent['score'])
            emit('POSITIVE','observed_work_in_declared_height_area_with_visible_harness_absent',float(min(scores)),attributes);continue
        if in_use:
            emit('NEGATIVE','positively_observed_harness_in_use',float(min(scores+[usage['score']])));continue
        if present and not_in_use:
            emit('POSITIVE','visible_harness_present_but_not_in_use_during_height_work',float(min(scores+[state['score'],usage['score']])),attributes);continue
        emit('UNKNOWN','harness_usage_unresolved_presence_is_not_use')
    return out
