"""Prepare an own-namespace Jupyter bootstrap; publishing is explicit and bounded.

This sends reviewed helper bytes to an own queue only; it is NOT a TPU task,
filesystem access through AMQP or permission to change captain state.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
from uuid import uuid4, UUID
import zipfile
from ml.linq.amqp import _environment_parameters, _connection_parameters
from ml.pipeline.capture_recovery import save_json
from ml.pipeline.runtime_lock import deployment_lock

DEFAULT_ARTIFACTS='/workspace/artifacts/linq-rpc/matvey-bootstrap-v1'
METADATA='matvey_upload_bridge.json'
CELL='matvey_start_jupyter_upload.py'
PAYLOAD='matvey_jupyter_upload_bootstrap.zip'


def _own_bootstrap(name):
    prefix='matvey_bootstrap_'
    if not isinstance(name,str) or not name.startswith(prefix) or str(UUID(name[len(prefix):]))!=name[len(prefix):]:
        raise ValueError('canonical own bootstrap queue required')
    return name


def build(project='/workspace/project',artifacts=DEFAULT_ARTIFACTS):
    project,artifacts=Path(project),Path(artifacts);artifacts.mkdir(parents=True,exist_ok=True)
    metadata_path=artifacts/METADATA
    if metadata_path.exists():raise FileExistsError('own bootstrap already exists; reuse its pinned metadata')
    files={'matvey_upload_agent.py':(project/'ml/linq/upload_agent.py').read_bytes(),
           'matvey_stage_program.py':(project/'ml/pipeline/stage_program.py').read_bytes()}
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,data in files.items():archive.writestr(name,data)
    payload=stream.getvalue();sha=hashlib.sha256(payload).hexdigest();nonce=str(uuid4())
    info={'bootstrap_queue':'matvey_bootstrap_'+nonce,'upload_queue':'matvey_upload_'+nonce,
          'bootstrap_sha256':sha,'scope':'own matvey directory and reviewed model bytes only; no TPU execution',
          'namespace_owner':'matvey','agent_lifetime_seconds':300,'max_upload_messages':4,
          'published':False,'publication_state':'PREPARED'}
    (artifacts/PAYLOAD).write_bytes(payload)
    # Run only in a NEW Matvey notebook/kernel, never captain's active kernel.
    # Existing private connection/header variables are read, never exported.
    code=f'''# OWN MATVEY NOTEBOOK/KERNEL ONLY. Do not run inside captain's notebook.
import os
for _matvey_key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_matvey_key] = "2"
import copy, functools, hashlib, importlib.util, io, json, re, sys, tempfile, types, zipfile
from pathlib import Path
from urllib.parse import urlsplit
import pika
from tpu_pycloud_format import TARGET_URI_ATTR_NAME
try:
    import cv2
    cv2.setNumThreads(1)
except ImportError:
    pass
# Any optional OWN ORT reference session must use these bounded options.
def matvey_ort_session_options():
    import onnxruntime as ort
    options = ort.SessionOptions()
    options.intra_op_num_threads, options.inter_op_num_threads = 2, 1
    return options
_matvey_header_uri = urlsplit(headers[TARGET_URI_ATTR_NAME])
_matvey_parts = _matvey_header_uri.path.split("/")
if (_matvey_header_uri.scheme != "file" or _matvey_header_uri.netloc or
    "%" in _matvey_header_uri.path or len(_matvey_parts) < 5 or
    _matvey_parts[:3] != ["", "auto", "cache"]):
    raise RuntimeError("RUNTIME_ACCOUNT_CONTEXT_REQUIRED")
_matvey_login = _matvey_parts[3]
if not re.fullmatch(r"[A-Za-z0-9_@+-][A-Za-z0-9_@.+-]*", _matvey_login) or ".." in _matvey_login:
    raise RuntimeError("RUNTIME_ACCOUNT_CONTEXT_REQUIRED")
_matvey_cache = Path("/auto/cache") / _matvey_login / "matvey"
_matvey_params = copy.deepcopy(channel.connection._impl.params)
_matvey_params.connection_attempts, _matvey_params.retry_delay = 1, 0
_matvey_params.socket_timeout, _matvey_params.stack_timeout = 5, 60
_matvey_params.blocked_connection_timeout = 5
_matvey_connection = pika.BlockingConnection(_matvey_params)
try:
    _matvey_channel = _matvey_connection.channel()
    _matvey_method, _, _matvey_payload = _matvey_channel.basic_get(queue={info['bootstrap_queue']!r}, auto_ack=False)
    if _matvey_method is None:
        raise RuntimeError("MATVEY_BOOTSTRAP_MESSAGE_NOT_AVAILABLE")
    if hashlib.sha256(_matvey_payload).hexdigest() != {sha!r}:
        raise RuntimeError("MATVEY_BOOTSTRAP_HASH_MISMATCH")
    with zipfile.ZipFile(io.BytesIO(_matvey_payload)) as _matvey_archive:
        if set(_matvey_archive.namelist()) != {{"matvey_upload_agent.py", "matvey_stage_program.py"}}:
            raise RuntimeError("MATVEY_BOOTSTRAP_CONTENTS_MISMATCH")
        # Only hash-pinned stdlib definitions execute before creating own folder.
        _matvey_stager = types.ModuleType("matvey_reviewed_stager")
        _matvey_stager.__file__ = str(_matvey_cache / "matvey_stage_program.py")
        exec(compile(_matvey_archive.read("matvey_stage_program.py"), "matvey_stage_program.py", "exec"), _matvey_stager.__dict__)
        _matvey_stager.owned_cache_directory(_matvey_cache, _matvey_login, create=True)
        _matvey_directory = Path(tempfile.mkdtemp(prefix="matvey_bootstrap_", dir=_matvey_cache))
        for _matvey_filename in ("matvey_upload_agent.py", "matvey_stage_program.py"):
            with (_matvey_directory / _matvey_filename).open("xb") as _matvey_file:
                _matvey_file.write(_matvey_archive.read(_matvey_filename))
    _matvey_channel.basic_ack(delivery_tag=_matvey_method.delivery_tag)
    _matvey_channel.queue_delete(queue={info['bootstrap_queue']!r})
finally:
    _matvey_connection.close()
_matvey_spec = importlib.util.spec_from_file_location("matvey_reviewed_upload", _matvey_directory / "matvey_upload_agent.py")
_matvey_upload = importlib.util.module_from_spec(_matvey_spec)
sys.modules["matvey_reviewed_upload"] = _matvey_upload
_matvey_spec.loader.exec_module(_matvey_upload)
def restart_matvey_upload_agent():
    global matvey_upload_agent
    if "matvey_upload_agent" in globals():
        matvey_upload_agent.stop()
    matvey_upload_agent = _matvey_upload.start_agent(_matvey_params, _matvey_cache,
        {info['upload_queue']!r}, functools.partial(_matvey_stager.stage, owner_login=_matvey_login))
    if not matvey_upload_agent.wait_ready(15):
        raise RuntimeError("MATVEY_UPLOAD_AGENT_NOT_READY:" + str(matvey_upload_agent.last_error_type))
    print({{"status":"UPLOAD_AGENT_READY", "namespace_owner":"matvey", "lifetime_seconds":300, "allowed_models":["helmet","pose-split"]}})
restart_matvey_upload_agent()
'''
    (artifacts/CELL).write_text(code)
    save_json(metadata_path,info)
    return info,payload


def publish(info,payload,artifacts=DEFAULT_ARTIFACTS):
    # Separate control-plane lock; never occupies the TPU admission/recovery fence.
    _validate_publication(info,payload)
    with deployment_lock(Path(artifacts)/'matvey_bootstrap.lock'):
        persisted=Path(artifacts,METADATA)
        if not persisted.is_file():raise ValueError('prepared own metadata required')
        current=json.loads(persisted.read_text())
        if current.get('bootstrap_queue')!=info['bootstrap_queue']:
            raise ValueError('prepared bootstrap association changed')
        _validate_publication(current,payload)
        return _publish(current,payload,artifacts)


def _validate_publication(info,payload):
    # Validate locally before obtaining credentials or opening ANY connection.
    _own_bootstrap(info.get('bootstrap_queue'))
    from ml.linq.namespace import check_upload_queue
    check_upload_queue(info.get('upload_queue'))
    if info.get('namespace_owner')!='matvey' or hashlib.sha256(payload).hexdigest()!=info.get('bootstrap_sha256'):
        raise ValueError('own bootstrap identity/hash mismatch')
    if info.get('published') or info.get('publication_state') in ('PUBLISHING_UNKNOWN','UNKNOWN_REVIEW_OWN_QUEUE'):
        raise ValueError('bootstrap already or possibly published; do not duplicate')
    if info.get('publication_state') not in ('PREPARED','NOT_PUBLISHED'):
        raise ValueError('unknown bootstrap publication state')


def _publish(info,payload,artifacts):
    import pika
    connection=None;attempted=False
    try:
        connection=pika.BlockingConnection(_connection_parameters(_environment_parameters(),60,'127.0.0.1',15672))
        channel=connection.channel()
        channel.queue_declare(queue=info['bootstrap_queue'],durable=False,exclusive=False,auto_delete=False)
        channel.confirm_delivery()
        # Control-plane bytes are also not republished after ambiguity.
        info['publication_state']='PUBLISHING_UNKNOWN'
        save_json(Path(artifacts,METADATA),info)
        attempted=True
        confirmed=channel.basic_publish(exchange='',routing_key=info['bootstrap_queue'],body=payload,mandatory=True,
                                        properties=pika.BasicProperties(expiration='3600000'))
        if confirmed is False:raise RuntimeError('own bootstrap publication not confirmed')
        info['published']=True;info['publication_state']='PUBLISHED'
    except Exception as error:
        # Ambiguous own bootstrap publication must not be repeated blindly.
        info['publish_error_type']=type(error).__name__
        info['publication_state']='UNKNOWN_REVIEW_OWN_QUEUE' if attempted else 'NOT_PUBLISHED'
    finally:
        if connection is not None:
            try:connection.close()
            except Exception:pass
    save_json(Path(artifacts,METADATA),info)
    return info


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifacts',default=DEFAULT_ARTIFACTS)
    parser.add_argument('--prepare-only',action='store_true')
    parser.add_argument('--publish-own-bootstrap',action='store_true',help='only after an own notebook is ready to receive')
    args=parser.parse_args()
    try:
        location=Path(args.artifacts)
        if (location/METADATA).exists():
            info=json.loads((location/METADATA).read_text());payload=(location/PAYLOAD).read_bytes()
            if hashlib.sha256(payload).hexdigest()!=info['bootstrap_sha256']:
                raise ValueError('prepared bootstrap bytes changed')
        else:info,payload=build(artifacts=args.artifacts)
        if args.publish_own_bootstrap and not args.prepare_only:info=publish(info,payload,args.artifacts)
        print(json.dumps({'prepared':True,'published':info['published'],'cell':str(Path(args.artifacts)/CELL),'bootstrap_sha256':info['bootstrap_sha256']}))
        return 0 if not args.publish_own_bootstrap or info['published'] else 1
    except Exception as error:
        print(json.dumps({'status':'NOT_READY','error_type':type(error).__name__}));return 1

if __name__=='__main__':raise SystemExit(main())
