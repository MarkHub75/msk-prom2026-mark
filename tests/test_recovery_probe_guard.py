"""The destructive-to-client diagnostic is one-shot, never an automatic retry."""
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from ml.pipeline.linq_recovery_probe import run_probe


class RecoveryProbeGuardTests(unittest.TestCase):
    def test_existing_intent_stops_before_any_new_connection_or_publication(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            (root/'video-session.json').write_text(json.dumps({'source_kind':'real-video'}))
            with sqlite3.connect(root/'events.sqlite') as db:
                db.execute('CREATE TABLE checkpoints(name TEXT PRIMARY KEY,body TEXT)')
                db.execute('INSERT INTO checkpoints VALUES(?,?)',('video',json.dumps({'frame_id':0,'complete':False})))
            report=root/'client-disconnect-check';report.mkdir();(report/'intent.json').write_text('{}')
            with patch('pika.BlockingConnection',side_effect=AssertionError('must not connect')) as connect:
                with self.assertRaisesRegex(ValueError,'already started'):
                    run_probe(root,root/'unused-source.mp4')
                connect.assert_not_called()
