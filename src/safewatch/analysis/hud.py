"""HUD frames (tech.md 8.2 item 8): what the player draws over the video, in 0..1 coordinates."""

from safewatch import texts
from safewatch.config import FeaturesConfig
from safewatch.rules.fire import FLAMES
from safewatch.rules.suspended_load import ID as LOAD
from safewatch.types import (
    Box,
    FrameContext,
    HudFrame,
    HudObject,
    HudTag,
    Keypoint,
    ObjectState,
    Observation,
    PersonState,
    Point,
)


def _unit(v: float, size: int) -> float:
    return min(1.0, max(0.0, v / size))


def _box(box: Box, w: int, h: int) -> Box:
    return (_unit(box[0], w), _unit(box[1], h), _unit(box[2], w), _unit(box[3], h))


def _kpts(points: list[Keypoint] | None, w: int, h: int) -> list[Keypoint] | None:
    if points is None:
        return None
    return [(_unit(x, w), _unit(y, h), conf) for x, y, conf in points]


def _projection(o: ObjectState, w: int, h: int) -> list[Point] | None:
    """Column under a suspended load down to the frame bottom (8.23): the `suspended_load` area."""
    if o.name != LOAD:
        return None
    x1, _, x2, y2 = _box(o.bbox, w, h)
    return [(x1, y2), (x2, y2), (x2, 1.0), (x1, 1.0)]


def _object_tags(o: ObjectState, violations: dict[str, list[HudTag]]) -> list[HudTag]:
    if o.name in FLAMES:
        return violations.get("fire", [])
    if o.name == LOAD:
        return [HudTag(code="load_projection", text=texts.HUD_LOAD_PROJECTION, level=None)]
    return []


def _person_tags(
    p: PersonState, ts_ms: int, running: dict[str, float], cfg: FeaturesConfig
) -> list[HudTag]:
    tags = []
    # Meters from the calibrated floor or the autocalibration, as in the running rule (8.21).
    speed: float | None
    if p.speed_m_s is not None:
        auto = p.speed_source == "auto"
        speed, limit = p.speed_m_s, running["speed_m_s"]
        run_text = texts.HUD_RUN_M_AUTO if auto else texts.HUD_RUN_M
        speed_text = texts.HUD_SPEED_M_AUTO if auto else texts.HUD_SPEED_M
    else:
        speed, limit = p.speed_bh_s, running["speed_bh_s"]
        run_text, speed_text = texts.HUD_RUN_BH, texts.HUD_SPEED_BH
    if speed is not None:
        v = texts.fmt_num(speed)
        # Same comparison as the running rule: the HUD turns yellow where the rule would fire.
        if speed >= limit:
            tags.append(HudTag(code="speed", text=run_text.format(v=v), level="yellow"))
        else:
            tags.append(HudTag(code="speed", text=speed_text.format(v=v), level=None))
    if p.posture == "lying" and p.lying_since_ms is not None:
        n = (ts_ms - p.lying_since_ms) // 1000
        tags.append(HudTag(code="lying", text=texts.HUD_LYING.format(n=n), level=None))
    if p.still_since_ms is not None and ts_ms - p.still_since_ms > cfg.still_after_s * 1000:
        n = (ts_ms - p.still_since_ms) // 1000
        tags.append(HudTag(code="still", text=texts.HUD_STILL.format(n=n), level=None))
    if not p.feet_visible:
        tags.append(HudTag(code="feet_hidden", text=texts.HUD_FEET_HIDDEN, level=None))
    if p.height_px < cfg.min_person_px:
        tags.append(HudTag(code="too_small", text=texts.HUD_TOO_SMALL, level=None))
    return tags


def _keys(subject: str) -> list[str]:
    """HUD objects of an observation subject (8.2 item 8: a label on every `P`).

    `pair:<p>-<v>` labels person `p` and vehicle `v`, `zone:<p>-<z>` person `p`; `fire` labels
    every flame of the frame; `track:<id>` is the person itself.
    """
    kind, _, rest = subject.partition(":")
    if kind == "pair":
        person, vehicle = rest.split("-")
        return [f"track:{person}", f"vehicle:{vehicle}"]
    if kind == "zone":
        return [f"track:{rest.split('-')[0]}"]
    return [subject]


def build_hud(
    ctx: FrameContext,
    running: dict[str, float],
    cfg: FeaturesConfig,
    observations: list[Observation],
) -> HudFrame:
    """`running`: effective parameters of the camera's running rule (speed_bh_s, speed_m_s)."""
    w, h = ctx.width, ctx.height
    violations: dict[str, list[HudTag]] = {}  # HUD object key → one tag per positive observation
    for o in observations:
        if o.state == "P":
            tag = HudTag(code=o.scenario, text=o.reason_text, level=o.level)
            for key in _keys(o.subject):
                violations.setdefault(key, []).append(tag)
    objects = [
        HudObject(
            track_id=p.track_id,
            kind="person",
            label=texts.OBJECT_LABELS["person"],
            score=p.score,
            bbox=_box(p.bbox, w, h),
            kpts=_kpts(p.kpts, w, h),
            tags=_person_tags(p, ctx.ts_ms, running, cfg)
            + violations.get(f"track:{p.track_id}", []),
        )
        for p in ctx.persons
    ]
    objects += [
        HudObject(
            track_id=v.track_id,
            kind="vehicle",
            label=texts.OBJECT_LABELS.get(v.name, v.name),
            score=v.score,
            bbox=_box(v.bbox, w, h),
            kpts=None,
            tags=violations.get(f"vehicle:{v.track_id}", []),
        )
        for v in ctx.vehicles
    ]
    objects += [
        HudObject(
            track_id=None,
            kind="phone" if o.name == "cell phone" else "other",
            label=texts.OBJECT_LABELS.get(o.name, o.name),
            score=o.score,
            bbox=_box(o.bbox, w, h),
            kpts=None,
            tags=_object_tags(o, violations),
            projection=_projection(o, w, h),
        )
        for o in ctx.objects
    ]
    return HudFrame(frame_idx=ctx.frame_idx, ts_ms=ctx.ts_ms, objects=objects)
