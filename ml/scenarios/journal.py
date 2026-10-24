"""Internal candidates join the existing outbox transaction, never its API sink."""
import json
import hashlib
from .contracts import validate_candidate


class CandidateJournal:
    def __init__(self,db):
        self.db=db
        db.execute('CREATE TABLE IF NOT EXISTS scenario_candidates(candidate_id TEXT,revision INTEGER,body TEXT NOT NULL,PRIMARY KEY(candidate_id,revision))')
        db.execute('CREATE TABLE IF NOT EXISTS scenario_diagnostics(camera_id TEXT,epoch TEXT,frame_id INTEGER,input_sha256 TEXT NOT NULL,body TEXT NOT NULL,PRIMARY KEY(camera_id,epoch,frame_id))')
        db.commit()

    @staticmethod
    def input_digest(batch):
        keys=('camera_id','stream_epoch','frame_id','media_time_ms','image_size','status','detections','scenario_context','source_sha256')
        value={k:batch[k] for k in keys if k in batch}
        return hashlib.sha256(json.dumps(value,sort_keys=True,allow_nan=False).encode()).hexdigest()

    def seen(self,batch):
        row=self.db.execute('SELECT input_sha256 FROM scenario_diagnostics WHERE camera_id=? AND epoch=? AND frame_id=?',
                            (batch['camera_id'],batch['stream_epoch'],batch['frame_id'])).fetchone()
        if row and row[0]!=self.input_digest(batch):raise ValueError('committed scenario observation changed')
        return bool(row)

    def last_evidence(self,identity):
        row=self.db.execute('SELECT body FROM scenario_candidates WHERE candidate_id=? ORDER BY revision DESC LIMIT 1',(identity,)).fetchone()
        return json.loads(row[0])['evidence'] if row else None

    def commit(self,db,candidates,findings,state,batch):
        for event in candidates:
            validate_candidate(event);body=json.dumps(event,sort_keys=True,allow_nan=False)
            old=db.execute('SELECT body FROM scenario_candidates WHERE candidate_id=? AND revision=?',(event['candidate_id'],event['revision'])).fetchone()
            if old and old[0]!=body:raise ValueError('candidate revision is immutable')
            db.execute('INSERT OR IGNORE INTO scenario_candidates VALUES(?,?,?)',(event['candidate_id'],event['revision'],body))
        body=json.dumps({**{k:batch[k] for k in ('camera_id','stream_epoch','frame_id','media_time_ms')},'findings':findings},sort_keys=True,allow_nan=False)
        key=(batch['camera_id'],batch['stream_epoch'],batch['frame_id'])
        old=db.execute('SELECT body FROM scenario_diagnostics WHERE camera_id=? AND epoch=? AND frame_id=?',key).fetchone()
        if old and old[0]!=body:raise ValueError('scenario frame verdicts are immutable')
        db.execute('INSERT OR IGNORE INTO scenario_diagnostics VALUES(?,?,?,?,?)',(*key,self.input_digest(batch),body))
        db.execute("INSERT OR REPLACE INTO checkpoints(name,body) VALUES('scenarios',?)",(json.dumps(state,allow_nan=False),))
