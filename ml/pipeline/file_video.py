"""Resume one offline video through the existing LinQ and behavior adapters.

File PTS drives behavior. Wall time measures processing and never substitutes for
unobserved media. A pending RPC stops the cursor without advancing the frame.
"""
from datetime import datetime,timezone
import hashlib
import json
import math
from pathlib import Path
import time
from uuid import uuid4

import cv2
import numpy as np
from ml.detection import preprocess,decode
from ml.pipeline.capture_recovery import save_json
from ml.pipeline.runtime_lock import deployment_lock

GLOBAL_VIDEO_LOCK=Path('/workspace/artifacts/linq-rpc/video-worker.lock')

def file_hash(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()


def _session(args,pipeline,manifests,fps):
    root=Path(args.state_dir);root.mkdir(parents=True,exist_ok=True)
    spec={'source_sha256':file_hash(args.source),'camera_id':args.camera_id,
          'source_fps':float(fps),'sample_fps':args.sample_fps,
          'start_ms':args.start_ms,'end_ms':args.end_ms,
          'rules':pipeline.behavior.config,'manifests':manifests}
    source_kind=getattr(args,'source_kind','real-video')
    if getattr(pipeline,'scenario_suite',None) is not None:
        spec['scenario_suite_sha256']=pipeline.scenario_suite.fingerprint
        spec['scenario_timestamp_basis']='encoded_best_effort_presentation_time'
    if source_kind!='real-video':spec['source_kind']=source_kind
    fingerprint=hashlib.sha256(json.dumps(spec,sort_keys=True,allow_nan=False).encode()).hexdigest()
    path=root/'video-session.json'
    if path.exists():
        session=json.loads(path.read_text())
        if session.get('fingerprint')!=fingerprint:raise ValueError('video state belongs to a different source/configuration')
    else:
        if pipeline.outbox.checkpoint() is not None:raise ValueError('existing state has no matching video session')
        session={'schema_version':'1.0','fingerprint':fingerprint,'stream_epoch':str(uuid4()),**spec}
        save_json(path,session)
    return session


def _checkpoint(session,frame_id,pts,*,complete=False):
    return {'fingerprint':session['fingerprint'],'stream_epoch':session['stream_epoch'],
            'frame_id':frame_id,'media_time_ms':pts,'complete':complete}


def _record(result,manifest):
    transport=result.get('transport_provenance')
    if transport is not None:
        keys=('request_id','response_id','status_code','journal_state','remote_completion',
              'cached_response','reconcile_only','timings')
        transport={key:transport[key] for key in keys if key in transport}
    return {'request_id':result['request_id'],'model_id':result['model_id'],
            'backend':'linq','status':result['status'],
            'program_sha256':manifest['linq']['program_sha256'],
            'execution_witness':result.get('execution_witness'),
            'execution_verified':result.get('execution_verified',False),
            'transport_provenance':transport,
            'timings':result.get('timings',{})}


def run_file_video(args,pipeline,cap,manifests,backends,fps):
    if not args.linq_runner_factory:raise ValueError('offline remote MVP requires explicit LinQ runner factory')
    root=Path(args.state_dir)
    # Serializes the MVP entry point across distinct state directories as well.
    with deployment_lock(GLOBAL_VIDEO_LOCK),deployment_lock(root/'video.lock'):
        opened=time.monotonic()
        session=_session(args,pipeline,manifests,fps)
        checkpoint=pipeline.outbox.checkpoint('video')
        if checkpoint and checkpoint['fingerprint']!=session['fingerprint']:
            raise ValueError('video cursor identity mismatch')
        if checkpoint and checkpoint['complete']:
            pipeline.outbox.export_jsonl(root)
            if pipeline.sink:pipeline.outbox.dispatch(pipeline.sink)
            result=json.loads((root/'summary.json').read_text()) if (root/'summary.json').exists() else {}
            previous={key:result.get(key) for key in ('wall_seconds_this_invocation','processed_fps_this_invocation',
                       'frame_cycle_p50_ms','frame_cycle_p95_ms','frames_this_invocation')}
            return {**result,'status':'COMPLETED_CACHED','new_remote_requests':0,
                'frames_this_invocation':0,'failed_frames_this_invocation':0,
                'wall_seconds_this_invocation':time.monotonic()-opened,
                'processed_fps_this_invocation':0,'frame_cycle_p50_ms':None,'frame_cycle_p95_ms':None,
                'previous_analysis_metrics':previous,**pipeline.outbox.counts()}
        return _process(args,pipeline,cap,manifests,backends,session,checkpoint,root)


def _process(args,pipeline,cap,manifests,backends,session,checkpoint,root):
    start=time.monotonic();last_id=checkpoint['frame_id'] if checkpoint else -1
    last_sample=checkpoint['media_time_ms'] if checkpoint else -math.inf
    frame_id=-1;previous_pts=-math.inf;processed=0;failures=0;last_batch=None;cycles=[]
    complete=False;status='PAUSED';pending=None
    clock=None
    if getattr(pipeline,'scenario_suite',None) is not None:
        from ml.pipeline.video_clock import FilePTS
        clock=FilePTS(args.source)
    try:
        while not args.max_frames or processed<args.max_frames:
            ok,bgr=cap.read()
            if not ok:
                complete=True;status='COMPLETED';break
            frame_id+=1;pts=clock.at(frame_id) if clock is not None else float(cap.get(cv2.CAP_PROP_POS_MSEC))
            if not math.isfinite(pts) or pts<0 or pts<=previous_pts:
                raise ValueError('file PTS is invalid or does not advance')
            previous_pts=pts
            if args.end_ms is not None and pts>args.end_ms:
                complete=True;status='COMPLETED';break
            if frame_id<=last_id or pts<args.start_ms or pts-last_sample+1e-6<1000/args.sample_fps:continue
            observed=time.monotonic();rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
            ingested_at=datetime.now(timezone.utc).isoformat()
            detections=[];records=[];errors=[]
            for manifest,backend in zip(manifests,backends):
                tensor,transform=preprocess(rgb,manifest)
                model_id=manifest['model_id'];input_name=manifest['input'].get('name','images')
                input_name=manifest['linq'].get('input_map',{}).get(input_name,input_name)
                result=backend.infer({'request_id':f"{session['stream_epoch']}:{frame_id}:{model_id}",
                    'model_id':model_id,'inputs':{input_name:tensor}})
                record=_record(result,manifest);records.append(record)
                if result['status']=='pending':
                    pending={'frame_id':frame_id,'media_time_ms':pts,'execution_records':records,
                             'stream_epoch':session['stream_epoch'],'reason':result.get('error',{})}
                    save_json(root/'pending-frame.json',pending);status='WAITING_FOR_LINQ';break
                if result['status']!='ok':
                    if result.get('error',{}).get('code')!='linq_service_failed':
                        raise ValueError('model contract/configuration failed; cursor preserved')
                    errors.append(model_id);continue
                if not result.get('execution_witness') or result['execution_witness'].get('completed') is not True:
                    raise ValueError('remote completion witness is required')
                mapping=manifest['linq'].get('output_map',{})
                outputs={mapping.get(name,name):value for name,value in result['outputs'].items()}
                detections.extend(decode(outputs,manifest,transform))
            if pending is not None:break
            for index,detection in enumerate(detections):detection['detection_id']=f'{frame_id}:{index}'
            batch={'schema_version':'1.0','camera_id':args.camera_id,'stream_epoch':session['stream_epoch'],
                'frame_id':frame_id,'media_time_ms':pts,'image_size':[rgb.shape[1],rgb.shape[0]],
                'source_fps':session['source_fps'],'source_sha256':session['source_sha256'],
                'source_kind':session.get('source_kind','real-video'),
                'ingested_at':ingested_at,'request_id':f"{session['stream_epoch']}:{frame_id}",
                'model_id':'+'.join(m['model_id'] for m in manifests),'model_ids':[m['model_id'] for m in manifests],
                'backend':'linq','execution_records':records,'status':'gap' if errors else 'ok',
                'detections':[] if errors else detections}
            if errors:batch['reason']='terminal_model_failure'
            elapsed=(time.monotonic()-observed)*1000;batch['frame_cycle_ms']=elapsed
            mutations=pipeline.process(batch,rgb if not errors else None,
                video_checkpoint=_checkpoint(session,frame_id,pts))
            pipeline.outbox.export_jsonl(root)
            for event in mutations:print(json.dumps(event,allow_nan=False),flush=True)
            processed+=1;failures+=bool(errors);cycles.append(elapsed)
            last_sample=pts;last_batch=batch;last_id=frame_id
            # It is safe to clear only after the frame and event checkpoint COMMIT.
            (root/'pending-frame.json').unlink(missing_ok=True)
        if complete:
            # EOF is a gap, never evidence of compliance. Commit it with completion.
            if last_batch is None:
                row=pipeline.outbox.db.execute('SELECT body FROM observations ORDER BY rowid DESC LIMIT 1').fetchone()
                last_batch=json.loads(row[0]) if row else None
            if last_batch is not None:
                gap={**last_batch,'frame_id':last_batch['frame_id']+1,
                     'media_time_ms':last_batch['media_time_ms']+.001,'status':'gap',
                     'detections':[],'reason':'source_ended'}
                for event in pipeline.process(gap,video_checkpoint=_checkpoint(session,gap['frame_id'],gap['media_time_ms'],complete=True)):
                    print(json.dumps(event,allow_nan=False),flush=True)
            else:
                pipeline.outbox.commit_batch([],pipeline.behavior.export_state(),
                    video_checkpoint=_checkpoint(session,-1,0,complete=True))
    finally:
        pipeline.outbox.export_jsonl(root)
    wall=time.monotonic()-start
    rows=[json.loads(row[0]) for row in pipeline.outbox.db.execute('SELECT body FROM observations ORDER BY rowid')]
    frames=[row for row in rows if row.get('reason')!='source_ended']
    calls=[record['transport_provenance'] for row in frames for record in row.get('execution_records',[])
           if record.get('transport_provenance')]
    latencies=[c['timings']['total_ms'] for c in calls if not c.get('cached_response') and not c.get('reconcile_only') and c.get('timings',{}).get('total_ms') is not None]
    summary={'status':status,'execution_backend':'linq','source_sha256':session['source_sha256'],
        'source_kind':session.get('source_kind','real-video'),
        'source_fps':session['source_fps'],'sample_fps':args.sample_fps,'max_concurrent_requests':1,
        'stream_epoch':session['stream_epoch'],'processed_frames':len(frames),'frames_this_invocation':processed,
        'failed_or_stale_frames':sum(row['status']!='ok' for row in frames),
        'failed_frames_this_invocation':failures,'wall_seconds_this_invocation':wall,
        'committed_frame_processing_ms':sum(row.get('frame_cycle_ms',0) for row in frames),
        'processed_fps_this_invocation':processed/wall if wall else None,
        'frame_cycle_p50_ms':float(np.percentile(cycles,50)) if cycles else None,
        'frame_cycle_p95_ms':float(np.percentile(cycles,95)) if cycles else None,
        'rpc_count_in_committed_frames':len(calls),
        'rpc_p50_ms':float(np.percentile(latencies,50)) if latencies else None,
        'rpc_p95_ms':float(np.percentile(latencies,95)) if latencies else None,
        'real_time_claim':False,'backend_integration':getattr(args,'sink_kind','external') if pipeline.sink else 'not_connected',
        **pipeline.outbox.counts()}
    save_json(root/'summary.json',summary)
    return summary
