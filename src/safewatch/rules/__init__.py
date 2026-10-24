"""Scenario plugins (tech.md 8.3). Each slice that brings a plugin registers it here."""

from safewatch import config, registry, texts
from safewatch.rules.fall import FallPlugin
from safewatch.rules.running import RunningPlugin
from safewatch.types import ScenarioMeta, ScenarioPlugin

PLUGINS: dict[str, ScenarioPlugin] = {"running": RunningPlugin(), "fall": FallPlugin()}


def defaults(scenario: str) -> dict[str, float]:
    """Parameters of `scenarios.<id>` in the config."""
    params: dict[str, float] = getattr(config.get_settings().scenarios, scenario)
    return dict(params)


def scenario_metas(active_classes: list[str] | None = None) -> list[ScenarioMeta]:
    """Plugins with status and config defaults; `active_classes`: snapshot of an analysis."""
    if active_classes is None:
        active_classes = registry.active_classes(config.get_settings())
    out = []
    for scenario, plugin in PLUGINS.items():
        meta = plugin.meta
        missing = [c for c in meta.required_classes if c not in active_classes]
        values = defaults(scenario)
        out.append(
            meta.model_copy(
                update={
                    "status": "model_missing" if missing else "active",
                    "status_text": texts.SCENARIO_MODEL_MISSING.format(classes=", ".join(missing))
                    if missing
                    else texts.SCENARIO_ACTIVE,
                    "params": [
                        p.model_copy(update={"default": values[p.key]}) for p in meta.params
                    ],
                }
            )
        )
    return out
