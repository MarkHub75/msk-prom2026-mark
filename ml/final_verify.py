"""Portable final-package integrity and provenance checks (standard library only)."""
import argparse
import hashlib
import json
from pathlib import Path


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def verify(root):
    root = Path(root).resolve()
    checks = json.loads((root / 'CHECKSUMS.json').read_text())
    for rel, item in checks['files'].items():
        path = (root / rel).resolve()
        if not path.is_relative_to(root) or not path.is_file() or path.stat().st_size != item['bytes'] or sha(path) != item['sha256']:
            raise ValueError('package file differs: ' + rel)
    catalog = json.loads((root / 'VIDEO_MANIFEST.json').read_text())
    frames, calls, events = 0, 0, 0
    sources = {}
    for scene in catalog['videos']:
        directory = root / scene['path']
        meta = json.loads((directory / 'manifest.json').read_text())
        video = root / scene['playback_mp4']
        if sha(video) != scene['source_sha256'] or meta['source_sha256'] != scene['source_sha256']:
            raise ValueError('source video identity differs')
        data = json.loads((directory / 'detections.json').read_text())
        rows = data['frames']
        if len(rows) != scene['frames'] or [r['frame_index'] for r in rows] != list(range(scene['frames'])):
            raise ValueError('full frame coverage differs')
        if any(r['backend'] != scene['backend'] or len(r['models']) != 3 for r in rows):
            raise ValueError('neural origin/model census differs')
        if scene['original_mp4'] is None and video.name != 'playback.mp4':
            raise ValueError('derived media mislabelled as original')
        visual = json.loads((directory / 'render_validation.json').read_text())
        time_map = json.loads((directory / 'video_time_map.json').read_text())
        if len(time_map) != len(rows) or visual['frames'] != len(rows) or visual['tracker_carried_predictions'] != 0:
            raise ValueError('visualization frame coverage differs')
        for r, v in zip(rows, time_map):
            if r['original_pts_ms'] != v['original_pts_ms'] or r['frame_index'] != v['frame_index'] or not v['neural_output_shown'] or v['tracker_propagation']:
                raise ValueError('visualization borrowed a frame/time/observation')
        frames += len(rows)
        calls += sum(len(r['models']) for r in rows)
        predicted = json.loads((directory / 'events.json').read_text())
        events += len(predicted)
        if len(predicted) != meta['event_count']:
            raise ValueError('Argus predicted event count differs')
        sources[scene['source_sha256']] = rows
    if frames != catalog['local_frames'] or calls != catalog['local_model_calls']:
        raise ValueError('global local inference coverage differs')
    tpu_calls, tpu_sources = 0, set()
    for directory in sorted((root / 'linq_captures').iterdir()):
        capture = json.loads((directory / 'matvey_linq_frames.intermediate.json').read_text())
        source_hash = capture['source']['sha256']
        if sha(directory / 'matvey_source_original.mp4') != source_hash or source_hash not in sources:
            raise ValueError('TPU capture source differs')
        observed = {}
        for r in capture['frames']:
            local = sources[source_hash][r['frame_index']]
            if r['original_pts_ms'] != local['original_pts_ms'] or r['source_rgb_sha256'] != local['rgb_sha256']:
                raise ValueError('TPU capture borrowed another source frame')
            observed[r['frame_index']] = [m['model_id'] for m in r['models']]
            for model in r['models']:
                proof = model['execution']
                if proof['request_id'] != proof['response_id'] or proof['status_code'] != 0 or proof['journal_state'] != 'COMPLETED':
                    raise ValueError('non-correlated TPU completion')
                tpu_calls += 1
                tpu_sources.add((source_hash, r['frame_index']))
        video_map = json.loads((directory / 'matvey_video_time_map.json').read_text())
        for m in video_map:
            if m['neural_output_shown'] != (m['frame_index'] in observed) or m['tracker_propagation']:
                raise ValueError('TPU missing frame was filled/interpolated')
            if m['shown_model_ids'] != observed.get(m['frame_index'], []):
                raise ValueError('TPU visualization model origin differs')
    if tpu_calls != catalog['historical_linq_model_calls'] or len(tpu_sources) != catalog['historical_linq_unique_source_frames'] or catalog['fresh_linq_calls'] != 0:
        raise ValueError('TPU coverage incorrectly claimed')
    actual = json.loads((root / 'integration/local_argus_cpu/validation.json').read_text())
    if actual['backend'] != 'ONNXRUNTIME_CPU' or actual['fake'] or actual['tpu_calls'] or actual['external_artifacts_injected']:
        raise ValueError('actual app backend incorrectly claimed')
    if actual['events'] != len(json.loads((root / 'integration/local_argus_cpu/events.json').read_text())):
        raise ValueError('actual app events differ')
    for response in json.loads((root / 'integration/local_argus_cpu/api_readbacks.json').read_text()):
        if response['status_code'] != 200:
            raise ValueError('actual app event readback failed')
    cpu_visual = json.loads((root / 'integration/local_argus_cpu/render_validation.json').read_text())
    if len(cpu_visual['inferred_frame_indices']) != 38 or len(cpu_visual['no_inference_frame_indices']) != 37 or cpu_visual['tracker_carried_predictions']:
        raise ValueError('sampled CPU app coverage differs')
    return {'status': 'PASS_FINAL_PACKAGE_INTEGRITY', 'files': len(checks['files']),
        'full_local_scenes': len(catalog['videos']), 'full_local_frames': frames,
        'full_local_model_calls': calls, 'saved_local_replay_episodes': events,
        'actual_local_argus_events': actual['events'], 'actual_local_argus_onnx_calls': actual['model_calls'],
        'historical_tpu_calls': tpu_calls, 'historical_tpu_unique_frames': len(tpu_sources),
        'fresh_tpu_calls': 0, 'independent_industrial_quality': 'NOT_QUALIFIED',
        'live_tpu_to_argus': 'NOT_VERIFIED', 'verification_neural_calls': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    print(json.dumps(verify(args.root), indent=2))


if __name__ == '__main__':
    main()
