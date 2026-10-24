"""03: sourced phone use plus visible hand/head geometry and activity context."""
from math import hypot
from ml.scenarios.common import finding,center,fact,covered


def evaluate(context,config):
    out=[];minimum=config.get('min_evidence_score',.5)
    for person in context['people']:
        key=person['track_key']
        def emit(verdict,reason,score=None,attributes=None):
            out.append(finding('03','phone_use_during_activity',key,verdict,reason,score,attributes))
        if person['score']<minimum:emit('UNKNOWN','person_detection_below_evidence_score');continue
        if not covered(context,config.get('phone_class','phone')):
            emit('BLOCKED','phone_detector_coverage_unavailable');continue
        def observed(name):
            f=fact(context,key,name)
            return f if f and f['score']>=minimum else None
        moving,working=observed('moving_observed'),observed('operating_equipment')
        active=any(f and f['value'] is True for f in (moving,working))
        if not active:
            emit('NEGATIVE' if moving and working and moving['value'] is False and working['value'] is False else 'UNKNOWN','activity_not_observed_or_unresolved');continue
        use=observed('phone_use_observed');ownership=observed('phone_object_key')
        if use and use['value'] is False:emit('NEGATIVE','sourced_phone_use_negative');continue
        if not use or use['value'] is not True or not ownership or not isinstance(ownership['value'],str):
            emit('UNKNOWN','phone_use_and_unique_ownership_required');continue
        phones=[o for o in context['objects'] if o['class_name']==config.get('phone_class','phone') and o['object_key']==ownership['value'] and o['score']>=minimum]
        if len(phones)!=1:emit('UNKNOWN','owned_phone_not_uniquely_observed');continue
        points=person.get('keypoints') or []
        wrists=[p for i,p in enumerate(points) if i in (9,10) and p[2]>=minimum]
        heads=[p for i,p in enumerate(points) if i in (0,1,2,3,4) and p[2]>=minimum]
        if not wrists or not heads:emit('UNKNOWN','wrist_and_head_visibility_required');continue
        phone=phones[0];p=center(phone['bbox_xyxy']);box=person['bbox_xyxy'];scale=max(1,hypot(box[2]-box[0],box[3]-box[1]))
        hand=min(hypot(p[0]-w[0],p[1]-w[1])/scale for w in wrists)
        head=min(hypot(p[0]-h[0],p[1]-h[1])/scale for h in heads)
        near_hand=hand<=config.get('max_phone_wrist_body_fraction',.15)
        near_head=head<=config.get('max_phone_head_body_fraction',.35)
        if not near_hand or not near_head:emit('UNKNOWN','phone_use_geometry_not_supported',attributes={'wrist_distance':hand,'head_distance':head});continue
        scores=[use['score'],ownership['score'],phone['score']]+[f['score'] for f in (moving,working) if f and f['value'] is True]
        emit('POSITIVE','owned_visible_phone_use_during_moving_or_equipment_work',float(min(scores)),{'object_key':phone['object_key'],'wrist_distance':hand,'head_distance':head,'prototype_policy':True})
    return out
