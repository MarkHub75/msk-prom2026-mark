"""Synthetic scenes → artifact JSONL (tech.md 6.1). Same seed, same lines.

A scene is a function of time that returns the objects in the frame. Sizes are in heights of
a person (`H`), so the scene looks the same at any resolution.
"""

import math
import random
from collections.abc import Callable

from safewatch.types import Box, Detection, FrameDetections, Keypoint, ModelTask

SCENES = (
    "demo",
    "walk",
    "running",
    "fall",
    "lying_still",
    "phone",
    "vehicle",
    "fence",
    "under",
    "two_walkers_crossing",
    "dark",
    "empty",
)

WALK_H_S = 0.6  # walking speed, person heights per second
RUN_H_S = 2.5  # above scenarios.running.speed_bh_s
PERSON_H = 0.4  # person height as a share of the frame height
COCO = {0: "person", 7: "truck", 67: "cell phone"}

# (kind, center x in H, posture or class) at time t; kind "person" or a COCO class id.
Obj = tuple[str, float, str]


def _walk_then(t: float, phases: list[tuple[float, float]]) -> float:
    """Distance in H after t seconds of phases (duration, speed); the last phase lasts."""
    x = 0.0
    for duration, speed in phases:
        step = min(t, duration)
        x += step * speed
        t -= step
        if t <= 0:
            break
    return x


def _demo(t: float) -> list[Obj]:
    # walks 3 s, runs 3 s, walks 2 s, falls and lies still 12 s.
    x = 0.5 + _walk_then(t, [(3, WALK_H_S), (3, RUN_H_S), (2, WALK_H_S), (math.inf, 0.0)])
    return [("person", x, "lying" if t >= 8.5 else "upright")]


def _fall(t: float) -> list[Obj]:
    x = 1.0 + _walk_then(t, [(2, WALK_H_S), (math.inf, 0.0)])
    return [("person", x, "lying" if t >= 2.5 else "upright")]


def _phone(t: float) -> list[Obj]:
    return [("person", 1.5, "upright"), ("67", 1.5, "phone")]


def _vehicle(t: float) -> list[Obj]:
    return [("person", 2.0, "upright"), ("7", 0.2 + t * 0.8, "vehicle")]


def _two(t: float) -> list[Obj]:
    return [("person", 0.5 + t * WALK_H_S, "upright"), ("person", 3.5 - t * WALK_H_S, "upright")]


_SCENES: dict[str, Callable[[float], list[Obj]]] = {
    "demo": _demo,
    "walk": lambda t: [("person", 0.5 + t * WALK_H_S, "upright")],
    "running": lambda t: [("person", 0.5 + t * RUN_H_S, "upright")],
    "fall": _fall,
    "lying_still": lambda t: [("person", 1.5, "lying")],
    "phone": _phone,
    "vehicle": _vehicle,
    "fence": lambda t: [("person", 0.3 + t * WALK_H_S, "upright")],
    "under": lambda t: [("person", 0.3 + t * WALK_H_S, "upright")],
    "two_walkers_crossing": _two,
    "dark": lambda t: [],
    "empty": lambda t: [],
}


def _person_box(x_h: float, posture: str, width: int, height: int) -> Box:
    h = PERSON_H * height
    span = max(width - h, 1.0)
    cx = h / 2 + (x_h * h) % span  # wraps at the right edge
    floor = height * 0.95
    if posture == "lying":
        return (cx - h / 2, floor - 0.35 * h, cx + h / 2, floor)
    return (cx - 0.2 * h, floor - h, cx + 0.2 * h, floor)


def _keypoints(box: Box, posture: str) -> list[Keypoint]:
    x1, y1, x2, y2 = box
    # COCO order: nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles.
    along = [0.05, 0.03, 0.03, 0.05, 0.05, 0.2, 0.2, 0.35, 0.35, 0.48, 0.48, 0.52, 0.52]
    along += [0.75, 0.75, 0.97, 0.97]
    side = [0.0, -0.1, 0.1, -0.2, 0.2, -0.5, 0.5, -0.6, 0.6, -0.6, 0.6, -0.3, 0.3]
    side += [-0.3, 0.3, -0.3, 0.3]
    points: list[Keypoint] = []
    for a, s in zip(along, side, strict=True):
        if posture == "lying":  # head on the left, body along the floor
            px = x1 + a * (x2 - x1)
            py = (y1 + y2) / 2 + s * (y2 - y1) / 2
        else:
            px = (x1 + x2) / 2 + s * (x2 - x1) / 2
            py = y1 + a * (y2 - y1)
        points.append((round(px, 2), round(py, 2), 0.9))
    return points


def _jitter(box: Box, rng: random.Random) -> Box:
    x1, y1, x2, y2 = (round(v + rng.uniform(-1.0, 1.0), 1) for v in box)
    return (x1, y1, x2, y2)


def render(
    scene: str,
    width: int,
    height: int,
    fps: float,
    frame_count: int,
    step: int,
    task: ModelTask,
    seed: int = 0,
) -> list[FrameDetections]:
    if scene not in _SCENES:
        raise ValueError(f"unknown scene {scene}")
    rng = random.Random(seed)
    frames: list[FrameDetections] = []
    for frame_idx in range(0, frame_count, step):
        ts_ms = frame_idx * 1000.0 / fps
        detections: list[Detection] = []
        for kind, x_h, mark in _SCENES[scene](ts_ms / 1000.0):
            score = round(0.85 + rng.uniform(-0.05, 0.05), 3)
            if kind == "person":
                box = _jitter(_person_box(x_h, mark, width, height), rng)
                if task == "pose":
                    kpts = _keypoints(box, mark)
                    detections.append(
                        Detection(cls=0, name="0", score=score, bbox_xyxy=box, kpts=kpts)
                    )
                else:
                    detections.append(Detection(cls=0, name="person", score=score, bbox_xyxy=box))
            elif task == "detect":
                cls = int(kind)
                person = _person_box(x_h, "upright", width, height)
                if cls == 67:  # phone in the upper part of the person
                    cx, top = (person[0] + person[2]) / 2, person[1]
                    h = person[3] - person[1]
                    box = (cx, top + 0.25 * h, cx + 0.08 * h, top + 0.35 * h)
                else:  # a truck twice as tall as a person
                    h = person[3] - person[1]
                    box = (person[0], person[3] - 2 * h, person[0] + 3 * h, person[3])
                detections.append(
                    Detection(cls=cls, name=COCO[cls], score=score, bbox_xyxy=_jitter(box, rng))
                )
        frames.append(FrameDetections(frame_idx=frame_idx, ts_ms=ts_ms, detections=detections))
    return frames


def to_jsonl(frames: list[FrameDetections]) -> str:
    return "".join(frame.model_dump_json() + "\n" for frame in frames)
