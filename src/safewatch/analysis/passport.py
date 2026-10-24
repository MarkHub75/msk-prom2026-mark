"""Camera suitability passport (tech.md 8.28): pure functions over the HUD of one analysis."""

import statistics

from safewatch import config, texts
from safewatch.config import PassportConfig
from safewatch.types import (
    CameraPassport,
    HudFrame,
    ObservabilityGap,
    PassportScenario,
    PassportVerdict,
    ScenarioMeta,
    Zone,
)

# Without a zone of its kind these scenarios never fire; `fall` and the rest work without one.
ZONE_REQUIRED = ("fence_crossing", "restricted_under", "no_harness", "no_helmet", "no_respirator")
PHONE = "phone"


def _median(values: list[float]) -> float | None:
    # One decimal: normalized boxes give 79.99999 for an 80 px person.
    return round(statistics.median(values), 1) if values else None


def _pct(share: float) -> int:
    return round(share * 100)


def _verdict(
    meta: ScenarioMeta,
    p: CameraPassport,
    kinds: set[str],
    cfg: PassportConfig,
    min_person_px: int,
    phone_min_person_px: float,
) -> tuple[PassportVerdict, str]:
    """The first matching row of the order in tech.md 8.28."""
    if meta.status != "active":
        missing = meta.status == "model_missing"
        return "unknown", texts.PASSPORT_MODEL_MISSING if missing else meta.status_text
    if p.frames < cfg.min_frames:
        return "unknown", texts.PASSPORT_FEW_FRAMES
    dark = p.dark_share or 0.0
    if dark > cfg.dark_unsuitable:
        return "unsuitable", texts.PASSPORT_DARK.format(pct=_pct(dark))
    people = "person" in meta.required_classes
    height = p.person_height_px_p50
    if people and height is None:
        return "unknown", texts.PASSPORT_NO_PEOPLE
    if people and height is not None and height < min_person_px:
        return "unsuitable", texts.PASSPORT_PEOPLE_TINY.format(px=int(height))
    if meta.id == PHONE and height is not None:
        small = p.small_object_px_p50
        if height < phone_min_person_px:
            return "partial", texts.PASSPORT_PHONE_POOR.format(px=int(height))
        if small is not None and small < cfg.small_object_px:
            return "partial", texts.PASSPORT_PHONE_POOR.format(px=int(small))
    if meta.id in ZONE_REQUIRED and not kinds & set(meta.zone_kinds):
        titles = {k.id: k.title for k in config.get_settings().zone_kinds}
        names = ", ".join(titles[k] for k in meta.zone_kinds)
        return "partial", texts.PASSPORT_NO_ZONES.format(kinds=names)
    reasons = []
    if people and height is not None and height < cfg.person_partial_px:
        reasons.append(texts.PASSPORT_PEOPLE_SMALL.format(px=int(height)))
    if dark > cfg.dark_partial:
        reasons.append(texts.PASSPORT_DARK_PARTIAL.format(pct=_pct(dark)))
    empty = p.empty_share or 0.0
    if empty > cfg.empty_partial:
        reasons.append(texts.PASSPORT_EMPTY.format(pct=_pct(empty)))
    if reasons:
        return "partial", "; ".join(reasons)
    return "suitable", texts.PASSPORT_SUITABLE


def build_passport(
    camera_id: int,
    analysis_id: int | None,
    hud: list[HudFrame],
    gaps: list[ObservabilityGap],
    duration_ms: int,
    width: int,
    height: int,
    metas: list[ScenarioMeta],
    zones: list[Zone],
    cfg: PassportConfig,
    min_person_px: int,
    phone_min_person_px: float,
) -> CameraPassport:
    """`hud`: frames of the analysis, boxes normalized to `width` × `height` of the video."""
    frames = len(hud)
    objects = [o for frame in hud for o in frame.objects]
    persons = [(o.bbox[3] - o.bbox[1]) * height for o in objects if o.kind == "person"]
    phones = [
        max((o.bbox[2] - o.bbox[0]) * width, (o.bbox[3] - o.bbox[1]) * height)
        for o in objects
        if o.kind == "phone"
    ]
    with_people = sum(any(o.kind == "person" for o in frame.objects) for frame in hud)
    empty = sum(not frame.objects for frame in hud)
    dark_ms = sum(
        max(0, min(g.end_ms, duration_ms) - max(g.start_ms, 0))
        for g in gaps
        if g.reason in ("dark", "obstructed")
    )
    passport = CameraPassport(
        camera_id=camera_id,
        analysis_id=analysis_id,
        frames=frames,
        person_height_px_p50=_median(persons),
        small_object_px_p50=_median(phones),
        person_frames_share=with_people / frames if frames else None,
        dark_share=dark_ms / duration_ms if duration_ms > 0 else None,
        empty_share=empty / frames if frames else None,
        scenarios=[],
    )
    kinds = {z.kind for z in zones}
    for meta in metas:
        if analysis_id is None:
            verdict: PassportVerdict = "unknown"
            reason = texts.PASSPORT_NO_VIDEO
        else:
            verdict, reason = _verdict(
                meta, passport, kinds, cfg, min_person_px, phone_min_person_px
            )
        passport.scenarios.append(
            PassportScenario(scenario=meta.id, title=meta.title, verdict=verdict, reason=reason)
        )
    return passport
