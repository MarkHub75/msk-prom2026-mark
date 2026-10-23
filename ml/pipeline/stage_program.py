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


def file_hash(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):value.update(block)
    return value.hexdigest()


def stage(cache_dir, source=None):
    source=Path(source) if source is not None else Path(__file__).resolve().parent/PROGRAM_NAME
    directory=Path(cache_dir).resolve()
    if not directory.is_dir() or not (directory/STOCK_NAME).is_file():
        raise FileNotFoundError('the selected cache directory does not contain the confirmed stock program')
    if file_hash(source)!=PROGRAM_SHA256:
        raise ValueError('source program differs from reviewed Helmet bytes')
    target=directory/PROGRAM_NAME
    if target.exists():
        if target.is_symlink() or file_hash(target)!=PROGRAM_SHA256:
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
            if file_hash(target)!=PROGRAM_SHA256:
                raise ValueError('staged program checksum mismatch')
        except Exception:
            if created:target.unlink(missing_ok=True)
            raise
        state='STAGED'
    return {'status':state,'program_name':PROGRAM_NAME,'program_sha256':PROGRAM_SHA256,
            'stock_program_present_in_selected_namespace':True,
            'worker_visibility':'NOT_VERIFIED_UNTIL_HELMET_REQUEST',
            'filesystem_path_and_account_not_exported':True}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache-dir',required=True)
    parser.add_argument('--program-file')
    parser.add_argument('--receipt',default='helmet-staging-receipt.json')
    args=parser.parse_args()
    try:
        result=stage(args.cache_dir,args.program_file)
    except Exception as exc:
        print(json.dumps({'status':'NOT_STAGED','error_type':type(exc).__name__}))
        return 1
    with Path(args.receipt).open('x') as output:json.dump(result,output,indent=2)
    print(json.dumps(result))
    return 0

if __name__=='__main__':raise SystemExit(main())
