"""Facade (tech.md 6.2): the one entry point for API, CLI, worker and tests.

Functions of slices that are not built yet raise `NotImplementedError("slice N")`; the API
answers them with 501 `not_implemented`.
"""

import asyncio
import hashlib
import json
import logging
import math
import shutil
import sqlite3
import time
import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import get_args

from pydantic import BaseModel

from safewatch import clock, config, media, registry, rules, seed, store, texts
from safewatch.analysis import pipeline
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
    BackendStatus,
    Broadcast,
    BroadcastIn,
    Calibration,
    CalibrationIn,
    Camera,
    CameraIn,
    CameraLiveView,
    CameraPatch,
    CameraRule,
    CameraRuleIn,
    CamerasAdminView,
    CameraSetupView,
    CameraState,
    CameraStateKind,
    CameraTile,
    CountRow,
    Episode,
    EpisodeDraft,
    EvalReport,
    EventAction,
    EventDetail,
    EventFilter,
    EventPage,
    EventStatus,
    EventSummary,
    Evidence,
    Health,
    HudFrame,
    HumanAction,
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
    OhsStats,
    OperatorDashboard,
    Percentiles,
    Provenance,
    Role,
    RoleMeta,
    RulesScreenView,
    Sector,
    SectorIn,
    SectorState,
    SectorView,
    SeedReport,
    ShiftSummary,
    StatusMeta,
    SystemView,
    TracksWindow,
    UploadResult,
    Verdict,
    Video,
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


def _enqueue(video_id: int, kind: JobKind = "process") -> int:
    settings = config.get_settings()
    values = {
        "kind": kind,
        "video_id": video_id,
        "backend": settings.inference_backend,
        "fake": int(settings.fake),
        "status": "queued",
        "stage": "queued",
        "created_at": clock.iso(clock.now()),
    }
    return store.insert("jobs", values)


def _register(
    camera_id: int, filename: str, sha256: str, size: int, probe: media.VideoProbe
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
                "status": "uploaded",
                "created_at": clock.iso(clock.now()),
            }
            video_id = store.insert("videos", values)
            job_id: int | None = _enqueue(video_id)
            new_job, reused = True, False
        else:
            video_id, reused = row["id"], True
            if row["status"] == "ready":
                job_id = None
            elif row["status"] == "failed":
                job_id = _enqueue(video_id)
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
    return _register(camera_id, filename, sha256, size, probe)


def video_import(camera_id: int, path: Path) -> UploadResult:
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
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 20):
            digest.update(chunk)
    sha256 = digest.hexdigest()
    target = settings.data_dir / "uploads" / f"{sha256}{ext}"
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    return _register(camera_id, path.name, sha256, size, probe)


def videos_list(camera_id: int) -> list[Video]:
    camera_get(camera_id)
    return [Video.model_validate(dict(row)) for row in store.videos(camera_id)]


def _video_row(video_id: int) -> sqlite3.Row:
    row = store.video(video_id)
    if row is None:
        raise NotFound(texts.VIDEO_NOT_FOUND, video_id=video_id)
    return row


def video_get(video_id: int) -> Video:
    return Video.model_validate(dict(_video_row(video_id)))


def video_file(video_id: int) -> Path:
    path: Path = config.get_settings().data_dir / _video_row(video_id)["path"]
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
    return Job.model_validate({**dict(row), "metrics": metrics})


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
    job_id: int, stage: JobStage, span: tuple[float, float], model: ModelSpec, video: sqlite3.Row
) -> int:
    """Artifact id of `model` on the video: from the cache or from a backend run."""
    settings = config.get_settings()
    backend = _backend_instance()
    store.job_update(job_id, {"stage": stage})
    _progress(job_id, span[0])
    step = analysis_step(video["fps"])
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
) -> AnalysisResult:
    """Worker thread: read the artifacts, analyze, write hud.jsonl; the database stays out."""
    det = artifacts.read_jsonl(det_path, None)
    pose_frames = None if pose is None else artifacts.read_jsonl(pose[1], None)
    pose_model = None if pose is None else pose[0]
    result = pipeline.analyze(det, pose_frames, video_path, cfg, pose_model, det_model)
    hud_path.parent.mkdir(parents=True, exist_ok=True)
    lines = "".join(frame.model_dump_json() + "\n" for frame in result.hud)
    hud_path.write_text(lines, encoding="utf-8", newline="\n")
    return result


