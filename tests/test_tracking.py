"""Slice 4: the tracker of tech.md 8.2 item 4 and the class filter before it."""

import itertools
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import settings as hyp_settings
from hypothesis import strategies as st

from safewatch import registry
from safewatch.analysis.pipeline import analyze
from safewatch.analysis.tracking import Tracker
from safewatch.config import get_settings
from safewatch.fakes import scenes
from safewatch.types import AnalysisConfig, Box, Detection, FrameDetections

W, H = 800, 240  # a walker of 0.4 H = 96 px crosses 6 heights without wrapping at the edge
STEP_MS = 80  # 25 fps, step 2
VIDEO = Path("unused.mp4")  # analyze reads the video only from slice 11 on


def _cfg() -> AnalysisConfig:
    s = get_settings()
    return AnalysisConfig(
        width=W, height=H, fps=25, step=2, duration_ms=0, calibration=None, zones=[], rules={},
        class_conf=s.class_conf, active_classes=registry.active_classes(s),
    )  # fmt: skip


def _people(scene: str, seconds: float) -> list[list[tuple[int | None, float]]]:
    """Per HUD frame: (track id, bbox center x) of every person."""
    det = scenes.render(scene, W, H, 25, round(seconds * 25), 2, "detect")
    model = registry.resolve(get_settings().pipeline.detector)
    result = analyze(det, None, VIDEO, _cfg(), None, model)
    return [
        [(o.track_id, (o.bbox[0] + o.bbox[2]) / 2) for o in f.objects if o.kind == "person"]
        for f in result.hud
    ]


def _det(box: Box, score: float = 0.9, name: str = "person") -> Detection:
    return Detection(cls=0, name=name, score=score, bbox_xyxy=box)


def _tracker() -> Tracker:
    return Tracker(get_settings().tracker, itertools.count(1))


BOX: Box = (100.0, 50.0, 140.0, 150.0)


def test_single_walker_keeps_one_id() -> None:
    frames = _people("walk", 10)
    ids = {track_id for frame in frames for track_id, _ in frame}
    assert ids == {1}
    assert all(len(frame) == 1 for frame in frames[1:])  # confirmed from the second frame


def test_crossing_people_keep_ids() -> None:
    frames = _people("two_walkers_crossing", 5)
    first = dict(frames[2])
    last = dict(frames[-1])
    assert len(first) == len(last) == 2
    left_start = min(first, key=lambda k: first[k])
    right_end = max(last, key=lambda k: last[k])
    assert left_start == right_end  # the walker from the left ends on the right
    assert {track_id for frame in frames for track_id, _ in frame} == set(first)


@pytest.mark.parametrize(("gap_ms", "same"), [(900, True), (1000, True), (1100, False)])
def test_lost_longer_than_ttl_gets_new_id(gap_ms: int, same: bool) -> None:
    tracker = _tracker()
    tracker.update(0, [_det(BOX)])
    assert tracker.update(STEP_MS, [_det(BOX)]) == [(1, _det(BOX))]
    back = STEP_MS + gap_ms
    out = tracker.update(back, [_det(BOX)])
    if same:
        assert [track_id for track_id, _ in out] == [1]
    else:
        assert out == []  # a new tentative track
        assert [t for t, _ in tracker.update(back + STEP_MS, [_det(BOX)])] == [2]


def test_low_score_only_extends_tracks() -> None:
    tracker = _tracker()
    tracker.update(0, [_det(BOX)])
    tracker.update(80, [_det(BOX)])
    for n, score in enumerate([0.1, 0.3, 0.5]):  # low and high stage keep the track
        assert [t for t, _ in tracker.update(160 + n * 80, [_det(BOX, score)])] == [1]
    assert tracker.update(400, [_det(BOX, 0.09)]) == []  # below low_thresh: not a detection
    far: Box = (500.0, 50.0, 540.0, 150.0)
    for opener, opens in [(0.3, False), (0.5, False), (0.59, False), (0.6, True)]:
        fresh = _tracker()
        fresh.update(0, [_det(far, opener)])
        out = fresh.update(80, [_det(far, 0.9)])
        # Opened at `opener`, the second hit confirms; not opened, 0.9 only starts a track.
        assert bool(out) is opens, opener


@hyp_settings(max_examples=30, deadline=None)
@given(
    x=st.floats(0, 600),
    speed=st.floats(-20, 20),
    frames=st.integers(3, 30),
)
def test_steady_walker_never_switches_id(x: float, speed: float, frames: int) -> None:
    """Property: one box moving steadily keeps id 1 whatever its start and speed."""
    tracker = _tracker()
    seen = set()
    for n in range(frames):
        dx = x + n * speed
        for track_id, _ in tracker.update(n * STEP_MS, [_det((dx, 50, dx + 40, 150))]):
            seen.add(track_id)
    assert seen == {1}


@pytest.mark.parametrize(("score", "kept"), [(0.34, False), (0.35, True)])
def test_class_conf_filters_before_tracking(score: float, kept: bool) -> None:
    model = registry.resolve(get_settings().pipeline.detector)
    truck = next(cls for cls, name in model.classes.items() if name == "truck")
    box: Box = (100.0, 20.0, 400.0, 220.0)

    def frame(n: int, s: float) -> FrameDetections:
        d = Detection(cls=truck, name="7", score=s, bbox_xyxy=box)
        return FrameDetections(frame_idx=n * 2, ts_ms=n * STEP_MS, detections=[d])

    det = [frame(0, 0.9), frame(1, 0.9), frame(2, score)]
    hud = analyze(det, None, VIDEO, _cfg(), None, model).hud
    vehicles = [o for o in hud[2].objects if o.kind == "vehicle"]
    assert [(o.label, o.track_id) for o in vehicles] == ([("грузовик", 1)] if kept else [])
