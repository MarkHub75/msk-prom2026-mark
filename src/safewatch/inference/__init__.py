"""Inference backends (tech.md 6.1)."""

from safewatch.config import Settings
from safewatch.inference.linq import JupyterShell, LinqBackend
from safewatch.types import InferenceBackend


def make_backend(settings: Settings) -> InferenceBackend:
    if settings.inference_backend == "local":
        raise NotImplementedError("slice 3")
    if settings.fake:
        from safewatch.fakes.remote import FakeRemoteShell  # fakes stay out of the real path

        return LinqBackend(settings, FakeRemoteShell())
    return LinqBackend(settings, JupyterShell(settings))
