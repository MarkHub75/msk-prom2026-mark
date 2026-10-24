"""Scenario `no_harness` (tech.md 8.3): work at height with a `no_harness` object on the person."""

from safewatch import texts
from safewatch.analysis.geometry import ioa
from safewatch.rules.base import obs, param, why_common, zones_at
from safewatch.types import EpisodeDraft, FrameContext, Observation, ScenarioMeta, WhyItem

ID = "no_harness"


class HarnessPlugin:
    meta = ScenarioMeta(
        id=ID,
        title=texts.SCENARIO_TITLES[ID],
        description=texts.SCENARIO_DESCRIPTIONS[ID],
        icon="harness",
        default_level="yellow",
        status="active",
        status_text="",
        required_classes=["person", "no_harness"],
        zone_kinds=["height"],
        params=[param("harness_hold_s", 0.0, 60.0)],
    )

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]:
        flags = [o for o in ctx.objects if o.name == "no_harness"]
        out = []
        for p in ctx.persons:
            zones = zones_at(ctx, p.anchor, ("height",))
            hits = [o for o in flags if ioa(p.bbox, o.bbox) > 0]
            if not zones or not hits:
                out.append(obs(ID, p, "N"))
                continue
            out.append(
                obs(
                    ID,
                    p,
                    "P",
                    hold_s=params["harness_hold_s"],
                    reason_code="no_harness",
                    reason_text=texts.NO_HARNESS,
                    metrics={"score": max(o.score for o in hits)},
                    zone_id=zones[0].id,
                )
            )
        return out

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        hold = texts.fmt_num(params["harness_hold_s"])
        rule = texts.WHY_HOLD.format(rule=episode.reason_text, s=hold)
        return [WhyItem(label=texts.WHY_RULE, value=rule), *why_common(episode)]
