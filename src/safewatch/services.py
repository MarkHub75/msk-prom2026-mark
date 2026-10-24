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
from datetime import datetime, timedelta
from pathlib import Path
from typing import get_args

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
    Episode,
    EpisodeDraft,
    EvalReport,
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
    ManagementStats,
    MasterInbox,
    Meta,
    ModelSpec,
    ModelsView,
    OhsStats,
    OperatorDashboard,
    Percentiles,
    Role,
    RoleMeta,
    RulesScreenView,
    Sector,
    SectorIn,
    SectorView,
    SeedReport,
    ShiftSummary,
    StatusMeta,
    SystemView,
    TracksWindow,
    UploadResult,
    Video,
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
        store.camera_delete(camera_id, clock.iso(clock.now()))


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
    video = _video_row(video_id)
    pose_text = None
    try:
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
        store.job_update(job_id, done | {"finished_at": clock.iso(clock.now())})
        store.video_update(video_id, {"status": "ready"})
    _publish_job(job_id)
    return job_get(job_id)


def camera_setup_view(camera_id: int) -> CameraSetupView:
    return CameraSetupView(
        camera=camera_get(camera_id),
        videos=videos_list(camera_id),
        jobs=[_job(row) for row in store.camera_jobs(camera_id)],
        calibration=None,  # slice 9
        zones=[],  # slice 9
        rules=[],  # slice 9
        broadcast=None,  # slice 6
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
        cameras=[],  # slice 6
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


def video_analysis(video_id: int) -> Analysis:
    video = _video_row(video_id)
    row = store.analysis(video["active_analysis_id"] or 0)
    if row is None:
        raise Conflict("video_not_ready", texts.VIDEO_NOT_READY)
    evidence: dict[int, list[Evidence]] = {}
    for e in store.analysis_evidence(row["id"]):
        item = Evidence(
            id=e["id"],
            kind=e["kind"],
            frame_idx=e["frame_idx"],
            ts_ms=e["ts_ms"],
            url=f"/api/evidence/{e['id']}/image",
            sha256=e["sha256"],
            objects=json.loads(e["objects_json"]),
        )
        evidence.setdefault(e["episode_id"], []).append(item)
    episodes = [
        Episode.model_validate(
            {
                **dict(ep),
                "scenario_title": texts.SCENARIO_TITLES[ep["scenario"]],
                "metrics": json.loads(ep["metrics_json"]),
                "evidence": evidence.get(ep["id"], []),
            }
        )
        for ep in store.episodes(row["id"])
    ]
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


def broadcast_get(camera_id: int) -> Broadcast | None:
    raise NotImplementedError("slice 6")


def broadcast_start(camera_id: int, data: BroadcastIn, role: Role | None) -> Broadcast:
    raise NotImplementedError("slice 6")


def broadcast_stop(camera_id: int, role: Role | None) -> None:
    raise NotImplementedError("slice 6")


def broadcast_tick() -> int:
    raise NotImplementedError("slice 6")


def camera_states() -> list[CameraState]:
    raise NotImplementedError("slice 6")


def operator_dashboard_view() -> OperatorDashboard:
    raise NotImplementedError("slice 6")


def operator_feed() -> list[EventSummary]:
    raise NotImplementedError("slice 6")


def sector_view(sector_id: int) -> SectorView:
    raise NotImplementedError("slice 6")


def camera_live_view(camera_id: int) -> CameraLiveView:
    raise NotImplementedError("slice 6")


async def camera_preview(camera_id: int) -> bytes:
    raise NotImplementedError("slice 6")


def event_detail(event_id: int, role: Role | None) -> EventDetail:
    raise NotImplementedError("slice 7")


def event_action(
    event_id: int, data: ActionIn, role: Role | None, actor: str | None
) -> EventDetail:
    raise NotImplementedError("slice 7")


def escalation_tick() -> int:
    raise NotImplementedError("slice 7")


def master_inbox_view() -> MasterInbox:
    raise NotImplementedError("slice 8")


def shift_summary_view(at: datetime | None = None) -> ShiftSummary:
    raise NotImplementedError("slice 8")


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
