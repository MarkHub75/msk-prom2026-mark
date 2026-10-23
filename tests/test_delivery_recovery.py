"""Backend ACK loss, immutable retry destination and typed ACK contract."""
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler,HTTPServer
import io
import json
from pathlib import Path
import socket
import tempfile
import threading
import unittest
from unittest.mock import patch

from ml.pipeline.delivery import HttpEventSink,Outbox
from test_delivery import event


class DeliveryRecoveryTest(unittest.TestCase):
    def test_ack_lost_after_commit_retries_same_revision_without_duplicate_incident(self):
        committed={};notifications=set();received=[]
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                value=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                key=(value['event_id'],value['revision']);received.append(value)
                committed.setdefault(key,value);notifications.add(value['event_id'])
                if len(received)==1:
                    self.close_connection=True
                    self.connection.shutdown(socket.SHUT_RDWR)
                    self.connection.close();return
                body=json.dumps({'committed':True,'event_id':key[0],'revision':key[1]}).encode()
                self.send_response(200);self.send_header('Content-Length',str(len(body)))
                self.end_headers();self.wfile.write(body)
        server=HTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            with tempfile.TemporaryDirectory() as temporary:
                path=Path(temporary)/'events.sqlite'
                sink=HttpEventSink(f'http://127.0.0.1:{server.server_port}/events')
                box=Outbox(path);box.enqueue(event())
                self.assertEqual(box.dispatch(sink),0)
                self.assertEqual(box.counts()['pending'],1)
                box.close();box=Outbox(path)
                with box.db:box.db.execute('UPDATE outbox SET next_attempt=0')
                self.assertEqual(box.dispatch(sink),1)
                self.assertEqual(box.dispatch(sink),0)
                self.assertEqual(received[0],received[1])
                self.assertEqual((len(committed),len(notifications)),(1,1))
                box.close()
        finally:server.shutdown();server.server_close();thread.join()

    def test_destination_change_is_blocked_before_network_and_no_url_is_stored(self):
        with tempfile.TemporaryDirectory() as temporary:
            box=Outbox(Path(temporary)/'events.sqlite');box.enqueue(event())
            sink=HttpEventSink('http://127.0.0.1:1/events',timeout=.01,evidence_base_url='https://media.invalid/a')
            box.dispatch(sink)
            stored=box.checkpoint('delivery_destination')
            self.assertNotIn('http',json.dumps(stored))
            changed=HttpEventSink(sink.url,evidence_base_url='https://media.invalid/b')
            with patch.object(changed,'publish') as publish:
                with self.assertRaises(ValueError):box.dispatch(changed)
                publish.assert_not_called()
            box.close()

    def test_boolean_or_float_revision_ack_is_not_an_integer_commit_ack(self):
        for revision in (True,1.0):
            class Opener:
                @contextmanager
                def open(self,*args,**kwargs):
                    yield io.BytesIO(json.dumps({'committed':True,'event_id':'incident-1','revision':revision}).encode())
            with patch('urllib.request.build_opener',return_value=Opener()):
                with self.assertRaises(ValueError):HttpEventSink('http://localhost/events').publish(event())

    def test_delivered_legacy_rows_are_not_silently_rebound_to_new_backend(self):
        with tempfile.TemporaryDirectory() as temporary:
            box=Outbox(Path(temporary)/'events.sqlite');value=event();box.enqueue(value)
            with box.db:box.db.execute('UPDATE outbox SET delivered=1')
            box.enqueue({**value,'revision':2})
            sink=HttpEventSink('http://localhost/events')
            with patch.object(sink,'publish') as publish:
                with self.assertRaises(ValueError):box.dispatch(sink)
                publish.assert_not_called()
            box.close()
