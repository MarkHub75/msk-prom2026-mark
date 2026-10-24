"""Export allowlisted intermediate results from completed real video TPU calls.

Not an Argus schema, importer, scenario engine, upload or new remote inference.
The source MP4 is copied byte-for-byte. Numeric tensors remain available for a
later contract adapter without repeating neural inference.
"""
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import shutil
from uuid import UUID

import numpy as np

from ml.detection import preprocess, decode
from ml.linq.journal import RequestJournal, tensor_metadata
from ml.pipeline.video_clock import FilePTS
from ml.quality.handoff import sha256
from ml.scenarios.cli import VideoEvidenceFrames


SOURCE = Path('/workspace/datasets/quality/temporal/raw/mendeley/4_tr6.mp4')
SOURCE_SHA256 = 'f0e34d76de139450b97decbb4e032a525d8ce9959d972cdd0071a1de69250c6a'
CAPTURE = Path('/workspace/artifacts/video-mvp/industrial-001')
OBSERVATIONS_SHA256 = '0ac461bd2221db1f796453ed963fdebb412cb50ab561fd67bf66868494375e59'
PROFILES = {
    'industrial': (SOURCE, SOURCE_SHA256, CAPTURE, OBSERVATIONS_SHA256,
                   {'helmet-v1', 'pose-split-v1'}, [0, 13]),
    'urfall01': (Path('/workspace/datasets/quality/temporal/processed/urfall/fall-01-cam0-rgb.mp4'),
                 'ad08c42886c274c03876a68fb7f2be3b065c951d7202847317d126c61bb1d760',
                 Path('/workspace/artifacts/quality/pose/e00-linq-urfall01-2fps'),
                 '526f147c2ed44513abe27ceb3fa56be1f4a089dea559443d6463337187518726',
                 {'pose-split-v1'}, list(range(0, 151, 15))),
}


