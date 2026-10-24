"""Facade (tech.md 6.2): the one entry point for API, CLI, worker and tests.

Functions of slices that are not built yet raise `NotImplementedError("slice N")`; the API
answers them with 501 `not_implemented`.
"""

import asyncio
import bisect
import csv
import hashlib
import io
import itertools
import json
import logging
import math
import shutil
import sqlite3
import time
import uuid
from collections import Counter
from collections.abc import AsyncIterator, Iterable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, get_args

import numpy as np
import yaml
from pydantic import BaseModel, ValidationError

from safewatch import (
    clock,
    config,
    delivery,
    demo,
    evaluate,
    media,
    registry,
    rules,
    seed,
    store,
    texts,
)
from safewatch.analysis import geometry, pipeline
from safewatch.errors import (
    Conflict,
    Forbidden,
    InferenceError,
    NotFound,
    RoleRequired,
    TooLarge,
    UnsupportedVideo,
    ValidationFailed,
)
from safewatch.hub import hub
from safewatch.inference import artifacts, make_backend
from safewatch.texts import VIDEOS_DIR_MISSING
from safewatch.types import (
    ActionIn,
    Analysis,
    AnalysisConfig,
    AnalysisResult,
    BackendName,
    BackendStatus,
    Broadcast,
    BroadcastIn,
    CalculatorDefaults,
    Calibration,
    CalibrationIn,
    Camera,
    CameraIn,
    CameraLiveView,
    CameraPassport,
    CameraPatch,
    CameraRule,
    CameraRuleIn,
    CamerasAdminView,
    CameraSetupView,
    CameraState,
    CameraStateKind,
    CameraTile,
    Channel,
    Clip,
    CountRow,
    DatasetView,
    DayRow,
    Delivery,
    DeliveryKind,
    DemoArtifact,
    DemoCamera,
    DemoImportReport,
    DemoLayout,
    DemoManifest,
    DemoPack,
    DemoVideo,
    Episode,
    EpisodeDraft,
    EvalLabels,
    EvalMetrics,
    EvalReport,
    EventAction,
    EventDetail,
    EventFilter,
    EventPage,
    EventStatus,
    EventSummary,
    Evidence,
    FacetItem,
    Health,
    HudFrame,
    HumanAction,
    IdentityIn,
    InferenceBackend,
    InferenceMetrics,
    Job,
    JobErrorCode,
    JobKind,
    JobStage,
    JobStatus,
    JournalFacets,
    LatencyStats,
    Level,
    LevelMeta,
    LogAction,
    ManagementStats,
    MasterInbox,
    Meta,
    ModelSpec,
    ModelsView,
    NoObservationReason,
    Notification,
    ObservabilityGap,
    OhsStats,
    OperatorDashboard,
    PeopleStats,
    Percentiles,
    Point,
    Provenance,
    RateRow,
    Role,
    RoleMeta,
    RolloutIn,
    RolloutResult,
    RulesScreenRow,
    RulesScreenView,
    ScaleIn,
    ScaleResult,
    ScenarioMeta,
    Sector,
    SectorIn,
    SectorState,
    SectorView,
    SeedReport,
    ShiftSummary,
    StatusMeta,
    SystemView,
    TracksWindow,
    TrendSummary,
    UploadResult,
    Verdict,
    Video,
    WeekRow,
    WhyItem,
    WsType,
    Zone,
    ZoneIn,
    ZoneKindMeta,
    ZonePatch,
)

log = logging.getLogger(__name__)

ACTOR_MAX = 60
ERROR_TEXT_MAX = 500  # jobs.error_text, tech.md 5.1
RETRYABLE: frozenset[JobErrorCode] = frozenset({"linq_unavailable", "timeout", "remote_error"})
NAME_MAX = 80
DESCRIPTION_MAX = 300

# Rights table of tech.md 6.2: human actions on events per role.
ROLE_ACTIONS: dict[Role, list[HumanAction]] = {
    "operator": ["view", "confirm", "false_alarm", "send_to_master"],
    "master": ["accept", "resolve"],
    "ohs": [],
    "management": [],
    "admin": [],
}
TERMINAL_STATUSES: frozenset[EventStatus] = frozenset(
    {"false_alarm", "resolved", "auto_finished", "superseded"}
)  # tech.md 8.6
LEVEL_COLORS: dict[Level, str] = {"yellow": "#FFC400", "red": "#FF3B30"}  # theme of tech.md 8.14

RECENT_JOBS = 20  # finished jobs on the IT screen (slice 3)

Source = tuple[BackendName, bool]  # backend and fake of a job or an artifact (tech.md 8.19)

# Lazy: made from the settings on the first job; the `conn` fixture resets it.
_backend: InferenceBackend | None = None
# The last real backend check: backend_check serves it for linq.check_cache_s.
_backend_status: BackendStatus | None = None


def health() -> Health:
    from safewatch.api import CONTRACT_VERSION  # api imports this module at the top

    return Health(status="ok", contract=CONTRACT_VERSION)


def seed_demo(videos_dir: Path | None = None) -> SeedReport:
    if videos_dir is not None and not videos_dir.is_dir():
        raise NotFound(VIDEOS_DIR_MISSING.format(path=videos_dir))
    report = seed.seed_demo()
    if videos_dir is not None and not report.skipped:
        cameras = seed.demo_camera_ids()
        files = sorted(p for p in videos_dir.iterdir() if p.is_file())
        for n, path in enumerate(files):
            video_import(cameras[n % len(cameras)], path)
        report = report.model_copy(update={"videos": len(files)})
    return report


def _require(role: Role | None, allowed: tuple[Role, ...]) -> None:
    if role is None:
        raise RoleRequired(texts.ROLE_REQUIRED)
    if role not in allowed:
        raise Forbidden(texts.FORBIDDEN_ROLE, role=role)


def meta() -> Meta:
    from safewatch.api import CONTRACT_VERSION  # api imports this module at the top

    settings = config.get_settings()
    return Meta(
        product_name=settings.product_name,
        contract=CONTRACT_VERSION,
        inference_backend=settings.inference_backend,
        fake=settings.fake,
        timezone=settings.timezone,
        roles=[
            RoleMeta(id=role, title=texts.ROLE_TITLES[role], actions=ROLE_ACTIONS[role])
            for role in get_args(Role)
        ],
        levels=[
            LevelMeta(id=level, title=texts.LEVEL_TITLES[level], color=LEVEL_COLORS[level])
            for level in get_args(Level)
        ],
        statuses=[
            StatusMeta(id=s, title=texts.STATUS_TITLES[s], terminal=s in TERMINAL_STATUSES)
            for s in get_args(EventStatus)
        ],
        zone_kinds=[ZoneKindMeta.model_validate(k.model_dump()) for k in settings.zone_kinds],
        scenarios=rules.scenario_metas(),
    )


def _sector(row: sqlite3.Row) -> Sector:
    return Sector(
        id=row["id"], name=row["name"], sort_order=row["sort_order"], is_demo=bool(row["is_demo"])
    )


def _camera(row: sqlite3.Row) -> Camera:
    return Camera(
        id=row["id"],
        sector_id=row["sector_id"],
        name=row["name"],
        description=row["description"],
        is_demo=bool(row["is_demo"]),
        has_calibration=bool(row["has_calibration"]),
        zones_count=row["zones_count"],
        videos_count=row["videos_count"],
    )


def _name(value: str) -> str:
    name = value.strip()
    if not 1 <= len(name) <= NAME_MAX:
        raise ValidationFailed(texts.NAME_INVALID, field="name")
    return name


def _description(value: str) -> str:
    if len(value) > DESCRIPTION_MAX:
        raise ValidationFailed(texts.DESCRIPTION_INVALID, field="description")
    return value


def _sector_row(sector_id: int) -> sqlite3.Row:
    row = store.sector(sector_id)
    if row is None:
        raise NotFound(texts.SECTOR_NOT_FOUND, sector_id=sector_id)
    return row


def _sector_exists_for_camera(sector_id: int) -> None:
    # A missing sector in a camera body is bad input (422), not a missing resource (404).
    if store.sector(sector_id) is None:
        raise ValidationFailed(texts.SECTOR_NOT_FOUND, field="sector_id")


def cameras_admin_view() -> CamerasAdminView:
    return CamerasAdminView(sectors=sectors_list(), cameras=cameras_list())


def sectors_list() -> list[Sector]:
    return [_sector(row) for row in store.sectors()]


def sector_create(data: SectorIn, role: Role | None) -> Sector:
    _require(role, ("admin",))
    name = _name(data.name)
    with store.tx():
        if store.sector_name_taken(name):
            raise Conflict("name_taken", texts.SECTOR_NAME_TAKEN, field="name")
        values = {"name": name, "sort_order": data.sort_order, "created_at": clock.iso(clock.now())}
        sector_id = store.insert("sectors", values)
    return _sector(_sector_row(sector_id))


def sector_update(sector_id: int, data: SectorIn, role: Role | None) -> Sector:
    _require(role, ("admin",))
    name = _name(data.name)
    with store.tx():
        _sector_row(sector_id)
        if store.sector_name_taken(name, except_id=sector_id):
            raise Conflict("name_taken", texts.SECTOR_NAME_TAKEN, field="name")
        store.sector_update(sector_id, name, data.sort_order)
    return _sector(_sector_row(sector_id))


def sector_delete(sector_id: int, role: Role | None) -> None:
    _require(role, ("admin",))
    with store.tx():
        _sector_row(sector_id)
        if store.sector_has_cameras(sector_id):
            raise Conflict("sector_not_empty", texts.SECTOR_NOT_EMPTY)
        try:
            store.sector_delete(sector_id)
        except sqlite3.IntegrityError:
            # Deleted cameras and events keep pointing at the sector (journal history).
            raise Conflict("sector_not_empty", texts.SECTOR_HAS_HISTORY) from None


def cameras_list(sector_id: int | None = None) -> list[Camera]:
    if sector_id is not None:
        _sector_row(sector_id)
    return [_camera(row) for row in store.cameras(sector_id)]


def camera_get(camera_id: int) -> Camera:
    row = store.camera(camera_id)
    if row is None:
        raise NotFound(texts.CAMERA_NOT_FOUND, camera_id=camera_id)
    return _camera(row)


def camera_create(data: CameraIn, role: Role | None) -> Camera:
    _require(role, ("admin",))
    values = {
        "sector_id": data.sector_id,
        "name": _name(data.name),
        "description": _description(data.description),
        "created_at": clock.iso(clock.now()),
    }
    with store.tx():
        _sector_exists_for_camera(data.sector_id)
        camera_id = store.insert("cameras", values)
    return camera_get(camera_id)


def camera_update(camera_id: int, data: CameraPatch, role: Role | None) -> Camera:
    _require(role, ("admin",))
    values = data.model_dump(exclude_none=True)
    if "name" in values:
        values["name"] = _name(values["name"])
    if "description" in values:
        values["description"] = _description(values["description"])
    with store.tx():
        camera_get(camera_id)
        if "sector_id" in values:
            _sector_exists_for_camera(values["sector_id"])
        if values:
            store.camera_update(camera_id, values)
    return camera_get(camera_id)


def camera_delete(camera_id: int, role: Role | None) -> None:
    _require(role, ("admin",))
    with store.tx():
        camera_get(camera_id)
        playing = store.camera_broadcast(camera_id)
        store.camera_delete(camera_id, clock.iso(clock.now()))
    if playing is not None and playing["status"] == "playing":
        hub.publish("broadcast.state", _broadcast_by_id(playing["id"]))


def _extension(filename: str) -> str:
    extensions = config.get_settings().upload.extensions
    ext = Path(filename).suffix.lower()
    if ext not in extensions:
        raise UnsupportedVideo(texts.VIDEO_EXTENSION.format(extensions=", ".join(extensions)))
    return ext


def _too_large() -> TooLarge:
    return TooLarge(texts.VIDEO_TOO_LARGE.format(mb=config.get_settings().upload.max_mb))


def _enqueue(video_id: int, kind: JobKind = "process", source: Source | None = None) -> int:
    """`source`: backend and fake of a demo pack (tech.md 8.19); none — the settings."""
    settings = config.get_settings()
    backend, fake = source or (settings.inference_backend, settings.fake)
    values = {
        "kind": kind,
        "video_id": video_id,
        "backend": backend,
        "fake": int(fake),
        "status": "queued",
        "stage": "queued",
        "created_at": clock.iso(clock.now()),
    }
    return store.insert("jobs", values)


def _register(
    camera_id: int,
    filename: str,
    sha256: str,
    size: int,
    probe: media.VideoProbe,
    web_path: str | None,
    source: Source | None = None,
) -> UploadResult:
    """Steps 5 and 6 of tech.md 8.1: the file already sits in `uploads/<sha256><ext>`."""
    new_job = False
    with store.tx():
        row = store.video_by_sha(camera_id, sha256)
        if row is None:
            values = {
                "camera_id": camera_id,
                "filename": filename,
                "sha256": sha256,
                "path": f"uploads/{sha256}{Path(filename).suffix.lower()}",
                "size_bytes": size,
                **probe.model_dump(),
                "browser_playable": int(probe.browser_playable),
                "web_path": web_path,
                "status": "uploaded",
                "created_at": clock.iso(clock.now()),
            }
            video_id = store.insert("videos", values)
            job_id: int | None = _enqueue(video_id, source=source)
            new_job, reused = True, False
        else:
            video_id, reused = row["id"], True
            if row["status"] == "ready":
                job_id = None
            elif row["status"] == "failed":
                job_id = _enqueue(video_id, source=source)
                store.video_update(video_id, {"status": "uploaded"})
                new_job = True
            else:
                last = store.video_last_job(video_id)
                job_id = None if last is None else last["id"]
    job = None if job_id is None else job_get(job_id)
    if new_job and job is not None:
        hub.publish("job.progress", job)
    return UploadResult(video=video_get(video_id), job=job, reused=reused)


