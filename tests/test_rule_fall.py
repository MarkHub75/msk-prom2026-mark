"""Slice 5: the `fall` plugin (tech.md 8.3) through the episode manager."""

from test_rule_running import context, person, zone

from safewatch import rules
from safewatch.analysis.episodes import EpisodeManager
from safewatch.config import get_settings
from safewatch.rules.fall import FallPlugin
from safewatch.types import Observation, PersonState

LYING = {"posture": "lying", "bbox": (450.0, 265.0, 550.0, 300.0), "height_px": 35.0}


def lying(**update: object) -> PersonState:
    return person(**LYING).model_copy(update=update)


def one(p: PersonState, ts_ms: int, zones=None, **params: float) -> Observation:
    ctx = context(p, zones=zones, ts_ms=ts_ms)
    (o,) = FallPlugin().observe(ctx, rules.defaults("fall") | params)
    return o


def test_fall_transition_red() -> None:
    # Upright until 1.0 s, lying from 1.5 s: a 0.5 s transition is a fall.
    fell = lying(last_upright_ms=1000, lying_since_ms=1500, still_since_ms=1500)
    o = one(fell, 1500)
    assert (o.state, o.level, o.hold_s, o.reason_text) == ("P", "red", 2.0, "Зафиксировано падение")
    manager = EpisodeManager(get_settings().episodes)
    for i, ts in enumerate(range(1500, 4000, 100)):
        manager.update(i, ts, [one(fell, ts)])
    (ep,) = manager.finish(4000)
    assert (ep.confirm_ms, ep.level_initial, ep.reason_code) == (3500, "red", "fall")
    assert (
        one(lying(last_upright_ms=1000, lying_since_ms=3000, still_since_ms=3000), 3000).state
        == "P"
    )
    slow = lying(last_upright_ms=1000, lying_since_ms=3100, still_since_ms=3100)
    assert one(slow, 3100).state == "N"  # 2.1 s: no fall seen, not still for long either
    assert one(slow, 3100, transition_s=2.1).state == "P"
    assert one(fell, 1500, confirm_s=3.0).hold_s == 3.0
    assert one(person(), 1500).state == "N"
    assert one(person(posture="unknown"), 1500).state == "U"
    assert one(fell.model_copy(update={"ref_height_px": 39.0}), 1500).state == "U"
    assert one(fell.model_copy(update={"ref_height_px": 40.0}), 1500).state == "P"


def test_lying_still_without_transition() -> None:
    since_start = lying(last_upright_ms=None, lying_since_ms=0, still_since_ms=0)
    assert one(since_start, 9900).state == "N"
    o = one(since_start, 10_000)
    assert (o.state, o.level, o.hold_s) == ("P", "red", 0.0)
    assert o.reason_text == "Человек лежит неподвижно 10 с"
    assert one(since_start, 10_000, still_s=10.1).state == "N"
    moving = lying(last_upright_ms=None, lying_since_ms=0, still_since_ms=5000)
    assert one(moving, 10_000).state == "N"


def test_lying_allowed_zone_threshold() -> None:
    repair = [zone("lying_allowed", name="Ремонт", zone_id=3)]
    fell = lying(last_upright_ms=0, lying_since_ms=500, still_since_ms=0)
    assert one(fell, 59_900, zones=repair).state == "N"  # a fall in the zone is no alarm
    o = one(fell, 60_000, zones=repair)
    assert (o.state, o.level, o.zone_id) == ("P", "red", 3)
    assert o.reason_text == "Человек лежит неподвижно 60 с в зоне ремонта"
    assert one(fell, 60_000, zones=repair, allowed_still_s=61.0).state == "N"
    assert one(fell, 500, zones=[zone("danger")]).state == "P"  # other kinds do not allow it
