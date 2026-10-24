"""Scenario `proximity` (tech.md 8.3): a person close to moving machinery or in a danger zone."""

from safewatch import texts
from safewatch.analysis.geometry import ioa, point_rect_distance, point_segment_distance
from safewatch.rules.base import obs, param, why_common, zones_at
from safewatch.types import (
    EpisodeDraft,
    FrameContext,
    Observation,
    PersonState,
    ScenarioMeta,
    VehicleState,
    WhyItem,
)

ID = "proximity"


def _moving(v: VehicleState, params: dict[str, float]) -> bool | None:
    """Calibrated speed wins over the speed in own heights; None: speed unknown."""
    if v.speed_m_s is not None:
        return v.speed_m_s >= params["moving_m_s"]
    if v.speed_vh_s is not None:
        return v.speed_vh_s >= params["moving_vh_s"]
    return None


def _pair(p: PersonState, v: VehicleState, params: dict[str, float]) -> Observation:
    subject = {"subject": f"pair:{p.track_id}-{v.track_id}"}
    moving = _moving(v, params)
    if moving is None:
        return obs(ID, p, "U").model_copy(update=subject)
    if p.ground is not None and v.footprint is not None:
        dist, method, key = point_segment_distance(p.ground, *v.footprint), "calibrated", "m"
        text = texts.PROXIMITY_M
    else:
        dist = point_rect_distance(p.foot, v.bbox) / p.ref_height_px
        method, key, text = "relative", "bh", texts.PROXIMITY_BH
    if not moving or dist > params[f"yellow_{key}"]:
        return obs(ID, p, "N", method=method).model_copy(update=subject)
    red = dist <= params[f"red_{key}"]
    reason = text.format(vehicle=texts.VEHICLE_WITH.get(v.name, v.name), v=texts.fmt_num(dist))
    o = obs(
        ID,
        p,
        "P",
        level="red" if red else "yellow",
        hold_s=params["red_hold_s" if red else "hold_s"],
        reason_code="proximity_red" if red else "proximity",
        reason_text=reason,
        method=method,
        metrics={f"distance_{key}": dist},
    )
    return o.model_copy(update=subject)


class ProximityPlugin:
    meta = ScenarioMeta(
        id=ID,
        title=texts.SCENARIO_TITLES[ID],
        description=texts.SCENARIO_DESCRIPTIONS[ID],
        icon="truck",
        default_level="red",
        status="active",
        status_text="",
        required_classes=["person", "car", "bus", "truck", "train"],
        zone_kinds=["danger"],
        params=[
            param("yellow_bh", 0.0, 20.0),
            param("red_bh", 0.0, 20.0),
            param("yellow_m", 0.0, 30.0),
            param("red_m", 0.0, 30.0),
            param("moving_vh_s", 0.0, 5.0),
            param("moving_m_s", 0.0, 10.0),
            param("hold_s", 0.0, 60.0),
            param("red_hold_s", 0.0, 60.0),
            param("driver_ioa", 0.0, 1.0),
        ],
    )

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]:
        out = []
        for p in ctx.persons:
            # A driver sits inside the machine: neither the pair nor a zone is about him.
            if any(ioa(p.bbox, v.bbox) >= params["driver_ioa"] for v in ctx.vehicles):
                continue
            out += [_pair(p, v, params) for v in ctx.vehicles]
            inside = {z.id for z in zones_at(ctx, p.anchor, ("danger",))}
            for z in ctx.zones:
                if z.kind != "danger":
                    continue
                subject = {"subject": f"zone:{p.track_id}-{z.id}"}
                if z.id not in inside:
                    out.append(obs(ID, p, "N").model_copy(update=subject))
                    continue
                o = obs(
                    ID,
                    p,
                    "P",
                    level="red",
                    hold_s=params["red_hold_s"],
                    reason_code="proximity_zone",
                    reason_text=texts.PERSON_IN_ZONE.format(zone=z.name),
                    zone_id=z.id,
                )
                out.append(o.model_copy(update=subject))
        return out

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        if episode.reason_code == "proximity_zone":
            rule = episode.reason_text
        elif episode.method == "calibrated":
            rule = texts.WHY_PROXIMITY_M.format(
                red=texts.fmt_num(params["red_m"]), yellow=texts.fmt_num(params["yellow_m"])
            )
        else:
            rule = texts.WHY_PROXIMITY_BH.format(
                red=texts.fmt_num(params["red_bh"]), yellow=texts.fmt_num(params["yellow_bh"])
            )
        return [WhyItem(label=texts.WHY_RULE, value=rule), *why_common(episode)]
