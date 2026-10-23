"""Standard-library-only verification; does not contact LinQ or install anything."""
import hashlib
import json
from pathlib import Path


def verify(root=None):
    root=Path(root) if root else Path(__file__).resolve().parent
    manifest=json.loads((root/'KIT-MANIFEST.json').read_text())
    for name,spec in manifest['contents'].items():
        relative=Path(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('invalid inventory path')
        path=root/relative
        if path.is_symlink() or not path.is_file():
            raise ValueError('missing or linked inventory file')
        data=path.read_bytes()
        if len(data)!=spec['bytes'] or hashlib.sha256(data).hexdigest()!=spec['sha256']:
            raise ValueError('kit inventory hash mismatch')
    print(json.dumps({'kit_integrity':'PASS','files':len(manifest['contents']),
                      'model_order':manifest['model_order'],
                      'actual_remote_api_binding':manifest['actual_remote_api_binding']}))
    return manifest

if __name__=='__main__':verify()
