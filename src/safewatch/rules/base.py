"""Helpers shared by the scenario plugins (tech.md 7, 8.3)."""

import math
from typing import Literal

from safewatch import config as app_config
from safewatch import texts
from safewatch.analysis.geometry import point_in_polygon
from safewatch.types import (
    EpisodeDraft,
    FrameContext,
    Level,
    ObjectState,
    Observation,
    ObsState,
    PersonState,
    Point,
    ScenarioParam,
    WhyItem,
    Zone,
)


def zones_at(ctx: FrameContext, point: Point, kinds: tuple[str, ...]) -> list[Zone]:
    """Polygon zones of `kinds` that hold `point` (pixels; zones are in 0..1)."""
    p = (point[0] / ctx.width, point[1] / ctx.height)
    return [z for z in ctx.zones if z.kind in kinds and point_in_polygon(p, z.points)]


WRISTS = (9, 10)  # COCO keypoints


def attach_objects(
    ctx: FrameContext, name: str, params: dict[str, float]
) -> dict[int, ObjectState | Literal["ambiguous"]]:
    """Objects `name` held by a person (tech.md 8.3), by track id.

    An object fits a person when its center is inside the upper `upper_frac` of the bbox or
    closer than `wrist_dist_bh` × H_ref to a visible wrist. One fit: attached; two or more:
    `ambiguous` for each of them.
    """
    kpt_conf = app_config.get_settings().pose.kpt_conf
    out: dict[int, ObjectState | Literal["ambiguous"]] = {}
    for o in ctx.objects:
        if o.name != name:
            continue
        cx, cy = (o.bbox[0] + o.bbox[2]) / 2, (o.bbox[1] + o.bbox[3]) / 2
        owners = []
        for p in ctx.persons:
            x1, y1, x2, y2 = p.bbox
            upper = x1 <= cx <= x2 and y1 <= cy <= y1 + params["upper_frac"] * (y2 - y1)
            reach = params["wrist_dist_bh"] * p.ref_height_px
            wrists = [p.kpts[i] for i in WRISTS if p.kpts is not None and p.kpts[i][2] >= kpt_conf]
            if upper or any(math.dist((cx, cy), w[:2]) < reach for w in wrists):
                owners.append(p.track_id)
        for track_id in owners:
            if len(owners) > 1:
                out[track_id] = "ambiguous"
            elif out.get(track_id) != "ambiguous":
                out.setdefault(track_id, o)
    return out


def head_objects(
    ctx: FrameContext, name: str, head_frac: float
) -> dict[int, ObjectState | Literal["ambiguous"]]:
    """Objects `name` on a person's head (tech.md 8.22), by track id.

    An object fits a person when its center is within the bbox x range and inside the upper
    `head_frac` of the bbox height. One fit: attached; two or more: `ambiguous` for each.
    """
    out: dict[int, ObjectState | Literal["ambiguous"]] = {}
    for o in ctx.objects:
        if o.name != name:
            continue
        cx, cy = (o.bbox[0] + o.bbox[2]) / 2, (o.bbox[1] + o.bbox[3]) / 2
        owners = [
            p.track_id
            for p in ctx.persons
            if p.bbox[0] <= cx <= p.bbox[2]
            and p.bbox[1] <= cy <= p.bbox[1] + head_frac * (p.bbox[3] - p.bbox[1])
        ]
        for track_id in owners:
            if len(owners) > 1:
                out[track_id] = "ambiguous"
            elif out.get(track_id) != "ambiguous":
                out.setdefault(track_id, o)
    return out


def param(key: str, lo: float, hi: float) -> ScenarioParam:
    """A plugin parameter with its range; titles and units live in `texts.PARAM_TITLES`."""
    title, unit = texts.PARAM_TITLES[key]
    # `default` is a placeholder: rules.scenario_metas() puts the value of config/default.yaml.
    return ScenarioParam(key=key, title=title, unit=unit, default=0.0, min=lo, max=hi)


def obs(
    scenario: str,
    person: PersonState,
    state: ObsState,
    *,
    level: Level = "yellow",
    hold_s: float = 0.0,
    reason_code: str = "",
    reason_text: str = "",
    method: str = "",
    metrics: dict[str, float] | None = None,
    zone_id: int | None = None,
) -> Observation:
    """An observation about one tracked person: subject `track:<id>`."""
    return Observation(
        scenario=scenario,
        subject=f"track:{person.track_id}",
        state=state,
        level=level,
        hold_s=hold_s,
        reason_code=reason_code,
        reason_text=reason_text,
        method=method,
        confidence=person.score,
        metrics=metrics or {},
        zone_id=zone_id,
        anchor=person.anchor,
        ref_height_px=person.ref_height_px,
    )


def why_common(episode: EpisodeDraft) -> list[WhyItem]:
    """The "why" lines every scenario shares: measured peaks, method, confidence, blind time."""
    items = [
        WhyItem(label=texts.METRIC_TITLES.get(key, key), value=texts.fmt_num(value))
        for key, value in episode.metrics.items()
    ]
    method = texts.METHOD_TITLES.get(episode.method, episode.method)
    items.append(WhyItem(label=texts.WHY_METHOD, value=method))
    items.append(WhyItem(label=texts.WHY_CONFIDENCE, value=texts.fmt_num(episode.confidence)))
    if episode.uncertain_ms > 0:
        n = episode.uncertain_ms // 1000
        items.append(WhyItem(label=texts.WHY_UNCERTAIN, value=texts.WHY_SECONDS.format(n=n)))
    return items