async def video_upload(
    camera_id: int, filename: str, chunks: AsyncIterator[bytes], role: Role | None
) -> UploadResult:
    _require(role, ("admin",))
    camera_get(camera_id)
    ext = _extension(filename)
    settings = config.get_settings()
    uploads = settings.data_dir / "uploads"
    uploads.mkdir(parents=True, exist_ok=True)
    tmp = uploads / f".tmp-{uuid.uuid4().hex}"
    limit = settings.upload.max_mb * 2**20
    digest, size = hashlib.sha256(), 0
    try:
        with tmp.open("wb") as f:
            async for chunk in chunks:
                size += len(chunk)
                if size > limit:
                    raise _too_large()
                digest.update(chunk)
                f.write(chunk)
        probe = await asyncio.to_thread(media.probe_video, tmp)
        if probe is None:
            raise UnsupportedVideo(texts.VIDEO_UNREADABLE)
        sha256 = digest.hexdigest()
        target = uploads / f"{sha256}{ext}"
        if not target.exists():
            tmp.replace(target)
    finally:
        tmp.unlink(missing_ok=True)
    web_path = await asyncio.to_thread(_web_copy, target, sha256, probe)
    return _register(camera_id, filename, sha256, size, probe, web_path)


def _web_copy(src: Path, sha256: str, probe: media.VideoProbe) -> str | None:
    """`videos.web_path` of tech.md 8.20: an H.264 copy for a codec browsers do not play.
    A copy made for an earlier upload of the same file is reused."""
    cfg = config.get_settings().transcode
    if probe.browser_playable or not cfg.enabled:
        return None
    dst = src.with_name(f"{sha256}{media.WEB_SUFFIX}")
    if not dst.exists() and not media.transcode(src, dst, cfg):
        return None
    return f"uploads/{dst.name}"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def video_import(camera_id: int, path: Path) -> UploadResult:
    return _video_import(camera_id, path, None)


def _video_import(camera_id: int, path: Path, source: Source | None) -> UploadResult:
    if not path.is_file():
        raise NotFound(texts.FILE_NOT_FOUND.format(path=path))
    camera_get(camera_id)
    ext = _extension(path.name)
    settings = config.get_settings()
    size = path.stat().st_size
    if size > settings.upload.max_mb * 2**20:
        raise _too_large()
    probe = media.probe_video(path)
    if probe is None:
        raise UnsupportedVideo(texts.VIDEO_UNREADABLE)
    sha256 = _sha256(path)
    target = settings.data_dir / "uploads" / f"{sha256}{ext}"
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    web_path = _web_copy(target, sha256, probe)
    return _register(camera_id, path.name, sha256, size, probe, web_path, source)


def _video(row: sqlite3.Row) -> Video:
    web_playable = bool(row["browser_playable"]) or row["web_path"] is not None
    return Video.model_validate({**dict(row), "web_playable": web_playable})


def videos_list(camera_id: int) -> list[Video]:
    camera_get(camera_id)
    return [_video(row) for row in store.videos(camera_id)]


def _video_row(video_id: int) -> sqlite3.Row:
    row = store.video(video_id)
    if row is None:
        raise NotFound(texts.VIDEO_NOT_FOUND, video_id=video_id)
    return row


def video_get(video_id: int) -> Video:
    return _video(_video_row(video_id))


def video_file(video_id: int) -> Path:
    """The H.264 copy when there is one (tech.md 8.20), else the source."""
    row = _video_row(video_id)
    path: Path = config.get_settings().data_dir / (row["web_path"] or row["path"])
    if not path.is_file():
        raise NotFound(texts.VIDEO_NOT_FOUND, video_id=video_id)
    return path


def _job(row: sqlite3.Row) -> Job:
    metrics = []
    for prefix in ("det", "pose"):
        if row[f"{prefix}_metrics"]:
            # The artifact came from an earlier run: this attempt did not call the backend.
            cached = row["started_at"] is not None and row[f"{prefix}_created"] < row["started_at"]
            data = json.loads(row[f"{prefix}_metrics"])
            metrics.append(InferenceMetrics(**data, cached=cached))
    job = Job.model_validate({**dict(row), "metrics": metrics})
    return job.model_copy(
        update={"status_text": texts.job_status_text(job, config.get_settings().timezone)}
    )


def jobs_list(status: JobStatus | None = None, limit: int = 50) -> list[Job]:
    list_max = config.get_settings().jobs.list_max
    if not 1 <= limit <= list_max:
        raise ValidationFailed(texts.LIMIT_INVALID.format(max=list_max), field="limit")
    return [_job(row) for row in store.jobs(status, limit)]


def job_get(job_id: int) -> Job:
    row = store.job(job_id)
    if row is None:
        raise NotFound(texts.JOB_NOT_FOUND, job_id=job_id)
    return _job(row)


def analysis_step(fps: float) -> int:
    """Every `step`-th frame goes to the models (tech.md 8.1)."""
    return max(1, math.floor(fps / config.get_settings().pipeline.target_analysis_fps))


def _backend_instance() -> InferenceBackend:
    global _backend
    if _backend is None:
        _backend = make_backend(config.get_settings())
    return _backend


def _publish_job(job_id: int) -> None:
    hub.publish("job.progress", job_get(job_id))


def _progress(job_id: int, value: float) -> None:
    store.job_progress(job_id, value)
    _publish_job(job_id)


async def _infer(
    job_id: int | None,
    stage: JobStage,
    span: tuple[float, float],
    model: ModelSpec,
    video: sqlite3.Row | dict[str, Any],
    source: Source | None = None,
) -> int:
    """Artifact id of `model` on the video: from the cache or from a backend run.

    `job_id=None`: `eval_run`, no job to report the stage and progress to. `source`: backend
    and fake of the job (tech.md 8.19): its key is looked up first, a run uses the backend.
    """
    settings = config.get_settings()
    backend = _backend_instance()
    if job_id is not None:
        store.job_update(job_id, {"stage": stage})
        _progress(job_id, span[0])
    step = analysis_step(video["fps"])
    if source is not None:
        found = store.artifact(artifacts.cache_key(video["sha256"], model, step, *source))
        if found is not None and (settings.data_dir / found["path"]).is_file():
            return int(found["id"])
    key = artifacts.cache_key(video["sha256"], model, step, backend.name, settings.fake)
    rel = f"artifacts/{key}.jsonl"
    existing = store.artifact(key)
    if existing is not None and (settings.data_dir / existing["path"]).is_file():
        return int(existing["id"])
    out = settings.data_dir / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    loop = asyncio.get_running_loop()
    low, high = span

    def progress(share: float) -> None:  # backend thread: the database belongs to the loop
        if job_id is not None:
            loop.call_soon_threadsafe(_progress, job_id, low + (high - low) * share)

    path = settings.data_dir / video["path"]
    metrics = await asyncio.to_thread(
        backend.run, path, video["sha256"], model, step, out, progress
    )
    values = {
        "cache_key": key,
        "video_sha256": video["sha256"],
        "model_id": model.id,
        "model_version": model.version,
        "task": model.task,
        "input_size": model.input_size,
        "step": step,
        "backend": backend.name,
        "fake": int(settings.fake),
        "path": rel,
        "frames": metrics.frames_processed,
        "metrics_json": metrics.model_dump_json(exclude={"cached"}),
        "created_at": clock.iso(clock.now()),
    }
    with store.tx():
        if existing is not None:  # the row outlived its file: run again, keep the id
            store.artifact_update(existing["id"], values)
            return int(existing["id"])
        return store.insert("artifacts", values)


def _job_failed(job_id: int, video_id: int, attempts: int, code: JobErrorCode, text: str) -> None:
    settings = config.get_settings()
    now = clock.now()
    values: dict[str, object] = {"error_code": code, "error_text": text[:ERROR_TEXT_MAX]}
    if code in RETRYABLE and attempts < settings.jobs.max_attempts:
        backoff = settings.jobs.retry_backoff_s
        wait = backoff[min(attempts - 1, len(backoff) - 1)]
        values |= {
            "status": "retry_wait",
            "next_attempt_at": clock.iso(now + timedelta(seconds=wait)),
        }
        store.job_update(job_id, values)
    else:
        store.job_update(job_id, values | {"status": "failed", "finished_at": clock.iso(now)})
        store.video_update(video_id, {"status": "failed"})


def _analysis_files(
    det_path: Path,
    pose: tuple[ModelSpec, Path] | None,
    video_path: Path,
    cfg: AnalysisConfig,
    det_model: ModelSpec,
    hud_path: Path,
    extra: list[tuple[ModelSpec, Path]],
) -> AnalysisResult:
    """Worker thread: read the artifacts, analyze, write hud.jsonl; the database stays out."""
    det = artifacts.read_jsonl(det_path, None)
    pose_frames = None if pose is None else artifacts.read_jsonl(pose[1], None)
    pose_model = None if pose is None else pose[0]
    extra_frames = [(m, artifacts.read_jsonl(path, None)) for m, path in extra]
    result = pipeline.analyze(
        det, pose_frames, video_path, cfg, pose_model, det_model, extra_frames
    )
    hud_path.parent.mkdir(parents=True, exist_ok=True)
    lines = "".join(frame.model_dump_json() + "\n" for frame in result.hud)
    hud_path.write_text(lines, encoding="utf-8", newline="\n")
    return result


def _analysis_config(
    video: sqlite3.Row | dict[str, Any], camera_id: int | None, extra_ids: list[int]
) -> AnalysisConfig:
    """Snapshot of tech.md 8.2; no camera (`eval_run`): no calibration and zones, default rules."""
    settings = config.get_settings()
    rows = [] if camera_id is None else store.camera_rules(camera_id)
    snapshot = _rules(camera_id or 0, rows, rules.scenario_metas())
    return AnalysisConfig(
        width=video["width"],
        height=video["height"],
        fps=video["fps"],
        step=analysis_step(video["fps"]),
        duration_ms=video["duration_ms"],
        calibration=None if camera_id is None else _calibration_of(camera_id),
        zones=[] if camera_id is None else [_zone(row) for row in store.zones(camera_id)],
        rules={r.scenario: r for r in snapshot},
        class_conf=settings.class_conf,
        active_classes=registry.active_classes(settings),
        extra_artifact_ids=extra_ids,
    )


async def _analyze(
    job_id: int,
    video: sqlite3.Row,
    det: tuple[ModelSpec, int],
    pose: tuple[ModelSpec, int] | None,
    extra: list[tuple[ModelSpec, int]],
) -> tuple[list[tuple[int, EpisodeDraft]], list[HudFrame]]:
    """Stage `analysis` of tech.md 8.1: a new `analyses` version, its HUD file and episodes."""
    settings = config.get_settings()
    store.job_update(job_id, {"stage": "analysis"})
    _progress(job_id, 0.85)
    video_id = video["id"]
    version = store.analysis_next_version(video_id)
    rel = f"analyses/{video_id}-v{version}/hud.jsonl"
    cfg = _analysis_config(video, video["camera_id"], [artifact_id for _, artifact_id in extra])
    data = settings.data_dir
    pose_files = None if pose is None else (pose[0], data / store.artifact_path(pose[1]))
    started = time.perf_counter()
    result = await asyncio.to_thread(
        _analysis_files,
        data / store.artifact_path(det[1]),
        pose_files,
        data / video["path"],
        cfg,
        det[0],
        data / rel,
        [(m, data / store.artifact_path(artifact_id)) for m, artifact_id in extra],
    )
    values = {
        "video_id": video_id,
        "version": version,
        "det_artifact_id": det[1],
        "pose_artifact_id": None if pose is None else pose[1],
        "config_json": cfg.model_dump_json(),
        "hud_path": rel,
        "gaps_json": json.dumps([gap.model_dump() for gap in result.gaps]),
        "duration_ms": video["duration_ms"],
        "created_at": clock.iso(clock.now()),
    }
    with store.tx():
        analysis_id = store.insert("analyses", values)
        episodes = []
        for draft in result.episodes:
            row = draft.model_dump(exclude={"metrics", "confirm_frame_idx", "escalate_frame_idx"})
            row |= {"analysis_id": analysis_id, "metrics_json": json.dumps(draft.metrics)}
            episodes.append((store.insert("episodes", row), draft))
        elapsed = round((time.perf_counter() - started) * 1000)
        store.job_update(job_id, {"analysis_id": analysis_id, "analysis_ms": elapsed})
        store.video_update(video_id, {"active_analysis_id": analysis_id})
    return episodes, result.hud


def _evidence_files(
    video_path: Path, shots: list[tuple[int, Path]], quality: int, width: int
) -> list[str]:
    """Worker thread: JPEG of each (frame_idx, file); sha256 of every file written."""
    digests = []
    for frame_idx, path in shots:
        data = media.encode_jpeg(media.read_frame(video_path, frame_idx), quality, width)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        digests.append(hashlib.sha256(data).hexdigest())
    return digests


async def _evidence(
    job_id: int,
    video: sqlite3.Row,
    episodes: list[tuple[int, EpisodeDraft]],
    hud: list[HudFrame],
) -> None:
    """Stage `evidence` (tech.md 8.2 item 9): the confirm and escalate frames of each episode."""
    settings = config.get_settings()
    store.job_update(job_id, {"stage": "evidence"})
    _progress(job_id, 0.95)
    shots: list[tuple[int, str, int]] = []
    for episode_id, draft in episodes:
        shots.append((episode_id, "confirm", draft.confirm_frame_idx))
        if draft.escalate_frame_idx is not None:
            shots.append((episode_id, "escalate", draft.escalate_frame_idx))
    data = settings.data_dir
    files = [(idx, data / f"evidence/{eid}-{kind}.jpg") for eid, kind, idx in shots]
    q, width = settings.evidence.jpeg_quality, settings.evidence.max_width
    digests = await asyncio.to_thread(_evidence_files, data / video["path"], files, q, width)
    frames = {f.frame_idx: f for f in hud}
    with store.tx():
        for (episode_id, kind, frame_idx), sha256 in zip(shots, digests, strict=True):
            objects = [o.model_dump(mode="json") for o in frames[frame_idx].objects]
            values = {
                "episode_id": episode_id,
                "kind": kind,
                "frame_idx": frame_idx,
                "ts_ms": frames[frame_idx].ts_ms,
                "path": f"evidence/{episode_id}-{kind}.jpg",
                "sha256": sha256,
                "objects_json": json.dumps(objects),
            }
            store.insert("evidence", values)


