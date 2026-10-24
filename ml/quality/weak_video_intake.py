"""Read-only intake of the reviewed weak-video handoff; never starts a job.

This schema grants whole-video development classification only. It cannot grant
frame labels, event GT, a new held-out test, or production model selection.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path

from ml.quality.handoff import HandoffError, sha256


TASK = 'VIDEO_WEAK_LABEL_CLASSIFICATION'


def require(condition, message):
    if not condition:
        raise HandoffError(message)


def checked(path, expected, root, size=None):
    path, root = Path(path), Path(root).resolve()
    require(path.is_absolute() and path.absolute() == path.resolve()
            and path.is_file() and path.resolve().is_relative_to(root),
            'noncanonical or out-of-scope artifact path')
    require(isinstance(expected, str) and len(expected) == 64
            and all(c in '0123456789abcdef' for c in expected), 'exact SHA256 required')
    before = path.stat()
    require(size is None or (type(size) is int and before.st_size == size), 'byte count changed')
    require(sha256(path) == expected, 'artifact SHA256 changed')
    after = path.stat()
    require((before.st_ino, before.st_size, before.st_mtime_ns)
            == (after.st_ino, after.st_size, after.st_mtime_ns), 'artifact changed during intake')
    return path


def read_json(path):
    return json.loads(Path(path).read_text())


def load_weak_video_ready(pointer, *, expected_pointer_sha256, checksums_sha256,
                         dataset_id, allowed_use,
                         releases_root='/workspace/datasets/research/releases'):
    """Verify pinned metadata, all copied media and clocks without decoding.

    CHECKSUMS has no digest in the producer pointer; its independently reviewed
    digest is mandatory. Do not derive that trust anchor from the file itself.
    """
    require(allowed_use == TASK, 'weak video labels do not approve requested use')
    pointer = Path(pointer)
    checked(pointer, expected_pointer_sha256, pointer.parent)
    catalog = read_json(pointer)
    require(catalog.get('schema_version') == 'mosprom-training-datasets-v1',
            'unsupported weak-video handoff schema')
    entries = [d for d in catalog.get('datasets', []) if d.get('dataset_id') == dataset_id]
    require(len(entries) == 1, 'unique dataset entry required')
    entry = entries[0]
    require(entry.get('status') == 'READY_FOR_TRAIN' and entry.get('task') == TASK
            and entry.get('label_unit') == 'ENTIRE_ORIGINAL_VIDEO_WEAK_CATEGORY',
            'whole-video weak-label capability required')
    require(entry.get('forbid_frame_label_broadcast') is True
            and entry.get('bbox_training_supported') is False
            and entry.get('independent_test') is False
            and entry.get('test_status') == 'EMPTY_BLOCKED_NO_INDEPENDENT_TEST'
            and entry.get('do_not_retrain_existing_four_heads') is True,
            'reviewed weak-label restrictions changed')
    require(bool(entry.get('license')) and bool(entry.get('known_limitations')),
            'rights and limitations required')
    root = Path(entry['absolute_path'])
    require(root.is_absolute() and root == root.resolve()
            and root.is_relative_to(Path(releases_root).resolve()), 'unapproved release root')
    checksums_path = checked(root / 'CHECKSUMS.json', checksums_sha256, root)
    checksums = read_json(checksums_path)
    require(isinstance(checksums, dict) and checksums, 'checksums registry required')
    for relative, expected in checksums.items():
        require(not Path(relative).is_absolute() and '..' not in Path(relative).parts,
                'unsafe checksum relative path')
        checked(root / relative, expected, root)
    for path_key, sha_key, name in [
        ('manifest_path', 'manifest_sha256', 'manifest.json'),
        ('validation_path', 'validation_sha256', 'VALIDATION.json'),
        ('train_path', 'train_sha256', 'train.jsonl'),
        ('val_path', 'val_sha256', 'val.jsonl'),
        ('class_map', 'class_map_sha256', 'class_map.json'),
    ]:
        require(entry.get(path_key) == str(root / name)
                and entry.get(sha_key) == checksums.get(name), 'pointer/registry binding mismatch')
    for key, name in [('split_manifest', 'split_manifest.json'), ('test_path', 'test.jsonl')]:
        require(entry.get(key) == str(root / name) and name in checksums,
                'split/test metadata must be pinned')
    require('ATTRIBUTION.md' in checksums, 'pinned attribution required')
    manifest, split = read_json(root / 'manifest.json'), read_json(root / 'split_manifest.json')
    classes, validation = read_json(root / 'class_map.json'), read_json(root / 'VALIDATION.json')
    for key in ('dataset_id', 'version', 'status', 'task', 'absolute_path', 'counts',
                'forbid_frame_label_broadcast', 'do_not_retrain_existing_four_heads', 'independent_test'):
        require(manifest.get(key) == entry.get(key), 'manifest identity/scope mismatch')
    require(classes.get('task') == TASK and classes.get('classes') == entry.get('classes')
            and classes.get('requires_video_bag_loss') is True
            and classes.get('forbid_frame_label_broadcast') is True
            and classes.get('bbox_training_supported') is False, 'class-map scope mismatch')
    require(validation.get('status') == 'PASS'
            and validation.get('manifest_sha256') == entry['manifest_sha256'],
            'producer validation binding mismatch')
    require(not (root / 'test.jsonl').read_text().strip() and split.get('test_groups') == []
            and split.get('independent_test') is False, 'test must remain empty and blocked')
    seen_ids, seen_media, seen_paths, groups, rgb_groups = set(), {}, set(), {}, {}
    counts, native_frames, media_bytes = {}, 0, 0
    rows_all = []
    for role in ('train', 'val'):
        rows = [json.loads(line) for line in (root / (role + '.jsonl')).read_text().splitlines() if line.strip()]
        counts[role] = dict(Counter(row['source_class'] for row in rows))
        declared_groups = split.get(role + '_groups', [])
        for row in rows:
            sid, group = row['source_id'], row['source_group']
            require(sid not in seen_ids and row.get('split') == role, 'duplicate ID or incorrect split')
            require(group in declared_groups and groups.get(group, role) == role, 'source group leaks across splits')
            require(seen_media.get(row['sha256'], role) == role, 'exact media leaks across splits')
            require(row.get('label_scope') == 'WHOLE_VIDEO_WEAK_CATEGORY'
                    and row.get('label_provenance') == 'SOURCE_ANNOTATION'
                    and row.get('frame_event_GT') is None and row.get('bbox_GT') is None
                    and type(row.get('class_id')) is int
                    and entry['classes'].get(str(row['class_id'])) == row['source_class'],
                    'row label scope or class mismatch')
            media = root / row['relative_path']
            require(row['path'] == str(media) and str(media) not in seen_paths, 'duplicate or mismatched media path')
            require(checksums.get(row['relative_path']) == row['sha256'], 'media not pinned in registry')
            checked(media, row['sha256'], root, row['bytes'])
            clock_name = row['clock_relative_path']
            require(checksums.get(clock_name) == row['clock_sha256'], 'clock not pinned in registry')
            clock = checked(root / clock_name, row['clock_sha256'], root)
            previous_pts, clock_count = None, 0
            for index, line in enumerate(clock.read_text().splitlines()):
                frame = json.loads(line)
                pts = frame.get('container_pts_ms')
                require(frame.get('source_id') == sid and frame.get('source_sha256') == row['sha256']
                        and frame.get('source_subject_group') == group
                        and type(frame.get('frame_index0')) is int and frame['frame_index0'] == index
                        and type(pts) in (int, float) and math.isfinite(pts)
                        and (previous_pts is None or pts > previous_pts)
                        and frame.get('frame_event_label') is None, 'clock/source/ordinal binding mismatch')
                rgb = frame.get('source_RGB_sha256')
                require(isinstance(rgb, str) and len(rgb) == 64, 'native RGB digest required')
                require(rgb_groups.get(rgb, role) == role, 'exact native RGB leaks across splits')
                rgb_groups[rgb], previous_pts, clock_count = role, pts, index + 1
            require(type(row.get('native_frames')) is int and clock_count == row['native_frames']
                    and clock_count > 0, 'native frame census mismatch')
            seen_ids.add(sid)
            seen_paths.add(str(media))
            seen_media[row['sha256']], groups[group] = role, role
            native_frames += clock_count
            media_bytes += row['bytes']
        rows_all.extend(rows)
    require(counts == entry['counts'] == split.get('counts'), 'split category counts mismatch')
    require(manifest.get('assets') == rows_all, 'manifest/split row census mismatch')
    require(set(groups) == set(split.get('train_groups', []) + split.get('val_groups', [])),
            'declared groups do not match rows')
    return {'status': 'VERIFIED_WEAK_VIDEO_DEVELOPMENT_ONLY', 'dataset_id': dataset_id,
            'version': entry['version'], 'pointer_sha256': expected_pointer_sha256,
            'manifest_sha256': entry['manifest_sha256'], 'checksums_sha256': checksums_sha256,
            'counts': counts, 'verified_media': len(rows_all), 'media_bytes': media_bytes,
            'verified_clock_rows': native_frames, 'verified_registry_files': len(checksums),
            'groups': groups, 'exact_media_crosssplit': 0, 'exact_native_rgb_crosssplit': 0,
            'rgb_verification_scope': 'digest equality from pinned source clocks; no fresh RGB decode',
            'near_duplicates': {'producer_candidates': split.get('phash_crosssubject_candidates'),
                                'independently_recomputed': False, 'physical_identity': 'UNKNOWN'},
            'allowed_use': allowed_use, 'license': entry['license'],
            'limitations': entry['known_limitations'], 'frame_event_gt': 'UNAVAILABLE',
            'bbox_training': 'FORBIDDEN', 'independent_test': 'BLOCKED_EMPTY',
            'existing_four_head_retraining': 'FORBIDDEN', 'automatic_training': False,
            'new_neural_calls': 0, 'new_remote_calls': 0}


def review_rejected_training(path, *, expected_sha256, approved_root='/workspace'):
    """Receive the pinned negative experiment without loading a checkpoint.

    Mutable producer-worktree files are deliberately outside this receipt.
    No unreviewed positive result is promoted through this negative-result path.
    """
    path = checked(path, expected_sha256, approved_root)
    handoff = read_json(path)
    require(handoff.get('schema') == 'matvey-training-result-handoff-v1'
            and handoff.get('status') == 'COMPLETED_TRAINED_CANDIDATE_REJECTED',
            'only reviewed rejected-training schema supported')
    for key in ('actual_training_result', 'best', 'last', 'baseline_kept'):
        spec = handoff[key]
        checked(spec['path'], spec['sha256'], approved_root, spec['bytes'])
    result = read_json(handoff['actual_training_result']['path'])
    require(result.get('decision') == 'REJECT_KEEP_BASELINE' and result.get('improved') is False
            and result.get('deployment_allowed') is False and result.get('export_or_linq_executed') is False,
            'negative experiment decision changed')
    before, after = result['baseline']['macro_f1'], result['candidate']['macro_f1']
    require(all(type(v) in (int, float) and math.isfinite(v) for v in (before, after)),
            'finite paired metrics required')
    gain = after - before
    require(math.isclose(gain, result['macro_f1_gain'], abs_tol=1e-12)
            and math.isclose(gain, handoff['validation_macro_f1_gain'], abs_tol=1e-12)
            and gain <= 0, 'rejected paired gain mismatch')
    for key, result_key in [('best', 'best'), ('last', 'last'), ('baseline_kept', 'baseline_checkpoint')]:
        require(handoff[key] == result[result_key], 'checkpoint lineage mismatch')
    return {'status': 'REJECT_KEEP_BASELINE', 'handoff_sha256': expected_sha256,
            'source_training_commit': handoff['source_training_commit'],
            'baseline_macro_f1': before, 'candidate_macro_f1': after, 'gain': gain,
            'label_unit': 'WHOLE_VIDEO_WEAK_CATEGORY',
            'metric_evidence': 'PRODUCER_REPORTED_PAIRED_VALIDATION_NOT_RECOMPUTED',
            'scope': result['scope'], 'deployment_allowed': False,
            'independent_event_quality': result['independent_event_quality'],
            'checkpoints': {k: handoff[k] for k in ('best', 'last', 'baseline_kept')},
            'mutable_producer_worktree_files': 'NOT_CONSUMED',
            'new_neural_calls': 0, 'new_remote_calls': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pointer', required=True)
    parser.add_argument('--pointer-sha256', required=True)
    parser.add_argument('--checksums-sha256', required=True)
    parser.add_argument('--dataset-id', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    require(output.resolve().is_relative_to(Path('/workspace/artifacts')), 'output must be outside Git in artifacts')
    require(not output.exists(), 'existing evidence must not be overwritten')
    report = load_weak_video_ready(args.pointer, expected_pointer_sha256=args.pointer_sha256,
                                  checksums_sha256=args.checksums_sha256,
                                  dataset_id=args.dataset_id, allowed_use=TASK)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x') as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({key: report[key] for key in ('status', 'verified_media', 'verified_clock_rows', 'automatic_training')}))


if __name__ == '__main__':
    main()
