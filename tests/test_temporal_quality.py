"""Reference-label/timing/leakage audit fixtures, not model quality tests."""
from copy import deepcopy
from io import StringIO, BytesIO
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from ml.quality.temporal.acquire import fetch
from ml.quality.temporal.urfall import native_rows, intervals
from ml.quality.temporal.audit import audit_reference


def reference():
    return {'schema_version':'temporal-reference-v1',
            'media':[{'video_id':'clip','media_sha256':'a'*64,'media_path':'not-read',
                      'duration_ms':300,'group_id':'same-source-camera','split':'validation'}],
            'annotations':[{'video_id':'clip','intervals':[
                {'start_ms':0,'end_ms':100,'state':'unknown'},
                {'start_ms':100,'end_ms':300,'state':'not_lying'}]}],
            'production_capabilities':{'running':'NOT_IMPLEMENTED','zone_intrusion':'NOT_IMPLEMENTED'}}


class TemporalReferenceTests(unittest.TestCase):
    def test_missing_frame_labels_remain_explicit_unknown(self):
        rows=native_rows(StringIO('adl-01,2,-1\nadl-01,4,-1\n'),
                         StringIO('1,0\n2,32\n3,67\n4,100\n'),'adl-01',4)
        self.assertEqual([v['state'] for v in rows],['unknown','not_lying','unknown','not_lying'])
        for r,t in zip(rows,[0,33.333,66.667,100]):r['video_pts_ms']=t
        grouped=intervals(rows,133.333)
        self.assertEqual(len(grouped),4)
        self.assertEqual(grouped[0]['end_ms'],33.333)
        self.assertEqual(rows[1]['source_time_ms'],32)
        self.assertEqual(rows[1]['video_pts_ms'],33.333)

    def test_adl_source_class_does_not_override_positive_posture_label(self):
        rows=native_rows(StringIO('adl-10,1,0\nadl-10,2,1\n'),StringIO('1,0\n2,33\n'),'adl-10',2)
        self.assertEqual([v['state'] for v in rows],['falling_transition','lying_on_ground'])

    def test_other_sequence_labels_cannot_contaminate_reference(self):
        rows=native_rows(StringIO('fall-02,1,1\nfall-01,1,-1\n'),StringIO('1,0\n'),'fall-01',1)
        self.assertEqual(rows[0]['state'],'not_lying')

    def test_duplicate_or_invalid_author_labels_rejected(self):
        for feature in ('fall-01,1,-1\nfall-01,1,1\n','fall-01,1,4\n','fall-01,2,1\n'):
            with self.assertRaises(ValueError):native_rows(StringIO(feature),StringIO('1,0\n'),'fall-01',1)

    def test_sync_must_cover_every_frame_and_strictly_advance(self):
        for sync in ('1,0\n','1,33\n2,0\n','1,0\n1,33\n','1,0\n2,nan\n'):
            with self.assertRaises(ValueError):native_rows(StringIO(''),StringIO(sync),'fall-01',2)

    def test_unimplemented_capabilities_are_na_not_zero_accuracy(self):
        report=audit_reference(reference())
        self.assertAlmostEqual(report['unknown_rate_by_duration'],1/3)
        for direction in ('running','zone_intrusion'):
            self.assertEqual(report['capability_results'][direction]['status'],'NOT_IMPLEMENTED')
            self.assertIsNone(report['capability_results'][direction]['precision'])
            self.assertIsNone(report['capability_results'][direction]['recall'])
        self.assertEqual(report['metrics']['status'],'NOT_EVALUATED')

    def test_no_annotation_does_not_mean_negative(self):
        value=reference();value['annotations']=[]
        with self.assertRaises(ValueError):audit_reference(value)

    def test_coverage_holes_or_overlap_must_not_be_silently_scored(self):
        for start in (99,101):
            value=reference();value['annotations'][0]['intervals'][1]['start_ms']=start
            with self.assertRaises(ValueError):audit_reference(value)

    def test_source_group_cannot_cross_splits_even_with_distinct_hashes(self):
        value=reference();value['media'].append({**value['media'][0],'video_id':'other','split':'test','media_sha256':'b'*64})
        with self.assertRaises(ValueError):audit_reference(value)

    def test_exact_duplicate_cannot_cross_splits_even_with_distinct_groups(self):
        value=reference();value['media'].append({**value['media'][0],'video_id':'other','split':'test','group_id':'other'})
        with self.assertRaises(ValueError):audit_reference(value)

    def test_download_budget_rejects_advertised_oversize_before_read(self):
        class Response(BytesIO):
            headers={'Content-Length':'101'}
        with tempfile.TemporaryDirectory() as tmp, patch('ml.quality.temporal.acquire.urlopen',return_value=Response(b'x'*101)):
            target=Path(tmp)/'source.mp4'
            with self.assertRaises(ValueError):fetch('https://source.invalid/data',target,100)
            self.assertFalse(target.exists());self.assertFalse(target.with_name('source.mp4.part').exists())

    def test_truncated_download_does_not_become_valid_raw_file(self):
        class Response(BytesIO):
            headers={'Content-Length':'4'}
        with tempfile.TemporaryDirectory() as tmp, patch('ml.quality.temporal.acquire.urlopen',return_value=Response(b'ab')):
            target=Path(tmp)/'source.mp4'
            with self.assertRaises(ValueError):fetch('https://source.invalid/data',target,10)
            self.assertFalse(target.exists())


if __name__=='__main__':unittest.main()
