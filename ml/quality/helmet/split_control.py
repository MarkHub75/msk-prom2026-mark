"""Pre-compile all52 float ABI parity control against preserved original outputs."""
from copy import deepcopy
import json,time
from pathlib import Path
import numpy as np
from PIL import Image
from ml.detection import preprocess,decode
from ml.quality.handoff import sha256
from .quantized import verified_inputs,ONNX_SHA
from .metrics import evaluate_dataset


def verify(ready,manifest_path,reference,output):
    import onnxruntime as ort
    dataset,quality,_=verified_inputs(ready)
    m=json.loads(Path(manifest_path).read_text()); graph=Path(manifest_path).parent/m['artifacts']['onnx']['file']
    if m['source_onnx_sha256']!=ONNX_SHA or sha256(graph)!=m['artifacts']['onnx']['sha256']:
        raise ValueError('graph lineage mismatch')
    m=deepcopy(m);m['thresholds']['confidence']=.001
    reference=Path(reference);out=Path(output);out.mkdir(parents=True,exist_ok=False);(out/'raw').mkdir()
    opts=ort.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
    session=ort.InferenceSession(str(graph),sess_options=opts,providers=['CPUExecutionProvider'])
    predictions={};checks=[];start=time.perf_counter()
    for n,image in enumerate(dataset['images']):
        tensor,t=preprocess(np.asarray(Image.open(image['path']).convert('RGB')),m)
        outputs=dict(zip([v.name for v in session.get_outputs()],session.run(None,{m['input']['name']:tensor})))
        combined=np.concatenate([outputs[m['split_outputs'][k]] for k in ('boxes','class_scores')],axis=1)
        with np.load(reference/'raw'/f'{n:04d}.npz',allow_pickle=False) as data: original=data['output0']
        exact=np.array_equal(combined,original);close=np.allclose(combined,original,rtol=1e-6,atol=1e-6)
        if not close: raise ValueError('float split output parity failed')
        checks.append({'image_id':image['image_id'],'bitwise_equal':exact,'allclose':close,'max_abs_diff':float(np.max(np.abs(combined-original)))})
        np.savez(out/'raw'/f'{n:04d}.npz',**outputs);predictions[image['image_id']]=decode(outputs,m,t)
    metrics=evaluate_dataset(dataset,predictions)
    prior=json.loads((reference/'metrics-reviewed.json').read_text())
    if metrics!=prior: raise ValueError('split decoded metrics differ')
    report={'status':'PASS','scope':'FLOAT_ONNX_CPU_NOT_ACTUAL_LINQ','images':52,'checks':checks,'metrics_identical':True,
            'graph_sha256':sha256(graph),'reference_manifest_sha256':sha256(reference/'frozen-input.json'),
            'ready_sha256':sha256(ready),'dataset_file_sha256':sha256(quality['manifest_path']),'seconds':time.perf_counter()-start}
    for name,value in [('parity.json',report),('predictions.json',predictions),('metrics-reviewed.json',metrics)]:
        (out/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    return report
