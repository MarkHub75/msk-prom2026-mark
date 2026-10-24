"""E012 one fixed CPU-only four-tile pose diagnostic; no model promotion."""
from collections import Counter
from dataclasses import asdict
import hashlib,json,time
from pathlib import Path
import numpy as np
from ml.quality.handoff import load_producer_ready,sha256
from ml.quality.temporal.caviar import DATASET,USE,associate,_label
from ml.detection.codec import preprocess,_nms


def tiles(width,height):
    """Round60% dimensions via floor(x+.5); clamp; starts0 or dimension-size."""
    cw=max(1,min(width,int(width*.6+.5)));ch=max(1,min(height,int(height*.6+.5)))
    return [(x,y,x+cw,y+ch) for y in (0,height-ch) for x in (0,width-cw)]


def proposals(outputs,manifest,transform,offset):
    """Only restore decoded layout/geometry; do not NMS or repeat neural math."""
    names=manifest['split_outputs'];nc=len(manifest['classes']);count=manifest.get('keypoint_count',17)
    boxes=np.asarray(outputs[names['boxes']]);scores=np.asarray(outputs[names['class_scores']]);xy=np.asarray(outputs[names['keypoint_xy']]);confidence=np.asarray(outputs[names['keypoint_scores']])
    if boxes.ndim!=3 or boxes.shape[:2]!=(1,4):raise ValueError('box ABI mismatch')
    n=boxes.shape[-1]
    if scores.shape!=(1,nc,n) or xy.shape!=(1,count,2,n) or confidence.shape!=(1,count,1,n):raise ValueError('split pose ABI mismatch')
    if any(v.dtype.kind!='f' or not np.isfinite(v).all() for v in (boxes,scores,xy,confidence)):raise ValueError('nonfinite/nonfloating pose output')
    if any(((v<0)|(v>1)).any() for v in (scores,confidence)):raise ValueError('probabilities required')
    pts=np.concatenate((xy,confidence),axis=2)[0].transpose(2,0,1);rows=boxes[0].T;classes=np.argmax(scores[0],axis=0);values=scores[0,classes,np.arange(n)]
    result=[]
    for i in np.flatnonzero((values>=.25)&(rows[:,2]>0)&(rows[:,3]>0)):
        box=np.r_[rows[i,:2]-rows[i,2:]/2,rows[i,:2]+rows[i,2:]/2]
        box=transform.points(box.reshape(2,2)).reshape(4)
        if box[2]<=box[0] or box[3]<=box[1]:continue
        box[[0,2]]+=offset[0];box[[1,3]]+=offset[1]
        kp=pts[i].astype(np.float64).copy();kp[:,:2]=transform.points(kp[:,:2]);kp[:,0]+=offset[0];kp[:,1]+=offset[1]
        result.append({'class_name':manifest['classes'][int(classes[i])],'score':float(values[i]),'bbox_xyxy':box.tolist(),'keypoints':kp.tolist()})
    return result


def global_nms(detections):
    if not detections:return []
    classes=sorted({d['class_name'] for d in detections});ids=np.asarray([classes.index(d['class_name']) for d in detections])
    kept=_nms(np.asarray([d['bbox_xyxy'] for d in detections]),np.asarray([d['score'] for d in detections]),ids,.45,300)
    return [dict(detections[i],detection_id=f'd{j}') for j,i in enumerate(kept)]


