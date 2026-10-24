"""Encoded-time checks; no neural inference or real-quality claim."""
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from ml.pipeline.video_clock import FilePTS
from ml.scenarios.cli import VideoEvidenceFrames
import numpy as np


class ScenarioClockTest(unittest.TestCase):
    def probe(self,times):
        return SimpleNamespace(returncode=0,stdout=json.dumps({'frames':[{'best_effort_timestamp_time':str(t)} for t in times]}).encode())

    def test_nonzero_encoded_origin_is_preserved(self):
        with patch('ml.pipeline.video_clock.subprocess.run',return_value=self.probe([.039,.079,.119])):
            clock=FilePTS('/synthetic-no-video')
        self.assertEqual(clock.at(0),39);self.assertEqual(clock.at(2),119)

    def test_duplicate_or_missing_pts_never_fabricates_frame_times(self):
        for values in ([],[0,0],[.1,.05],[float('nan')]):
            with self.subTest(values=values),patch('ml.pipeline.video_clock.subprocess.run',return_value=self.probe(values)):
                with self.assertRaises(ValueError):FilePTS('/synthetic-no-video')

    def test_invalid_frame_index_cannot_attach_neighbor_evidence(self):
        with patch('ml.pipeline.video_clock.subprocess.run',return_value=self.probe([.039])):clock=FilePTS('/synthetic-no-video')
        for index in (-1,1,True):
            with self.assertRaises(ValueError):clock.at(index)

    def test_evidence_uses_sequential_frame_ordinal_without_approximate_seek(self):
        class Capture:
            def __init__(self):self.reads=0
            def read(self):
                image=np.full((3,4,3),self.reads,dtype=np.uint8);self.reads+=1;return True,image
            def set(self,*args):raise AssertionError('approximate seeking must not be used')
            def release(self):pass
            def isOpened(self):return True
        cap=Capture();reader=object.__new__(VideoEvidenceFrames)
        reader.cv2=SimpleNamespace(COLOR_BGR2RGB=1,cvtColor=lambda bgr,code:bgr.copy(),VideoCapture=lambda path:Capture())
        reader.cap=cap;reader.path='/synthetic';reader.sha256='fixture';reader.clock=SimpleNamespace(at=lambda i:i*40)
        reader.cursor=-1;reader.last_frame=None
        batch={'source_sha256':'fixture','frame_id':5,'media_time_ms':200,'image_size':[4,3]}
        self.assertEqual(int(reader(batch)[0,0,0]),5);self.assertEqual(cap.reads,6)
        batch.update(frame_id=0,media_time_ms=0);self.assertEqual(int(reader(batch)[0,0,0]),0)
        batch['source_sha256']='wrong'
        with self.assertRaises(ValueError):reader(batch)
