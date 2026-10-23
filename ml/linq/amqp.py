"""One-request AMQP transport bound explicitly to the organizer's notebook.

Requires EXACT tpu_pycloud_format==0.0.1. No replacement codec, guessed PyTask
kwargs, guessed routing, credentials, or automatic publish retry is provided.
"""
from __future__ import annotations

import argparse
from collections.abc import Mapping
from contextlib import contextmanager
import copy
from dataclasses import dataclass
import importlib
import importlib.metadata
import importlib.util
import os
import re
import json
import hashlib
import math
from pathlib import Path
from time import monotonic
from uuid import UUID, uuid4

import numpy as np

from .notebook import capture_call, _arrays, _file_hash, _name, _save_report
from .journal import DEFAULT_JOURNAL_DIR, TERMINAL, RequestJournal, atomic_json, fsync_directory

FORMAT_VERSION = "0.0.1"
_MAX_BYTES = 128 * 1024 * 1024


class AmqpError(RuntimeError):
    """Only stable codes and allowlisted numeric/UUID diagnostics are exposed."""
    def __init__(self, code, phase, *, exception_type=None, status_code=None):
        super().__init__(code)
        self.details = {"code": code, "phase": phase}
        if exception_type is not None:
            self.details["exception_type"] = exception_type
        if status_code is not None:
            self.details["status_code"] = status_code


@dataclass(repr=False)
class AmqpBinding:
    """User-owned actual-notebook bindings; never print this object/parameters.

    task_factory(request_id, reply_queue, inputs, program) -> official fmt.PyTask
    get_response_id(decoded_response, AMQP_properties) returns explicit ID. Other
    selectors take decoded response, returning numeric status and
    ONLY selected named numeric output arrays. No response structure is assumed.
    request exchange/routing and reply policy have no service-specific defaults.
    """
    parameters: object
    task_factory: object
    get_response_id: object
    get_status: object
    get_outputs: object
    output_names: object
    request_exchange: str
    request_routing_key: str
    reply_policy: str
    reply_setup: object = None  # (channel, generated_reply_queue, request_id)
    properties_factory: object = None  # (request_id, generated_reply_queue, program)
    program_file: object = None  # explicit LOCAL bytes corresponding to remote identifier
    format_source_manifest: object = None  # reviewed source-only official-format inventory
    reply_queue_factory: object = None  # explicit (request_id)->queue_name, or server-generated
    get_service_error: object = None  # optional explicit worker error selector, never public JSON
    reply_exclusive: bool = True  # generic policy; official notebook explicitly uses False


def _load_format(source_manifest=None):
    try:
        version = importlib.metadata.version("tpu_pycloud_format")
    except importlib.metadata.PackageNotFoundError:
        version = None
    except Exception as error:
        raise AmqpError("official_format_unavailable", "load_format", exception_type=type(error).__name__) from None
    if version is not None and version != FORMAT_VERSION:
        raise AmqpError("official_format_wrong_version", "load_format")
    if source_manifest is not None:
        try:
            audit = json.loads(Path(source_manifest).read_text(encoding="utf-8"))
            expected = {"__init__.py", "_io.py", "headers.py", "message_pb2.py", "message.proto"}
            if (audit.get("distribution") != "tpu_pycloud_format" or audit.get("version") != FORMAT_VERSION or
                    not isinstance(audit.get("files"), dict) or set(audit["files"]) != expected):
                raise ValueError("invalid source inventory")
            spec = importlib.util.find_spec("tpu_pycloud_format")
            if spec is None or not spec.origin:
                raise ValueError("official source module unavailable")
            directory = Path(spec.origin).resolve().parent
            if {str(path.relative_to(directory)) for path in directory.rglob("*.py")} != expected - {"message.proto"}:
                raise ValueError("unreviewed active Python source")
            for name, digest in audit["files"].items():
                path = (directory / name).resolve()
                if not path.is_relative_to(directory) or _file_hash(path) != digest:
                    raise ValueError("official source hash mismatch")
        except Exception as error:
            raise AmqpError("official_format_source_verification_failed", "load_format",
                            exception_type=type(error).__name__) from None
    elif version is None:
        raise AmqpError("official_format_missing", "load_format")
    try:
        fmt = importlib.import_module("tpu_pycloud_format")
    except Exception as error:
        raise AmqpError("official_format_unavailable", "load_format", exception_type=type(error).__name__) from None
    if (not isinstance(getattr(fmt, "PyTask", None), type) or
            not callable(getattr(fmt, "serialize", None)) or
            not callable(getattr(fmt, "deserialize", None))):
        raise AmqpError("official_format_api_mismatch", "load_format")
    return fmt


