import csv
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from ml.linq.compile import sha256
from ml.linq.quantized_video import pin_selection, verify_decoders, decoder_command


class FrozenSelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.reference, self.manifest = self.root/'reference.json', self.root/'manifest.json'
        self.manifest.write_text(json.dumps({'decoder': 'split_pose_v8',
                                           'artifacts': {'onnx': {'sha256': 'a'*64}}}))
        for name in ['quantized.qm.onnx', 'scales.json', 'optimized.onnx']:
            (self.root/name).write_text('fixture')
        (self.root/'compile-report.json').write_text(json.dumps({'compile_status': 'PASS', 'source_onnx_sha256': 'a'*64}))
        self.media = []
        for i in range(20):
            video, annotation = self.root/f'{i}.mp4', self.root/f'{i}.csv'
            video.write_bytes(b'not-decoded-in-unit-test')
            with annotation.open('w') as file:
                writer = csv.DictWriter(file, fieldnames=['source_frame_id','video_pts_ms','state'])
                writer.writeheader()
                for frame in range(30): writer.writerow({'source_frame_id':frame+1,'video_pts_ms':frame*1000/30,'state':'unknown'})
            self.media.append({'video_id':str(i),'split':'validation','fps':30,'frame_count':30,
                'duration_ms':1000,'media_path':str(video),'media_sha256':sha256(video),
                'annotation_path':str(annotation),'annotation_sha256':sha256(annotation),
                'width':2,'height':2,'group_id':'conservative-source'})

    def selection(self):
        self.reference.write_text(json.dumps({'media':self.media}))
        return pin_selection(self.reference,self.manifest,self.root)

    def test_zero_based_stride_and_native_pts_frozen(self):
        reference, manifest, selection = self.selection()
        self.assertEqual(selection['selected_frame_count'],40)
        frames = selection['videos'][0]['selected_frames']
        self.assertEqual([x['source_frame_index'] for x in frames],[0,15])
        self.assertEqual([float(x['video_pts_ms']) for x in frames],[0,500])
        self.assertEqual([int(x['source_frame_id']) for x in frames],[1,16])

    def test_holdout_and_source_drift_rejected(self):
        self.media[0]['split']='test'
        with self.assertRaises(ValueError): self.selection()
        self.media[0]['split']='validation';self.media[0]['media_sha256']='0'*64
        with self.assertRaises(ValueError): self.selection()

    @patch('ml.linq.quantized_video.subprocess.run')
    def test_decoder_duplication_rejected_before_neural_inference(self, execute):
        reference, _, selection = self.selection()
        execute.return_value = subprocess.CompletedProcess([],0,stdout=bytes(12*3))
        with self.assertRaises(ValueError): verify_decoders(reference,selection)
        self.assertNotIn('decoder_check',selection)
        command=decoder_command(self.media[0])
        self.assertEqual(command[command.index('-fps_mode')+1],'passthrough')

    @patch('ml.linq.quantized_video.subprocess.run')
    def test_all_selected_rgb_hashes_pinned(self, execute):
        reference, _, selection=self.selection()
        execute.return_value=subprocess.CompletedProcess([],0,stdout=bytes(24))
        verify_decoders(reference,selection)
        self.assertEqual(execute.call_count,20)
        self.assertTrue(all(len(f['decoded_rgb_sha256'])==64 for v in selection['videos'] for f in v['selected_frames']))


if __name__=='__main__': unittest.main()
