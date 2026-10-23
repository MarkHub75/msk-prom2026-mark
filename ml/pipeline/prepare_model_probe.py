"""Prepare existing golden arrays for one own-model AMQP request; no inference."""
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image
from ml.detection import preprocess


def prepare(name,root='/workspace/artifacts'):
    if name not in ('helmet','pose-split'):raise ValueError('unknown reviewed model')
    root=Path(root);base=root/'detection'/name
    manifest=json.loads((base/'manifest.json').read_text())
    if name=='helmet':
        with np.load(base/'golden.npz',allow_pickle=False) as values:
            inputs={key.removeprefix('input__'):values[key] for key in values.files if key.startswith('input__')}
            outputs={key.removeprefix('output__'):values[key] for key in values.files if key.startswith('output__')}
    else:
        inputs={'images':np.load(base/'golden-input.npy',allow_pickle=False)}
        with np.load(base/'golden-outputs.npz',allow_pickle=False) as values:outputs={key:values[key] for key in values.files}
    with Image.open(root/'detection/bus.jpg') as image:
        tensor,transform=preprocess(np.asarray(image.convert('RGB')),manifest)
    if set(inputs)!={'images'} or not np.array_equal(inputs['images'],tensor):raise ValueError('golden input mismatch')
    directory=root/'linq-rpc'/name;directory.mkdir(parents=True,exist_ok=True)
    for filename,data in [('inputs.npz',inputs),('golden-outputs.npz',outputs)]:
        target=directory/filename
        if target.exists():
            with np.load(target,allow_pickle=False) as old:
                if set(old.files)!=set(data) or any(not np.array_equal(old[key],value) for key,value in data.items()):raise ValueError('existing probe data differs')
        else:
            with target.open('xb') as stream:np.savez(stream,**data)
    metadata={'original_transform':asdict(transform),'runtime_to_reference':{key:key for key in outputs}}
    (directory/'comparison-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    return {'status':'PREPARED_ONLY','model_id':manifest['model_id'],'directory':str(directory),'output_names':list(outputs)}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('name',choices=['helmet','pose-split'])
    print(json.dumps(prepare(parser.parse_args().name)))
