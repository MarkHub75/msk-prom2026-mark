"""Verified PUBLIC LOCAL API, not the organizer's unidentified remote service.

This matches the downloaded vendor example_torch_resnet50.py. Use only on an
execution host where actual local pytpu devices are accessible. Jupyter login
alone does not establish this. It intentionally is not the default kit path.
"""
from ml.linq.local import LocalPytpuRunner
from ml.linq.notebook import capture_call, ExpectedClass
import hashlib
from pathlib import Path


def capture_local_resnet(program_path, preprocessed_input, output_dir):
    sha=hashlib.sha256(Path(program_path).read_bytes()).hexdigest()
    with LocalPytpuRunner(program_path,sha) as runner:
        def run(inputs):
            return runner(inputs,{'request_id':'stock-local-capture','model_id':'stock-resnet50',
                                  'program_sha256':sha})['outputs']
        return capture_call(run,inputs={'input.1':preprocessed_input},output_names=['495'],
            program_path=program_path,output_dir=output_dir,model_id='stock-resnet50',
            expected_class=ExpectedClass('495',257,axis=-1,class_offset=1),placement_attested=True)
