"""Scenario `fire_smoking` (tech.md 8.3): fire or smoke outside the allowed zones, smoking."""

from safewatch import config as app_config
from safewatch import texts
from safewatch.rules.base import attach_objects, obs, param, why_common, zones_at
from safewatch.types import (
    EpisodeDraft,
    FrameContext,
    Observation,
    ObsState,
    ScenarioMeta,
    WhyItem,
)

ID = "fire_smoking"
FLAMES = ("fire", "smoke")


def _fire(ctx: FrameContext, params: dict[str, float]) -> Observation:
    """One subject `fire` per frame: P while any flame has its center outside fire_allowed."""
    outside = []
    for o in ctx.objects:
        center = ((o.bbox[0] + o.bbox[2]) / 2, (o.bbox[1] + o.bbox[3]) / 2)
        if o.name in FLAMES and not zones_at(ctx, center, ("fire_allowed",)):
            outside.append(o)
    state: ObsState = "P" if outside else "N"
    score = max((o.score for o in outside), default=0.0)
    return Observation(
        scenario=ID,
        subject="fire",
        state=state,
        level="red",
        hold_s=params["fire_hold_s"],
        reason_code="fire" if outside else "",
        reason_text=texts.FIRE_OUTSIDE if outside else "",
        method="",
        confidence=score,
        metrics={"score": score} if outside else {},
        zone_id=None,
        anchor=None,
        ref_height_px=None,
    )


class FirePlugin:
    meta = ScenarioMeta(
        id=ID,
        title=texts.SCENARIO_TITLES[ID],
        description=texts.SCENARIO_DESCRIPTIONS[ID],
        icon="fire",
        default_level="red",
        status="active",
        status_text="",
        required_classes=["fire", "smoke", "cigarette"],  # any one of them (rules.ANY_CLASS)
        zone_kinds=["fire_allowed", "danger"],
        params=[param("fire_hold_s", 0.0, 60.0), param("smoking_hold_s", 0.0, 60.0)],
    )

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]:
        out = [_fire(ctx, params)]
        # The cigarette is bound like a phone: upper_frac and wrist_dist_bh of scenarios.phone.
        attach = app_config.get_settings().scenarios.phone
        cigarettes = attach_objects(ctx, "cigarette", attach)
        for p in ctx.persons:
            cigarette = cigarettes.get(p.track_id)
            if cigarette == "ambiguous":
                out.append(obs(ID, p, "U", reason_code="owner_ambiguous"))
                continue
            if cigarette is None:
                out.append(obs(ID, p, "N"))
                continue
            zones = zones_at(ctx, p.anchor, ("danger",))
            reason = texts.SMOKING + (texts.IN_ZONE.format(zone=zones[0].name) if zones else "")
            o = obs(
                ID,
                p,
                "P",
                level="red" if zones else "yellow",
                hold_s=params["smoking_hold_s"],
                reason_code="smoking_zone" if zones else "smoking",
                reason_text=reason,
                metrics={"score": cigarette.score},
                zone_id=zones[0].id if zones else None,
            )
            out.append(o)
        return out

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        hold = params["fire_hold_s" if episode.subject == "fire" else "smoking_hold_s"]
        rule = texts.WHY_HOLD.format(rule=episode.reason_text, s=texts.fmt_num(hold))
        return [WhyItem(label=texts.WHY_RULE, value=rule), *why_common(episode)]