def _validate_binding(binding):
    if not isinstance(binding, AmqpBinding):
        if isinstance(binding, Mapping):
            try:
                binding = AmqpBinding(**binding)
            except Exception:
                raise AmqpError("invalid_binding", "validate_binding") from None
        else:
            raise AmqpError("invalid_binding", "validate_binding")
    if type(binding.reply_exclusive) is not bool:
        raise AmqpError("explicit_reply_exclusive_policy_required", "validate_binding")
    callbacks = (binding.task_factory, binding.get_response_id, binding.get_status, binding.get_outputs)
    if not all(callable(fn) for fn in callbacks):
        raise AmqpError("explicit_binding_callbacks_required", "validate_binding")
    if not isinstance(binding.request_exchange, str) or not isinstance(binding.request_routing_key, str):
        raise AmqpError("explicit_request_routing_required", "validate_binding")
    if binding.reply_policy == "default_exchange":
        if binding.reply_setup is not None:
            raise AmqpError("ambiguous_reply_policy", "validate_binding")
    elif binding.reply_policy == "custom_setup":
        if not callable(binding.reply_setup):
            raise AmqpError("explicit_reply_setup_required", "validate_binding")
    else:
        raise AmqpError("explicit_reply_policy_required", "validate_binding")
    if binding.reply_queue_factory is not None and not callable(binding.reply_queue_factory):
        raise AmqpError("invalid_reply_queue_factory", "validate_binding")
    if binding.get_service_error is not None and not callable(binding.get_service_error):
        raise AmqpError("invalid_service_error_selector", "validate_binding")
    if binding.properties_factory is not None and not callable(binding.properties_factory):
        raise AmqpError("invalid_properties_factory", "validate_binding")
    if not isinstance(binding.output_names, (tuple, list)) or not binding.output_names:
        raise AmqpError("explicit_output_names_required", "validate_binding")
    try:
        names = [_name(name) for name in binding.output_names]
    except Exception:
        raise AmqpError("invalid_output_names", "validate_binding") from None
    if len(set(names)) != len(names):
        raise AmqpError("duplicate_output_names", "validate_binding")
    return binding


def _connection_parameters(original, timeout, host, port):
    """Copy supplied credentials/TLS unchanged; enforce current loopback tunnel."""
    if host != "127.0.0.1" or port != 15672:
        raise AmqpError("loopback_tunnel_127_0_0_1_15672_required", "connection_parameters")
    try:
        params = copy.copy(original)
        params.host, params.port = host, port
        # One attempt; TCP/socket, connection stack and broker-blocked waits bounded.
        params.connection_attempts, params.retry_delay = 1, 0
        params.socket_timeout = min(5.0, timeout / 2)
        params.stack_timeout = timeout
        params.blocked_connection_timeout = min(5.0, timeout)
        params.heartbeat = 5  # this session only; detect a blackholed tunnel without indefinite inherited heartbeat
        return params
    except Exception as error:
        raise AmqpError("invalid_connection_parameters", "connection_parameters", exception_type=type(error).__name__) from None


def _service_error_excerpt(value, parameters):
    """Allow only bounded sanitized worker error text, never worker metadata."""
    if not isinstance(value, str):
        return None
    # Explicitly supplied credentials only; no environment/store inspection here.
    credentials = getattr(parameters, "credentials", None)
    secrets = (getattr(credentials, "password", None),
               getattr(credentials, "username", None), os.environ.get("LINQ_LOGIN"))
    for secret in secrets:
        if isinstance(secret, str) and secret:
            value = value.replace(secret, "[redacted]")
    value = re.sub(r"(?i)([a-z][a-z0-9+.-]*://)[^/\s@]+@", r"\1[redacted]@", value)
    value = re.sub(r"(?i)(password|passwd|token|secret|authorization|cookie|api[_-]?key)(\s*[:=]\s*)([^&\s;]+)",
                   lambda match: match[1] + match[2] + "[redacted]", value)
    return value[:1024]


TIMING_KEYS=("connection_setup_ms","serialize_ms","publish_confirm_ms","response_wait_ms","close_ms","total_ms")


