"""Final fixed 2x2 overlapping-tile hypothesis; no GT-adaptive ROI or model change."""
from copy import deepcopy
from datetime import datetime, timezone
import fcntl,hashlib,json,time
from pathlib import Path
import numpy as np
from ml.detection import preprocess,decode,NativeReferenceBackend
from ml.detection.codec import _nms
from .metrics import evaluate_dataset

POLICY={"policy_id":"helmet-tiles60-v1","tiles_only":True,"tile_count":4,
        "tile_fraction":.6,"start_fraction":.4,"rounding":"nearest integer using (3*d+2)//5 and (2*d+2)//5",
        "operating_confidence":.25,"raw_score_floor":.001,"global_nms_iou":.45,"global_max_detections":300,
        "tile_local_suppression":"disabled: IoU1.0 and anchor-count cap; one effective NMS after original-coordinate restoration"}


def tile_bounds(width,height):
    if type(width) is not int or type(height) is not int or min(width,height)<2:raise ValueError('image dimensions must be integers >=2')
    tw,th=(3*width+2)//5,(3*height+2)//5
    x,y=(2*width+2)//5,(2*height+2)//5
    return [(xx,yy,xx+tw,yy+th) for yy in (0,y) for xx in (0,x)]


def merge_tile_detections(tiles,image_size,classes=('helmet','bare_head'),score_floor=.001,iou=.45,max_detections=300):
    """Restore source pixels then apply the existing class-aware NMS globally."""
    width,height=image_size;all_detections=[]
    for bounds,detections in tiles:
        x,y,x2,y2=bounds
        if not (0<=x<x2<=width and 0<=y<y2<=height):raise ValueError('tile bounds outside source image')
        for detection in detections:
            item=deepcopy(detection);box=np.asarray(item['bbox_xyxy'],float)
            if box.shape!=(4,) or not np.isfinite(box).all() or not (0<=box[0]<box[2]<=x2-x and 0<=box[1]<box[3]<=y2-y):raise ValueError('invalid tile-local box')
            if item['class_name'] not in classes or not np.isfinite(item['score']) or not 0<=item['score']<=1:raise ValueError('invalid helmet detection')
            if item.get('keypoints') is not None:raise ValueError('helmet policy does not transform pose keypoints')
            if item['score']<score_floor:continue
            item['bbox_xyxy']=(box+np.array([x,y,x,y])).tolist();all_detections.append(item)
    if not all_detections:return []
    boxes=np.array([i['bbox_xyxy'] for i in all_detections]);scores=np.array([i['score'] for i in all_detections]);indices=np.array([classes.index(i['class_name']) for i in all_detections])
    keep=_nms(boxes,scores,indices,iou,max_detections);results=[all_detections[i] for i in keep]
    for index,item in enumerate(results):item['detection_id']=f'd{index}'
    return results


def infer_tiled(frame,manifest,backend,request_prefix='tiles',raw_directory=None):
    if manifest.get('decoder')!='detect_v8' or manifest.get('classes')!=['helmet','bare_head']:raise ValueError('fixed hypothesis requires existing helmet-v1 ABI')
    started=time.perf_counter();height,width=frame.shape[:2];parts=[];record=[];nn_ms=prep_ms=decode_ms=0.
    local=deepcopy(manifest);local['thresholds']={'confidence':.001,'iou':1.,'max_detections':8400}
    for index,bounds in enumerate(tile_bounds(width,height)):
        x,y,x2,y2=bounds;prep_start=time.perf_counter();tensor,transform=preprocess(frame[y:y2,x:x2],local);prep_ms+=(time.perf_counter()-prep_start)*1000
        call_start=time.perf_counter();result=backend.infer({'request_id':f'{request_prefix}-{index}','model_id':manifest['model_id'],'inputs':{manifest['input']['name']:tensor}});nn_ms+=(time.perf_counter()-call_start)*1000
        if result.get('status')!='ok':raise ValueError('tile inference failed, no local fallback')
        decoded_start=time.perf_counter();detections=decode(result['outputs'],local,transform);decode_ms+=(time.perf_counter()-decoded_start)*1000
        parts.append((bounds,detections));record.append({'tile_index':index,'bounds_xyxy':list(bounds),'decoded_candidates_before_global_nms':len(detections)})
        if raw_directory is not None:np.savez(Path(raw_directory)/f'{request_prefix}-tile{index}.npz',**result['outputs'])
    nms_start=time.perf_counter();merged=merge_tile_detections(parts,(width,height));global_ms=(time.perf_counter()-nms_start)*1000
    return merged,{'preprocess_ms':prep_ms,'four_nn_calls_ms':nn_ms,'tile_decode_ms':decode_ms,'global_nms_ms':global_ms,'frame_total_ms':(time.perf_counter()-started)*1000},record


def _macro_f1(metrics):
    values=[c['f1'] for c in metrics['classes'].values() if c['f1'] is not None]
    return sum(values)/len(values) if values else None


