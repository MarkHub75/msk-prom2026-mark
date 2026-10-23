"""Publish a hash-pinned two-file Jupyter bootstrap over the existing bridge.

This is explicit setup for an authorized notebook, NOT a TPU inference request
and NOT a way to infer filesystem rights from RabbitMQ connectivity.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
from uuid import uuid4
import zipfile
from ml.linq.amqp import _environment_parameters,_connection_parameters


def build(project='/workspace/project',artifacts='/workspace/artifacts/linq-rpc'):
    project,artifacts=Path(project),Path(artifacts);artifacts.mkdir(parents=True,exist_ok=True)
    metadata_path=artifacts/'upload-bridge.json'
    if metadata_path.exists():raise FileExistsError('bootstrap metadata already exists; do not create a second bridge silently')
    files={'upload_agent.py':(project/'ml/linq/upload_agent.py').read_bytes(),
           'stage_program.py':(project/'ml/pipeline/stage_program.py').read_bytes()}
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,data in files.items():archive.writestr(name,data)
    payload=stream.getvalue();sha=hashlib.sha256(payload).hexdigest();nonce=uuid4().hex
    info={'bootstrap_queue':'notebook_bootstrap_'+nonce,'upload_queue':'notebook_upload_'+nonce,
          'bootstrap_sha256':sha,'scope':'two reviewed program files only; requires explicit Jupyter startup',
          'agent_lifetime_seconds':300,'max_upload_messages':4,'published':False}
    (artifacts/'jupyter-upload-bootstrap.zip').write_bytes(payload)
    # No account or broker credential value appears in the code or metadata.
    code=f'''# Run ONCE in the already authenticated stock LinQ notebook on Arch.
import copy, hashlib, importlib.util, io, json, sys, tempfile, zipfile
from pathlib import Path
from urllib.parse import urlsplit, unquote
import pika
from tpu_pycloud_format import TARGET_URI_ATTR_NAME
_mos_stock = urlsplit(headers[TARGET_URI_ATTR_NAME])
_mos_cache = Path(unquote(_mos_stock.path)).parent.resolve()
if (_mos_stock.scheme != "file" or _mos_stock.netloc or
    Path(unquote(_mos_stock.path)).name != "torch_resnet50_b1_o5_h1m.tpu" or
    not _mos_cache.is_relative_to(Path("/auto/cache").resolve()) or
    not (_mos_cache / "torch_resnet50_b1_o5_h1m.tpu").is_file()):
    raise RuntimeError("CONFIRMED_STOCK_CACHE_NOT_VISIBLE_IN_JUPYTER")
_mos_params = copy.deepcopy(channel.connection._impl.params)
_mos_params.connection_attempts, _mos_params.retry_delay = 1, 0
_mos_params.socket_timeout, _mos_params.stack_timeout = 5, 60
_mos_params.blocked_connection_timeout = 5
_mos_connection = pika.BlockingConnection(_mos_params)
try:
    _mos_channel = _mos_connection.channel()
    _mos_method, _, _mos_payload = _mos_channel.basic_get(queue={info['bootstrap_queue']!r}, auto_ack=False)
    if _mos_method is None:
        raise RuntimeError("BOOTSTRAP_MESSAGE_NOT_AVAILABLE")
    if hashlib.sha256(_mos_payload).hexdigest() != {sha!r}:
        raise RuntimeError("BOOTSTRAP_HASH_MISMATCH")
    _mos_directory = Path(tempfile.mkdtemp(prefix="mosprom-upload-"))
    with zipfile.ZipFile(io.BytesIO(_mos_payload)) as _mos_archive:
        if set(_mos_archive.namelist()) != {{"upload_agent.py", "stage_program.py"}}:
            raise RuntimeError("BOOTSTRAP_CONTENTS_MISMATCH")
        _mos_archive.extractall(_mos_directory)
    _mos_channel.basic_ack(delivery_tag=_mos_method.delivery_tag)
    _mos_channel.queue_delete(queue={info['bootstrap_queue']!r})
finally:
    _mos_connection.close()
def _mos_load(name, filename):
    spec = importlib.util.spec_from_file_location(name, _mos_directory / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
_mos_upload = _mos_load("mosprom_reviewed_upload", "upload_agent.py")
_mos_stage = _mos_load("mosprom_reviewed_stager", "stage_program.py")
def restart_linq_upload_agent():
    global mosprom_upload_agent
    if "mosprom_upload_agent" in globals():
        mosprom_upload_agent.stop()
    mosprom_upload_agent = _mos_upload.start_agent(_mos_params, _mos_cache,
        {info['upload_queue']!r}, _mos_stage.stage)
    if not mosprom_upload_agent.wait_ready(15):
        raise RuntimeError("UPLOAD_AGENT_NOT_READY:" + str(mosprom_upload_agent.last_error_type))
    print({{"status":"UPLOAD_AGENT_READY", "lifetime_seconds":300, "allowed_models":["helmet","pose-split"]}})
restart_linq_upload_agent()
'''
    (artifacts/'start_jupyter_upload.py').write_text(code)
    metadata_path.write_text(json.dumps(info,indent=2)+'\n')
    return info,payload


def publish(info,payload,artifacts='/workspace/artifacts/linq-rpc'):
    import pika
    connection=None;declared=False
    try:
        connection=pika.BlockingConnection(_connection_parameters(_environment_parameters(),60,'127.0.0.1',15672))
        channel=connection.channel()
        channel.queue_declare(queue=info['bootstrap_queue'],durable=False,exclusive=False,auto_delete=False)
        declared=True;channel.confirm_delivery()
        channel.basic_publish(exchange='',routing_key=info['bootstrap_queue'],body=payload,mandatory=True,
                              properties=pika.BasicProperties(expiration='3600000'))
        info['published']=True
    except Exception as error:
        info['publish_error_type']=type(error).__name__
    finally:
        if connection is not None:
            try:connection.close()
            except Exception:pass
    Path(artifacts,'upload-bridge.json').write_text(json.dumps(info,indent=2)+'\n')
    return info


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args()
    try:
        info,payload=build()
        if not args.prepare_only:info=publish(info,payload)
        print(json.dumps({'prepared':True,'published':info['published'],
                          'cell':'/workspace/artifacts/linq-rpc/start_jupyter_upload.py',
                          'bootstrap_sha256':info['bootstrap_sha256']}))
        return 0 if args.prepare_only or info['published'] else 1
    except Exception as error:
        print(json.dumps({'status':'NOT_READY','error_type':type(error).__name__}));return 1

if __name__=='__main__':raise SystemExit(main())