@contextmanager
def _measure(summary,key):
    started=monotonic()
    try:yield
    finally:
        elapsed=max(0.0,(monotonic()-started)*1000)
        if not math.isfinite(elapsed):raise AmqpError('invalid_clock_interval','timing')
        summary['timings'][key]=summary['timings'].get(key,0.0)+elapsed


class AmqpRunner:
    """One publish plus durable intent; recovery only receives the original UUID."""
    def __init__(self, binding=None, program=None, *, timeout=30.0, host="127.0.0.1", port=15672,
                 journal_dir=DEFAULT_JOURNAL_DIR, purpose="inference", capture_dir=None):
        if (not isinstance(timeout,(int,float)) or isinstance(timeout,bool) or
                not math.isfinite(timeout) or timeout<=0):
            raise AmqpError("positive_finite_timeout_required","configuration")
        if program is not None and (not isinstance(program,str) or not program):
            raise AmqpError("explicit_program_identifier_required","configuration")
        if purpose not in {"inference","model_upload"}:
            raise AmqpError("invalid_request_purpose","configuration")
        self.binding=None if binding is None else _validate_binding(binding)
        if self.binding is not None and self.binding.reply_exclusive:
            raise AmqpError("nonexclusive_reply_queue_required_for_recovery","configuration")
        self.program,self.timeout,self.host,self.port=program,float(timeout),host,port
        self.journal=RequestJournal(journal_dir)
        self.purpose,self.capture_dir=purpose,capture_dir
        self.last_response=None
        self._private_service_error=None

    def _summary(self,request_id,record=None):
        summary={"request_id":request_id,"status":"not_started","status_code":None,
            "publish_attempted":False,"publish_confirmed":False,"remote_completion":"not_submitted",
            "required_format_version":FORMAT_VERSION,"timings":{key:0.0 for key in TIMING_KEYS},"outputs":{},
            "latency_kind":"initial_call",
            "journal_request_id":request_id,"journal_path":str(self.journal.path(request_id)),
            "journal_state":"NOT_SUBMITTED","purpose":self.purpose,"broker_ready":False,"durable_response":False}
        if record is not None:
            summary.update(journal_state=record['state'],purpose=record['purpose'],
                publish_attempted=record['state']!='NOT_SUBMITTED',
                publish_confirmed=record.get('broker_confirmed',False),status_code=record.get('status_code'))
        self.last_response=summary
        return summary

    def _capture_context(self):
        if self.capture_dir is None:return None
        directory=Path(self.capture_dir).resolve()
        path=directory/'capture.json'
        if not path.exists():return None
        value=json.loads(path.read_text())
        if value.get('status')!='pending_call' or value.get('call_completed') is not False:
            raise AmqpError('capture_context_not_pending','associate_capture')
        value_id=value.get('capture_id')
        if not isinstance(value_id,str) or str(UUID(value_id))!=value_id:
            raise AmqpError('invalid_capture_context','associate_capture')
        return value_id

    def _associate(self,request_id,capture_id):
        if self.capture_dir is None:return
        directory=Path(self.capture_dir).resolve();directory.mkdir(parents=True,exist_ok=True,mode=0o700)
        # Persist the context's parent entry too, not only files inside the context.
        fsync_directory(directory.parent)
        pointer={'schema_version':'1.0','journal_request_id':request_id,
                 'journal_path':str(self.journal.path(request_id)),'purpose':self.purpose}
        path=directory/'request-pointer.json'
        if path.exists():
            old=json.loads(path.read_text())
            if old.get('journal_request_id')!=request_id:
                raise AmqpError('context_already_has_request','associate_capture')
        atomic_json(path,pointer)
        if capture_id is not None:
            path=directory/'capture.json';value=json.loads(path.read_text())
            if value.get('capture_id')!=capture_id:
                raise AmqpError('capture_context_changed','associate_capture')
            value.update(journal_request_id=request_id,journal_path=pointer['journal_path'])
            atomic_json(path,value)

    def _open(self,timeout=None):
        fmt=_load_format(self.binding.format_source_manifest)
        pika=importlib.import_module('pika')
        parameters=_connection_parameters(self.binding.parameters,self.timeout if timeout is None else timeout,self.host,self.port)
        return fmt,pika,pika.BlockingConnection(parameters)

    def _error(self,request_id,error,phase,publish_possible):
        summary=self.last_response
        details=error.details if isinstance(error,AmqpError) else {
            'code':'transport_or_binding_failure','phase':phase,'exception_type':type(error).__name__}
        summary.update(status='failed',error=dict(details))
        if details['code'].startswith('official_format_'):
            summary['next_action']='provide_exact_official_tpu_pycloud_format_0_0_1'
        try:
            record=self.journal.load(request_id)
            if record['state'] not in TERMINAL:
                record=self.journal.update(request_id,'UNKNOWN' if publish_possible else 'NOT_SUBMITTED',
                                           last_error=dict(details))
            summary['journal_state']=record['state']
        except Exception as journal_error:
            summary['journal_error_type']=type(journal_error).__name__
            if publish_possible:summary['journal_state']='UNKNOWN'
        return error if isinstance(error,AmqpError) else AmqpError(**{
            'code':details['code'],'phase':details['phase'],'exception_type':details['exception_type']})

    def _cleanup(self,request_id,connection,channel,reply_queue):
        with _measure(self.last_response,'close_ms'):
            self._cleanup_resources(request_id,connection,channel,reply_queue)

    def _cleanup_resources(self,request_id,connection,channel,reply_queue):
        summary=self.last_response
        try:state=self.journal.load(request_id)['state']
        except Exception:state=summary.get('journal_state','UNKNOWN')
        if channel is not None and reply_queue is not None:
            if state=='NOT_SUBMITTED' or (state in TERMINAL and summary.get('durable_response') is True):
                try:
                    channel.queue_delete(queue=reply_queue)
                    summary['reply_queue_cleanup']='deleted'
                except Exception as error:
                    summary['reply_queue_cleanup']='failed';summary['queue_cleanup_error_type']=type(error).__name__
            else:summary['reply_queue_cleanup']='retained_for_recovery'
        if connection is not None:
            try:connection.close()
            except Exception as error:summary['close_error_type']=type(error).__name__

    def _receive(self,request_id,fmt,connection,channel,reply_queue,deadline):
        summary=self.last_response
        while True:
            with _measure(summary,'response_wait_ms'):
                remaining=deadline-monotonic()
                if remaining<=0:raise AmqpError('response_timeout','wait_response')
                method,properties,body=channel.basic_get(queue=reply_queue,auto_ack=False)
                if method is None:connection.process_data_events(time_limit=min(.05,remaining))
            if method is None:continue
            if not isinstance(body,(bytes,bytearray)) or len(body)>_MAX_BYTES:
                raise AmqpError('invalid_serialized_response','deserialize_response')
            response=fmt.deserialize(bytes(body))
            response_id=self.binding.get_response_id(response,properties)
            try:
                UUID(response_id)
                summary['response_id']=response_id if isinstance(response_id,str) and len(response_id)<=36 else None
            except (ValueError,TypeError,AttributeError):summary['response_id']=None
            if response_id!=request_id:
                self.journal.update(request_id,response_id_mismatch=summary['response_id'])
                # Leave foreign/malformed responses UNACKED; closing requeues them.
                raise AmqpError('response_id_mismatch','correlate_response')
            status=self.binding.get_status(response)
            if not isinstance(status,(int,np.integer)) or isinstance(status,(bool,np.bool_)):
                raise AmqpError('numeric_status_required','check_status')
            status=int(status);summary.update(status_code=status,remote_completion='response_received')
            if status:
                if self.binding.get_service_error is not None:
                    message=self.binding.get_service_error(response)
                    if isinstance(message,str):
                        self._private_service_error=_service_error_excerpt(message,self.binding.parameters)
                        summary['service_error']=self._private_service_error
                try:outputs=_arrays(self.binding.get_outputs(response),names=self.binding.output_names,max_bytes=_MAX_BYTES)
                except Exception:outputs={}
            else:outputs=_arrays(self.binding.get_outputs(response),names=self.binding.output_names,max_bytes=_MAX_BYTES)
            # Fsync numeric response AND terminal metadata before any broker ACK.
            record=self.journal.complete(request_id,outputs,status_code=status,response_id=response_id)
            summary['journal_state']=record['state']
            summary['durable_response']=True
            summary['outputs']={name:{'shape':list(value.shape),'dtype':value.dtype.name} for name,value in outputs.items()}
            try:channel.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as error:summary['ack_error_type']=type(error).__name__
            if status:raise AmqpError('service_reported_failure','check_status',status_code=status)
            summary['status']='completed'
            return outputs

    def __call__(self,inputs):
        started=monotonic();deadline=started+self.timeout;request_id=str(uuid4())
        summary=self._summary(request_id)
        connection=channel=reply_queue=None;publish_possible=False;phase='validate_inputs'
        try:
            if self.binding is None or self.program is None:
                raise AmqpError('explicit_binding_and_program_required','configuration')
            arrays=_arrays(inputs,max_bytes=_MAX_BYTES)
            capture_id=self._capture_context()
            requested_queue='' if self.binding.reply_queue_factory is None else self.binding.reply_queue_factory(request_id)
            if not isinstance(requested_queue,str):raise AmqpError('invalid_reply_queue_name','declare_reply_queue')
            self.journal.create(request_id,purpose=self.purpose,
                program_uri_sha256=hashlib.sha256(self.program.encode()).hexdigest(),inputs=arrays,
                output_names=self.binding.output_names,reply_queue=requested_queue or None,
                capture_dir=self.capture_dir,capture_id=capture_id)
            with self.journal.lock(request_id):
                phase='associate_capture';self._associate(request_id,capture_id)
                try:
                    with _measure(summary,'connection_setup_ms'):
                        phase='open_connection';fmt,pika,connection=self._open();channel=connection.channel()
                        declared=channel.queue_declare(queue=requested_queue,durable=False,exclusive=False,auto_delete=True)
                        reply_queue=declared.method.queue
                        if not isinstance(reply_queue,str) or not reply_queue:raise AmqpError('invalid_reply_queue','declare_reply_queue')
                        self.journal.update(request_id,reply_queue=reply_queue)
                        phase='reply_setup'
                        if self.binding.reply_policy=='custom_setup':self.binding.reply_setup(channel,reply_queue,request_id)
                        summary['broker_ready']=True
                    phase='build_task';task=self.binding.task_factory(request_id,reply_queue,arrays,self.program)
                    if not isinstance(task,fmt.PyTask):raise AmqpError('task_factory_must_return_official_pytask',phase)
                    phase='serialize_request'
                    with _measure(summary,'serialize_ms'):body=fmt.serialize(task)
                    if not isinstance(body,(bytes,bytearray)) or len(body)>_MAX_BYTES:
                        raise AmqpError('invalid_serialized_request',phase)
                    phase='publish_properties'
                    properties=(pika.BasicProperties(correlation_id=request_id,reply_to=reply_queue)
                        if self.binding.properties_factory is None else
                        self.binding.properties_factory(request_id,reply_queue,self.program))
                    with _measure(summary,'connection_setup_ms'):channel.confirm_delivery()
                    if monotonic()>=deadline:raise AmqpError('deadline_before_publish','confirm_mode')
                    phase='journal_submitting'
                    self.journal.update(request_id,'SUBMITTING',request_body_sha256=hashlib.sha256(body).hexdigest())
                    summary.update(journal_state='SUBMITTING',status='pending_response',
                                   publish_attempted=True,remote_completion='unknown')
                    phase='publish';publish_possible=True
                    with _measure(summary,'publish_confirm_ms'):
                        confirmed=channel.basic_publish(exchange=self.binding.request_exchange,
                            routing_key=self.binding.request_routing_key,body=bytes(body),properties=properties,mandatory=True)
                    if confirmed is False:raise AmqpError('publish_not_confirmed',phase)
                    summary['publish_confirmed']=True
                    phase='journal_accepted';self.journal.update(request_id,'ACCEPTED',broker_confirmed=True)
                    summary['journal_state']='ACCEPTED';phase='wait_response'
                    return self._receive(request_id,fmt,connection,channel,reply_queue,deadline)
                except Exception as error:
                    raise self._error(request_id,error,phase,publish_possible) from None
                finally:self._cleanup(request_id,connection,channel,reply_queue)
        except Exception as error:
            if summary['status']!='failed':raise self._error(request_id,error,phase,publish_possible) from None
            raise
        finally:summary['timings']['total_ms']=(monotonic()-started)*1000

    def reconcile(self,request_id,*,timeout=None):
        """Receive original retained queue only; NEVER build/serialize/publish tasks."""
        started=monotonic();duration=self.timeout if timeout is None else timeout
        if not isinstance(duration,(int,float)) or isinstance(duration,bool) or not math.isfinite(duration) or duration<=0:
            raise AmqpError('positive_finite_timeout_required','configuration')
        record=self.journal.load(request_id);summary=self._summary(request_id,record)
        summary['reconcile_only']=True
        summary['latency_kind']='recovery_only'
        connection=channel=None;reply_queue=record.get('reply_queue')
        try:
            with self.journal.lock(request_id):
                record=self.journal.recover(request_id);summary['journal_state']=record['state']
                if record['state'] in TERMINAL:
                    outputs=self.journal.outputs(request_id)
                    summary.update(status='completed' if record['state']=='COMPLETED' else 'failed',
                        status_code=record['status_code'],response_id=record['response_id'],
                        remote_completion='response_received',cached_response=True,durable_response=True,latency_kind='cached_response',
                        outputs={name:{'shape':list(value.shape),'dtype':value.dtype.name} for name,value in outputs.items()})
                    if record['state']=='SERVICE_FAILED':
                        raise AmqpError('service_reported_failure','cached_response',status_code=record['status_code'])
                    return outputs
                if record['state']=='NOT_SUBMITTED':raise AmqpError('request_was_not_submitted','reconcile')
                if self.binding is None:raise AmqpError('binding_required_for_pending_reconcile','reconcile')
                if set(record['output_names'])!=set(self.binding.output_names):
                    raise AmqpError('reconcile_output_names_mismatch','reconcile')
                if not isinstance(reply_queue,str) or not reply_queue:
                    raise AmqpError('retained_reply_queue_missing','reconcile')
                try:
                    with _measure(summary,'connection_setup_ms'):
                        fmt,_,connection=self._open(timeout=duration);channel=connection.channel()
                        summary['broker_ready']=True
                    # No queue declaration/binding/task serialization/publish here.
                    return self._receive(request_id,fmt,connection,channel,reply_queue,started+duration)
                except Exception as error:
                    raise self._error(request_id,error,'reconcile',True) from None
                finally:self._cleanup(request_id,connection,channel,reply_queue)
        finally:summary['timings']['total_ms']=(monotonic()-started)*1000


