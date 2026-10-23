"""Bounded Jupyter-side staging agent for two reviewed TPU programs.

Standalone bootstrap module: stdlib + NumPy, lazy official format/pika imports.
The kernel supplies its existing connection parameters and a reviewed stage_fn.
No credential/env reads, notebook execution, arbitrary paths or code payloads.
"""
from __future__ import annotations

from collections.abc import Mapping
import copy
import hashlib
import importlib
import json
from pathlib import Path
import re
import tempfile
import threading
from time import monotonic
from uuid import UUID

import numpy as np

_MODELS = {
    "helmet": ("helmet-v1.tpu", "408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa"),
    "pose-split": ("pose-split-v1.tpu", "c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b"),
}
MAX_PROGRAM_BYTES = 8 * 1024 * 1024
MAX_AGENT_SECONDS = 300
MAX_MESSAGES = 4


class UploadError(ValueError):
    """Stable protocol code only; no server paths or exception messages."""
    def __init__(self, code, request_id=None, callback=None):
        super().__init__(code)
        self.code, self.request_id, self.callback = code, request_id, callback


def _queue_name(value):
    if not isinstance(value, str) or not value.startswith("notebook_upload_"):
        raise UploadError("INVALID_UPLOAD_QUEUE")
    token = value[len("notebook_upload_"):]
    try:
        parsed = UUID(token)
    except (ValueError, TypeError, AttributeError):
        raise UploadError("INVALID_UPLOAD_QUEUE") from None
    if token not in (str(parsed), parsed.hex):
        raise UploadError("INVALID_UPLOAD_QUEUE")
    return value


def _headers(fmt, properties):
    headers = getattr(properties, "headers", None)
    if not isinstance(headers, Mapping):
        raise UploadError("INVALID_HEADERS")
    request_id = headers.get(fmt.MESSAGE_ID_ATTR_NAME)
    try:
        if not isinstance(request_id, str) or str(UUID(request_id)) != request_id:
            raise ValueError("invalid UUID")
    except (ValueError, TypeError, AttributeError):
        raise UploadError("INVALID_REQUEST_ID") from None
    route = headers.get(fmt.RESPONSE_ROUTING_KEYS_ATTR_NAME)
    try:
        if not isinstance(route, str):
            raise ValueError("JSON routing list required")
        routes = json.loads(route)
        expected = "notebook_" + request_id[:8]
        if not isinstance(routes, list) or routes != [expected]:
            raise ValueError("single generated callback required")
        callback = routes[0]
    except Exception:
        raise UploadError("INVALID_CALLBACK") from None
    known = {fmt.MESSAGE_ID_ATTR_NAME, fmt.RESPONSE_ROUTING_KEYS_ATTR_NAME, fmt.TARGET_URI_ATTR_NAME}
    if set(headers) != known:
        raise UploadError("UNKNOWN_HEADERS", request_id, callback)
    model = headers.get(fmt.TARGET_URI_ATTR_NAME)
    if not isinstance(model, str) or model not in _MODELS:
        raise UploadError("INVALID_MODEL", request_id, callback)
    return request_id, callback, model


def _stage_payload(fmt, body, cache_dir, model, stage_fn):
    if not isinstance(body, (bytes, bytearray)) or len(body) > MAX_PROGRAM_BYTES + 65536:
        raise UploadError("INVALID_BODY_SIZE")
    try:
        decoded = fmt.deserialize(bytes(body))
    except Exception:
        raise UploadError("INVALID_BODY") from None
    if not isinstance(decoded, tuple) or len(decoded) != 3:
        raise UploadError("INVALID_TASK")
    data, metadata, worker = decoded
    if not isinstance(data, Mapping) or set(data) != {"program_bytes"}:
        raise UploadError("UNKNOWN_DATA_FIELDS")
    if metadata is not None and not (isinstance(metadata, tuple) and len(metadata) == 0):
        raise UploadError("METADATA_NOT_ALLOWED")
    if (not isinstance(worker, Mapping) or worker.get("status_code") != 0 or
            isinstance(worker.get("status_code"), (bool, np.bool_))):
        raise UploadError("INVALID_TASK_STATUS")
    allowed_worker = {"worker_pid", "thread_name", "inference_time", "status_code", "error_message",
                      "inference_opening_timestamp"}
    if set(worker) - allowed_worker:
        raise UploadError("UNKNOWN_TASK_FIELDS")
    if (any(worker.get(key, "") != "" for key in ("worker_pid", "thread_name", "error_message")) or
            any(worker.get(key, 0) not in (None, 0, 0.0) for key in ("inference_time", "inference_opening_timestamp"))):
        raise UploadError("WORKER_REPORT_NOT_ALLOWED")
    value = data["program_bytes"]
    if (not isinstance(value, np.ndarray) or value.dtype != np.dtype("uint8") or value.ndim != 1 or
            not 0 < value.size <= MAX_PROGRAM_BYTES):
        raise UploadError("INVALID_PROGRAM_TENSOR")
    blob = value.tobytes(order="C")
    digest = hashlib.sha256(blob).hexdigest()
    expected_name, expected_hash = _MODELS[model]
    if digest != expected_hash:
        raise UploadError("PROGRAM_HASH_MISMATCH")
    # No directories/files are created until every request field and hash passes.
    with tempfile.TemporaryDirectory(prefix="linq-program-") as temporary:
        source = Path(temporary) / "program.tpu"
        source.write_bytes(blob)
        receipt = stage_fn(cache_dir, source, model=model)
    if (not isinstance(receipt, Mapping) or receipt.get("status") not in {"STAGED", "ALREADY_STAGED_IDENTICAL"} or
            receipt.get("program_name") != expected_name or receipt.get("program_sha256") != expected_hash or
            receipt.get("stock_program_present_in_selected_namespace") is not True):
        raise UploadError("INVALID_STAGE_RECEIPT")
    return {"sha256": np.frombuffer(bytes.fromhex(digest), dtype=np.uint8).copy(),
            "byte_count": np.array([len(blob)], dtype=np.int64)}


