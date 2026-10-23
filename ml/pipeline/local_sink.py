"""Loopback-only TEST receiver for the existing event contract, not team backend.

Use as a context manager for bounded integration tests. It persists before ACK,
deduplicates revisions/alerts and serves only explicitly rooted evidence files.
"""
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import json
from pathlib import Path
import sqlite3
import threading
from urllib.parse import unquote,urlsplit

from ml.contracts import validate_event
from ml.pipeline.capture_recovery import save_json


@contextmanager
def local_event_sink(directory,evidence_root):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    database=directory/'receiver.sqlite'
    evidence_root=Path(evidence_root).resolve()
    with sqlite3.connect(database) as db:
        db.execute('PRAGMA synchronous=FULL')
        db.execute('CREATE TABLE IF NOT EXISTS received(event_id TEXT,revision INTEGER,body TEXT NOT NULL,PRIMARY KEY(event_id,revision))')
        db.execute('CREATE TABLE IF NOT EXISTS notifications(event_id TEXT PRIMARY KEY)')
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_POST(self):
            if self.path!='/api/v1/ml/events':self.send_error(404);return
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=1024*1024:raise ValueError('invalid payload size')
                event=validate_event(json.loads(self.rfile.read(size)))
                key=(event['event_id'],event['revision'])
                if self.headers.get('Idempotency-Key')!=f'{key[0]}:{key[1]}':raise ValueError('missing identity')
                body=json.dumps(event,sort_keys=True,allow_nan=False)
                with sqlite3.connect(database) as db:
                    db.execute('PRAGMA synchronous=FULL')
                    old=db.execute('SELECT body FROM received WHERE event_id=? AND revision=?',key).fetchone()
                    if old and old[0]!=body:raise ValueError('immutable revision mismatch')
                    db.execute('INSERT OR IGNORE INTO received VALUES(?,?,?)',(*key,body))
                    if event['state']=='open':db.execute('INSERT OR IGNORE INTO notifications VALUES(?)',(event['event_id'],))
                # The transaction context committed before this acknowledgment.
                value=json.dumps({'committed':True,'event_id':key[0],'revision':key[1]}).encode()
                self.send_response(200);self.send_header('Content-Type','application/json')
                self.send_header('Content-Length',str(len(value)));self.end_headers();self.wfile.write(value)
            except Exception:self.send_error(400,'invalid event')
        def do_GET(self):
            path=unquote(urlsplit(self.path).path)
            if not path.startswith('/evidence/') or '\\' in path:self.send_error(404);return
            candidate=(evidence_root/path.removeprefix('/evidence/')).resolve()
            if (not candidate.is_relative_to(evidence_root) or candidate.suffix not in ('.jpg','.json') or
                not candidate.is_file()):self.send_error(404);return
            data=candidate.read_bytes();self.send_response(200)
            self.send_header('Content-Type','image/jpeg' if candidate.suffix=='.jpg' else 'application/json')
            self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    config_path=directory/'receiver-config.json'
    port=json.loads(config_path.read_text())['port'] if config_path.exists() else 0
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    if not config_path.exists():save_json(config_path,{'kind':'local_test_sink','port':server.server_port})
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base=f'http://127.0.0.1:{server.server_port}'
    try:yield {'event_url':base+'/api/v1/ml/events','evidence_base_url':base,'database':str(database),'kind':'local_test_sink'}
    finally:server.shutdown();server.server_close();thread.join()
