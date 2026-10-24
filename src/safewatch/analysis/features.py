"""Features of tracked people (tech.md 8.2 items 2 and 5): keypoints, posture, H_ref, speed."""

import math
import statistics
from itertools import pairwise

from safewatch.analysis.geometry import iou
from safewatch.config import FeaturesConfig
from safewatch.types import Box, Detection, Keypoint, PersonState, Point, Posture

SHOULDERS_HIPS = (5, 6, 11, 12)  # COCO keypoints that give the torso angle
ANKLES = (15, 16)
FRAME_EDGE_PX = 2  # a bbox bottom this close to the frame edge may hide the feet

# Per track id: (ts_ms, state) of every earlier observation, oldest first.
History = dict[int, list[tuple[int, PersonState]]]


def attach_keypoints(
    boxes: list[Box], poses: list[Detection], match_iou: float
) -> dict[int, list[Keypoint]]:
    """Greedy by IoU of the detector and pose boxes: index of `boxes` → keypoints."""
    pairs = sorted(
        (
            (iou(box, pose.bbox_xyxy), i, j)
            for i, box in enumerate(boxes)
            for j, pose in enumerate(poses)
            if pose.kpts
        ),
        reverse=True,
    )
    out: dict[int, list[Keypoint]] = {}
    used: set[int] = set()
    for score, i, j in pairs:
        if score < match_iou:
            break
        if i not in out and j not in used:
            out[i] = poses[j].kpts or []
            used.add(j)
    return out


def _recent(past: list[tuple[int, PersonState]], since_ms: float) -> list[tuple[int, PersonState]]:
    out = []
    for ts, state in reversed(past):
        if ts < since_ms:
            break
        out.append((ts, state))
    return out[::-1]


def _center(box: Box) -> Point:
    return ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)


def _posture(
    box: Box, points: list[Keypoint] | None, cfg: FeaturesConfig, kpt_conf: float
) -> tuple[Posture, float | None]:
    if points is not None and all(points[i][2] >= kpt_conf for i in SHOULDERS_HIPS):
        sx, sy = (points[5][0] + points[6][0]) / 2, (points[5][1] + points[6][1]) / 2
        hx, hy = (points[11][0] + points[12][0]) / 2, (points[11][1] + points[12][1]) / 2
        deg = math.degrees(math.atan2(abs(sx - hx), abs(sy - hy)))
        if deg >= cfg.lying_torso_deg:
            return "lying", deg
        if deg < cfg.upright_torso_deg:
            return "upright", deg
        return "unknown", deg
    w, h = box[2] - box[0], box[3] - box[1]
    if w > 0 and h / w >= cfg.upright_hw:
        return "upright", None
    if h > 0 and w / h >= cfg.lying_wh:
        return "lying", None
    return "unknown", None


def _speed(points: list[tuple[int, Point]], ref: float, cfg: FeaturesConfig) -> float | None:
    window_ms = cfg.speed_window_s * 1000
    if len(points) < cfg.speed_min_samples:
        return None
    if any(b[0] - a[0] > cfg.speed_max_gap_s * 1000 for a, b in pairwise(points)):
        return None
    dt = points[-1][0] - points[0][0]
    if dt <= 0 or dt < window_ms / 2:
        return None
    return math.dist(points[-1][1], points[0][1]) / (dt / 1000) / ref


def person_states(
    tracks: list[tuple[int, Detection]],
    kpts: dict[int, list[Keypoint]],
    ts_ms: int,
    frame_height: int,
    history: History,
    cfg: FeaturesConfig,
    kpt_conf: float,
) -> list[PersonState]:
    """States of the people tracked in this frame; `history` gets this frame appended."""
    states = []
    for track_id, det in tracks:
        box = det.bbox_xyxy
        x1, _, x2, y2 = box
        height = box[3] - box[1]
        foot = ((x1 + x2) / 2, y2)
        points = kpts.get(track_id)
        ankles = [p for i in ANKLES if points is not None and (p := points[i])[2] >= kpt_conf]
        anchor = max(ankles, key=lambda p: p[1])[:2] if ankles else foot
        feet_visible = bool(ankles) if points is not None else y2 < frame_height - FRAME_EDGE_PX
        posture, torso_deg = _posture(box, points, cfg, kpt_conf)
        past = history.setdefault(track_id, [])
        prev_ts, prev = past[-1] if past else (None, None)

        if posture == "lying" and prev is not None:
            ref = prev.ref_height_px  # frozen: a lying bbox is no measure of the height
        else:
            window = _recent(past, ts_ms - cfg.ref_window_s * 1000)
            ups = [s.height_px for _, s in window if s.posture == "upright"]
            ups += [height] if posture == "upright" else []
            if ups:
                ref = statistics.median(ups)
            elif prev is not None and prev.last_upright_ms is not None:
                ref = prev.ref_height_px
            else:
                ref = height

        feet = [(ts, s.foot) for ts, s in _recent(past, ts_ms - cfg.speed_window_s * 1000)]
        speed = _speed([*feet, (ts_ms, foot)], ref, cfg)

        center, limit = _center(box), cfg.still_motion_bh * ref
        still_since = ts_ms
        for ts, s in reversed(past):
            if math.dist(_center(s.bbox), center) > limit:
                break
            still_since = ts

        lying_since = None
        if posture == "lying":  # a lying previous state carries the start of the run
            lying_since = ts_ms
            if prev is not None and prev.lying_since_ms is not None:
                lying_since = prev.lying_since_ms
        last_upright = ts_ms if posture == "upright" else (prev.last_upright_ms if prev else None)
        state = PersonState(
            track_id=track_id,
            bbox=box,
            score=det.score,
            foot=foot,
            anchor=(anchor[0], anchor[1]),
            feet_visible=feet_visible,
            ground=None,  # slice 9: calibration
            height_px=height,
            ref_height_px=ref,
            speed_bh_s=speed,
            speed_m_s=None,  # slice 9: calibration
            posture=posture,
            posture_method="pose" if torso_deg is not None else "bbox",
            torso_deg=torso_deg,
            last_upright_ms=last_upright,
            lying_since_ms=lying_since,
            still_since_ms=still_since,
            prev_anchor=prev.anchor if prev else None,
            prev_ts_ms=prev_ts,
            kpts=points,
        )
        past.append((ts_ms, state))
        states.append(state)
    return states
