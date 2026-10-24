"""Scenario `fence_crossing` (tech.md 8.3): the step prev_anchor → anchor crosses a fence line."""

from safewatch import texts
from safewatch.analysis.geometry import segment_crossing
from safewatch.rules.base import obs, param, why_common
from safewatch.types import EpisodeDraft, FrameContext, Observation, ScenarioMeta, WhyItem

ID = "fence_crossing"


class FencePlugin:
    meta = ScenarioMeta(
        id=ID,
        title=texts.SCENARIO_TITLES[ID],
        description=texts.SCENARIO_DESCRIPTIONS[ID],
        icon="fence",
        default_level="red",
        status="active",
        status_text="",
        required_classes=["person"],
        zone_kinds=["fence"],
        params=[param("max_gap_s", 0.0, 10.0)],
    )

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]:
        fences = [z for z in ctx.zones if z.kind == "fence"]
        out = []
        for p in ctx.persons:
            if p.prev_anchor is None or p.prev_ts_ms is None:
                out.append(obs(ID, p, "U", level="red"))
                continue
            a = (p.prev_anchor[0] / ctx.width, p.prev_anchor[1] / ctx.height)
            b = (p.anchor[0] / ctx.width, p.anchor[1] / ctx.height)
            crossed = [z for z in fences if segment_crossing(a, b, z.points[0], z.points[1])]
            if not crossed:
                out.append(obs(ID, p, "N", level="red"))
                continue
            reason = texts.FENCE_CROSSED.format(zone=crossed[0].name)
            code = "fence_crossing"
            # A long blind gap still holds the crossing, but nobody saw the moment itself.
            if ctx.ts_ms - p.prev_ts_ms > params["max_gap_s"] * 1000:
                reason, code = reason + texts.FENCE_UNSEEN, "fence_unseen"
            out.append(
                obs(
                    ID,
                    p,
                    "P",
                    level="red",
                    reason_code=code,
                    reason_text=reason,
                    zone_id=crossed[0].id,
                )
            )
        return out

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        return [WhyItem(label=texts.WHY_RULE, value=episode.reason_text), *why_common(episode)]
