"""Run verified remote models through the existing file worker; no local fallback."""
import argparse
from contextlib import nullcontext
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

from ml.detection import prepare_verified_manifest
from ml.contracts import validate_event,validate_observation
from ml.pipeline.capture_recovery import save_json
from ml.pipeline.local_sink import local_event_sink


def verify_results(state,receiver=None,source_path=None):
    import cv2
    import jsonschema
    from urllib.request import urlopen
    state=Path(state)
    session=json.loads((state/'video-session.json').read_text())
    observations=[validate_observation(json.loads(line)) for line in (state/'observations.jsonl').read_text().splitlines()]
    events=[validate_event(json.loads(line)) for line in (state/'events.jsonl').read_text().splitlines()]
    schema=json.loads((Path(__file__).parents[1]/'contracts/schemas/event.schema.json').read_text())
    frames={batch['frame_id']:batch for batch in observations if batch.get('reason')!='source_ended'}
    calls=[record['transport_provenance'] for batch in frames.values() for record in batch['execution_records']
           if record['status']=='ok']
    if any(c['request_id']!=c['response_id'] or c['status_code']!=0 or c['journal_state']!='COMPLETED' for c in calls):
        raise ValueError('uncorrelated or failed remote execution')
    identities=[(event['event_id'],event['revision']) for event in events]
    if len(identities)!=len(set(identities)):raise ValueError('duplicate event revision')
    evidence_count=0
    original_frames={}
    required={e['evidence']['frame_id'] for e in events if e['evidence']['status']=='ready'}
    if source_path and required:
        cap=cv2.VideoCapture(str(source_path));index=-1
        try:
            while required-set(original_frames):
                ok,bgr=cap.read()
                if not ok:raise ValueError('evidence source frame is missing')
                index+=1
                if index in required:
                    rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
                    original_frames[index]=(float(cap.get(cv2.CAP_PROP_POS_MSEC)),hashlib.sha256(rgb.tobytes(order='C')).hexdigest())
        finally:cap.release()
    for event in events:
        jsonschema.Draft202012Validator(schema).validate(event)
        evidence=event['evidence']
        if evidence['status']!='ready':continue
        batch=frames[evidence['frame_id']]
        if evidence['media_time_ms']!=batch['media_time_ms']:raise ValueError('wrong evidence PTS')
        snapshot=state/evidence['snapshot_ref']
        metadata=json.loads(snapshot.with_suffix('.json').read_text())
        if (metadata['frame_id']!=batch['frame_id'] or metadata['media_time_ms']!=batch['media_time_ms'] or
            metadata['source_sha256']!=session['source_sha256'] or
            metadata['snapshot_sha256']!=hashlib.sha256(snapshot.read_bytes()).hexdigest()):
            raise ValueError('evidence identity/hash mismatch')
        if source_path:
            pts,rgb_hash=original_frames[batch['frame_id']]
            if abs(pts-batch['media_time_ms'])>1e-6 or metadata['rgb_sha256']!=rgb_hash:
                raise ValueError('evidence does not refer to the original source frame')
        evidence_count+=1
        if receiver:
            with urlopen(receiver['evidence_base_url']+'/'+evidence['snapshot_ref'],timeout=5) as response:
                if response.read()!=snapshot.read_bytes():raise ValueError('receiver fetched different evidence')
    # A replayed/cached execution must not masquerade as a newly submitted call.
    rpc_ids={c['request_id'] for c in calls}
    result={'status':'PASS' if events and evidence_count and calls else 'NO_CONFIRMED_EPISODE',
        'scope':'file frames + remote LinQ; source kind and event policy are explicit, not ground truth',
        'source_kind':session.get('source_kind','real-video'),
        'processed_frames':len(frames),'correlated_completed_rpc_ids':len(rpc_ids),
        'event_revisions':len(events),'incidents':len({event['event_id'] for event in events}),
        'evidence_references_checked':evidence_count,'source_fps':session['source_fps'],
        'team_backend_integration':'NOT_VERIFIED','target_video_accuracy':'NOT_EVALUATED'}
    if receiver:
        with sqlite3.connect(receiver['database']) as db:
            result['local_test_received_revisions']=db.execute('SELECT count(*) FROM received').fetchone()[0]
            result['local_test_notifications']=db.execute('SELECT count(*) FROM notifications').fetchone()[0]
        result['local_test_evidence_http']='PASS' if evidence_count else 'NOT_EXERCISED'
        if result['local_test_received_revisions']!=len(events):raise ValueError('receiver has not committed all event revisions')
        if result['local_test_notifications']!=len({event['event_id'] for event in events if event['state']=='open'}):
            raise ValueError('incident notification duplication')
    save_json(state/'integration-review.json',result)
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--state-dir',default='/workspace/artifacts/video-mvp/industrial-001')
    parser.add_argument('--sample-fps',type=float,default=2)
    parser.add_argument('--max-frames',type=int,default=0)
    parser.add_argument('--start-ms',type=float,default=0)
    parser.add_argument('--end-ms',type=float)
    parser.add_argument('--timeout',type=float,default=60)
    parser.add_argument('--camera-id',default='industrial-demo-01')
    parser.add_argument('--source-kind',choices=['real-video','repeated-image-fixture'],default='real-video')
    parser.add_argument('--demo-policy',action='store_true',help='Explicit confidence0.25 diagnostic policy; default remains0.5')
    sinks=parser.add_mutually_exclusive_group()
    sinks.add_argument('--local-test-sink',action='store_true')
    sinks.add_argument('--backend-url')
    parser.add_argument('--evidence-base-url')
    args=parser.parse_args(argv)
    state=Path(args.state_dir).resolve();project=Path(__file__).parents[2]
    try:
        if not Path(args.source).is_file():raise ValueError('provide an existing real video file')
        if state.is_relative_to(project):raise ValueError('runtime video state must remain outside Git')
        state.mkdir(parents=True,exist_ok=True)
        manifests=[]
        for name in ('pose-split','helmet'):
            manifest=prepare_verified_manifest(name)
            target=state/(name+'-verified.json')
            if target.exists() and json.loads(target.read_text())!=manifest:raise ValueError('existing verified manifest changed')
            if not target.exists():save_json(target,manifest)
            manifests.append(target)
        receiver_context=local_event_sink(state/'test-receiver',state/'evidence') if args.local_test_sink else nullcontext(None)
        with receiver_context as receiver:
            command=[sys.executable,'-m','ml.pipeline.cli','--state-dir',str(state)]
            if args.demo_policy:command+=['--rules',str(project/'configs/rules.demo.json')]
            if receiver:command+=['--backend-url',receiver['event_url'],'--evidence-base-url',receiver['evidence_base_url'],'--sink-kind','local-test']
            elif args.backend_url:
                command+=['--backend-url',args.backend_url]
                if args.evidence_base_url:command+=['--evidence-base-url',args.evidence_base_url]
            command+=['video','--source',str(Path(args.source).resolve()),'--camera-id',args.camera_id,
                '--source-kind',args.source_kind,
                '--backend','linq','--linq-runner-factory','ml.linq.video:create_runner',
                '--sample-fps',str(args.sample_fps),'--max-frames',str(args.max_frames),
                '--start-ms',str(args.start_ms),'--linq-timeout',str(args.timeout)]
            if args.end_ms is not None:command+=['--end-ms',str(args.end_ms)]
            for manifest in manifests:command+=['--manifest',str(manifest)]
            print(json.dumps({'phase':'video_worker_started','state_dir':str(state),'neural_backend':'linq','local_test_sink':bool(receiver)}),flush=True)
            # Preserve earlier logs; SQLite-backed JSONL is the canonical deduplicated export.
            with (state/'worker.stdout.jsonl').open('a') as output,(state/'worker.stderr.log').open('a') as error:
                code=subprocess.run(command,stdout=output,stderr=error,check=False).returncode
            if code:
                print(json.dumps({'status':'WAITING_FOR_LINQ' if code==3 else 'NOT_COMPLETED','worker_exit_code':code,'state_dir':str(state)}))
                return code
            result=verify_results(state,receiver,args.source);print(json.dumps(result))
            return 0 if result['status']=='PASS' else 2
    except Exception as error:
        print(json.dumps({'status':'NOT_COMPLETED','error_type':type(error).__name__}))
        return 1


if __name__=='__main__':raise SystemExit(main())
