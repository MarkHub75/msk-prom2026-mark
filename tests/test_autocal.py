"""Slice 19: autocalibration by the height of standing people and speed in m/s (tech.md 8.21)."""

from pathlib import Path
from typing import Any

import httpx
import pytest
from test_analysis_api import _demo_job
from test_calibration import camera
from test_jobs import _tune
from test_rule_running import context, person, truck

from safewatch import registry, rules, services, store
from safewatch.analysis import autocal, features, hud, pipeline
from safewatch.config import Settings, get_settings
from safewatch.rules.proximity import ProximityPlugin
from safewatch.rules.running import RunningPlugin
from safewatch.types import (
    Analysis,
    AnalysisConfig,
    AutoCalibration,
    CalibrationIn,
    CameraSetupView,
    Detection,
    EpisodeDraft,
    FrameDetections,
    Observation,
    PersonState,
    VehicleState,
)

W, H = 1600, 900
A, B = 50.0, 0.4  # height of a standing person in px: h = A + B·y2
CAL = AutoCalibration(
    ok=True, reason="", samples=40, a_px=A, b=B, rmse_px=0.0, r2=1.0, person_height_m=1.7
)


def _det(x1: float, y2: float, h: float, score: float = 0.9, w: float | None = None) -> Detection:
    w = h / 2.5 if w is None else w  # h/w = 2,5: standing by the bbox
    return Detection(cls=0, name="person", score=score, bbox_xyxy=(x1, y2 - h, x1 + w, y2))


def _people(
    n: int, a: float = A, b: float = B, rows: tuple[float, float] = (200, 880), jitter: float = 0
) -> list[Detection]:
    """n standing people on the line h = a + b·y2, feet spread over `rows`, ±jitter of h."""
    out = []
    for i in range(n):
        y2 = rows[0] + (rows[1] - rows[0]) * i / max(n - 1, 1)
        out.append(_det(20 + 30 * i, y2, (a + b * y2) * (1 + jitter * (-1) ** i)))
    return out


def _fit(dets: list[Detection], **cfg: Any) -> AutoCalibration:
    s = get_settings()
    frames = [FrameDetections(frame_idx=0, ts_ms=0, detections=dets)]
    section = s.autocal.model_copy(update=cfg)
    return autocal.fit(frames, {0}, W, H, section, s.features.upright_hw, s.tracker.high_thresh)


def _close(value: float, target: float, share: float) -> bool:
    return abs(value - target) <= share * abs(target)


# --- criterion 1 ---------------------------------------------------------------------------
def test_fit_recovers_height_line() -> None:
    cal = _fit(_people(40, jitter=0.03))
    assert (cal.ok, cal.reason, cal.samples, cal.person_height_m) == (True, "", 40, 1.7)
    assert _close(cal.a_px, A, 0.02) and _close(cal.b, B, 0.02)
    assert 0 < cal.rmse_px < 0.03 * (A + B * 880) and cal.r2 > 0.95
    assert autocal.scale_at(cal, 500) == pytest.approx(1.7 / (cal.a_px + cal.b * 500))

    # The filters of 8.21 item 1, each on the threshold and one step past it.
    line = _people(40)
    y2, h = 500.0, A + B * 500
    assert _fit([*line, _det(1300, y2, h, score=0.5)]).samples == 41  # tracker.high_thresh
    assert _fit([*line, _det(1300, y2, h, score=0.49)]).samples == 40
    assert _fit([*line, _det(1300, y2, h, w=h / 1.2)]).samples == 41  # features.upright_hw
    assert _fit([*line, _det(1300, y2, h, w=h / 1.19)]).samples == 40
    other = _det(1300, y2, h).model_copy(update={"cls": 2})
    assert _fit([*line, other]).samples == 40  # not a person
    lowest = min(d.bbox_xyxy[3] - d.bbox_xyxy[1] for d in line)  # 130 px at y2 = 200
    assert _fit(line, min_person_px=lowest).samples == 40  # autocal.min_person_px
    assert _fit(line, min_person_px=lowest + 0.01).samples == 39
    assert _fit(line, person_height_m=1.8).person_height_m == 1.8  # autocal.person_height_m
    assert autocal.scale_at(_fit(line, person_height_m=1.8), 500) == pytest.approx(1.8 / 250)


