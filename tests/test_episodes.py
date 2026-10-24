"""Slice 5: the episode manager of tech.md 8.4 (every row of its table)."""

from safewatch.analysis.episodes import EpisodeManager
from safewatch.config import EpisodesConfig, get_settings
from safewatch.types import EpisodeDraft, Level, Observation, ObsState, Point


def _o(
    state: ObsState,
    subject: str = "track:1",
    level: Level = "yellow",
    hold_s: float = 1.0,
    anchor: Point = (100.0, 200.0),
    text: str = "Бег",
) -> Observation:
    return Observation(
        scenario="running", subject=subject, state=state, level=level, hold_s=hold_s,
        reason_code="running", reason_text=text, method="relative", confidence=0.8,
        metrics={"speed_bh_s": 2.0}, zone_id=None, anchor=anchor, ref_height_px=100.0,
    )  # fmt: skip


def _cfg(**update: float) -> EpisodesConfig:
    return get_settings().episodes.model_copy(update=update)


def _feed(m: EpisodeManager, frames: list[tuple[int, list[Observation]]]) -> None:
    for i, (ts, obs) in enumerate(frames):
        m.update(i, ts, obs)


def _run(
    frames: list[tuple[int, list[Observation]]], end_ms: int = 60_000, **cfg: float
) -> list[EpisodeDraft]:
    m = EpisodeManager(_cfg(**cfg))
    _feed(m, frames)
    return m.finish(end_ms)


def _span(start: int, stop: int, step: int, obs: list[Observation]) -> list:
    """Frames every `step` ms in [start, stop] with the same observations."""
    return [(ts, obs) for ts in range(start, stop + 1, step)]


def test_confirm_after_hold() -> None:
    short = _span(0, 990, 10, [_o("P")]) + [(1000, [_o("N")])]
    assert _run(short) == []
    (ep,) = _run(_span(0, 1000, 10, [_o("P")]))
    assert (ep.start_ms, ep.confirm_ms, ep.confirm_frame_idx) == (0, 1000, 100)
    assert (ep.level_initial, ep.level_max, ep.reason_text) == ("yellow", "yellow", "Бег")
    (now,) = _run([(500, [_o("P", hold_s=0.0)])])  # hold 0: the first P confirms
    assert now.confirm_ms == now.start_ms == 500


def test_negative_resets_candidate() -> None:
    reset = _span(0, 500, 10, [_o("P")]) + [(510, [_o("N")])] + _span(520, 1600, 10, [_o("P")])
    (ep,) = _run(reset)
    assert (ep.start_ms, ep.confirm_ms) == (520, 1520)
    # A 0.5 s gap without observations keeps the candidate, 0.6 s drops it.
    for gap, start in [(500, 0), (600, 900)]:
        resume = 300 + gap
        frames = _span(0, 300, 10, [_o("P")]) + _span(310, resume - 10, 10, [])
        frames += _span(resume, resume + 1000, 10, [_o("P")])
        (ep,) = _run(frames)
        assert ep.start_ms == start, gap
    # U counts as no observation: a 0.6 s run of U drops the candidate as well.
    frames = _span(0, 300, 10, [_o("P")]) + _span(310, 890, 10, [_o("U")])
    assert _run(frames + _span(900, 1000, 10, [_o("P")])) == []
    # candidate_gap_s from the config changes the outcome of the same frames.
    assert _run(frames + _span(900, 1300, 10, [_o("P")]), candidate_gap_s=0.6)[0].start_ms == 0


def test_gap_tolerance_and_lost_timeout() -> None:
    confirmed = _span(0, 1000, 100, [_o("P")])
    alive = _run(confirmed + _span(1100, 6000, 100, []) + [(6100, [_o("P")])], end_ms=7000)
    assert [(e.end_reason, e.end_ms, e.uncertain_ms) for e in alive] == [("video_end", 7000, 5000)]
    lost = _run(confirmed + _span(1100, 6100, 100, [_o("U")]), end_ms=7000)
    assert [(e.end_reason, e.end_ms) for e in lost] == [("track_lost_timeout", 1000)]
    assert lost[0].uncertain_ms == 5100
    longer = _run(confirmed + _span(1100, 6100, 100, []), end_ms=7000, lost_timeout_s=5.1)
    assert longer[0].end_reason == "video_end"


def test_end_after_negatives_and_rearm() -> None:
    confirmed = _span(0, 1000, 100, [_o("P")])
    closed = _run(confirmed + _span(1100, 3100, 100, [_o("N")]))
    assert [(e.end_reason, e.end_ms) for e in closed] == [("observed_exit", 1100)]
    kept = _run(confirmed + _span(1100, 3000, 100, [_o("N")]) + [(3100, [_o("P")])], end_ms=9000)
    assert [(e.end_reason, e.end_ms) for e in kept] == [("video_end", 9000)]
    quick = _run(confirmed + _span(1100, 2100, 100, [_o("N")]), end_after_s=1.0)
    assert [(e.end_reason, e.end_ms) for e in quick] == [("observed_exit", 1100)]
    # After the close a new P starts a new candidate at once: no silence timer.
    again = _run(confirmed + _span(1100, 3100, 100, [_o("N")]) + _span(3200, 4200, 100, [_o("P")]))
    assert [(e.start_ms, e.confirm_ms) for e in again] == [(0, 1000), (3200, 4200)]


def test_escalation_keeps_same_episode() -> None:
    yellow = _span(0, 1000, 100, [_o("P", text="Телефон {duration_s} с")])
    red = [_o("P", level="red", hold_s=0.5, text="Телефон {duration_s} с у пресса")]
    (ep,) = _run(yellow + _span(1100, 2500, 100, red))
    assert (ep.level_initial, ep.level_max, ep.escalate_ms) == ("yellow", "red", 1600)
    assert ep.escalate_frame_idx == 16 and ep.reason_text == "Телефон 1 с у пресса"
    (short,) = _run(yellow + _span(1100, 1500, 100, red) + _span(1600, 2500, 100, [_o("P")]))
    assert (short.level_max, short.escalate_ms, short.reason_text) == (
        "yellow",
        None,
        "Телефон 1 с",
    )


def test_id_switch_merges_but_two_people_do_not() -> None:
    first = _span(0, 1000, 100, [_o("P")])
    for dx, count in [(90.0, 1), (100.0, 1), (110.0, 2)]:  # in H_ref = 100 px
        second = [_o("P", subject="track:2", anchor=(100.0 + dx, 200.0))]
        episodes = _run(first + _span(1100, 2500, 100, second))
        assert len(episodes) == count, dx
    both = [_o("P"), _o("P", subject="track:2", anchor=(150.0, 200.0))]
    assert len(_run(_span(0, 2500, 100, both))) == 2
    far = [_o("P", subject="track:2", anchor=(210.0, 200.0))]
    assert len(_run(first + _span(1100, 2500, 100, far), merge_dist_bh=1.1)) == 1


def test_video_end_closes_episode() -> None:
    frames = _span(0, 4900, 100, [_o("P")]) + [(5000, [_o("P"), _o("P", subject="track:2")])]
    (ep,) = _run(frames, end_ms=5000)  # the unconfirmed candidate of track 2 is no episode
    assert (ep.end_reason, ep.end_ms, ep.subject) == ("video_end", 5000, "track:1")
