import copy
import json
from pathlib import Path
import tempfile
import unittest

from ml.quality.handoff import HandoffError, sha256
from ml.quality.weak_video_intake import TASK, load_weak_video_ready, review_rejected_training


class WeakVideoIntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.release = self.root / 'release'
        self.release.mkdir()
        self.rows = []
        for role, group, category, class_id in [('train', 'a', 'ADL', 0), ('val', 'b', 'Fall', 1)]:
            media = self.release / (role + '.mp4')
            media.write_bytes(role.encode())
            clock = self.release / (role + '-clock.jsonl')
            row = {'source_id': role, 'source_group': group, 'split': role,
                   'source_class': category, 'class_id': class_id, 'path': str(media),
                   'relative_path': media.name, 'sha256': sha256(media), 'bytes': media.stat().st_size,
                   'label_scope': 'WHOLE_VIDEO_WEAK_CATEGORY', 'label_provenance': 'SOURCE_ANNOTATION',
                   'frame_event_GT': None, 'bbox_GT': None, 'native_frames': 1,
                   'clock_relative_path': clock.name}
            self.write(clock, {'source_id': role, 'source_sha256': row['sha256'],
                               'source_subject_group': group, 'frame_index0': 0,
                               'container_pts_ms': 39.028, 'source_RGB_sha256': sha256(media),
                               'frame_event_label': None})
            row['clock_sha256'] = sha256(clock)
            self.write(self.release / (role + '.jsonl'), row)
            self.rows.append(row)
        self.counts = {'train': {'ADL': 1}, 'val': {'Fall': 1}}
        self.entry = {'dataset_id': 'fixture', 'version': 'v1', 'status': 'READY_FOR_TRAIN',
                      'task': TASK, 'label_unit': 'ENTIRE_ORIGINAL_VIDEO_WEAK_CATEGORY',
                      'absolute_path': str(self.release), 'forbid_frame_label_broadcast': True,
                      'bbox_training_supported': False, 'independent_test': False,
                      'test_status': 'EMPTY_BLOCKED_NO_INDEPENDENT_TEST',
                      'do_not_retrain_existing_four_heads': True, 'license': 'TEST_ONLY',
                      'known_limitations': ['synthetic labels; no quality evidence'],
                      'classes': {'0': 'ADL', '1': 'Fall'}, 'counts': self.counts}
        self.manifest = copy.deepcopy(self.entry)
        self.manifest['assets'] = self.rows
        self.write(self.release / 'class_map.json', {'task': TASK, 'classes': self.entry['classes'],
                   'requires_video_bag_loss': True, 'forbid_frame_label_broadcast': True,
                   'bbox_training_supported': False})
        self.write(self.release / 'split_manifest.json', {'train_groups': ['a'], 'val_groups': ['b'],
                   'test_groups': [], 'independent_test': False, 'counts': self.counts})
        (self.release / 'test.jsonl').write_text('')
        (self.release / 'ATTRIBUTION.md').write_text('Synthetic fixture')
        self.pointer = self.root / 'READY.json'
        self.seal()

    @staticmethod
    def write(path, value):
        path.write_text(json.dumps(value) + '\n')

    def seal(self):
        self.write(self.release / 'manifest.json', self.manifest)
        self.write(self.release / 'VALIDATION.json', {'status': 'PASS',
                   'manifest_sha256': sha256(self.release / 'manifest.json')})
        for path_key, sha_key, name in [('manifest_path', 'manifest_sha256', 'manifest.json'),
             ('validation_path', 'validation_sha256', 'VALIDATION.json'),
             ('train_path', 'train_sha256', 'train.jsonl'), ('val_path', 'val_sha256', 'val.jsonl'),
             ('class_map', 'class_map_sha256', 'class_map.json')]:
            self.entry[path_key], self.entry[sha_key] = str(self.release / name), sha256(self.release / name)
        self.entry['split_manifest'] = str(self.release / 'split_manifest.json')
        self.entry['test_path'] = str(self.release / 'test.jsonl')
        registry = {p.name: sha256(p) for p in self.release.iterdir() if p.name != 'CHECKSUMS.json'}
        self.write(self.release / 'CHECKSUMS.json', registry)
        self.write(self.pointer, {'schema_version': 'mosprom-training-datasets-v1', 'datasets': [self.entry]})

    def review(self, **changes):
        args = dict(expected_pointer_sha256=sha256(self.pointer),
                    checksums_sha256=sha256(self.release / 'CHECKSUMS.json'),
                    dataset_id='fixture', allowed_use=TASK, releases_root=self.root)
        args.update(changes)
        return load_weak_video_ready(self.pointer, **args)

    def test_whole_video_intake_preserves_blocked_quality(self):
        result = self.review()
        self.assertEqual(result['verified_media'], 2)
        self.assertEqual(result['verified_clock_rows'], 2)
        self.assertFalse(result['automatic_training'])
        self.assertEqual(result['independent_test'], 'BLOCKED_EMPTY')

    def test_event_or_bbox_use_rejected_before_consumption(self):
        for use in ('event_quality', 'bbox_training', 'independent_test'):
            with self.subTest(use=use), self.assertRaisesRegex(HandoffError, 'requested use'):
                self.review(allowed_use=use)

    def test_pinned_pointer_and_registry_are_both_required(self):
        for arg in ('expected_pointer_sha256', 'checksums_sha256'):
            with self.subTest(arg=arg), self.assertRaisesRegex(HandoffError, 'SHA256 changed'):
                self.review(**{arg: '0' * 64})

    def test_changed_media_rejected(self):
        (self.release / 'train.mp4').write_bytes(b'mutation')
        with self.assertRaisesRegex(HandoffError, 'SHA256 changed'):
            self.review()

    def test_wrong_clock_source_rejected_even_with_new_valid_hashes(self):
        clock = self.release / 'val-clock.jsonl'
        frame = json.loads(clock.read_text())
        frame['source_id'] = 'different source'
        self.write(clock, frame)
        self.rows[1]['clock_sha256'] = sha256(clock)
        self.write(self.release / 'val.jsonl', self.rows[1])
        self.seal()
        with self.assertRaisesRegex(HandoffError, 'clock/source'):
            self.review()

    def test_rgb_duplicate_between_groups_rejected(self):
        clock = self.release / 'val-clock.jsonl'
        frame = json.loads(clock.read_text())
        frame['source_RGB_sha256'] = self.rows[0]['sha256']
        self.write(clock, frame)
        self.rows[1]['clock_sha256'] = sha256(clock)
        self.write(self.release / 'val.jsonl', self.rows[1])
        self.seal()
        with self.assertRaisesRegex(HandoffError, 'RGB leaks'):
            self.review()

    def test_empty_test_cannot_be_replaced_with_evaluation_rows(self):
        (self.release / 'test.jsonl').write_text('{}\n')
        self.seal()
        with self.assertRaisesRegex(HandoffError, 'test must remain empty'):
            self.review()

    def test_pinned_manifest_must_match_split_rows(self):
        self.manifest['assets'] = list(reversed(self.rows))
        self.seal()
        with self.assertRaisesRegex(HandoffError, 'row census'):
            self.review()

    def test_symlink_cannot_replace_pinned_media(self):
        media = self.release / 'train.mp4'
        original = self.root / 'other.mp4'
        original.write_bytes(media.read_bytes())
        media.unlink()
        media.symlink_to(original)
        with self.assertRaisesRegex(HandoffError, 'noncanonical'):
            self.review()

    def test_positive_training_not_admitted_as_rejected(self):
        path = self.root / 'training.json'
        self.write(path, {'schema': 'matvey-training-result-handoff-v1', 'status': 'IMPROVED'})
        with self.assertRaisesRegex(HandoffError, 'rejected-training'):
            review_rejected_training(path, expected_sha256=sha256(path), approved_root=self.root)

    def training_fixture(self, gain=0):
        def spec(path):
            return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha256(path)}
        checkpoint = self.root / 'checkpoint.bin'
        checkpoint.write_bytes(b'not deserialized')
        result = {'decision': 'REJECT_KEEP_BASELINE', 'improved': False,
                  'deployment_allowed': False, 'export_or_linq_executed': False,
                  'baseline': {'macro_f1': .5}, 'candidate': {'macro_f1': .5},
                  'macro_f1_gain': gain, 'best': spec(checkpoint), 'last': spec(checkpoint),
                  'baseline_checkpoint': spec(checkpoint), 'scope': 'synthetic weak video',
                  'independent_event_quality': 'NOT_EVALUATED'}
        result_path = self.root / 'result.json'
        self.write(result_path, result)
        path = self.root / 'training.json'
        self.write(path, {'schema': 'matvey-training-result-handoff-v1',
                         'status': 'COMPLETED_TRAINED_CANDIDATE_REJECTED',
                         'source_training_commit': 'fixture', 'validation_macro_f1_gain': gain,
                         'actual_training_result': spec(result_path),
                         'best': spec(checkpoint), 'last': spec(checkpoint), 'baseline_kept': spec(checkpoint)})
        return path

    def test_rejected_candidate_is_received_without_loading_weights(self):
        path = self.training_fixture()
        report = review_rejected_training(path, expected_sha256=sha256(path), approved_root=self.root)
        self.assertFalse(report['deployment_allowed'])
        self.assertEqual(report['gain'], 0)

    def test_rejected_candidate_cannot_claim_inconsistent_gain(self):
        path = self.training_fixture(gain=.1)
        with self.assertRaisesRegex(HandoffError, 'paired gain mismatch'):
            review_rejected_training(path, expected_sha256=sha256(path), approved_root=self.root)