class UploadAgent:
    """Thread-owned connection. Readiness is real only after consumer registration."""
    def __init__(self, parameters, cache_dir, queue_name, stage_fn):
        self._queue = _queue_name(queue_name)
        if not callable(stage_fn):
            raise UploadError("STAGE_FUNCTION_REQUIRED")
        self._parameters = parameters
        self._cache_dir, self._stage_fn = Path(cache_dir), stage_fn
        self._stop = threading.Event()
        self._ready = threading.Event()
        self._startup_done = threading.Event()
        self._thread = threading.Thread(target=self._serve, name="linq-reviewed-upload", daemon=True)
        self._connection = None
        self.last_error_type = None
        self._messages = 0

    @property
    def is_ready(self):
        return self._ready.is_set() and self._thread.is_alive() and not self._stop.is_set()

    def wait_ready(self, timeout=10):
        self._startup_done.wait(timeout)
        return self.is_ready

    def stop(self, timeout=12):
        self._stop.set()
        connection = self._connection
        if connection is not None:
            try:
                connection.add_callback_threadsafe(lambda: None)
            except Exception:
                pass
        self._thread.join(timeout)
        return not self._thread.is_alive()

    def _consume(self, fmt, pika, channel, method, properties, body):
        if self._messages >= MAX_MESSAGES:
            self._stop.set()
            try:
                channel.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as error:
                self.last_error_type = type(error).__name__
            return
        self._messages += 1
        request_id = callback = None
        try:
            request_id, callback, model = _headers(fmt, properties)
            outputs = _stage_payload(fmt, body, self._cache_dir, model, self._stage_fn)
            status, error_code = 0, ""
        except UploadError as error:
            request_id = request_id or error.request_id
            callback = callback or error.callback
            outputs, status, error_code = {}, 1, error.code
        except Exception as error:
            self.last_error_type = type(error).__name__
            outputs, status, error_code = {}, 2, "STAGE_FAILED"
        try:
            if request_id is not None and callback is not None:
                reply = fmt.serialize(fmt.PyTask(data=outputs, status_code=status, error_message=error_code))
                channel.basic_publish(exchange="", routing_key=callback, body=reply,
                    properties=pika.BasicProperties(headers={fmt.MESSAGE_ID_ATTR_NAME: request_id}), mandatory=True)
        except Exception as error:
            self.last_error_type = type(error).__name__
        finally:
            # Exactly one acknowledgment attempt even if reply serialization/publish fails.
            try:
                channel.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as error:
                self.last_error_type = type(error).__name__
            if self._messages >= MAX_MESSAGES:
                self._stop.set()

    def _serve(self):
        connection = channel = None
        declared = False
        try:
            fmt = importlib.import_module("tpu_pycloud_format")
            if (not isinstance(getattr(fmt, "PyTask", None), type) or
                    not callable(getattr(fmt, "serialize", None)) or not callable(getattr(fmt, "deserialize", None)) or
                    tuple(getattr(fmt, name, None) for name in (
                        "MESSAGE_ID_ATTR_NAME", "RESPONSE_ROUTING_KEYS_ATTR_NAME", "TARGET_URI_ATTR_NAME")) != (
                        "tpu_pycloud_message_id", "response_routing_keys", "uri")):
                raise UploadError("OFFICIAL_FORMAT_REQUIRED")
            pika = importlib.import_module("pika")
            parameters = copy.copy(self._parameters)
            parameters.connection_attempts, parameters.retry_delay = 1, 0
            parameters.socket_timeout, parameters.stack_timeout = 5, 10
            parameters.blocked_connection_timeout = 5
            connection = pika.BlockingConnection(parameters)
            self._connection = connection
            if self._stop.is_set():
                return
            channel = connection.channel()
            channel.queue_declare(queue=self._queue, durable=False, auto_delete=True, exclusive=False)
            declared = True
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=self._queue, auto_ack=False,
                on_message_callback=lambda ch, method, props, body: self._consume(fmt, pika, ch, method, props, body))
            self._ready.set()
            self._startup_done.set()
            deadline = monotonic() + MAX_AGENT_SECONDS
            while not self._stop.is_set() and monotonic() < deadline:
                connection.process_data_events(time_limit=0.2)
        except Exception as error:
            self.last_error_type = type(error).__name__
        finally:
            self._ready.clear()
            self._startup_done.set()
            if declared and channel is not None:
                try:
                    channel.queue_delete(queue=self._queue)
                except Exception as error:
                    self.last_error_type = type(error).__name__
            if connection is not None:
                try:
                    connection.close()
                except Exception as error:
                    self.last_error_type = type(error).__name__
            self._connection = None


def start_agent(parameters, cache_dir, queue_name, stage_fn):
    """Start the explicit bounded service; parameters stay in the browser kernel.

    It accepts at most four messages over five minutes and only the two pinned
    program blobs. The injected reviewed stage_fn alone chooses target paths.
    Nothing in requests can select a filesystem path, execute code, or alter auth.
    """
    handle = UploadAgent(parameters, cache_dir, queue_name, stage_fn)
    handle._thread.start()
    return handle
