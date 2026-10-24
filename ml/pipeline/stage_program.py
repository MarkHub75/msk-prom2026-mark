"""Stage reviewed own bytes INSIDE an explicitly owned Matvey Jupyter folder.

Stdlib only. No stock/captain/baseline lookup, guessed path, broker access or
overwrite. Account identity is supplied privately by the authorized notebook.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import re

PROGRAM_NAME='matvey_helmet-v1.tpu'
PROGRAM_SHA256='408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa'
POSE_NAME='matvey_pose-split-v1.tpu'
POSE_SHA256='c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b'
CACHE_ROOT=Path('/auto/cache')


def file_hash(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):value.update(block)
    return value.hexdigest()


def owned_cache_directory(cache_dir, owner_login, *, create=False):
    """Validate literal identity and reject symlink escapes before any write."""
    if (not isinstance(owner_login,str) or not re.fullmatch(r'[A-Za-z0-9_@+-][A-Za-z0-9_@.+-]*',owner_login)
            or '..' in owner_login):
        raise ValueError('private explicit runtime account required')
    expected=CACHE_ROOT/owner_login/'matvey'
    directory=Path(cache_dir)
    if directory!=expected or str(cache_dir)!=str(directory):
        raise ValueError('only the runtime account matvey directory is allowed')
    parent=expected.parent
    if not parent.is_dir() or parent.resolve()!=parent or directory.is_symlink():
        raise ValueError('owned directory parent is missing or symlinked')
    if create and not directory.exists():directory.mkdir(mode=0o755)
    if not directory.is_dir() or directory.resolve()!=directory:
        raise FileNotFoundError('owned matvey directory must be explicitly prepared')
    return directory


def stage(cache_dir, source=None, model='helmet', *, owner_login=None):
    directory=owned_cache_directory(cache_dir,owner_login)
    if model=='helmet':
        name,expected=PROGRAM_NAME,PROGRAM_SHA256
    elif model=='pose-split':
        name,expected=POSE_NAME,POSE_SHA256
    else:
        raise ValueError('only reviewed Helmet and Split-Pose programs are allowed')
    if not name.startswith('matvey_') or '/' in name or '..' in name or 'mosprom_' in name or '_cut_ap9999' in name:
        raise ValueError('protected or foreign program name forbidden')
    source=Path(source) if source is not None else Path(__file__).resolve().parent/name
    if (source.is_symlink() or not source.resolve().is_relative_to(directory)
            or not source.name.startswith('matvey_') or not source.is_file()):
        raise ValueError('source must be a regular own program inside matvey')
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
                # Own model bytes contain no credentials; service worker needs read.
                os.fchmod(output.fileno(),0o644)
            if file_hash(target)!=expected:
                raise ValueError('staged program checksum mismatch')
        except Exception:
            if created:target.unlink(missing_ok=True)
            raise
        state='STAGED'
    return {'status':state,'program_name':name,'program_sha256':expected,
            'namespace_owner':'matvey','program_path_namespace_verified':True,
            'worker_visibility':'NOT_VERIFIED_UNTIL_HELMET_REQUEST',
            'filesystem_path_and_account_not_exported':True}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache-dir',required=True)
    parser.add_argument('--program-file')
    parser.add_argument('--model',choices=['helmet','pose-split'],default='helmet')
    parser.add_argument('--receipt',default='matvey_staging_receipt.json')
    args=parser.parse_args()
    try:
        directory=owned_cache_directory(args.cache_dir,os.environ.get('LINQ_LOGIN'))
        receipt=directory/args.receipt
        if Path(args.receipt).name!=args.receipt or not args.receipt.startswith('matvey_'):
            raise ValueError('own receipt basename required')
        result=stage(directory,args.program_file,args.model,owner_login=os.environ.get('LINQ_LOGIN'))
    except Exception as exc:
        print(json.dumps({'status':'NOT_STAGED','error_type':type(exc).__name__}))
        return 1
    with receipt.open('x') as output:json.dump(result,output,indent=2)
    print(json.dumps(result))
    return 0

if __name__=='__main__':raise SystemExit(main())
