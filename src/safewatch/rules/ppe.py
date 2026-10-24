"""Scenarios `no_helmet` and `no_respirator` (tech.md 8.22): PPE on the head inside a zone."""

from safewatch import texts
from safewatch.rules.base import head_objects, obs, param, why_common, zones_at
from safewatch.types import (
    EpisodeDraft,
    FrameContext,
    ObjectState,
    Observation,
    ScenarioMeta,
    WhyItem,
)


def _meta(scenario: str, icon: str, missing: str, kind: str) -> ScenarioMeta:
    return ScenarioMeta(
        id=scenario,
        title=texts.SCENARIO_TITLES[scenario],
        description=texts.SCENARIO_DESCRIPTIONS[scenario],
        icon=icon,
        default_level="yellow",
        status="active",
        status_text="",
        required_classes=["person", missing],
        zone_kinds=[kind],
        params=[
            param("hold_s", 0.0, 60.0),
            param("head_frac", 0.0, 1.0),
            param("min_person_px", 0.0, 2000.0),
        ],
    )


def _observe(
    ctx: FrameContext,
    params: dict[str, float],
    scenario: str,
    worn: str,
    kind: str,
    reason: str,
) -> list[Observation]:
    """P: `no_<worn>` on the head in a `kind` zone; N: `worn` on the head or outside the zone."""
    missing = head_objects(ctx, f"no_{worn}", params["head_frac"])
    present = head_objects(ctx, worn, params["head_frac"])
    out = []
    for p in ctx.persons:
        zones = zones_at(ctx, p.anchor, (kind,))
        if not zones:
            out.append(obs(scenario, p, "N"))
            continue
        if p.height_px < params["min_person_px"]:
            out.append(obs(scenario, p, "U", reason_code="too_small"))
            continue
        bad, good = missing.get(p.track_id), present.get(p.track_id)
        # Both classes on one head (the model wavers): the surer one wins, a tie stays P.
        if (
            isinstance(bad, ObjectState)
            and isinstance(good, ObjectState)
            and good.score > bad.score
        ):
            bad = None
        if bad == "ambiguous" or (bad is None and good == "ambiguous"):
            out.append(obs(scenario, p, "U", reason_code="owner_ambiguous"))
        elif bad is not None:
            o = obs(
                scenario,
                p,
                "P",
                hold_s=params["hold_s"],
                reason_code=scenario,
                reason_text=reason.format(zone=zones[0].name),
                metrics={"score": bad.score},
                zone_id=zones[0].id,
            )
            out.append(o)
        elif good is not None:
            out.append(obs(scenario, p, "N"))
        else:
            out.append(obs(scenario, p, "U", reason_code="head_unseen"))
    return out


def _explain(episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
    rule = texts.WHY_HOLD.format(rule=episode.reason_text, s=texts.fmt_num(params["hold_s"]))
    return [WhyItem(label=texts.WHY_RULE, value=rule), *why_common(episode)]


class HelmetPlugin:
    meta = _meta("no_helmet", "helmet", "no_helmet", "helmet_required")

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]:
        return _observe(ctx, params, "no_helmet", "helmet", "helmet_required", texts.NO_HELMET)

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        return _explain(episode, params)


class RespiratorPlugin:
    meta = _meta("no_respirator", "mask", "no_respirator", "respirator_required")

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]:
        kind, text = "respirator_required", texts.NO_RESPIRATOR
        return _observe(ctx, params, "no_respirator", "respirator", kind, text)

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        return _explain(episode, params)