def test_too_few_samples_not_ok() -> None:
    assert _fit(_people(30)).ok
    few = _fit(_people(29))
    assert (few.ok, few.reason, few.samples) == (False, "Мало стоящих людей в кадре: 29 из 30", 29)
    assert autocal.scale_at(few, 500) is None
    assert _fit(_people(29), min_samples=29).ok  # autocal.min_samples
    assert _fit([]).reason == "Мало стоящих людей в кадре: 0 из 30"

    # ĥ(y) must stay above zero over the whole height of the frame.
    perspective = "Рост людей не согласуется с перспективой"
    zero_top = _fit(_people(40, a=-20, b=0.5))
    assert (zero_top.ok, zero_top.reason) == (False, perspective)
    assert _fit(_people(40, a=1, b=0.5)).ok
    falling = _people(40, a=400, b=-0.45, rows=(400, 600))  # ĥ(900) = -5 px
    assert (_fit(falling).ok, _fit(falling).reason) == (False, perspective)
    assert _fit(_people(40, a=400, b=-0.4, rows=(400, 600))).ok  # ĥ(900) = 40 px
    one_row = [_det(20 + 30 * i, 500, 250) for i in range(40)]  # the slope is unknown
    one_row_text = "Все люди стоят в одном ряду кадра: перспективу не оценить"
    assert (_fit(one_row).ok, _fit(one_row).reason) == (False, one_row_text)

    assert autocal.scale_at(CAL, -A / B) is None  # ĥ = 0 above the frame
    assert autocal.scale_at(CAL, -A / B + 1) == pytest.approx(1.7 / B)


# --- criterion 2 ---------------------------------------------------------------------------
def _at_edge(edge: str, margin: float) -> Detection:
    """A standing person on the line with `margin` px between the bbox and one frame edge."""
    if edge == "left":
        return _det(margin, 500, 250)
    if edge == "right":
        return _det(W - margin - 100, 500, 250)
    if edge == "top":
        y2 = (margin + A) / (1 - B)  # y2 − h = margin
        return _det(800, y2, A + B * y2)
    return _det(800, H - margin, A + B * (H - margin))


def test_outliers_rejected() -> None:
    inliers = _people(40, jitter=0.03)
    rows = (300, 450, 600, 750, 850)
    crouched = [_det(1300, y2, (A + B * y2) * 0.6, w=(A + B * y2) / 2.5) for y2 in rows]
    cut = [  # cut by the top edge of the frame: their bboxes touch it
        Detection(cls=0, name="person", score=0.9, bbox_xyxy=(1400, 0, 1440, y2))
        for y2 in (110, 120, 130, 140, 150)
    ]
    cal = _fit([*inliers, *crouched, *cut])
    assert (cal.ok, cal.samples) == (True, 40)
    assert _close(cal.a_px, A, 0.03) and _close(cal.b, B, 0.03)
    kept = _fit([*inliers, *crouched, *cut], iterations=0)  # autocal.iterations
    assert kept.samples == 45 and not (_close(kept.a_px, A, 0.03) and _close(kept.b, B, 0.03))
    assert _fit([*inliers, *crouched], max_residual=0.5).samples == 45  # autocal.max_residual

    # autocal.max_residual = 0,15: one point 14 % off the line stays, 16 % off goes.
    line = _people(40)
    assert _fit([*line, _det(1300, 500, 250 * 1.14)]).samples == 41
    assert _fit([*line, _det(1300, 500, 250 * 1.16)]).samples == 40

    # autocal.edge_px = 2: a bbox 2 px from an edge is not measured, 3 px is.
    for edge in ("left", "right", "top", "bottom"):
        assert _fit([*line, _at_edge(edge, 2)]).samples == 40, edge
        assert _fit([*line, _at_edge(edge, 3)]).samples == 41, edge
    assert _fit([*line, _at_edge("left", 3)], edge_px=3).samples == 40  # autocal.edge_px


