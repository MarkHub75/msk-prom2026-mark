"""Scenario `load_carrying` (tech.md 8.3): a skeleton, the carrying rules are not defined yet."""

from safewatch import texts
from safewatch.types import EpisodeDraft, FrameContext, Observation, ScenarioMeta, WhyItem

ID = "load_carrying"


class LoadCarryingPlugin:
    meta = ScenarioMeta(
        id=ID,
        title=texts.SCENARIO_TITLES[ID],
        description=texts.SCENARIO_DESCRIPTIONS[ID],
        icon="box",
        default_level="yellow",
        status="skeleton",  # rules.scenario_metas() keeps it: no logic, no analysis
        status_text="",
        required_classes=[],
        zone_kinds=[],
        params=[],
    )

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]:
        return []

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        return []
