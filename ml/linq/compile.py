"""Compile static ONNX with the issued 2026.9 SDK and real calibration tensors.

Run in the separate matched SDK environment. Does not install software or run TPU.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import time
import numpy as np


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as file:
        for block in iter(lambda: file.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def compile_model(onnx_path, calibration_path, output_dir, model_id, preset='O1'):
    """Return immutable result metadata; caller must separately validate TPU parity."""
    if preset not in ('O1','O5'):
        raise ValueError('preset must be O1 or O5')
    if not model_id or not isinstance(model_id,str):
        raise ValueError('model_id is required')
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    report={'model_id':model_id,'linq_status':'NOT_RUN','compile_status':'RUNNING',
            'preset':preset,'target':'TPU_H1M','stages':{},'calibration_sha256':sha256(calibration_path),
            'source_onnx_sha256':sha256(onnx_path)}
    stage='import_sdk';start=time.perf_counter()
    try:
        import onnx
        from tpu_framework import (RegularModel, QuantizedModel, Network, compiler,
                                   TpuProgram, O1, O5, TPU_H1M, preliminary_model_conditioning)
        stage='load_onnx'
        model=onnx.load(str(onnx_path))
        initializers={x.name for x in model.graph.initializer}
        for entry in list(model.graph.input):
            if entry.name in initializers:model.graph.input.remove(entry)
        onnx.checker.check_model(model)
        for entry in model.graph.input:
            shape=[d.dim_value for d in entry.type.tensor_type.shape.dim]
            if not shape or any(d<=0 for d in shape):
                raise ValueError('dynamic input shapes are unsupported')
        stage='conditioning'
        model=preliminary_model_conditioning(model)
        onnx.save(model,str(out/'optimized.onnx'))
        def specs(values):
            result=[]
            for value in values:
                shape=[d.dim_value for d in value.type.tensor_type.shape.dim]
                if not shape or any(d<=0 for d in shape):
                    raise ValueError('dynamic tensor dimensions need verified static inference')
                dtype=str(np.dtype(onnx.helper.tensor_dtype_to_np_dtype(value.type.tensor_type.elem_type)))
                result.append({'name':value.name,'shape':shape,'dtype':dtype})
            return result
        report['inputs']=specs(model.graph.input)
        # These describe conditioned ONNX ABI. Runtime ABI must be verified before use.
        report['outputs']=specs(model.graph.output)
        stage='calibration_input'
        with np.load(calibration_path,allow_pickle=False) as data:
            calibration={name:np.ascontiguousarray(data[name]) for name in data.files}
        if set(calibration)!={s['name'] for s in report['inputs']}:
            raise ValueError('calibration tensor names differ from model inputs')
        for spec in report['inputs']:
            value=calibration[spec['name']]
            # Vendor calibrator permits a corpus on the leading sample dimension.
            if (value.ndim!=len(spec['shape']) or list(value.shape[1:])!=spec['shape'][1:] or
                    value.shape[0]<spec['shape'][0] or value.dtype!=np.dtype(spec['dtype']) or
                    not np.isfinite(value).all()):
                raise ValueError('calibration dtype/shape/values mismatch')
        stage='quantize'
        regular=RegularModel(model=model)
        thresholds=regular.calibrate_torch(calibration_data=calibration)
        RegularModel.dump_thresholds(str(out/'thresholds.json'),thresholds)
        quantized=regular.quantize(thresholds)
        quantized.save(file_dir=str(out),file_name='quantized.qm.onnx')
        stage='network'
        network,_=Network.from_quantized_model(quantized)
        stage='compile'
        executable,descriptions=compiler.compile_(hardware_parameters=TPU_H1M,network=network,
                                                 parameters=O1 if preset=='O1' else O5)
        stage='save_program'
        program=TpuProgram.from_executable(executable,descriptions)
        program.to_file(str(out/'model.tpu'))
        report.update(compile_status='PASS',program_sha256=sha256(out/'model.tpu'),
                      runtime_abi_verified=False)
        report['stages']['compile']={'status':'PASS'}
    except Exception as error:
        report['compile_status']='FAIL'
        report['stages'][stage]={'status':'FAIL','exception_type':type(error).__name__}
        # Keep input-derived/SDK error strings out of routinely published metadata.
    report['total_ms']=(time.perf_counter()-start)*1000
    (out/'compile-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--onnx',required=True)
    parser.add_argument('--calibration',required=True,help='NPZ named actual preprocessed tensors; never random for quality evaluation')
    parser.add_argument('--output',required=True)
    parser.add_argument('--model-id',required=True)
    parser.add_argument('--preset',choices=('O1','O5'),default='O1')
    args=parser.parse_args()
    report=compile_model(args.onnx,args.calibration,args.output,args.model_id,args.preset)
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if report['compile_status']=='PASS' else 1)


if __name__=='__main__':main()
