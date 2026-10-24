"""Demo pack files (tech.md 8.19): `data/demo/<name>/manifest.json` next to videos and artifacts."""

import hashlib
from pathlib import Path

from safewatch.types import DemoManifest

MANIFEST = "manifest.json"


def read_manifest(path: Path) -> DemoManifest:
    return DemoManifest.model_validate_json(path.read_text(encoding="utf-8"))


def write_manifest(path: Path, manifest: DemoManifest) -> str:
    data = (manifest.model_dump_json(indent=2) + "\n").encode()
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest()