def _stored_artifact(artifact_id: int) -> tuple[ModelSpec, int] | None:
    row = store.artifact_by_id(artifact_id)
    if row is None or not (config.get_settings().data_dir / row["path"]).is_file():
        return None
    return registry.resolve(f"{row['model_id']}@{row['model_version']}"), artifact_id


def _analysis_inputs(
    video: sqlite3.Row,
) -> tuple[tuple[ModelSpec, int], tuple[ModelSpec, int] | None, list[tuple[ModelSpec, int]]] | None:
    """Artifacts of the active analysis for a recompute; `None` when a file is gone."""
    analysis = store.analysis(video["active_analysis_id"] or 0)
    if analysis is None:
        return None
    det = _stored_artifact(analysis["det_artifact_id"])
    pose_id = analysis["pose_artifact_id"]
    pose = None if pose_id is None else _stored_artifact(pose_id)
    if det is None or (pose_id is not None and pose is None):
        return None
    ids = AnalysisConfig.model_validate_json(analysis["config_json"]).extra_artifact_ids
    extra = [_stored_artifact(artifact_id) for artifact_id in ids]
    found = [item for item in extra if item is not None]
    return None if len(found) < len(ids) else (det, pose, found)


async def run_next_job() -> Job | None:
    settings = config.get_settings()
    now = clock.now()
    with store.tx():
        row = store.next_job(clock.iso(now))
        if row is None:
            return None
        job_id, video_id, attempts = row["id"], row["video_id"], row["attempts"] + 1
        start = {"status": "running", "attempts": attempts, "started_at": clock.iso(now)}
        store.job_update(job_id, start | {"next_attempt_at": None, "error_code": None})
        store.video_update(video_id, {"status": "processing"})
    pose_text = None
    try:
        video = _video_row(video_id)
        pose: tuple[ModelSpec, int] | None = None
        extra: list[tuple[ModelSpec, int]] = []
        if row["kind"] == "recompute":  # the same artifacts, no inference (tech.md 8.12)
            inputs = _analysis_inputs(video)
            if inputs is None:
                raise InferenceError("artifacts_missing", texts.ARTIFACTS_MISSING)
            (detector, det_id), pose, extra = inputs
            pose_id = None if pose is None else pose[1]
            store.job_update(job_id, {"det_artifact_id": det_id, "pose_artifact_id": pose_id})
        else:
            src: Source = (row["backend"], bool(row["fake"]))
            detector = registry.resolve(settings.pipeline.detector)
            span = (0.0, 0.45)
            det_id = await _infer(job_id, "inference_detect", span, detector, video, src)
            store.job_update(job_id, {"det_artifact_id": det_id})
            for ref in settings.pipeline.extra:  # own classes, --nc (tech.md 6.1)
                model = registry.resolve(ref)
                span = (0.45, 0.45)
                artifact_id = await _infer(job_id, "inference_detect", span, model, video, src)
                extra.append((model, artifact_id))
            try:
                if settings.pipeline.pose is not None:
                    pose_model = registry.resolve(settings.pipeline.pose)
                    span = (0.45, 0.85)
                    stage: JobStage = "inference_pose"
                    pose_id = await _infer(job_id, stage, span, pose_model, video, src)
                    store.job_update(job_id, {"pose_artifact_id": pose_id})
                    pose = (pose_model, pose_id)
            except InferenceError as exc:
                if exc.code not in ("remote_error", "bad_output"):
                    raise
                pose_text = f"pose: {exc.message}"  # the analysis goes on without keypoints
        episodes, hud_frames = await _analyze(job_id, video, (detector, det_id), pose, extra)
        await _evidence(job_id, video, episodes, hud_frames)
    except InferenceError as exc:
        log.warning("linq: %s %s", exc.code, exc.message)
        _job_failed(job_id, video_id, attempts, exc.code, exc.message)
    except Exception as exc:
        log.exception("job %s failed", job_id)
        _job_failed(job_id, video_id, attempts, "internal", (str(exc).splitlines() or ["error"])[0])
    else:
        done = {"status": "done", "stage": "done", "progress": 1.0, "error_text": pose_text}
        with store.tx():
            store.job_update(job_id, done | {"finished_at": clock.iso(clock.now())})
            store.video_update(video_id, {"status": "ready"})
            superseded: list[int] = []
            if row["kind"] == "process":
                restarted = [b for b in [_autostart(video)] if b is not None]
            else:
                superseded, restarted = _recomputed(video_id)
        for event_id in superseded:
            hub.publish("event.updated", _event_summary(event_id))
        for broadcast_id in restarted:
            hub.publish("broadcast.state", _broadcast_by_id(broadcast_id))
    _publish_job(job_id)
    return job_get(job_id)


def _recomputed(video_id: int) -> tuple[list[int], list[int]]:
    """Steps 1 and 3 of tech.md 8.12: superseded event ids, the stopped and started broadcast."""
    fresh = store.video(video_id)
    analysis = None if fresh is None else store.analysis(fresh["active_analysis_id"])
    assert fresh is not None and analysis is not None  # set by _analyze
    comment = texts.RECOMPUTE_COMMENT.format(n=analysis["version"])
    superseded = []
    for e in store.supersedable_events(video_id, analysis["id"]):
        store.event_update(e["id"], {"status": "superseded"})
        _system_action(e["id"], "superseded", e["status"], "superseded", comment)
        superseded.append(int(e["id"]))
    current = store.camera_broadcast(fresh["camera_id"])
    if current is None or current["status"] != "playing" or current["video_id"] != video_id:
        return superseded, []
    stopped = _stop_playing(fresh["camera_id"])
    assert stopped is not None  # it was playing
    return superseded, [stopped, _broadcast_insert(fresh, bool(current["loop"]))]


def _autostart(video: sqlite3.Row) -> int | None:
    """Broadcast of a freshly processed video when the camera has none playing (tech.md 8.5)."""
    settings = config.get_settings()
    current = store.camera_broadcast(video["camera_id"])
    if not settings.broadcast.autostart or (current is not None and current["status"] == "playing"):
        return None
    fresh = store.video(video["id"])
    assert fresh is not None and fresh["active_analysis_id"] is not None  # set by _analyze
    return _broadcast_insert(fresh, settings.broadcast.loop_default)


def camera_setup_view(camera_id: int) -> CameraSetupView:
    return CameraSetupView(
        camera=camera_get(camera_id),
        videos=videos_list(camera_id),
        jobs=[_job(row) for row in store.camera_jobs(camera_id)],
        calibration=calibration_get(camera_id),
        zones=zones_list(camera_id),
        rules=camera_rules(camera_id),
        broadcast=broadcast_get(camera_id),
    )


def job_retry(job_id: int, role: Role | None) -> Job:
    _require(role, ("admin",))
    with store.tx():
        row = store.job(job_id)
        if row is None:
            raise NotFound(texts.JOB_NOT_FOUND, job_id=job_id)
        if row["status"] != "failed":
            raise Conflict("job_not_failed", texts.JOB_NOT_FAILED)
        fresh = {"status": "queued", "stage": "queued", "progress": 0.0, "attempts": 0}
        cleared = {"next_attempt_at": None, "error_code": None, "error_text": None}
        store.job_update(job_id, fresh | cleared | {"finished_at": None})
        store.video_update(row["video_id"], {"status": "uploaded"})
    _publish_job(job_id)
    return job_get(job_id)


def recover_jobs() -> int:
    """A job left `running` by a stopped server goes back to the queue."""
    with store.tx():
        return store.jobs_recover()


def _unchecked() -> BackendStatus:
    settings = config.get_settings()
    return BackendStatus(
        backend=settings.inference_backend,
        fake=settings.fake,
        state="unchecked",
        checked_at=None,
        latency_ms=None,
        present=[],
        missing=[],
        message=texts.BACKEND_UNCHECKED,
    )


async def backend_check(force: bool = False) -> BackendStatus:
    global _backend_status
    last = _backend_status
    fresh_s = config.get_settings().linq.check_cache_s
    if not force and last is not None and last.checked_at is not None:
        if clock.now() - last.checked_at < timedelta(seconds=fresh_s):
            return last
    status = await asyncio.to_thread(_backend_instance().check)
    _backend_status = status
    hub.publish("backend.status", status)
    return status


def models_view() -> ModelsView:
    settings = config.get_settings()
    return ModelsView(
        backend=settings.inference_backend,
        fake=settings.fake,
        active=registry.active_models(settings),
        available=registry.load_models(registry.MODELS_FILE),
    )


def system_view() -> SystemView:
    settings = config.get_settings()
    return SystemView(
        backend=settings.inference_backend,
        fake=settings.fake,
        backend_status=_backend_status or _unchecked(),
        queue=[_job(row) for row in store.queue_jobs()],
        recent_jobs=[_job(row) for row in store.finished_jobs(RECENT_JOBS)],
        cameras=camera_states(),
        models=registry.active_models(settings),
        latency=_latency(),
        channels=[
            Channel(name=w.name, kind="webhook", target=delivery.target(w.url), levels=w.levels)
            for w in settings.delivery.webhooks
        ],
        server_now=clock.now(),
    )


def _latency() -> LatencyStats:
    """Every broadcast event: `published_at − started_at`, s, and lag behind the planned confirm."""
    delay, lag = [], []
    for r in store.publish_latencies():
        started, published = clock.parse(r["started_at"]), clock.parse(r["published_at"])
        planned = started + timedelta(milliseconds=r["confirm_ms"] - r["video_start_ms"])
        delay.append((published - started).total_seconds())
        lag.append((published - planned) / timedelta(milliseconds=1))
    return LatencyStats(notify_delay_s=_percentiles(delay, 0), publish_lag_ms=_percentiles(lag, 0))


def video_tracks(video_id: int, from_ms: int, to_ms: int) -> TracksWindow:
    video = _video_row(video_id)
    window_max = config.get_settings().hud.window_max_ms
    if from_ms >= to_ms or to_ms - from_ms > window_max:
        raise ValidationFailed(texts.TRACKS_WINDOW_INVALID.format(max=window_max), field="to_ms")
    analysis_id = video["active_analysis_id"]
    row = None if analysis_id is None else store.analysis(analysis_id)
    if row is None:
        raise Conflict("video_not_ready", texts.VIDEO_NOT_READY)
    path = config.get_settings().data_dir / row["hud_path"]
    with path.open(encoding="utf-8") as f:
        frames = [HudFrame.model_validate_json(line) for line in f]
    window = [frame for frame in frames if from_ms <= frame.ts_ms < to_ms]
    return TracksWindow(
        video_id=video_id, analysis_id=analysis_id, from_ms=from_ms, to_ms=to_ms, frames=window
    )


def _evidence_item(e: sqlite3.Row) -> Evidence:
    return Evidence(
        id=e["id"],
        kind=e["kind"],
        frame_idx=e["frame_idx"],
        ts_ms=e["ts_ms"],
        url=f"/api/evidence/{e['id']}/image",
        sha256=e["sha256"],
        objects=json.loads(e["objects_json"]),
    )


def _episode(ep: sqlite3.Row, evidence: list[Evidence]) -> Episode:
    return Episode.model_validate(
        {
            **dict(ep),
            "scenario_title": texts.SCENARIO_TITLES[ep["scenario"]],
            "metrics": json.loads(ep["metrics_json"]),
            "evidence": evidence,
        }
    )


def video_analysis(video_id: int) -> Analysis:
    video = _video_row(video_id)
    row = store.analysis(video["active_analysis_id"] or 0)
    if row is None:
        raise Conflict("video_not_ready", texts.VIDEO_NOT_READY)
    evidence: dict[int, list[Evidence]] = {}
    for e in store.analysis_evidence(row["id"]):
        evidence.setdefault(e["episode_id"], []).append(_evidence_item(e))
    episodes = [_episode(ep, evidence.get(ep["id"], [])) for ep in store.episodes(row["id"])]
    return Analysis(
        id=row["id"],
        video_id=video_id,
        version=row["version"],
        created_at=clock.parse(row["created_at"]),
        duration_ms=row["duration_ms"],
        pose_used=row["pose_artifact_id"] is not None,
        episodes=episodes,
        gaps=json.loads(row["gaps_json"]),
    )


def video_recompute(video_id: int, role: Role | None) -> Job:
    _require(role, ("admin", "ohs"))
    with store.tx():
        video = _video_row(video_id)
        if video["status"] != "ready" or video["active_analysis_id"] is None:
            raise Conflict("video_not_ready", texts.VIDEO_NOT_READY)
        if _analysis_inputs(video) is None:
            raise Conflict("artifacts_missing", texts.ARTIFACTS_MISSING)
        last = store.video_last_job(video_id)
        if last is not None and (last["kind"], last["status"]) == ("recompute", "queued"):
            return job_get(last["id"])  # repeated clicks share the queued job
        job_id = _enqueue(video_id, "recompute")
    _publish_job(job_id)
    return job_get(job_id)


def evidence_file(evidence_id: int) -> Path:
    row = store.evidence(evidence_id)
    path: Path | None = None if row is None else config.get_settings().data_dir / row["path"]
    if path is None or not path.is_file():
        raise NotFound(texts.EVIDENCE_NOT_FOUND, evidence_id=evidence_id)
    return path


def _broadcast(row: sqlite3.Row) -> Broadcast:
    return Broadcast(
        id=row["id"],
        camera_id=row["camera_id"],
        video_id=row["video_id"],
        analysis_id=row["analysis_id"],
        status=row["status"],
        loop=bool(row["loop"]),
        cycle=row["cycle"],
        started_at=clock.parse(row["started_at"]),
        position_ms=row["position_ms"],
        duration_ms=row["duration_ms"],
        server_now=clock.now(),
    )


