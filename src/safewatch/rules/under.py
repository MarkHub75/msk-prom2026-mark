"""Scenario `restricted_under` (tech.md 8.3): a person under a conveyor or a lifted load."""

from safewatch import texts
from safewatch.rules.base import obs, param, why_common, zones_at
from safewatch.types import EpisodeDraft, FrameContext, Observation, ScenarioMeta, WhyItem

ID = "restricted_under"


class UnderPlugin:
    meta = ScenarioMeta(
        id=ID,
        title=texts.SCENARIO_TITLES[ID],
        description=texts.SCENARIO_DESCRIPTIONS[ID],
        icon="conveyor",
        default_level="red",
        status="active",
        status_text="",
        required_classes=["person"],
        zone_kinds=["under_load"],
        params=[param("under_hold_s", 0.0, 60.0)],
    )

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]:
        out = []
        for p in ctx.persons:
            zones = zones_at(ctx, p.anchor, ("under_load",))
            if not zones:
                out.append(obs(ID, p, "N", level="red"))
                continue
            out.append(
                obs(
                    ID,
                    p,
                    "P",
                    level="red",
                    hold_s=params["under_hold_s"],
                    reason_code="under_zone",
                    reason_text=texts.PERSON_IN_ZONE.format(zone=zones[0].name),
                    zone_id=zones[0].id,
                )
            )
        return out

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        hold = texts.fmt_num(params["under_hold_s"])
        rule = texts.WHY_HOLD.format(rule=episode.reason_text, s=hold)
        return [WhyItem(label=texts.WHY_RULE, value=rule), *why_common(episode)]
