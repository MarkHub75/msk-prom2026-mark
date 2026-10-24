from typing import Any

import httpx
import pytest
from test_broadcast import camera, ready_video

from safewatch import config, rules, services, store, texts
from safewatch.analysis.passport import build_passport
from safewatch.config import Settings
from safewatch.types import (
    CameraPassport,
    HudFrame,
    HudObject,
    ObservabilityGap,
    Zone,
)

W = H = 1000  # frame size: a box of n / 1000 is n px
DURATION = 10_000


@pytest.fixture
def cfg(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> Settings:
    """Test settings for the zone titles `build_passport` reads."""
    monkeypatch.setattr(config, "get_settings", lambda: settings)
    return settings


def person(px: float) -> HudObject:
    return HudObject(
        track_id=1, kind="person", label="человек", score=0.9,
        bbox=(0.1, 0.0, 0.2, px / H), kpts=None, tags=[],
    )  # fmt: skip


def phone(px: float) -> HudObject:
    """The longer side is `px`."""
    return HudObject(
        track_id=None, kind="phone", label="телефон", score=0.9,
        bbox=(0.5, 0.5, 0.5 + px / W, 0.5 + px / (2 * H)), kpts=None, tags=[],
    )  # fmt: skip


def frames(n: int = 100, objects: list[HudObject] | None = None, empty: int = 0) -> list[HudFrame]:
    """`n` frames, the first `empty` of them without objects, the rest with `objects`."""
    filled = [person(80), phone(20)] if objects is None else objects
    return [
        HudFrame(frame_idx=i, ts_ms=i * 100, objects=[] if i < empty else filled) for i in range(n)
    ]


def zones(*kinds: str) -> list[Zone]:
    return [
        Zone(id=i, camera_id=1, kind=k, name=k, points=[(0, 0), (1, 0), (1, 1)])
        for i, k in enumerate(kinds)
    ]


ALL_ZONES = ("danger", "vehicle_path", "fence", "under_load", "height", "helmet_required")
ALL_ZONES += ("respirator_required", "lying_allowed", "fire_allowed", "walkway", "rest")


def build(
    hud: list[HudFrame] | None = None,
    gaps: list[ObservabilityGap] | None = None,
    kinds: tuple[str, ...] = ALL_ZONES,
    analysis_id: int | None = 7,
    statuses: dict[str, str] | None = None,
    **passport: float,
) -> CameraPassport:
    """Every plugin active (the skeleton one stays skeleton) unless `statuses` says otherwise."""
    settings = config.get_settings()
    every = sorted({c for p in rules.PLUGINS for c in p.meta.required_classes})
    metas = [
        m.model_copy(update={"status": (statuses or {}).get(m.id, m.status)})
        for m in rules.scenario_metas(every)
    ]
    return build_passport(
        1, analysis_id, frames() if hud is None else hud, gaps or [], DURATION, W, H, metas,
        zones(*kinds), settings.passport.model_copy(update=passport),
        settings.features.min_person_px, rules.defaults("phone")["min_person_px"],
    )  # fmt: skip


def verdicts(p: CameraPassport) -> dict[str, tuple[str, str]]:
    return {s.scenario: (s.verdict, s.reason) for s in p.scenarios}


PEOPLE = [p.meta.id for p in rules.PLUGINS if "person" in p.meta.required_classes]


@pytest.mark.parametrize(
    ("px", "verdict", "reason"),
    [
        (39, "unsuitable", "Люди слишком мелкие: 39 px"),  # row 4
        (40, "partial", "Люди мелкие для уверенной оценки: 40 px"),  # row 7
        (79, "partial", "Люди мелкие для уверенной оценки: 79 px"),
        (80, "suitable", "Годна"),  # row 8
    ],
)
def test_verdicts_by_person_height(cfg: Settings, px: int, verdict: str, reason: str) -> None:
    p = build(frames(objects=[person(px), phone(20)]))
    assert p.person_height_px_p50 == px
    got = verdicts(p)
    for scenario in PEOPLE:
        if scenario != "phone":  # row 5 sees the same person first
            assert got[scenario] == (verdict, reason), scenario
    assert got["fire_smoking"] == ("suitable", "Годна")  # no people in the scenario


def test_metrics_and_people_rows(cfg: Settings) -> None:
    hud = frames(4, objects=[]) + frames(3, [person(30)]) + frames(3, [person(90), phone(15)])
    hud += frames(4, [person(80)])
    p = build(hud, [ObservabilityGap(start_ms=9_000, end_ms=12_000, reason="dark")])
    assert (p.frames, p.person_height_px_p50, p.small_object_px_p50) == (14, 80, 15)
    assert (p.person_frames_share, p.empty_share) == (10 / 14, 4 / 14)
    assert p.dark_share == 0.1  # clipped to the duration
    nobody = verdicts(build(frames(objects=[phone(20)])))
    assert nobody["running"] == ("unknown", "В записи нет людей")
    assert nobody["fire_smoking"] == ("suitable", "Годна")
    # A key of the passport changes the verdict: 79 px pass at 60.
    assert verdicts(build(frames(objects=[person(79)]), person_partial_px=60))["running"] == (
        "suitable",
        "Годна",
    )


@pytest.mark.parametrize(
    ("dark_ms", "reason", "verdict", "text"),
    [
        (2_000, "dark", "suitable", "Годна"),
        (2_100, "dark", "partial", "Темно или камера закрыта 21 % времени"),  # row 7
        (2_100, "obstructed", "partial", "Темно или камера закрыта 21 % времени"),
        (5_000, "dark", "partial", "Темно или камера закрыта 50 % времени"),
        (5_100, "dark", "unsuitable", "Слишком темно или камера закрыта 51 % времени"),  # row 3
        (5_100, "obstructed", "unsuitable", "Слишком темно или камера закрыта 51 % времени"),
        (5_100, "stale", "suitable", "Годна"),  # a stale stream is not darkness
    ],
)
def test_dark_share_partial(
    cfg: Settings, dark_ms: int, reason: Any, verdict: str, text: str
) -> None:
    p = build(gaps=[ObservabilityGap(start_ms=0, end_ms=dark_ms, reason=reason)])
    got = verdicts(p)
    assert got["running"] == (verdict, text)
    assert got["fire_smoking"] == (verdict, text)  # darkness hits every scenario


@pytest.mark.parametrize(
    ("empty", "verdict", "text"),
    [(80, "suitable", "Годна"), (81, "partial", "Пустые кадры: 81 % записи")],
)
def test_empty_share_partial(cfg: Settings, empty: int, verdict: str, text: str) -> None:
    got = verdicts(build(frames(100, empty=empty)))
    assert got["running"] == (verdict, text)


@pytest.mark.parametrize(
    ("statuses", "n", "scenario", "verdict", "reason"),
    [
        ({"running": "model_missing"}, 100, "running", "unknown", "Модель не подключена"),  # row 1
        ({}, 100, "load_carrying", "unknown", texts.SCENARIO_SKELETON),
        ({"running": "model_missing"}, 10, "running", "unknown", "Модель не подключена"),
        ({}, 49, "running", "unknown", "Мало кадров для оценки"),  # row 2
        ({}, 50, "running", "suitable", "Годна"),
    ],
)
def test_model_missing_unknown(
    cfg: Settings, statuses: dict[str, str], n: int, scenario: str, verdict: str, reason: str
) -> None:
    got = verdicts(build(frames(n), statuses=statuses))
    assert got[scenario] == (verdict, reason)


def test_min_frames_key(cfg: Settings) -> None:
    assert verdicts(build(frames(50), min_frames=51))["running"][0] == "unknown"


@pytest.mark.parametrize(
    ("scenario", "kinds", "objects", "verdict", "reason"),
    [
        ("fence_crossing", (), None, "partial", "Нет зон: Ограждение"),  # row 6
        ("fence_crossing", ("fence",), None, "suitable", "Годна"),
        ("no_helmet", ("danger",), None, "partial", "Нет зон: Обязательна каска"),
        ("restricted_under", (), None, "partial", "Нет зон: Под конвейером / грузом"),
        ("no_harness", (), None, "partial", "Нет зон: Работа на высоте"),
        ("no_respirator", (), None, "partial", "Нет зон: Обязателен респиратор"),
        ("fall", (), None, "suitable", "Годна"),  # works without its zone
        ("running", (), None, "suitable", "Годна"),
        ("phone", ALL_ZONES, [person(120), phone(11)], "partial", "Телефон виден плохо: 11 px"),
        ("phone", ALL_ZONES, [person(120), phone(12)], "suitable", "Годна"),  # row 5
        ("phone", ALL_ZONES, [person(119), phone(20)], "partial", "Телефон виден плохо: 119 px"),
        ("phone", ALL_ZONES, [person(120)], "suitable", "Годна"),  # no phone seen
    ],
)
def test_zone_missing_partial(
    cfg: Settings,
    scenario: str,
    kinds: tuple[str, ...],
    objects: list[HudObject] | None,
    verdict: str,
    reason: str,
) -> None:
    got = verdicts(build(frames(objects=objects), kinds=kinds))
    assert got[scenario] == (verdict, reason)


def _hud(video_id: int, hud: list[HudFrame]) -> None:
    """The HUD of the video's active analysis, written the way the analysis writes it."""
    video = store.video(video_id)
    assert video is not None
    analysis = store.analysis(video["active_analysis_id"])
    assert analysis is not None
    path = config.get_settings().data_dir / analysis["hud_path"]
    lines = "".join(frame.model_dump_json() + "\n" for frame in hud)
    path.write_text(lines, encoding="utf-8", newline="\n")
    with store.tx():
        store.video_update(video_id, {"width": W, "height": H})


async def test_no_analysis_unknown(client: httpx.AsyncClient) -> None:
    assert (await client.get("/api/cameras/999/passport")).status_code == 404
    camera_id = camera()
    with store.tx():
        processing = ready_video(camera_id, [])
        store.video_update(processing, {"status": "processing"})
    body = (await client.get(f"/api/cameras/{camera_id}/passport")).json()
    p = CameraPassport.model_validate(body)
    assert (p.analysis_id, p.frames, p.dark_share) == (None, 0, None)
    assert len(p.scenarios) == len(rules.PLUGINS)
    assert {(s.verdict, s.reason) for s in p.scenarios} == {("unknown", "Нет обработанного видео")}
    services.camera_delete(camera_id, "admin")
    assert (await client.get(f"/api/cameras/{camera_id}/passport")).status_code == 404


async def test_ready_video_passport(client: httpx.AsyncClient) -> None:
    camera_id = camera()
    video_id = ready_video(camera_id, [])
    _hud(video_id, frames(60))
    p = CameraPassport.model_validate(
        (await client.get(f"/api/cameras/{camera_id}/passport")).json()
    )
    assert p.analysis_id is not None and (p.frames, p.person_height_px_p50) == (60, 80)
    got = verdicts(p)
    assert got["running"] == ("suitable", "Годна")
    assert got["fence_crossing"] == ("partial", "Нет зон: Ограждение")
    assert got["no_helmet"] == ("unknown", "Модель не подключена")  # no helmet model by default
