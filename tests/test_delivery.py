import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from ml.pipeline.delivery import Outbox, HttpEventSink


def event():
    return {'schema_version':'1.0','event_id':'incident-1','revision':1,'camera_id':'cam',
            'stream_epoch':'s','track_key':'cam/s/1/1','type':'missing_helmet','state':'open',
            'start_media_ms':0,'confirmed_media_ms':2000,'evidence':{'status':'unavailable'}}


class DeliveryTest(unittest.TestCase):
    def test_commit_restart_retry_immutable_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'events.sqlite'
            box = Outbox(path)
            box.enqueue(event()); box.enqueue(event())
            changed = event(); changed['state'] = 'closed'
            with self.assertRaises(ValueError): box.enqueue(changed)
            box.close(); box = Outbox(path)
            self.assertEqual(box.counts(), {'pending':1,'delivered':0})
            class Failed:
                def publish(self, event): raise RuntimeError('secret must not be persisted')
            self.assertEqual(box.dispatch(Failed()),0)
            self.assertEqual(box.db.execute('SELECT last_error FROM outbox').fetchone()[0], 'RuntimeError')
            box.db.execute('UPDATE outbox SET next_attempt=0'); box.db.commit()
            class Success:
                def publish(self, event): return True
            self.assertEqual(box.dispatch(Success()),1)
            self.assertEqual(box.dispatch(Success()),0)
            box.close()

    def test_http_requires_committed_matching_ack(self):
        class Handler(BaseHTTPRequestHandler):
            committed = False
            def do_POST(self):
                value=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                self.send_response(200); self.end_headers()
                self.wfile.write(json.dumps({'event_id':value['event_id'],'revision':value['revision'], 'committed':self.committed}).encode())
            def log_message(self,*args): pass
        server=HTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            sink=HttpEventSink(f'http://127.0.0.1:{server.server_port}/api/v1/ml/events')
            with self.assertRaises(ValueError): sink.publish(event())
            Handler.committed=True
            self.assertTrue(sink.publish(event())['committed'])
        finally:
            server.shutdown();server.server_close();thread.join()

    def test_remote_secret_requires_tls(self):
        with self.assertRaises(ValueError): HttpEventSink('http://example.com/events',token='private')

if __name__ == '__main__': unittest.main()

class EvidenceReferenceTest(unittest.TestCase):
    def test_clip_only_reference_uses_artifact_prefix(self):
        from unittest.mock import patch
        from contextlib import contextmanager
        import io
        value=event();value['evidence']={'status':'ready','snapshot_ref':None,'clip_ref':'evidence/clip name.mp4'}
        seen=[]
        class Opener:
            @contextmanager
            def open(self, request, timeout):
                seen.append(json.loads(request.data))
                yield io.BytesIO(json.dumps({'committed':True,'event_id':value['event_id'],'revision':1}).encode())
        with patch('urllib.request.build_opener',return_value=Opener()):
            HttpEventSink('http://localhost/events',evidence_base_url='https://media.example/').publish(value)
        self.assertIsNone(seen[0]['evidence']['snapshot_ref'])
        self.assertEqual(seen[0]['evidence']['clip_ref'],'https://media.example/evidence/clip%20name.mp4')

    def test_parent_escape_is_rejected_before_network(self):
        from unittest.mock import patch
        value=event();value['evidence']={'status':'ready','snapshot_ref':'../events.sqlite'}
        with patch('urllib.request.build_opener') as opener:
            with self.assertRaises(ValueError):
                HttpEventSink('http://localhost/events',evidence_base_url='https://media.example/').publish(value)
            opener.assert_not_called()
