"""Local device runner matching the organizer's usage_example_python_api.zip.

This is for a host with /dev/tpu* and the matched driver/libtpu/pytpu, e.g. an
issued execution host. It does not turn this API into a remote HTTP service.
"""
from __future__ import annotations
from contextlib import ExitStack
import hashlib
import importlib
from pathlib import Path
import numpy as np
from .backend import UnavailableError


class LocalPytpuRunner:
    def __init__(self, program_path, program_sha256, device=None):
        if not isinstance(program_sha256, str) or len(program_sha256) != 64:
            raise ValueError("a pinned TPU program SHA256 is required")
        try:
            bytes.fromhex(program_sha256)
        except ValueError:
            raise ValueError("invalid program SHA256") from None
        self.path = Path(program_path)
        self.sha256 = program_sha256.lower()
        self.device = device
        self._stack = None
        self._inference = None

    def __enter__(self):
        if self._stack is not None:
            raise RuntimeError("runner is already open")
        digest = hashlib.sha256()
        with self.path.open("rb") as file:
            for block in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(block)
        if digest.hexdigest() != self.sha256:
            raise ValueError("TPU program hash mismatch")
        try:
            tpu = importlib.import_module("pytpu")
        except (ImportError, OSError):
            raise UnavailableError("matched pytpu runtime unavailable") from None
        devices = tpu.Device.list_devices()
        if not devices:
            raise UnavailableError("no local TPU device")
        device = self.device if self.device is not None else devices[0]
        if device not in devices:
            raise UnavailableError("configured TPU device unavailable")
        stack = ExitStack()
        try:
            handle = stack.enter_context(tpu.Device.open(device))
            program = stack.enter_context(handle.load(str(self.path)))
            inference = stack.enter_context(program.inference())
        except BaseException:
            stack.close()
            raise
        self._stack, self._inference = stack, inference
        return self

    def __call__(self, inputs, metadata):
        if self._inference is None:
            raise UnavailableError("local TPU runner must be opened as a context manager")
        if metadata.get("program_sha256") != self.sha256:
            raise ValueError("request program differs from opened TPU program")
        # The official current example uses run(), not historical sync().
        outputs = self._inference.run(inputs)
        # Copy while runtime/session is alive, before caller can close this runner.
        copied = {name: np.array(value, copy=True, order="C") for name, value in outputs.items()}
        return {"outputs": copied, "execution_witness": {
            "request_id": metadata["request_id"], "model_id": metadata["model_id"],
            "program_sha256": self.sha256, "device_kind": "linq_tpu", "completed": True}}

    def __exit__(self, *exc):
        stack, self._stack = self._stack, None
        self._inference = None
        if stack is not None:
            return stack.__exit__(*exc)
        return False
