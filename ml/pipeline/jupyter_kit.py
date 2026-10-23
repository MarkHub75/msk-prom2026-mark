"""Build a portable allowlisted LinQ Jupyter handoff from existing artifacts.

No training, compilation, package installation, credentials or notebook execution.
"""
import argparse
from dataclasses import asdict
import hashlib
import io
import json
from pathlib import Path
import zipfile
import numpy as np

CODE_FILES = (
    'ml/__init__.py', 'ml/linq/__init__.py', 'ml/linq/backend.py',
    'ml/linq/local.py', 'ml/linq/notebook.py', 'ml/linq/jupyter.py',
    'ml/detection/__init__.py', 'ml/detection/codec.py', 'ml/detection/reference.py',
    'ml/detection/export.py', 'ml/detection/compare_capture.py',
    'ml/pipeline/__init__.py', 'ml/pipeline/capture_review.py',
)
MODEL_NAMES = ('helmet', 'pose-split')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def _json(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode()


def _npz(values):
    out=io.BytesIO()
    np.savez_compressed(out, **values)
    return out.getvalue()


def _numeric(path):
    with np.load(path,allow_pickle=False) as archive:
        arrays={name:archive[name].copy() for name in archive.files}
    if not arrays or any(value.dtype.kind not in 'iuf' or not value.size or not np.isfinite(value).all() for value in arrays.values()):
        raise ValueError('invalid existing golden arrays')
    return arrays


def collect_files(project, artifacts):
    """Only explicit code/docs plus two known model directories enter the archive."""
    project,artifacts=Path(project),Path(artifacts)
    files={name:(project/name).read_bytes() for name in CODE_FILES}
    for name in ('README.md','requirements.txt','verify_kit.py','bindings.py','run_case.py'):
        files[name]=(project/'jupyter-kit'/name).read_bytes()
    for name in ('JUPYTER_RUNBOOK.md','JUPYTER_KIT.md'):
        files['docs/'+name]=(project/'docs'/name).read_bytes()
    for path in sorted((project/'jupyter-kit/examples').glob('*.py')):
        files['examples/'+path.name]=path.read_bytes()
    from PIL import Image
    from ml.detection.codec import preprocess
    image=np.asarray(Image.open(artifacts/'detection/bus.jpg').convert('RGB'))
    for name in MODEL_NAMES:
        model_dir=artifacts/'detection'/name
        compiled_dir=artifacts/'linq-sdk'/(name+'-compile')
        manifest=json.loads((model_dir/'manifest.json').read_text())
        report=json.loads((compiled_dir/'compile-report.json').read_text())
        program=(compiled_dir/'model.tpu').read_bytes()
        if report['compile_status']!='PASS' or report['model_id']!=manifest['model_id']:
            raise ValueError('model/compiler identity mismatch')
        if digest(program)!=report['program_sha256'] or report['source_onnx_sha256']!=manifest['artifacts']['onnx']['sha256']:
            raise ValueError('model artifact hash mismatch')
        if name=='helmet':
            golden=_numeric(model_dir/'golden.npz')
            inputs={key.removeprefix('input__'):value for key,value in golden.items() if key.startswith('input__')}
            outputs={key.removeprefix('output__'):value for key,value in golden.items() if key.startswith('output__')}
        else:
            inputs={'images':np.load(model_dir/'golden-input.npy',allow_pickle=False)}
            outputs=_numeric(model_dir/'golden-outputs.npz')
        tensor,transform=preprocess(image,manifest)
        if set(inputs)!={'images'} or not np.array_equal(inputs['images'],tensor):
            raise ValueError('golden input/preprocessing mismatch')
        if set(outputs)!={spec['name'] for spec in report['outputs']}:
            raise ValueError('golden output/compiler names mismatch')
        for spec in report['outputs']:
            value=outputs[spec['name']]
            if list(value.shape)!=spec['shape'] or value.dtype!=np.dtype(spec['dtype']):
                raise ValueError('golden output/compiler ABI mismatch')
        portable=dict(manifest)
        portable['linq_status']='NOT_CAPTURED'
        portable['linq']={'program_path':'model.tpu','program_sha256':report['program_sha256'],
                          'runtime_abi_verified':False,'inputs':report['inputs'],'outputs':report['outputs']}
        prefix='models/'+name+'/'
        files[prefix+'manifest.json']=_json(portable)
        files[prefix+'compile-report.json']=_json(report)
        files[prefix+'model.tpu']=program
        files[prefix+'inputs.npz']=_npz(inputs)
        files[prefix+'golden-outputs.npz']=_npz(outputs)
        files[prefix+'capture-transform.json']=_json({'original_transform':asdict(transform)})
        files[prefix+'NOTES.txt']=(
            'Existing TPU_H1M O1 compiler-smoke program. Runtime ABI is not verified.\n'
            'Golden arrays are float ONNX references, not TPU outputs.\n'
            'One-image calibration is not independent accuracy validation.\n'
            'Use only the supplied actual service to upload/load this exact program.\n').encode()
    files['KIT-MANIFEST.json']=_json({
        'schema_version':'1.0','kit':'mosprom-linq-jupyter','model_order':list(MODEL_NAMES),
        'actual_remote_api_binding':'NOT_PROVIDED_YET',
        'stock_run_user_report':{'status_code':0,'class_index':257,'response_seconds':0.39,
                                 'scope':'reported by user; tensor capture pending'},
        'contents':{name:{'sha256':digest(body),'bytes':len(body)} for name,body in sorted(files.items())},
    })
    return files


def build_kit(project,artifacts,output):
    files=collect_files(project,artifacts)
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    temp=output.with_suffix('.tmp')
    try:
        with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
            for name,body in sorted(files.items()):
                info=zipfile.ZipInfo(name,date_time=(2026,10,23,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o100644 << 16
                archive.writestr(info,body)
        # Verify the inventory before publishing the complete archive.
        with zipfile.ZipFile(temp) as archive:
            if archive.testzip() is not None or set(archive.namelist())!=set(files):
                raise ValueError('archive structure verification failed')
            for name,body in files.items():
                if archive.read(name)!=body:
                    raise ValueError('archive content mismatch')
        temp.replace(output)
    finally:
        temp.unlink(missing_ok=True)
    return {'path':str(output),'bytes':output.stat().st_size,'sha256':digest(output.read_bytes()),
            'file_count':len(files),'models':list(MODEL_NAMES),'actual_remote_api_binding':'NOT_PROVIDED_YET'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument('--artifacts',default='/workspace/artifacts')
    parser.add_argument('--output',default='/workspace/artifacts/linq-jupyter-kit.zip')
    args=parser.parse_args()
    print(json.dumps(build_kit(args.project,args.artifacts,args.output),indent=2))

if __name__=='__main__':main()