def official_binding(parameters, *, request_exchange, request_routing_key, reply_exchange,
                     output_names, format_source_manifest=None, program_file=None, reply_queue_factory=None):
    """Use the INSPECTED official format; routing/URI/credentials stay explicit.

    PyTask(data=inputs) is the actual exported dataclass. deserialize returns
    (data, metadata, worker_data). IDs/URI/reply routing are official AMQP headers,
    not invented PyTask fields. No worker error string/metadata is exported.
    The worker's reply exchange must be supplied from the actual deployment.
    """
    fmt = _load_format(format_source_manifest)
    names = ("MESSAGE_ID_ATTR_NAME", "RESPONSE_ROUTING_KEYS_ATTR_NAME", "TARGET_URI_ATTR_NAME")
    if tuple(getattr(fmt, name, None) for name in names) != (
            "tpu_pycloud_message_id", "response_routing_keys", "uri"):
        raise AmqpError("official_header_constants_mismatch", "create_official_binding")
    if not isinstance(reply_exchange, str):
        raise AmqpError("explicit_reply_exchange_required", "create_official_binding")
    def task_factory(request_id, reply_queue, inputs, program):
        return fmt.PyTask(data=inputs)
    def properties_factory(request_id, reply_queue, program):
        pika = importlib.import_module("pika")
        return pika.BasicProperties(headers={fmt.MESSAGE_ID_ATTR_NAME: request_id,
            fmt.RESPONSE_ROUTING_KEYS_ATTR_NAME: json.dumps([reply_queue]),
            fmt.TARGET_URI_ATTR_NAME: program})
    def response_id(response, properties):
        headers = getattr(properties, "headers", None)
        return headers.get(fmt.MESSAGE_ID_ATTR_NAME) if isinstance(headers, Mapping) else None
    def checked_response(response):
        if not isinstance(response, tuple) or len(response) != 3 or not isinstance(response[2], Mapping):
            raise AmqpError("official_response_tuple_required", "select_response")
        return response
    def status(response):
        return checked_response(response)[2]["status_code"]
    def service_error(response):
        return checked_response(response)[2].get("error_message", "")
    def outputs(response):
        data = checked_response(response)[0]
        if not isinstance(data, Mapping):
            raise AmqpError("numeric_response_mapping_required", "select_outputs")
        return {name: data[name] for name in output_names}
    def reply_setup(channel, queue, request_id):
        channel.queue_bind(queue=queue, exchange=reply_exchange, routing_key=queue)
    return AmqpBinding(parameters=parameters, task_factory=task_factory,
        get_response_id=response_id, get_status=status, get_outputs=outputs,
        output_names=output_names, request_exchange=request_exchange,
        request_routing_key=request_routing_key,
        reply_policy="default_exchange" if reply_exchange == "" else "custom_setup",
        reply_setup=None if reply_exchange == "" else reply_setup,
        properties_factory=properties_factory, program_file=program_file,
        format_source_manifest=format_source_manifest, reply_queue_factory=reply_queue_factory,
        get_service_error=service_error, reply_exclusive=False)


