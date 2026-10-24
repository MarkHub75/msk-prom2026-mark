"""Compare actual saved Phone/COCO observations through an unchanged Argus.

No inference, invented objects, policy zones or GT passed to the rules. Python's
return profiler records the actual attach_objects/PhonePlugin decisions without
replacing either function. The candidate profile excludes primary phone67 under
a distinct ModelSpec, so a COCO proposal cannot be credited to the candidate.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

from ml.argus_replay import digest, snapshot_import, write_json
from ml.pipeline.video_clock import FilePTS


def compare(index, integration, registry, snapshot, output):
    snapshot_import(snapshot)
    from safewatch import config as app_config, media
    from safewatch.analysis.pipeline import analyze
    from safewatch.inference.artifacts import read_jsonl, cache_key
    from safewatch.rules.base import attach_objects
    from safewatch.rules.phone import PhonePlugin
    from safewatch.types import ModelSpec, AnalysisConfig
    import yaml
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    index = Path(index)
    entries = json.loads(index.read_text())['scenes']
    phone_meta = json.loads(Path(integration).read_text())
    specs = yaml.safe_load(Path(registry).read_text())['models']
    primary = ModelSpec.model_validate(next(m for m in specs if m['id'] == 'coco-reference-yolov8n'))
    pose = ModelSpec.model_validate(next(m for m in specs if m['id'] == 'matvey-pose-yolov8n'))
    phone = ModelSpec.model_validate(phone_meta['model_spec'])
    filtered = ModelSpec.model_validate(phone_meta['candidate_comparison_primary'])
    assert 67 in primary.classes and 67 not in filtered.classes
    assert primary.local_onnx == filtered.local_onnx and primary.version != filtered.version
    params = app_config.get_settings()
    summary = []
    for entry in entries:
        if entry['status'] != 'COMPLETE':
            raise ValueError('partial source cannot be a complete evaluation scene')
        source = Path(entry['scene_video']['path'])
        if digest(source) != entry['scene_video']['sha256']:
            raise ValueError('scene bytes changed')
        clock = FilePTS(source)
        if len(clock.times) != entry['frames']:
            raise ValueError('scene clock census differs')
        probe = media.probe_video(source)
        assert probe is not None
        records = {}
        for m in entry['models']:
            f = m['argus_jsonl']
            if digest(f['path']) != f['sha256']:
                raise ValueError('pinned GPU JSONL changed')
            frames = read_jsonl(Path(f['path']), entry['frames'])
            if [f.frame_idx for f in frames] != list(range(entry['frames'])):
                raise ValueError('missing/duplicate neural frame')
            if any(abs(f.ts_ms - clock.at(f.frame_idx)) > .002 for f in frames):
                raise ValueError('GPU JSONL scene encoded PTS differ')
            records[m['role']] = frames
        det_no_phone = [f.model_copy(update={'detections': [d for d in f.detections if d.cls != 67]})
                        for f in records['detector']]
        end = round(clock.times[-1] + clock.times[-1] - clock.times[-2])
        scene_summary = {'scene_id': entry['scene_id'], 'source_sha256': entry['scene_video']['sha256'],
                         'frames': entry['frames'], 'profiles': {}, 'target_event_metrics': 'NOT_MEASURED'}
        for profile, detector, model, extra in [
            ('baseline_coco', records['detector'], primary, []),
            ('candidate_phone', det_no_phone, filtered, [(phone, records['extra'])])]:
            target = output / entry['scene_id'] / profile
            target.mkdir(parents=True)
            traces = {}
            def capture(frame, event, value):
                if event != 'return':
                    return
                if frame.f_code is attach_objects.__code__ and frame.f_locals.get('name') == 'cell phone':
                    ctx = frame.f_locals['ctx']
                    traces.setdefault(ctx.frame_idx, {}).update(
                        frame_idx=ctx.frame_idx, ts_ms=ctx.ts_ms,
                        persons=[p.model_dump(mode='json') for p in ctx.persons],
                        phone_objects=[o.model_dump(mode='json') for o in ctx.objects if o.name == 'cell phone'],
                        attachments={str(k): v if isinstance(v, str) else v.model_dump(mode='json')
                                     for k, v in value.items()})
                elif frame.f_code is PhonePlugin.observe.__code__:
                    ctx = frame.f_locals['ctx']
                    traces.setdefault(ctx.frame_idx, {}).update(
                        observations=[o.model_dump(mode='json') for o in value],
                        effective_params=frame.f_locals['params'])
            active = sorted(set(model.classes.values()) | {v for m, _ in extra for v in m.classes.values()})
            config = AnalysisConfig(width=probe.width, height=probe.height, fps=probe.fps, step=1,
                duration_ms=end, calibration=None, zones=[], rules={},
                class_conf=params.class_conf, active_classes=active)
            previous = sys.getprofile()
            try:
                sys.setprofile(capture)
                result = analyze(detector, records['pose'], source, config, pose, model, extra)
            finally:
                sys.setprofile(previous)
            write_json(target / 'analysis.json', result.model_dump(mode='json'))
            write_json(target / 'events.json', [e.model_dump(mode='json') for e in result.episodes])
            write_json(target / 'models.json', {'detector': model.model_dump(mode='json'),
                'pose': pose.model_dump(mode='json'), 'extra': [m.model_dump(mode='json') for m, _ in extra]})
            write_json(target / 'analysis_config.json', config.model_dump(mode='json'))
            with (target / 'phone_association.jsonl').open('x') as f:
                for idx in sorted(traces):
                    f.write(json.dumps(traces[idx], ensure_ascii=False, allow_nan=False) + '\n')
            states = Counter(o['state'] for t in traces.values() for o in t.get('observations', []))
            reasons = Counter(o['reason_code'] for t in traces.values() for o in t.get('observations', []) if o['reason_code'])
            phone_events = [e for e in result.episodes if e.scenario == 'phone']
            review = {'phone_object_frames_after_rule_confidence': sum(bool(t.get('phone_objects')) for t in traces.values()),
                'positive_phone_observation_frames': sum(any(o['state'] == 'P' for o in t.get('observations', [])) for t in traces.values()),
                'observation_trace_stage': 'actual plugin returns before observability suppression',
                'positive_phone_HUD_frames_after_observability': sum(any(
                    tag.code == 'phone' for obj in f.objects for tag in obj.tags) for f in result.hud),
                'person_phone_states': dict(states), 'reason_counts': dict(reasons),
                'phone_episodes': len(phone_events), 'all_episodes': len(result.episodes),
                'GT_events': None, 'FP': None, 'FN': None, 'event_F1': 'NOT_MEASURED',
                'no_GT_or_manual_detections_injected': True, 'new_NN_calls': 0, 'new_TPU_calls': 0}
            write_json(target / 'association_summary.json', review)
            scene_summary['profiles'][profile] = review
        old_key = cache_key(entry['scene_video']['sha256'], primary, 1, 'local', False)
        new_key = cache_key(entry['scene_video']['sha256'], filtered, 1, 'local', False)
        if old_key == new_key:
            raise ValueError('isolated candidate primary reused baseline cache')
        scene_summary['filtered_primary_has_distinct_cache'] = True
        summary.append(scene_summary)
    report = {'status': 'PASS_UNMODIFIED_ARGUS_PAIRED_PHONE_ASSOCIATION', 'scenes': summary,
        'input_index': {'path': str(index), 'sha256': digest(index)}, 'source_main':
        json.loads((Path(snapshot) / 'MATVEY_SNAPSHOT.json').read_text())['source_commit'],
        'new_NN_calls': 0, 'new_TPU_calls': 0, 'rules_source_changed': False,
        'rule_trace_method': 'read-only Python return profiler, original functions execute normally',
        'event_quality': 'NOT_MEASURED_NO_EXHAUSTIVE_TARGET_EVENT_GT'}
    write_json(output / 'SUMMARY.json', report)
    print(json.dumps({'status': report['status'], 'scenes': [s['scene_id'] for s in summary],
        'phone_episodes': {p: sum(s['profiles'][p]['phone_episodes'] for s in summary)
                           for p in ['baseline_coco', 'candidate_phone']}}))
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--index', type=Path, required=True)
    p.add_argument('--integration', type=Path, required=True)
    p.add_argument('--registry', type=Path, required=True)
    p.add_argument('--argus-snapshot', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    compare(a.index, a.integration, a.registry, a.argus_snapshot, a.output)


if __name__ == '__main__':
    main()
