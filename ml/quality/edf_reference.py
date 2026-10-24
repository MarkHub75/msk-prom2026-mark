"""Paired EDF source-positive development diagnostic, never exhaustive event GT."""
from datetime import datetime,timezone
import fcntl,json,math,subprocess,time
from pathlib import Path
import numpy as np
from PIL import Image
from ml.quality.handoff import load_producer_ready,sha256

USE='noncommercial research temporal/pose development with UNKNOWN mask outside source positives'
DATASET='edf-native-fall-source3'
VARIANTS=('native_rgb','half_bilinear_restored')


def degrade(rgb):
    """Floor half dimensions (min1), PIL BILINEAR twice, restore original grid."""
    h,w=rgb.shape[:2]
    return np.asarray(Image.fromarray(rgb).resize((max(1,w//2),max(1,h//2)),Image.Resampling.BILINEAR)
                      .resize((w,h),Image.Resampling.BILINEAR))


def project(window,pts):
    # Native one-based inclusive assumption, preserve +/-1 original-frame bounds.
    a,b=window['start_frame']-1,window['end_frame']-1
    if not 0<=a<=b<len(pts): raise ValueError('source interval outside encoded frame clock')
    return {**window,'start_ms':pts[a],'last_ms':pts[b],
            'start_lower_ms':pts[max(0,a-1)],'start_upper_ms':pts[min(len(pts)-1,a+1)],
            'last_lower_ms':pts[max(0,b-1)],'last_upper_ms':pts[min(len(pts)-1,b+1)],
            'origin_policy':'one-based inclusive assumed; +/-1 original frame uncertainty, not exact onset GT'}


def hit_bounds(start,end,window):
    if end<start: raise ValueError('reversed predicted support')
    possible=[]
    for a in (window['start_lower_ms'],window['start_upper_ms']):
        for b in (window['last_lower_ms'],window['last_upper_ms']):
            if b>=a:possible.append(start<=b and end>=a)
    return all(possible),any(possible)


def summarize(observations,mutations,windows):
    events={e['event_id']:e for e in mutations if e['type']=='suspected_fall'}
    records=[]
    for w in windows:
        supported=[];confirmed=[]
        for e in events.values():
            if e['camera_id']!=Path(w['video_path']).stem:continue
            supported.append(hit_bounds(e['start_media_ms'],e['confirmed_media_ms'],w))
            confirmed.append(hit_bounds(e['confirmed_media_ms'],e['confirmed_media_ms'],w))
        records.append({'video_id':Path(w['video_path']).stem,'native_event_ordinal':w['native_event_ordinal'],
             'support_hit_lower':any(x[0] for x in supported),'support_hit_upper':any(x[1] for x in supported),
             'confirmation_hit_lower':any(x[0] for x in confirmed),'confirmation_hit_upper':any(x[1] for x in confirmed),
             'possible_duplicate_additional_episodes':max(0,sum(x[1] for x in supported)-1)})
    count=len(records);persons=sum(o['eligible_persons'] for o in observations);unknown=sum(o['unknown_postures'] for o in observations)
    return {'scope':'SOURCE_POSITIVE_WINDOW_HIT_COVERAGE_NOT_INDEPENDENT_EVENT_RECALL',
        'sampled_frames':len(observations),'frames_with_eligible_person':sum(o['eligible_persons']>0 for o in observations),
        'eligible_person_detections':persons,'full_visible_torso_detections':sum(o['full_torsos'] for o in observations),
        'torso_available_fraction_of_eligible_detections':sum(o['full_torsos'] for o in observations)/persons if persons else None,
        'posture_unknown_rate_of_eligible_detections':unknown/persons if persons else None,
        'no_eligible_person_frame_fraction':sum(o['eligible_persons']==0 for o in observations)/len(observations) if observations else None,
        'source_positive_windows':count,'support_hit_coverage_lower':sum(x['support_hit_lower'] for x in records)/count,
        'support_hit_coverage_upper':sum(x['support_hit_upper'] for x in records)/count,
        'confirmation_hit_coverage_lower':sum(x['confirmation_hit_lower'] for x in records)/count,
        'confirmation_hit_coverage_upper':sum(x['confirmation_hit_upper'] for x in records)/count,
        'possible_duplicate_additional_episodes':sum(x['possible_duplicate_additional_episodes'] for x in records),
        'unique_suspected_fall_episodes':len(events),'per_window':records,
        'precision':'NOT_MEASURABLE','f1':'NOT_MEASURABLE','false_alerts_per_hour':'NOT_MEASURABLE',
        'prolonged_lying_source_mapping':'NOT_MEASURABLE; source fall-process windows are not lying/immobility GT',
        'outside_source_windows':'UNKNOWN, never negative','person_detection_recall':'NOT_MEASURABLE; no person GT'}


def prepare(pointer,output):
    manifest,verification=load_producer_ready(pointer,dataset_id=DATASET,allowed_use=USE)
    root=Path(manifest['absolute_path']);out=Path(output);out.mkdir(parents=True,exist_ok=False)
    classmap=json.loads((root/'class_map.json').read_text())
    if classmap['outside_source_windows']!='UNKNOWN' or classmap['canonical_event_mapping'] is not None:
        raise ValueError('source semantics changed')
    windows=json.loads((root/'source_temporal_manifest.json').read_text());videos=[];projected=[]
    for asset in manifest['assets']:
        if asset['role']!='original_RGB_video':continue
        raw=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
            '-show_frames','-show_streams','-show_entries','frame=best_effort_timestamp,best_effort_timestamp_time:stream=width,height,time_base,r_frame_rate',
            '-of','json',asset['path']],text=True))
        frames=raw['frames'];pts=[float(f['best_effort_timestamp_time'])*1000 for f in frames]
        if not pts or any(b<=a for a,b in zip(pts,pts[1:])):raise ValueError('encoded PTS not strictly increasing')
        selected=list(range(0,len(pts),5));stream=raw['streams'][0]
        videos.append({'video_id':asset['asset_id'],'path':asset['path'],'sha256':asset['sha256'],
            'width':stream['width'],'height':stream['height'],'time_base':stream['time_base'],'r_frame_rate':stream['r_frame_rate'],
            'frames':len(pts),'encoded_pts_ms':pts,'encoded_pts_ticks':[f['best_effort_timestamp'] for f in frames],
            'selected_zero_based_indices':selected})
        projected.extend(project(w,pts) for w in windows if w['video_path']==asset['path'])
    if len(videos)!=3 or sum(v['frames'] for v in videos)!=12917 or len(projected)!=24:raise ValueError('EDF census changed')
    from ml.behavior.engine import DEFAULTS
    protocol={'dataset':DATASET,'created_utc':datetime.now(timezone.utc).isoformat(),'producer_verification':verification,
        'producer_manifest':manifest,'class_map':classmap,'videos':videos,'windows':projected,
        'sample_policy':'indices0,5,10,...; encoded presentation PTS, no wall-clock substitution',
        'variants':list(VARIANTS),'transform':'PIL BILINEAR to floor(W/2),floor(H/2) then BILINEAR to original W,H; before identical640 preprocess',
        'behavior_defaults':DEFAULTS,'scope':'staged air-mattress source-positive development, not industrial floor or exhaustive event GT',
        'metric_policy':'suspected_fall only; support[start,confirmed] and confirmation-point overlap, all/any +/-1-frame endpoint alternatives; no matching of prolonged_lying to falls',
        'max_seconds':900,'gpu_threads':2,'tf32':False}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2,allow_nan=False)+'\n')
    return protocol