def _environment_parameters(config_path=None):
    # Read only an explicitly selected file OR these three documented env keys.
    if config_path is not None:
        try:
            path = Path(config_path)
            if path.stat().st_size > 65536:
                raise ValueError("config too large")
            config = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(config, dict) or set(config) != {"username", "password", "virtual_host"}:
                raise ValueError("invalid config keys")
            username, password, vhost = (config["username"], config["password"], config["virtual_host"])
        except Exception as error:
            raise AmqpError("connection_config_invalid", "configuration", exception_type=type(error).__name__) from None
    else:
        username = os.environ.get("LINQ_AMQP_USERNAME")
        password = os.environ.get("LINQ_AMQP_PASSWORD")
        vhost = os.environ.get("LINQ_AMQP_VHOST")
    if not all(isinstance(value, str) and value for value in (username, password, vhost)):
        raise AmqpError("explicit_broker_credentials_and_vhost_required", "configuration")
    pika = importlib.import_module("pika")
    return pika.ConnectionParameters(host="127.0.0.1", port=15672, virtual_host=vhost,
                                     credentials=pika.PlainCredentials(username, password))


def _load_binding(value):
    try:
        module, name = value.split(":", 1)
        factory = getattr(importlib.import_module(module), name)
        return _validate_binding(factory())
    except AmqpError:
        raise
    except Exception as error:
        raise AmqpError("binding_load_failed", "load_binding", exception_type=type(error).__name__) from None


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise AmqpError("invalid_cli_arguments", "arguments")