def observation_metrics(refs,observations):
    indexed={}
    for item in observations:
        b=item['batch'];key=(item.get('video_id',b['camera_id']),b['frame_id'])
        if key in indexed or key not in refs:raise ValueError('duplicate/unexpected observation')
        indexed[key]=item
    if set(indexed)!=set(refs):raise ValueError('incomplete345 sample cannot be scored as full')
    counters=Counter();details=[]
    for key,ref in refs.items():
        item=indexed[key];b=item['batch']
        if b['status']!='ok' or b['image_size']!=[ref['width'],ref['height']] or b['media_time_ms']!=ref['canonical_frame_time_ms'] or item['input_sha256']!=ref['sha256']:raise ValueError('source binding differs')
        persons=[d for d in b['detections'] if d['class_name']=='person' and d['score']>=.5]
        matches=associate(ref['source_objects'],persons)
        counters['unassigned_observed_persons_unknown']+=len(persons)-len(matches)
        for i,obj in enumerate(ref['source_objects']):
            label=_label(obj)
            if label not in ('running','walking'):
                counters['source_actor_frames_excluded_unknown_other']+=1;continue
            box=obj['bbox_xyxy_original'];w,h=ref['width'],ref['height'];oob=not (0<=box[0]<box[2]<=w and 0<=box[1]<box[3]<=h)
            strata=['all','out_of_bounds' if oob else 'in_bounds'];matched=i in matches
            for s in strata:counters[f'{label}:{s}:total']+=1;counters[f'{label}:{s}:matched']+=matched
            details.append({'source':key[0],'frame_id':key[1],'source_actor':obj['track_id'],'movement':label,'source_box':box,'out_of_bounds_gt':oob,'consumer_unique_match':matched,'matched_detection':persons[matches[i]] if matched else None})
    result={'counts':dict(counters),'actor_frames':details,'sampled_frames':len(indexed),'scope':'unique bidirectional IoU>=.5 for literal visible running/walking actors; consumer>=.5; other/unboxed unknown, no precision or event quality'}
    for label in ('running','walking'):
        result[label]={s:{'matched':int(counters[f'{label}:{s}:matched']),'total':int(counters[f'{label}:{s}:total']),
             'recall':counters[f'{label}:{s}:matched']/counters[f'{label}:{s}:total'] if counters[f'{label}:{s}:total'] else None} for s in ('all','in_bounds','out_of_bounds')}
    return result


