"""Slice 11: blind intervals in the camera state (tech.md 8.9 rule 4) and `freshness_ms`."""

import json
from typing import Any

import pytest
from conftest import FakeClock
from test_broadcast import at, camera, hud_file, playing, started
from test_operator_views import SETUPS

from safewatch import services, store, texts
from safewatch.config import Settings
from safewatch.types import BroadcastIn

GAPS = [
    {"start_ms": 1000, "end_ms": 3001, "reason": "stale"},
    {"start_ms": 5000, "end_ms": 8000, "reason": "dark"},
    {"start_ms": 10_000, "end_ms": 13_000, "reason": "obstructed"},
    {"start_ms": 10_000, "end_ms": 14_000, "reason": "dark"},  # overlap: the first one wins
]


def _at_position(pos: int, *setup: str) -> tuple[str, str | None, str]:
    """State of a camera that plays an analysis with GAPS, at broadcast position `pos`."""
    camera_id = camera()
    for name in setup:
        SETUPS[name](camera_id)
    SETUPS["playing"](camera_id)
    store.run("UPDATE analyses SET gaps_json = ?", json.dumps(GAPS))
    store.run("UPDATE broadcasts SET position_ms = ? WHERE status = 'playing'", pos)
    (found,) = services.camera_states()
    return found.state, found.reason, found.reason_text


@pytest.mark.parametrize(
    ("pos", "setup", "state", "reason"),
    [
        (999, [], "normal", None),
        (1000, [], "no_observation", "stale"),
        (3000, [], "no_observation", "stale"),
        (3001, [], "normal", None),
        (4999, [], "normal", None),
        (5000, [], "no_observation", "dark"),
        (7999, [], "no_observation", "dark"),
        (8000, [], "normal", None),
        (10_000, [], "no_observation", "obstructed"),
        (13_500, [], "no_observation", "dark"),
        (14_000, [], "normal", None),
        # Rules 1–2 come before the gaps; a closed or ended event does not.
        (5000, ["red"], "red", None),
        (5000, ["yellow"], "yellow", None),
        (5000, ["yellow_ended", "red_closed"], "no_observation", "dark"),
    ],
)
def test_all_no_observation_reasons(
    core: Settings, pos: int, setup: list[str], state: str, reason: str | None
) -> None:
    titles = {"red": texts.LEVEL_TITLES["red"], "yellow": texts.LEVEL_TITLES["yellow"]}
    text = texts.NO_OBSERVATION_TEXTS[reason] if reason else titles.get(state, texts.STATE_NORMAL)  # type: ignore[index]
    assert _at_position(pos, *setup) == (state, reason, text)


def test_gaps_only_while_playing(core: Settings) -> None:
    """Rule 3 wins over the gaps: a stopped broadcast is `no_source`, an ended one `ended`."""
    camera_id = camera()
    SETUPS["stopped"](camera_id)
    store.run("UPDATE analyses SET gaps_json = ?", json.dumps(GAPS))
    store.run("UPDATE broadcasts SET position_ms = 5000")
    (found,) = services.camera_states()
    assert (found.state, found.reason, found.freshness_ms) == ("no_observation", "no_source", None)


def test_freshness_ms(core: Settings, fake_clock: FakeClock) -> None:
    b = playing([], duration_ms=10_000)
    store.run("UPDATE analyses SET hud_path = ?", hud_file("fresh", [200, 300, 400, 2900]))
    t0 = started(b)
    seen: list[Any] = []
    for ms in (100, 250, 300, 2899, 2900, 5000):
        at(fake_clock, t0, ms)
        services.broadcast_tick()
        seen.append(services.system_view().cameras[0].freshness_ms)
    # Before the first analyzed frame there is none to be fresh from.
    assert seen == [None, 50, 0, 2499, 0, 2100]
    services.broadcast_stop(services.camera_states()[0].camera_id, "admin")
    assert services.camera_states()[0].freshness_ms is None
    services.broadcast_start(services.camera_states()[0].camera_id, BroadcastIn(), "admin")
    assert services.camera_states()[0].freshness_ms is None  # position 0 < the first frame
