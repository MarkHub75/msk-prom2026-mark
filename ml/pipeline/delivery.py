"""At-least-once transport; the receiver must deduplicate event/revision."""
import json
import sqlite3
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from ml.contracts import validate_event


class Outbox:
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('''CREATE TABLE IF NOT EXISTS outbox (
            event_id TEXT, revision INTEGER, body TEXT NOT NULL,
            delivered INTEGER NOT NULL DEFAULT 0, attempts INTEGER NOT NULL DEFAULT 0,
            next_attempt REAL NOT NULL DEFAULT 0, last_error TEXT,
            PRIMARY KEY(event_id, revision))''')
        self.db.execute('CREATE TABLE IF NOT EXISTS checkpoints (name TEXT PRIMARY KEY, body TEXT NOT NULL)')
        self.db.execute('''CREATE TABLE IF NOT EXISTS observations (
            camera_id TEXT, stream_epoch TEXT, frame_id INTEGER, body TEXT NOT NULL,
            PRIMARY KEY(camera_id,stream_epoch,frame_id))''')
        self.db.commit()

    def checkpoint(self, name='behavior'):
        row = self.db.execute('SELECT body FROM checkpoints WHERE name=?', (name,)).fetchone()
        return json.loads(row[0]) if row else None

    def last_evidence(self, event_id):
        row = self.db.execute('SELECT body FROM outbox WHERE event_id=? ORDER BY revision DESC LIMIT 1', (event_id,)).fetchone()
        return json.loads(row[0]).get('evidence') if row else None

    def commit_batch(self, events, state, *, video_checkpoint=None, observation=None, extension=None):
        with self.db:
            for event in events:
                self._enqueue(event)
            self.db.execute("INSERT OR REPLACE INTO checkpoints(name,body) VALUES('behavior',?)",
                            (json.dumps(state, allow_nan=False),))
            if video_checkpoint is not None:
                self.db.execute("INSERT OR REPLACE INTO checkpoints(name,body) VALUES('video',?)",
                                (json.dumps(video_checkpoint, allow_nan=False),))
            if observation is not None:
                body=json.dumps(observation,allow_nan=False,sort_keys=True)
                key=(observation['camera_id'],observation['stream_epoch'],observation['frame_id'])
                old=self.db.execute('SELECT body FROM observations WHERE camera_id=? AND stream_epoch=? AND frame_id=?',key).fetchone()
                if old and old[0]!=body:raise ValueError('committed observation is immutable')
                self.db.execute('INSERT OR IGNORE INTO observations VALUES(?,?,?,?)',(*key,body))
            if extension is not None:extension(self.db)

    def export_jsonl(self, directory):
        """Rebuild exports from committed rows: retries cannot append duplicates."""
        import os
        from uuid import uuid4
        directory=Path(directory)
        exports=[('events','outbox'),('observations','observations')]
        for name,table in (('candidates','scenario_candidates'),('scenario-diagnostics','scenario_diagnostics')):
            if self.db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",(table,)).fetchone():exports.append((name,table))
        for name,table in exports:
            target=directory/(name+'.jsonl');temporary=directory/(name+'.'+uuid4().hex+'.tmp')
            try:
                fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
                with os.fdopen(fd,'w') as stream:
                    for row in self.db.execute('SELECT body FROM '+table+' ORDER BY rowid'):
                        stream.write(row[0]+'\n')
                    stream.flush();os.fsync(stream.fileno())
                os.replace(temporary,target)
            finally:temporary.unlink(missing_ok=True)

    def enqueue(self, event):
        with self.db:
            self._enqueue(event)

    def _enqueue(self, event):
        validate_event(event)
        body = json.dumps(event, allow_nan=False, sort_keys=True)
        old = self.db.execute('SELECT body FROM outbox WHERE event_id=? AND revision=?',
                              (event['event_id'], event['revision'])).fetchone()
        if old and old[0] != body:
            raise ValueError('event revision is immutable')
        self.db.execute('INSERT OR IGNORE INTO outbox(event_id,revision,body) VALUES(?,?,?)',
                        (event['event_id'], event['revision'], body))

    def dispatch(self, sink, limit=20):
        rows = self.db.execute('''SELECT event_id, revision, body, attempts FROM outbox
            WHERE delivered=0 AND next_attempt<=? ORDER BY rowid LIMIT ?''', (time.time(), limit)).fetchall()
        if (rows or self.checkpoint('delivery_destination') is not None) and getattr(sink,'delivery_identity',None) is not None:
            self._bind_destination(sink.delivery_identity)
        sent = 0
        for event_id, revision, body, attempts in rows:
            try:
                sink.publish(json.loads(body))
            except Exception as exc:
                # Do not persist URLs, credentials, response bodies or arbitrary exception text.
                with self.db:
                    self.db.execute('''UPDATE outbox SET attempts=attempts+1,next_attempt=?,last_error=?
                        WHERE event_id=? AND revision=?''',
                        (time.time() + min(60, 2 ** min(attempts, 6)), type(exc).__name__, event_id, revision))
                continue
            with self.db:
                self.db.execute('UPDATE outbox SET delivered=1,attempts=attempts+1,last_error=NULL WHERE event_id=? AND revision=?',
                                (event_id, revision))
            sent += 1
        return sent

    def _bind_destination(self, identity):
        """Keep retries byte-stable and prevent silently switching the receiver."""
        if not isinstance(identity,str) or len(identity)!=64:
            raise ValueError('invalid receiver identity digest')
        old=self.checkpoint('delivery_destination')
        if old is not None:
            if old.get('sha256')!=identity:
                raise ValueError('outbox is already bound to another receiver/evidence prefix')
            return
        if self.db.execute('SELECT 1 FROM outbox WHERE delivered=1 LIMIT 1').fetchone():
            raise ValueError('legacy delivered outbox has no receiver identity; use a separate state directory')
        with self.db:
            self.db.execute("INSERT INTO checkpoints(name,body) VALUES('delivery_destination',?)",
                            (json.dumps({'schema_version':'1.0','sha256':identity}),))

    def counts(self):
        return {name: self.db.execute('SELECT count(*) FROM outbox WHERE delivered=?', (flag,)).fetchone()[0]
                for name, flag in [('pending', 0), ('delivered', 1)]}

    def close(self):
        self.db.close()


