"""Facade (tech.md 6.2): the one entry point for API, CLI, worker and tests.

Functions of slices that are not built yet raise `NotImplementedError("slice N")`; the API
answers them with 501 `not_implemented`.
"""

import sqlite3
from collections.abc import AsyncIterator
from datetime import datetime
from pathlib import Path
from typing import get_args

from safewatch import clock, config, seed, store, texts
from safewatch.errors import Conflict, Forbidden, NotFound, RoleRequired, ValidationFailed
from safewatch.texts import VIDEOS_DIR_MISSING
from safewatch.types import (
    ActionIn,
    Analysis,
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
    EvalReport,
    EventDetail,
    EventFilter,
    EventPage,
    EventStatus,
    EventSummary,
    Health,
    HumanAction,
    Job,
    JobStatus,
    JournalFacets,
    Level,
    LevelMeta,
    ManagementStats,
    MasterInbox,
    Meta,
    ModelsView,
    OhsStats,
    OperatorDashboard,
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

ACTOR_MAX = 60
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
        # rules.scenario_metas() arrives with the first plugins in slice 5.
        scenarios=[],
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


async def video_upload(
    camera_id: int, filename: str, chunks: AsyncIterator[bytes], role: Role | None
) -> UploadResult:
    raise NotImplementedError("slice 2")


def video_import(camera_id: int, path: Path) -> UploadResult:
    raise NotImplementedError("slice 2")


def videos_list(camera_id: int) -> list[Video]:
    raise NotImplementedError("slice 2")


def video_get(video_id: int) -> Video:
    raise NotImplementedError("slice 2")


def video_file(video_id: int) -> Path:
    raise NotImplementedError("slice 2")


def jobs_list(status: JobStatus | None = None, limit: int = 50) -> list[Job]:
    raise NotImplementedError("slice 2")


def job_get(job_id: int) -> Job:
    raise NotImplementedError("slice 2")


async def run_next_job() -> Job | None:
    raise NotImplementedError("slice 2")


def camera_setup_view(camera_id: int) -> CameraSetupView:
    raise NotImplementedError("slice 2")


def job_retry(job_id: int, role: Role | None) -> Job:
    raise NotImplementedError("slice 3")


def recover_jobs() -> int:
    raise NotImplementedError("slice 3")


async def backend_check(force: bool = False) -> BackendStatus:
    raise NotImplementedError("slice 3")


def models_view() -> ModelsView:
    raise NotImplementedError("slice 3")


def system_view() -> SystemView:
    raise NotImplementedError("slice 3")


def video_tracks(video_id: int, from_ms: int, to_ms: int) -> TracksWindow:
    raise NotImplementedError("slice 4")


def video_analysis(video_id: int) -> Analysis:
    raise NotImplementedError("slice 5")


def video_recompute(video_id: int, role: Role | None) -> Job:
    raise NotImplementedError("slice 5")


def evidence_file(evidence_id: int) -> Path:
    raise NotImplementedError("slice 5")


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
