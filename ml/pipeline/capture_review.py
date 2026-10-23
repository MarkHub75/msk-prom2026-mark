"""Verify exported capture integrity; never infer hardware placement from hashes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile
import numpy as np


def _hash(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            digest.update(block)
    return digest.hexdigest()


def _sha(value):
    return isinstance(value,str) and re.fullmatch('[0-9a-f]{64}',value) is not None


def _verify_arrays(path, expected, max_bytes):
    if not isinstance(expected,dict) or not expected:
        raise ValueError('missing tensor manifest')
    with zipfile.ZipFile(path) as archive:
        if sum(info.file_size for info in archive.infolist()) > max_bytes + 1024*1024:
            raise ValueError('capture byte budget exceeded')
    total=0
    with np.load(path,allow_pickle=False) as archive:
        if len(set(archive.files))!=len(archive.files) or set(archive.files)!=set(expected):
            raise ValueError('tensor names differ from capture manifest')
        for name in archive.files:
            spec=expected[name];value=archive[name]
            if not isinstance(spec,dict) or value.dtype.kind not in 'buif' or not value.size or not np.isfinite(value).all():
                raise ValueError('invalid numeric tensor')
            if list(value.shape)!=spec.get('shape') or value.dtype.name!=spec.get('dtype') or value.nbytes!=spec.get('nbytes'):
                raise ValueError('tensor specification mismatch')
            total+=value.nbytes
            if total>max_bytes:
                raise ValueError('capture byte budget exceeded')
            if not _sha(spec.get('sha256')) or hashlib.sha256(np.ascontiguousarray(value).tobytes(order='C')).hexdigest()!=spec['sha256']:
                raise ValueError('tensor hash mismatch')
    return len(expected), total


def review_capture(directory, expected_program_sha256=None, max_bytes=256*1024*1024):
    """Validate completed capture + file/tensor hashes, optional trusted program hash.

    These hashes detect inconsistent transfer. They are not signatures, hardware
    attestation or proof that an untrusted author actually executed the call.
    """
    directory=Path(directory)
    if type(max_bytes) is not int or max_bytes<=0:
        raise ValueError('invalid byte budget')
    report_path=directory/'capture.json'
    if report_path.stat().st_size>1024*1024:
        raise ValueError('capture manifest too large')
    capture=json.loads(report_path.read_text())
    if (capture.get('schema_version')!='1.0' or capture.get('status')!='completed' or
        capture.get('call_started') is not True or capture.get('call_completed') is not True):
        raise ValueError('capture does not report a completed validated call')
    program=capture.get('program',{}).get('sha256')
    if not _sha(program):
        raise ValueError('invalid program hash')
    if expected_program_sha256 is not None and (not _sha(expected_program_sha256) or program!=expected_program_sha256):
        raise ValueError('capture program differs from expected program')
    checked={}
    for kind in ('inputs','outputs'):
        asset=capture.get('artifacts',{}).get(kind,{})
        name=kind+'.npz'
        if asset.get('file')!=name or not _sha(asset.get('sha256')):
            raise ValueError('invalid capture artifact reference')
        path=directory/name
        if path.is_symlink() or _hash(path)!=asset['sha256']:
            raise ValueError('artifact hash mismatch or symlink')
        count,size=_verify_arrays(path,capture.get(kind),max_bytes)
        checked[kind]={'file_sha256':asset['sha256'],'tensor_count':count,'tensor_bytes':size}
    return {'status':'CAPTURE_INTEGRITY_VALID','schema_version':'1.0','program_sha256':program,
            'expected_program_matched':expected_program_sha256 is not None,'artifacts':checked,
            'hardware_execution':'NOT_ESTABLISHED_BY_INTEGRITY_REVIEW','target_quality':'NOT_EVALUATED'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture',required=True)
    parser.add_argument('--expected-program-sha256')
    parser.add_argument('--output')
    args=parser.parse_args()
    try:
        report=review_capture(args.capture,args.expected_program_sha256)
    except Exception as exc:
        report={'status':'INVALID_CAPTURE','error_type':type(exc).__name__,
                'hardware_execution':'NOT_ESTABLISHED_BY_INTEGRITY_REVIEW'}
    if args.output:
        Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if report['status']!='CAPTURE_INTEGRITY_VALID':
        raise SystemExit(2)

if __name__=='__main__':main()