def _broadcast_by_id(broadcast_id: int) -> Broadcast:
    row = store.broadcast(broadcast_id)
    assert row is not None  # the caller just wrote it
    return _broadcast(row)


def _broadcast_insert(video: sqlite3.Row, loop: bool) -> int:
    values = {
        "camera_id": video["camera_id"],
        "video_id": video["id"],
        "analysis_id": video["active_analysis_id"],
        "started_at": clock.iso(clock.now()),
        "loop": int(loop),
        "status": "playing",
    }
    return store.insert("broadcasts", values)


def _stop_playing(camera_id: int) -> int | None:
    """Stop the playing broadcast of the camera; its id, or None when nothing played."""
    row = store.camera_broadcast(camera_id)
    if row is None or row["status"] != "playing":
        return None
    store.broadcast_update(row["id"], {"status": "stopped", "stopped_at": clock.iso(clock.now())})
    return int(row["id"])


def broadcast_get(camera_id: int) -> Broadcast | None:
    camera_get(camera_id)
    row = store.camera_broadcast(camera_id)
    return None if row is None else _broadcast(row)


def broadcast_start(camera_id: int, data: BroadcastIn, role: Role | None) -> Broadcast:
    _require(role, ("admin",))
    with store.tx():
        camera_get(camera_id)
        if data.video_id is None:
            video = store.last_ready_video(camera_id)
            if video is None:
                raise Conflict("no_ready_video", texts.NO_READY_VIDEO)
        else:
            video = store.video(data.video_id)
            if video is None or video["camera_id"] != camera_id:
                raise NotFound(texts.VIDEO_NOT_FOUND, video_id=data.video_id)
            if video["status"] != "ready" or video["active_analysis_id"] is None:
                raise Conflict("video_not_ready", texts.VIDEO_NOT_READY)
        stopped = _stop_playing(camera_id)
        loop = config.get_settings().broadcast.loop_default if data.loop is None else data.loop
        broadcast_id = _broadcast_insert(video, loop)
    if stopped is not None:
        hub.publish("broadcast.state", _broadcast_by_id(stopped))
    started = _broadcast_by_id(broadcast_id)
    hub.publish("broadcast.state", started)
    return started


def broadcast_stop(camera_id: int, role: Role | None) -> None:
    _require(role, ("admin",))
    with store.tx():
        camera_get(camera_id)
        stopped = _stop_playing(camera_id)
    if stopped is not None:
        hub.publish("broadcast.state", _broadcast_by_id(stopped))


# The states published last: camera.state and sector.state go out only on a change.
_camera_seen: dict[int, CameraState] = {}
_sector_seen: dict[int, SectorState] = {}
# Camera id -> (made at, JPEG): preview frames live for preview.cache_s.
_preview_cache: dict[int, tuple[datetime, bytes]] = {}
# Frame times of an analysis for `freshness_ms`; an analysis never changes once written.
_frames_ts: dict[int, list[int]] = {}
# (event id, kind) waiting for `deliveries_flush`: the broadcast tick and actions add to it.
_deliveries: list[tuple[int, DeliveryKind]] = []

Message = tuple[WsType, BaseModel, list[Role] | None]


# Event priority of tech.md 8.8: red waiting for the operator, yellow waiting, other open, closed.
PRIORITY = {"red_pending": 3, "yellow_pending": 2, "open": 1, "terminal": 0}


def _priority(level: Level, status: EventStatus) -> int:
    if status in TERMINAL_STATUSES:
        return PRIORITY["terminal"]
    if status in ("new", "viewed"):
        return PRIORITY[f"{level}_pending"]
    return PRIORITY["open"]


def _summary(row: sqlite3.Row) -> EventSummary:
    started = clock.parse(row["started_at"])
    end = clock.parse(row["ended_at"]) if row["ended_at"] else clock.now()
    level, escalated = row["level"], bool(row["escalated_by_timeout"])
    return EventSummary(
        id=row["id"],
        scenario=row["scenario"],
        title=row["title"],
        level=level,
        status=row["status"],
        status_title=texts.STATUS_TITLES[row["status"]],
        operator_verdict=row["operator_verdict"],
        escalated_by_timeout=escalated,
        mode="demo" if row["is_demo"] else "replay",
        camera_id=row["camera_id"],
        camera_name=row["camera_name"],
        sector_id=row["sector_id"],
        sector_name=row["sector_name"],
        zone_id=row["zone_id"],
        zone_name=row["zone_name"],
        reason_text=row["reason_text"],
        notification_text=texts.notification_text(
            level, row["sector_name"], row["reason_text"], escalated
        ),
        started_at=started,
        published_at=clock.parse(row["published_at"]),
        red_at=clock.parse(row["red_at"]) if row["red_at"] else None,
        ended_at=clock.parse(row["ended_at"]) if row["ended_at"] else None,
        duration_s=(end - started).total_seconds(),
        priority=_priority(level, row["status"]),
        is_demo=bool(row["is_demo"]),
        evidence_url=f"/api/evidence/{row['evidence_id']}/image" if row["evidence_id"] else None,
        clip=_clip(row),
    )


def _clip(row: sqlite3.Row | dict[str, Any]) -> Clip | None:
    """Window of the source video around the episode (tech.md 8.20); none for a seed event."""
    if row["clip_video_id"] is None:
        return None
    cfg = config.get_settings().clips
    start_ms = max(0, round(row["clip_start_ms"] - cfg.pre_s * 1000))
    end_ms = min(
        row["clip_duration_ms"],
        round(row["clip_confirm_ms"] + cfg.post_s * 1000),
        round(start_ms + cfg.max_s * 1000),
    )
    video_id = row["clip_video_id"]
    return Clip(
        video_id=video_id,
        url=f"/api/videos/{video_id}/file#t={start_ms / 1000:.1f},{end_ms / 1000:.1f}",
        start_ms=start_ms,
        end_ms=end_ms,
        playable=bool(row["clip_browser_playable"]) or row["clip_web_path"] is not None,
    )


def _event_summary(event_id: int) -> EventSummary:
    row = store.event(event_id)
    assert row is not None  # the caller just wrote it
    return _summary(row)


def _system_action(
    event_id: int, action: str, before: str | None, after: str, comment: str = ""
) -> None:
    values = {
        "event_id": event_id,
        "at": clock.iso(clock.now()),
        "actor_role": "system",
        "actor_name": texts.DEMO_ACTOR["system"],
        "action": action,
        "from_status": before,
        "to_status": after,
        "comment": comment,
    }
    store.insert("event_actions", values)


def _operator_alert(summary: EventSummary, kind: str) -> Notification:
    """Rows 1 and 2 of the table in tech.md 8.8: yellow chimes, red sirens and takes over."""
    red = summary.level == "red"
    return Notification(
        id=f"e{summary.id}:{kind}",
        event_id=summary.id,
        level=summary.level,
        text=summary.notification_text,
        audience=["operator"],
        sound="siren" if red else "chime",
        takeover=red,
    )


def _ms(delta: timedelta) -> int:
    return delta // timedelta(milliseconds=1)


def _play(b: sqlite3.Row, camera: sqlite3.Row, cycle: int, pos: int, out: list[Message]) -> int:
    """One cycle of a broadcast up to `pos` (tech.md 8.5); the number of actions written."""
    now = clock.now()
    base = clock.parse(b["started_at"]) + timedelta(milliseconds=cycle * b["duration_ms"])
    events = {row["episode_id"]: row for row in store.broadcast_events(b["id"], cycle)}
    written = 0
    for ep in store.episodes(b["analysis_id"]):
        if ep["confirm_ms"] > pos:
            continue
        escalated = ep["escalate_ms"] is not None and ep["escalate_ms"] <= pos
        ended = ep["end_ms"] <= pos
        row = events.get(ep["id"])
        if row is None:
            red = ep["level_initial"] == "red" or escalated
            values = {
                "pub_key": f"b{b['id']}:c{cycle}:e{ep['id']}",
                "episode_id": ep["id"],
                "broadcast_id": b["id"],
                "cycle": cycle,
                "video_id": b["video_id"],
                "camera_id": b["camera_id"],
                "sector_id": camera["sector_id"],
                "zone_id": ep["zone_id"],
                "scenario": ep["scenario"],
                "title": texts.SCENARIO_TITLES[ep["scenario"]],
                "reason_text": ep["reason_text"],
                "level": "red" if red else "yellow",
                "status": "new",
                "started_at": clock.iso(base + timedelta(milliseconds=ep["start_ms"])),
                "published_at": clock.iso(now),
                "red_at": clock.iso(now) if red else None,
                "ended_at": clock.iso(base + timedelta(milliseconds=ep["end_ms"]))
                if ended
                else None,
                "video_start_ms": ep["start_ms"],
                "video_end_ms": ep["end_ms"],
            }
            event_id = store.insert("events", values)
            _system_action(event_id, "published", None, "new")
            summary = _event_summary(event_id)
            out.append(("event.created", summary, None))
            out.append(("notification", _operator_alert(summary, "published"), ["operator"]))
            written += 1
            continue
        if row["level"] == "yellow" and escalated:
            store.event_update(row["id"], {"level": "red", "red_at": clock.iso(now)})
            _system_action(row["id"], "level_escalated", row["status"], row["status"])
            summary = _event_summary(row["id"])
            out.append(("event.escalated", summary, None))
            out.append(("notification", _operator_alert(summary, "escalated"), ["operator"]))
            if row["status"] in ("sent_to_master", "master_accepted"):  # row 4 of tech.md 8.8
                out.append(("notification", _master_alert(summary, "master_escalated"), ["master"]))
            written += 1
        if ended and row["ended_at"] is None:
            values = {"ended_at": clock.iso(base + timedelta(milliseconds=ep["end_ms"]))}
            finish = row["level"] == "yellow" and not escalated
            if finish and row["status"] in ("new", "viewed"):
                values["status"] = "auto_finished"
                _system_action(row["id"], "auto_finished", row["status"], "auto_finished")
                written += 1
            store.event_update(row["id"], values)
            out.append(("event.updated", _event_summary(row["id"]), None))
    return written


# Broadcast messages that go to the delivery channels too (slice 15).
DELIVERED: dict[WsType, DeliveryKind] = {
    "event.created": "published",
    "event.escalated": "escalated",
}


def broadcast_tick() -> int:
    """Advance every playing broadcast to the server clock; the number of actions written."""
    out: list[Message] = []
    written = 0
    now = clock.now()
    with store.tx():
        for b in store.playing_broadcasts():
            camera = store.camera(b["camera_id"])
            assert camera is not None  # a deleted camera has no playing broadcast
            duration, t = b["duration_ms"], max(0, _ms(now - clock.parse(b["started_at"])))
            cycle, pos = divmod(t, duration) if b["loop"] else (0, min(t, duration))
            if cycle > b["cycle"]:  # finish the previous cycle; cycles missed whole are skipped
                written += _play(b, camera, b["cycle"], duration, out)
            written += _play(b, camera, cycle, pos, out)
            values: dict[str, object] = {"cycle": cycle, "position_ms": pos}
            ended = not b["loop"] and t >= duration
            if ended:
                values["status"] = "ended"
            store.broadcast_update(b["id"], values)
            if ended or cycle != b["cycle"]:
                out.append(("broadcast.state", _broadcast_by_id(b["id"]), None))
        cameras = camera_states()
        sectors = _sector_states(cameras)
    for kind, data, audience in out:
        hub.publish(kind, data, audience)
        if kind in DELIVERED:  # queued after the commit: a rolled back tick sends nothing
            assert isinstance(data, EventSummary)
            _deliveries.append((data.id, DELIVERED[kind]))
    for camera_state in cameras:
        # Freshness moves on every tick; a message goes out only when the state itself changes.
        seen = camera_state.model_copy(update={"freshness_ms": None})
        if _camera_seen.get(camera_state.camera_id) != seen:
            _camera_seen[camera_state.camera_id] = seen
            hub.publish("camera.state", camera_state)
    for sector_state in sectors:
        if _sector_seen.get(sector_state.sector_id) != sector_state:
            _sector_seen[sector_state.sector_id] = sector_state
            hub.publish("sector.state", sector_state)
    return written


def _camera_state(row: sqlite3.Row) -> CameraState:
    """The first rule of tech.md 8.9 that fits."""
    reason: NoObservationReason | None = None
    pos = row["position_ms"]
    gap = None
    if row["playing"]:
        gaps = [ObservabilityGap.model_validate(g) for g in json.loads(row["gaps_json"])]
        gap = next((g for g in gaps if g.start_ms <= pos < g.end_ms), None)
    if row["open_red"]:
        state: CameraStateKind = "red"
        text = texts.LEVEL_TITLES["red"]
    elif row["yellow_live"]:
        state, text = "yellow", texts.LEVEL_TITLES["yellow"]
    elif not row["playing"]:
        state = "no_observation"
        if row["processing"]:
            reason = "processing"
        elif row["last_job"] == "failed":
            reason = "failed"
        elif row["last_broadcast"] == "ended":
            reason = "ended"
        else:
            reason = "no_source"
        text = texts.NO_OBSERVATION_TEXTS[reason]
    elif gap is not None:
        state, reason = "no_observation", gap.reason
        text = texts.NO_OBSERVATION_TEXTS[reason]
    else:
        state, text = "normal", texts.STATE_NORMAL
    return CameraState(
        camera_id=row["camera_id"],
        sector_id=row["sector_id"],
        state=state,
        reason=reason,
        reason_text=text,
        freshness_ms=_freshness(row["analysis_id"], row["hud_path"], pos)
        if row["playing"]
        else None,
        open_yellow=row["open_yellow"],
        open_red=row["open_red"],
    )


