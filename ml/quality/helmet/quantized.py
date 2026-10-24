"""Frozen Helmet CPU quantized-reference experiment; never actual TPU execution."""
from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path
import time
import numpy as np
from PIL import Image
from ml.quality.handoff import load_ready, sha256
from .metrics import evaluate_dataset

READY_SHA='5f30081065e69e9316e96b972353267caaae868212194b312ddc8ceae065f74b'
ONNX_SHA='b312701494991ff7ecc82cb86cc71a8a145a871f6ff342908bb5137e1e8caa47'


def verified_inputs(ready):
    if sha256(ready)!=READY_SHA: raise ValueError('READY identity changed')
    _, quality=load_ready(ready,dataset_id='helmet-quality-v3-52',capability='detection_quality')
    _, calibration=load_ready(ready,dataset_id='mendeley8-calibration-v1',capability='calibration')
    dataset=json.loads(Path(quality['manifest_path']).read_text())
    if len(dataset['images'])!=52 or dataset['dataset_digest']!=quality['dataset_semantic_digest']:
        raise ValueError('frozen validation identity changed')
    media={a['path']:a['sha256'] for a in quality['assets'] if a['role']=='media'}
    if any(media.get(i['path'])!=i['file_sha256'] or i['split']!='val' for i in dataset['images']):
        raise ValueError('validation media not pinned by READY')
    return dataset,quality,calibration


def comparison(baseline,candidate):
    classes=('helmet','bare_head')
    def macro(m):
        values=[m['classes'][c]['f1'] for c in classes]
        if any(x is None for x in values): raise ValueError('undefined primary F1')
        return sum(values)/2
    gain=macro(candidate)-macro(baseline)
    drops={c:baseline['classes'][c]['recall']-candidate['classes'][c]['recall'] for c in classes}
    fp_ok=candidate['classes']['bare_head']['fp']<=baseline['classes']['bare_head']['fp']
    return {'scope':'SIMULATED_CPU_NOT_ACTUAL_LINQ','macro_f1_gain':gain,'recall_drops':drops,
            'bare_head_fp_nonincrease':fp_ok,'accepted':gain>=.01 and max(drops.values())<=.02 and fp_ok,
            'policy':{'macro_f1_min_gain':.01,'max_per_class_recall_drop':.02,'bare_head_fp_nonincrease':True}}


def run(ready,manifest_path,compiled,output,max_seconds=300):
    dataset,quality,_=verified_inputs(ready)
    compiled=Path(compiled); report=json.loads((compiled/'compile-report.json').read_text())
    if report['source_onnx_sha256']!=ONNX_SHA: raise ValueError('source ONNX changed')
    manifest=json.loads(Path(manifest_path).read_text())
    if manifest['thresholds']['iou']!=.45: raise ValueError('fixed NMS required')
    manifest=deepcopy(manifest);manifest['thresholds']['confidence']=.001
    out=Path(output);out.mkdir(parents=True,exist_ok=False);(out/'raw').mkdir()
    def save(name,value): (out/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    save('frozen-input.json',{'ready_sha256':sha256(ready),'dataset_file_sha256':sha256(quality['manifest_path']),
         'dataset_digest':dataset['dataset_digest'],'manifest_sha256':sha256(manifest_path),
         'compile_report_sha256':sha256(compiled/'compile-report.json'),
         'quantized_sha256':sha256(compiled/'quantized.qm.onnx'),'scales_sha256':sha256(compiled/'scales.json'),
         'score_floor':.001,'primary_confidence':.25,'nms_iou':.45,'cpu_threads':2,'scope':'SIMULATED_CPU_NOT_ACTUAL_LINQ'})
    import torch
    torch.set_num_threads(2)
    from ml.linq.quantized_reference import QuantizedReferenceBackend
    from ml.detection import preprocess,decode
    start=time.perf_counter()
    backend=QuantizedReferenceBackend(compiled/'quantized.qm.onnx',compiled/'scales.json',compiled/'compile-report.json',threads=2)
    predictions={};timings=[];transforms={}
    for n,image in enumerate(dataset['images']):
        if time.perf_counter()-start>max_seconds: raise TimeoutError('bounded CPU allocation expired')
        tensor,transform=preprocess(np.asarray(Image.open(image['path']).convert('RGB')),manifest)
        before=time.perf_counter();outputs=backend.infer({manifest['input']['name']:tensor});timings.append(time.perf_counter()-before)
        np.savez(out/'raw'/f'{n:04d}.npz',**outputs)
        predictions[image['image_id']]=decode(outputs,manifest,transform)
        transforms[image['image_id']]={'raw_file':f'raw/{n:04d}.npz','transform':asdict(transform)}
        print(f'completed {n+1}/52',flush=True)
    save('predictions.json',predictions);save('transforms.json',transforms)
    metrics=evaluate_dataset(dataset,predictions,confidence=.25)
    save('metrics-reviewed.json',metrics)
    status={'status':'COMPLETED','scope':'SIMULATED_CPU_NOT_ACTUAL_LINQ','images':52,'seconds':time.perf_counter()-start,
            'mean_forward_seconds':float(np.mean(timings)),'final_test':'NOT_RUN'}
    save('run.json',status)
    return status

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--ready',required=True);p.add_argument('--manifest',required=True)
    p.add_argument('--compiled',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    print(json.dumps(run(a.ready,a.manifest,a.compiled,a.output)))