def prepare(pointer,legacy_protocol,selected,baseline,baseline_run,model_manifest,weights,output):
    release,verified=load_producer_ready(pointer,dataset_id=DATASET,allowed_use=USE)
    p=json.loads(Path(legacy_protocol).read_text());run=json.loads(Path(baseline_run).read_text());m=json.loads(Path(model_manifest).read_text())
    for path,digest in p['hashes'].items():
        if not path.endswith('/READY.json') and sha256(path)!=digest:raise ValueError('frozen source changed')
    if p['hashes'].get(str(Path(release['absolute_path'])/'manifest.json'))!=verified['manifest_sha256']:raise ValueError('producer release differs from E003')
    if run['status']!='COMPLETED' or run['observations_sha256']!=sha256(baseline) or run['selected_inputs_sha256']!=sha256(selected) or run['protocol_sha256']!=sha256(legacy_protocol):raise ValueError('saved baseline changed')
    if run['model_manifest_sha256']!=sha256(model_manifest) or run['weights_sha256']!=sha256(weights):raise ValueError('same model identity required')
    if m['decoder']!='split_pose_v8' or m['thresholds']!={'confidence':.25,'iou':.45,'max_detections':300}:raise ValueError('fixed ABI/thresholds required')
    annotations=Path(release['absolute_path'])/'frame_annotations.jsonl';allrefs={(r['sequence'],r['frame_id_from_source_filename']):r for r in map(json.loads,annotations.read_text().splitlines())}
    rows=list(map(json.loads,Path(selected).read_text().splitlines()));refs={}
    for r in rows:
        key=(r['sequence'],r['frame_id_from_source_filename']);source=allrefs[key]
        if key in refs or key[1]%5 or any(r[k]!=source[k] for k in ('path','sha256','bytes','width','height','canonical_frame_time_ms')) or sha256(r['path'])!=r['sha256']:raise ValueError('source selected binding changed')
        refs[key]=source
    if len(refs)!=345:raise ValueError('full frozen345 required')
    baseline_metrics=observation_metrics(refs,list(map(json.loads,Path(baseline).read_text().splitlines())))
    out=Path(output);out.mkdir(parents=True,exist_ok=False)
    record={'experiment':'E012','status':'FROZEN_BEFORE_FORWARD','producer_verification':verified,'legacy_READY_catalog_hash':{k:v for k,v in p['hashes'].items() if k.endswith('/READY.json')},
       'hashes':{str(x):sha256(x) for x in (legacy_protocol,selected,baseline,baseline_run,model_manifest,weights,annotations)},
       'sampled_frames':345,'selection':'SAME E003 source_frame_id%5=0; no GT-adaptive ROI','source_time':'frameID*40ms nominal25FPS DERIVED, not camera PTS',
       'tile_policy':'four60% dimensions floor(dim*.6+.5), cornerstarts0 or dim-cropdim, stable row-major; no full-frame pass',
       'decode':'no per-cropNMS; decoded boxes/keypoints inverseletterbox+offset; one global class-aware original-coordinate NMS.45/max300',
       'archive_policy':'all1380 crops bound by originalJPEGsha,cropRGBsha,modeltensorSHA,transform,translatedproposals; losslessrawRGBNPZ onlyfirst20 deterministiccropcalls, no full640floatNPZ',
       'decoder_confidence':.25,'consumer_score':.5,'threads':2,'opencv_threads':1,'device':'cpu','maximum_wall_seconds':600,
       'acceptance':{'running_unique_match_recall_gain_min':.10,'walking_unique_match_recall_drop_max':.02,'walking_unique_match_count_min':baseline_metrics['walking']['all']['matched']},
       'baseline_device':run['device'],'candidate_device':'cpu','precision_runtime_limit':'baseline saved CUDA versus candidateCPU float reference; no additional wholeframecontrol authorized',
       'baseline_metrics':baseline_metrics,'tile_bounds_by_size':{f'{r["width"]}x{r["height"]}':tiles(r['width'],r['height']) for r in rows},
       'limits':['partial actorGT, unboxed/unknown excluded; no FP precision/fullrunningevent quality','out-of-bounds sourceGT stratified without clipping/GT repair','no promotion/industrialquality/actualLinQ claim','only1boundedhypothesis; no threshold/weights/ROI variants']}
    (out/'protocol.json').write_text(json.dumps(record,indent=2)+'\n')
    return rows,refs,m,record


