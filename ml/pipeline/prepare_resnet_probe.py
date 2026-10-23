"""Prepare the already supplied vendor ResNet50 image, never run inference."""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image


def prepare(output='/workspace/artifacts/linq-rpc/resnet50'):
    image_path=Path('/workspace/artifacts/linq-api/ILSVRC2012_val_00000045.JPEG')
    program_path=Path('/workspace/artifacts/linq-api/torch_resnet50_b1_o5_h1m.tpu')
    with Image.open(image_path) as source:
        image=source.convert('RGB')
        width,height=image.size
        # Exact arithmetic from the inspected public vendor Python example.
        minimum=int(min(height,width)*.85)
        top,left=(height-minimum)//2,(width-minimum)//2
        image=image.crop((left,top,left+minimum,top+minimum)).resize((224,224))
        mean=np.array([.485,.456,.406],np.float32)
        std=np.array([.229,.224,.225],np.float32)
        array=(np.asarray(image)/255.0-mean)/std
        array=np.array(np.expand_dims(np.transpose(array,(2,0,1)),axis=0)).astype(np.float32)
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    inputs=output/'inputs.npz'
    if inputs.exists():
        with np.load(inputs,allow_pickle=False) as saved:
            if set(saved.files)!={'input.1'} or not np.array_equal(saved['input.1'],array):
                raise ValueError('existing probe input differs; never overwrite it silently')
    else:
        with inputs.open('xb') as stream:np.savez(stream,**{'input.1':array})
    report={'scope':'prepared_input_only_no_inference','input_name':'input.1','shape':list(array.shape),'dtype':str(array.dtype),
            'image_sha256':hashlib.sha256(image_path.read_bytes()).hexdigest(),
            'inputs_npz_sha256':hashlib.sha256(inputs.read_bytes()).hexdigest(),
            'local_expected_program_sha256':hashlib.sha256(program_path.read_bytes()).hexdigest(),
            'remote_program_bytes_verified':False,'expected_output_name':'495','expected_class':257,'class_offset':1}
    (output/'prepared-input.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':print(json.dumps(prepare(),indent=2))
