"""Render saved observations only; no model calls or tracker propagation.

Every input frame is shown once. Original encoded PTS remain in JSON and HUD;
the H264 presentation timeline is normalized to zero and quantized to 1 ms.
Missing TPU frames have no boxes, including between genuine captured frames.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from ml.argus_replay import digest, write_json
from ml.pipeline.video_clock import FilePTS


SKELETON = [(5, 6), (5, 7), (7, 9), (6, 8), (8, 10), (5, 11),
            (6, 12), (11, 12), (11, 13), (13, 15), (12, 14), (14, 16)]
DISPLAY_CLASSES = {'person', 'car', 'bus', 'train', 'truck', 'cell phone',
                   'helmet', 'no_helmet', 'fire', 'smoke', 'cigarette'}


def visible_events(events, pts):
    # No future confirmation is displayed on an earlier frame.
    return [e for e in events if e['confirm_ms'] <= pts < e['end_ms']]


def render(scene, output, replay=None, historical=None, local_app=None):
    import cv2
    import numpy as np
    cv2.setNumThreads(1)
    scene, output = Path(scene), Path(output)
    meta = json.loads((scene / 'matvey_scene.json').read_text())
    source = scene / 'matvey_source_original.mp4'
    if digest(source) != meta['source_sha256']:
        raise ValueError('source video bytes differ')
    rows = [json.loads(x) for x in (scene / 'matvey_detections.jsonl').read_text().splitlines()]
    clock = FilePTS(source)
    if len(rows) != len(clock.times):
        raise ValueError('source frame census differs')
    captured = None
    if historical:
        capture = json.loads((Path(historical) / 'matvey_linq_frames.intermediate.json').read_text())
        if capture['source']['sha256'] != meta['source_sha256']:
            raise ValueError('TPU capture belongs to another video')
        captured = {r['frame_index']: r for r in capture['frames']}
    local_frames = None
    if local_app:
        if replay or historical:
            raise ValueError('actual local app visualization must use its own results only')
        app = Path(local_app)
        validation = json.loads((app / 'validation.json').read_text())
        if validation['source_sha256'] != meta['source_sha256'] or validation['fake'] or validation['tpu_calls']:
            raise ValueError('local app execution/source identity differs')
        registry = json.loads((app.parent / 'models/MODEL_REGISTRY.json').read_text())['models']
        local_frames = {}
        for item in json.loads((app / 'artifacts.json').read_text()):
            spec = next(m['model'] for m in registry if m['model']['id'] == item['model_id'])
            artifact = app / item['file']
            if digest(artifact) != item['sha256']:
                raise ValueError('actual app artifact changed')
            for r in (json.loads(x) for x in artifact.read_text().splitlines()):
                i = r['frame_idx']
                if abs(r['ts_ms'] - clock.at(i)) > .051:
                    raise ValueError('actual app PTS differs')
                models = local_frames.setdefault(i, {'models': []})['models']
                models.append({'model_id': item['model_id'], 'detections': [
                    {'class_name': spec['classes'][str(d['cls'])], 'confidence': d['score'],
                     'bbox_xyxy': d['bbox_xyxy'], 'pose_coco17': d.get('kpts')} for d in r['detections']]})
        events = json.loads((app / 'episodes.json').read_text())
    else:
        events = json.loads((Path(replay) / 'events.json').read_text()) if replay else []
    if historical and replay:
        raise ValueError('TPU-only visualization cannot borrow local replay events')
    output.mkdir(parents=True, exist_ok=False)
    # Separate top/bottom bands preserve the whole source picture.
    width, height = rows[0]['image_size']
    shown_width = 960
    shown_height = int(round(height * shown_width / width / 2) * 2)
    band, foot = 104, 60
    sx, sy = shown_width / width, shown_height / height
    cap, maps = cv2.VideoCapture(str(source)), []
    with tempfile.TemporaryDirectory(prefix='matvey_render_', dir=output) as temp:
        temp = Path(temp)
        for i, row in enumerate(rows):
            ok, bgr = cap.read()
            if not ok:
                raise ValueError('source decoder ended early')
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            if hashlib.sha256(rgb.tobytes()).hexdigest() != row['rgb_sha256']:
                raise ValueError('source RGB differs from saved neural input')
            canvas = np.zeros((band + shown_height + foot, shown_width, 3), dtype=np.uint8)
            canvas[:] = (22, 22, 22)
            canvas[band:band + shown_height] = cv2.resize(bgr, (shown_width, shown_height), interpolation=cv2.INTER_LINEAR)
            current = local_frames.get(i) if local_frames is not None else captured.get(i) if captured is not None else row
            models = current['models'] if current else []
            counts = {}
            for model in models:
                pose_model = 'pose' in model['model_id']
                for d in model['detections']:
                    name = d['class_name']
                    counts[name] = counts.get(name, 0) + 1
                    if name not in DISPLAY_CLASSES:
                        continue
                    color = (80, 225, 110) if name == 'person' else (0, 185, 255)
                    if name == 'no_helmet':
                        color = (210, 80, 245)
                    if name == 'helmet':
                        color = (245, 210, 70)
                    if pose_model:
                        color = (235, 180, 65)
                    x1, y1, x2, y2 = d['bbox_xyxy']
                    a, b = (round(x1 * sx), band + round(y1 * sy)), (round(x2 * sx), band + round(y2 * sy))
                    cv2.rectangle(canvas, a, b, color, 1 if pose_model else 2)
                    label = ('pose' if pose_model else name) + ' ' + format(d['confidence'], '.2f')
                    cv2.putText(canvas, label, (max(0, a[0]), max(band + 13, a[1] - 4)), cv2.FONT_HERSHEY_SIMPLEX, .43, color, 1, cv2.LINE_AA)
                    points = d.get('pose_coco17')
                    if points:
                        for a_id, b_id in SKELETON:
                            a_kp, b_kp = points[a_id], points[b_id]
                            if min(a_kp[2], b_kp[2]) >= .3:
                                cv2.line(canvas, (round(a_kp[0] * sx), band + round(a_kp[1] * sy)),
                                         (round(b_kp[0] * sx), band + round(b_kp[1] * sy)), color, 2, cv2.LINE_AA)
                        for x, y, score in points:
                            if score >= .3:
                                cv2.circle(canvas, (round(x * sx), band + round(y * sy)), 3, color, -1, cv2.LINE_AA)
            label = 'HISTORICAL LinQ | sampled actual frames only | new TPU calls: 0' if captured is not None else row['backend'] + ' | full-scene saved neural outputs | not a TPU run'
            title = meta['scene_id'] + ' | ' + ('TPU INFERENCE CAPTURE' if captured is not None and current else 'NO TPU INFERENCE ON THIS FRAME' if captured is not None else 'MODEL OUTPUTS')
            if local_frames is not None:
                label = 'ONNXRUNTIME CPU | real Argus job | 38/75 source frames | not a TPU run'
                title = meta['scene_id'] + ' | ' + ('ACTUAL ARGUS NEURAL OUTPUT' if current else 'NO NEURAL INFERENCE ON THIS FRAME')
            for y, text, color in [(25, title, (255, 255, 255)), (51, label, (125, 220, 255)),
                (78, 'Original frame: ' + str(i) + ' | original PTS: ' + format(row['original_pts_ms'], '.3f') + ' ms', (210, 210, 210))]:
                cv2.putText(canvas, text, (14, y), cv2.FONT_HERSHEY_SIMPLEX, .55, color, 1, cv2.LINE_AA)
            active = visible_events(events, row['original_pts_ms'])
            status = 'ARGUS PREDICTION: ' + ', '.join(e['scenario'] + '/' + e['level_max'] for e in active) if active else 'Argus: no confirmed episode at this timestamp' if replay or local_frames is not None else 'Detector/pose visualization; no event decision'
            cv2.putText(canvas, status, (14, band + shown_height + 23), cv2.FONT_HERSHEY_SIMPLEX, .53, (60, 155, 255) if active else (220, 220, 220), 1, cv2.LINE_AA)
            cv2.putText(canvas, 'GT NOT SHOWN | no interpolation | boxes are model proposals, not verified violations', (14, band + shown_height + 47), cv2.FONT_HERSHEY_SIMPLEX, .43, (175, 175, 175), 1, cv2.LINE_AA)
            if not cv2.imwrite(str(temp / f'{i:06d}.png'), canvas):
                raise ValueError('PNG encode failed')
            maps.append({'frame_index': i, 'original_pts_ms': clock.at(i),
                'source_rgb_sha256': row['rgb_sha256'], 'neural_output_shown': current is not None,
                'shown_model_ids': [m['model_id'] for m in models], 'tracker_propagation': False,
                'confirmed_argus_episodes_shown': len(active)})
        if cap.read()[0]:
            raise ValueError('unreported source frames')
        cap.release()
        with (temp / 'frames.ffconcat').open('x') as stream:
            stream.write('ffconcat version 1.0\n')
            for i in range(len(rows)):
                duration = (clock.at(i + 1) - clock.at(i)) / 1000 if i + 1 < len(rows) else (clock.at(i) - clock.at(i - 1)) / 1000 if i else 1
                stream.write(f"file '{i:06d}.png'\noption framerate 1000\nduration {duration:.9f}\n")
        cmd = ['ffmpeg', '-v', 'warning', '-nostdin', '-threads', '1', '-safe', '0', '-f', 'concat',
            '-i', str(temp / 'frames.ffconcat'), '-an', '-c:v', 'libx264', '-threads', '2', '-preset', 'veryfast',
            '-crf', '20', '-pix_fmt', 'yuv420p', '-fps_mode', 'vfr',
            '-enc_time_base', '1:1000', '-video_track_timescale', '1000000', '-movflags', '+faststart',
            str(output / 'annotated.mp4')]
        with (output / 'render.log').open('x') as log:
            log.write(' '.join(cmd).replace(str(temp), '<temporary_png_directory>') + '\n')
            log.flush()
            subprocess.run(cmd, check=True, stdout=log, stderr=subprocess.STDOUT)
    presented = FilePTS(output / 'annotated.mp4')
    if len(presented.times) != len(rows):
        raise ValueError('render frame count changed')
    errors = []
    for row, pts in zip(maps, presented.times):
        row['annotated_pts_ms'] = pts
        error = pts - (row['original_pts_ms'] - clock.at(0))
        row['presentation_quantization_error_ms'] = error
        errors.append(abs(error))
    if max(errors) > 1.01:
        raise ValueError('annotated presentation timing drift exceeded 1ms')
    write_json(output / 'video_time_map.json', maps)
    report = {'status': 'PASS_ALL_SOURCE_FRAMES_RENDERED', 'source_sha256': meta['source_sha256'],
        'annotated_sha256': digest(output / 'annotated.mp4'), 'frames': len(maps),
        'source_pts_origin_ms': clock.at(0), 'presentation_pts_origin_ms': presented.at(0),
        'max_presentation_quantization_error_ms': max(errors), 'source_pts_exact_in_json': True,
        'last_frame_display_duration': 'encoder packet duration may differ; all source frames and their presentation PTS verified',
        'mode': 'ACTUAL_LOCAL_ARGUS_JOB' if local_frames is not None else 'HISTORICAL_TPU_CAPTURE_ONLY' if captured is not None else 'LOCAL_NEURAL_OUTPUTS',
        'new_neural_calls': 0, 'new_tpu_calls': 0,
        'inferred_frame_indices': sorted(local_frames) if local_frames is not None else sorted(captured) if captured is not None else list(range(len(rows))),
        'no_inference_frame_indices': [i for i in range(len(rows)) if (local_frames is not None and i not in local_frames) or (captured is not None and i not in captured)],
        'tracker_carried_predictions': 0, 'source_video_resized_for_visualization_only': True,
        'no_source_crop': True, 'audio_not_copied_in_visualization': True,
        'event_source': str(Path(local_app) / 'episodes.json') if local_app else str(Path(replay) / 'events.json') if replay else None}
    write_json(output / 'render_validation.json', report)
    print(json.dumps({'scene': meta['scene_id'], 'frames': len(maps), 'render_status': report['status']}), flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scene', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--replay', type=Path)
    parser.add_argument('--historical-capture', type=Path)
    parser.add_argument('--argus-local-run', type=Path)
    args = parser.parse_args()
    render(args.scene, args.output, args.replay, args.historical_capture, args.argus_local_run)


if __name__ == '__main__':
    main()
