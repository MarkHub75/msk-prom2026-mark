import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from ml.pipeline.backend_probe import run_probe
from ml.pipeline.local_sink import local_event_sink
from ml.pipeline.delivery import HttpEventSink
from test_delivery import event


class BackendProbeTest(unittest.TestCase):
    def test_post_ack_duplicate_journal_evidence_and_restart_use_one_incident(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);media=root/'evidence';media.mkdir()
            snapshot=media/'frame.jpg';snapshot.write_bytes(b'explicit media fixture')
            value={**event(),'execution_backend':'synthetic-test'}
            value['evidence']={'status':'ready','snapshot_ref':'evidence/frame.jpg','frame_id':10,'media_time_ms':2000}
            template=root/'template.json';template.write_text(json.dumps(value))
            with local_event_sink(root/'receiver',media) as receiver:
                kwargs={'event_url':receiver['event_url'],'journal_url':receiver['event_url']+'/{event_id}',
                    'event_file':template,'state_dir':root/'probe','evidence_base_url':receiver['evidence_base_url'],
                    'evidence_file':snapshot,'receiver_kind':'local-test'}
                first=run_probe(**kwargs);second=run_probe(**kwargs)
                self.assertEqual(first['event_id'],second['event_id'])
                self.assertEqual(first['evidence_http_sha256'],'PASS')
                self.assertEqual(first['receiver_kind'],'local-test')
                with patch('ml.pipeline.backend_probe._get',side_effect=TimeoutError('fixture timeout')):
                    with self.assertRaises(TimeoutError):run_probe(**kwargs)
                latest=json.loads((root/'probe/last-attempt.json').read_text())
                self.assertEqual(latest['status'],'NOT_COMPLETED')
                self.assertEqual(latest['event_id'],first['event_id'])
                run_probe(**kwargs)
                with self.assertRaises(ValueError):run_probe(**{**kwargs,'evidence_file':None})
                self.assertEqual(json.loads((root/'probe/last-attempt.json').read_text())['status'],'NOT_COMPLETED')
                with sqlite3.connect(receiver['database']) as db:
                    self.assertEqual(db.execute('SELECT count(*) FROM received').fetchone()[0],1)
                    self.assertEqual(db.execute('SELECT count(*) FROM notifications').fetchone()[0],1)

    def test_journal_returns_latest_revision_after_late_old_revision(self):
        from urllib.request import urlopen
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            with local_event_sink(root/'receiver',root/'evidence') as receiver:
                sink=HttpEventSink(receiver['event_url'])
                value=event();sink.publish({**value,'revision':2,'state':'interrupted','end_media_ms':2500})
                sink.publish(value)
                with urlopen(receiver['event_url']+'/'+value['event_id']) as response:latest=json.load(response)
                self.assertEqual(latest['revision'],2)
                self.assertEqual(latest['state'],'interrupted')
