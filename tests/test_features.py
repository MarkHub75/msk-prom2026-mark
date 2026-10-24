"""Slice 4: features of people, tech.md 8.2 items 2 and 5."""

import math

import pytest

from safewatch.analysis import features
from safewatch.config import get_settings
from safewatch.types import Box, Detection, Keypoint, PersonState

FRAME_H = 1000


def _states(
    frames: list[tuple[int, Box]], kpts: list[list[Keypoint] | None] | None = None
) -> list[PersonState]:
    """States of track 1 over (ts_ms, bbox) frames, with optional keypoints per frame."""
    s = get_settings()
    history: features.History = {}
    out = []
    for n, (ts, box) in enumerate(frames):
        points = kpts[n] if kpts else None
        det = Detection(cls=0, name="person", score=0.9, bbox_xyxy=box)
        attached = {} if points is None else {1: points}
        out += features.person_states(
            [(1, det)], attached, ts, FRAME_H, history, s.features, s.pose.kpt_conf
        )
    return out


def _walker(times: list[int], bh_s: float, h: float = 100.0) -> list[tuple[int, Box]]:
    """An upright box (h/w 2.5) whose foot moves at `bh_s` heights per second."""
    return [(t, (bh_s * h * t / 1000, 100.0, bh_s * h * t / 1000 + 40, 100 + h)) for t in times]


def test_speed_body_heights_per_second() -> None:
    steady = _states(_walker(list(range(0, 1600, 80)), 2.0))
    assert steady[-1].speed_bh_s == pytest.approx(2.0, rel=0.05)
    assert steady[-1].ref_height_px == 100.0
    assert steady[0].speed_bh_s is None  # one point

    three = _states(_walker([0, 450, 900], 2.0))  # gaps 450 ms, coverage 0.9 s, but 3 points
    assert three[-1].speed_bh_s is None
    four = _states(_walker([0, 300, 600, 900], 2.0))
    assert four[-1].speed_bh_s == pytest.approx(2.0, rel=0.05)

    gap = _states(_walker([*range(0, 480, 80), 1000, 1080], 2.0))  # 0.6 s hole inside the window
    assert gap[-1].speed_bh_s is None
    short = _states(_walker([*range(0, 480, 80), 900, 980, 1060], 2.0))  # holes of 0.5 s at most
    assert short[-1].speed_bh_s is not None


def test_pose_attached_by_iou() -> None:
    person: Box = (0.0, 0.0, 100.0, 100.0)
    points: list[Keypoint] = [(50.0, 50.0, 0.9)] * 17
    for h, attached in [(50.0, True), (49.0, False)]:  # IoU = h / 100
        pose = Detection(cls=0, name="0", score=0.9, bbox_xyxy=(0.0, 0.0, 100.0, h), kpts=points)
        got = features.attach_keypoints([person], [pose], get_settings().pose.match_iou)
        assert (got == {0: points}) is attached, h


def _torso(deg: float) -> list[Keypoint]:
    """Hips at (500, 500); shoulders 100 px away at `deg` from the vertical; ankles hidden."""
    sx = 500 + 100 * math.sin(math.radians(deg))
    sy = 500 - 100 * math.cos(math.radians(deg))
    points: list[Keypoint] = [(0.0, 0.0, 0.0)] * 17
    for i in (5, 6):
        points[i] = (sx, sy, 0.9)
    for i in (11, 12):
        points[i] = (500.0, 500.0, 0.9)
    return points


def test_posture_from_pose_and_bbox() -> None:
    box: Box = (400.0, 300.0, 600.0, 700.0)
    for deg, posture in [(65, "lying"), (25, "upright"), (45, "unknown")]:
        state = _states([(0, box)], [_torso(deg)])[0]
        assert (state.posture, state.posture_method) == (posture, "pose"), deg
        assert state.torso_deg == pytest.approx(deg)
        assert not state.feet_visible  # pose without visible ankles

    by_box = [
        ((0.0, 0.0, 100.0, 120.0), "upright"),  # h/w 1.2
        ((0.0, 0.0, 100.0, 119.0), "unknown"),
        ((0.0, 0.0, 130.0, 100.0), "lying"),  # w/h 1.3
        ((0.0, 0.0, 129.0, 100.0), "unknown"),
    ]
    for b, posture in by_box:
        state = _states([(0, b)])[0]
        assert (state.posture, state.posture_method) == (posture, "bbox"), b
        assert state.feet_visible  # bottom far from the frame edge

    upright = [(t, (0.0, 100.0, 40.0, 100.0 + h)) for t, h in [(0, 98), (80, 100), (160, 102)]]
    lying = [(240 + 80 * n, (0.0, 160.0, 120.0, 200.0)) for n in range(40)]  # 3.2 s on the floor
    states = _states([*upright, *lying])
    assert states[2].ref_height_px == 100.0
    assert {s.ref_height_px for s in states[3:]} == {100.0}  # frozen while lying
    assert states[-1].lying_since_ms == 240 and states[-1].last_upright_ms == 160
