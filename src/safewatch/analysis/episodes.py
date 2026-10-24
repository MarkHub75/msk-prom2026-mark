"""Episode manager (tech.md 8.4): observations per frame → confirmed episodes.

State lives per (scenario, subject); time is `ts_ms` of the source frames. `U` and a missing
observation are the same thing here: no data about the subject in this frame.
"""

import math
from dataclasses import dataclass, field

from safewatch.config import EpisodesConfig
from safewatch.types import EndReason, EpisodeDraft, Level, Observation, Point

Key = tuple[str, str]  # (scenario, subject)


@dataclass
class _State:
    scenario: str
    subject: str
    start_ms: int
    last_p_ms: int
    last_seen_ms: int  # last P or N
    last_ts_ms: int  # last frame this state went through
    first: Observation
    confirmed: bool = False
    confirm_ms: int = 0
    confirm_frame_idx: int = 0
    level_initial: Level = "yellow"
    level_max: Level = "yellow"
    escalate_ms: int | None = None
    escalate_frame_idx: int | None = None
    red_since_ms: int | None = None  # start of the current run of red P on a yellow episode
    closing_since_ms: int | None = None  # first N of the current run of N
    uncertain_ms: int = 0
    confidence: float = 0.0
    metrics: dict[str, float] = field(default_factory=dict)
    reason: Observation | None = None  # the observation that confirmed or escalated
    anchor: Point | None = None
    ref_height_px: float | None = None


class EpisodeManager:
    def __init__(self, cfg: EpisodesConfig) -> None:
        self.cfg = cfg
        self._states: dict[Key, _State] = {}  # a merged track id points at the same state
        self._done: list[tuple[_State, int, EndReason]] = []

    def update(self, frame_idx: int, ts_ms: int, observations: list[Observation]) -> None:
        seen = {(o.scenario, o.subject): o for o in observations if o.state != "U"}
        touched: set[int] = set()
        for key, o in seen.items():
            state = self._states.get(key)
            if state is None:
                if o.state == "N":
                    continue
                state = self._merge_target(o, seen) or self._candidate(o, ts_ms)
                self._states[key] = state
            touched.add(id(state))
            self._observe(state, o, frame_idx, ts_ms)
        for state in {id(s): s for s in self._states.values()}.values():
            if id(state) not in touched:
                self._unseen(state, ts_ms)
            state.last_ts_ms = ts_ms
        self._states = {k: s for k, s in self._states.items() if not self._gone(s)}

    def finish(self, duration_ms: int) -> list[EpisodeDraft]:
        """Close what is still active at the end of the video; all episodes by start."""
        for state in {id(s): s for s in self._states.values()}.values():
            if state.confirmed:
                self._done.append((state, duration_ms, "video_end"))
        self._states = {}
        return [self._draft(*item) for item in sorted(self._done, key=lambda d: d[0].start_ms)]

    # --- transitions ------------------------------------------------------------------------
    def _candidate(self, o: Observation, ts_ms: int) -> _State:
        return _State(o.scenario, o.subject, ts_ms, ts_ms, ts_ms, ts_ms, first=o)

    def _merge_target(self, o: Observation, seen: dict[Key, Observation]) -> _State | None:
        """An active episode of the same scenario whose subject vanished near this one."""
        if o.anchor is None:
            return None
        best, best_d = None, math.inf
        for key, state in self._states.items():
            if key[0] != o.scenario or not state.confirmed or state.anchor is None:
                continue
            if any(k in seen for k, s in self._states.items() if s is state):
                continue  # the earlier subject is still in view: two people, two episodes
            d = math.dist(o.anchor, state.anchor)
            if d <= self.cfg.merge_dist_bh * (state.ref_height_px or 0.0) and d < best_d:
                best, best_d = state, d
        return best

    def _observe(self, s: _State, o: Observation, frame_idx: int, ts_ms: int) -> None:
        if not s.confirmed:
            if o.state == "N":
                s.closing_since_ms = ts_ms  # marks the candidate for removal
                return
            if ts_ms - s.last_p_ms > self.cfg.candidate_gap_s * 1000:
                s.start_ms = ts_ms  # the gap reset the candidate; this P starts a new one
            self._positive(s, o, ts_ms)
            if ts_ms - s.start_ms >= o.hold_s * 1000:
                s.confirmed, s.confirm_ms, s.confirm_frame_idx = True, ts_ms, frame_idx
                s.level_initial = s.level_max = o.level
                s.reason = o
            return
        s.last_seen_ms = ts_ms
        if o.state == "N":
            s.red_since_ms = None
            if s.closing_since_ms is None:
                s.closing_since_ms = ts_ms
            if ts_ms - s.closing_since_ms >= self.cfg.end_after_s * 1000:
                self._close(s, s.closing_since_ms, "observed_exit")
            return
        s.closing_since_ms = None
        self._positive(s, o, ts_ms)
        if o.level == "red" and s.level_max == "yellow":
            if s.red_since_ms is None:
                s.red_since_ms = ts_ms
            if ts_ms - s.red_since_ms >= o.hold_s * 1000:
                s.escalate_ms, s.escalate_frame_idx, s.level_max = ts_ms, frame_idx, "red"
                s.reason = o
        elif o.level != "red":
            s.red_since_ms = None

    def _positive(self, s: _State, o: Observation, ts_ms: int) -> None:
        s.last_p_ms = s.last_seen_ms = ts_ms
        s.confidence = max(s.confidence, o.confidence)
        for k, v in o.metrics.items():
            s.metrics[k] = max(s.metrics.get(k, v), v)
        s.anchor, s.ref_height_px = o.anchor, o.ref_height_px

    def _unseen(self, s: _State, ts_ms: int) -> None:
        if not s.confirmed:
            if ts_ms - s.last_p_ms > self.cfg.candidate_gap_s * 1000:
                s.closing_since_ms = ts_ms  # the candidate is dropped
            return
        s.red_since_ms = None
        s.uncertain_ms += ts_ms - s.last_ts_ms
        if ts_ms - s.last_seen_ms > self.cfg.lost_timeout_s * 1000:
            self._close(s, s.last_p_ms, "track_lost_timeout")

    def _close(self, s: _State, end_ms: int, reason: EndReason) -> None:
        self._done.append((s, end_ms, reason))
        s.confirmed = False
        s.closing_since_ms = end_ms

    def _gone(self, s: _State) -> bool:
        return not s.confirmed and s.closing_since_ms is not None

    # --- output -----------------------------------------------------------------------------
    def _draft(self, s: _State, end_ms: int, end_reason: EndReason) -> EpisodeDraft:
        o = s.reason or s.first
        moment = s.escalate_ms if s.escalate_ms is not None else s.confirm_ms
        text = o.reason_text.replace("{duration_s}", str((moment - s.start_ms) // 1000))
        return EpisodeDraft(
            scenario=s.scenario,
            subject=s.subject,
            zone_id=o.zone_id,
            level_initial=s.level_initial,
            level_max=s.level_max,
            start_ms=s.start_ms,
            confirm_ms=s.confirm_ms,
            escalate_ms=s.escalate_ms,
            end_ms=end_ms,
            end_reason=end_reason,
            reason_code=o.reason_code,
            reason_text=text,
            method=o.method,
            confidence=s.confidence,
            metrics=dict(s.metrics),
            uncertain_ms=s.uncertain_ms,
            confirm_frame_idx=s.confirm_frame_idx,
            escalate_frame_idx=s.escalate_frame_idx,
        )
