"""Bounded native E00 on an already frozen development manifest; never test."""
from copy import deepcopy
from datetime import datetime,timezone
import fcntl,hashlib,json,time
from pathlib import Path
import numpy as np
from PIL import Image
from .metrics import evaluate_dataset


def run(dataset_path,model_manifest,weights,output,device='cuda:0',gpu_lock='/workspace/artifacts/quality/gpu.lock',max_seconds=600):
    dataset=json.loads(Path(dataset_path).read_text());manifest=json.loads(Path(model_manifest).read_text())
    if any(i.get('split')!='val' for i in dataset['images']):raise ValueError('E00 runner accepts validation only')
    if len(dataset['images'])>256:raise ValueError('bounded E00 maximum256images')
    for i in dataset['images']:
        if hashlib.sha256(Path(i['path']).read_bytes()).hexdigest()!=i['file_sha256']:raise ValueError('frozen image bytes changed')
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    save=lambda name,value:(output/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    save('frozen-input.json',{'dataset_digest':dataset['dataset_digest'],'dataset_file_sha256':hashlib.sha256(Path(dataset_path).read_bytes()).hexdigest(),
                            'model_manifest_sha256':hashlib.sha256(Path(model_manifest).read_bytes()).hexdigest(),'weights_sha256':hashlib.sha256(Path(weights).read_bytes()).hexdigest(),
                            'timestamp_utc':datetime.now(timezone.utc).isoformat(),'operating_confidence':.25,'raw_score_floor':.001,'scope':'native PyTorch validation only; no LinQ claim'})
    Path(gpu_lock).parent.mkdir(parents=True,exist_ok=True)
    with Path(gpu_lock).open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:
            import torch
            from ml.detection import preprocess,decode,NativeReferenceBackend
            torch.set_num_threads(2);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
            m=deepcopy(manifest);m['thresholds']['confidence']=.001
            backend=NativeReferenceBackend(weights,m,device=device);predictions={};timings=[];start=time.perf_counter();(output/'raw').mkdir()
            for index,image in enumerate(dataset['images']):
                if time.perf_counter()-start>max_seconds:raise TimeoutError('bounded E00 time budget')
                rgb=np.asarray(Image.open(image['path']).convert('RGB'));tensor,transform=preprocess(rgb,m)
                result=backend.infer({'request_id':f'e00-{index:04d}','model_id':m['model_id'],'inputs':{m['input']['name']:tensor}})
                np.savez(output/'raw'/f'{index:04d}.npz',**result['outputs'])
                predictions[image['image_id']]=decode(result['outputs'],m,transform);timings.append(result['timings']['roundtrip_ms'])
            save('predictions.json',predictions)
            primary=evaluate_dataset(dataset,predictions)
            source=deepcopy(dataset)
            for image in source['images']:image['class_coverage']={c:'complete' for c in ['helmet','bare_head']}
            provisional=evaluate_dataset(source,predictions);provisional['status']='PROVISIONAL_SOURCE_LABEL_BENCHMARK';provisional['limitation']='known missing and incorrect source labels; not primary quality; no independent-test claim'
            save('metrics-reviewed.json',primary);save('metrics-source-provisional.json',provisional)
            status={'status':'COMPLETED','execution_backend':'pytorch','device':device,'images':len(predictions),'dataset_digest':dataset['dataset_digest'],
                    'total_seconds':time.perf_counter()-start,'mean_inference_ms':float(np.mean(timings)),'linq_execution':'NOT_RUN_BY_THIS_JOB','final_test':'NOT_RUN'}
            save('run.json',status)
        finally:fcntl.flock(lock,fcntl.LOCK_UN)
    return status


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--dataset',required=True);p.add_argument('--manifest',required=True);p.add_argument('--weights',required=True);p.add_argument('--output',required=True);p.add_argument('--device',default='cuda:0');a=p.parse_args()
    print(json.dumps(run(a.dataset,a.manifest,a.weights,a.output,a.device)))
