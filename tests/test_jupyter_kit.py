"""Archive boundary/identity tests; fixtures never claim hardware execution."""
from dataclasses import asdict
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
import numpy as np
from PIL import Image
from ml.detection.codec import preprocess
from ml.pipeline.jupyter_kit import CODE_FILES,build_kit


class JupyterKitTest(unittest.TestCase):
    def fixtures(self,root):
        project=root/'project';assets=root/'artifacts'
        repo=Path(__file__).resolve().parents[1]
        for name in CODE_FILES:
            p=project/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('# allowlisted source fixture\n')
        for path in (repo/'jupyter-kit').rglob('*'):
            if path.is_file():
                p=project/'jupyter-kit'/path.relative_to(repo/'jupyter-kit');p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(path.read_bytes())
        (project/'docs').mkdir()
        for name in ('JUPYTER_RUNBOOK.md','JUPYTER_KIT.md'):(project/'docs'/name).write_text('fixture documentation')
        img=assets/'detection/bus.jpg';img.parent.mkdir(parents=True)
        Image.fromarray(np.full((2,2,3),255,np.uint8)).save(img)
        image=np.asarray(Image.open(img).convert('RGB'))
        for name in ('helmet','pose-split'):
            md=assets/'detection'/name;md.mkdir()
            cd=assets/'linq-sdk'/(name+'-compile');cd.mkdir(parents=True)
            program=b'mock compiler output '+name.encode();(cd/'model.tpu').write_bytes(program)
            manifest={'model_id':name+'-v1','input':{'name':'images','shape':[1,3,2,2],'dtype':'float32'},
                      'artifacts':{'onnx':{'sha256':'a'*64}}}
            (md/'manifest.json').write_text(json.dumps(manifest))
            report={'compile_status':'PASS','model_id':manifest['model_id'],
                    'program_sha256':hashlib.sha256(program).hexdigest(),'source_onnx_sha256':'a'*64,
                    'inputs':[manifest['input']], 'outputs':[{'name':'output0','shape':[1,2],'dtype':'float32'}]}
            (cd/'compile-report.json').write_text(json.dumps(report))
            tensor,_=preprocess(image,manifest)
            outputs={'output0':np.array([[.1,.9]],np.float32)}
            if name=='helmet':np.savez(md/'golden.npz',input__images=tensor,output__output0=outputs['output0'])
            else:
                np.save(md/'golden-input.npy',tensor);np.savez(md/'golden-outputs.npz',**outputs)
            # Non-allowlisted assets must never be copied, even beside approved files.
            (md/'secret.env').write_text('not a real secret')
            (md/'profile.ovpn').write_text('excluded fixture')
            (md/'source.mp4').write_bytes(b'excluded fixture')
        return project,assets

    def test_inventory_binary_identity_and_allowlist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);project,assets=self.fixtures(root)
            archive=root/'kit.zip';report=build_kit(project,assets,archive)
            with zipfile.ZipFile(archive) as z:
                names=z.namelist();manifest=json.loads(z.read('KIT-MANIFEST.json'))
                self.assertEqual(set(names),set(manifest['contents'])|{'KIT-MANIFEST.json'})
                self.assertFalse(any(n.endswith(('.env','.ovpn','.mp4','.pt','.onnx')) for n in names))
                for name,spec in manifest['contents'].items():
                    self.assertEqual(hashlib.sha256(z.read(name)).hexdigest(),spec['sha256'])
                self.assertEqual(manifest['actual_remote_api_binding'],'NOT_PROVIDED_YET')
                self.assertEqual(set(json.loads(z.read('models/helmet/capture-transform.json'))),{'original_transform'})
                target=root/'unpacked';z.extractall(target)
            checked=subprocess.run([sys.executable,str(target/'verify_kit.py')],capture_output=True,text=True)
            self.assertEqual(checked.returncode,0,checked.stderr)
            self.assertEqual(report['models'],['helmet','pose-split'])
            (target/'models/helmet/model.tpu').write_bytes(b'changed')
            changed=subprocess.run([sys.executable,str(target/'verify_kit.py')],capture_output=True,text=True)
            self.assertNotEqual(changed.returncode,0)

    def test_mismatched_program_is_rejected_before_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);project,assets=self.fixtures(root)
            (assets/'linq-sdk/helmet-compile/model.tpu').write_bytes(b'changed')
            with self.assertRaises(ValueError):build_kit(project,assets,root/'kit.zip')
            self.assertFalse((root/'kit.zip').exists())

    def test_mismatched_golden_input_cannot_be_packaged_as_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);project,assets=self.fixtures(root)
            np.save(assets/'detection/pose-split/golden-input.npy',np.zeros((1,3,2,2),np.float32))
            with self.assertRaises(ValueError):build_kit(project,assets,root/'kit.zip')
