"""Adapter around the actual, issued LinQ runner.

Transport is deliberately injected: a local pytpu runner is not a remote HTTP API.
Never include SDK exception messages in results: they may contain auth material.
"""
from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Mapping, Any
import numpy as np


class UnavailableError(RuntimeError):
    """Required issued runtime or configured runner is unavailable."""


@dataclass(frozen=True)
class TensorSpec:
    name: str
    shape: tuple[int, ...]
    dtype: str

    @classmethod
    def parse(cls, value: Mapping[str, Any]) -> "TensorSpec":
        shape = tuple(value["shape"])
        if not shape or any(type(x) is not int or x <= 0 for x in shape):
            raise ValueError("tensor shape must contain positive static dimensions")
        name = value["name"]
        if not isinstance(name, str) or not name:
            raise ValueError("tensor name must be nonempty")
        dtype = np.dtype(value["dtype"])
        if dtype.kind not in "buif":
            raise ValueError("only real numeric tensor dtypes are supported")
        return cls(name, shape, dtype.name)

    def validate(self, array: np.ndarray) -> None:
        if not isinstance(array, np.ndarray):
            raise ValueError("tensor must be a numpy ndarray")
        if array.shape != self.shape or array.dtype != np.dtype(self.dtype):
            raise ValueError("tensor shape/dtype does not match model manifest")
        if not array.flags.c_contiguous:
            raise ValueError("tensor must be C-contiguous")
        if array.nbytes != int(np.prod(self.shape, dtype=object)) * np.dtype(self.dtype).itemsize:
            raise ValueError("unexpected tensor byte size")
        if not np.isfinite(array).all():
            raise ValueError("tensor contains non-finite values")


class LinQBackend:
    """Validate named tensors, call a supplied blocking runner, own returned data.

    Manifest requires model_id, inputs and outputs (lists of name/shape/dtype).
    Runner receives (inputs, request_metadata), and returns a tensor mapping or
    {"outputs": mapping, "execution_witness": mapping}. Witness is retained only
    through an allowlist, and must refer to this request/model/program. It is a
    recorded service claim, not independent verification of TPU placement.
    """

    def __init__(self, manifest: Mapping[str, Any], runner: Callable | None = None):
        self.model_id = manifest.get("model_id")
        if not isinstance(self.model_id, str) or not self.model_id:
            raise ValueError("manifest requires model_id")
        self.program_sha256 = manifest.get("program_sha256")
        self.inputs = self._specs(manifest.get("inputs", []))
        self.outputs = self._specs(manifest.get("outputs", []))
        self.runner = runner

    @staticmethod
    def _specs(values: list) -> dict[str, TensorSpec]:
        specs = [TensorSpec.parse(value) for value in values]
        if not specs or len({spec.name for spec in specs}) != len(specs):
            raise ValueError("manifest requires nonempty, unique tensor specs")
        return {spec.name: spec for spec in specs}

    def infer(self, request: Mapping[str, Any]) -> dict:
        started = perf_counter()
        result = {
            "request_id": request.get("request_id"), "model_id": self.model_id,
            "backend": "linq", "status": "error", "outputs": {},
            "execution_verified": False, "execution_witness": None,
        }
        try:
            if not isinstance(request.get("request_id"), str) or not request["request_id"]:
                raise ValueError("request_id required")
            if request.get("model_id") != self.model_id:
                raise ValueError("requested model does not match loaded model")
            arrays = request.get("inputs")
            if not isinstance(arrays, Mapping) or set(arrays) != set(self.inputs):
                raise ValueError("input tensor names do not match manifest")
            for name, spec in self.inputs.items():
                spec.validate(arrays[name])
            if self.runner is None:
                raise UnavailableError("issued LinQ runner is not configured")
            metadata = {"request_id": request["request_id"], "model_id": self.model_id,
                        "program_sha256": self.program_sha256}
            run_started = perf_counter()
            raw = self.runner(arrays, metadata)
            result["timings"] = {"runner_ms": (perf_counter() - run_started) * 1000}
            if not isinstance(raw, Mapping):
                raise ValueError("runner must return a mapping")
            if "outputs" in raw:
                outputs = raw["outputs"]
                witness = raw.get("execution_witness")
            else:
                outputs, witness = raw, None
            if not isinstance(outputs, Mapping) or set(outputs) != set(self.outputs):
                raise ValueError("output tensor names do not match manifest")
            copied = {}
            for name, spec in self.outputs.items():
                spec.validate(outputs[name])
                copied[name] = outputs[name].copy(order="C")
            # Avoid blindly logging arbitrary SDK metadata (URLs, tokens, user names).
            if isinstance(witness, Mapping):
                keys = ("request_id", "model_id", "program_sha256", "device_kind", "completed")
                safe = {key: witness[key] for key in keys if key in witness}
                if (safe.get("request_id") != request["request_id"] or
                        safe.get("model_id") != self.model_id or
                        safe.get("program_sha256") != self.program_sha256):
                    raise ValueError("execution witness correlation mismatch")
                if safe.get("device_kind") != "linq_tpu" or safe.get("completed") is not True:
                    raise ValueError("execution witness does not report completed TPU execution")
                result["execution_witness"] = safe
            result.update(status="ok", outputs=copied)
        except Exception as error:
            if isinstance(error, UnavailableError):
                code = "linq_unavailable"
            elif isinstance(error, (ValueError, TypeError, KeyError, OverflowError)):
                code = "contract_error"
            else:
                code = "runner_error"
            result["error"] = {"code": code, "exception_type": type(error).__name__}
        result.setdefault("timings", {})["total_ms"] = (perf_counter() - started) * 1000
        return result