def _freshness(analysis_id: int, hud_path: str, pos: int) -> int | None:
    """Position minus `ts_ms` of the last analyzed frame not later than it (tech.md 8.9)."""
    if analysis_id not in _frames_ts:
        path = config.get_settings().data_dir / hud_path
        if not path.exists():  # a cleaned data folder must not break every camera state
            return None
        with path.open(encoding="utf-8") as f:
            _frames_ts[analysis_id] = [json.loads(line)["ts_ms"] for line in f]
    frames = _frames_ts[analysis_id]
    i = bisect.bisect_right(frames, pos)
    return pos - frames[i - 1] if i else None


def camera_states() -> list[CameraState]:
    return [_camera_state(row) for row in store.camera_state_rows()]


def _sector_state(sector: sqlite3.Row, cameras: list[CameraState]) -> SectorState:
    kinds = {c.state for c in cameras}
    blind = sum(c.state == "no_observation" for c in cameras)
    if "red" in kinds:
        state: CameraStateKind = "red"
        text = texts.LEVEL_TITLES["red"]
    elif "yellow" in kinds:
        state, text = "yellow", texts.LEVEL_TITLES["yellow"]
    elif not cameras:
        state, text = "no_observation", texts.SECTOR_EMPTY
    elif blind:
        state = "no_observation"
        text = texts.SECTOR_NO_OBSERVATION.format(n=blind, total=len(cameras))
    else:
        state, text = "normal", texts.STATE_NORMAL
    return SectorState(
        sector_id=sector["id"],
        name=sector["name"],
        state=state,
        reason_text=text,
        cameras_total=len(cameras),
        cameras_no_observation=blind,
        open_yellow=sum(c.open_yellow for c in cameras),
        open_red=sum(c.open_red for c in cameras),
    )


def _sector_states(cameras: list[CameraState]) -> list[SectorState]:
    return [
        _sector_state(s, [c for c in cameras if c.sector_id == s["id"]]) for s in store.sectors()
    ]


def _feed(sector_id: int | None = None) -> list[EventSummary]:
    settings = config.get_settings()
    closed_after = clock.now() - timedelta(minutes=settings.feed.recent_closed_min)
    items = [_summary(row) for row in store.feed(clock.iso(closed_after), sector_id)]
    items.sort(key=lambda e: (e.priority, e.published_at, e.id), reverse=True)
    return items[: settings.feed.limit]


def operator_dashboard_view() -> OperatorDashboard:
    return OperatorDashboard(
        sectors=_sector_states(camera_states()), feed=_feed(), server_now=clock.now()
    )


def operator_feed() -> list[EventSummary]:
    return _feed()


def sector_view(sector_id: int) -> SectorView:
    sector = _sector_row(sector_id)
    states = [c for c in camera_states() if c.sector_id == sector_id]
    by_id = {c.camera_id: c for c in states}
    broadcasts = {row["camera_id"]: row for row in store.latest_broadcasts()}
    tiles = []
    for camera in cameras_list(sector_id):
        row = broadcasts.get(camera.id)
        preview = f"/api/cameras/{camera.id}/preview" if camera.videos_count else None
        tiles.append(
            CameraTile(
                camera=camera,
                state=by_id[camera.id],
                broadcast=None if row is None else _broadcast(row),
                preview_url=preview,
            )
        )
    return SectorView(sector=_sector_state(sector, states), cameras=tiles, feed=_feed(sector_id))


def camera_live_view(camera_id: int) -> CameraLiveView:
    camera = camera_get(camera_id)
    broadcast = broadcast_get(camera_id)
    video_row = store.video(broadcast.video_id) if broadcast else store.last_ready_video(camera_id)
    video = None if video_row is None else _video(video_row)
    analysis = None if video is None or not video.active_analysis_id else video_analysis(video.id)
    (state,) = [c for c in camera_states() if c.camera_id == camera_id]
    return CameraLiveView(
        camera=camera,
        state=state,
        broadcast=broadcast,
        video=video,
        analysis=analysis,
        zones=zones_list(camera_id),
        calibration=calibration_get(camera_id),
    )


async def camera_preview(camera_id: int) -> bytes:
    """Frame at the broadcast position, else the first frame of the last ready video."""
    settings = config.get_settings()
    camera_get(camera_id)
    now = clock.now()
    cached = _preview_cache.get(camera_id)
    if cached is not None and now - cached[0] < timedelta(seconds=settings.preview.cache_s):
        return cached[1]
    playing = store.camera_broadcast(camera_id)
    if playing is not None and playing["status"] == "playing":
        video, pos = store.video(playing["video_id"]), playing["position_ms"]
    else:
        video, pos = store.last_ready_video(camera_id), 0
    if video is None:
        raise NotFound(texts.PREVIEW_NOT_FOUND, camera_id=camera_id)
    frame_idx = min(video["frame_count"] - 1, round(pos / 1000 * video["fps"]))
    path = settings.data_dir / video["path"]
    q, width = settings.evidence.jpeg_quality, settings.preview.max_width
    img = await asyncio.to_thread(media.read_frame, path, frame_idx)
    data = await asyncio.to_thread(media.encode_jpeg, img, q, width)
    _preview_cache[camera_id] = (now, data)
    return data


COMMENT_MAX = 500

# A step of a human action: (journal action, status after it); the event ends in the status of
# the last step, `from_status` of a step is the status after the previous one.
Step = tuple[LogAction, EventStatus]
VERDICTS: dict[HumanAction, Verdict] = {
    "confirm": "confirmed",
    "false_alarm": "false_alarm",
    "send_to_master": "confirmed",  # the operator only sends what he takes for real
}


def _steps(action: HumanAction, row: sqlite3.Row) -> list[Step] | None:
    """Human rows of the table in tech.md 8.6; None: the pair (action, status) is not there."""
    status, red = row["status"], row["level"] == "red"
    deciding = status in ("new", "viewed", "confirmed")
    # A timeout escalation leaves the operator his verdict (rows 4 and 6 of the table).
    late = (
        status == "sent_to_master"
        and bool(row["escalated_by_timeout"])
        and row["operator_verdict"] == "none"
    )
    if action == "view" and status == "new":
        return [("viewed", "viewed")]
    if action == "confirm" and red and deciding:
        return [("confirmed", "confirmed"), ("sent_to_master", "sent_to_master")]
    if action == "confirm" and not red and status in ("new", "viewed"):
        return [("confirmed", "confirmed")]
    if action == "confirm" and red and late:
        return [("confirmed", "sent_to_master")]
    if action == "false_alarm" and (deciding or late):
        return [("false_alarm", "false_alarm")]
    if action == "send_to_master" and deciding:
        return [("sent_to_master", "sent_to_master")]
    if action == "accept" and status == "sent_to_master":
        return [("master_accepted", "master_accepted")]
    if action == "resolve" and status == "master_accepted":
        return [("resolved", "resolved")]
    return None


def _event_row(event_id: int) -> sqlite3.Row:
    row = store.event(event_id)
    if row is None:
        raise NotFound(texts.EVENT_NOT_FOUND, event_id=event_id)
    return row


def _master_alert(summary: EventSummary, kind: str = "to_master") -> Notification:
    """Rows 3 and 4 of the table in tech.md 8.8: sent to the master (by the operator or by
    timeout), or turned red while with the master."""
    return Notification(
        id=f"e{summary.id}:{kind}",
        event_id=summary.id,
        level=summary.level,
        text=summary.notification_text,
        audience=["master"],
        sound="chime",
        takeover=False,
    )


def _provenance(episode: Episode) -> Provenance:
    analysis = store.analysis(episode.analysis_id)
    assert analysis is not None  # episodes belong to an analysis
    det = store.artifact_by_id(analysis["det_artifact_id"])
    pose = store.artifact_by_id(analysis["pose_artifact_id"] or 0)
    video = store.video(analysis["video_id"])
    job = store.analysis_job(analysis["id"])
    assert det is not None and video is not None
    # The rule ran with config defaults and the camera overrides of the snapshot (tech.md 8.3).
    rule = AnalysisConfig.model_validate_json(analysis["config_json"]).rules.get(episode.scenario)
    params = rules.defaults(episode.scenario) | (
        rule.effective | rule.params if rule is not None else {}
    )
    shot = next((e.sha256 for e in episode.evidence if e.kind == "confirm"), None)
    return Provenance(
        backend=det["backend"],
        fake=bool(det["fake"]),
        det_model=f"{det['model_id']}@{det['model_version']}",
        pose_model=None if pose is None else f"{pose['model_id']}@{pose['model_version']}",
        job_id=None if job is None else job["id"],
        video_sha256=video["sha256"],
        analysis_version=analysis["version"],
        rule_params=params,
        evidence_sha256=shot,
    )


def event_detail(event_id: int, role: Role | None) -> EventDetail:
    row = _event_row(event_id)
    episode: Episode | None = None
    why = [WhyItem(label=texts.WHY_REASON, value=row["reason_text"])]
    provenance = Provenance(
        backend=None,
        fake=False,
        det_model=None,
        pose_model=None,
        job_id=None,
        video_sha256=None,
        analysis_version=None,
        rule_params={},
        evidence_sha256=None,
    )
    if row["episode_id"] is not None:  # demo events have no episode
        ep = store.episode(row["episode_id"])
        assert ep is not None
        episode = _episode(ep, [_evidence_item(e) for e in store.episode_evidence(ep["id"])])
        provenance = _provenance(episode)
        frames = {e.kind: e.frame_idx for e in episode.evidence}
        draft = EpisodeDraft.model_validate(
            episode.model_dump()
            | {"confirm_frame_idx": frames["confirm"], "escalate_frame_idx": frames.get("escalate")}
        )
        why = rules.plugin(episode.scenario).explain(draft, provenance.rule_params)
    broadcast = store.camera_broadcast(row["camera_id"])
    allowed = [] if role is None else ROLE_ACTIONS[role]
    return EventDetail(
        event=_summary(row),
        episode=episode,
        why=why,
        actions=[EventAction.model_validate(dict(a)) for a in store.event_actions(event_id)],
        allowed_actions=[a for a in allowed if _steps(a, row) is not None],
        provenance=provenance,
        deliveries=[Delivery.model_validate(dict(d)) for d in store.event_deliveries(event_id)],
        video_id=row["video_id"],
        video_start_ms=row["video_start_ms"],
        video_end_ms=row["video_end_ms"],
        broadcast=None if broadcast is None else _broadcast(broadcast),
    )


def event_action(
    event_id: int, data: ActionIn, role: Role | None, actor: str | None
) -> EventDetail:
    _require(role, tuple(r for r, actions in ROLE_ACTIONS.items() if data.action in actions))
    assert role is not None  # _require raised otherwise
    if len(data.comment) > COMMENT_MAX:
        raise ValidationFailed(texts.COMMENT_TOO_LONG, field="comment")
    comment = data.comment.strip()
    if data.action == "resolve" and not comment:
        raise ValidationFailed(texts.COMMENT_REQUIRED, field="comment")
    name = texts.DEMO_ACTOR[role] if actor is None else actor.strip()
    if not 1 <= len(name) <= ACTOR_MAX:
        raise ValidationFailed(texts.ACTOR_INVALID, field="X-Actor")
    with store.tx():
        row = _event_row(event_id)
        steps = _steps(data.action, row)
        if steps is None:
            raise Conflict("invalid_transition", texts.INVALID_TRANSITION)
        status, now = row["status"], clock.iso(clock.now())
        for n, (logged, after) in enumerate(steps):
            values = {
                "event_id": event_id,
                "at": now,
                "actor_role": role,
                "actor_name": name,
                "action": logged,
                "from_status": status,
                "to_status": after,
                "comment": comment if n == 0 else "",
            }
            store.insert("event_actions", values)
            status = after
        update: dict[str, object] = {"status": status}
        if data.action in VERDICTS:
            update["operator_verdict"] = VERDICTS[data.action]
        store.event_update(event_id, update)
    summary = _event_summary(event_id)
    hub.publish("event.updated", summary)
    if status == "sent_to_master" and row["status"] != "sent_to_master":
        hub.publish("notification", _master_alert(summary), ["master"])
        _deliveries.append((event_id, "to_master"))
    return event_detail(event_id, role)


def escalation_tick() -> int:
    """Red events the operator left without a decision go to the master (tech.md 8.7)."""
    settings = config.get_settings().escalation
    if not settings.enabled:
        return 0
    red_before = clock.iso(clock.now() - timedelta(seconds=settings.timeout_s))
    with store.tx():
        due = store.escalation_due(red_before)
        for row in due:
            store.event_update(row["id"], {"status": "sent_to_master", "escalated_by_timeout": 1})
            _system_action(row["id"], "timeout_escalated", row["status"], "sent_to_master")
    for row in due:
        summary = _event_summary(row["id"])
        hub.publish("event.updated", summary)
        hub.publish("notification", _master_alert(summary), ["master"])
        _deliveries.append((row["id"], "to_master"))
    return len(due)


def master_inbox_view() -> MasterInbox:
    limit = config.get_settings().master.recent_resolved
    return MasterInbox(
        active=[_summary(row) for row in store.master_active()],
        recent_resolved=[_summary(row) for row in store.master_resolved(limit)],
        server_now=clock.now(),
    )


def _shift_window(at: datetime) -> tuple[str, str, datetime, datetime]:
    """The shift of `settings.shifts` holding `at` in `settings.timezone`: id, title, start, end;
    a shift whose end is not after its start runs over midnight."""
    settings = config.get_settings()
    local = clock.local(at, settings.timezone)
    for shift in settings.shifts:
        (sh, sm), (eh, em) = (map(int, t.split(":")) for t in (shift.start, shift.end))
        for day in (local.date() - timedelta(days=1), local.date()):
            midnight = datetime.combine(day, datetime.min.time(), local.tzinfo)
            start = midnight + timedelta(hours=sh, minutes=sm)
            end = midnight + timedelta(hours=eh, minutes=em)
            if end <= start:
                end += timedelta(days=1)
            if start <= local < end:
                return shift.id, shift.title, start, end
    raise LookupError(f"no shift at {local}")  # config/default.yaml covers the whole day


