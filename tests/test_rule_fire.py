"""Slice 10: the `fire_smoking` plugin (tech.md 8.3)."""

from test_rule_phone import ctx_with, worker
from test_rule_running import zone

from safewatch import rules
from safewatch.analysis.episodes import EpisodeManager
from safewatch.config import get_settings
from safewatch.rules.fire import FirePlugin
from safewatch.types import FrameContext, ObjectState, Observation


def flame(name: str, cx: float, cy: float) -> ObjectState:
    return ObjectState(name=name, bbox=(cx - 10, cy - 10, cx + 10, cy + 10), score=0.8)


def observe(ctx: FrameContext, **params: float) -> list[Observation]:
    return FirePlugin().observe(ctx, rules.defaults("fire_smoking") | params)


def fire(objects: list[ObjectState], zones=None, **params: float) -> Observation:
    o = observe(ctx_with([worker()], objects, zones), **params)[0]
    assert o.subject == "fire"
    return o


def test_fire_outside_allowed_zone_red() -> None:
    furnace = [zone("fire_allowed", name="Печь")]  # holds (500, 300) px
    o = fire([flame("fire", 500, 300)])
    assert (o.state, o.level, o.hold_s, o.reason_text) == (
        "P",
        "red",
        1.0,
        "Открытый огонь вне разрешённой зоны",
    )
    assert fire([flame("smoke", 500, 300)]).state == "P"
    assert fire([flame("fire", 500, 300)], furnace).state == "N"
    assert fire([flame("fire", 500, 300), flame("fire", 100, 50)], furnace).state == "P"
    assert fire([]).state == "N"
    assert fire([flame("fire", 500, 300)], fire_hold_s=2.0).hold_s == 2.0

    manager = EpisodeManager(get_settings().episodes)
    for i, ts in enumerate(range(0, 1001, 100)):
        manager.update(i, ts, observe(ctx_with([worker()], [flame("fire", 500, 300)], ts_ms=ts)))
    (ep,) = manager.finish(2000)
    assert (ep.subject, ep.level_initial, ep.confirm_ms) == ("fire", "red", 1000)


def test_smoking_yellow_red_in_danger() -> None:
    cigarette = flame("cigarette", 500, 150)
    o = observe(ctx_with([worker()], [cigarette]))[1]
    assert (o.subject, o.state, o.level, o.hold_s, o.reason_text) == (
        "track:1",
        "P",
        "yellow",
        3.0,
        "Курение",
    )
    red = observe(ctx_with([worker()], [cigarette], [zone("danger")]), smoking_hold_s=4.0)[1]
    assert (red.level, red.hold_s, red.reason_text) == ("red", 4.0, "Курение в зоне «Пресс»")
    assert observe(ctx_with([worker()], []))[1].state == "N"
    left = worker()
    right = worker(track_id=2, bbox=(540.0, 100.0, 640.0, 300.0))
    shared = observe(ctx_with([left, right], [flame("cigarette", 545, 150)]))
    assert [(o.state, o.reason_code) for o in shared[1:]] == [("U", "owner_ambiguous")] * 2