def run(pointer,legacy_protocol,selected,baseline,baseline_run,model_manifest,weights,output):
    start=time.perf_counter();rows,refs,m,p=prepare(pointer,legacy_protocol,selected,baseline,baseline_run,model_manifest,weights,output)
    out=Path(output);(out/'crop-inputs').mkdir()
    import cv2,torch
    from ml.detection.reference import NativeReferenceBackend
    torch.set_num_threads(2);torch.set_num_interop_threads(2);cv2.setNumThreads(1)
    backend=NativeReferenceBackend(weights,m,device='cpu');observations=[];timings=[];count=0
    status={'status':'RUNNING','device':'cpu','frames_completed':0,'NN_calls':0,'protocol_sha256':sha256(out/'protocol.json')}
    save=lambda:(out/'run.json').write_text(json.dumps(status,indent=2)+'\n')
    save()
    try:
        with (out/'observations.jsonl').open('x') as obsfile,(out/'crop-records.jsonl').open('x') as cropfile:
            for index,r in enumerate(rows):
                if time.perf_counter()-start>600:raise TimeoutError('600s bounded CPU allocation expired')
                rgb=cv2.cvtColor(cv2.imread(r['path']),cv2.COLOR_BGR2RGB);allproposals=[];before=time.perf_counter()
                for tile_id,bounds in enumerate(tiles(r['width'],r['height'])):
                    if time.perf_counter()-start>600:raise TimeoutError('600s bounded CPU allocation expired')
                    x,y,a,b=bounds;crop=np.ascontiguousarray(rgb[y:b,x:a]);tensor,t=preprocess(crop,m)
                    path=out/'crop-inputs'/f'{index:04d}-{tile_id}.npz' if index*4+tile_id<20 else None
                    if path is not None:np.savez_compressed(path,rgb=crop)
                    result=backend.infer({'model_id':m['model_id'],'request_id':f'E012-{index}-{tile_id}','inputs':{m['input']['name']:tensor}});status['NN_calls']+=1
                    candidates=proposals(result['outputs'],m,t,(x,y));allproposals.extend(candidates)
                    cropfile.write(json.dumps({'source':r['sequence'],'frame_id':r['frame_id_from_source_filename'],'source_sha256':r['sha256'],'tile_id':tile_id,'crop_xyxy_original':bounds,'raw_rgb_npz':str(path) if path else None,'raw_rgb_npz_sha256':sha256(path) if path else None,'raw_rgb_sha256':hashlib.sha256(crop.tobytes()).hexdigest(),'model_tensor_sha256':hashlib.sha256(tensor.tobytes()).hexdigest(),'letterbox_transform':asdict(t),'translated_pre_nms_proposals':candidates},allow_nan=False)+'\n')
                detections=global_nms(allproposals);fid=r['frame_id_from_source_filename'];seq=r['sequence']
                batch={'schema_version':'1.0','camera_id':seq,'stream_epoch':'E012-person-roi-v1/'+seq,'frame_id':fid,'media_time_ms':r['canonical_frame_time_ms'],'image_size':[r['width'],r['height']],'status':'ok','detections':detections,'backend':'pytorch','model_id':m['model_id'],'request_id':f'E012-{index}'}
                item={'video_id':seq,'batch':batch,'input_sha256':r['sha256'],'time_provenance':p['source_time']};observations.append(item);obsfile.write(json.dumps(item,allow_nan=False)+'\n');timings.append(time.perf_counter()-before);count+=1;status['frames_completed']=count
                if count%25==0:save();print(f'completed {count}/345',flush=True)
        actual=observation_metrics(refs,observations);base=p['baseline_metrics'];running_gain=actual['running']['all']['recall']-base['running']['all']['recall'];walking_drop=base['walking']['all']['recall']-actual['walking']['all']['recall'];walking_count_ok=actual['walking']['all']['matched']>=p['acceptance']['walking_unique_match_count_min']
        report={'status':'COMPLETED_FULL345','scope':'PARTIAL_SOURCE_ACTOR_OBSERVATION_DIAGNOSTIC_NOT_EVENTQUALITY','candidate':actual,'baseline':base,'running_recall_gain':running_gain,'walking_recall_drop':walking_drop,'walking_count_guard':walking_count_ok,'predeclared_gate_pass':running_gain>=.10 and walking_drop<=.02 and walking_count_ok,'promotion':'NOT_GRANTED; independent/fullGT/LinQ gates remain','precision':'NOT_MEASURABLE','false_alerts_per_hour':'NOT_MEASURABLE','timing':{'total_seconds':time.perf_counter()-start,'mean_four_tile_frame_seconds':float(np.mean(timings)),'NN_calls':status['NN_calls']}}
        (out/'comparison.json').write_text(json.dumps(report,indent=2)+'\n');status.update(status='COMPLETED_FULL345',total_seconds=time.perf_counter()-start,observations_sha256=sha256(out/'observations.jsonl'));save();return report
    except BaseException as error:
        status.update(status='INCOMPLETE_NOT_SCORED_AS_FULL',error_type=type(error).__name__,seconds=time.perf_counter()-start);save();raise

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    for k in ('pointer','legacy-protocol','selected','baseline','baseline-run','model-manifest','weights','output'):parser.add_argument('--'+k,required=True)
    a=parser.parse_args();result=run(a.pointer,a.legacy_protocol,a.selected,a.baseline,a.baseline_run,a.model_manifest,a.weights,a.output)
    print(json.dumps({k:v for k,v in result.items() if k not in ('candidate','baseline')}))
