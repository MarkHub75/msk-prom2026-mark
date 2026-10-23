"""Eight fixed Mendeley calibration midpoints; never reads reserved-source pixels.

The entire Mendeley camera/scene component is calibration-only. This is not a
quality evaluation. Requires ffmpeg/ffprobe plus existing detection preprocess.
"""
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np
from ml.detection.codec import preprocess
from .compile import sha256

CLIPS = ('0_te23.mp4', '0_te9.mp4', '0_tr128.mp4', '0_tr16.mp4',
         '4_te19.mp4', '4_te5.mp4', '4_tr13.mp4', '4_tr6.mp4')
COMPONENT = 'mendeley-industrial-unknown-camera-component'


def prepare_frames(clips_root, model_manifest, reservations_path, output):
    out = Path(output)
    if out.exists():
        raise ValueError('fresh calibration directory required')
    reservations = json.loads(Path(reservations_path).read_text())
    if not {'construction-ppe', 'urfall', 'sfchd', 'sh17'} <= set(reservations['reserved_dataset_families']):
        raise ValueError('all reserved dataset families must be declared')
    if COMPONENT in reservations['reserved_groups']:
        raise ValueError('Mendeley component must not also be reserved evaluation data')
    manifest = json.loads(Path(model_manifest).read_text())
    sources = [Path(clips_root) / name for name in CLIPS]
    hashes = [sha256(path) for path in sources]
    if set(hashes) & set(reservations['reserved_source_sha256']):
        raise ValueError('calibration video overlaps reserved sources')
    out.mkdir(parents=True, exist_ok=False)
    entries = []
    for path, digest in zip(sources, hashes):
        probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,nb_frames,avg_frame_rate', '-of', 'json', str(path)],
            check=True, capture_output=True, timeout=90)
        stream = json.loads(probe.stdout)['streams'][0]
        count = int(stream['nb_frames'])
        if count < 2:
            raise ValueError('source must expose a known nontrivial frame count')
        frame_index = count // 2
        decoded = subprocess.run(['ffmpeg', '-v', 'error', '-threads', '2', '-noautorotate',
            '-i', str(path), '-vf', f'select=eq(n\\,{frame_index})', '-frames:v', '1',
            '-threads', '2', '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'],
            check=True, capture_output=True, timeout=90)
        frame = np.frombuffer(decoded.stdout, np.uint8).reshape(stream['height'], stream['width'], 3).copy()
        tensor, transform = preprocess(frame, manifest)
        name = path.stem
        np.savez(out / (name + '-rgb.npz'), rgb=frame)
        sample_path = out / (name + '-input.npz')
        np.savez(sample_path, **{manifest['input']['name']: tensor})
        entries.append({'path': sample_path.name, 'sha256': sha256(sample_path),
            'source_dataset': 'mendeley-industrial', 'source_group': COMPONENT,
            'source_sha256': digest, 'source_filename': path.name, 'split': 'calibration',
            'source_frame_index': frame_index, 'source_frame_count': count,
            'selection': 'zero-based floor(nb_frames/2), sequential ffmpeg select; no autorotate',
            'source_avg_frame_rate': stream['avg_frame_rate'],
            'source_pts_ms': None, 'pts_note': 'frame-index selection; exact PTS not asserted',
            'rgb_npz': name + '-rgb.npz', 'rgb_npz_sha256': sha256(out / (name + '-rgb.npz')),
            'decoded_rgb_sha256': hashlib.sha256(frame.tobytes()).hexdigest(),
            'original_transform': asdict(transform)})
    report = dict(reservations, samples=entries, sample_count=len(entries),
        calibration_source_dataset='mendeley-industrial',
        group_independence='ONE_CONSERVATIVE_UNKNOWN_CAMERA_COMPONENT',
        all_mendeley_usage='TRAIN_CALIBRATION_ONLY_NEVER_INDEPENDENT_QUALITY',
        near_duplicate_review='CONSERVATIVE_SHARED_COMPONENT; no independence claimed',
        preprocessing='existing ml.detection.codec.preprocess RGB uint8, bilinear letterbox114 /255',
        model_manifest_sha256=sha256(model_manifest),
        calibration_statistics_status='NEXT prepare_candidate BEFORE METRICS',
        evaluation='NOT_RUN', linq_status='NOT_RUN')
    (out / 'calibration-manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('clips-root', 'model-manifest', 'reservations', 'output'):
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    report = prepare_frames(args.clips_root, args.model_manifest, args.reservations, args.output)
    print(json.dumps({'status': 'PREPARED_CALIBRATION_ONLY', 'sample_count': report['sample_count'],
                      'source_group_count': 1, 'evaluation': 'NOT_RUN'}))


if __name__ == '__main__':
    main()