def main(argv=None):
    parser = _Parser(description=__doc__)
    parser.add_argument("--binding", help="Optional trusted user-owned module:function returning AmqpBinding")
    parser.add_argument("--format-source-manifest", help="Reviewed source-only official 0.0.1 inventory")
    parser.add_argument("--exchange", help="Actual request exchange; explicitly pass empty string for default exchange")
    parser.add_argument("--routing-key", help="Actual worker request routing key")
    parser.add_argument("--reply-exchange", help="Actual worker reply exchange; explicitly pass empty string for default exchange")
    parser.add_argument("--output-name", action="append", help="Exact numeric response name; repeat for multiple outputs")
    parser.add_argument("--connection-config", help="Explicit private outside-Git JSON: username/password/virtual_host")
    parser.add_argument("--program", "--target-uri", dest="program", help="Exact actual program URI passed verbatim as official uri header")
    parser.add_argument("--login-env", help="Explicit env key containing actual LinQ login for the USER-CONFIRMED stock ResNet URI only")
    parser.add_argument("--notebook-reply-queue", action="store_true", help="Use actual notebook_{request_id[:8]} reply queue")
    parser.add_argument("--save-service-error", action="store_true", help="Preserve bounded worker error text privately outside Git; never stdout")
    parser.add_argument("--program-file", help="Local .tpu bytes for hash; not proof of loaded remote identity")
    parser.add_argument("--input-npz")
    parser.add_argument("--output-dir")
    parser.add_argument("--model-id", default="explicit-amqp-model")
    parser.add_argument("--journal-dir", default=DEFAULT_JOURNAL_DIR)
    parser.add_argument("--purpose", choices=("inference","model_upload"), default="inference")
    parser.add_argument("--reconcile", metavar="UUID", help="Receive/cache existing request only; never publish")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=15672)
    parser.add_argument("--attest-program-match", action="store_true")
    parser.add_argument("--attest-linq-placement", action="store_true")
    runner = None
    try:
        args = parser.parse_args(argv)
        if args.reconcile is not None:
            record=RequestJournal(args.journal_dir).load(args.reconcile)
            runner=AmqpRunner(None,timeout=args.timeout,journal_dir=args.journal_dir)
            if record['state'] not in TERMINAL and record['state']!='NOT_SUBMITTED':
                _load_format(args.format_source_manifest)
                if args.binding:
                    binding=_load_binding(args.binding)
                    if args.format_source_manifest is not None:binding.format_source_manifest=args.format_source_manifest
                else:
                    # Request routes/URI are unused: this path never publishes or binds.
                    binding=official_binding(_environment_parameters(args.connection_config),
                        request_exchange='',request_routing_key='',reply_exchange='',
                        output_names=record['output_names'],format_source_manifest=args.format_source_manifest)
                runner=AmqpRunner(binding,timeout=args.timeout,host=args.host,port=args.port,
                                  journal_dir=args.journal_dir,purpose=record['purpose'])
            runner.reconcile(args.reconcile)
            print(json.dumps({'status':runner.last_response['status'],'response':runner.last_response},allow_nan=False))
            return 0
        if args.input_npz is None or args.output_dir is None:
            raise AmqpError('input_and_output_capture_paths_required','configuration')
        if args.program is not None and args.login_env is not None:
            raise AmqpError("choose_exact_uri_or_explicit_login_env", "configuration")
        if args.program is None:
            if args.login_env is None:
                raise AmqpError("explicit_target_uri_required", "configuration")
            login = os.environ.get(args.login_env)
            if not isinstance(login, str) or not login or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-" for char in login):
                raise AmqpError("valid_explicit_linq_login_required", "configuration")
            # This path was explicitly supplied and confirmed by the user, not inferred.
            args.program = "file:///auto/cache/" + login + "/torch_resnet50_b1_o5_h1m.tpu?raw=False"
        # Useful action error before importing user binding/network dependencies.
        _load_format(args.format_source_manifest)
        if args.binding:
            binding = _load_binding(args.binding)
            if args.format_source_manifest is not None:
                binding.format_source_manifest = args.format_source_manifest
        else:
            if any(value is None for value in (args.exchange, args.routing_key, args.reply_exchange)) or not args.output_name:
                raise AmqpError("explicit_routing_reply_exchange_and_outputs_required", "configuration")
            binding = official_binding(_environment_parameters(args.connection_config),
                request_exchange=args.exchange, request_routing_key=args.routing_key,
                reply_exchange=args.reply_exchange, output_names=args.output_name,
                format_source_manifest=args.format_source_manifest, program_file=args.program_file,
                reply_queue_factory=(lambda request_id: "notebook_" + request_id[:8]) if args.notebook_reply_queue else None)
        local_program = args.program_file or binding.program_file
        if local_program is None:
            raise AmqpError("explicit_local_program_file_required", "configuration")
        with np.load(args.input_npz, allow_pickle=False) as archive:
            if len(set(archive.files)) != len(archive.files):
                raise AmqpError("duplicate_input_name", "load_inputs")
            inputs = _arrays({name: archive[name] for name in archive.files}, max_bytes=_MAX_BYTES)
        runner = AmqpRunner(binding, args.program, timeout=args.timeout, host=args.host, port=args.port,
                            journal_dir=args.journal_dir,purpose=args.purpose,capture_dir=args.output_dir)
        capture = capture_call(runner, inputs=inputs, output_names=list(binding.output_names),
            program_path=local_program, output_dir=args.output_dir, model_id=args.model_id,
            placement_attested=args.attest_linq_placement)
        capture["program_identity"] = {"hash_basis": "provided_local_file",
            "remote_program_match_attested": args.attest_program_match,
            "independently_verified": False}
        directory = Path(args.output_dir)
        path = directory / "capture.json"
        if path.is_file():
            # Never modify a preexisting capture rejected by capture_call.
            stored = json.loads(path.read_text())
            if stored.get("capture_id") == capture["capture_id"]:
                _save_report(path, capture)
                if runner.last_response is not None:
                    _save_report(directory / "response.json", runner.last_response)
                    if args.save_service_error and runner._private_service_error is not None:
                        fd = os.open(directory / "service-error.txt", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                        with os.fdopen(fd, "w", encoding="utf-8") as error_file:
                            error_file.write(runner._private_service_error)
        print(json.dumps({"status": capture["status"], "call_completed": capture["call_completed"],
                          "response": runner.last_response}, allow_nan=False))
        return 0 if capture["status"] == "completed" else 1
    except AmqpError as error:
        value = {"status": "failed", "error": error.details}
        if runner is not None and runner.last_response is not None:value["response"]=runner.last_response
        if error.details["code"].startswith("official_format_"):
            value.update(required_format_version=FORMAT_VERSION,
                         next_action="provide_exact_official_tpu_pycloud_format_0_0_1")
        print(json.dumps(value))
        return 1
    except Exception as error:
        print(json.dumps({"status": "failed", "error": {
            "code": "cli_failure", "exception_type": type(error).__name__}}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
