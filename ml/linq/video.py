"""Durable per-logical-frame factory using the existing AMQP client only."""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
from uuid import UUID

from .amqp import AmqpError, AmqpRunner, _environment_parameters, official_binding
from .backend import PendingRequestError, TerminalRequestError, TensorSpec, safe_transport
from .journal import RequestJournal, TERMINAL, atomic_json, fsync_directory, tensor_metadata
from .notebook import _arrays, _file_hash

_MODELS={
    'helmet-v1':('matvey_helmet-v1.tpu','408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa'),
    'pose-split-v1':('matvey_pose-split-v1.tpu','c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b'),
}


def _specs(values):
    result={}
    for value in values:
        spec=TensorSpec.parse(value)
        if spec.name in result:raise ValueError('duplicate model tensor name')
        result[spec.name]={'shape':list(spec.shape),'dtype':spec.dtype}
    if not result:raise ValueError('explicit tensor specs required')
    return result


def _read(path):
    value=json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value,dict):raise ValueError('invalid logical state')
    return value


def _mkdir_durable(path):
    missing=[];current=Path(path)
    while not current.exists():missing.append(current);current=current.parent
    for directory in reversed(missing):
        directory.mkdir(mode=0o700,exist_ok=True)
        fsync_directory(directory.parent)


class DurableVideoRunner:
    def __init__(self,manifest):
        self.model_id=manifest['model_id']
        if self.model_id not in _MODELS:raise ValueError('unsupported reviewed model')
        expected_name,expected_hash=_MODELS[self.model_id]
        self.program_name=manifest['program_name'];self.program_sha256=manifest['program_sha256']
        # Old names may load existing local terminal journals only. _uri rejects
        # them before any fresh submission; never rename/migrate old journals.
        if self.program_name not in (expected_name,expected_name.removeprefix('matvey_')) or self.program_sha256!=expected_hash:
            raise ValueError('unreviewed TPU program binding')
        if _file_hash(manifest['program_path'])!=expected_hash:raise ValueError('local TPU program changed')
        self.inputs=_specs(manifest['inputs']);self.outputs=_specs(manifest['outputs'])
        self.timeout=manifest.get('timeout',60)
        if not isinstance(self.timeout,(int,float)) or isinstance(self.timeout,bool) or not math.isfinite(self.timeout) or self.timeout<=0:
            raise ValueError('finite positive timeout required')
        self.state_dir=Path(manifest['rpc_state_dir']).resolve()
        self.journal_dir=Path(manifest['journal_dir']).resolve();self.run_dir=self.journal_dir.parent
        if self.state_dir.name!=self.model_id or self.state_dir.parent!=self.run_dir/'rpc':
            raise ValueError('RPC model state and journal must belong to the same run')
        self.format_source_manifest=manifest['format_source_manifest']
        self.store=RequestJournal(self.journal_dir)
        self.last_response=None

    def __enter__(self):return self
    def __exit__(self,*args):return False

    @contextmanager
    def _lock(self):
        _mkdir_durable(self.run_dir)
        fd=os.open(self.run_dir/'.linq-video.lock',os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
        try:
            try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:raise PendingRequestError('linq_busy') from None
            yield
        finally:os.close(fd)

    def _logical(self,inputs,metadata):
        if (not isinstance(metadata,dict) or metadata.get('model_id')!=self.model_id or
                metadata.get('program_sha256')!=self.program_sha256):
            raise ValueError('logical model/program identity mismatch')
        request_id=metadata.get('request_id')
        if not isinstance(request_id,str) or not request_id or len(request_id)>512:
            raise ValueError('logical request identity required')
        arrays=_arrays(inputs,specs=self.inputs,max_bytes=128*1024*1024)
        key=hashlib.sha256(request_id.encode()).hexdigest();context=self.state_dir/key
        expected={'schema_version':'1.0','logical_request_id':request_id,'model_id':self.model_id,
                  'program_sha256':self.program_sha256,'inputs':tensor_metadata(arrays)}
        _mkdir_durable(context)
        path=context/'logical.json'
        if path.exists():
            saved=_read(path)
            if {k:v for k,v in saved.items() if k!='program_uri_sha256'}!=expected:
                raise ValueError('logical request was reused with different inputs or identity')
        else:atomic_json(path,expected)
        return arrays,key,context

    def _pointer_record(self,context):
        pointer=_read(context/'request-pointer.json');request_id=pointer['journal_request_id']
        if not isinstance(request_id,str) or str(UUID(request_id))!=request_id:
            raise ValueError('invalid transport pointer UUID')
        if (pointer.get('schema_version')!='1.0' or pointer.get('purpose')!='inference' or
                Path(pointer['journal_path']).resolve()!=self.store.path(request_id)):
            raise ValueError('invalid transport journal pointer')
        try:
            with self.store.lock(request_id):record=self.store.load(request_id)
        except BlockingIOError:
            raise PendingRequestError('linq_pending',{'request_id':request_id,
                'journal_state':'UNKNOWN','remote_completion':'unknown','journal_path':str(self.store.path(request_id))}) from None
        logical=_read(context/'logical.json')
        logical_model=logical.get('model_id')
        if (logical_model not in _MODELS or logical.get('program_sha256')!=_MODELS[logical_model][1] or
                not isinstance(logical.get('logical_request_id'),str) or
                hashlib.sha256(logical['logical_request_id'].encode()).hexdigest()!=context.name):
            raise ValueError('invalid active logical identity')
        if (record.get('purpose')!='inference' or record.get('capture_dir')!=str(context) or
                record.get('inputs')!=logical['inputs'] or
                (logical_model==self.model_id and set(record['output_names'])!=set(self.outputs)) or
                not isinstance(logical.get('program_uri_sha256'),str) or
                record.get('program_uri_sha256')!=logical['program_uri_sha256']):
            raise ValueError('logical context does not match transport intent')
        return request_id,record

    def _active_context(self):
        path=self.run_dir/'.linq-active.json'
        if not path.exists():return None
        active=_read(path)
        if (active.get('model_id') not in _MODELS or
                not isinstance(active.get('logical_key'),str) or not re.fullmatch('[a-f0-9]{64}',active['logical_key'])):
            raise ValueError('invalid active logical request fence')
        return self.run_dir/'rpc'/active['model_id']/active['logical_key']

    def _check_fresh_admission(self):
        active=self._active_context()
        if active is None or not (active/'request-pointer.json').exists():return
        request_id,record=self._pointer_record(active)
        if record['state'] not in TERMINAL|{'NOT_SUBMITTED'}:
            raise PendingRequestError('linq_pending',{'request_id':request_id,
                'journal_state':record['state'],'remote_completion':'unknown','journal_path':str(self.store.path(request_id))})

    def _uri(self,context):
        login=os.environ.get('LINQ_LOGIN')
        if (not isinstance(login,str) or not re.fullmatch(r'[A-Za-z0-9_@.+-]{1,128}',login) or login in {'.','..'}):
            raise PendingRequestError('linq_not_submitted',{'journal_state':'NOT_SUBMITTED','remote_completion':'not_submitted'})
        from .namespace import program_uri
        try:uri=program_uri(login,self.program_name)
        except ValueError:raise PendingRequestError('linq_not_submitted') from None
        value=_read(context/'logical.json');digest=hashlib.sha256(uri.encode()).hexdigest()
        if 'program_uri_sha256' in value and value['program_uri_sha256']!=digest:
            raise ValueError('runtime namespace changed for existing logical request')
        if 'program_uri_sha256' not in value:
            value['program_uri_sha256']=digest;atomic_json(context/'logical.json',value)
        return uri

    def _binding(self):
        return official_binding(_environment_parameters(),request_exchange='tpu.direct',
            request_routing_key='input',reply_exchange='tpu.direct',output_names=list(self.outputs),
            format_source_manifest=self.format_source_manifest,
            owner_login=os.environ.get('LINQ_LOGIN'))

    @staticmethod
    def _provenance(summary):
        value=dict(summary)
        value['latency_kind']=('cached_response' if value.get('cached_response') else
                               'recovery_only' if value.get('reconcile_only') else 'initial_call')
        return safe_transport(value)

    def _archive_unsent(self,context,request_id):
        attempts=context/'attempts';attempts.mkdir(exist_ok=True,mode=0o700)
        target=attempts/(request_id+'.json')
        if target.exists():raise ValueError('unsent attempt already archived')
        (context/'request-pointer.json').rename(target)
        fsync_directory(attempts);fsync_directory(context)

    def __call__(self,inputs,metadata):
        try:return self._run(inputs,metadata)
        except (OSError,ImportError):
            raise PendingRequestError('linq_pending', {'journal_state':'UNKNOWN','remote_completion':'unknown'}) from None

    def _run(self,inputs,metadata):
        with self._lock():
            arrays,key,context=self._logical(inputs,metadata)
            transport=None;known_record=None;known_request_id=None
            try:
                if (context/'request-pointer.json').exists():
                    request_id,record=self._pointer_record(context)
                    known_record=record;known_request_id=request_id
                    if record['state']=='NOT_SUBMITTED':
                        self._archive_unsent(context,request_id)
                        known_record=None;known_request_id=None
                    else:
                        # Terminal cache needs neither runtime credentials nor format import.
                        binding=None if record['state'] in TERMINAL else self._binding()
                        transport=AmqpRunner(binding,journal_dir=self.journal_dir,timeout=self.timeout)
                        outputs=transport.reconcile(request_id)
                        return self._result(outputs,metadata,transport.last_response)
                self._check_fresh_admission()
                uri=self._uri(context)
                binding=self._binding()
                _mkdir_durable(self.journal_dir)
                atomic_json(self.run_dir/'.linq-active.json',{'schema_version':'1.0','model_id':self.model_id,'logical_key':key})
                transport=AmqpRunner(binding,uri,timeout=self.timeout,journal_dir=self.journal_dir,
                                     purpose='inference',capture_dir=context)
                outputs=transport(arrays)
                return self._result(outputs,metadata,transport.last_response)
            except (AmqpError,ImportError,OSError):
                summary=transport.last_response if transport is not None else None
                if summary is None:
                    summary=({'request_id':known_request_id,'journal_state':known_record['state'],
                              'remote_completion':'unknown','journal_path':str(self.store.path(known_request_id))}
                             if known_record is not None else
                             {'journal_state':'NOT_SUBMITTED','remote_completion':'not_submitted'})
                provenance=self._provenance(summary)
                self.last_response=provenance
                if summary.get('journal_state')=='SERVICE_FAILED':raise TerminalRequestError(provenance) from None
                raise PendingRequestError('linq_not_submitted' if summary.get('journal_state')=='NOT_SUBMITTED'
                                          else 'linq_pending',provenance) from None

    def _result(self,outputs,metadata,summary):
        provenance=self._provenance(summary)
        if (provenance.get('journal_state')!='COMPLETED' or provenance.get('status_code')!=0 or
                provenance.get('request_id')!=provenance.get('response_id') or
                provenance.get('remote_completion')!='response_received'):
            raise ValueError('completed correlated transport response required')
        outputs=_arrays(outputs,names=list(self.outputs),specs=self.outputs,max_bytes=128*1024*1024)
        self.last_response=provenance
        return {'outputs':outputs,'execution_witness':{
            'request_id':metadata['request_id'],'model_id':self.model_id,'program_sha256':self.program_sha256,
            'device_kind':'linq_tpu','completed':True},'transport_provenance':provenance}


def create_runner(effective_manifest):
    """Factory for --linq-runner-factory ml.linq.video:create_runner."""
    return DurableVideoRunner(effective_manifest)
