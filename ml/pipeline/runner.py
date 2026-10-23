import json
import copy
from pathlib import Path
from ml.contracts import validate_observation
from ml.pipeline.evidence import save_snapshot


class Pipeline:
    def __init__(self, behavior, outbox, state_dir, sink=None):
        self.behavior, self.outbox = behavior, outbox
        self.state_dir, self.sink = Path(state_dir), sink
        self.latest = {}
        checkpoint = self.outbox.checkpoint()
        if checkpoint is not None:
            self.behavior.restore_state(checkpoint)

    def process(self, batch, frame=None, *, video_checkpoint=None):
        validate_observation(batch)
        key = (batch['camera_id'], batch['stream_epoch'])
        order = (batch['media_time_ms'], batch['frame_id'])
        if key in self.latest and order <= self.latest[key]:
            return []
        previous_state = self.behavior.export_state()
        try:
            events = copy.deepcopy(self.behavior.update(batch) if batch['status'] == 'ok' else self.behavior.on_gap(batch))
            for event in events:
                if 'source_kind' in batch:event['source_kind']=batch['source_kind']
                if event['state'] == 'open' and frame is not None:
                    event['evidence'] = {'frame_id': batch['frame_id'], 'snapshot_ref': save_snapshot(self.state_dir, batch, frame),
                                         'media_time_ms':batch['media_time_ms'],'clip_ref': None, 'status': 'ready'}
                elif self.outbox.last_evidence(event['event_id']):
                    event['evidence'] = self.outbox.last_evidence(event['event_id'])
                elif not event.get('evidence') or event['evidence'].get('status') == 'pending':
                    event['evidence'] = {'frame_id': batch['frame_id'], 'snapshot_ref': None, 'clip_ref': None, 'status': 'unavailable'}
            if video_checkpoint is None:
                self.outbox.commit_batch(events, self.behavior.export_state())
            else:
                self.outbox.commit_batch(events,self.behavior.export_state(),
                    video_checkpoint=video_checkpoint,observation=batch)
        except Exception:
            self.behavior.restore_state(previous_state)
            raise
        self.latest[key] = order
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