# --- criterion 3 ---------------------------------------------------------------------------
FPS, SPEED = 10, 2.9  # a 1,7 m person walks 2,9 m/s on the row y2 = 500 (250 px tall)


def _walk(calibrators: bool) -> list[FrameDetections]:
    """30 frames; with `calibrators`, 8 people stand still above the walker (rows 100..240)."""
    px_s = SPEED * (A + B * 500) / 1.7
    rows = [100 + 20 * i for i in range(8)]
    still = [
        _det(100 + 180 * i, y2, (A + B * y2) * (1 + 0.04 * (-1) ** i)) for i, y2 in enumerate(rows)
    ]
    return [
        FrameDetections(
            frame_idx=i,
            ts_ms=i * 1000 / FPS,
            detections=[_det(50 + px_s * i / FPS, 500, 250), *(still if calibrators else [])],
        )
        for i in range(30)
    ]


def _config(calibration: Any = None) -> AnalysisConfig:
    s = get_settings()
    return AnalysisConfig(
        width=W, height=H, fps=FPS, step=1, duration_ms=3000, calibration=calibration, zones=[],
        rules={}, class_conf=s.class_conf, active_classes=registry.active_classes(s),
    )  # fmt: skip


def _walker_states(frames: list[FrameDetections], cal: AutoCalibration | None) -> PersonState:
    s, history = get_settings(), {}
    states: list[PersonState] = []
    for f in frames:
        walker = f.detections[0]
        states = features.person_states(
            [(1, walker)], {}, round(f.ts_ms), H, history, s.features, s.pose.kpt_conf, None, cal
        )
    return states[0]


def _speed_texts(result_hud: list[Any]) -> set[str]:
    return {t.text for f in result_hud for o in f.objects for t in o.tags if t.code == "speed"}


def test_speed_auto_m_s_within_20pct() -> None:
    model = registry.resolve(get_settings().pipeline.detector)
    result = pipeline.analyze(_walk(True), None, Path("unused.mp4"), _config(), None, model)
    assert result.auto_calibration is not None and result.auto_calibration.ok
    (episode,) = result.episodes
    assert (episode.scenario, episode.method) == ("running", "auto")
    assert _close(episode.metrics["speed_m_s"], SPEED, 0.2)
    assert any(
        t.startswith("бег ≈") and t.endswith(" м/с (авто)") for t in _speed_texts(result.hud)
    )

    last = _walker_states(_walk(True), result.auto_calibration)
    assert last.speed_source == "auto" and last.speed_m_s is not None
    assert _close(last.speed_m_s, SPEED, 0.2)

    # Without manual calibration and autocalibration: heights per second, no meters.
    alone = pipeline.analyze(_walk(False), None, Path("unused.mp4"), _config(), None, model)
    assert alone.auto_calibration is not None and not alone.auto_calibration.ok
    assert [e.method for e in alone.episodes] == ["relative"]
    assert all(t.endswith("роста/с") for t in _speed_texts(alone.hud))
    relative = _walker_states(_walk(False), alone.auto_calibration)
    assert (relative.speed_m_s, relative.speed_source) == (None, "relative")
    assert relative.speed_bh_s is not None
    assert _walker_states(_walk(True), None).speed_source == "relative"


def test_manual_calibration_wins(core: Settings) -> None:
    # The whole frame is 16 x 9 m: 100 px per meter, the walker does 4,3 m/s on this floor.
    cal = services.calibration_set(
        camera(),
        CalibrationIn(
            image_points=[(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)],
            world_points=[(0.0, 0.0), (16.0, 0.0), (16.0, 9.0), (0.0, 9.0)],
        ),
        "admin",
    )
    model = registry.resolve(get_settings().pipeline.detector)
    result = pipeline.analyze(_walk(True), None, Path("unused.mp4"), _config(cal), None, model)
    assert result.auto_calibration is not None and result.auto_calibration.ok  # fitted anyway
    (episode,) = result.episodes
    assert episode.method == "calibrated"
    px_s = SPEED * (A + B * 500) / 1.7
    assert episode.metrics["speed_m_s"] == pytest.approx(px_s / 100, rel=1e-3)
    assert all(t.endswith(" м/с (калибровка)") for t in _speed_texts(result.hud))


