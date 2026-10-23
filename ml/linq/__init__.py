"""Explicit LinQ execution boundary; no automatic CPU/GPU fallback."""
from .backend import LinQBackend, TensorSpec, UnavailableError
from .local import LocalPytpuRunner

__all__ = ["LinQBackend", "TensorSpec", "UnavailableError", "LocalPytpuRunner"]
