"""Blind intervals of a video (tech.md 8.10): no fresh frames, too dark, covered or blurred."""

from collections.abc import Callable

from safewatch.config import ObservabilityConfig
from safewatch.types import NoObservationReason, ObservabilityGap

Luma = tuple[int, float, float]  # (ts_ms, mean, std) of a grey, downscaled frame


def find_gaps(
    frames_ts: list[int],
    luma: list[Luma],
    duration_ms: int,
    params: ObservabilityConfig,
) -> list[ObservabilityGap]:
    """Intervals `[start_ms, end_ms)` by start; a stale one spans the two frames around it."""
    gaps = [
        ObservabilityGap(start_ms=a, end_ms=b, reason="stale")
        for a, b in zip(frames_ts, frames_ts[1:], strict=False)
        if b - a > params.stale_after_ms
    ]
    gaps += _runs(luma, duration_ms, params, "dark", lambda mean, _: mean < params.dark_mean)
    gaps += _runs(
        luma, duration_ms, params, "obstructed", lambda _, std: std < params.obstructed_std
    )
    order: list[NoObservationReason] = ["stale", "dark", "obstructed"]
    return sorted(gaps, key=lambda g: (g.start_ms, order.index(g.reason)))


def _runs(
    luma: list[Luma],
    duration_ms: int,
    params: ObservabilityConfig,
    reason: NoObservationReason,
    bad: Callable[[float, float], bool],
) -> list[ObservabilityGap]:
    """Runs of bad samples; a run lasts until the next good sample or the end of the video."""
    out = []
    start: int | None = None
    for ts, mean, std in [*luma, (duration_ms, 255.0, 255.0)]:
        if bad(mean, std) and ts < duration_ms:
            start = ts if start is None else start
            continue
        if start is not None and ts - start >= params.min_duration_s * 1000:
            out.append(ObservabilityGap(start_ms=start, end_ms=ts, reason=reason))
        start = None
    return out
