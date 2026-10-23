import json
from pathlib import Path
from ml.contracts import validate_observation
from ml.pipeline.evidence import save_snapshot


class Pipeline:
    def __init__(self, behavior, outbox, state_dir, sink=None):
        self.behavior, self.outbox = behavior, outbox
        self.state_dir, self.sink = Path(state_dir), sink
        self.latest = {}

    def process(self, batch, frame=None):
        validate_observation(batch)
        key = (batch['camera_id'], batch['stream_epoch'])
        order = (batch['media_time_ms'], batch['frame_id'])
        if key in self.latest and order <= self.latest[key]:
            return []
        self.latest[key] = order
        events = self.behavior.update(batch) if batch['status'] == 'ok' else self.behavior.on_gap(batch)
        for event in events:
            if event['state'] == 'open' and frame is not None:
                event['evidence'] = {'frame_id': batch['frame_id'], 'snapshot_ref': save_snapshot(self.state_dir, batch, frame),
                                     'clip_ref': None, 'status': 'ready'}
            elif not event.get('evidence'):
                event['evidence'] = {'frame_id': batch['frame_id'], 'snapshot_ref': None, 'clip_ref': None, 'status': 'unavailable'}
            self.outbox.enqueue(event)
        if self.sink:
            self.outbox.dispatch(self.sink)
        return events


def read_jsonl(path):
    with open(path) as stream:
        for number, line in enumerate(stream, 1):
            if line.strip():
                try:
                    yield validate_observation(json.loads(line))
                except (ValueError, KeyError, TypeError) as exc:
                    raise ValueError(f'invalid observation line {number}') from exc
