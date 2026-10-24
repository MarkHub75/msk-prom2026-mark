"""Scenario `running` (tech.md 8.3): running, red in a danger zone or next to a vehicle."""

from safewatch import texts
from safewatch.analysis.geometry import point_rect_distance, point_segment_distance
from safewatch.rules.base import obs, param, why_common, zones_at
from safewatch.types import (
    EpisodeDraft,
    FrameContext,
    Level,
    Observation,
    PersonState,
    ScenarioMeta,
    WhyItem,
)

ID = "running"
DANGER_KINDS = ("danger", "vehicle_path")


def _near_vehicle(ctx: FrameContext, p: PersonState, params: dict[str, float]) -> bool:
    for v in ctx.vehicles:
        if p.ground is not None and v.footprint is not None:
            if point_segment_distance(p.ground, *v.footprint) <= params["near_vehicle_m"]:
                return True
        elif point_rect_distance(p.foot, v.bbox) / p.ref_height_px <= params["near_vehicle_bh"]:
            return True
    return False


class RunningPlugin:
    meta = ScenarioMeta(
        id=ID,
        title=texts.SCENARIO_TITLES[ID],
        description=texts.SCENARIO_DESCRIPTIONS[ID],
        icon="run",
        default_level="yellow",
        status="active",
        status_text="",
        required_classes=["person"],
        zone_kinds=list(DANGER_KINDS),
        params=[
            param("speed_bh_s", 0.5, 5.0),
            param("speed_m_s", 0.5, 10.0),
            param("hold_s", 0.0, 60.0),
            param("red_hold_s", 0.0, 60.0),
            param("near_vehicle_bh", 0.0, 20.0),
            param("near_vehicle_m", 0.0, 30.0),
        ],
    )

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]:
        out = []
        for p in ctx.persons:
            if p.speed_m_s is not None:  # calibrated floor: meters per second
                speed, limit, method = p.speed_m_s, params["speed_m_s"], "calibrated"
                key, text = "speed_m_s", texts.RUN_M
            elif p.speed_bh_s is not None:
                speed, limit, method = p.speed_bh_s, params["speed_bh_s"], "relative"
                key, text = "speed_bh_s", texts.RUN_BH
            else:
                out.append(obs(ID, p, "U"))
                continue
            if speed < limit:
                out.append(obs(ID, p, "N", method=method))
                continue
            reason = text.format(v=texts.fmt_num(speed))
            level: Level = "yellow"
            hold, code, zone_id = params["hold_s"], "running", None
            zones = zones_at(ctx, p.anchor, DANGER_KINDS)
            if zones:
                level, hold, code, zone_id = (
                    "red",
                    params["red_hold_s"],
                    "running_zone",
                    zones[0].id,
                )
                reason += texts.IN_ZONE.format(zone=zones[0].name)
            elif _near_vehicle(ctx, p, params):
                level, hold, code = "red", params["red_hold_s"], "running_vehicle"
                reason += texts.NEAR_VEHICLE
            out.append(
                obs(
                    ID,
                    p,
                    "P",
                    level=level,
                    hold_s=hold,
                    reason_code=code,
                    reason_text=reason,
                    method=method,
                    metrics={key: speed},
                    zone_id=zone_id,
                )  # fmt: skip
            )
        return out

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        hold = texts.fmt_num(params["red_hold_s" if episode.level_initial == "red" else "hold_s"])
        if episode.method == "calibrated":
            rule = texts.WHY_RUN_M.format(v=texts.fmt_num(params["speed_m_s"]), s=hold)
        else:
            rule = texts.WHY_RUN_BH.format(v=texts.fmt_num(params["speed_bh_s"]), s=hold)
        return [WhyItem(label=texts.WHY_RULE, value=rule), *why_common(episode)]
