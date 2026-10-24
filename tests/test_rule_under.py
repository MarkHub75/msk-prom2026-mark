"""Slice 10: the `restricted_under` plugin (tech.md 8.3) through the episode manager."""

from test_rule_running import context, person, zone

from safewatch import rules
from safewatch.analysis.episodes import EpisodeManager
from safewatch.config import get_settings
from safewatch.rules.under import UnderPlugin
from safewatch.types import EpisodeDraft


def inside(until_ms: int, **params: float) -> list[EpisodeDraft]:
    zones = [zone("under_load", name="Под конвейером")]
    manager = EpisodeManager(get_settings().episodes)
    values = rules.defaults("restricted_under") | params
    for i, ts in enumerate(range(0, until_ms + 1, 10)):
        manager.update(i, ts, UnderPlugin().observe(context(person(), zones=zones), values))
    out = person(anchor=(100.0, 100.0))
    manager.update(1000, until_ms + 10, UnderPlugin().observe(context(out, zones=zones), values))
    return manager.finish(until_ms + 100)


def test_under_zone_red_after_hold() -> None:
    assert inside(490) == []
    (ep,) = inside(500)
    assert (ep.level_initial, ep.reason_text, ep.zone_id) == (
        "red",
        "Человек в зоне «Под конвейером»",
        7,
    )
    assert inside(500, under_hold_s=0.6) == []
    (o,) = UnderPlugin().observe(context(person()), rules.defaults("restricted_under"))
    assert o.state == "N"  # no zone: outside
    other = [zone("danger")]
    (o,) = UnderPlugin().observe(context(person(), zones=other), rules.defaults("restricted_under"))
    assert o.state == "N"
