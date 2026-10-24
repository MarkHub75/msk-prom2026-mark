"""Pure shared geometry and observable-fact helpers; no neural execution."""
import math


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def center(box):
    return [(box[0] + box[2]) / 2, (box[1] + box[3]) / 2]


def foot(person, min_score=.5):
    points = person.get('keypoints')
    if not points or len(points) != 17:
        return None
    feet = [points[15], points[16]]
    if any(len(p) != 3 or not all(finite(v) for v in p) or p[2] < min_score for p in feet):
        return None
    return [(feet[0][0] + feet[1][0]) / 2, max(feet[0][1], feet[1][1])]


def inside(point, polygon):
    """Boundary is included; rules must explicitly require appropriate geometry."""
    if point is None or not polygon or len(polygon) < 3:
        return False
    x, y = point; result = False
    for i, b in enumerate(polygon):
        a = polygon[i - 1]; dx, dy = b[0] - a[0], b[1] - a[1]
        if abs((x-a[0])*dy-(y-a[1])*dx) < 1e-8 and min(a[0],b[0])-1e-8 <= x <= max(a[0],b[0])+1e-8 and min(a[1],b[1])-1e-8 <= y <= max(a[1],b[1])+1e-8:
            return True
        if (a[1] > y) != (b[1] > y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
            result = not result
    return result


def iou(a, b):
    area = max(0, min(a[2], b[2])-max(a[0], b[0])) * max(0, min(a[3], b[3])-max(a[1], b[1]))
    union = max(0, a[2]-a[0])*max(0, a[3]-a[1]) + max(0, b[2]-b[0])*max(0, b[3]-b[1]) - area
    return area / union if union > 0 else 0.


def _json_finite(value):
    if value is None or isinstance(value, (str, bool)):
        return True
    if finite(value):
        return True
    if isinstance(value, list):
        return all(_json_finite(v) for v in value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and _json_finite(v) for k, v in value.items())
    return False


def fact(context, track_key, name):
    """Return exactly one current, sourced observation; never infer missing facts.

    Facts may be classifier outputs or explicitly labelled manual/test annotation.
    Their source must remain in evidence provenance. They are NOT ground truth.
    """
    batch = context['batch']; found = []
    for item in batch.get('scenario_context', {}).get('facts', []):
        if not isinstance(item, dict) or item.get('track_key') != track_key or item.get('name') != name:
            continue
        if (type(item.get('frame_id')) is not int or item['frame_id'] != batch['frame_id']
                or not finite(item.get('media_time_ms')) or item['media_time_ms'] != batch['media_time_ms']
                or not finite(item.get('score')) or not 0 <= item['score'] <= 1
                or not isinstance(item.get('source'), str) or not item['source']
                or 'value' not in item or not _json_finite(item['value'])):
            continue
        if any(k in item and item[k]!=batch.get(k) for k in ('camera_id','stream_epoch','source_sha256')):
            continue
        if batch.get('backend')!='synthetic-test':
            if item.get('camera_id')!=batch['camera_id'] or item.get('stream_epoch')!=batch['stream_epoch']:
                continue
            if batch.get('source_sha256') is not None and item.get('source_sha256')!=batch['source_sha256']:
                continue
        found.append(item)
    return found[0] if len(found) == 1 else None


def covered(context, class_name):
    return context['batch'].get('scenario_context', {}).get('coverage', {}).get(class_name) == 'complete'


def finding(scenario_id, subrule, person_or_track_key, verdict, reason, score=None, attributes=None):
    key = person_or_track_key.get('track_key') if isinstance(person_or_track_key, dict) else person_or_track_key
    value = {'scenario_id': scenario_id, 'subrule': subrule, 'track_key': key,
             'verdict': verdict, 'reason': reason, 'score': score, 'attributes': attributes or {}}
    return validate_finding(value)


def validate_finding(value):
    if value.get('scenario_id') not in {f'{i:02d}' for i in range(1, 9)}:
        raise ValueError('official scenario ID required')
    for key in ('subrule', 'track_key', 'reason'):
        if not isinstance(value.get(key), str) or not value[key]:
            raise ValueError('nonempty finding identity and reason required')
    if value.get('verdict') not in ('POSITIVE', 'NEGATIVE', 'UNKNOWN', 'BLOCKED'):
        raise ValueError('explicit observable verdict required')
    score = value.get('score')
    if score is not None and (not finite(score) or not 0 <= score <= 1):
        raise ValueError('finite confidence required')
    if not isinstance(value.get('attributes'), dict) or not _json_finite(value['attributes']):
        raise ValueError('JSON finite attributes required')
    return value