# --- criterion 4 ---------------------------------------------------------------------------
def _run(p: PersonState, cal: AutoCalibration | None, **params: float) -> Observation:
    ctx = context(p).model_copy(update={"auto_calibration": cal})
    (o,) = RunningPlugin().observe(ctx, rules.defaults("running") | params)
    return o


def test_running_uses_auto_threshold() -> None:
    def auto(v: float) -> PersonState:
        return person(speed_m_s=v, speed_source="auto", speed_bh_s=0.1)

    fast = _run(auto(2.5), CAL)
    assert (fast.state, fast.method, fast.reason_text) == ("P", "auto", "Бег 2,5 м/с")
    assert fast.metrics == {"speed_m_s": 2.5, "autocal_samples": 40}
    slow = _run(auto(2.49), CAL)
    assert (slow.state, slow.method) == ("N", "auto")
    assert _run(auto(2.9), CAL, speed_m_s=3.0).state == "N"  # the camera's threshold

    # No autocalibration: heights per second as in v4.
    relative = _run(person(speed_bh_s=1.5), None)
    assert (relative.state, relative.method) == ("P", "relative")
    assert (_run(person(speed_bh_s=1.49), None).state, relative.metrics) == (
        "N",
        {"speed_bh_s": 1.5},
    )


# --- criterion 5 ---------------------------------------------------------------------------
def _tags(p: PersonState, **running: float) -> list[tuple[str, str | None]]:
    ctx = context(p)
    frame = hud.build_hud(ctx, rules.defaults("running") | running, get_settings().features, [])
    return [(t.text, t.level) for t in frame.objects[0].tags if t.code == "speed"]


def _draft(method: str, metrics: dict[str, float]) -> EpisodeDraft:
    return EpisodeDraft(
        scenario="running", subject="track:1", zone_id=None, level_initial="yellow",
        level_max="yellow", start_ms=0, confirm_ms=1000, escalate_ms=None, end_ms=5000,
        end_reason="video_end", reason_code="running", reason_text="", method=method,
        confidence=0.9, metrics=metrics, uncertain_ms=0, confirm_frame_idx=10,
        escalate_frame_idx=None,
    )  # fmt: skip


def test_hud_labels_auto_and_calibration() -> None:
    def tagged(v: float, source: str) -> PersonState:
        return person(speed_m_s=v, speed_source=source, speed_bh_s=0.1)

    assert _tags(tagged(2.9, "auto")) == [("бег ≈2,9 м/с (авто)", "yellow")]
    assert _tags(tagged(2.5, "auto")) == [("бег ≈2,5 м/с (авто)", "yellow")]
    assert _tags(tagged(2.4, "auto")) == [("≈2,4 м/с (авто)", None)]
    assert _tags(tagged(2.9, "calibration")) == [("бег 2,9 м/с (калибровка)", "yellow")]
    assert _tags(tagged(2.4, "calibration")) == [("2,4 м/с (калибровка)", None)]
    assert _tags(person(speed_bh_s=2.4), speed_bh_s=3.0) == [("2,4 роста/с", None)]
    assert _tags(person(speed_bh_s=2.4)) == [("бег 2,4 роста/с", "yellow")]

    params = rules.defaults("running")
    why = RunningPlugin().explain(_draft("auto", {"speed_m_s": 2.9, "autocal_samples": 34}), params)
    lines = {w.label: w.value for w in why}
    assert lines["Скорость"] == "автокалибровка по росту людей (34 замеров, точность около ±20 %)"
    assert lines["Правило"] == "Бег: скорость выше 2,5 м/с дольше 1,0 с"
    assert lines["Метод"] == "автокалибровка" and "autocal_samples" not in lines
    calibrated = RunningPlugin().explain(_draft("calibrated", {"speed_m_s": 2.9}), params)
    assert {w.label: w.value for w in calibrated}["Скорость"] == "по калибровке камеры"
    relative = RunningPlugin().explain(_draft("relative", {"speed_bh_s": 2.0}), params)
    assert "Скорость" not in {w.label for w in relative}


