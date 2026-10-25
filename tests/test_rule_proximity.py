"""Slice 10: the `proximity` plugin (tech.md 8.3) and the vehicle features (8.2 item 6)."""

import re

import pytest
from test_rule_running import PERSON, context, person, zone

from safewatch import rules
from safewatch.analysis import features
from safewatch.analysis.episodes import EpisodeManager
from safewatch.config import get_settings
from safewatch.rules.proximity import ProximityPlugin
from safewatch.types import (
    Detection,
    EpisodeDraft,
    FrameContext,
    Observation,
    PersonState,
    VehicleState,
)


def truck(
    distance_bh: float = 1.0,
    vh_s: float | None = 1.0,
    m_s: float | None = None,
    footprint=None,
    x1: float | None = None,
) -> VehicleState:
    """A truck whose left edge is `distance_bh` heights (100 px) right of the foot at x=500."""
    left = 500.0 + 100.0 * distance_bh if x1 is None else x1
    return VehicleState(
        track_id=9, name="truck", bbox=(left, 100.0, left + 200.0, 300.0), score=0.9,
        footprint=footprint, height_px=200.0, speed_vh_s=vh_s, speed_m_s=m_s,
    )  # fmt: skip


def observe(ctx: FrameContext, **params: float) -> list[Observation]:
    return ProximityPlugin().observe(ctx, rules.defaults("proximity") | params)


def pair(v: VehicleState, p: PersonState | None = None, **params: float) -> Observation:
    (o,) = observe(context(p or person(), vehicles=[v]), **params)
    assert o.subject == f"pair:{(p or person()).track_id}-{v.track_id}"
    return o


@pytest.mark.parametrize(
    ("distance", "state", "level", "hold"),
    [
        (0.5, "P", "red", 0.3),
        (0.51, "P", "yellow", 0.5),
        (2.0, "P", "yellow", 0.5),
        (2.01, "N", "yellow", 0.0),
    ],
)
def test_moving_vehicle_distance_levels(
    distance: float, state: str, level: str, hold: float
) -> None:
    o = pair(truck(distance))
    assert (o.state, o.level, o.hold_s, o.method) == (state, level, hold, "relative")
    if state == "P":
        assert o.reason_text == f"Сближение с грузовиком: {distance:.1f} роста".replace(".", ",")
        assert o.metrics == {"distance_bh": pytest.approx(distance)}


def test_distance_thresholds_follow_params() -> None:
    assert pair(truck(2.01), yellow_bh=2.1).state == "P"
    assert pair(truck(0.5), red_bh=0.4).level == "yellow"
    assert pair(truck(1.0), hold_s=2.0).hold_s == 2.0
    assert pair(truck(0.5), red_hold_s=1.0).hold_s == 1.0


def test_calibrated_distance_in_metres() -> None:
    on_floor = person(ground=(0.0, 0.0))

    def at(m: float, **params: float) -> Observation:
        return pair(truck(5.0, m_s=1.0, footprint=((m, 0.0), (m + 2.0, 0.0))), on_floor, **params)

    red = at(1.0)
    assert (red.state, red.level, red.method) == ("P", "red", "calibrated")
    assert red.reason_text == "Сближение с грузовиком: 1,0 м" and red.metrics == {"distance_m": 1.0}
    assert (at(1.01).state, at(1.01).level) == ("P", "yellow")
    assert (at(3.0).state, at(3.0).level) == ("P", "yellow")
    assert at(3.01).state == "N"
    assert at(3.01, yellow_m=3.1).state == "P"
    assert at(1.01, red_m=1.1).level == "red"


def test_stationary_vehicle_negative() -> None:
    assert pair(truck(0.5, vh_s=0.19)).state == "N"
    assert pair(truck(0.5, vh_s=0.2)).state == "P"
    assert pair(truck(0.5, vh_s=0.1), moving_vh_s=0.1).state == "P"
    # Calibrated speed wins over the speed in heights.
    assert pair(truck(0.5, vh_s=5.0, m_s=0.49)).state == "N"
    assert pair(truck(0.5, vh_s=0.0, m_s=0.5)).state == "P"
    assert pair(truck(0.5, vh_s=0.0, m_s=0.4), moving_m_s=0.4).state == "P"
    assert pair(truck(0.5, vh_s=None)).state == "U"

    # vehicle_states: the bbox center over speed_window_s, in its own heights per second.
    cfg = get_settings().features
    history: features.VehicleHistory = {}
    still: features.VehicleHistory = {}
    on_floor = {}
    for i, ts in enumerate(range(0, 1001, 100)):
        box = (100.0 + 20 * i, 100.0, 300.0 + 20 * i, 300.0)  # 200 px/s, 200 px tall
        det = Detection(cls=7, name="truck", score=0.9, bbox_xyxy=box)
        (moving,) = features.vehicle_states([(9, det)], ts, history, cfg, lambda p: (p[0] / 100, 0))
        stopped = Detection(cls=7, name="truck", score=0.9, bbox_xyxy=(100.0, 100.0, 300.0, 300.0))
        (parked,) = features.vehicle_states([(8, stopped)], ts, still, cfg)
        on_floor[ts] = moving
    assert on_floor[200].speed_vh_s is None  # 3 samples < speed_min_samples
    assert on_floor[1000].speed_vh_s == pytest.approx(1.0)
    assert on_floor[1000].footprint == ((3.0, 0), (5.0, 0))
    assert on_floor[1000].speed_m_s == pytest.approx(2.0)
    assert (parked.speed_vh_s, parked.footprint, parked.speed_m_s) == (0.0, None, None)
    assert pair(parked.model_copy(update={"bbox": truck(0.5).bbox})).state == "N"


