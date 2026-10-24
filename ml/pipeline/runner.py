import json
import copy
from pathlib import Path
from ml.contracts import validate_observation
from ml.pipeline.evidence import save_snapshot


class Pipeline:
    def __init__(self, behavior, outbox, state_dir, sink=None, scenario_suite=None):
        self.behavior, self.outbox = behavior, outbox
        self.state_dir, self.sink = Path(state_dir), sink
        self.latest = {}
        self.scenario_suite=scenario_suite;self.candidate_journal=None;self.last_candidates=[]
        checkpoint = self.outbox.checkpoint()
        if checkpoint is not None:
            self.behavior.restore_state(checkpoint)
        if scenario_suite is not None:
            from ml.scenarios.journal import CandidateJournal
            self.candidate_journal=CandidateJournal(outbox.db)
            checkpoint=outbox.checkpoint('scenarios')
            if checkpoint is not None:scenario_suite.restore_state(checkpoint)

    def process(self, batch, frame=None, *, video_checkpoint=None):
        validate_observation(batch)
        self.last_candidates=[]
        if self.candidate_journal is not None:
            if self.candidate_journal.seen(batch):return []
            camera=self.behavior.export_state()['cameras'].get(batch['camera_id'])
            if camera and (batch['stream_epoch'] in camera['retired_epochs'] or camera['epoch']==batch['stream_epoch'] and
                           camera['last_time'] is not None and (batch['media_time_ms']<=camera['last_time'] or camera['last_frame'] is not None and batch['frame_id']<=camera['last_frame'])):return []
        key = (batch['camera_id'], batch['stream_epoch'])
        order = (batch['media_time_ms'], batch['frame_id'])
        if key in self.latest and order <= self.latest[key]:
            return []
        previous_state = self.behavior.export_state()
        scenario_state=self.scenario_suite.export_state() if self.scenario_suite is not None else None
        try:
            events = copy.deepcopy(self.behavior.update(batch) if batch['status'] == 'ok' else self.behavior.on_gap(batch))
            candidates,findings=self.scenario_suite.update(batch,self.behavior,events) if self.scenario_suite is not None else ([],[])
            for event in events:
                if 'source_kind' in batch:event['source_kind']=batch['source_kind']
                if event['state'] == 'open' and frame is not None:
                    event['evidence'] = {'frame_id': batch['frame_id'], 'snapshot_ref': save_snapshot(self.state_dir, batch, frame),
                                         'media_time_ms':batch['media_time_ms'],'clip_ref': None, 'status': 'ready'}
                elif self.outbox.last_evidence(event['event_id']):
                    event['evidence'] = self.outbox.last_evidence(event['event_id'])
                elif not event.get('evidence') or event['evidence'].get('status') == 'pending':
                    event['evidence'] = {'frame_id': batch['frame_id'], 'snapshot_ref': None, 'clip_ref': None, 'status': 'unavailable'}
            for event in candidates:
                if event['state']=='open' and frame is not None and event['camera_id']==batch['camera_id'] and event['stream_epoch']==batch['stream_epoch']:
                    event['evidence']={'frame_id':batch['frame_id'],'media_time_ms':batch['media_time_ms'],
                        'snapshot_ref':save_snapshot(self.state_dir,batch,frame),'clip_ref':None,'status':'ready'}
                else:
                    event['evidence']=self.candidate_journal.last_evidence(event['candidate_id']) or {
                        'frame_id':event['evidence']['frame_id'],'media_time_ms':event['evidence']['media_time_ms'],
                        'snapshot_ref':None,'clip_ref':None,'status':'unavailable'}
            if self.scenario_suite is not None:
                self.outbox.commit_batch(events,self.behavior.export_state(),video_checkpoint=video_checkpoint,observation=batch,
                    extension=lambda db:self.candidate_journal.commit(db,candidates,findings,self.scenario_suite.export_state(),batch))
            elif video_checkpoint is None:
                self.outbox.commit_batch(events, self.behavior.export_state())
            else:
                self.outbox.commit_batch(events,self.behavior.export_state(),
                    video_checkpoint=video_checkpoint,observation=batch)
        except Exception:
            self.behavior.restore_state(previous_state)
            if self.scenario_suite is not None:self.scenario_suite.restore_state(scenario_state)
            raise
        self.last_candidates=candidates
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