def write_json(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write('\n')


def file_spec(path):
    path = Path(path)
    return {'bytes': path.stat().st_size, 'sha256': sha256(path)}


def model_detection(value, classes):
    source_name = value['class_name']
    class_id = classes.index(source_name)
    return {'class_id': class_id, 'source_class_name': source_name,
            'class_name': 'no_helmet' if source_name == 'bare_head' else source_name,
            'confidence': value['score'], 'bbox_xyxy': value['bbox_xyxy'],
            'pose_coco17': value.get('keypoints')}


def verified_completed_request(journal, request_id, execution):
    if str(UUID(request_id)) != request_id:
        raise ValueError('canonical transport UUID required')
    record = journal.load(request_id)
    provenance = execution['transport_provenance']
    if (record['state'] != 'COMPLETED' or record['purpose'] != 'inference'
            or type(record.get('status_code')) is not int or record['status_code'] != 0
            or record.get('response_id') != request_id
            or provenance.get('response_id') != request_id
            or type(provenance.get('status_code')) is not int or provenance['status_code'] != 0
            or provenance.get('remote_completion') != 'response_received'
            or execution.get('status') != 'ok' or execution.get('backend') != 'linq'):
        raise ValueError('completed correlated actual inference required')
    return record, journal.outputs(request_id)


def export_captured_video(output, profile='industrial'):
    """Export an explicitly pinned completed sample, never relabel as a fresh run."""
    import cv2
    cv2.setNumThreads(1)
    source, source_sha, capture, observations_sha, expected_models, expected_frames = PROFILES[profile]
    output = Path(output)
    observations_path = capture / 'observations.jsonl'
    if sha256(source) != source_sha or sha256(observations_path) != observations_sha:
        raise ValueError('reviewed source or capture observations changed')
    all_observations = [json.loads(line) for line in observations_path.read_text().splitlines() if line.strip()]
    observations = [b for b in all_observations if b['status'] == 'ok']
    session = json.loads((capture / 'video-session.json').read_text())
    manifests = {m['model_id']: m for m in session['manifests']}
    if set(manifests) != expected_models or [b['frame_id'] for b in observations] != expected_frames:
        raise ValueError('fixed real capture scope required')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'models').mkdir()
    decoder_keys = {'schema_version', 'model_id', 'decoder', 'classes', 'source_classes', 'input',
                    'output_layout', 'nms_in_graph', 'padding_value', 'thresholds', 'versions', 'opset',
                    'keypoint_count', 'keypoint_order', 'split_outputs', 'output_shapes'}
    for model_id, manifest in manifests.items():
        write_json(output / 'models' / (model_id + '_decoder.json'),
                   {k: v for k, v in manifest.items() if k in decoder_keys})
    shutil.copyfile(source, output / 'matvey_source_original.mp4')
    if sha256(output / 'matvey_source_original.mp4') != source_sha:
        raise ValueError('original MP4 copy changed bytes')
    journal = RequestJournal(capture / 'requests')
    provider, frames, calls = VideoEvidenceFrames(source), [], []
    try:
        for batch in observations:
            rgb = provider(batch)
            pts = provider.clock.at(batch['frame_id'])
            rgb_sha = hashlib.sha256(rgb.tobytes(order='C')).hexdigest()
            frame = {'frame_index': batch['frame_id'], 'original_pts_ms': pts,
                     'original_observation_media_time_ms': batch['media_time_ms'],
                     'image_size': batch['image_size'], 'source_rgb_sha256': rgb_sha, 'models': []}
            if batch.get('backend') != 'linq' or batch.get('source_sha256') != source_sha:
                raise ValueError('real LinQ observation/source binding required')
            for execution in batch['execution_records']:
                model_id = execution['model_id']
                manifest = manifests[model_id]
                program_sha = manifest['linq']['program_sha256']
                if execution['program_sha256'] != program_sha:
                    raise ValueError('executed program identity mismatch')
                request_id = execution['transport_provenance']['request_id']
                record, tensors = verified_completed_request(journal, request_id, execution)
                directory = journal.path(request_id)
                if (record['input_artifact']['file'] != 'inputs.npz'
                        or sha256(directory / 'inputs.npz') != record['input_artifact']['sha256']):
                    raise ValueError('captured input file checksum mismatch')
                with np.load(directory / 'inputs.npz', allow_pickle=False) as archive:
                    inputs = {name: archive[name].copy() for name in archive.files}
                if tensor_metadata(inputs) != record['inputs']:
                    raise ValueError('captured input tensor checksum mismatch')
                tensor, transform = preprocess(rgb, manifest)
                if set(inputs) != {'images'} or not np.array_equal(tensor, inputs['images']):
                    raise ValueError('source frame does not reproduce actual submitted tensor')
                spec_by_name = {s['name']: s for s in manifest['linq']['outputs']}
                if set(spec_by_name) != set(tensors):
                    raise ValueError('actual output names differ from reviewed runtime ABI')
                for name, spec in spec_by_name.items():
                    if list(tensors[name].shape) != spec['shape'] or tensors[name].dtype.name != spec['dtype']:
                        raise ValueError('actual output tensor ABI mismatch')
                raw_model_dir = output / 'numeric' / request_id
                raw_model_dir.mkdir(parents=True)
                for name in ('inputs.npz', 'response.npz'):
                    shutil.copyfile(directory / name, raw_model_dir / name)
                detections = decode(tensors, manifest, transform)
                mapped = [model_detection(d, manifest['classes']) for d in detections]
                relative = str(raw_model_dir.relative_to(output))
                receipt = {'request_id': request_id, 'response_id': record['response_id'], 'status_code': 0,
                           'journal_state': 'COMPLETED', 'model_id': model_id, 'program_sha256': program_sha,
                           'request_created_utc': record['created_at'], 'completion_record_updated_utc': record['updated_at'],
                           'input_tensors': record['inputs'], 'output_tensors': record['response']['tensors'],
                           'full_transport_timings_ms': execution['transport_provenance'].get('timings', {}),
                           'device_only_ms': None, 'independent_hardware_attestation': False,
                           'scope': 'historical actual service completion; no new submission during export'}
                write_json(raw_model_dir / 'matvey_completion_receipt.json', receipt)
                frame['models'].append({'model_id': model_id, 'version': model_id.rsplit('-', 1)[-1],
                    'program_sha256': program_sha, 'export_versions': manifest.get('versions', {}),
                    'input_spec': manifest['input'], 'decoder': manifest['decoder'],
                    'decoder_manifest': 'models/' + model_id + '_decoder.json',
                    'original_transform': asdict(transform),
                    'actual_preprocessing': 'PIL_BILINEAR_RGB_LETTERBOX_PAD114_FLOAT32_MULTIPLY_1_OVER_255',
                    'decoder_thresholds': manifest['thresholds'], 'source_classes': manifest['classes'],
                    'detections': mapped, 'numeric_directory': relative, 'execution': receipt})
                calls.append(receipt)
            frames.append(frame)
    finally:
        provider.close()
    clock = FilePTS(source)
    result = {'format': 'MATVEY_INTERMEDIATE_CAPTURE_EXPORT_NOT_ARGUS_FINAL',
              'source': {'file': 'matvey_source_original.mp4', **file_spec(source),
                         'original_frame_count': len(clock.times), 'first_original_pts_ms': clock.times[0],
                         'last_original_pts_ms': clock.times[-1], 'modified': False},
              'coverage': {'partial': True, 'processed_frame_indices': [f['frame_index'] for f in frames],
                           'processed_frames': len(frames), 'historical_tpu_model_calls': len(calls),
                           'unprocessed_frames_are': 'NOT_INFERRED_NOT_NEGATIVE',
                           'fresh_tpu_model_calls': 0},
              'backend': 'LINQ_HISTORICAL_REAL_SERVICE_OUTPUTS',
              'profile': profile,
              'non_inference_records': [{'frame_index': b['frame_id'], 'media_time_ms': b['media_time_ms'],
                                         'status': b['status'], 'meaning': 'NO_NEURAL_INFERENCE'}
                                        for b in all_observations if b['status'] != 'ok'],
              'export_operation': 'OFFLINE_INTEGRITY_REVIEW_AND_DECODE_ONLY',
              'frames': frames, 'new_neural_calls': 0, 'new_remote_calls': 0,
              'raw_tensor_scope': 'full explicitly selected numeric input/output tensors only; no notebook or credentials',
              'class_mapping': {mid: {str(i): ('no_helmet' if name == 'bare_head' else name)
                                      for i, name in enumerate(m['classes'])} for mid, m in manifests.items()},
              'mapping_authority': 'main docs/ML_INTEGRATION.md and ml/safewatch.class_map.json; final Argus contract pending',
              'preprocessing_compatibility': 'historical PIL resize differs from current Argus OpenCV resize; use actual decoded original-pixel results/transform, do not claim identical Argus input tensors',
              'quality': 'NO_EXHAUSTIVE_GT_OR_CONFIRMED_INDUSTRIAL_VIOLATION',
              'fresh_run_blocker': 'own Matvey staging/receipt and authorized namespace-aware binding absent; no fresh submission attempted'}
    write_json(output / 'matvey_linq_frames.intermediate.json', result)
    write_json(output / 'matvey_tpu_proof.json', {'actual_historical_correlated_completions': calls,
        'input_source_rgb_and_preprocessing': f'BITWISE_MATCH_ALL_{len(calls)}_SUBMISSIONS',
        'output_files_and_tensor_hashes': 'PASS', 'actual_new_inference_this_export': False,
        'fresh_remote_submission': 'BLOCKED_BY_OWN_PLACEMENT', 'no_independent_chip_attestation': True})
    write_json(output / 'matvey_checksums.json', {
        str(p.relative_to(output)): file_spec(p) for p in sorted(output.rglob('*')) if p.is_file()})
    return result