def compare_policy(dataset,baseline,candidate):
    b=evaluate_dataset(dataset,baseline,confidence=.25);c=evaluate_dataset(dataset,candidate,confidence=.25)
    b['macro_f1'],c['macro_f1']=_macro_f1(b),_macro_f1(c)
    guards={name:{'baseline_recall':value['recall'],'candidate_recall':c['classes'][name]['recall'],
                 'recall_delta':c['classes'][name]['recall']-value['recall'],
                 'pass':c['classes'][name]['recall']+1e-12>=value['recall']-.02} for name,value in b['classes'].items() if value['recall'] is not None}
    improved=c['macro_f1'] is not None and b['macro_f1'] is not None and c['macro_f1']>b['macro_f1']
    return {'baseline':b,'candidate':c,'macro_f1_increased':improved,'recall_guards':guards,
            'status':'VALIDATION_GATE_PASS_REQUIRES_LINQ_AND_SEALED_TEST' if improved and all(v['pass'] for v in guards.values()) else 'REJECTED_VALIDATION',
            'independent_test':'NOT_RUN','linq_tile_gate':'NOT_RUN','policy':POLICY,'hypothesis_budget':'final Helmet hypothesis; stop/freeze regardless'}


def run(dataset_path,model_manifest,weights,baseline_predictions,output,device='cuda:0',gpu_lock='/workspace/artifacts/quality/gpu.lock',max_seconds=600):
    dataset=json.loads(Path(dataset_path).read_text());manifest=json.loads(Path(model_manifest).read_text());baseline=json.loads(Path(baseline_predictions).read_text())
    if len(dataset['images'])!=52 or any(i.get('split')!='val' for i in dataset['images']):raise ValueError('hypothesis fixed to the52 validation samples')
    if set(baseline)!={i['image_id'] for i in dataset['images']}:raise ValueError('baseline/sample identity mismatch')
    for image in dataset['images']:
        if hashlib.sha256(Path(image['path']).read_bytes()).hexdigest()!=image['file_sha256']:raise ValueError('frozen image bytes changed')
    output=Path(output);output.mkdir(parents=True,exist_ok=False);(output/'raw').mkdir()
    save=lambda name,value:(output/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    save('frozen-input.json',{'dataset_digest':dataset['dataset_digest'],'dataset_file_sha256':hashlib.sha256(Path(dataset_path).read_bytes()).hexdigest(),
                            'weights_sha256':hashlib.sha256(Path(weights).read_bytes()).hexdigest(),'model_manifest_sha256':hashlib.sha256(Path(model_manifest).read_bytes()).hexdigest(),
                            'baseline_predictions_sha256':hashlib.sha256(Path(baseline_predictions).read_bytes()).hexdigest(),'policy':POLICY,
                            'created_at':datetime.now(timezone.utc).isoformat(),'scope':'native PyTorch hypothesis only; not TPU or target acceptance'})
    predictions={};timings=[];tile_metadata=[]
    with Path(gpu_lock).open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:
            import torch
            from PIL import Image
            torch.set_num_threads(2);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
            backend=NativeReferenceBackend(weights,manifest,device=device);start=time.perf_counter()
            for index,image in enumerate(dataset['images']):
                if time.perf_counter()-start>max_seconds:raise TimeoutError('tile hypothesis time budget')
                frame=np.asarray(Image.open(image['path']).convert('RGB'))
                detections,latency,bounds=infer_tiled(frame,manifest,backend,request_prefix=f'image{index:03d}',raw_directory=output/'raw')
                predictions[image['image_id']]=detections;timings.append(latency);tile_metadata.append({'image_id':image['image_id'],'tiles':bounds,'latency':latency})
            inference_seconds=time.perf_counter()-start
        finally:fcntl.flock(lock,fcntl.LOCK_UN)
    save('predictions.json',predictions);save('tile-metadata.json',tile_metadata)
    comparison=compare_policy(dataset,baseline,predictions);comparison['dataset_digest']=dataset['dataset_digest']
    comparison['latency_native']={key:{'mean':float(np.mean([t[key] for t in timings])),'p95':float(np.percentile([t[key] for t in timings],95))} for key in timings[0]}
    comparison['latency_scope']='native four calls plus preparation/decode/NMS; frame_total also includes diagnostic NPZ writes, excludes image loading and model initialization'
    comparison['inference_seconds']=inference_seconds;comparison['calls']=len(dataset['images'])*4
    save('comparison.json',comparison)
    save('run.json',{'status':'COMPLETED','execution_backend':'pytorch','images':52,'nn_calls':208,'dataset_digest':dataset['dataset_digest'],'linq':'NOT_RUN','test':'NOT_RUN','validation_gate':comparison['status']})
    return {'status':comparison['status'],'baseline_macro_f1':comparison['baseline']['macro_f1'],'candidate_macro_f1':comparison['candidate']['macro_f1'],'recall_guards':comparison['recall_guards'],'latency_native':comparison['latency_native']}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--dataset',required=True);p.add_argument('--manifest',required=True);p.add_argument('--weights',required=True);p.add_argument('--baseline-predictions',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    print(json.dumps(run(a.dataset,a.manifest,a.weights,a.baseline_predictions,a.output)))
