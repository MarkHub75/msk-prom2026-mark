"""Autocalibration by the height of standing people (tech.md 8.21): pure functions."""

import math

from safewatch import texts
from safewatch.config import AutocalConfig
from safewatch.types import AutoCalibration, FrameDetections

Sample = tuple[float, float]  # (foot y2, bbox height) in pixels


def _line(samples: list[Sample]) -> tuple[float, float] | None:
    """Least squares h = a + b·y; None when the feet do not spread over the rows."""
    n = len(samples)
    if n < 2:
        return None
    my = sum(y for y, _ in samples) / n
    mh = sum(h for _, h in samples) / n
    syy = sum((y - my) ** 2 for y, _ in samples)
    if syy == 0:
        return None
    b = sum((y - my) * (h - mh) for y, h in samples) / syy
    return mh - b * my, b


def fit(
    frames: list[FrameDetections],
    person_cls: set[int],
    width: int,
    height: int,
    cfg: AutocalConfig,
    upright_hw: float,
    high_thresh: float,
) -> AutoCalibration:
    samples: list[Sample] = []
    for frame in frames:
        for d in frame.detections:
            x1, y1, x2, y2 = d.bbox_xyxy
            w, h = x2 - x1, y2 - y1
            if d.cls not in person_cls or d.score < high_thresh or w <= 0 or h / w < upright_hw:
                continue
            if h < cfg.min_person_px or min(x1, y1, width - x2, height - y2) <= cfg.edge_px:
                continue
            samples.append((y2, h))
    line = _line(samples)
    for _ in range(cfg.iterations):
        if line is None:
            break
        a, b = line
        kept = [
            (y, h) for y, h in samples if abs(h - (a + b * y)) <= cfg.max_residual * (a + b * y)
        ]
        samples, line = kept, _line(kept)
    a, b = line or (0.0, 0.0)
    rmse = r2 = 0.0
    if line is not None:
        residuals = sum((h - (a + b * y)) ** 2 for y, h in samples)
        mh = sum(h for _, h in samples) / len(samples)
        spread = sum((h - mh) ** 2 for _, h in samples)
        rmse = math.sqrt(residuals / len(samples))
        r2 = 1 - residuals / spread if spread > 0 else 1.0
    reason = ""
    if len(samples) < cfg.min_samples:
        reason = texts.AUTOCAL_FEW.format(n=len(samples), need=cfg.min_samples)
    elif line is None or min(a, a + b * height) <= 0:
        reason = texts.AUTOCAL_PERSPECTIVE
    return AutoCalibration(
        ok=reason == "",
        reason=reason,
        samples=len(samples),
        a_px=a,
        b=b,
        rmse_px=rmse,
        r2=r2,
        person_height_m=cfg.person_height_m,
    )


def scale_at(cal: AutoCalibration, foot_y_px: float) -> float | None:
    """Meters per pixel on the floor row `foot_y_px`; None if not ok or height <= 0."""
    expected = cal.a_px + cal.b * foot_y_px
    if not cal.ok or expected <= 0:
        return None
    return cal.person_height_m / expected
