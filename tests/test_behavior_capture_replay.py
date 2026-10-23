"""Replay real saved decoded captures; never a video or live-TPU benchmark.

External artifacts stay outside Git. Tests are skipped where captures are absent;
when available their exact files and numeric input hashes are checked. Derived
negative controls are explicitly marked and never represented as model outputs.
"""
import hashlib
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

import numpy as np
from ml.behavior import BehaviorEngine
from ml.behavior.scenarios import build_scenario
from ml.pipeline.delivery import Outbox
from ml.pipeline.runner import Pipeline

CAPTURE_ROOT = Path('/workspace/artifacts/linq-rpc')
EXPECTED_INPUT_SHA256 = '9f03adcc058f220364e1c1ebcc5e41051702228a11083c655356413bd4611160'
DECODED_SHA256 = {
    'helmet-001': 'ab82001d1b966708e3c6021c06340903b297a9314cc38de4887451afb2abb29b',
    'pose-split-001': '49812809f785bcb511a31d71a49a3a096987ebd184149c9c3da750c6b1acabeb',
}
DEMO_POLICY = {'min_score': 0.25, 'keypoint_score': 0.5,
               'allow_bbox_head_association': False, 'rule_version': 'demo-capture-replay-v1'}


class SavedCaptureReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        required = [CAPTURE_ROOT/name/file for name in DECODED_SHA256
                    for file in ('detections.json', 'capture.json', 'inputs.npz')]
        if not all(p.is_file() for p in required):
            raise unittest.SkipTest('external saved Helmet/SplitPose captures are unavailable')
        cls.decoded = {}
        for name, digest in DECODED_SHA256.items():
            directory = CAPTURE_ROOT/name
            raw = (directory/'detections.json').read_bytes()
            if hashlib.sha256(raw).hexdigest() != digest:
                raise AssertionError('saved decoded capture differs from pinned fixture')
            metadata = json.loads((directory/'capture.json').read_text())
            if metadata['status'] != 'completed':
                raise AssertionError('source capture is not marked completed')
            if metadata['inputs']['images']['sha256'] != EXPECTED_INPUT_SHA256:
                raise AssertionError('source metadata no longer identifies the expected input')
            with np.load(directory/'inputs.npz', allow_pickle=False) as archive:
                images = archive['images']
                if images.dtype != np.float32 or images.shape != (1, 3, 640, 640):
                    raise AssertionError('unexpected numeric input ABI')
                if hashlib.sha256(images.tobytes()).hexdigest() != EXPECTED_INPUT_SHA256:
                    raise AssertionError('numeric input identity differs')
            cls.decoded[name] = json.loads(raw)
        cls.detections = cls.decoded['pose-split-001'] + cls.decoded['helmet-001']

    def observation(self, t, *, detections=None, status='ok', modified=False):
        return {'schema_version': '1.0', 'camera_id': 'saved-bus-capture-replay',
                'stream_epoch': 'repeated-single-image-not-video', 'frame_id': t//500,
                'media_time_ms': t, 'image_size': [810, 1080],
                'request_id': f'capture-replay-{t}',
                'model_id': 'replayed-decoded-pose-and-helmet',
                'model_ids': ['pose-split-v1', 'helmet-v1'],
                'backend': 'replayed-real-capture', 'status': status,
                'detections': deepcopy(self.detections if detections is None else detections),
                'replay_provenance': {
                    'repeated_single_input': True, 'video_inference_performed': False,
                    'live_inference_performed': False, 'modified_negative_control': modified,
                    'original_input_sha256': EXPECTED_INPUT_SHA256,
                    'decoded_file_sha256': dict(DECODED_SHA256)}}

    def test_default_policy_abstains_on_actual_low_head_scores(self):
        engine = BehaviorEngine()
        for t in range(0, 4501, 500):
            self.assertEqual(engine.update(self.observation(t)), [])
        self.assertEqual([d['score'] for d in self.decoded['helmet-001']],
                         [0.35258615016937256, 0.25950342416763306])

    def test_explicit_demo_policy_confirms_two_owners_preserves_restart_identity(self):
        original = json.dumps(self.detections, sort_keys=True)
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory)/'outbox.sqlite3'
            outbox = Outbox(db)
            pipeline = Pipeline(BehaviorEngine(DEMO_POLICY), outbox, directory)
            events = []
            for t in (0, 500, 1000, 1500, 2000):
                events.extend(pipeline.process(self.observation(t)))
            self.assertEqual(len(events), 2)
            self.assertEqual({e['type'] for e in events}, {'missing_helmet'})
            self.assertEqual({e['confirmed_media_ms'] for e in events}, {2000})
            self.assertEqual({e['execution_backend'] for e in events}, {'replayed-real-capture'})
            self.assertEqual(len({e['track_key'] for e in events}), 2)
            self.assertEqual({e['revision'] for e in events}, {1})
            self.assertEqual({e['evidence']['status'] for e in events}, {'unavailable'})
            before = outbox.checkpoint()
            ids = {e['event_id'] for e in events}
            outbox.close()
            outbox = Outbox(db)
            pipeline = Pipeline(BehaviorEngine(DEMO_POLICY), outbox, directory)
            self.assertEqual(pipeline.behavior.export_state(), before)
            for t in range(2500, 6501, 500):
                self.assertEqual(pipeline.process(self.observation(t)), [])
            for t in range(0, 6501, 500):
                self.assertEqual(pipeline.process(self.observation(t)), [])
            rows = [json.loads(row[0]) for row in outbox.db.execute('SELECT body FROM outbox')]
            self.assertEqual({row['event_id'] for row in rows}, ids)
            self.assertEqual([row['revision'] for row in rows], [1, 1])
            self.assertEqual(outbox.counts(), {'pending': 2, 'delivered': 0})
            outbox.close()
        self.assertEqual(json.dumps(self.detections, sort_keys=True), original)

    def test_actual_capture_with_sparse_source_pts_cannot_accumulate_dwell(self):
        engine = BehaviorEngine(DEMO_POLICY)
        for t in range(0, 7001, 1000):
            self.assertEqual(engine.update(self.observation(t)), [])

    def test_explicit_missing_observation_breaks_pending_confirmation(self):
        engine = BehaviorEngine(DEMO_POLICY)
        for t in (0, 500, 1000):
            self.assertEqual(engine.update(self.observation(t)), [])
        self.assertEqual(engine.update(self.observation(1500, detections=[], status='gap')), [])
        for t in (2000, 2500, 3000, 3500):
            self.assertEqual(engine.update(self.observation(t)), [])
        events = engine.update(self.observation(4000))
        self.assertEqual(len(events), 2)
        self.assertEqual({e['start_media_ms'] for e in events}, {2000})

    def test_derived_low_confidence_head_control_is_unknown_not_safe_or_violation(self):
        engine = BehaviorEngine(DEMO_POLICY)
        for t in (0, 500, 1000):
            self.assertEqual(engine.update(self.observation(t)), [])
        modified = deepcopy(self.detections)
        for item in modified:
            if item['class_name'] == 'bare_head':
                item['score'] = 0.249
        self.assertEqual(engine.update(self.observation(1500, detections=modified, modified=True)), [])
        for t in (2000, 2500, 3000, 3500):
            self.assertEqual(engine.update(self.observation(t)), [])
        self.assertEqual(len(engine.update(self.observation(4000))), 2)

    def test_derived_missing_head_keypoints_control_keeps_strict_ownership(self):
        engine = BehaviorEngine(DEMO_POLICY)
        for t in range(0, 4501, 500):
            modified = deepcopy(self.detections)
            for item in modified:
                if item['class_name'] == 'person':
                    for point in item['keypoints'][:5]:
                        point[2] = 0.49
            self.assertEqual(engine.update(self.observation(t, detections=modified, modified=True)), [])


class SparseFallSamplingTests(unittest.TestCase):
    def test_gap_before_lying_does_not_establish_observed_fall_transition(self):
        observations, _ = build_scenario('fall_immobility')
        engine = BehaviorEngine()
        events = []
        for batch in observations[:2]:
            events.extend(engine.update(batch))
        gap = deepcopy(observations[2])
        gap.update(media_time_ms=750, frame_id=2, status='gap', detections=[])
        engine.update(gap)
        for batch in observations[2:]:
            events.extend(engine.update(batch))
        self.assertTrue(events)
        self.assertEqual({e['execution_backend'] for e in events}, {'synthetic-test'})
        self.assertEqual({e['type'] for e in events}, {'prolonged_lying'})
        self.assertEqual(events[0]['confirmed_media_ms'], 4000)


if __name__ == '__main__':
    unittest.main()