def _count_rows(events: list[EventSummary], key: str, titles: dict[str, str]) -> list[CountRow]:
    rows: dict[str, CountRow] = {}
    for e in events:
        k = str(getattr(e, key))
        r = rows.setdefault(
            k, CountRow(key=k, title=titles[k], count=0, confirmed=0, false_alarm=0)
        )
        r.count += 1
        r.confirmed += e.operator_verdict == "confirmed"
        r.false_alarm += e.operator_verdict == "false_alarm"
    return sorted(rows.values(), key=lambda r: (-r.count, r.title))


def shift_summary_view(at: datetime | None = None) -> ShiftSummary:
    when = clock.now() if at is None else at if at.tzinfo else at.replace(tzinfo=UTC)
    shift_id, title, start, end = _shift_window(when)
    events = [_summary(row) for row in store.shift_events(clock.iso(start), clock.iso(end))]
    sectors = {str(e.sector_id): e.sector_name for e in events}
    return ShiftSummary(
        shift_id=shift_id,
        title=title,
        start=start.astimezone(UTC),
        end=end.astimezone(UTC),
        total=len(events),
        by_sector=_count_rows(events, "sector_id", sectors),
        by_scenario=_count_rows(events, "scenario", texts.SCENARIO_TITLES),
        events=[e for e in events if e.operator_verdict == "confirmed"],
    )


ZONE_NAME_MAX = 60
ZONE_POINTS_MAX = 32
WORLD_MIN_AREA = 0.01  # m²: three floor points closer to a line than this are collinear (9)


def _in_frame(points: list[Point], field: str) -> None:
    if any(not (0 <= x <= 1 and 0 <= y <= 1) for x, y in points):
        raise ValidationFailed(texts.POINTS_OUTSIDE, field=field)


def _collinear(points: list[Point], min_area: float) -> bool:
    return any(
        geometry.polygon_area(list(triple)) < min_area
        for triple in itertools.combinations(points, 3)
    )


def _rmse(h: np.ndarray, pairs: list[tuple[Point, Point]]) -> float:
    errors = [math.dist(geometry.apply_h(h, image), world) ** 2 for image, world in pairs]
    return math.sqrt(sum(errors) / len(errors))


def _calibration(row: sqlite3.Row) -> Calibration:
    world = [(x, y) for x, y in json.loads(row["world_points_json"])]
    h = np.array(json.loads(row["homography_json"]), np.float64)
    return Calibration(
        camera_id=row["camera_id"],
        image_points=json.loads(row["image_points_json"]),
        world_points=world,
        control_points=json.loads(row["control_json"]),
        fit_rmse_m=row["fit_rmse_m"],
        control_rmse_m=row["control_rmse_m"],
        grid=geometry.grid_segments(h, world),
        updated_at=clock.parse(row["updated_at"]),
    )


def _calibration_of(camera_id: int) -> Calibration | None:
    row = store.calibration(camera_id)
    return None if row is None else _calibration(row)


def calibration_get(camera_id: int) -> Calibration | None:
    camera_get(camera_id)
    return _calibration_of(camera_id)


def calibration_set(camera_id: int, data: CalibrationIn, role: Role | None) -> Calibration:
    _require(role, ("admin",))
    camera_get(camera_id)
    image, world = data.image_points, data.world_points
    if not geometry.MIN_CAL_POINTS <= len(image) <= geometry.MAX_CAL_POINTS:
        raise ValidationFailed(texts.CAL_POINTS_COUNT, field="image_points")
    if len(world) != len(image):
        raise ValidationFailed(texts.CAL_POINTS_MISMATCH, field="world_points")
    if len(data.control_points) > geometry.MAX_CAL_POINTS:
        raise ValidationFailed(texts.CAL_CONTROL_MAX, field="control_points")
    _in_frame(image, "image_points")
    _in_frame([c.image for c in data.control_points], "control_points")
    h = geometry.homography(image, world)
    if h is None or _collinear(image, geometry.MIN_AREA) or _collinear(world, WORLD_MIN_AREA):
        raise ValidationFailed(texts.CAL_COLLINEAR, field="image_points")
    control = [(c.image, c.world) for c in data.control_points]
    values = {
        "camera_id": camera_id,
        "image_points_json": json.dumps(image),
        "world_points_json": json.dumps(world),
        "control_json": json.dumps([c.model_dump() for c in data.control_points]),
        "homography_json": json.dumps(h.tolist()),
        "fit_rmse_m": _rmse(h, list(zip(image, world, strict=True))),
        "control_rmse_m": _rmse(h, control) if control else None,
        "updated_at": clock.iso(clock.now()),
    }
    with store.tx():
        store.calibration_put(values)
    calibration = _calibration_of(camera_id)
    assert calibration is not None  # just written
    return calibration


def calibration_delete(camera_id: int, role: Role | None) -> None:
    _require(role, ("admin",))
    with store.tx():
        camera_get(camera_id)
        store.calibration_delete(camera_id)


def _zone(row: sqlite3.Row) -> Zone:
    return Zone(
        id=row["id"],
        camera_id=row["camera_id"],
        kind=row["kind"],
        name=row["name"],
        points=json.loads(row["points_json"]),
    )


def _zone_name(value: str) -> str:
    name = value.strip()
    if not 1 <= len(name) <= ZONE_NAME_MAX:
        raise ValidationFailed(texts.ZONE_NAME_INVALID, field="name")
    return name


def _zone_points(kind: str, points: list[Point]) -> str:
    """Geometry rules of tech.md 9 for the zone kind; the points as JSON."""
    kinds = {k.id: k.geometry for k in config.get_settings().zone_kinds}
    if kind not in kinds:
        raise ValidationFailed(texts.ZONE_KIND_UNKNOWN, field="kind")
    _in_frame(points, "points")
    if kinds[kind] == "line":
        if len(points) != 2 or points[0] == points[1]:
            raise ValidationFailed(texts.ZONE_LINE_POINTS, field="points")
    elif not 3 <= len(points) <= ZONE_POINTS_MAX:
        raise ValidationFailed(texts.ZONE_POLYGON_POINTS, field="points")
    elif geometry.polygon_area(points) < geometry.MIN_AREA:
        raise ValidationFailed(texts.ZONE_DEGENERATE, field="points")
    return json.dumps(points)


def _zone_row(zone_id: int) -> sqlite3.Row:
    row = store.zone(zone_id)
    if row is None:
        raise NotFound(texts.ZONE_NOT_FOUND, zone_id=zone_id)
    return row


def zones_list(camera_id: int) -> list[Zone]:
    camera_get(camera_id)
    return [_zone(row) for row in store.zones(camera_id)]


def zone_create(camera_id: int, data: ZoneIn, role: Role | None) -> Zone:
    _require(role, ("admin", "ohs"))
    camera_get(camera_id)
    values = {
        "camera_id": camera_id,
        "kind": data.kind,
        "name": _zone_name(data.name),
        "points_json": _zone_points(data.kind, data.points),
        "created_at": clock.iso(clock.now()),
    }
    with store.tx():
        zone_id = store.insert("zones", values)
    return _zone(_zone_row(zone_id))


def zone_update(zone_id: int, data: ZonePatch, role: Role | None) -> Zone:
    _require(role, ("admin", "ohs"))
    row = _zone_row(zone_id)
    values = {}
    if data.name is not None:
        values["name"] = _zone_name(data.name)
    if data.points is not None:
        values["points_json"] = _zone_points(row["kind"], data.points)
    if values:
        with store.tx():
            store.zone_update(zone_id, values)
    return _zone(_zone_row(zone_id))


def zone_delete(zone_id: int, role: Role | None) -> None:
    _require(role, ("admin", "ohs"))
    with store.tx():
        _zone_row(zone_id)
        store.zone_update(zone_id, {"deleted_at": clock.iso(clock.now())})


def _rules(camera_id: int, rows: list[sqlite3.Row], metas: list[ScenarioMeta]) -> list[CameraRule]:
    """A rule per plugin (tech.md 8.3): no stored row — on when the scenario is active."""
    stored = {row["scenario"]: row for row in rows}
    out = []
    for meta in metas:
        row = stored.get(meta.id)
        params: dict[str, float] = {} if row is None else json.loads(row["params_json"])
        out.append(
            CameraRule(
                camera_id=camera_id,
                scenario=meta.id,
                enabled=meta.status == "active" if row is None else bool(row["enabled"]),
                params=params,
                effective=rules.defaults(meta.id) | params,
                status=meta.status,
            )
        )
    return out


def _range(x: float) -> str:
    return f"{x:g}".replace(".", ",")


def camera_rules(camera_id: int) -> list[CameraRule]:
    camera_get(camera_id)
    return _rules(camera_id, store.camera_rules(camera_id), rules.scenario_metas())


def camera_rule_set(
    camera_id: int, scenario: str, data: CameraRuleIn, role: Role | None
) -> CameraRule:
    _require(role, ("admin", "ohs"))
    camera_get(camera_id)
    metas = {meta.id: meta for meta in rules.scenario_metas()}
    if scenario not in metas:
        raise NotFound(texts.SCENARIO_NOT_FOUND, scenario=scenario)
    ranges = {p.key: (p.min, p.max) for p in metas[scenario].params}
    for key, value in data.params.items():
        if key not in ranges:
            raise ValidationFailed(texts.PARAM_UNKNOWN.format(key=key), field=f"params.{key}")
        lo, hi = ranges[key]
        if not lo <= value <= hi:
            text = texts.PARAM_RANGE.format(key=key, lo=_range(lo), hi=_range(hi))
            raise ValidationFailed(text, field=f"params.{key}")
    values = {
        "camera_id": camera_id,
        "scenario": scenario,
        "enabled": int(data.enabled),
        "params_json": json.dumps(data.params),
        "updated_at": clock.iso(clock.now()),
    }
    with store.tx():
        store.camera_rule_put(values)
    (rule,) = [r for r in camera_rules(camera_id) if r.scenario == scenario]
    return rule


def rules_screen_view() -> RulesScreenView:
    metas = rules.scenario_metas()
    stored: dict[int, list[sqlite3.Row]] = {}
    for row in store.camera_rules():
        stored.setdefault(row["camera_id"], []).append(row)
    rows = [
        RulesScreenRow(camera=camera, rules=_rules(camera.id, stored.get(camera.id, []), metas))
        for camera in cameras_list()
    ]
    return RulesScreenView(scenarios=metas, rows=rows)


QUERY_MAX = 100


def _utc(dt: datetime | None) -> str | None:
    """A query datetime as stored; one without a time zone is UTC."""
    if dt is None:
        return None
    return clock.iso(dt if dt.tzinfo else dt.replace(tzinfo=UTC))


def _journal_where(f: EventFilter) -> tuple[str, list[Any]]:
    """Checks of tech.md 9 «фильтр журнала» and the WHERE of the filter."""

    def bad(field: str) -> ValidationFailed:
        return ValidationFailed(texts.FILTER_INVALID.format(field=field), field=field)

    if not 1 <= f.limit <= config.get_settings().journal.page_max:
        raise bad("limit")
    if f.q is not None and len(f.q) > QUERY_MAX:
        raise bad("q")
    date_from, date_to = _utc(f.date_from), _utc(f.date_to)
    if date_from is not None and date_to is not None and date_from > date_to:
        raise bad("date_from")
    if f.cursor is not None and not (f.cursor.isascii() and f.cursor.isdigit()):
        raise bad("cursor")
    # LIKE ... ESCAPE '\': the backslash first, then the wildcards are searched literally.
    q = f.q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") if f.q else None
    equal = {
        "level": f.level,
        "scenario": f.scenario,
        "status": f.status,
        "sector_id": f.sector_id,
        "camera_id": f.camera_id,
        "zone_id": f.zone_id,
    }
    return store.journal_where(equal, date_from, date_to, q, f.include_demo, f.include_superseded)


def events_list(f: EventFilter) -> EventPage:
    where = _journal_where(f)
    after = int(f.cursor) if f.cursor is not None else None
    rows, total = store.journal(where, after, f.limit + 1)
    items = [_summary(row) for row in rows[: f.limit]]
    more = len(rows) > f.limit
    return EventPage(items=items, total=total, next_cursor=str(items[-1].id) if more else None)


def _msk(dt: datetime) -> str:
    return clock.local(dt, config.get_settings().timezone).strftime("%Y-%m-%d %H:%M:%S")


def events_export_csv(f: EventFilter) -> str:
    """The whole filtered journal up to `journal.export_max_rows`: `;`, UTF-8 with BOM."""
    rows, _ = store.journal(_journal_where(f), None, config.get_settings().journal.export_max_rows)
    history: dict[int, list[str]] = {}
    for a in store.journal_actions([row["id"] for row in rows]):
        role = a["actor_role"]
        who = texts.DEMO_ACTOR["system"] if role == "system" else texts.ROLE_TITLES[role]
        step = f"{_msk(clock.parse(a['at']))} {who}: {texts.ACTION_TITLES[a['action']]}"
        history.setdefault(a["event_id"], []).append(
            f"{step} ({a['comment']})" if a["comment"] else step
        )
    out = io.StringIO()
    writer = csv.writer(out, delimiter=";", lineterminator="\r\n")
    writer.writerow(texts.CSV_COLUMNS)
    for row in rows:
        e = _summary(row)
        writer.writerow(
            [
                e.id,
                _msk(e.published_at),
                _msk(e.started_at),
                e.sector_name,
                e.camera_name,
                e.zone_name or "",
                e.title,
                texts.LEVEL_TITLES[e.level],
                e.status_title,
                texts.VERDICT_TITLES[e.operator_verdict],
                texts.YES if e.escalated_by_timeout else texts.NO,
                e.reason_text,
                f"{e.duration_s:.1f}".replace(".", ","),  # the decimal comma of Russian Excel
                texts.YES if e.is_demo else texts.NO,
                row["evidence_sha256"] or "",
                "; ".join(history.get(e.id, [])),
            ]
        )
    return "﻿" + out.getvalue()


