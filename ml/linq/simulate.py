"""Bounded SDK hardware-aware Torch diagnostic, explicitly NOT TPU execution.

The I/O policy comes from emitted scales.json: quantize input by its recorded
multiplier, evaluate .gm, dequantize output by recorded channel scales. Vendor
runtime codec confirmation and hardware parity remain separate acceptance gates.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import time
import numpy as np


def quantize_input(array, spec):
    dtype=np.dtype(spec['data_type'])
    if dtype.kind not in 'iu':
        raise ValueError('diagnostic supports only explicit integer-coded inputs')
    if spec.get('zero_point',0)!=0:
        raise ValueError('nonzero input zero-point needs a verified codec')
    scale=np.asarray(spec['data_scale'],dtype=np.float64)
    if not np.isfinite(scale).all() or (scale<=0).any():
        raise ValueError('invalid input scale')
    limits=np.iinfo(dtype)
    # Torch hardware graph kernels consume floating representations of integer codes.
    return np.clip(np.round(array*scale),limits.min,limits.max).astype(np.float32)


def dequantize_output(array,spec):
    if spec.get('zero_point',0)!=0:
        raise ValueError('nonzero output zero-point needs a verified codec')
    scale=np.asarray(spec['data_scale'],dtype=np.float32)
    if not np.isfinite(scale).all() or (scale<=0).any():
        raise ValueError('invalid output scale')
    result=np.asarray(array,dtype=np.float32)*scale
    if result.shape!=array.shape:
        raise ValueError('scale broadcast altered tensor shape')
    return result


def simulate(quantized_path,scales_path,input_npz,source_onnx,output_dir):
    import torch
    import onnxruntime as ort
    from tpu_framework import QuantizedModel
    torch.set_num_threads(4)
    started=time.perf_counter();out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    scales=json.loads(Path(scales_path).read_text())
    with np.load(input_npz,allow_pickle=False) as data:
        inputs={name:np.ascontiguousarray(data[name]) for name in data.files}
    graph=QuantizedModel.load(str(quantized_path)).as_torch_graph(batch_size=1)
    input_names=list(graph.get_inputs_anchors())
    output_names=list(graph.get_outputs_anchors())
    if set(inputs)!=set(input_names):
        raise ValueError('simulation input names differ from graph anchors')
    coded={name:quantize_input(inputs[name],scales[name+':0']) for name in input_names}
    with torch.no_grad():
        raw=graph.gm(**{name:torch.from_numpy(value) for name,value in coded.items()})
    if isinstance(raw,dict):
        raw_outputs=raw
    elif isinstance(raw,(tuple,list)):
        if len(raw)!=len(output_names):raise ValueError('output count differs from anchors')
        raw_outputs=dict(zip(output_names,raw))
    elif len(output_names)==1:
        raw_outputs={output_names[0]:raw}
    else:raise ValueError('multiple outputs need mapped tensors')
    raw_outputs={name:value.detach().cpu().numpy() for name,value in raw_outputs.items()}
    outputs={name:dequantize_output(value,scales[name+':0']) for name,value in raw_outputs.items()}
    options=ort.SessionOptions();options.intra_op_num_threads=4;options.inter_op_num_threads=1
    session=ort.InferenceSession(str(source_onnx),sess_options=options,providers=['CPUExecutionProvider'])
    reference=dict(zip([x.name for x in session.get_outputs()],session.run(None,inputs)))
    if set(reference)!=set(outputs):raise ValueError('source and simulation output names differ')
    report={'kind':'quantized_torch_scaled_smoke_NOT_HARDWARE',
            'runtime_codec_confirmed':False,'calibration_separation_verified':False,
            'io_policy':'round(input*input_data_scale); output*recorded_output_data_scale',
            'outputs':{},'seconds':time.perf_counter()-started}
    for name,value in outputs.items():
        ref=reference[name]
        if ref.shape!=value.shape:raise ValueError('source and simulated tensor shapes differ')
        report['outputs'][name]={'shape':list(value.shape),'finite':bool(np.isfinite(value).all()),
            'quant_min':float(value.min()),'quant_max':float(value.max()),
            'reference_min':float(ref.min()),'reference_max':float(ref.max()),
            'mean_abs_diff':float(np.abs(value-ref).mean()),'max_abs_diff':float(np.abs(value-ref).max()),
            'count_ge_025':int((value>=.25).sum()),'reference_count_ge_025':int((ref>=.25).sum())}
    np.savez(out/'simulation-output.npz',**outputs)
    np.savez(out/'simulation-reference.npz',**reference)
    np.savez(out/'simulation-raw-codes.npz',**raw_outputs)
    (out/'simulation-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--quantized',required=True);p.add_argument('--scales',required=True)
    p.add_argument('--inputs',required=True);p.add_argument('--source-onnx',required=True)
    p.add_argument('--output',required=True)
    a=p.parse_args()
    print(json.dumps(simulate(a.quantized,a.scales,a.inputs,a.source_onnx,a.output),indent=2))


if __name__=='__main__':main()
