import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from ml.linq.calibration_frames import CLIPS, COMPONENT, prepare_frames
from ml.linq.compile import sha256


class CalibrationFramesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in CLIPS: (self.root / name).write_bytes(name.encode())
        self.model = self.root / 'model.json'
        self.model.write_text(json.dumps({'input': {'name': 'images', 'shape': [1, 3, 2, 2],
            'layout': 'NCHW', 'dtype': 'float32', 'scale': 1/255}, 'padding_value': 114}))
        self.reserved = self.root / 'reserved.json'
        self.reservations = {'reserved_dataset_families': ['construction-ppe', 'urfall', 'sfchd', 'sh17'],
                             'reserved_groups': ['urfall-whole-family'], 'reserved_source_sha256': []}

    def run_prepare(self):
        self.reserved.write_text(json.dumps(self.reservations))
        return prepare_frames(self.root, self.model, self.reserved, self.root / 'output')

    @patch('ml.linq.calibration_frames.subprocess.run')
    def test_exact_eight_midpoints_and_conservative_group(self, run):
        def external(args, **kwargs):
            if args[0] == 'ffprobe':
                data = json.dumps({'streams': [{'width': 2, 'height': 2,
                                    'nb_frames': '7', 'avg_frame_rate': '25/1'}]}).encode()
            else:
                self.assertIn('select=eq(n\\,3)', args)
                data = np.arange(12, dtype=np.uint8).tobytes()
            return subprocess.CompletedProcess(args, 0, stdout=data)
        run.side_effect = external
        report = self.run_prepare()
        self.assertEqual(run.call_count, 16)
        self.assertEqual(len(report['samples']), 8)
        self.assertEqual({x['source_group'] for x in report['samples']}, {COMPONENT})
        self.assertTrue(all(x['source_frame_index'] == 3 for x in report['samples']))
        self.assertEqual(report['evaluation'], 'NOT_RUN')
        with np.load(self.root / 'output' / '4_tr6-input.npz', allow_pickle=False) as data:
            self.assertEqual(data['images'].shape, (1, 3, 2, 2))

    @patch('ml.linq.calibration_frames.subprocess.run')
    def test_reserved_source_rejected_before_decode_or_output(self, run):
        self.reservations['reserved_source_sha256'] = [sha256(self.root / CLIPS[0])]
        with self.assertRaises(ValueError): self.run_prepare()
        run.assert_not_called()
        self.assertFalse((self.root / 'output').exists())

    @patch('ml.linq.calibration_frames.subprocess.run')
    def test_missing_reserved_family_rejected(self, run):
        self.reservations['reserved_dataset_families'].remove('sh17')
        with self.assertRaises(ValueError): self.run_prepare()
        run.assert_not_called()


if __name__ == '__main__': unittest.main()
