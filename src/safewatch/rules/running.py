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
AUTOCAL_SAMPLES = "autocal_samples"  # episode metric: standing people behind the "auto" speed


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
            metrics: dict[str, float] = {}
            if p.speed_m_s is not None:  # calibrated floor or autocalibration: m/s (8.21)
                speed, limit = p.speed_m_s, params["speed_m_s"]
                key, text = "speed_m_s", texts.RUN_M
                method = "auto" if p.speed_source == "auto" else "calibrated"
                if method == "auto" and ctx.auto_calibration is not None:
                    metrics[AUTOCAL_SAMPLES] = ctx.auto_calibration.samples
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
                    metrics={key: speed} | metrics,
                    zone_id=zone_id,
                )  # fmt: skip
            )
        return out

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        hold = texts.fmt_num(params["red_hold_s" if episode.level_initial == "red" else "hold_s"])
        if episode.method in ("calibrated", "auto"):
            rule = texts.WHY_RUN_M.format(v=texts.fmt_num(params["speed_m_s"]), s=hold)
        else:
            rule = texts.WHY_RUN_BH.format(v=texts.fmt_num(params["speed_bh_s"]), s=hold)
        items = [WhyItem(label=texts.WHY_RULE, value=rule)]
        # The source of the speed (tech.md 8.21); the sample count is no metric of its own.
        samples = episode.metrics.get(AUTOCAL_SAMPLES)
        if episode.method == "auto" and samples is not None:
            source = texts.WHY_SPEED_AUTO.format(n=round(samples))
            items.append(WhyItem(label=texts.WHY_SPEED, value=source))
        elif episode.method == "calibrated":
            items.append(WhyItem(label=texts.WHY_SPEED, value=texts.WHY_SPEED_CALIBRATION))
        metrics = {k: v for k, v in episode.metrics.items() if k != AUTOCAL_SAMPLES}
        return [*items, *why_common(episode.model_copy(update={"metrics": metrics}))]