class HttpEventSink:
    """ACK JSON must contain committed:true plus the exact event_id/revision.

    evidence_base_url is a receiver-accessible artifact prefix, never an inference API.
    This client intentionally supports no redirects to avoid forwarding credentials.
    """
    def __init__(self, url, token=None, timeout=5, evidence_base_url=None):
        import hashlib
        import math
        from urllib.parse import urlsplit
        parts = urlsplit(url)
        if parts.scheme not in ('http', 'https') or not parts.netloc or parts.username or parts.password or parts.fragment:
            raise ValueError('invalid backend URL')
        if token and parts.scheme != 'https' and parts.hostname not in ('localhost', '127.0.0.1', '::1'):
            raise ValueError('authenticated remote backend requires HTTPS')
        if isinstance(timeout,bool) or not isinstance(timeout,(int,float)) or not math.isfinite(timeout) or timeout<=0:
            raise ValueError('finite positive delivery timeout required')
        self.url, self.token, self.timeout = url, token, timeout
        self.evidence_base_url = evidence_base_url
        if evidence_base_url is not None:
            media=urlsplit(evidence_base_url)
            if (media.scheme not in ('http','https') or not media.netloc or media.username or media.password or
                media.query or media.fragment):raise ValueError('invalid evidence URL prefix')
        self.delivery_identity=hashlib.sha256(json.dumps({'event_url':url,'evidence_base_url':evidence_base_url},sort_keys=True).encode()).hexdigest()

    def prepare_payload(self, event):
        """Render the existing v1 payload without publishing or mutating it."""
        payload = dict(event)
        evidence = dict(payload['evidence'])
        if evidence.get('status') == 'ready':
            if not self.evidence_base_url:
                raise ValueError('receiver-accessible evidence_base_url is required')
            from urllib.parse import quote
            from pathlib import PurePosixPath
            for key in ('snapshot_ref', 'clip_ref'):
                reference = evidence.get(key)
                if not reference:
                    continue
                path = PurePosixPath(reference)
                if path.is_absolute() or '..' in path.parts or ':' in reference or '\\' in reference:
                    raise ValueError('evidence reference must be a relative artifact path')
                evidence[key] = self.evidence_base_url.rstrip('/') + '/' + quote(reference, safe='/')
        payload['evidence'] = evidence
        return payload

    def publish(self, event):
        from urllib.request import build_opener, HTTPRedirectHandler
        class NoRedirect(HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None
        payload=self.prepare_payload(event)
        headers = {'Content-Type': 'application/json', 'Idempotency-Key': f"{event['event_id']}:{event['revision']}"}
        if self.token:
            headers['Authorization'] = 'Bearer ' + self.token
        request = Request(self.url, json.dumps(payload, allow_nan=False).encode(), headers, method='POST')
        with build_opener(NoRedirect).open(request, timeout=self.timeout) as response:
            ack = json.loads(response.read(65536))
        if (not isinstance(ack,dict) or ack.get('committed') is not True or
            not isinstance(ack.get('event_id'),str) or ack['event_id']!=event['event_id'] or
            type(ack.get('revision')) is not int or ack['revision']!=event['revision']):
            raise ValueError('backend did not acknowledge committed event revision')
        return ack
