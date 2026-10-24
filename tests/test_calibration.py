"""Slice 9: calibration of tech.md 8.11 and its validation (tech.md 9); meters in the features."""

import math
from pathlib import Path
from typing import Any

import cv2
import httpx
import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from safewatch import registry, services
from safewatch.analysis import geometry, pipeline
from safewatch.config import Settings, get_settings
from safewatch.types import (
    AnalysisConfig,
    ApiError,
    Calibration,
    CalibrationIn,
    CameraIn,
    CameraRule,
    Detection,
    FrameDetections,
    SectorIn,
)

ADMIN, OHS = {"X-Role": "admin"}, {"X-Role": "ohs"}
SQUARE = [(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)]
FLOOR = [(0.0, 0.0), (8.0, 0.0), (8.0, 6.0), (0.0, 6.0)]


def camera() -> int:
    sector = services.sector_create(SectorIn(name="Цех калибровки"), "admin")
    return services.camera_create(CameraIn(sector_id=sector.id, name="Камера"), "admin").id


def body(image: list[Any], world: list[Any], control: list[Any] | None = None) -> dict[str, Any]:
    return {"image_points": image, "world_points": world, "control_points": control or []}


_jitter = st.floats(-0.08, 0.08)


@given(
    shifts=st.lists(st.tuples(_jitter, _jitter), min_size=4, max_size=4),
    size=st.tuples(st.floats(2, 40), st.floats(2, 40)),
    query=st.tuples(st.floats(0.2, 0.8), st.floats(0.2, 0.8)),
)
def _maps_known_perspective(
    shifts: list[tuple[float, float]], size: tuple[float, float], query: tuple[float, float]
) -> None:
    image = [(x + dx, y + dy) for (x, y), (dx, dy) in zip(SQUARE, shifts, strict=True)]
    w, d = size
    world = [(0.0, 0.0), (w, 0.0), (w, d), (0.0, d)]
    known = cv2.getPerspectiveTransform(np.float32(image), np.float32(world)).astype(np.float64)
    h = geometry.homography(image, world)
    assert h is not None
    for p, q in zip(image, world, strict=True):
        assert math.dist(geometry.apply_h(h, p), q) < 1e-6
    # A point off the fit follows the same perspective (float32 input of the reference).
    assert math.dist(geometry.apply_h(h, query), geometry.apply_h(known, query)) < 1e-3 * max(w, d)


async def test_homography_maps_points(client: httpx.AsyncClient) -> None:
    _maps_known_perspective()

    camera_id = camera()
    url = f"/api/cameras/{camera_id}/calibration"
    assert (await client.get(url)).json() is None
    control = [{"image": [0.5, 0.5], "world": [4.0, 3.0]}]
    assert (
        await client.put(url, json=body(SQUARE, FLOOR, control), headers=OHS)
    ).status_code == 403
    assert (await client.put(url, json=body(SQUARE, FLOOR))).status_code == 400
    r = await client.put(url, json=body(SQUARE, FLOOR, control), headers=ADMIN)
    assert r.status_code == 200, r.text
    cal = Calibration.model_validate(r.json())
    assert cal.fit_rmse_m < 1e-6
    assert cal.control_rmse_m is not None and cal.control_rmse_m < 1e-6
    assert Calibration.model_validate((await client.get(url)).json()) == cal
    assert services.camera_get(camera_id).has_calibration
    # 9 vertical and 7 horizontal 1 m lines of the 8 x 6 m floor, all inside the frame.
    assert len(cal.grid) == 9 + 7
    assert all(0 <= v <= 1 for seg in cal.grid for point in seg for v in point)
    first = cal.grid[0]  # the line x = 0 m is the left edge of the square
    assert math.dist(first[0], (0.1, 0.1)) < 1e-9 and math.dist(first[1], (0.1, 0.9)) < 1e-9

    off = [{"image": [0.5, 0.5], "world": [5.0, 3.0]}]  # 1 m away from the fitted floor
    r = await client.put(url, json=body(SQUARE, FLOOR, off), headers=ADMIN)
    assert abs(Calibration.model_validate(r.json()).control_rmse_m - 1.0) < 1e-6  # type: ignore[operator]
    r = await client.put(url, json=body(SQUARE, FLOOR), headers=ADMIN)
    assert Calibration.model_validate(r.json()).control_rmse_m is None  # «нет контрольных точек»

    assert (await client.delete(url)).status_code == 400
    assert (await client.delete(url, headers=ADMIN)).status_code == 204
    assert (await client.get(url)).json() is None
    assert (await client.get("/api/cameras/999/calibration")).status_code == 404


def _ring(n: int, cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    """n points on a circle: no three on one line."""
    return [
        (cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n))
        for k in range(n)
    ]


