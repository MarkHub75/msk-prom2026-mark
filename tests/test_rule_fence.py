"""Slice 10: the `fence_crossing` plugin (tech.md 8.3) through the episode manager."""

from test_rule_running import context, person

from safewatch import rules
from safewatch.analysis.episodes import EpisodeManager
from safewatch.config import get_settings
from safewatch.rules.fence import FencePlugin
from safewatch.types import EpisodeDraft, Observation, Point, Zone

# A vertical fence at x = 500 px from y = 100 to y = 400 px (frame 1000 × 500).
FENCE = Zone(
    id=4, camera_id=1, kind="fence", name="Забор у пресса", points=[(0.5, 0.2), (0.5, 0.8)]
)


def step(prev: Point | None, now: Point, gap_ms: int = 100, **params: float) -> Observation:
    p = person(anchor=now, prev_anchor=prev, prev_ts_ms=None if prev is None else 5000 - gap_ms)
    (o,) = FencePlugin().observe(
        context(p, zones=[FENCE], ts_ms=5000), rules.defaults("fence_crossing") | params
    )
    return o


def walk(xs: list[float], y: float = 300.0) -> list[EpisodeDraft]:
    """A track walking along `xs` (one point per 100 ms), seen from its first point."""
    manager = EpisodeManager(get_settings().episodes)
    prev: Point | None = None
    for i, x in enumerate(xs):
        p = person(
            anchor=(x, y), prev_anchor=prev, prev_ts_ms=None if prev is None else i * 100 - 100
        )
        ctx = context(p, zones=[FENCE], ts_ms=i * 100)
        manager.update(i, i * 100, FencePlugin().observe(ctx, rules.defaults("fence_crossing")))
        prev = (x, y)
    return manager.finish(len(xs) * 100 + 5000)


def test_crossing_detected_once() -> None:
    (ep,) = walk([400.0 + 20 * i for i in range(11)])  # 400 → 600 px, crosses at 500
    assert (ep.level_initial, ep.reason_text, ep.zone_id) == (
        "red",
        "Пересечение ограждения «Забор у пресса»",
        4,
    )
    o = step((490.0, 300.0), (510.0, 300.0))
    assert (o.state, o.hold_s, o.reason_code) == ("P", 0.0, "fence_crossing")
    assert step((510.0, 300.0), (490.0, 300.0)).state == "P"  # either direction
    assert step((480.0, 300.0), (495.0, 300.0)).state == "N"
    # A crossing of the line below the segment end (y = 400 px) is no crossing of the fence.
    assert step((490.0, 450.0), (510.0, 450.0)).state == "N"
    assert walk([400.0 + 20 * i for i in range(11)], y=450.0) == []


def test_crossing_over_gap_unseen() -> None:
    blind = step((490.0, 300.0), (510.0, 300.0), gap_ms=1100)
    assert (blind.state, blind.reason_code) == ("P", "fence_unseen")
    assert blind.reason_text == "Пересечение ограждения «Забор у пресса»: момент не виден"
    seen = step((490.0, 300.0), (510.0, 300.0), gap_ms=1000)
    assert (seen.state, seen.reason_code) == ("P", "fence_crossing")
    assert (
        step((490.0, 300.0), (510.0, 300.0), gap_ms=1100, max_gap_s=1.2).reason_code
        == "fence_crossing"
    )


def test_appearing_inside_is_not_crossing() -> None:
    assert step(None, (510.0, 300.0)).state == "U"
    assert walk([520.0 + 20 * i for i in range(10)]) == []
