"""Model registry (tech.md 6.6): config/models.yaml and the active references of `pipeline`."""

from pathlib import Path

import yaml
from pydantic import TypeAdapter

from safewatch import config
from safewatch.config import Settings
from safewatch.types import ModelSpec

MODELS_FILE = config.CONFIG_DIR / "models.yaml"


def load_models(path: Path) -> list[ModelSpec]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return TypeAdapter(list[ModelSpec]).validate_python(data.get("models", []))


def resolve(ref: str, models: list[ModelSpec] | None = None) -> ModelSpec:
    """`id@version` → its entry; an unknown reference stops the start with this text."""
    known = load_models(MODELS_FILE) if models is None else models
    for model in known:
        if f"{model.id}@{model.version}" == ref:
            return model
    raise ValueError(f"model {ref} is not in config/models.yaml")


def active_models(settings: Settings) -> list[ModelSpec]:
    models = load_models(MODELS_FILE)
    refs = [settings.pipeline.detector, settings.pipeline.pose, *settings.pipeline.extra]
    return [resolve(ref, models) for ref in refs if ref]


def active_classes(settings: Settings) -> list[str]:
    names: list[str] = []
    for model in active_models(settings):
        names.extend(name for name in model.classes.values() if name not in names)
    return names
