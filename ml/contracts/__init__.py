"""Version 1 wire contracts, shared by inference, behavior and delivery."""
import math

SCHEMA_VERSION = '1.0'


def _number(value):
    return type(value) in (int, float) and math.isfinite(value)


def _identity(value, key):
    if not isinstance(value.get(key), str) or not value[key]:
        raise ValueError(f'invalid {key}')


def validate_observation(value: dict) -> dict:
    required = ('schema_version', 'camera_id', 'stream_epoch', 'frame_id', 'media_time_ms', 'image_size', 'status', 'detections')
    if not isinstance(value, dict):
        raise ValueError('observation must be an object')
    for key in required:
        if key not in value:
            raise ValueError(f'missing {key}')
    if value['schema_version'] != SCHEMA_VERSION:
        raise ValueError('unsupported schema_version')
    if value['status'] not in ('ok', 'error', 'gap'):
        raise ValueError('invalid observation status')
    if type(value['frame_id']) is not int or value['frame_id'] < 0:
        raise ValueError('invalid frame_id')
    if not _number(value['media_time_ms']) or value['media_time_ms'] < 0:
        raise ValueError('invalid media_time_ms')
    for key in ('camera_id', 'stream_epoch'):
        _identity(value, key)
    size = value['image_size']
    if not isinstance(size, (list, tuple)) or len(size) != 2 or not all(type(v) is int and v > 0 for v in size):
        raise ValueError('invalid image_size')
    w, h = size
    if not isinstance(value['detections'], list) or value['status'] != 'ok' and value['detections']:
        raise ValueError('invalid detections for status')
    for d in value['detections']:
        if not isinstance(d, dict):
            raise ValueError('detection must be an object')
        box = d.get('bbox_xyxy')
        score = d.get('score')
        if not isinstance(box, (list, tuple)) or len(box) != 4 or not all(_number(v) for v in box) or not _number(score):
            raise ValueError('invalid detection')
        x1, y1, x2, y2 = box
        if not (0 <= x1 <= x2 <= w and 0 <= y1 <= y2 <= h and 0 <= score <= 1):
            raise ValueError('invalid detection')
        _identity(d, 'class_name')
        points = d.get('keypoints')
        if points is not None:
            if not isinstance(points, (list, tuple)) or len(points) != 17:
                raise ValueError('invalid keypoints')
            for point in points:
                if not isinstance(point, (list, tuple)) or len(point) != 3 or not all(_number(v) for v in point) or not 0 <= point[2] <= 1:
                    raise ValueError('invalid keypoints')
    return value


def validate_event(value: dict) -> dict:
    if not isinstance(value, dict):
        raise ValueError('event must be an object')
    for key in ('schema_version', 'event_id', 'revision', 'camera_id', 'stream_epoch', 'track_key', 'type', 'state', 'start_media_ms', 'confirmed_media_ms', 'evidence'):
        if key not in value:
            raise ValueError(f'missing {key}')
    if value['schema_version'] != SCHEMA_VERSION:
        raise ValueError('unsupported schema_version')
    if value['type'] not in ('missing_helmet', 'suspected_fall', 'prolonged_lying'):
        raise ValueError('unsupported event type')
    if value['state'] not in ('open', 'closed', 'interrupted') or type(value['revision']) is not int or value['revision'] < 1:
        raise ValueError('invalid event state/revision')
    for key in ('event_id', 'camera_id', 'stream_epoch', 'track_key'):
        _identity(value, key)
    if not all(_number(value[k]) and value[k] >= 0 for k in ('confirmed_media_ms', 'start_media_ms')) or value['confirmed_media_ms'] < value['start_media_ms']:
        raise ValueError('invalid event times')
    if 'end_media_ms' in value and (not _number(value['end_media_ms']) or value['end_media_ms'] < value['confirmed_media_ms']):
        raise ValueError('invalid end_media_ms')
    evidence = value['evidence']
    if not isinstance(evidence, dict) or evidence.get('status') not in ('pending', 'ready', 'unavailable', 'partial'):
        raise ValueError('invalid evidence')
    for key in ('snapshot_ref', 'clip_ref'):
        if evidence.get(key) is not None and not isinstance(evidence[key], str):
            raise ValueError('invalid evidence reference')
    if evidence['status'] == 'ready' and not (evidence.get('snapshot_ref') or evidence.get('clip_ref')):
        raise ValueError('ready evidence requires a reference')
    if evidence.get('frame_id') is not None and (type(evidence['frame_id']) is not int or evidence['frame_id'] < 0):
        raise ValueError('invalid evidence frame_id')
    return value