# --- criterion 6 ---------------------------------------------------------------------------
def _pair(x1: float, cal: AutoCalibration | None, **params: float) -> Observation:
    moving = truck(x1).model_copy(update={"speed_m_s": 1.0, "speed_source": "auto"})
    ctx = context(person(), vehicles=[moving]).model_copy(update={"auto_calibration": cal})
    (o,) = ProximityPlugin().observe(ctx, rules.defaults("proximity") | params)
    return o


def test_proximity_meters_with_autocal() -> None:
    # Feet at y = 300: ĥ = 170 px for 1,7 m, 0,01 m per px; the truck starts 100 px away per meter.
    red = _pair(600, CAL)
    assert (red.state, red.level, red.method) == ("P", "red", "auto")
    assert red.metrics == {"distance_m": pytest.approx(1.0)}
    assert red.reason_text == "Сближение с грузовиком: 1,0 м"
    assert (_pair(601, CAL).level, _pair(800, CAL).level) == ("yellow", "yellow")  # red_m, yellow_m
    assert _pair(801, CAL).state == "N"
    assert _pair(700, CAL, red_m=2.0).level == "red"  # the camera's thresholds in meters
    assert _pair(700, CAL, yellow_m=1.5).state == "N"
    not_ok = CAL.model_copy(update={"ok": False})
    assert (_pair(600, not_ok).method, _pair(600, None).method) == ("relative", "relative")
    assert _pair(600, None).metrics == {"distance_bh": 1.0}
    why = ProximityPlugin().explain(
        _draft("auto", {}).model_copy(update={"scenario": "proximity", "reason_code": "proximity"}),
        rules.defaults("proximity"),
    )
    assert why[0].value.startswith("Сближение: техника движется, дистанция до 1,0 м")

    # A vehicle's speed: the middle of its bottom edge, scaled at its row (8.21).
    s, history = get_settings(), {}
    states: list[VehicleState] = []
    for i in range(6):  # 100 px/s on the row y = 300: 1,0 m/s
        box = (100 + 10.0 * i, 100.0, 300 + 10.0 * i, 300.0)
        det = Detection(cls=7, name="truck", score=0.9, bbox_xyxy=box)
        states = features.vehicle_states([(9, det)], i * 100, history, s.features, None, CAL)
    assert states[0].speed_source == "auto"
    assert states[0].speed_m_s == pytest.approx(1.0)


# --- criterion 7 ---------------------------------------------------------------------------
async def test_analysis_stores_autocal(
    client: httpx.AsyncClient,
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
) -> None:
    camera_id = camera()
    empty = await client.get(f"/api/admin/cameras/{camera_id}")
    assert CameraSetupView.model_validate(empty.json()).auto_calibration is None  # no video yet
    job = await _demo_job(monkeypatch, tmp_path, camera_id)
    row = store.analysis(job.analysis_id or 0)
    assert row is not None and row["autocal_json"] is not None
    stored = AutoCalibration.model_validate_json(row["autocal_json"])
    assert stored.person_height_m == 1.7
    r = await client.get(f"/api/videos/{job.video_id}/analysis")
    assert Analysis.model_validate(r.json()).auto_calibration == stored
    setup = await client.get(f"/api/admin/cameras/{camera_id}")
    assert CameraSetupView.model_validate(setup.json()).auto_calibration == stored

    # A recompute fits anew: another configured height lands in the new analysis.
    _tune(monkeypatch, core, autocal={"person_height_m": 1.8})
    services.video_recompute(job.video_id, "admin")
    done = await services.run_next_job()
    assert done is not None and done.analysis_id != job.analysis_id
    fresh = services.video_analysis(job.video_id).auto_calibration
    assert fresh is not None and fresh.person_height_m == 1.8
    assert services.camera_setup_view(camera_id).auto_calibration == fresh

    # An analysis made before v5 has no fit.
    store.run("UPDATE analyses SET autocal_json = NULL WHERE id = ?", done.analysis_id)
    assert services.video_analysis(job.video_id).auto_calibration is None
    assert services.camera_setup_view(camera_id).auto_calibration is None