def verify_export(directory):
    """Review a portable export using only its files and the existing decoder."""
    import cv2
    cv2.setNumThreads(1)
    directory = Path(directory).resolve()
    checksums = json.loads((directory / 'matvey_checksums.json').read_text())
    for relative, expected in checksums.items():
        path = directory / relative
        if (path.absolute() != path.resolve() or not path.is_file()
                or not path.resolve().is_relative_to(directory) or file_spec(path) != expected):
            raise ValueError('export checksum/path mismatch')
    data = json.loads((directory / 'matvey_linq_frames.intermediate.json').read_text())
    source = directory / data['source']['file']
    if file_spec(source) != {k: data['source'][k] for k in ('bytes', 'sha256')}:
        raise ValueError('original source bytes changed')
    frames = data['frames']
    if (data['coverage']['processed_frame_indices'] != [f['frame_index'] for f in frames]
            or data['coverage']['processed_frames'] != len(frames)
            or data['coverage']['partial'] is not True or data['coverage']['fresh_tpu_model_calls'] != 0):
        raise ValueError('partial historical coverage declaration mismatch')
    provider, calls = VideoEvidenceFrames(source), 0
    try:
        if data['source']['original_frame_count'] != len(provider.clock.times):
            raise ValueError('original frame census mismatch')
        previous = -1
        for frame in frames:
            if frame['frame_index'] <= previous:
                raise ValueError('frame index does not grow')
            previous = frame['frame_index']
            batch = {'frame_id': frame['frame_index'], 'media_time_ms': frame['original_pts_ms'],
                     'image_size': frame['image_size'], 'source_sha256': data['source']['sha256']}
            rgb = provider(batch)
            if hashlib.sha256(rgb.tobytes(order='C')).hexdigest() != frame['source_rgb_sha256']:
                raise ValueError('source RGB binding mismatch')
            for model in frame['models']:
                manifest = json.loads((directory / model['decoder_manifest']).read_text())
                tensor, transform = preprocess(rgb, manifest)
                if asdict(transform) != model['original_transform']:
                    raise ValueError('original coordinate transform mismatch')
                location = directory / model['numeric_directory']
                receipt = json.loads((location / 'matvey_completion_receipt.json').read_text())
                if (receipt != model['execution'] or receipt['request_id'] != receipt['response_id']
                        or receipt['status_code'] != 0 or receipt['journal_state'] != 'COMPLETED'
                        or receipt['program_sha256'] != model['program_sha256']):
                    raise ValueError('correlated completion receipt mismatch')
                with np.load(location / 'inputs.npz', allow_pickle=False) as archive:
                    inputs = {name: archive[name] for name in archive.files}
                with np.load(location / 'response.npz', allow_pickle=False) as archive:
                    outputs = {name: archive[name] for name in archive.files}
                if (tensor_metadata(inputs) != receipt['input_tensors']
                        or tensor_metadata(outputs) != receipt['output_tensors']
                        or not np.array_equal(tensor, inputs['images'])):
                    raise ValueError('input/output tensor integrity or source preprocessing mismatch')
                decoded = [model_detection(d, manifest['classes']) for d in decode(outputs, manifest, transform)]
                if decoded != model['detections']:
                    raise ValueError('decoded detections differ from saved raw TPU outputs')
                calls += 1
    finally:
        provider.close()
    if calls != data['coverage']['historical_tpu_model_calls']:
        raise ValueError('TPU completion census mismatch')
    return {'status': 'VERIFIED_HISTORICAL_CAPTURE_EXPORT', 'processed_frames': len(frames),
            'historical_correlated_model_calls': calls, 'original_mp4_byte_identical': True,
            'source_rgb_input_and_output_hashes': 'PASS', 'decoded_results_reproduced': True,
            'partial': True, 'new_remote_calls': 0, 'final_argus_schema': 'PENDING'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--profile', choices=tuple(PROFILES), default='industrial')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    output = Path(args.output)
    if not output.resolve().is_relative_to(Path('/workspace/artifacts')):
        parser.error('handoff media/tensors must stay under artifacts, outside Git')
    if args.verify_only:
        print(json.dumps(verify_export(output)))
        return
    result = export_captured_video(output, args.profile)
    print(json.dumps({'output': str(output), 'coverage': result['coverage'], 'new_remote_calls': 0}))


if __name__ == '__main__':
    main()