def run(pointer,output,model_manifest,weights):
    # Reverify producer bytes and use BEFORE decoding any pixels/model forward.
    load_producer_ready(pointer,dataset_id=DATASET,allowed_use=USE)
    out=Path(output);protocol=json.loads((out/'protocol.json').read_text())
    manifest=json.loads(Path(model_manifest).read_text())
    if manifest['decoder']!='split_pose_v8' or sha256(weights)!=manifest['artifacts']['weights']['sha256']:
        raise ValueError('same trusted split-pose checkpoint required')
    if manifest['artifacts']['weights']['sha256']!='c6fa93dd1ee4a2c18c900a45c1d864a1c6f7aba75d84f91648a30b7fb641d212':raise ValueError('weights changed')
    import cv2,torch
    from ml.detection import NativeReferenceBackend,preprocess,decode
    from ml.behavior import BehaviorEngine
    cv2.setNumThreads(2);torch.set_num_threads(2);torch.backends.cuda.matmul.allow_tf32=False
    torch.backends.cudnn.allow_tf32=False;torch.backends.cudnn.benchmark=False
    if not torch.cuda.is_available():raise RuntimeError('allocated GPU required; no fallback')
    lock=Path('/workspace/artifacts/quality/gpu.lock');lock.parent.mkdir(parents=True,exist_ok=True)
    with lock.open('a') as stream:
        fcntl.flock(stream,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:
            utilization=subprocess.check_output(['nvidia-smi','--query-gpu=utilization.gpu,memory.used','--format=csv,noheader,nounits'],text=True).strip()
            if any(int(line.split(',')[0])>5 or int(line.split(',')[1])>256 for line in utilization.splitlines()):raise RuntimeError('GPU already occupied; coordinate before starting')
            start=time.perf_counter();backend=NativeReferenceBackend(weights,manifest,device='cuda:0');reports={}
            (out/'model-identity.json').write_text(json.dumps({'manifest_sha256':sha256(model_manifest),'weights_sha256':sha256(weights),'protocol_sha256':sha256(out/'protocol.json'),'execution':'NATIVE_CUDA_NOT_LINQ','gpu_before':utilization},indent=2))
            for variant in VARIANTS:
                dest=out/variant;dest.mkdir(exist_ok=False);engine=BehaviorEngine();observations=[];mutations=[];timings=[]
                with (dest/'observations.jsonl').open('x') as obsfile,(dest/'event-mutations.jsonl').open('x') as eventfile:
                    for video in protocol['videos']:
                        cap=cv2.VideoCapture(video['path']);index=0;selected=set(video['selected_zero_based_indices'])
                        while True:
                            ok,bgr=cap.read()
                            if not ok:break
                            if time.perf_counter()-start>900:raise TimeoutError('paired allocation900s expired')
                            if index>=video['frames']:raise ValueError('decoded more frames than pinned clock')
                            if abs(cap.get(cv2.CAP_PROP_POS_MSEC)-video['encoded_pts_ms'][index])>2:raise ValueError('decoder index/PTS disagreement')
                            if index in selected:
                                rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
                                if variant==VARIANTS[1]:rgb=degrade(rgb)
                                before=time.perf_counter();tensor,transform=preprocess(rgb,manifest)
                                result=backend.infer({'request_id':f'{variant}-{video["video_id"]}-{index}','model_id':manifest['model_id'],'inputs':{manifest['input']['name']:tensor}})
                                detections=decode(result['outputs'],manifest,transform);elapsed=time.perf_counter()-before;timings.append(elapsed)
                                batch={'schema_version':'1.0','camera_id':video['video_id'],'stream_epoch':f'edf-{variant}','frame_id':index,
                                    'media_time_ms':video['encoded_pts_ms'][index],'image_size':[video['width'],video['height']],
                                    'request_id':f'edf-{variant}-{video["video_id"]}-{index}','model_id':manifest['model_id'],'backend':'pytorch','status':'ok','detections':detections}
                                people=[p for p in detections if p['class_name']=='person' and p['score']>=engine.config['min_score']]
                                full=0
                                for p in people:
                                    k=p['keypoints']
                                    if all(k[i][2]>=engine.config['keypoint_score'] for i in (5,6,11,12)):
                                        a=[(k[5][j]+k[6][j])/2 for j in (0,1)];b=[(k[11][j]+k[12][j])/2 for j in (0,1)]
                                        full+=math.hypot(a[0]-b[0],a[1]-b[1])>=engine.config['min_torso_px']
                                row={'video_id':video['video_id'],'source_frame_index':index,'source_pts_ms':batch['media_time_ms'],
                                     'eligible_persons':len(people),'full_torsos':int(full),'unknown_postures':sum(engine._posture(p)=='unknown' for p in people),'batch':batch}
                                obsfile.write(json.dumps(row,allow_nan=False)+'\n');observations.append(row)
                                events=engine.update(batch)
                                for e in events:eventfile.write(json.dumps(e,allow_nan=False)+'\n')
                                mutations.extend(events)
                            index+=1
                        cap.release()
                        if index!=video['frames']:raise ValueError('decoded frame census differs')
                        print(f'{variant} {video["video_id"]} completed',flush=True)
                metrics=summarize(observations,mutations,protocol['windows']);metrics['timings']={'frames':len(timings),'mean_seconds':float(np.mean(timings)),'p95_seconds':float(np.percentile(timings,95))}
                (dest/'metrics.json').write_text(json.dumps(metrics,indent=2,allow_nan=False)+'\n');reports[variant]=metrics
            result={'status':'COMPLETED','execution':'NATIVE_CUDA_NOT_LINQ','total_seconds':time.perf_counter()-start,'variants':reports,'final_test':'NOT_RUN'}
            (out/'summary.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
            return result
        finally:fcntl.flock(stream,fcntl.LOCK_UN)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','run']);p.add_argument('--ready',required=True);p.add_argument('--output',required=True);p.add_argument('--manifest');p.add_argument('--weights');a=p.parse_args()
    result=prepare(a.ready,a.output) if a.stage=='prepare' else run(a.ready,a.output,a.manifest,a.weights)
    print(json.dumps({'status':result.get('status','PREPARED')}))
