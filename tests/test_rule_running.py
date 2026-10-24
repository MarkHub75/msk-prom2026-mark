"""Slice 5: the `running` plugin (tech.md 8.3) and how analyze() picks the plugins."""

from pathlib import Path

from safewatch import registry, rules
from safewatch.analysis.pipeline import analyze
from safewatch.config import get_settings
from safewatch.fakes import scenes
from safewatch.rules.running import RunningPlugin
from safewatch.types import (
    AnalysisConfig,
    CameraRule,
    FrameContext,
    Observation,
    PersonState,
    VehicleState,
    Zone,
)

W, H = 1000, 500
PERSON = (480.0, 200.0, 520.0, 300.0)  # 100 px tall, foot at (500, 300)


def person(**update: object) -> PersonState:
    base = PersonState(
        track_id=1, bbox=PERSON, score=0.9, foot=(500.0, 300.0), anchor=(500.0, 300.0),
        feet_visible=True, ground=None, height_px=100.0, ref_height_px=100.0, speed_bh_s=None,
        speed_m_s=None, posture="upright", posture_method="bbox", torso_deg=None,
        last_upright_ms=0, lying_since_ms=None, still_since_ms=None, prev_anchor=None,
        prev_ts_ms=None, kpts=None,
    )  # fmt: skip
    return base.model_copy(update=update)


def context(p: PersonState, zones: list[Zone] | None = None, vehicles=(), ts_ms: int = 0):
    return FrameContext(
        frame_idx=0, ts_ms=ts_ms, width=W, height=H, persons=[p], vehicles=list(vehicles),
        objects=[], zones=zones or [], calibrated=p.ground is not None,
    )  # fmt: skip


def zone(kind: str, name: str = "Пресс", zone_id: int = 7) -> Zone:
    # 0.4..0.6 of the frame: holds the foot at (500, 300) px = (0.5, 0.6)
    points = [(0.4, 0.4), (0.6, 0.4), (0.6, 0.7), (0.4, 0.7)]
    return Zone(id=zone_id, camera_id=1, kind=kind, name=name, points=points)


def truck(x1: float, footprint=None) -> VehicleState:
    return VehicleState(
        track_id=9, name="truck", bbox=(x1, 100.0, x1 + 200.0, 300.0), score=0.9,
        footprint=footprint, height_px=200.0, speed_vh_s=None, speed_m_s=None,
    )  # fmt: skip


def one(ctx: FrameContext, **params: float) -> Observation:
    (o,) = RunningPlugin().observe(ctx, rules.defaults("running") | params)
    return o


def test_running_threshold_boundary() -> None:
    fast = one(context(person(speed_bh_s=1.5)))
    assert (fast.state, fast.level, fast.hold_s, fast.subject) == ("P", "yellow", 1.0, "track:1")
    assert (fast.reason_text, fast.method, fast.metrics) == (
        "Бег 1,5 роста/с",
        "relative",
        {"speed_bh_s": 1.5},
    )
    assert one(context(person(speed_bh_s=1.49))).state == "N"
    assert one(context(person())).state == "U"
    assert one(context(person(speed_bh_s=1.5)), speed_bh_s=1.6).state == "N"
    # Calibrated speed wins over the speed in heights: the threshold is 2.5 m/s.
    metres = one(context(person(speed_bh_s=0.1, speed_m_s=2.5)))
    assert (metres.state, metres.reason_text, metres.method) == ("P", "Бег 2,5 м/с", "calibrated")
    assert one(context(person(speed_bh_s=3.0, speed_m_s=2.49))).state == "N"
    assert one(context(person(speed_m_s=2.5)), speed_m_s=2.6).state == "N"


def test_running_red_in_danger_zone() -> None:
    fast = person(speed_bh_s=2.0)
    for kind in ("danger", "vehicle_path"):
        red = one(context(fast, zones=[zone(kind)]))
        assert (red.level, red.hold_s, red.zone_id) == ("red", 0.5, 7), kind
        assert red.reason_text == "Бег 2,0 роста/с в зоне «Пресс»"
    assert one(context(fast, zones=[zone("rest")])).level == "yellow"
    assert one(context(fast, zones=[zone("danger")]), red_hold_s=0.8).hold_s == 0.8
    # Foot (500, 300) to the truck box: 3.0 H_ref → red, 3.01 → yellow.
    near = one(context(fast, vehicles=[truck(800.0)]))
    assert (near.level, near.reason_text) == ("red", "Бег 2,0 роста/с рядом с техникой")
    assert one(context(fast, vehicles=[truck(801.0)])).level == "yellow"
    assert one(context(fast, vehicles=[truck(801.0)]), near_vehicle_bh=3.01).level == "red"
    # Calibrated: from the floor point to the footprint segment, in meters.
    grounded = fast.model_copy(update={"ground": (0.0, 0.0)})
    at_3m = truck(900.0, footprint=((3.0, -1.0), (3.0, 1.0)))
    assert one(context(grounded, vehicles=[at_3m])).level == "red"
    far = truck(900.0, footprint=((3.1, -1.0), (3.1, 1.0)))
    assert one(context(grounded, vehicles=[far])).level == "yellow"
    assert one(context(grounded, vehicles=[far]), near_vehicle_m=3.1).level == "red"


def _demo(**cfg_update: object) -> list[str]:
    """Scenarios of the episodes analyze() finds on the synthetic demo scene."""
    s = get_settings()
    w, h, fps = 1600, 300, 10
    cfg = AnalysisConfig(
        width=w, height=h, fps=fps, step=1, duration_ms=20_000, calibration=None, zones=[],
        rules={}, class_conf=s.class_conf, active_classes=registry.active_classes(s),
    ).model_copy(update=cfg_update)  # fmt: skip
    det = scenes.render("demo", w, h, fps, 200, 1, "detect")
    pose = scenes.render("demo", w, h, fps, 200, 1, "pose")
    detector, pose_model = registry.resolve(s.pipeline.detector), registry.resolve(s.pipeline.pose)
    result = analyze(det, pose, Path("unused.mp4"), cfg, pose_model, detector)
    return [e.scenario for e in result.episodes]


def test_running_camera_rule_and_status() -> None:
    assert _demo() == ["running", "fall"]

    def rule(enabled: bool, params: dict[str, float]) -> CameraRule:
        return CameraRule(
            camera_id=1, scenario="running", enabled=enabled, params=params, effective={},
            status="active",
        )  # fmt: skip

    assert _demo(rules={"running": rule(False, {})}) == ["fall"]
    assert _demo(rules={"running": rule(True, {"speed_bh_s": 3.0})}) == ["fall"]  # runs 2,5
    assert _demo(rules={"running": rule(True, {"speed_bh_s": 2.0})}) == ["running", "fall"]
    assert _demo(active_classes=["car"]) == []  # model_missing: the plugins stay out
