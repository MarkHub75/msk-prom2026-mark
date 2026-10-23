import json
import tempfile
import unittest
from pathlib import Path
import numpy as np
from PIL import Image
from ml.behavior import BehaviorEngine
from ml.pipeline.runner import Pipeline
from ml.pipeline.delivery import Outbox
from test_behavior import batch, person, head

class PipelineTest(unittest.TestCase):
    def test_snapshot_event_commit_and_restart_suppression(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/'events.sqlite'
            box=Outbox(db);pipe=Pipeline(BehaviorEngine(),box,tmp)
            image=np.zeros((800,1000,3),dtype=np.uint8)
            for t in (0,500,1000,1500,2000):
                events=pipe.process(batch(t,[person(),head()]),image)
            self.assertEqual(len(events),1)
            ref=events[0]['evidence']['snapshot_ref']
            with Image.open(Path(tmp)/ref) as im: self.assertEqual(im.size,(1000,800))
            box.close()
            box=Outbox(db);pipe=Pipeline(BehaviorEngine(),box,tmp)
            self.assertEqual(pipe.process(batch(2500,[person(),head()]),image),[])
            events=pipe.process(batch(3000,[person(),head('helmet')]),image)
            self.assertEqual(events[0]['evidence']['snapshot_ref'],ref)
            self.assertEqual(box.counts()['pending'],2)
            box.close()

    def test_json_replay_has_no_fabricated_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            box=Outbox(Path(tmp)/'events.sqlite');pipe=Pipeline(BehaviorEngine(),box,tmp)
            for t in (0,500,1000,1500,2000): events=pipe.process(batch(t,[person(),head()]))
            self.assertEqual(events[0]['evidence']['status'],'unavailable')
            box.close()

    def test_persistence_failure_restores_candidate_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            box=Outbox(Path(tmp)/'events.sqlite');pipe=Pipeline(BehaviorEngine(),box,tmp)
            for t in (0,500,1000,1500): pipe.process(batch(t,[person(),head()]))
            original=box.commit_batch
            def broken(*args): raise OSError('disk unavailable')
            box.commit_batch=broken
            with self.assertRaises(OSError): pipe.process(batch(2000,[person(),head()]))
            box.commit_batch=original
            self.assertEqual(len(pipe.process(batch(2000,[person(),head()]))),1)
            box.close()
