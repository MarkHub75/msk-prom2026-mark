"""Synthetic video/adapter integration tests; these do not execute LinQ."""
import json
import io
from contextlib import redirect_stdout
from pathlib import Path
import sqlite3
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from uuid import uuid4

import cv2
import numpy as np
from ml.behavior import BehaviorEngine
from ml.pipeline.delivery import Outbox
from ml.pipeline.runner import Pipeline
from ml.pipeline.file_video import run_file_video


def people():
    points=[[0,0,0] for _ in range(17)]
    points[0]=[40,10,.99]
    points[5]=[30,30,.99];points[6]=[50,30,.99]
    points[11]=[30,60,.99];points[12]=[50,60,.99]
    return [{'class_name':'person','score':.99,'bbox_xyxy':[10,0,70,79],
             'keypoints':points,'detection_id':'person'}]


class FakeBackend:
    def __init__(self,model_id):self.model_id=model_id;self.calls=[];self.pending_frame=None
    def infer(self,request):
        self.calls.append(request['request_id'])
        frame=int(request['request_id'].split(':')[1])
        result={'request_id':request['request_id'],'model_id':self.model_id,'backend':'linq',
            'status':'ok','outputs':{'model':self.model_id},
            'execution_witness':{'request_id':request['request_id'],'model_id':self.model_id,
                'program_sha256':'0'*64,'device_kind':'linq_tpu','completed':True},
            'transport_provenance':{'request_id':str(uuid4()),'status_code':0,
                'journal_state':'COMPLETED','remote_completion':'response_received','timings':{'total_ms':1}}}
        if frame==self.pending_frame:result.update(status='pending',error={'code':'linq_pending'})
        return result


class FileVideoTests(unittest.TestCase):
    def fixture(self,root):
        source=root/'synthetic.avi'
        writer=cv2.VideoWriter(str(source),cv2.VideoWriter_fourcc(*'MJPG'),20,(100,80))
        self.assertTrue(writer.isOpened())
        for i in range(61):writer.write(np.full((80,100,3),i,np.uint8))
        writer.release()
        args=SimpleNamespace(source=str(source),state_dir=str(root/'state'),camera_id='synthetic-camera',
            linq_runner_factory='synthetic-only',source_kind='repeated-image-fixture',sample_fps=2,start_ms=0,end_ms=None,max_frames=0)
        manifests=[{'model_id':model,'input':{'name':'images'},
                    'linq':{'program_sha256':'0'*64}} for model in ('pose','helmet')]
        backends=[FakeBackend(m['model_id']) for m in manifests]
        return args,manifests,backends

    def execute(self,args,manifests,backends):
        root=Path(args.state_dir);box=Outbox(root/'events.sqlite')
        pipeline=Pipeline(BehaviorEngine(),box,root)
        cap=cv2.VideoCapture(args.source)
        def decode(outputs,manifest,transform):
            if outputs['model']=='pose':return people()
            return [{'class_name':'bare_head','score':.99,'bbox_xyxy':[25,0,55,20],
                     'keypoints':None,'detection_id':'head'}]
        try:
            with redirect_stdout(io.StringIO()),patch('ml.pipeline.file_video.GLOBAL_VIDEO_LOCK',root/'test-global.lock'),patch('ml.pipeline.file_video.preprocess',return_value=(np.zeros((1,3,4,4),np.float32),None)),patch('ml.pipeline.file_video.decode',side_effect=decode):
                return run_file_video(args,pipeline,cap,manifests,backends,cap.get(cv2.CAP_PROP_FPS))
        finally:cap.release();box.close()

    def test_pause_restart_stable_epoch_one_episode_and_original_evidence_pts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);args,manifests,backends=self.fixture(root)
            args.max_frames=3
            first=self.execute(args,manifests,backends)
            self.assertEqual(first['status'],'PAUSED')
            args.max_frames=0
            second=self.execute(args,manifests,backends)
            self.assertEqual(first['stream_epoch'],second['stream_epoch'])
            self.assertEqual(second['processed_frames'],7)
            events=[json.loads(line) for line in (Path(args.state_dir)/'events.jsonl').read_text().splitlines()]
            self.assertEqual(len({e['event_id'] for e in events}),1)
            self.assertEqual([e['state'] for e in events],['open','interrupted'])
            opened=events[0];self.assertAlmostEqual(opened['confirmed_media_ms'],2000)
            self.assertEqual(opened['source_kind'],'repeated-image-fixture')
            self.assertEqual(opened['evidence']['frame_id'],40)
            self.assertAlmostEqual(opened['evidence']['media_time_ms'],2000)
            sidecar=Path(args.state_dir)/Path(opened['evidence']['snapshot_ref']).with_suffix('.json')
            self.assertEqual(json.loads(sidecar.read_text())['frame_id'],40)
            calls=sum(len(b.calls) for b in backends)
            cached=self.execute(args,manifests,backends)
            self.assertEqual(cached['status'],'COMPLETED_CACHED')
            self.assertEqual(cached['frames_this_invocation'],0)
            self.assertEqual(cached['new_remote_requests'],0)
            self.assertIsNone(cached['frame_cycle_p50_ms'])
            self.assertEqual(sum(len(b.calls) for b in backends),calls)

    def test_pending_stops_same_frame_without_gap_or_new_epoch(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);args,manifests,backends=self.fixture(root)
            backends[1].pending_frame=10
            first=self.execute(args,manifests,backends)
            self.assertEqual(first['status'],'WAITING_FOR_LINQ')
            self.assertEqual(first['processed_frames'],1)
            with sqlite3.connect(Path(args.state_dir)/'events.sqlite') as db:
                cursor=json.loads(db.execute("SELECT body FROM checkpoints WHERE name='video'").fetchone()[0])
            self.assertEqual(cursor['frame_id'],0)
            backends[1].pending_frame=None
            second=self.execute(args,manifests,backends)
            self.assertEqual(second['stream_epoch'],first['stream_epoch'])
            events=[json.loads(line) for line in (Path(args.state_dir)/'events.jsonl').read_text().splitlines()]
            self.assertEqual(len({e['event_id'] for e in events}),1)
            args.sample_fps=3
            before=sum(len(b.calls) for b in backends)
            with self.assertRaises(ValueError):self.execute(args,manifests,backends)
            self.assertEqual(sum(len(b.calls) for b in backends),before)

    def test_observation_cursor_and_behavior_roll_back_together(self):
        with tempfile.TemporaryDirectory() as temporary:
            box=Outbox(Path(temporary)/'events.sqlite')
            try:
                box.db.execute("CREATE TRIGGER fail_observation BEFORE INSERT ON observations BEGIN SELECT RAISE(ABORT,'fixture'); END")
                observation={'camera_id':'test','stream_epoch':'synthetic','frame_id':0}
                with self.assertRaises(sqlite3.IntegrityError):
                    box.commit_batch([],{'version':1},video_checkpoint={'frame_id':0},observation=observation)
                self.assertIsNone(box.checkpoint())
                self.assertIsNone(box.checkpoint('video'))
            finally:box.close()
