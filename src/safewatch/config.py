"""Settings (tech.md 6.6): switches and secrets from .env, everything else from config/*.yaml."""

from functools import cache
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from safewatch.types import BackendName, Level, ZoneGeometry

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"


class _Section(BaseModel):
    # A typo in a yaml key stops the start instead of silently using a default.
    model_config = ConfigDict(extra="forbid")


class ServerConfig(_Section):
    host: str
    port: int
    static_dir: Path


class UploadConfig(_Section):
    max_mb: int
    extensions: list[str]


class PipelineConfig(_Section):
    target_analysis_fps: float
    min_analysis_fps: float
    detector: str
    pose: str | None
    extra: list[str]

    @model_validator(mode="after")
    def _fps_floor(self) -> "PipelineConfig":
        if self.target_analysis_fps < self.min_analysis_fps:
            raise ValueError("pipeline.target_analysis_fps is below pipeline.min_analysis_fps")
        return self


class TrackerConfig(_Section):
    high_thresh: float
    low_thresh: float
    new_track_thresh: float
    min_iou: float
    max_lost_s: float
    min_hits: int


class PoseConfig(_Section):
    match_iou: float
    kpt_conf: float


class FeaturesConfig(_Section):
    ref_window_s: float
    upright_hw: float
    lying_wh: float
    upright_torso_deg: float
    lying_torso_deg: float
    speed_window_s: float
    speed_min_samples: int
    speed_max_gap_s: float
    still_motion_bh: float
    still_after_s: float
    min_person_px: float


class EpisodesConfig(_Section):
    candidate_gap_s: float
    end_after_s: float
    lost_timeout_s: float
    merge_dist_bh: float


class ScenariosConfig(_Section):
    running: dict[str, float]
    proximity: dict[str, float]
    phone: dict[str, float]
    fall: dict[str, float]
    fence_crossing: dict[str, float]
    restricted_under: dict[str, float]
    fire_smoking: dict[str, float]
    no_harness: dict[str, float]
    suspended_load: dict[str, float]
    load_carrying: dict[str, float]


class ZoneKindConfig(_Section):
    id: str
    title: str
    color: str
    geometry: ZoneGeometry
    description: str


class EscalationConfig(_Section):
    enabled: bool
    timeout_s: float
    tick_ms: int


class BroadcastConfig(_Section):
    tick_ms: int
    loop_default: bool
    autostart: bool


class FeedConfig(_Section):
    limit: int
    recent_closed_min: float


class ObservabilityConfig(_Section):
    stale_after_ms: int
    sample_s: float
    dark_mean: float
    obstructed_std: float
    min_duration_s: float


class EvidenceConfig(_Section):
    jpeg_quality: int
    max_width: int


class PreviewConfig(_Section):
    cache_s: float
    max_width: int


class HudConfig(_Section):
    window_max_ms: int


class JobsConfig(_Section):
    max_attempts: int
    retry_backoff_s: list[float]
    idle_poll_ms: int
    list_max: int


class LinqConfig(_Section):
    tools_dir: Path
    remote_dir: str
    file_prefix: str
    programs_dir: str
    inflight: int
    poll_interval_s: float
    job_timeout_s: float
    call_timeout_s: float
    check_cache_s: float


class LocalConfig(_Section):
    threads: int


class ShiftConfig(_Section):
    id: str
    title: str
    start: str
    end: str


class StatsConfig(_Section):
    default_days: int
    weeks_default: int
    trend_weeks: int


class JournalConfig(_Section):
    page_max: int
    export_max_rows: int


class MasterConfig(_Section):
    recent_resolved: int


class WebhookConfig(_Section):
    name: str
    url: str
    levels: list[Level]
    timeout_s: float

    @model_validator(mode="after")
    def _http_url(self) -> "WebhookConfig":
        # A bad URL fails at load, not in every delivery flush and system_view (R15).
        try:
            parts = urlsplit(self.url)
            ok = parts.scheme in ("http", "https") and bool(parts.hostname)
            _ = parts.port  # ValueError on a port out of range
        except ValueError:
            ok = False
        if not ok:
            raise ValueError(f"delivery.webhooks: {self.name}: url must be http(s)://host")
        return self


class DeliveryConfig(_Section):
    webhooks: list[WebhookConfig]


class EvalConfig(_Section):
    deadline_s: float


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    # From .env or the environment: switches and secrets, all with defaults.
    inference_backend: BackendName = Field(default="linq", validation_alias="INFERENCE_BACKEND")
    fake: bool = Field(default=False, validation_alias="SAFEWATCH_FAKE")
    linq_jupyter_url: str = ""
    linq_jupyter_user: str = ""
    linq_jupyter_password: str = ""
    linq_jupyter_token: str = ""

    # From config/*.yaml: required sections.
    product_name: str
    data_dir: Path
    timezone: str
    server: ServerConfig
    upload: UploadConfig
    pipeline: PipelineConfig
    class_conf: dict[str, float]
    tracker: TrackerConfig
    pose: PoseConfig
    features: FeaturesConfig
    episodes: EpisodesConfig
    scenarios: ScenariosConfig
    zone_kinds: list[ZoneKindConfig]
    escalation: EscalationConfig
    broadcast: BroadcastConfig
    feed: FeedConfig
    observability: ObservabilityConfig
    evidence: EvidenceConfig
    preview: PreviewConfig
    hud: HudConfig
    jobs: JobsConfig
    linq: LinqConfig
    local: LocalConfig
    shifts: list[ShiftConfig]
    stats: StatsConfig
    journal: JournalConfig
    master: MasterConfig
    delivery: DeliveryConfig
    eval: EvalConfig

    @model_validator(mode="after")
    def _resolve_paths(self) -> "Settings":
        if not self.data_dir.is_absolute():
            self.data_dir = ROOT / self.data_dir
        if not self.server.static_dir.is_absolute():
            self.server.static_dir = ROOT / self.server.static_dir
        if not self.linq.tools_dir.is_absolute():
            self.linq.tools_dir = ROOT / self.linq.tools_dir
        return self


# Fields read from .env have defaults; the yaml sections are required.
ENV_KEYS = [name for name, field in Settings.model_fields.items() if not field.is_required()]
# The .env name of each such field, for doctor.
ENV_NAMES = {
    name: (field.validation_alias if isinstance(field.validation_alias, str) else name.upper())
    for name, field in Settings.model_fields.items()
    if not field.is_required()
}


def _deep_merge(base: dict[str, Any], over: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key, value in over.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or {}


@cache
def get_settings() -> Settings:
    merged: dict[str, Any] = {}
    for name in ("default.yaml", "user.example.yaml", "user.yaml"):
        merged = _deep_merge(merged, _load_yaml(CONFIG_DIR / name))
    unknown = sorted(set(merged) - {n for n in Settings.model_fields if n not in ENV_KEYS})
    if unknown:
        raise ValueError(f"config: unknown keys {', '.join(unknown)}")
    return Settings(**merged)
