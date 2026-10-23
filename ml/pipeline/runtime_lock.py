"""Prevent concurrent orchestrators from submitting the same model operation."""
from contextlib import contextmanager
import fcntl
import os
from pathlib import Path


@contextmanager
def deployment_lock(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("another deployment is already running") from None
        yield
    finally:
        os.close(descriptor)
