"""One allocated native SplitPose feature pass on frozen CAVIAR JPEGs.

Run only AFTER explicit root GPU allocation. No network/TPU/training. The lock is
an additional concurrency guard, not permission to take another worker's slot.
"""
import argparse
from datetime import datetime,timezone
import fcntl
import json
from pathlib import Path
from uuid import uuid4,uuid5,UUID
from ml.quality.handoff import load_producer_ready
from .caviar import DATASET,USE,digest


def preflight(protocol,selected,model_manifest,weights):
    protocol=Path(protocol);p=json.loads(protocol.read_text())
    # Original READY scope is reverified before any pixels or GPU import.
    pointer=next(k for k in p['hashes'] if k.endswith('/READY.json'))
    load_producer_ready(pointer,dataset_id=DATASET,allowed_use=USE)
    for path,h in p['hashes'].items():
        if digest(path)!=h:raise ValueError('frozen reference changed')
    rows=[json.loads(x) for x in Path(selected).read_text().splitlines()]
    if len(rows)!=p['sampled_images'] or len({(r['sequence'],r['frame_id_from_source_filename']) for r in rows})!=len(rows):raise ValueError('sample census changed')
    # Compare actual input list with source annotation rather than trusting an
    # independently replaced selected-inputs file carrying different frames.
    ann=next(k for k in p['hashes'] if k.endswith('/frame_annotations.jsonl'))
    expected={(r['sequence'],r['frame_id_from_source_filename']):r for r in (json.loads(x) for x in Path(ann).read_text().splitlines()) if r['frame_id_from_source_filename']%5==0}
    for r in rows:
        e=expected.get((r['sequence'],r['frame_id_from_source_filename']))
        if e is None or any(r[k]!=e[k] for k in ('path','sha256','bytes','width','height','canonical_frame_time_ms')):raise ValueError('selected input differs from frozen source')
        if Path(r['path']).stat().st_size!=r['bytes'] or digest(r['path'])!=r['sha256']:raise ValueError('source JPEG changed')
    m=json.loads(Path(model_manifest).read_text())
    if m['decoder']!='split_pose_v8' or digest(weights)!=m['artifacts']['weights']['sha256']:raise ValueError('reviewed SplitPose model identity required')
    return p,rows,m


def run(protocol,selected,model_manifest,weights,output,*,device='cuda:0',gpu_lock='/workspace/artifacts/quality/gpu.lock'):
    p,rows,m=preflight(protocol,selected,model_manifest,weights)
    target=Path(output)
    if target.exists():raise ValueError('fresh immutable output required')
    with Path(gpu_lock).open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        import cv2
        import torch
        from ml.detection.codec import preprocess,decode
        from ml.detection.reference import NativeReferenceBackend
        torch.set_num_threads(2);cv2.setNumThreads(1)
        torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
        target.mkdir(parents=True,exist_ok=False);run_id=str(uuid4())
        record={'status':'RUNNING','backend':'pytorch','TPU':'NOT_RUN','run_id':run_id,'device':device,'protocol_sha256':digest(protocol),'selected_inputs_sha256':digest(selected),
            'model_manifest_sha256':digest(model_manifest),'weights_sha256':digest(weights),'preprocessing':m['input'],
            'codec_sha256':digest(Path(__file__).parents[2]/'detection/codec.py'),'runner_sha256':digest(__file__),
            'time_basis':'NOMINAL25FPS_DERIVED frameID*40ms NOT cameraPTS','frame_count':0,'torch_version':torch.__version__}
        def checkpoint():(target/'run.json').write_text(json.dumps(record,indent=2)+'\n')
        checkpoint()
        try:
            backend=NativeReferenceBackend(weights,m,device)
            with (target/'observations.jsonl').open('w') as stream:
                for r in rows:
                    rgb=cv2.cvtColor(cv2.imread(r['path']),cv2.COLOR_BGR2RGB)
                    if list(rgb.shape[:2])!=[r['height'],r['width']]:raise ValueError('source image geometry changed')
                    tensor,transform=preprocess(rgb,m);fid=r['frame_id_from_source_filename'];seq=r['sequence']
                    request=str(uuid5(UUID(run_id),f'{seq}/{fid}'))
                    result=backend.infer({'request_id':request,'model_id':m['model_id'],'inputs':{m['input']['name']:tensor}})
                    batch={'schema_version':'1.0','camera_id':seq,'stream_epoch':run_id+'/'+seq,'frame_id':fid,'media_time_ms':fid*40,
                        'image_size':[r['width'],r['height']],'status':'ok','detections':decode(result['outputs'],m,transform),
                        'backend':'pytorch','model_id':m['model_id'],'request_id':request,'ingested_at':datetime.now(timezone.utc).isoformat()}
                    stream.write(json.dumps({'video_id':seq,'batch':batch,'input_sha256':r['sha256'],'time_provenance':record['time_basis'],'timings_ms':result.get('timings',{})},allow_nan=False)+'\n')
                    record['frame_count']+=1
            record.update(status='COMPLETED',observations_sha256=digest(target/'observations.jsonl'));checkpoint()
        except BaseException as e:
            record.update(status='FAILED',error_type=type(e).__name__);checkpoint();raise
    return record


def main():
    a=argparse.ArgumentParser(description=__doc__)
    for name in ('protocol','selected','model-manifest','weights','output'):a.add_argument('--'+name,required=True)
    a.add_argument('--device',default='cuda:0');x=a.parse_args()
    print(json.dumps(run(x.protocol,x.selected,x.model_manifest,x.weights,x.output,device=x.device)))

if __name__=='__main__':main()
