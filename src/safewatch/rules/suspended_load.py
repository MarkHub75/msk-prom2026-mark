"""Scenario `suspended_load` (tech.md 8.3): a person below a lifted load, within its width."""

from safewatch import texts
from safewatch.rules.base import obs, param, why_common
from safewatch.types import EpisodeDraft, FrameContext, Observation, ScenarioMeta, WhyItem

ID = "suspended_load"


class SuspendedLoadPlugin:
    meta = ScenarioMeta(
        id=ID,
        title=texts.SCENARIO_TITLES[ID],
        description=texts.SCENARIO_DESCRIPTIONS[ID],
        icon="crane",
        default_level="red",
        status="active",
        status_text="",
        required_classes=["person", "suspended_load"],
        zone_kinds=[],
        params=[param("load_hold_s", 0.0, 60.0)],
    )

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]:
        loads = [o for o in ctx.objects if o.name == "suspended_load"]
        out = []
        for p in ctx.persons:
            x, y = p.anchor
            under = [o for o in loads if o.bbox[0] <= x <= o.bbox[2] and y > o.bbox[3]]
            if not under:
                out.append(obs(ID, p, "N", level="red"))
                continue
            out.append(
                obs(
                    ID,
                    p,
                    "P",
                    level="red",
                    hold_s=params["load_hold_s"],
                    reason_code="suspended_load",
                    reason_text=texts.UNDER_LOAD,
                    metrics={"score": max(o.score for o in under)},
                )
            )
        return out

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        hold = texts.fmt_num(params["load_hold_s"])
        rule = texts.WHY_HOLD.format(rule=episode.reason_text, s=hold)
        return [WhyItem(label=texts.WHY_RULE, value=rule), *why_common(episode)]
