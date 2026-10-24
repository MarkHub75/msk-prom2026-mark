"""Helpers shared by the scenario plugins (tech.md 7, 8.3)."""

from safewatch import texts
from safewatch.analysis.geometry import point_in_polygon
from safewatch.types import (
    EpisodeDraft,
    FrameContext,
    Level,
    Observation,
    ObsState,
    PersonState,
    Point,
    ScenarioParam,
    WhyItem,
    Zone,
)


def zones_at(ctx: FrameContext, point: Point, kinds: tuple[str, ...]) -> list[Zone]:
    """Polygon zones of `kinds` that hold `point` (pixels; zones are in 0..1)."""
    p = (point[0] / ctx.width, point[1] / ctx.height)
    return [z for z in ctx.zones if z.kind in kinds and point_in_polygon(p, z.points)]


def param(key: str, lo: float, hi: float) -> ScenarioParam:
    """A plugin parameter with its range; titles and units live in `texts.PARAM_TITLES`."""
    title, unit = texts.PARAM_TITLES[key]
    # `default` is a placeholder: rules.scenario_metas() puts the value of config/default.yaml.
    return ScenarioParam(key=key, title=title, unit=unit, default=0.0, min=lo, max=hi)


def obs(
    scenario: str,
    person: PersonState,
    state: ObsState,
    *,
    level: Level = "yellow",
    hold_s: float = 0.0,
    reason_code: str = "",
    reason_text: str = "",
    method: str = "",
    metrics: dict[str, float] | None = None,
    zone_id: int | None = None,
) -> Observation:
    """An observation about one tracked person: subject `track:<id>`."""
    return Observation(
        scenario=scenario,
        subject=f"track:{person.track_id}",
        state=state,
        level=level,
        hold_s=hold_s,
        reason_code=reason_code,
        reason_text=reason_text,
        method=method,
        confidence=person.score,
        metrics=metrics or {},
        zone_id=zone_id,
        anchor=person.anchor,
        ref_height_px=person.ref_height_px,
    )


def why_common(episode: EpisodeDraft) -> list[WhyItem]:
    """The "why" lines every scenario shares: measured peaks, method, confidence, blind time."""
    items = [
        WhyItem(label=texts.METRIC_TITLES.get(key, key), value=texts.fmt_num(value))
        for key, value in episode.metrics.items()
    ]
    method = texts.METHOD_TITLES.get(episode.method, episode.method)
    items.append(WhyItem(label=texts.WHY_METHOD, value=method))
    items.append(WhyItem(label=texts.WHY_CONFIDENCE, value=texts.fmt_num(episode.confidence)))
    if episode.uncertain_ms > 0:
        n = episode.uncertain_ms // 1000
        items.append(WhyItem(label=texts.WHY_UNCERTAIN, value=texts.WHY_SECONDS.format(n=n)))
    return items
