"""Scenario plugins (tech.md 8.3). Each slice that brings a plugin registers it here."""

from safewatch import config, registry, texts
from safewatch.rules.fall import FallPlugin
from safewatch.rules.fence import FencePlugin
from safewatch.rules.fire import FirePlugin
from safewatch.rules.harness import HarnessPlugin
from safewatch.rules.load_carrying import LoadCarryingPlugin
from safewatch.rules.phone import PhonePlugin
from safewatch.rules.ppe import HelmetPlugin, RespiratorPlugin
from safewatch.rules.proximity import ProximityPlugin
from safewatch.rules.running import RunningPlugin
from safewatch.rules.suspended_load import SuspendedLoadPlugin
from safewatch.rules.under import UnderPlugin
from safewatch.types import ScenarioMeta, ScenarioPlugin

PLUGINS: list[ScenarioPlugin] = [
    RunningPlugin(),
    ProximityPlugin(),
    PhonePlugin(),
    FallPlugin(),
    FencePlugin(),
    UnderPlugin(),
    FirePlugin(),
    HarnessPlugin(),
    SuspendedLoadPlugin(),
    LoadCarryingPlugin(),
    HelmetPlugin(),
    RespiratorPlugin(),
]
ANY_CLASS = {"fire_smoking"}  # one of `required_classes` is enough (tech.md 8.3)
ANY_VEHICLE = {"proximity"}  # person and one of `pipeline.vehicle_classes` (tech.md 8.30)


def plugin(scenario: str) -> ScenarioPlugin:
    """The plugin of a scenario id; `KeyError` when there is none."""
    for p in PLUGINS:
        if p.meta.id == scenario:
            return p
    raise KeyError(scenario)


def defaults(scenario: str) -> dict[str, float]:
    """Parameters of `scenarios.<id>` in the config."""
    params: dict[str, float] = getattr(config.get_settings().scenarios, scenario)
    return dict(params)


def scenario_metas(active_classes: list[str] | None = None) -> list[ScenarioMeta]:
    """Plugins with status and config defaults; `active_classes`: snapshot of an analysis."""
    if active_classes is None:
        active_classes = registry.active_classes(config.get_settings())
    vehicles = config.get_settings().pipeline.vehicle_classes
    out = []
    for plug in PLUGINS:
        meta = plug.meta
        required = ["person", *vehicles] if meta.id in ANY_VEHICLE else meta.required_classes
        missing = [c for c in required if c not in active_classes]
        if meta.id in ANY_CLASS and len(missing) < len(required):
            missing = []
        if meta.id in ANY_VEHICLE and any(v in active_classes for v in vehicles):
            missing = [c for c in missing if c not in vehicles]
        if meta.status == "skeleton":
            status, text = "skeleton", texts.SCENARIO_SKELETON
        elif missing:
            status = "model_missing"
            text = texts.SCENARIO_MODEL_MISSING.format(classes=", ".join(missing))
        else:
            status, text = "active", texts.SCENARIO_ACTIVE
        values = defaults(meta.id)
        out.append(
            meta.model_copy(
                update={
                    "status": status,
                    "status_text": text,
                    "required_classes": required,
                    "params": [
                        p.model_copy(update={"default": values[p.key]}) for p in meta.params
                    ],
                }
            )
        )
    return out
