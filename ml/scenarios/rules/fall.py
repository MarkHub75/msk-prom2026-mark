"""Scenario07 wraps own-track existing events, never diagnoses consciousness."""
from ml.scenarios.common import finding


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
                out.append(finding('07',subrule,key,'UNKNOWN','no_matching_legacy_observation',attributes=attrs));continue
            attrs.update(legacy_event_id=event['event_id'],legacy_revision=event['revision'],legacy_type=event['type'],legacy_state=event['state'],legacy_start_media_ms=event.get('start_media_ms'),legacy_confirmed_media_ms=event.get('confirmed_media_ms'))
            if event['state']=='closed' and event.get('close_reason')=='observed_upright':
                out.append(finding('07',subrule,key,'NEGATIVE','legacy_observed_upright_closure',attributes=attrs));continue
            if event['state']!='open':
                out.append(finding('07',subrule,key,'UNKNOWN','legacy_episode_not_open',attributes=attrs));continue
            if subrule=='immobility_observed' and event.get('attributes',{}).get('immobility_observed') is not True:
                out.append(finding('07',subrule,key,'UNKNOWN','visible_keypoint_immobility_not_confirmed',attributes=attrs));continue
            if subrule=='immobility_observed':attrs['immobility_observed']=True
            out.append(finding('07',subrule,key,'POSITIVE','legacy_confirmed_observable_state',attributes=attrs))
    return out
