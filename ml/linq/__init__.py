"""Explicit LinQ execution boundary; no automatic CPU/GPU fallback."""
from .backend import LinQBackend, TensorSpec, UnavailableError

__all__ = ["LinQBackend", "TensorSpec", "UnavailableError"]