def journal_facets() -> JournalFacets:
    def items(pairs: Iterable[tuple[object, str]]) -> list[FacetItem]:
        return [FacetItem(id=str(key), title=title) for key, title in pairs]

    return JournalFacets(
        scenarios=items(texts.SCENARIO_TITLES.items()),
        levels=items(texts.LEVEL_TITLES.items()),
        statuses=items(texts.STATUS_TITLES.items()),
        sectors=items((s["id"], s["name"]) for s in store.sectors()),
        cameras=items((c["id"], c["name"]) for c in store.cameras()),
        zones=items((z["id"], f"{z['camera_name']} · {z['name']}") for z in store.all_zones()),
    )


OPERATOR_DECISIONS = frozenset({"confirmed", "false_alarm", "sent_to_master"})  # tech.md 8.13
HANDOVERS = frozenset({"sent_to_master", "timeout_escalated"})  # the event goes to the master


def _percentiles(values: list[float], pending: int) -> Percentiles:
    """Nearest rank: sorted `x[ceil(p·n) − 1]` (tech.md 8.13)."""
    x = sorted(values)

    def rank(p: float) -> float | None:
        # round: 0.95·n in floating point may land a hair above an integer rank.
        return x[math.ceil(round(p * len(x), 9)) - 1] if x else None

    return Percentiles(n=len(x), pending=pending, p50=rank(0.5), p95=rank(0.95))


def _reactions(events: list[EventSummary]) -> tuple[Percentiles, Percentiles, Percentiles]:
    """Operator reaction, master accept and master resolve times of tech.md 8.13, seconds."""
    log: dict[int, list[sqlite3.Row]] = {}
    for a in store.journal_actions([e.id for e in events]):
        log.setdefault(a["event_id"], []).append(a)
    operator: list[float] = []
    accept: list[float] = []
    resolve: list[float] = []
    pending = [0, 0, 0]
    for e in events:
        actions = log.get(e.id, [])
        first = next(
            (
                a
                for a in actions
                if a["actor_role"] == "operator" and a["action"] in OPERATOR_DECISIONS
            ),
            None,
        )
        if first is not None:
            operator.append((clock.parse(first["at"]) - e.published_at).total_seconds())
        elif e.status not in TERMINAL_STATUSES:
            pending[0] += 1
        handed: datetime | None = None
        accepted: datetime | None = None
        for a in actions:
            at = clock.parse(a["at"])
            if a["action"] in HANDOVERS and accepted is None:
                handed = at  # the last hand-over before the master accepts
            elif a["action"] == "master_accepted" and handed is not None and accepted is None:
                accepted = at
                accept.append((at - handed).total_seconds())
            elif a["action"] == "resolved" and accepted is not None:
                resolve.append((at - accepted).total_seconds())
        pending[1] += e.status == "sent_to_master"
        pending[2] += e.status == "master_accepted"
    return (
        _percentiles(operator, pending[0]),
        _percentiles(accept, pending[1]),
        _percentiles(resolve, pending[2]),
    )


def _fixed_rows(
    pairs: Iterable[tuple[str, str]], keyed: Iterable[tuple[str, EventSummary]]
) -> list[CountRow]:
    """Count rows in the order of `pairs`, zero rows kept (hours, shifts)."""
    rows = {k: CountRow(key=k, title=t, count=0, confirmed=0, false_alarm=0) for k, t in pairs}
    for k, e in keyed:
        r = rows[k]
        r.count += 1
        r.confirmed += e.operator_verdict == "confirmed"
        r.false_alarm += e.operator_verdict == "false_alarm"
    return list(rows.values())


def _add_levels(row: DayRow | WeekRow, e: EventSummary) -> None:
    row.yellow += e.level == "yellow"
    row.red += e.level == "red"
    row.confirmed += e.operator_verdict == "confirmed"
    row.false_alarm += e.operator_verdict == "false_alarm"


def _share(part: int, whole: int) -> float | None:
    return part / whole if whole else None


def ohs_stats_view(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    sector_id: int | None = None,
    camera_id: int | None = None,
    include_demo: bool = True,
) -> OhsStats:
    settings = config.get_settings()
    tz = settings.timezone

    def aware(dt: datetime) -> datetime:  # a query datetime without a time zone is UTC
        return dt if dt.tzinfo else dt.replace(tzinfo=UTC)

    end = aware(date_to) if date_to is not None else clock.now()
    start = (
        aware(date_from)
        if date_from is not None
        else end - timedelta(days=settings.stats.default_days)
    )
    if start > end:
        raise ValidationFailed(texts.PERIOD_INVALID, field="date_from")
    equal = {"sector_id": sector_id, "camera_id": camera_id}
    where = store.journal_where(equal, clock.iso(start), clock.iso(end), None, include_demo, False)
    events = [_summary(row) for row in store.events_where(where)]
    local = {e.id: clock.local(e.started_at, tz) for e in events}
    first = clock.local(start, tz).date()
    last = clock.local(max(start, end - timedelta(milliseconds=1)), tz).date()
    days = {
        d.isoformat(): DayRow(date=d.isoformat(), yellow=0, red=0, confirmed=0, false_alarm=0)
        for d in (first + timedelta(days=i) for i in range((last - first).days + 1))
    }
    for e in events:
        _add_levels(days[local[e.id].date().isoformat()], e)
    hours = [(f"{h:02d}", f"{h:02d}:00") for h in range(24)]
    reviewed = sum(e.operator_verdict != "none" for e in events)
    false_alarm = sum(e.operator_verdict == "false_alarm" for e in events)
    operator, accept, resolve = _reactions(events)
    return OhsStats(
        date_from=start,
        date_to=end,
        include_demo=include_demo,
        total=len(events),
        by_status=_count_rows(events, "status", texts.STATUS_TITLES),
        by_scenario=_count_rows(events, "scenario", texts.SCENARIO_TITLES),
        by_sector=_count_rows(
            events, "sector_id", {str(e.sector_id): e.sector_name for e in events}
        ),
        by_camera=_count_rows(
            events, "camera_id", {str(e.camera_id): e.camera_name for e in events}
        ),
        by_shift=_fixed_rows(
            ((s.id, s.title) for s in settings.shifts),
            ((_shift_window(e.started_at)[0], e) for e in events),
        ),
        by_hour=_fixed_rows(hours, ((f"{local[e.id].hour:02d}", e) for e in events)),
        by_day=list(days.values()),
        reviewed=reviewed,
        false_alarm_share=_share(false_alarm, reviewed),
        review_coverage=_share(reviewed, len(events)),
        operator_reaction_s=operator,
        master_accept_s=accept,
        master_resolve_s=resolve,
    )


def _trend(previous: int, recent: int, weeks: int) -> TrendSummary:
    if previous == 0:
        return TrendSummary(previous=0, recent=recent, change_pct=None, text=texts.TREND_NO_DATA)
    change = (recent - previous) / previous * 100
    pct, span = round(abs(change)), texts.weeks_span(weeks)
    template = (
        texts.TREND_SAME if pct == 0 else texts.TREND_LESS if change < 0 else texts.TREND_MORE
    )
    text = template.format(pct=pct, span=span)
    return TrendSummary(previous=previous, recent=recent, change_pct=change, text=text)


def management_view(weeks: int | None = None, include_demo: bool = True) -> ManagementStats:
    settings = config.get_settings()
    n = settings.stats.weeks_default if weeks is None else weeks
    if not 1 <= n <= 52:
        raise ValidationFailed(texts.PERIOD_INVALID, field="weeks")
    tz, trend = settings.timezone, settings.stats.trend_weeks
    today = clock.local(clock.now(), tz)
    week = timedelta(days=7)
    monday = datetime.combine(
        today.date() - timedelta(days=today.weekday()), datetime.min.time(), today.tzinfo
    )
    first = monday - (n - 1) * week
    since = min(first, monday - 2 * trend * week)
    where = store.journal_where(
        {}, clock.iso(since), clock.iso(monday + week), None, include_demo, False
    )
    events = [_summary(row) for row in store.events_where(where)]
    rows = {
        start.date().isoformat(): WeekRow(
            week_start=start.date().isoformat(), yellow=0, red=0, confirmed=0, false_alarm=0
        )
        for start in (first + i * week for i in range(n))
    }
    for e in events:
        day = clock.local(e.started_at, tz).date()
        row = rows.get((day - timedelta(days=day.weekday())).isoformat())
        if row is not None:
            _add_levels(row, e)
    top_from = monday - (trend - 1) * week
    confirmed = Counter(
        e.sector_id
        for e in events
        if e.operator_verdict == "confirmed" and e.started_at >= top_from
    )
    cameras = Counter(c["sector_id"] for c in store.cameras())
    top = [
        RateRow(
            key=str(s["id"]),
            title=s["name"],
            cameras=cameras[s["id"]],
            confirmed=confirmed[s["id"]],
            per_camera=_share(confirmed[s["id"]], cameras[s["id"]]),
        )
        for s in store.sectors()
        if include_demo or not s["is_demo"]
    ]
    top.sort(key=lambda r: (r.per_camera is None, -(r.per_camera or 0), r.title))

    def yellow(lo: datetime, hi: datetime) -> int:
        return sum(
            e.level == "yellow" and e.operator_verdict != "false_alarm" and lo <= e.started_at < hi
            for e in events
        )

    recent = yellow(monday - trend * week, monday)
    previous = yellow(monday - 2 * trend * week, monday - trend * week)
    in_weeks = [e for e in events if e.started_at >= first]
    return ManagementStats(
        weeks=list(rows.values()),
        top_sectors=top,
        top_scenarios=_count_rows(in_weeks, "scenario", texts.SCENARIO_TITLES),
        yellow_trend=_trend(previous, recent, trend),
    )


def _eval_labels(path: Path) -> EvalLabels:
    """Labels of tech.md 8.18 and the row «разметка оценки» of tech.md 9."""
    if not path.is_file():
        raise NotFound(texts.FILE_NOT_FOUND.format(path=path))
    try:
        labels = EvalLabels.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
    except yaml.YAMLError:
        raise ValidationFailed(
            texts.EVAL_LABELS_INVALID.format(field="yaml"), field="yaml"
        ) from None
    except ValidationError as exc:
        field = ".".join(str(part) for part in exc.errors()[0]["loc"]) or "labels"
        raise ValidationFailed(texts.EVAL_LABELS_INVALID.format(field=field), field=field) from None
    for i, video in enumerate(labels.videos):
        for j, e in enumerate(video.expected):
            if e.start_s >= e.end_s:
                field = f"videos.{i}.expected.{j}"
                raise ValidationFailed(texts.EVAL_INTERVAL_INVALID.format(field=field), field=field)
    return labels


async def _eval_episodes(path: Path, camera_id: int | None) -> tuple[list[EpisodeDraft], int]:
    """Inference with the artifact cache and analysis of one labelled video, like a job."""
    settings = config.get_settings()
    probe = media.probe_video(path)
    if probe is None:
        raise UnsupportedVideo(texts.VIDEO_UNREADABLE)
    # An absolute path: `data_dir / path` in _infer keeps it.
    video: dict[str, Any] = probe.model_dump() | {"sha256": _sha256(path), "path": str(path)}
    detector = registry.resolve(settings.pipeline.detector)
    det_id = await _infer(None, "inference_detect", (0.0, 0.0), detector, video)
    extra = []
    for ref in settings.pipeline.extra:
        model = registry.resolve(ref)
        extra.append((model, await _infer(None, "inference_detect", (0.0, 0.0), model, video)))
    pose = None
    if settings.pipeline.pose is not None:
        pose_model = registry.resolve(settings.pipeline.pose)
        pose = (pose_model, await _infer(None, "inference_pose", (0.0, 0.0), pose_model, video))
    cfg = _analysis_config(video, camera_id, [artifact_id for _, artifact_id in extra])
    data = settings.data_dir
    det_path = data / store.artifact_path(det_id)
    pose_files = None if pose is None else (pose[0], data / store.artifact_path(pose[1]))
    extra_files = [(m, data / store.artifact_path(artifact_id)) for m, artifact_id in extra]

    def analysis() -> AnalysisResult:  # worker thread: files in, episodes out
        det = artifacts.read_jsonl(det_path, None)
        pose_frames = None if pose_files is None else artifacts.read_jsonl(pose_files[1], None)
        pose_model = None if pose_files is None else pose_files[0]
        extra_frames = [(m, artifacts.read_jsonl(p, None)) for m, p in extra_files]
        return pipeline.analyze(det, pose_frames, path, cfg, pose_model, detector, extra_frames)

    result = await asyncio.to_thread(analysis)
    return result.episodes, probe.duration_ms


def _eval_rows(outcomes: list[evaluate.Outcome], hours: float) -> list[EvalMetrics]:
    """A row per scenario and the total `*` (tech.md 8.18); a zero denominator gives `None`."""
    rows = []
    for key in [*sorted({scenario for scenario, _, _ in outcomes}), "*"]:
        mine = [o for o in outcomes if key in ("*", o[0])]
        n = Counter(kind for _, kind, _ in mine)
        tp, fn, fp = n["tp"], n["fn"], n["fp"]
        precision, recall = _share(tp, tp + fp), _share(tp, tp + fn)
        f1 = None
        if precision is not None and recall is not None and precision + recall > 0:
            f1 = 2 * precision * recall / (precision + recall)
        delays = [delay for _, kind, delay in mine if kind == "tp" and delay is not None]
        rows.append(
            EvalMetrics(
                scenario=key,
                expected=tp + fn,
                episodes=tp + fp + n["duplicate"] + n["late"],
                tp=tp,
                fn=fn,
                fp=fp,
                duplicates=n["duplicate"],
                late=n["late"],
                precision=precision,
                recall=recall,
                f1=f1,
                fp_per_hour=fp / hours if hours else None,
                delay_s=_percentiles(delays, 0),
            )
        )
    return rows