async def test_calibration_validation(client: httpx.AsyncClient) -> None:
    url = f"/api/cameras/{camera()}/calibration"

    async def put(image: list[Any], world: list[Any]) -> tuple[int, str]:
        r = await client.put(url, json=body(image, world), headers=ADMIN)
        return r.status_code, ApiError.model_validate(r.json()).message if r.is_error else ""

    for n in (4, 8):
        assert (await put(_ring(n, 0.5, 0.5, 0.4), _ring(n, 5, 5, 4)))[0] == 200
    for n in (3, 9):
        assert await put(_ring(n, 0.5, 0.5, 0.4), _ring(n, 5, 5, 4)) == (
            422,
            "Нужно от 4 до 8 точек",
        )
    assert (await put(_ring(4, 0.5, 0.5, 0.4), _ring(5, 5, 5, 4)))[0] == 422
    assert await put([(1.01, 0.1), *SQUARE[1:]], FLOOR) == (422, "Точки вне кадра")
    line = [(0.1, 0.1), (0.5, 0.5), (0.9, 0.9), (0.1, 0.9)]
    assert await put(line, FLOOR) == (422, "Три точки на одной прямой")
    floor_line = [(0.0, 0.0), (4.0, 0.0), (8.0, 0.0), (0.0, 6.0)]
    assert await put(SQUARE, floor_line) == (422, "Три точки на одной прямой")


# --- criterion 8: meters on the floor ------------------------------------------------------
W, H, FPS = 1000, 500, 10


def _walk(x0: float) -> list[FrameDetections]:
    """A person 100 px tall walks right at 100 px/s: 1 height per second, below 1,5."""
    frames = []
    for i in range(40):
        x = x0 + 10 * i
        box = (x, 300.0, x + 40, 400.0)
        det = Detection(cls=0, name="person", score=0.9, bbox_xyxy=box)
        frames.append(FrameDetections(frame_idx=i, ts_ms=i * 100, detections=[det]))
    return frames


def _config(calibration: Calibration | None, rules: dict[str, CameraRule]) -> AnalysisConfig:
    s = get_settings()
    return AnalysisConfig(
        width=W, height=H, fps=FPS, step=1, duration_ms=4000, calibration=calibration, zones=[],
        rules=rules, class_conf=s.class_conf, active_classes=registry.active_classes(s),
    )  # fmt: skip


def _speed_tags(result_hud: list[Any]) -> set[tuple[str, str | None]]:
    tags = {(t.text, t.level) for f in result_hud for o in f.objects for t in o.tags}
    return {(text.split(" (")[0].split(" ")[-1], level) for text, level in tags}


def test_running_uses_m_s_with_calibration(core: Settings) -> None:
    # The left half of the frame is 15 m wide: 500 px = 15 m, the walker does 3 m/s there.
    cal = services.calibration_set(
        camera(),
        CalibrationIn(
            image_points=[(0.0, 0.0), (0.5, 0.0), (0.5, 1.0), (0.0, 1.0)],
            world_points=[(0.0, 0.0), (15.0, 0.0), (15.0, 5.0), (0.0, 5.0)],
        ),
        "admin",
    )
    to_floor = pipeline._ground(_config(cal, {}))
    assert to_floor is not None
    inside = to_floor((250.0, 250.0))
    assert inside is not None and math.dist(inside, (7.5, 2.5)) < 1e-6
    assert to_floor((750.0, 250.0)) is None  # outside the hull of the points

    model = registry.resolve(get_settings().pipeline.detector)
    left = pipeline.analyze(_walk(20), None, Path("unused.mp4"), _config(cal, {}), None, model)
    assert [(e.scenario, e.method) for e in left.episodes] == [("running", "calibrated")]
    assert left.episodes[0].reason_text == "Бег 3,0 м/с"
    assert ("м/с", "yellow") in _speed_tags(left.hud)

    right = pipeline.analyze(_walk(520), None, Path("unused.mp4"), _config(cal, {}), None, model)
    assert right.episodes == []  # relative: 1 height per second is below 1,5
    assert ("роста/с", None) in _speed_tags(right.hud)
    assert all(t != "м/с" for t, _ in _speed_tags(right.hud))

    # The camera rule raises the threshold: no episode, and the HUD follows the rule.
    slow = CameraRule(
        camera_id=1, scenario="running", enabled=True, params={"speed_m_s": 3.5}, effective={},
        status="active",
    )  # fmt: skip
    cfg = _config(cal, {"running": slow})
    tuned = pipeline.analyze(_walk(20), None, Path("unused.mp4"), cfg, None, model)
    assert tuned.episodes == []
    assert ("м/с", None) in _speed_tags(tuned.hud)
    assert ("м/с", "yellow") not in _speed_tags(tuned.hud)
