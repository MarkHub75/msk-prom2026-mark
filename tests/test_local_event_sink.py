"""Real loopback HTTP contract exercise, explicitly a TEST backend."""
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError

from ml.pipeline.local_sink import local_event_sink
from ml.pipeline.delivery import HttpEventSink
from test_delivery import event


class LocalEventSinkTests(unittest.TestCase):
    def test_commit_dedup_revision_and_evidence_over_http(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);evidence=root/'state/evidence';evidence.mkdir(parents=True)
            (evidence/'frame.jpg').write_bytes(b'explicit test media fixture')
            with local_event_sink(root/'receiver',evidence) as receiver:
                sink=HttpEventSink(receiver['event_url'],evidence_base_url=receiver['evidence_base_url'])
                value=event();value['evidence']={'status':'ready','frame_id':40,'media_time_ms':2000,'snapshot_ref':'evidence/frame.jpg'}
                sink.publish(value);sink.publish(value)
                value={**value,'revision':2,'state':'interrupted','end_media_ms':2500}
                sink.publish(value)
                with sqlite3.connect(receiver['database']) as db:
                    self.assertEqual(db.execute('SELECT count(*) FROM received').fetchone()[0],2)
                    self.assertEqual(db.execute('SELECT count(*) FROM notifications').fetchone()[0],1)
                    snapshot=json.loads(db.execute('SELECT body FROM received LIMIT 1').fetchone()[0])['evidence']['snapshot_ref']
                with urlopen(snapshot) as response:self.assertEqual(response.read(),b'explicit test media fixture')
                with self.assertRaises(HTTPError):urlopen(receiver['evidence_base_url']+'/evidence/../receiver.sqlite')
