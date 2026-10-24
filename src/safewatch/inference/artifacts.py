"""Artifact cache key and JSONL reading (tech.md 5.3): pure logic, no database."""

import hashlib
from pathlib import Path

from pydantic import ValidationError

from safewatch.errors import InferenceError
from safewatch.types import BackendName, FrameDetections, ModelSpec

CACHE_SCHEMA = "jsonl-v1"


def cache_key(
    video_sha256: str, model: ModelSpec, step: int, backend: BackendName, fake: bool
) -> str:
    text = (
        f"{CACHE_SCHEMA}|{video_sha256}|{model.id}|{model.version}|{model.input_size}|{step}"
        f"|{backend}|{int(fake)}"
    )
    return hashlib.sha256(text.encode()).hexdigest()


def read_jsonl(path: Path, expected_frames: int | None) -> list[FrameDetections]:
    """Frames of an artifact; any deviation from the worker format is `bad_output`."""
    frames: list[FrameDetections] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for n, line in enumerate(lines, 1):
        try:
            frame = FrameDetections.model_validate_json(line)
        except ValidationError as exc:
            raise InferenceError("bad_output", f"line {n}: {exc.errors()[0]['msg']}") from None
        if frames and frame.frame_idx <= frames[-1].frame_idx:
            raise InferenceError("bad_output", f"line {n}: frame_idx does not grow")
        frames.append(frame)
    if expected_frames is not None and len(frames) != expected_frames:
        raise InferenceError("bad_output", f"{len(frames)} lines, expected {expected_frames}")
    return frames
