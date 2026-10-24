"""Bounded inference-only video sampling using the existing durable LinQ client.

No behavior rules, zones, events, app writes, upload, network setup or fallback.
Preflight validates own staging receipts offline BEFORE opening any connection.
"""
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import shutil

import numpy as np

from ml.detection import preprocess, decode
from ml.linq.journal import RequestJournal, atomic_json, tensor_metadata
from ml.linq.namespace import check_program_name, reply_queue
from ml.linq.video import DurableVideoRunner
from ml.pipeline.runtime_lock import deployment_lock
from ml.quality.handoff import sha256
from ml.scenarios.cli import VideoEvidenceFrames
from ml.video_handoff import file_spec, model_detection


PROFILES = {
    'helmet-v1': ('helmet', 'matvey_helmet-v1.tpu', '408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa'),
    'pose-split-v1': ('pose-split', 'matvey_pose-split-v1.tpu', 'c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b'),
}
BASELINE = Path('/workspace/artifacts/video-mvp/industrial-001')
UPLOAD_JOURNAL = Path('/workspace/artifacts/linq-rpc/requests')


def prepare_bindings(output):
    """Prepare local names only; never fabricate placement or change TPU bytes."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    paths = []
    for model_id, (short, own_name, expected_sha) in PROFILES.items():
        manifest = json.loads((BASELINE / (short + '-verified.json')).read_text())
        if manifest['model_id'] != model_id or manifest['linq']['program_sha256'] != expected_sha:
            raise ValueError('reviewed baseline identity changed')
        manifest['linq']['program_name'] = own_name
        manifest['matvey_staging_receipt'] = str(Path('/workspace/artifacts/linq-rpc') /
                                               ('matvey_' + short + '_staging_v1/staging-receipt.json'))
        path = output / ('matvey_' + short + '_manifest.json')
        atomic_json(path, manifest)
        paths.append(str(path))
    atomic_json(output / 'matvey_preparation.json', {'status': 'LOCAL_BINDINGS_ONLY_NOT_REMOTE_READY',
                'manifests': paths, 'remote_files_created': 0, 'new_remote_calls': 0})
    return paths


def preflight_manifest(path, *, upload_journal=UPLOAD_JOURNAL):
    manifest = json.loads(Path(path).read_text())
    model_id = manifest['model_id']
    if model_id not in PROFILES:
        raise ValueError('only reviewed Helmet/Split-Pose supported')
    short, own_name, expected_sha = PROFILES[model_id]
    runtime = manifest['linq']
    check_program_name(runtime['program_name'])
    if (runtime['program_name'] != own_name or runtime['program_sha256'] != expected_sha
            or sha256(runtime['program_path']) != expected_sha or runtime.get('runtime_abi_verified') is not True):
        raise ValueError('reviewed program bytes and ABI required')
    reference = json.loads((BASELINE / (short + '-verified.json')).read_text())
    for key in ('decoder', 'classes', 'input', 'split_outputs', 'keypoint_count'):
        if manifest.get(key) != reference.get(key):
            raise ValueError('stable model class/input/decoder ABI changed')
    for key in ('inputs', 'outputs', 'input_map', 'output_map'):
        if runtime.get(key) != reference['linq'].get(key):
            raise ValueError('runtime tensor ABI differs from verified baseline')
    receipt_path = Path(manifest.get('matvey_staging_receipt', ''))
    if not receipt_path.is_file():
        raise ValueError('verified own Matvey staging receipt missing')
    receipt = json.loads(receipt_path.read_text())
    if (receipt.get('status') != 'STAGED' or receipt.get('namespace_owner') != 'matvey'
            or receipt.get('model_id') != model_id or receipt.get('program_name') != own_name
            or receipt.get('program_sha256') != expected_sha
            or receipt.get('bytes') != Path(runtime['program_path']).stat().st_size
            or receipt.get('program_path_namespace_verified') is not True
            or receipt.get('remote_completion') != 'response_received'):
        raise ValueError('own staging receipt identity mismatch')
    # The receipt must refer to the actual numeric upload reply, not just a flag.
    store = RequestJournal(upload_journal)
    record = store.load(receipt['upload_request_id'])
    if (record['purpose'] != 'model_upload' or record['state'] != 'COMPLETED'
            or type(record.get('status_code')) is not int or record['status_code'] != 0
            or record.get('reply_queue') != reply_queue(receipt['upload_request_id'])
            or record.get('response_id') != receipt['upload_request_id']):
        raise ValueError('completed correlated own upload required')
    outputs = store.outputs(receipt['upload_request_id'])
    if (set(outputs) != {'sha256', 'byte_count'} or outputs['sha256'].dtype != np.uint8
            or outputs['sha256'].shape != (32,) or outputs['sha256'].tobytes().hex() != expected_sha
            or outputs['byte_count'].dtype != np.int64 or outputs['byte_count'].shape != (1,)
            or int(outputs['byte_count'][0]) != receipt['bytes']):
        raise ValueError('remote upload hash/byte-count proof mismatch')
    return manifest


def load_completed_result(path, manifest, tensor, transform, rgb_sha256, logical_id, output):
    """Recheck the saved prediction against its completed numeric journal offline."""
    saved = json.loads(Path(path).read_text())
    value = saved['result']
    mid, program_sha = manifest['model_id'], manifest['linq']['program_sha256']
    if (saved['source_rgb_sha256'] != rgb_sha256 or value['model_id'] != mid
            or value['program_sha256'] != program_sha or value['original_transform'] != asdict(transform)):
        raise ValueError('completed frame source/model/geometry changed')
    uid = value['transport_provenance']['request_id']
    context = output / 'rpc' / mid / hashlib.sha256(logical_id.encode()).hexdigest()
    pointer = json.loads((context / 'request-pointer.json').read_text())
    logical = json.loads((context / 'logical.json').read_text())
    store = RequestJournal(output / 'requests')
    record = store.load(uid)
    if (pointer['journal_request_id'] != uid or logical['model_id'] != mid
            or logical['program_sha256'] != program_sha
            or logical['logical_request_id'] != logical_id or record['purpose'] != 'inference'
            or record['state'] != 'COMPLETED' or type(record.get('status_code')) is not int
            or record['status_code'] != 0 or record.get('response_id') != uid
            or logical['inputs'] != tensor_metadata({'images': tensor}) or record['inputs'] != logical['inputs']):
        raise ValueError('completed frame durable request binding mismatch')
    decoded = [model_detection(d, manifest['classes']) for d in decode(store.outputs(uid), manifest, transform)]
    if decoded != value['detections']:
        raise ValueError('saved detections differ from completed TPU tensors')
    return value


def run(source, source_sha256, manifests, frame_indices, output):
    """Sequential frame/model calls; same state resumes the same durable UUID."""
    import cv2
    cv2.setNumThreads(1)
    if (not manifests or len(manifests) > 2 or not frame_indices or frame_indices != sorted(set(frame_indices))
            or any(type(i) is not int or i < 0 for i in frame_indices)
            or len(frame_indices) * len(manifests) > 24):
        raise ValueError('sorted unique frames required; bounded maximum24 model calls')
    if sha256(source) != source_sha256:
        raise ValueError('source MP4 checksum mismatch')
    # All models must pass before ANY runner can submit a task.
    models = [preflight_manifest(path) for path in manifests]
    if len({m['model_id'] for m in models}) != len(models):
        raise ValueError('unique model manifests required')
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    with deployment_lock(output / 'matvey_frames.lock'):
        identity = {'source_sha256': source_sha256, 'frame_indices': frame_indices,
                    'model_manifests': {str(Path(p).resolve()): sha256(p) for p in manifests}}
        session = output / 'matvey_session.json'
        if session.exists():
            if json.loads(session.read_text()) != identity:
                raise ValueError('state belongs to a different source/model/sample configuration')
        else:
            atomic_json(session, identity)
        original = output / 'matvey_source_original.mp4'
        if not original.exists():
            shutil.copyfile(source, original)
        if sha256(original) != source_sha256:
            raise ValueError('original MP4 copy changed')
        provider = VideoEvidenceFrames(source)
        frames = []
        try:
            for index in frame_indices:
                pts = provider.clock.at(index)
                # Image geometry is read from the actual decoder, not invented.
                cap_size = [int(provider.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(provider.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))]
                batch = {'source_sha256': source_sha256, 'frame_id': index, 'media_time_ms': pts, 'image_size': cap_size}
                rgb = provider(batch)
                frame = {'frame_index': index, 'original_pts_ms': pts, 'image_size': cap_size,
                         'source_rgb_sha256': hashlib.sha256(rgb.tobytes(order='C')).hexdigest(), 'models': []}
                for manifest in models:
                    mid = manifest['model_id']
                    tensor, transform = preprocess(rgb, manifest)
                    logical_id = source_sha256 + ':' + str(index) + ':' + mid
                    result_path = output / ('matvey_frame_' + str(index) + '_' + mid + '.json')
                    if result_path.exists():
                        frame['models'].append(load_completed_result(result_path, manifest, tensor, transform,
                                              frame['source_rgb_sha256'], logical_id, output))
                        continue
                    effective = dict(manifest['linq'], model_id=mid, timeout=60,
                                     rpc_state_dir=str(output / 'rpc' / mid), journal_dir=str(output / 'requests'),
                                     format_source_manifest='/workspace/artifacts/linq-rpc/format-source.json')
                    with DurableVideoRunner(effective) as runner:
                        result = runner({'images': tensor}, {'request_id': logical_id, 'model_id': mid,
                                        'program_sha256': effective['program_sha256']})
                    provenance = result['transport_provenance']
                    decoded = [model_detection(d, manifest['classes']) for d in decode(result['outputs'], manifest, transform)]
                    exported = {'model_id': mid, 'version': mid.rsplit('-', 1)[-1],
                                'program_sha256': effective['program_sha256'], 'original_transform': asdict(transform),
                                'decoder_thresholds': manifest['thresholds'], 'detections': decoded,
                                'actual_preprocessing': 'PIL_BILINEAR_RGB_LETTERBOX_PAD114',
                                'transport_provenance': provenance,
                                'raw_numeric_directory': str(Path('requests') / provenance['request_id'])}
                    atomic_json(result_path, {'source_rgb_sha256': frame['source_rgb_sha256'], 'result': exported})
                    frame['models'].append(exported)
                frames.append(frame)
                atomic_json(output / 'matvey_frames.intermediate.json', {
                    'format': 'MATVEY_INTERMEDIATE_NOT_ARGUS_FINAL', 'source': {'file': original.name, **file_spec(original)},
                    'frames': frames, 'requested_frame_indices': frame_indices,
                    'processed_frame_indices': [f['frame_index'] for f in frames], 'partial': True,
                    'original_frame_count': len(provider.clock.times), 'backend': 'linq',
                    'scope': 'actual per-frame inference only; no rules/events/industrial-quality claim'})
        finally:
            provider.close()
    return {'status': 'COMPLETED_SELECTED_FRAMES', 'frames': len(frames), 'models': len(models),
            'whole_video_processed': False, 'output': str(output)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-bindings')
    parser.add_argument('--manifest', action='append', default=[])
    parser.add_argument('--preflight-only', action='store_true')
    parser.add_argument('--source')
    parser.add_argument('--source-sha256')
    parser.add_argument('--frames', default='0')
    parser.add_argument('--output')
    args = parser.parse_args()
    if args.prepare_bindings:
        if not Path(args.prepare_bindings).resolve().is_relative_to(Path('/workspace/artifacts')):
            parser.error('prepared bindings stay outside Git under artifacts')
        print(json.dumps({'status': 'PREPARED_NOT_REMOTE_READY', 'manifests': prepare_bindings(args.prepare_bindings)}))
        return 0
    if not args.manifest:
        parser.error('reviewed manifests required')
    try:
        if args.preflight_only:
            for path in args.manifest:
                preflight_manifest(path)
            print(json.dumps({'status': 'OWN_STAGING_PREFLIGHT_PASS', 'new_remote_calls': 0}))
            return 0
        if not args.source or not args.source_sha256 or not args.output:
            parser.error('source, source SHA256 and output required')
        if not Path(args.output).resolve().is_relative_to(Path('/workspace/artifacts')):
            parser.error('state and media stay outside Git under artifacts')
        print(json.dumps(run(args.source, args.source_sha256, args.manifest,
                             [int(i) for i in args.frames.split(',')], args.output)))
        return 0
    except Exception as error:
        from ml.linq.backend import PendingRequestError
        if isinstance(error, PendingRequestError):
            print(json.dumps({'status': 'PAUSED_SAME_REQUEST', 'code': error.code,
                              'transport': error.transport_provenance}))
            return 3
        print(json.dumps({'status': 'BLOCKED', 'error_type': type(error).__name__,
                          'error_code': 'OWN_STAGING_GATE_FAILED' if args.preflight_only else 'STOPPED_PRESERVE_DURABLE_STATE',
                          'no_automatic_retry': True}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
