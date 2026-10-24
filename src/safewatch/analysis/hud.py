"""HUD frames (tech.md 8.2 item 8): what the player draws over the video, in 0..1 coordinates."""

from safewatch import texts
from safewatch.config import FeaturesConfig
from safewatch.types import Box, FrameContext, HudFrame, HudObject, HudTag, Keypoint, PersonState


def _unit(v: float, size: int) -> float:
    return min(1.0, max(0.0, v / size))


def _box(box: Box, w: int, h: int) -> Box:
    return (_unit(box[0], w), _unit(box[1], h), _unit(box[2], w), _unit(box[3], h))


def _kpts(points: list[Keypoint] | None, w: int, h: int) -> list[Keypoint] | None:
    if points is None:
        return None
    return [(_unit(x, w), _unit(y, h), conf) for x, y, conf in points]


def _person_tags(p: PersonState, ts_ms: int, run_bh_s: float, cfg: FeaturesConfig) -> list[HudTag]:
    tags = []
    if p.speed_bh_s is not None:
        v = texts.fmt_num(p.speed_bh_s)
        # Same comparison as the running rule: the HUD turns yellow where the rule would fire.
        if p.speed_bh_s >= run_bh_s:
            tags.append(HudTag(code="speed", text=texts.HUD_RUN_BH.format(v=v), level="yellow"))
        else:
            tags.append(HudTag(code="speed", text=texts.HUD_SPEED_BH.format(v=v), level=None))
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


def build_hud(ctx: FrameContext, run_bh_s: float, cfg: FeaturesConfig) -> HudFrame:
    """`run_bh_s`: the running threshold that turns the speed tag yellow."""
    w, h = ctx.width, ctx.height
    objects = [
        HudObject(
            track_id=p.track_id,
            kind="person",
            label=texts.OBJECT_LABELS["person"],
            score=p.score,
            bbox=_box(p.bbox, w, h),
            kpts=_kpts(p.kpts, w, h),
            tags=_person_tags(p, ctx.ts_ms, run_bh_s, cfg),
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
            tags=[],
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
            tags=[],
        )
        for o in ctx.objects
    ]
    return HudFrame(frame_idx=ctx.frame_idx, ts_ms=ctx.ts_ms, objects=objects)
