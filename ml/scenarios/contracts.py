"""Internal EventCandidate v1; existing external event validator is unchanged."""
from uuid import UUID
from ml.scenarios.common import finite, _json_finite


def validate_candidate(value):
    if value.get('schema_version') != '1.0' or value.get('contract') != 'mosprom.event_candidate.v1':
        raise ValueError('internal candidate contract required')
    if value.get('scenario_id') not in {f'{i:02d}' for i in range(1, 9)}:
        raise ValueError('official scenario ID required')
    if str(UUID(value['candidate_id'])) != value['candidate_id']:
        raise ValueError('canonical candidate UUID required')
    for key in ('camera_id','stream_epoch','track_key','subrule','type','reason'):
        if not isinstance(value.get(key),str) or not value[key]:raise ValueError('candidate identity required')
    if type(value.get('revision')) is not int or value['revision'] < 1 or value.get('state') not in ('open','closed','interrupted'):
        raise ValueError('candidate revision/state required')
    a,b = value.get('start_media_ms'),value.get('confirmed_media_ms')
    if not finite(a) or not finite(b) or not 0 <= a <= b:raise ValueError('invalid candidate media time')
    if 'end_media_ms' in value and (not finite(value['end_media_ms']) or value['end_media_ms'] < b):
        raise ValueError('invalid candidate end time')
    score=value.get('confidence')
    if score is not None and (not finite(score) or not 0 <= score <= 1):raise ValueError('invalid confidence')
    evidence=value.get('evidence',{})
    if evidence.get('status') not in ('pending','ready','unavailable','partial'):raise ValueError('evidence status required')
    if type(evidence.get('frame_id')) is not int or evidence['frame_id']<0 or not finite(evidence.get('media_time_ms')) or evidence['media_time_ms']<0:
        raise ValueError('original evidence frame/time required')
    if evidence['status']=='ready' and not (evidence.get('snapshot_ref') or evidence.get('clip_ref')):
        raise ValueError('ready evidence requires reference')
    if not isinstance(value.get('attributes'),dict) or not _json_finite(value):raise ValueError('finite JSON candidate required')
    if value.get('qualification') != 'PROTOTYPE_NOT_INDEPENDENTLY_VALIDATED':raise ValueError('explicit qualification required')
    return value
