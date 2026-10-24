"""Slice 10: the `phone` plugin (tech.md 8.3) and `rules.base.attach_objects`."""

from test_rule_running import context, person, zone

from safewatch import rules
from safewatch.analysis.episodes import EpisodeManager
from safewatch.config import get_settings
from safewatch.rules.phone import PhonePlugin
from safewatch.types import EpisodeDraft, FrameContext, ObjectState, Observation, PersonState

TALL = {"bbox": (450.0, 100.0, 550.0, 300.0), "height_px": 200.0, "ref_height_px": 200.0}


def worker(**update: object) -> PersonState:
    return person(**TALL).model_copy(update=update)


def phone(cx: float, cy: float) -> ObjectState:
    return ObjectState(name="cell phone", bbox=(cx - 5, cy - 5, cx + 5, cy + 5), score=0.7)


def ctx_with(
    people: list[PersonState], objects: list[ObjectState], zones=None, ts_ms: int = 0
) -> FrameContext:
    ctx = context(people[0], zones=zones, ts_ms=ts_ms)
    return ctx.model_copy(update={"persons": people, "objects": objects})


def observe(ctx: FrameContext, **params: float) -> list[Observation]:
    return PhonePlugin().observe(ctx, rules.defaults("phone") | params)


def held(until_ms: int, zones=None) -> list[EpisodeDraft]:
    manager = EpisodeManager(get_settings().episodes)
    for i, ts in enumerate(range(0, until_ms + 1, 10)):
        manager.update(i, ts, observe(ctx_with([worker()], [phone(500, 150)], zones, ts)))
    manager.update(10_000, until_ms + 10, observe(ctx_with([worker()], [], zones)))
    return manager.finish(until_ms + 100)


def test_phone_hold_boundary() -> None:
    assert held(9990) == []
    (ep,) = held(10_000)
    assert (ep.level_initial, ep.reason_text, ep.reason_code) == (
        "yellow",
        "Телефон в руке 10 с",
        "phone",
    )
    danger = [zone("danger")]
    assert held(2990, danger) == []
    (red,) = held(3000, danger)
    assert (red.level_initial, red.zone_id, red.reason_code) == ("red", 7, "phone_zone")
    (o,) = observe(ctx_with([worker()], [phone(500, 150)]), hold_s=5.0)
    assert (o.state, o.hold_s) == ("P", 5.0)
    (o,) = observe(ctx_with([worker()], [phone(500, 150)], danger), danger_hold_s=4.0)
    assert (o.level, o.hold_s) == ("red", 4.0)


def test_phone_binding_upper_part_and_wrist() -> None:
    # upper_frac 0.6 of the 200 px bbox from y=100: the phone center up to y=220 is held.
    assert observe(ctx_with([worker()], [phone(500, 220)]))[0].state == "P"
    assert observe(ctx_with([worker()], [phone(500, 221)]))[0].state == "N"
    assert observe(ctx_with([worker()], [phone(500, 221)]), upper_frac=0.7)[0].state == "P"
    assert observe(ctx_with([worker()], [phone(560, 150)]))[0].state == "N"  # beside the bbox
    # A wrist (keypoint 10) at (600, 250): closer than 0.25 × 200 = 50 px holds the phone.
    kpts = [(0.0, 0.0, 0.0)] * 17
    kpts[10] = (600.0, 250.0, 0.9)
    hand = worker(kpts=kpts)
    assert observe(ctx_with([hand], [phone(649, 250)]))[0].state == "P"
    assert observe(ctx_with([hand], [phone(650, 250)]))[0].state == "N"
    assert observe(ctx_with([hand], [phone(650, 250)]), wrist_dist_bh=0.3)[0].state == "P"
    kpts[10] = (600.0, 250.0, 0.29)  # below pose.kpt_conf: the wrist is not visible
    assert observe(ctx_with([worker(kpts=kpts)], [phone(649, 250)]))[0].state == "N"


def test_small_person_unknown() -> None:
    small = worker(height_px=119.0)
    (o,) = observe(ctx_with([small], [phone(500, 150)]))
    assert (o.state, o.reason_code) == ("U", "too_small")
    assert observe(ctx_with([worker(height_px=120.0)], []))[0].state == "N"
    assert observe(ctx_with([worker(height_px=120.0)], []), min_person_px=121)[0].state == "U"
    # One phone between two people: neither owns it.
    left = worker(bbox=(450.0, 100.0, 550.0, 300.0))
    right = worker(track_id=2, bbox=(540.0, 100.0, 640.0, 300.0))
    both = observe(ctx_with([left, right], [phone(545, 150)]))
    assert [(o.subject, o.state, o.reason_code) for o in both] == [
        ("track:1", "U", "owner_ambiguous"),
        ("track:2", "U", "owner_ambiguous"),
    ]
    one = observe(ctx_with([left, right], [phone(500, 150)]))
    assert [o.state for o in one] == ["P", "N"]
