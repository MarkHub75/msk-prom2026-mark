"""Run INSIDE organizer Jupyter to stage reviewed Helmet bytes, stdlib only.

The AMQP file:// URI refers to the worker's filesystem, never the Vast path.
This checks the existing stock-program namespace before creating one new file.
No credentials, broker connection, guessed alternative paths or overwrites.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat

PROGRAM_NAME='helmet-v1.tpu'
PROGRAM_SHA256='408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa'
STOCK_NAME='torch_resnet50_b1_o5_h1m.tpu'
POSE_NAME='pose-split-v1.tpu'
POSE_SHA256='c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b'


def file_hash(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):value.update(block)
    return value.hexdigest()


def stage(cache_dir, source=None, model='helmet'):
    if model=='helmet':
        name,expected=PROGRAM_NAME,PROGRAM_SHA256
    elif model=='pose-split':
        name,expected=POSE_NAME,POSE_SHA256
    else:
        raise ValueError('only reviewed Helmet and Split-Pose programs are allowed')
    source=Path(source) if source is not None else Path(__file__).resolve().parent/name
    directory=Path(cache_dir).resolve()
    if not directory.is_dir() or not (directory/STOCK_NAME).is_file():
        raise FileNotFoundError('the selected cache directory does not contain the confirmed stock program')
    if file_hash(source)!=expected:
        raise ValueError('source program differs from reviewed Helmet bytes')
    target=directory/name
    if target.exists():
        if target.is_symlink() or file_hash(target)!=expected:
            raise FileExistsError('a different target already exists; it will not be overwritten')
        state='ALREADY_STAGED_IDENTICAL'
    else:
        created=False
        try:
            with target.open('xb') as output,source.open('rb') as incoming:
                created=True
                shutil.copyfileobj(incoming,output,1024*1024)
                output.flush();os.fsync(output.fileno())
                # Match read permissions of the already working stock program.
                os.fchmod(output.fileno(),stat.S_IMODE((directory/STOCK_NAME).stat().st_mode)&0o666)
            if file_hash(target)!=expected:
                raise ValueError('staged program checksum mismatch')
        except Exception:
            if created:target.unlink(missing_ok=True)
            raise
        state='STAGED'
    return {'status':state,'program_name':name,'program_sha256':expected,
            'stock_program_present_in_selected_namespace':True,
            'worker_visibility':'NOT_VERIFIED_UNTIL_HELMET_REQUEST',
            'filesystem_path_and_account_not_exported':True}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache-dir',required=True)
    parser.add_argument('--program-file')
    parser.add_argument('--model',choices=['helmet','pose-split'],default='helmet')
    parser.add_argument('--receipt',default='helmet-staging-receipt.json')
    args=parser.parse_args()
    try:
        result=stage(args.cache_dir,args.program_file,args.model)
    except Exception as exc:
        print(json.dumps({'status':'NOT_STAGED','error_type':type(exc).__name__}))
        return 1
    with Path(args.receipt).open('x') as output:json.dump(result,output,indent=2)
    print(json.dumps(result))
    return 0

if __name__=='__main__':raise SystemExit(main())
