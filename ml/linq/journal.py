"""Fsynced local request intent and selected numeric response; never auth/URI."""
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
from uuid import UUID, uuid4

import numpy as np

DEFAULT_JOURNAL_DIR = '/workspace/artifacts/linq-rpc/requests'
STATES = {'NOT_SUBMITTED','SUBMITTING','ACCEPTED','UNKNOWN','COMPLETED','SERVICE_FAILED'}
TERMINAL = {'COMPLETED','SERVICE_FAILED'}


def fsync_directory(path):
    fd=os.open(path,os.O_RDONLY | getattr(os,'O_DIRECTORY',0))
    try:os.fsync(fd)
    finally:os.close(fd)


def atomic_json(path,value):
    path=Path(path);temporary=path.with_name('.'+path.name+'.'+uuid4().hex+'.tmp')
    try:
        fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w',encoding='utf-8') as file:
            json.dump(value,file,indent=2,allow_nan=False);file.write('\n');file.flush();os.fsync(file.fileno())
        os.replace(temporary,path);fsync_directory(path.parent)
    finally:temporary.unlink(missing_ok=True)


def _uuid(value):
    if not isinstance(value,str) or str(UUID(value))!=value:raise ValueError('canonical request UUID required')
    return value


def _hash(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as file:
        for block in iter(lambda:file.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()


def tensor_metadata(arrays):
    return {name:{'shape':list(value.shape),'dtype':value.dtype.name,'nbytes':value.nbytes,
                  'sha256':hashlib.sha256(value.tobytes(order='C')).hexdigest()}
            for name,value in arrays.items()}


class RequestJournal:
    def __init__(self,root=DEFAULT_JOURNAL_DIR):self.root=Path(root).resolve()
    def path(self,request_id):return self.root/_uuid(request_id)

    def create(self,request_id,*,purpose,program_uri_sha256,inputs,output_names,reply_queue=None,capture_dir=None,capture_id=None):
        if purpose not in {'inference','model_upload'}:raise ValueError('invalid request purpose')
        directory=self.path(request_id)
        self.root.mkdir(parents=True,exist_ok=True,mode=0o700)
        directory.mkdir(mode=0o700)
        fsync_directory(self.root)
        # Store only explicitly selected numeric input arrays, never headers/auth.
        temporary=directory/('.inputs.'+uuid4().hex+'.tmp')
        try:
            fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,'wb') as file:
                np.savez(file,**inputs);file.flush();os.fsync(file.fileno())
            os.replace(temporary,directory/'inputs.npz');fsync_directory(directory)
        finally:temporary.unlink(missing_ok=True)
        record={'schema_version':'1.0','request_id':request_id,'state':'NOT_SUBMITTED',
                'purpose':purpose,'program_uri_sha256':program_uri_sha256,'reply_queue':reply_queue,
                'inputs':tensor_metadata(inputs),'input_artifact':{'file':'inputs.npz','sha256':_hash(directory/'inputs.npz')},
                'output_names':list(output_names),
                'capture_dir':str(Path(capture_dir).resolve()) if capture_dir is not None else None,
                'capture_id':capture_id,'created_at':datetime.now(timezone.utc).isoformat()}
        atomic_json(directory/'request.json',record)
        return record

    def load(self,request_id):
        record=json.loads((self.path(request_id)/'request.json').read_text(encoding='utf-8'))
        if (not isinstance(record,dict) or record.get('request_id')!=request_id or
                record.get('state') not in STATES or record.get('purpose') not in {'inference','model_upload'} or
                not isinstance(record.get('output_names'),list)):
            raise ValueError('invalid request journal')
        return record

    @contextmanager
    def lock(self,request_id):
        fd=os.open(self.path(request_id)/'.lock',os.O_RDWR|os.O_CREAT,0o600)
        try:
            fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
            yield
        finally:
            fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)

    def update(self,request_id,state=None,**fields):
        record=self.load(request_id)
        if state is not None:
            if state not in STATES:raise ValueError('invalid journal state')
            allowed={'NOT_SUBMITTED':{'NOT_SUBMITTED','SUBMITTING'},
                     'SUBMITTING':{'NOT_SUBMITTED','SUBMITTING','ACCEPTED','UNKNOWN','COMPLETED','SERVICE_FAILED'},
                     'ACCEPTED':{'ACCEPTED','UNKNOWN','COMPLETED','SERVICE_FAILED'},
                     'UNKNOWN':{'UNKNOWN','COMPLETED','SERVICE_FAILED'},
                     'COMPLETED':{'COMPLETED'},'SERVICE_FAILED':{'SERVICE_FAILED'}}
            if state not in allowed[record['state']]:raise ValueError('invalid request state transition')
            record['state']=state
        if set(fields)-{'reply_queue','request_body_sha256','status_code','response_id','response',
                        'last_error','queue_cleanup','response_id_mismatch','broker_confirmed'}:
            raise ValueError('non-allowlisted journal metadata')
        record.update(fields);record['updated_at']=datetime.now(timezone.utc).isoformat()
        atomic_json(self.path(request_id)/'request.json',record)
        return record

    def recover(self,request_id):
        record=self.load(request_id)
        if record['state'] in {'SUBMITTING','ACCEPTED'}:
            record=self.update(request_id,'UNKNOWN',last_error={'code':'process_restarted_before_terminal_response'})
        return record

    def complete(self,request_id,outputs,*,status_code,response_id):
        if response_id!=request_id:raise ValueError('uncorrelated response')
        if type(status_code) is not int:raise ValueError('numeric status required')
        from .notebook import _arrays
        record=self.load(request_id)
        if outputs:
            arrays=_arrays(outputs,max_bytes=128*1024*1024)
            if not set(arrays).issubset(record['output_names']):raise ValueError('unselected response tensor')
        else:arrays={}
        if status_code==0 and set(arrays)!=set(record['output_names']):raise ValueError('missing selected output')
        directory=self.path(request_id);path=directory/'response.npz'
        temporary=directory/('.response.'+uuid4().hex+'.tmp')
        try:
            fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,'wb') as file:
                np.savez(file,**arrays);file.flush();os.fsync(file.fileno())
            os.replace(temporary,path);fsync_directory(directory)
        finally:temporary.unlink(missing_ok=True)
        response={'file':'response.npz','sha256':_hash(path),'tensors':tensor_metadata(arrays)}
        return self.update(request_id,'COMPLETED' if status_code==0 else 'SERVICE_FAILED',
                           status_code=status_code,response_id=response_id,response=response)

    def outputs(self,request_id):
        record=self.load(request_id)
        if record['state'] not in TERMINAL:raise ValueError('response not terminal')
        artifact=record['response']
        if artifact.get('file')!='response.npz':raise ValueError('invalid response artifact')
        path=self.path(request_id)/'response.npz'
        if _hash(path)!=artifact['sha256']:raise ValueError('response checksum mismatch')
        with np.load(path,allow_pickle=False) as archive:
            if len(archive.files)!=len(set(archive.files)):raise ValueError('duplicate response array')
            arrays={name:archive[name].copy(order='C') for name in archive.files}
        if tensor_metadata(arrays)!=artifact['tensors']:raise ValueError('response tensor checksum mismatch')
        if any(a.dtype.kind not in 'buif' or not np.isfinite(a).all() for a in arrays.values()):
            raise ValueError('invalid numeric response')
        return arrays