def test_driver_excluded() -> None:
    # The person bbox is 40 px wide (480..520): a truck from x=496 holds 0.6 of it.
    assert observe(context(person(), vehicles=[truck(x1=496.0)])) == []
    (o,) = observe(context(person(), vehicles=[truck(x1=496.4)]))
    assert (o.state, o.level) == ("P", "red")  # 0.59 of the bbox: not the driver
    assert observe(context(person(), vehicles=[truck(x1=496.4)]), driver_ioa=0.59) == []
    assert PERSON == (480.0, 200.0, 520.0, 300.0)


def test_danger_zone_entry_red() -> None:
    (o,) = observe(context(person(), zones=[zone("danger")]))
    assert (o.subject, o.state, o.level, o.hold_s, o.zone_id) == ("zone:1-7", "P", "red", 0.3, 7)
    assert o.reason_text == "Человек в зоне «Пресс»"
    away = person(anchor=(100.0, 100.0))
    assert [x.state for x in observe(context(away, zones=[zone("danger")]))] == ["N"]
    assert observe(context(person(), zones=[zone("vehicle_path")])) == []
    (slow,) = observe(context(person(), zones=[zone("danger")]), red_hold_s=1.0)
    assert slow.hold_s == 1.0


def test_vehicle_path_walk_alone_quiet_truck_still_red() -> None:
    """Stage 2, camera 1.3: walking along a forklift lane is no alarm; a moving truck near is."""
    lane = zone("vehicle_path")
    assert observe(context(person(), zones=[lane])) == []
    (o,) = observe(context(person(), vehicles=[truck(0.4)], zones=[lane]))
    assert (o.subject, o.state, o.level, o.reason_code) == ("pair:1-9", "P", "red", "proximity_red")
    stopped = truck(0.4, vh_s=0.0)
    assert [x.state for x in observe(context(person(), vehicles=[stopped], zones=[lane]))] == ["N"]


def test_two_people_two_episodes() -> None:
    first = person()
    second = person(track_id=2, foot=(500.0, 290.0), anchor=(500.0, 290.0))
    manager = EpisodeManager(get_settings().episodes)
    for i, ts in enumerate(range(0, 1001, 100)):
        ctx = context(first, vehicles=[truck(0.4)], ts_ms=ts)
        ctx = ctx.model_copy(update={"persons": [first, second]})
        manager.update(i, ts, observe(ctx))
    episodes = manager.finish(2000)
    assert sorted(e.subject for e in episodes) == ["pair:1-9", "pair:2-9"]
    assert {e.level_initial for e in episodes} == {"red"}


@pytest.mark.parametrize(
    ("scenario", "code", "reason", "method", "zone_id"),
    [
        ("proximity", "proximity_zone", "Человек в зоне «Пресс»", "bbox", 7),
        ("proximity", "proximity_red", "Сближение с грузовиком: 0,4 роста", "relative", None),
        ("proximity", "proximity_red", "Сближение с грузовиком: 1,0 м", "calibrated", None),
        ("phone", "phone_zone", "Телефон в руке", "bbox", 7),
        (
            "fence_crossing",
            "fence_unseen",
            "Пересечение ограждения «Л»: момент не виден",
            "bbox",
            7,
        ),
        ("restricted_under", "under_zone", "Человек в зоне «Кран»", "bbox", 7),
        ("fire_smoking", "fire", "Открытый огонь вне разрешённой зоны", "bbox", None),
        ("no_harness", "no_harness", "Работа на высоте без привязи", "bbox", None),
        ("suspended_load", "suspended_load", "Человек под подвешенным грузом", "bbox", None),
    ],
)
def test_explain_has_units(
    scenario: str, code: str, reason: str, method: str, zone_id: int | None
) -> None:
    """Debt S10: the rule line of every S10 plugin names its threshold with a unit."""
    draft = EpisodeDraft(
        scenario=scenario, subject="fire" if scenario == "fire_smoking" else "track:1",
        zone_id=zone_id, level_initial="red", level_max="red", start_ms=0, confirm_ms=1000,
        escalate_ms=None, end_ms=5000, end_reason="video_end", reason_code=code,
        reason_text=reason, method=method, confidence=0.9, metrics={"score": 0.8},
        uncertain_ms=0, confirm_frame_idx=10, escalate_frame_idx=None,
    )  # fmt: skip
    rule, *rest = rules.plugin(scenario).explain(draft, rules.defaults(scenario))
    assert rule.label == "Правило"
    assert reason in rule.value or code in ("proximity_red", "phone_zone")  # zone in the reason
    assert re.search(r"\d(,\d+)? (с|м|роста)", rule.value), rule.value
    assert ("Уверенность объекта", "0,8") in [(w.label, w.value) for w in rest]
