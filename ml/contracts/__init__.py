"""Version 1 wire contracts, shared by inference, behavior and delivery."""
from dataclasses import dataclass, field, asdict
from typing import Any
import math

SCHEMA_VERSION = "1.0"

def validate_observation(value: dict) -> dict:
    required = ("camera_id", "stream_epoch", "frame_id", "media_time_ms", "image_size", "status", "detections")
    for key in required:
        if key not in value:
            raise ValueError(f"missing {key}")
    if value.get("schema_version", SCHEMA_VERSION) != SCHEMA_VERSION:
        raise ValueError("unsupported schema_version")
    if value["status"] not in ("ok", "error", "gap"):
        raise ValueError("invalid observation status")
    if not isinstance(value["frame_id"], int) or value["frame_id"] < 0:
        raise ValueError("invalid frame_id")
    if not isinstance(value["media_time_ms"], (int, float)) or not math.isfinite(value["media_time_ms"]) or value["media_time_ms"] < 0:
        raise ValueError("invalid media_time_ms")
    w, h = value["image_size"]
    if w <= 0 or h <= 0:
        raise ValueError("invalid image_size")
    for d in value["detections"]:
        x1,y1,x2,y2 = d["bbox_xyxy"]
        if not all(math.isfinite(v) for v in (x1,y1,x2,y2,d["score"])) or not (0 <= x1 <= x2 <= w and 0 <= y1 <= y2 <= h and 0 <= d["score"] <= 1):
            raise ValueError("invalid detection")
        if not isinstance(d["class_name"], str):
            raise ValueError("invalid class_name")
    return value

def validate_event(value: dict) -> dict:
    for key in ("event_id", "revision", "camera_id", "stream_epoch", "track_key", "type", "state", "start_media_ms", "confirmed_media_ms", "evidence"):
        if key not in value:
            raise ValueError(f"missing {key}")
    if value["type"] not in ("missing_helmet", "suspected_fall", "prolonged_lying"):
        raise ValueError("unsupported event type")
    if value["state"] not in ("open", "closed", "interrupted") or value["revision"] < 1:
        raise ValueError("invalid event state/revision")
    if value["confirmed_media_ms"] < value["start_media_ms"]:
        raise ValueError("invalid event times")
    return value
