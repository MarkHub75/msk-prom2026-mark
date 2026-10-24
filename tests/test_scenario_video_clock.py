"""Encoded-time checks; no neural inference or real-quality claim."""
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from ml.pipeline.video_clock import FilePTS


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
