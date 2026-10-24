"""Facade (tech.md 6.2): the one entry point for API, CLI, worker and tests.

Functions of slices that are not built yet raise `NotImplementedError("slice N")`; the API
answers them with 501 `not_implemented`.
"""

from collections.abc import AsyncIterator
from datetime import datetime
from pathlib import Path

from safewatch import seed
from safewatch.errors import NotFound
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
    EventSummary,
    Health,
    Job,
    JobStatus,
    JournalFacets,
    ManagementStats,
    MasterInbox,
    Meta,
    ModelsView,
    OhsStats,
    OperatorDashboard,
    Role,
    RulesScreenView,
    Sector,
    SectorIn,
    SectorView,
    SeedReport,
    ShiftSummary,
    SystemView,
    TracksWindow,
    UploadResult,
    Video,
    Zone,
    ZoneIn,
    ZonePatch,
)

ACTOR_MAX = 60


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


def meta() -> Meta:
    raise NotImplementedError("slice 1")


def cameras_admin_view() -> CamerasAdminView:
    raise NotImplementedError("slice 1")


def sectors_list() -> list[Sector]:
    raise NotImplementedError("slice 1")


def sector_create(data: SectorIn, role: Role | None) -> Sector:
    raise NotImplementedError("slice 1")


def sector_update(sector_id: int, data: SectorIn, role: Role | None) -> Sector:
    raise NotImplementedError("slice 1")


def sector_delete(sector_id: int, role: Role | None) -> None:
    raise NotImplementedError("slice 1")


def cameras_list(sector_id: int | None = None) -> list[Camera]:
    raise NotImplementedError("slice 1")


def camera_get(camera_id: int) -> Camera:
    raise NotImplementedError("slice 1")


def camera_create(data: CameraIn, role: Role | None) -> Camera:
    raise NotImplementedError("slice 1")


def camera_update(camera_id: int, data: CameraPatch, role: Role | None) -> Camera:
    raise NotImplementedError("slice 1")


def camera_delete(camera_id: int, role: Role | None) -> None:
    raise NotImplementedError("slice 1")


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
