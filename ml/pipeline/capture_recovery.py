"""Complete interrupted capture persistence from a correlated durable RPC result.

No request is sent here. The caller must use the existing transport's receive-only
reconciliation, then supply its validated result and matching request identity.
"""
import json
import os
from pathlib import Path
from uuid import uuid4

import numpy as np
from ml.linq.notebook import _arrays, _file_hash, _tensor_manifest
from ml.pipeline.capture_review import _verify_arrays, review_capture

MAX_BYTES = 256 * 1024 * 1024


def save_json(path, value):
    """Atomically persist local execution state before acknowledging progress."""
    path = Path(path)
    temporary = path.with_name(path.name + "." + uuid4().hex + ".tmp")
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    finally:
        temporary.unlink(missing_ok=True)


def complete_capture(directory, outputs, response):
    directory = Path(directory)
    if directory.is_symlink():
        raise ValueError("capture directory cannot be a symlink")
    capture = json.loads((directory / "capture.json").read_text())
    pointer = json.loads((directory / "request-pointer.json").read_text())
    request_id = pointer["journal_request_id"]
    if (response.get("request_id") != request_id or
            response.get("response_id") != request_id or
            response.get("status_code") != 0 or
            response.get("remote_completion") != "response_received"):
        raise ValueError("successful correlated completion required")
    if capture.get("journal_request_id", request_id) != request_id:
        raise ValueError("capture request identity differs from journal pointer")
    values = _arrays(outputs, max_bytes=MAX_BYTES)
    inputs = directory / "inputs.npz"
    if (inputs.is_symlink() or
            capture.get("artifacts", {}).get("inputs", {}).get("sha256") != _file_hash(inputs)):
        raise ValueError("stored input evidence changed")
    _verify_arrays(inputs, capture.get("inputs"), MAX_BYTES)

    output_path = directory / "outputs.npz"
    if output_path.exists():
        if output_path.is_symlink():
            raise ValueError("output artifact cannot be a symlink")
        with np.load(output_path, allow_pickle=False) as saved:
            if (set(saved.files) != set(values) or len(saved.files) != len(values) or
                    any(not np.array_equal(saved[key], value) or saved[key].dtype != value.dtype
                        for key, value in values.items())):
                raise ValueError("existing output differs from durable RPC result")
    else:
        temporary = directory / ("outputs." + uuid4().hex + ".tmp")
        try:
            descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "wb") as stream:
                np.savez(stream, **values)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, output_path)
        finally:
            temporary.unlink(missing_ok=True)
    # response.json is recoverable even if the next atomic capture update fails.
    save_json(directory / "response.json", response)
    capture.update(status="completed", call_started=True, call_completed=True,
                   journal_request_id=request_id, recovered_from_durable_rpc=True)
    capture.pop("error", None)
    capture["outputs"] = _tensor_manifest(values)
    capture.setdefault("checks", {})["numeric_outputs"] = "PASS"
    capture.setdefault("artifacts", {})["outputs"] = {
        "file": "outputs.npz", "sha256": _file_hash(output_path)}
    save_json(directory / "capture.json", capture)
    return review_capture(directory)
