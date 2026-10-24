"""04: separate sourced smoking and open-flame findings outside declared zones."""
from ml.scenarios.common import finding,center,foot,inside,fact,covered


def evaluate(context,config):
    out=[];minimum=config.get('min_evidence_score',.5)
    def observed(key,name):
        f=fact(context,key,name)
        return f if f and f['score']>=minimum else None
    for subrule,cls,zones_key,targets in (
        ('open_fire_outside_allowed_zone',config.get('fire_class','flame'),'allowed_fire_zones',context['objects']),
        ('smoking_outside_allowed_zone',config.get('cigarette_class','cigarette'),'allowed_smoking_zones',context['people'])):
        selected=[t for t in targets if subrule.startswith('smoking') or t['class_name']==cls or (subrule.startswith('open_fire') and t['class_name'] in ('steam','smoke'))]
        if not selected and subrule.startswith('open_fire'):
            selected=[{'object_key':'scene','class_name':cls}]
        for target in selected:
            key=target.get('track_key',target.get('object_key'))
            def emit(v,r,s=None,a=None):out.append(finding('04',subrule,key,v,r,s,a))
            if config.get('policy_declared') is not True or zones_key not in config or not config.get('policy_source'):
                emit('BLOCKED','allowed_zone_policy_not_declared');continue
            if not covered(context,cls):emit('BLOCKED','required_detector_coverage_unavailable');continue
            smoking=subrule.startswith('smoking')
            if not smoking and target.get('class_name') in ('steam','smoke'):emit('UNKNOWN','steam_or_smoke_is_not_open_flame');continue
            if not smoking and target.get('object_key')=='scene':emit('NEGATIVE','complete_flame_coverage_no_flame');continue
            if target.get('score',0)<minimum:emit('UNKNOWN','activity_detection_below_evidence_score');continue
            evidence=observed(key,'smoking_observed' if smoking else 'open_flame_observed')
            if evidence and evidence['value'] is False:emit('NEGATIVE','sourced_activity_negative');continue
            if not evidence or evidence['value'] is not True:emit('UNKNOWN','positive_viewable_activity_evidence_required');continue
            if smoking:
                own=observed(key,'cigarette_object_key');gesture=observed(key,'smoking_gesture_observed')
                cigarettes=[o for o in context['objects'] if o['class_name']==cls and own and o['object_key']==own['value'] and o['score']>=minimum]
                if len(cigarettes)!=1 or not gesture or gesture['value'] is not True:emit('UNKNOWN','cigarette_alone_is_not_smoking');continue
                location=foot(target,min_score=minimum)
            else:
                clarity=observed(key,'flame_not_steam_or_reflection')
                if not clarity or clarity['value'] is not True:emit('UNKNOWN','steam_or_reflection_not_excluded');continue
                location=center(target['bbox_xyxy'])
            if location is None:emit('UNKNOWN','activity_location_not_viewable');continue
            allowed=any(inside(location,p) for p in config[zones_key])
            evidence_scores=[evidence['score'],target.get('score',1)]
            evidence_scores += [own['score'],gesture['score'],cigarettes[0]['score']] if smoking else [clarity['score']]
            emit('NEGATIVE' if allowed else 'POSITIVE','inside_explicit_allowed_zone' if allowed else 'observed_activity_outside_explicit_allowed_zones',float(min(evidence_scores)),{'location':list(location),'policy_source':config['policy_source'],'prototype_policy':True})
    return out