async def _analyze(
    job_id: int,
    video: sqlite3.Row,
    det: tuple[ModelSpec, int],
    pose: tuple[ModelSpec, int] | None,
) -> tuple[list[tuple[int, EpisodeDraft]], list[HudFrame]]:
    """Stage `analysis` of tech.md 8.1: a new `analyses` version, its HUD file and episodes."""
    settings = config.get_settings()
    store.job_update(job_id, {"stage": "analysis"})
    _progress(job_id, 0.85)
    video_id = video["id"]
    version = store.analysis_next_version(video_id)
    rel = f"analyses/{video_id}-v{version}/hud.jsonl"
    cfg = AnalysisConfig(
        width=video["width"],
        height=video["height"],
        fps=video["fps"],
        step=analysis_step(video["fps"]),
        duration_ms=video["duration_ms"],
        calibration=None,  # slice 9
        zones=[],  # slice 9
        rules={},  # slice 9
        class_conf=settings.class_conf,
        active_classes=registry.active_classes(settings),
    )
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
) -> tuple[tuple[ModelSpec, int], tuple[ModelSpec, int] | None] | None:
    """Artifacts of the active analysis for a recompute; `None` when a file is gone."""
    analysis = store.analysis(video["active_analysis_id"] or 0)
    if analysis is None:
        return None
    det = _stored_artifact(analysis["det_artifact_id"])
    pose_id = analysis["pose_artifact_id"]
    pose = None if pose_id is None else _stored_artifact(pose_id)
    if det is None or (pose_id is not None and pose is None):
        return None
    return det, pose


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
        if row["kind"] == "recompute":  # the same artifacts, no inference (tech.md 8.12)
            inputs = _analysis_inputs(video)
            if inputs is None:
                raise InferenceError("artifacts_missing", texts.ARTIFACTS_MISSING)
            (detector, det_id), pose = inputs
            pose_id = None if pose is None else pose[1]
            store.job_update(job_id, {"det_artifact_id": det_id, "pose_artifact_id": pose_id})
        else:
            detector = registry.resolve(settings.pipeline.detector)
            det_id = await _infer(job_id, "inference_detect", (0.0, 0.45), detector, video)
            store.job_update(job_id, {"det_artifact_id": det_id})
            try:
                if settings.pipeline.pose is not None:
                    pose_model = registry.resolve(settings.pipeline.pose)
                    span = (0.45, 0.85)
                    pose_id = await _infer(job_id, "inference_pose", span, pose_model, video)
                    store.job_update(job_id, {"pose_artifact_id": pose_id})
                    pose = (pose_model, pose_id)
            except InferenceError as exc:
                if exc.code not in ("remote_error", "bad_output"):
                    raise
                pose_text = f"pose: {exc.message}"  # the analysis goes on without keypoints
        episodes, hud_frames = await _analyze(job_id, video, (detector, det_id), pose)
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
            started = _autostart(video) if row["kind"] == "process" else None
        if started is not None:
            hub.publish("broadcast.state", _broadcast_by_id(started))
    _publish_job(job_id)
    return job_get(job_id)


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
        calibration=None,  # slice 9
        zones=[],  # slice 9
        rules=[],  # slice 9
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
    empty = Percentiles(n=0, pending=0, p50=None, p95=None)  # notifications come in slice 6
    return SystemView(
        backend=settings.inference_backend,
        fake=settings.fake,
        backend_status=_backend_status or _unchecked(),
        queue=[_job(row) for row in store.queue_jobs()],
        recent_jobs=[_job(row) for row in store.finished_jobs(RECENT_JOBS)],
        cameras=camera_states(),
        models=registry.active_models(settings),
        latency=LatencyStats(notify_delay_s=empty, publish_lag_ms=empty),
        channels=[],  # slice 15
        server_now=clock.now(),
    )


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
    )


def _event_summary(event_id: int) -> EventSummary:
    row = store.event(event_id)
    assert row is not None  # the caller just wrote it
    return _summary(row)