def eval_run(labels: Path, out_dir: Path | None = None) -> EvalReport:
    """Sync: runs its own event loop, the CLI is its only caller."""
    settings = config.get_settings()
    spec = _eval_labels(labels)
    paths = []
    for video in spec.videos:
        path = Path(video.path)
        path = path if path.is_absolute() else config.ROOT / path
        if not path.is_file():
            raise NotFound(texts.FILE_NOT_FOUND.format(path=video.path))
        if video.camera_id is not None:
            camera_get(video.camera_id)
        paths.append(path)
    deadline_s = settings.eval.deadline_s if spec.deadline_s is None else spec.deadline_s
    outcomes: list[evaluate.Outcome] = []
    duration_ms = 0
    for video, path in zip(spec.videos, paths, strict=True):
        episodes, ms = asyncio.run(_eval_episodes(path, video.camera_id))
        outcomes += evaluate.match_episodes(video.expected, episodes, deadline_s)
        duration_ms += ms
    now = clock.now()
    out = out_dir or settings.data_dir / "eval" / now.strftime("%Y%m%d-%H%M%S")
    hours = duration_ms / 3_600_000
    report = EvalReport(
        created_at=now,
        labels=str(labels),
        hours=hours,
        deadline_s=deadline_s,
        rows=_eval_rows(outcomes, hours),
        out_dir=str(out),
    )
    out.mkdir(parents=True, exist_ok=True)
    text = report.model_dump_json(indent=2) + "\n"
    (out / "report.json").write_text(text, encoding="utf-8", newline="\n")
    (out / "report.md").write_text(evaluate.report_md(report), encoding="utf-8", newline="\n")
    return report


async def deliveries_flush() -> int:
    """Send the queued deliveries to every channel with the event level; the rows written.

    One attempt per `(event, channel, kind)`: a key already in `deliveries` is not sent again,
    a failure stays `failed` and never touches the event.
    """
    queued = list(dict.fromkeys(_deliveries))
    _deliveries.clear()
    channels = [
        delivery.WebhookChannel(w.name, w.url, w.levels, w.timeout_s)
        for w in config.get_settings().delivery.webhooks
    ]
    if not queued or not channels:
        return 0
    events = {row["id"]: _summary(row) for row in store.events_by_ids([e for e, _ in queued])}
    done = store.delivery_keys(list(events))
    written = 0
    for event_id, kind in queued:
        summary = events[event_id]
        for channel in channels:
            key = (event_id, f"webhook:{channel.name}", kind)
            if summary.level not in channel.levels or key in done:
                continue
            ok, http_status, error = await asyncio.to_thread(channel.deliver, summary, kind)
            values = {
                "event_id": event_id,
                "channel": key[1],
                "kind": kind,
                "status": "sent" if ok else "failed",
                "http_status": http_status,
                "error": error,
                "at": clock.iso(clock.now()),
            }
            store.insert("deliveries", values)
            done.add(key)
            written += 1
    return written


# --- v5 (tech.md 6.11.4): declared in slice 16, built by the slice in each stub -----------
def _field(exc: ValidationError) -> str:
    return ".".join(str(part) for part in exc.errors()[0]["loc"]) or "root"


def _demo_layout(path: Path) -> DemoLayout:
    if not path.is_file():
        raise NotFound(texts.FILE_NOT_FOUND.format(path=path))
    try:
        return DemoLayout.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
    except yaml.YAMLError:
        raise ValidationFailed(
            texts.DEMO_LAYOUT_INVALID.format(field="yaml"), field="yaml"
        ) from None
    except ValidationError as exc:
        field = _field(exc)
        raise ValidationFailed(texts.DEMO_LAYOUT_INVALID.format(field=field), field=field) from None


def _demo_videos(cameras: list[DemoCamera], videos_dir: Path) -> dict[str, Path]:
    """Every layout video by its file name: present and readable, before anything is written."""
    found: dict[str, Path] = {}
    for camera in cameras:
        for video in camera.videos:
            path = videos_dir / video.file
            if not path.is_file():
                raise NotFound(texts.FILE_NOT_FOUND.format(path=path))
            if media.probe_video(path) is None:
                raise UnsupportedVideo(texts.VIDEO_UNREADABLE)
            found[video.file] = path
    return found


def _demo_run(
    backend: InferenceBackend, video: Path, out: Path, done: dict[str, DemoArtifact]
) -> DemoVideo:
    """Step 3 of tech.md 8.19 for one video: every active model, one backend run at a time."""
    settings = config.get_settings()
    probe = media.probe_video(video)
    assert probe is not None  # checked by _demo_videos
    sha256 = _sha256(video)
    step = analysis_step(probe.fps)
    refs = [settings.pipeline.detector, *settings.pipeline.extra]
    refs += [] if settings.pipeline.pose is None else [settings.pipeline.pose]
    items = []
    for ref in refs:
        model = registry.resolve(ref)
        key = artifacts.cache_key(sha256, model, step, backend.name, settings.fake)
        if key not in done:
            jsonl = out / "artifacts" / f"{key}.jsonl"
            metrics = backend.run(video, sha256, model, step, jsonl, lambda share: None)
            frames = len(artifacts.read_jsonl(jsonl, metrics.frames_processed))
            done[key] = DemoArtifact(
                model=ref,
                task=model.task,
                input_size=model.input_size,
                step=step,
                backend=backend.name,
                fake=settings.fake,
                file=f"artifacts/{key}.jsonl",
                frames=frames,
                metrics=metrics,
            )
        items.append(done[key])
    return DemoVideo(file=f"videos/{video.name}", sha256=sha256, artifacts=items)


def demo_build(layout: Path, videos_dir: Path, out: Path, allow_fake: bool = False) -> DemoManifest:
    """Pack files only (tech.md 8.19), the database stays as is; a failure leaves no `out`."""
    from safewatch.api import CONTRACT_VERSION  # api imports this module at the top

    spec = _demo_layout(layout)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValidationFailed(texts.DEMO_OUT_NOT_EMPTY.format(path=out), field="out")
    if config.get_settings().fake and not allow_fake:
        raise ValidationFailed(texts.DEMO_FAKE_REFUSED, field="allow_fake")
    sources = _demo_videos(spec.cameras, videos_dir)
    backend = _backend_instance()
    done: dict[str, DemoArtifact] = {}
    try:
        (out / "videos").mkdir(parents=True, exist_ok=True)
        (out / "artifacts").mkdir(exist_ok=True)
        cameras = []
        for camera in spec.cameras:
            videos = []
            for video in camera.videos:
                copy = out / "videos" / sources[video.file].name
                if not copy.exists():
                    shutil.copyfile(sources[video.file], copy)
                videos.append(_demo_run(backend, copy, out, done))
            cameras.append(camera.model_copy(update={"videos": videos}))
        manifest = DemoManifest(
            name=spec.name, created_at=clock.now(), contract=CONTRACT_VERSION, cameras=cameras
        )
        demo.write_manifest(out / demo.MANIFEST, manifest)
    except BaseException:
        shutil.rmtree(out, ignore_errors=True)
        raise
    return manifest


def _demo_manifest(path: Path) -> tuple[DemoManifest, str]:
    """The manifest and the sha256 of its file; schema, models and pack files checked."""
    file = path / demo.MANIFEST
    if not path.is_dir() or not file.is_file():
        raise NotFound(texts.FILE_NOT_FOUND.format(path=file))
    try:
        manifest = demo.read_manifest(file)
    except ValidationError as exc:
        field = _field(exc)
        raise ValidationFailed(
            texts.DEMO_MANIFEST_INVALID.format(field=field), field=field
        ) from None
    for camera in manifest.cameras:
        for video in camera.videos:
            for a in video.artifacts:
                try:
                    registry.resolve(a.model)
                except ValueError:
                    raise ValidationFailed(
                        texts.DEMO_MODEL_UNKNOWN.format(model=a.model), field="model"
                    ) from None
                if not (path / a.file).is_file():
                    raise NotFound(texts.FILE_NOT_FOUND.format(path=path / a.file))
            if not (path / video.file).is_file():
                raise NotFound(texts.FILE_NOT_FOUND.format(path=path / video.file))
            if _sha256(path / video.file) != video.sha256:
                raise ValidationFailed(
                    texts.DEMO_SHA_MISMATCH.format(file=video.file), field="sha256"
                )
    return manifest, _sha256(file)


def _demo_camera(camera: DemoCamera) -> int:
    """Step 3 of tech.md 8.19: the camera by sector and name; its setup only where it has none."""
    sector = store.sector_by_name(camera.sector.strip())
    if sector is None:
        sector_id = sector_create(SectorIn(name=camera.sector), "admin").id
    else:
        sector_id = sector["id"]
    row = store.camera_by_name(sector_id, camera.name.strip())
    if row is None:
        data = CameraIn(sector_id=sector_id, name=camera.name, description=camera.description)
        camera_id = camera_create(data, "admin").id
    else:
        camera_id = row["id"]
    if camera.calibration is not None and store.calibration(camera_id) is None:
        calibration_set(camera_id, camera.calibration, "admin")
    if not store.zones(camera_id):
        for zone in camera.zones:
            zone_create(camera_id, zone, "admin")
    stored = {row["scenario"] for row in store.camera_rules(camera_id)}
    for scenario, rule in camera.rules.items():
        if scenario not in stored:
            camera_rule_set(camera_id, scenario, rule, "admin")
    return int(camera_id)


def demo_import(path: Path) -> DemoImportReport:
    manifest, sha256 = _demo_manifest(path)
    pack = [a for c in manifest.cameras for v in c.videos for a in v.artifacts]
    videos = sum(len(c.videos) for c in manifest.cameras)
    counts = {"name": manifest.name, "cameras": len(manifest.cameras), "videos": videos}
    if store.demo_pack(manifest.name) is not None:
        return DemoImportReport(skipped=True, jobs=0, **counts)
    backend = pack[0].backend if pack else config.get_settings().inference_backend
    source: Source = (backend, any(a.fake for a in pack))
    jobs = 0
    with store.tx():
        for camera in manifest.cameras:
            camera_id = _demo_camera(camera)
            for video in camera.videos:
                result = _video_import(camera_id, path / video.file, source)
                for a in video.artifacts:
                    artifact_import(
                        result.video.id, a.model, path / a.file, a.backend, a.fake, a.metrics
                    )
                jobs += int(result.job is not None and not result.reused)
        values = {
            "name": manifest.name,
            "sha256": sha256,
            "backend": source[0],
            "fake": int(source[1]),
            "cameras": counts["cameras"],
            "videos": videos,
            "imported_at": clock.iso(clock.now()),
        }
        store.insert("demo_packs", values)
    return DemoImportReport(skipped=False, jobs=jobs, **counts)


def demo_packs() -> list[DemoPack]:
    return [DemoPack.model_validate(dict(row)) for row in store.demo_packs()]


def artifact_import(
    video_id: int,
    model_ref: str,
    jsonl: Path,
    backend: BackendName,
    fake: bool,
    metrics: InferenceMetrics | None = None,
) -> int:
    """An artifact made elsewhere (a demo pack, later Vast): the job cache finds it by its key."""
    settings = config.get_settings()
    video = _video_row(video_id)
    if not jsonl.is_file():
        raise NotFound(texts.FILE_NOT_FOUND.format(path=jsonl))
    try:
        model = registry.resolve(model_ref)
    except ValueError:
        raise ValidationFailed(
            texts.DEMO_MODEL_UNKNOWN.format(model=model_ref), field="model"
        ) from None
    try:
        frames = len(artifacts.read_jsonl(jsonl, None))
    except InferenceError as exc:
        text = texts.ARTIFACT_INVALID.format(file=jsonl.name, error=exc.message)
        raise ValidationFailed(text, field="jsonl") from None
    step = analysis_step(video["fps"]) if metrics is None else metrics.step
    if metrics is None:
        metrics = InferenceMetrics(
            backend=backend,
            fake=fake,
            model_id=model.id,
            model_version=model.version,
            task=model.task,
            input_size=model.input_size,
            step=step,
            frames_processed=frames,
            wall_s=0.0,
            throughput_fps=0.0,
            preprocess_ms=None,
            postprocess_ms=None,
            tpu_rtt_p50_ms=None,
            tpu_rtt_p90_ms=None,
            upload_s=None,
            total_s=0.0,
            cached=False,
        )
    key = artifacts.cache_key(video["sha256"], model, step, backend, fake)
    rel = f"artifacts/{key}.jsonl"
    target = settings.data_dir / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(jsonl, target)
    values = {
        "cache_key": key,
        "video_sha256": video["sha256"],
        "model_id": model.id,
        "model_version": model.version,
        "task": model.task,
        "input_size": model.input_size,
        "step": step,
        "backend": backend,
        "fake": int(fake),
        "path": rel,
        "frames": frames,
        "metrics_json": metrics.model_dump_json(exclude={"cached"}),
        "created_at": clock.iso(clock.now()),
    }
    with store.tx():
        existing = store.artifact(key)
        if existing is not None:
            store.artifact_update(existing["id"], values)
            return int(existing["id"])
        return store.insert("artifacts", values)


def calculator_defaults() -> CalculatorDefaults:
    raise NotImplementedError("slice 24")


def calculator_rollout(data: RolloutIn, role: Role | None) -> RolloutResult:
    raise NotImplementedError("slice 24")


def calculator_scale(data: ScaleIn, role: Role | None) -> ScaleResult:
    raise NotImplementedError("slice 24")


async def datasets_flush() -> int:
    raise NotImplementedError("slice 25")


def datasets_view() -> DatasetView:
    raise NotImplementedError("slice 25")


def dataset_export(out: Path | None = None) -> Path:
    raise NotImplementedError("slice 25")


def event_identify(
    event_id: int, data: IdentityIn, role: Role | None, actor: str | None
) -> EventDetail:
    raise NotImplementedError("slice 26")


def people_stats_view(
    date_from: datetime | None = None, date_to: datetime | None = None, include_demo: bool = True
) -> PeopleStats:
    raise NotImplementedError("slice 26")


def camera_passport(camera_id: int) -> CameraPassport:
    raise NotImplementedError("slice 27")


def shift_report_pdf(at: datetime | None = None) -> bytes:
    raise NotImplementedError("slice 30")


def backend_close() -> None:
    raise NotImplementedError("slice 28")
