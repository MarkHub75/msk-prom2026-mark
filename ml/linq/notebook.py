"""Capture one explicitly bound notebook inference call, never a notebook/session.

Only named numeric arrays and allowlisted metadata leave the live session. A
successful capture proves that the supplied callable returned validated tensors;
TPU placement remains the user's supplied-runtime attestation, not independent
hardware verification. This helper performs no authentication, retries or API
endpoint discovery and never records exception messages or caller locals.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
from time import perf_counter
from uuid import uuid4

import numpy as np
from .backend import TensorSpec

_NAME = re.compile(r"[A-Za-z0-9_./:+-]{1,256}\Z")
_TRANSFORM_KEYS = (
    "original_width", "original_height", "input_width", "input_height",
    "resized_width", "resized_height", "left", "top",
)


@dataclass(frozen=True)
class ExpectedClass:
    """Opt-in classification check; axis and offset must come from the example."""
    output_name: str
    class_index: int
    axis: int
    class_offset: int = 0


def _name(value):
    if not isinstance(value, str) or not _NAME.fullmatch(value):
        raise ValueError("invalid explicit tensor name")
    return value


def _file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _arrays(values, *, names=None, specs=None, max_bytes):
    if not isinstance(values, Mapping) or not values:
        raise ValueError("nonempty explicit tensor mapping required")
    for name in values:
        _name(name)
    if names is not None and set(values) != set(names):
        raise ValueError("returned tensor names differ from the explicit allowlist")
    if specs is not None and set(specs) != set(values):
        raise ValueError("tensor specs must exactly match the selected tensor names")
    total = 0
    for name, value in values.items():
        if not isinstance(value, np.ndarray) or value.dtype.kind not in "buif":
            raise ValueError("only real numeric numpy arrays may be captured")
        if not value.size or value.dtype.hasobject or not np.isfinite(value).all():
            raise ValueError("arrays must be nonempty and finite")
        total += value.nbytes
        if total > max_bytes:
            raise ValueError("tensor byte budget exceeded")
        if specs is not None:
            spec = TensorSpec.parse({"name": name, **specs[name]})
            if spec.name != name:
                raise ValueError("tensor spec cannot rename an explicit tensor")
            # Preserve actual dtype/shape; never silently convert to satisfy specs.
            spec.validate(np.ascontiguousarray(value))
    return {name: np.array(value, copy=True, order="C") for name, value in values.items()}


def _tensor_manifest(values):
    return {name: {"shape": list(value.shape), "dtype": value.dtype.name,
                   "nbytes": value.nbytes,
                   "sha256": hashlib.sha256(value.tobytes(order="C")).hexdigest()}
            for name, value in values.items()}


def _save_arrays(path, values):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as file:
        np.savez(file, **values)


def _save_report(path, report):
    tmp = path.with_suffix(".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, allow_nan=False)
        file.write("\n")
    os.replace(tmp, path)


def _transform(value):
    if not isinstance(value, Mapping) or set(value) != set(_TRANSFORM_KEYS):
        raise ValueError("only the eight explicit letterbox transform fields are allowed")
    result = {}
    for key in _TRANSFORM_KEYS:
        item = value[key]
        if type(item) is not int or item < (0 if key in ("left", "top") else 1):
            raise ValueError("invalid numeric letterbox transform")
        result[key] = item
    if (result["left"] + result["resized_width"] > result["input_width"] or
            result["top"] + result["resized_height"] > result["input_height"]):
        raise ValueError("resized image lies outside input canvas")
    return result


def capture_call(run, *, inputs, output_names, program_path, output_dir,
                 model_id, input_specs=None, output_specs=None,
                 runtime_to_reference=None, original_transform=None,
                 expected_class: ExpectedClass | None = None,
                 placement_attested=False, max_bytes=256 * 1024 * 1024):
    """Invoke a supplied callable once and capture its explicit numeric boundary.

    ``run`` takes an owned copy of the named input mapping and must return only
    the named numeric output mapping. It must contain the actual EXISTING call
    from the inspected example, not a guessed endpoint. Output dir must be new;
    existing captures are never overwritten. Specs, when supplied, map tensor
    names to {shape, dtype}; they are assertions, not conversions.

    Return safe metadata. Failures record only phase/type, never the exception
    string. ``call_completed`` becomes true only after the callable returns;
    status completed additionally requires validated outputs and saved artifacts.
    ``independently_verified`` is always false. No source code, closures, globals,
    arbitrary runtime metadata, paths, auth material or notebook outputs are read.
    """
    start = perf_counter()
    report = {
        "schema_version": "1.0", "capture_id": str(uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "not_started", "call_started": False, "call_completed": False,
        "hardware_placement": {"claimed_device": "unverified", "basis": "not_attested",
                               "independently_verified": False},
        "checks": {}, "artifacts": {}, "timings": {},
    }
    directory = None
    phase = "validate_configuration"
    call_start = None
    try:
        if not callable(run) or type(max_bytes) is not int or max_bytes <= 0:
            raise ValueError("callable and positive numeric byte budget required")
        if (not isinstance(model_id, str) or
                not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", model_id)):
            raise ValueError("explicit model label required")
        if type(placement_attested) is not bool:
            raise ValueError("placement attestation must be an explicit bool")
        if not isinstance(output_names, (tuple, list)) or not output_names:
            raise ValueError("explicit output name list required")
        names = [_name(name) for name in output_names]
        if len(set(names)) != len(names):
            raise ValueError("output names must be unique")
        report["model_id"] = model_id
        if placement_attested:
            report["hardware_placement"].update(
                claimed_device="linq_tpu", basis="user_supplied_runtime_attestation")
        if runtime_to_reference is not None:
            if (not isinstance(runtime_to_reference, Mapping) or
                    set(runtime_to_reference) != set(names)):
                raise ValueError("explicit output mapping must cover every captured output")
            mapped = {name: _name(value) for name, value in runtime_to_reference.items()}
            if len(set(mapped.values())) != len(mapped):
                raise ValueError("output map must be one-to-one")
            report["runtime_to_reference"] = mapped
        if original_transform is not None:
            report["original_transform"] = _transform(original_transform)
        if expected_class is not None:
            if (not isinstance(expected_class, ExpectedClass) or
                    expected_class.output_name not in names or
                    type(expected_class.class_index) is not int or expected_class.class_index < 0 or
                    type(expected_class.axis) is not int or type(expected_class.class_offset) is not int):
                raise ValueError("explicit classification check configuration required")
        phase = "validate_inputs"
        saved_inputs = _arrays(inputs, specs=input_specs, max_bytes=max_bytes)
        report["inputs"] = _tensor_manifest(saved_inputs)
        phase = "hash_program"
        report["program"] = {"sha256": _file_hash(program_path)}
        phase = "create_capture_directory"
        directory = Path(output_dir)
        directory.mkdir(mode=0o700, parents=True, exist_ok=False)
        phase = "save_inputs"
        _save_arrays(directory / "inputs.npz", saved_inputs)
        report["artifacts"]["inputs"] = {
            "file": "inputs.npz", "sha256": _file_hash(directory / "inputs.npz")}
        report["status"] = "pending_call"
        _save_report(directory / "capture.json", report)
        # Separate copy ensures a mutating runner cannot change the stored input evidence.
        call_inputs = {name: value.copy(order="C") for name, value in saved_inputs.items()}
        phase = "invoke_supplied_call"
        report["call_started"] = True
        call_start = perf_counter()
        raw = run(call_inputs)  # Exactly one invocation, with no hidden retry.
        report["timings"]["call_ms"] = (perf_counter() - call_start) * 1000
        report["call_completed"] = True
        phase = "validate_outputs"
        outputs = _arrays(raw, names=names, specs=output_specs, max_bytes=max_bytes)
        report["outputs"] = _tensor_manifest(outputs)
        report["checks"]["numeric_outputs"] = "PASS"
        phase = "expected_class"
        if expected_class is not None:
            value = outputs[expected_class.output_name]
            top = np.argmax(value, axis=expected_class.axis)
            if top.size != 1:
                raise ValueError("classification check requires exactly one prediction")
            observed = int(top.reshape(-1)[0]) + expected_class.class_offset
            report["checks"]["expected_class"] = {
                "status": "PASS" if observed == expected_class.class_index else "FAIL",
                "observed": observed, "expected": expected_class.class_index,
                "output_name": expected_class.output_name,
                "axis": expected_class.axis, "class_offset": expected_class.class_offset,
            }
        phase = "save_outputs"
        _save_arrays(directory / "outputs.npz", outputs)
        report["artifacts"]["outputs"] = {
            "file": "outputs.npz", "sha256": _file_hash(directory / "outputs.npz")}
        report["status"] = ("validation_failed" if
            report["checks"].get("expected_class", {}).get("status") == "FAIL" else "completed")
    except Exception as error:
        if call_start is not None and "call_ms" not in report["timings"]:
            report["timings"]["call_ms"] = (perf_counter() - call_start) * 1000
        report["status"] = "failed"
        report["error"] = {"phase": phase, "exception_type": type(error).__name__}
    report["timings"]["total_ms"] = (perf_counter() - start) * 1000
    # Do not overwrite an existing directory if creation itself failed.
    if directory is not None and phase != "create_capture_directory":
        try:
            _save_report(directory / "capture.json", report)
        except Exception as error:
            report["status"] = "failed"
            report["error"] = {"phase": "save_report", "exception_type": type(error).__name__}
    return report