def _system_action(event_id: int, action: str, before: str | None, after: str) -> None:
    values = {
        "event_id": event_id,
        "at": clock.iso(clock.now()),
        "actor_role": "system",
        "actor_name": texts.DEMO_ACTOR["system"],
        "action": action,
        "from_status": before,
        "to_status": after,
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
    for camera_state in cameras:
        if _camera_seen.get(camera_state.camera_id) != camera_state:
            _camera_seen[camera_state.camera_id] = camera_state
            hub.publish("camera.state", camera_state)
    for sector_state in sectors:
        if _sector_seen.get(sector_state.sector_id) != sector_state:
            _sector_seen[sector_state.sector_id] = sector_state
            hub.publish("sector.state", sector_state)
    return written


def _camera_state(row: sqlite3.Row) -> CameraState:
    """The first rule of tech.md 8.9 that fits; gaps of the analysis (rule 4) come in S11."""
    reason: NoObservationReason | None = None
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
    else:
        state, text = "normal", texts.STATE_NORMAL
    return CameraState(
        camera_id=row["camera_id"],
        sector_id=row["sector_id"],
        state=state,
        reason=reason,
        reason_text=text,
        freshness_ms=None,  # slice 11
        open_yellow=row["open_yellow"],
        open_red=row["open_red"],
    )


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
    video = None if video_row is None else Video.model_validate(dict(video_row))
    analysis = None if video is None or not video.active_analysis_id else video_analysis(video.id)
    (state,) = [c for c in camera_states() if c.camera_id == camera_id]
    return CameraLiveView(
        camera=camera,
        state=state,
        broadcast=broadcast,
        video=video,
        analysis=analysis,
        zones=[],  # slice 9
        calibration=None,  # slice 9
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
    params = rules.defaults(episode.scenario) | (rule.params if rule is not None else {})
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
        why = rules.PLUGINS[episode.scenario].explain(draft, provenance.rule_params)
    broadcast = store.camera_broadcast(row["camera_id"])
    allowed = [] if role is None else ROLE_ACTIONS[role]
    return EventDetail(
        event=_summary(row),
        episode=episode,
        why=why,
        actions=[EventAction.model_validate(dict(a)) for a in store.event_actions(event_id)],
        allowed_actions=[a for a in allowed if _steps(a, row) is not None],
        provenance=provenance,
        deliveries=[],  # slice 15
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
        r = rows.setdefault(k, CountRow(key=k, title=titles[k], count=0, confirmed=0, false_alarm=0))
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


def calibration_get(camera_id: int) -> Calibration | None:
    raise NotImplementedError("slice 9")


def calibration_set(camera_id: int, data: CalibrationIn, role: Role | None) -> Calibration:
    raise NotImplementedError("slice 9")


def calibration_delete(camera_id: int, role: Role | None) -> None:
    raise NotImplementedError("slice 9")


def zones_list(camera_id: int) -> list[Zone]:
    raise NotImplementedError("slice 9")


def zone_create(camera_id: int, data: ZoneIn, role: Role | None) -> Zone:
    raise NotImplementedError("slice 9")


def zone_update(zone_id: int, data: ZonePatch, role: Role | None) -> Zone:
    raise NotImplementedError("slice 9")


def zone_delete(zone_id: int, role: Role | None) -> None:
    raise NotImplementedError("slice 9")


def camera_rules(camera_id: int) -> list[CameraRule]:
    raise NotImplementedError("slice 9")


def camera_rule_set(
    camera_id: int, scenario: str, data: CameraRuleIn, role: Role | None
) -> CameraRule:
    raise NotImplementedError("slice 9")


def rules_screen_view() -> RulesScreenView:
    raise NotImplementedError("slice 9")


def events_list(f: EventFilter) -> EventPage:
    raise NotImplementedError("slice 12")


def events_export_csv(f: EventFilter) -> str:
    raise NotImplementedError("slice 12")


def journal_facets() -> JournalFacets:
    raise NotImplementedError("slice 12")


def ohs_stats_view(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    sector_id: int | None = None,
    camera_id: int | None = None,
    include_demo: bool = True,
) -> OhsStats:
    raise NotImplementedError("slice 13")


def management_view(weeks: int | None = None, include_demo: bool = True) -> ManagementStats:
    raise NotImplementedError("slice 13")


def eval_run(labels: Path, out_dir: Path | None = None) -> EvalReport:
    raise NotImplementedError("slice 14")


async def deliveries_flush() -> int:
    raise NotImplementedError("slice 15")
