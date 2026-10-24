"""REST and WebSocket (tech.md 6.4, 6.5). Handlers only call the facade."""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated, cast, get_args
from urllib.parse import unquote

from fastapi import APIRouter, Depends, FastAPI, Header, Query, Request, UploadFile, WebSocket
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.types import Scope
from starlette.websockets import WebSocketDisconnect

from safewatch import clock, registry, services, texts, worker
from safewatch.config import Settings
from safewatch.errors import AppError, RoleRequired, ValidationFailed
from safewatch.hub import Client, hub
from safewatch.types import (
    ActionIn,
    Analysis,
    ApiError,
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
    ShiftSummary,
    SystemView,
    TracksWindow,
    UploadResult,
    Video,
    WsHello,
    WsMessage,
    Zone,
    ZoneIn,
    ZonePatch,
)

CONTRACT_VERSION = "1.0.0"
UPLOAD_CHUNK = 1 << 20
WS_UNKNOWN_ROLE = 4400
WS_TOO_SLOW = 1013

# Every error body is ApiError (tech.md 6.2); 4XX also covers the 422 of a malformed request.
router = APIRouter(responses={"4XX": {"model": ApiError}, 501: {"model": ApiError}})


def _role(x_role: Annotated[str | None, Header(alias="X-Role")] = None) -> Role | None:
    if not x_role:
        return None
    if x_role not in get_args(Role):
        raise RoleRequired(texts.ROLE_REQUIRED)
    return cast(Role, x_role)


def _actor(x_actor: Annotated[str | None, Header(alias="X-Actor")] = None) -> str | None:
    if x_actor is None:
        return None
    name = unquote(x_actor).strip()
    if not 1 <= len(name) <= services.ACTOR_MAX:
        raise ValidationFailed(texts.ACTOR_INVALID, field="X-Actor")
    return name


RoleDep = Annotated[Role | None, Depends(_role)]
ActorDep = Annotated[str | None, Depends(_actor)]
FilterDep = Annotated[EventFilter, Query()]


# --- slice 0 -----------------------------------------------------------------------------
@router.get("/api/health")
async def health() -> Health:
    return services.health()


class _Done(Exception):
    """Ends the other loop of a WebSocket connection."""


async def _send_loop(websocket: WebSocket, client: Client) -> None:
    while (payload := await client.queue.get()) is not None:
        try:
            await websocket.send_text(payload)
        except (WebSocketDisconnect, RuntimeError):
            raise _Done from None  # the client left between two messages
    await websocket.close(code=WS_TOO_SLOW)
    raise _Done


async def _receive_loop(websocket: WebSocket) -> None:
    # The client sends nothing; receiving only notices the disconnect.
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        raise _Done from None


@router.websocket("/ws")
async def ws(websocket: WebSocket, role: str = "") -> None:
    await websocket.accept()
    if role not in get_args(Role):
        await websocket.close(code=WS_UNKNOWN_ROLE)
        return
    now = clock.now()
    hello = WsHello(server_now=now, contract=CONTRACT_VERSION, role=cast(Role, role))
    await websocket.send_text(WsMessage(type="hello", at=now, data=hello).model_dump_json())
    client = hub.connect(cast(Role, role))
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(_send_loop(websocket, client))
            tg.create_task(_receive_loop(websocket))
    except* _Done:
        pass
    finally:
        hub.disconnect(client)


# --- slice 1 -----------------------------------------------------------------------------
@router.get("/api/meta")
async def meta() -> Meta:
    return services.meta()


@router.get("/api/admin/cameras")
async def cameras_admin_view() -> CamerasAdminView:
    return services.cameras_admin_view()


@router.get("/api/sectors")
async def sectors_list() -> list[Sector]:
    return services.sectors_list()


@router.post("/api/sectors", status_code=201)
async def sector_create(data: SectorIn, role: RoleDep) -> Sector:
    return services.sector_create(data, role)


@router.put("/api/sectors/{sector_id}")
async def sector_update(sector_id: int, data: SectorIn, role: RoleDep) -> Sector:
    return services.sector_update(sector_id, data, role)


@router.delete("/api/sectors/{sector_id}", status_code=204)
async def sector_delete(sector_id: int, role: RoleDep) -> None:
    services.sector_delete(sector_id, role)


@router.get("/api/cameras")
async def cameras_list(sector_id: int | None = None) -> list[Camera]:
    return services.cameras_list(sector_id)


@router.post("/api/cameras", status_code=201)
async def camera_create(data: CameraIn, role: RoleDep) -> Camera:
    return services.camera_create(data, role)


@router.get("/api/cameras/{camera_id}")
async def camera_get(camera_id: int) -> Camera:
    return services.camera_get(camera_id)


@router.patch("/api/cameras/{camera_id}")
async def camera_update(camera_id: int, data: CameraPatch, role: RoleDep) -> Camera:
    return services.camera_update(camera_id, data, role)


@router.delete("/api/cameras/{camera_id}", status_code=204)
async def camera_delete(camera_id: int, role: RoleDep) -> None:
    services.camera_delete(camera_id, role)


# --- slice 2 -----------------------------------------------------------------------------
@router.post("/api/cameras/{camera_id}/videos", status_code=201)
async def video_upload(camera_id: int, file: UploadFile, role: RoleDep) -> UploadResult:
    async def chunks() -> AsyncIterator[bytes]:
        while chunk := await file.read(UPLOAD_CHUNK):
            yield chunk

    return await services.video_upload(camera_id, file.filename or "", chunks(), role)


@router.get("/api/cameras/{camera_id}/videos")
async def videos_list(camera_id: int) -> list[Video]:
    return services.videos_list(camera_id)


@router.get("/api/videos/{video_id}")
async def video_get(video_id: int) -> Video:
    return services.video_get(video_id)


@router.get("/api/videos/{video_id}/file")
async def video_file(video_id: int) -> FileResponse:
    # FileResponse answers Range requests with 206 (starlette 1.9).
    return FileResponse(services.video_file(video_id))


@router.get("/api/jobs")
async def jobs_list(status: JobStatus | None = None, limit: int = 50) -> list[Job]:
    return services.jobs_list(status, limit)


@router.get("/api/jobs/{job_id}")
async def job_get(job_id: int) -> Job:
    return services.job_get(job_id)


@router.get("/api/admin/cameras/{camera_id}")
async def camera_setup_view(camera_id: int) -> CameraSetupView:
    return services.camera_setup_view(camera_id)


# --- slice 3 -----------------------------------------------------------------------------
@router.post("/api/jobs/{job_id}/retry")
async def job_retry(job_id: int, role: RoleDep) -> Job:
    return services.job_retry(job_id, role)


@router.get("/api/system")
async def system_view() -> SystemView:
    return services.system_view()


@router.post("/api/system/backend-check")
async def backend_check() -> BackendStatus:
    return await services.backend_check(force=True)


@router.get("/api/models")
async def models_view() -> ModelsView:
    return services.models_view()


# --- slices 4, 5 -------------------------------------------------------------------------
@router.get("/api/videos/{video_id}/tracks")
async def video_tracks(video_id: int, from_ms: int, to_ms: int) -> TracksWindow:
    return services.video_tracks(video_id, from_ms, to_ms)


@router.get("/api/videos/{video_id}/analysis")
async def video_analysis(video_id: int) -> Analysis:
    return services.video_analysis(video_id)


@router.post("/api/videos/{video_id}/recompute", status_code=202)
async def video_recompute(video_id: int, role: RoleDep) -> Job:
    return services.video_recompute(video_id, role)


@router.get("/api/evidence/{evidence_id}/image")
async def evidence_image(evidence_id: int) -> FileResponse:
    return FileResponse(services.evidence_file(evidence_id), media_type="image/jpeg")


# --- slice 6 -----------------------------------------------------------------------------
@router.get("/api/cameras/{camera_id}/broadcast")
async def broadcast_get(camera_id: int) -> Broadcast | None:
    return services.broadcast_get(camera_id)


@router.post("/api/cameras/{camera_id}/broadcast", status_code=201)
async def broadcast_start(camera_id: int, data: BroadcastIn, role: RoleDep) -> Broadcast:
    return services.broadcast_start(camera_id, data, role)


@router.delete("/api/cameras/{camera_id}/broadcast", status_code=204)
async def broadcast_stop(camera_id: int, role: RoleDep) -> None:
    services.broadcast_stop(camera_id, role)


@router.get("/api/operator/dashboard")
async def operator_dashboard_view() -> OperatorDashboard:
    return services.operator_dashboard_view()


@router.get("/api/operator/feed")
async def operator_feed() -> list[EventSummary]:
    return services.operator_feed()


@router.get("/api/sectors/{sector_id}/view")
async def sector_view(sector_id: int) -> SectorView:
    return services.sector_view(sector_id)


@router.get("/api/cameras/{camera_id}/view")
async def camera_live_view(camera_id: int) -> CameraLiveView:
    return services.camera_live_view(camera_id)


@router.get("/api/cameras/{camera_id}/preview")
async def camera_preview(camera_id: int) -> Response:
    return Response(await services.camera_preview(camera_id), media_type="image/jpeg")


# --- slices 7, 8 -------------------------------------------------------------------------
# export.csv is declared before /api/events/{event_id}, or the id route would take it.
@router.get("/api/events/export.csv")
async def events_export_csv(f: FilterDep) -> Response:
    return Response(services.events_export_csv(f), media_type="text/csv; charset=utf-8")


@router.get("/api/events/{event_id}")
async def event_detail(event_id: int, role: RoleDep) -> EventDetail:
    return services.event_detail(event_id, role)


@router.post("/api/events/{event_id}/actions")
async def event_action(
    event_id: int, data: ActionIn, role: RoleDep, actor: ActorDep
) -> EventDetail:
    return services.event_action(event_id, data, role, actor)


@router.get("/api/master/inbox")
async def master_inbox_view() -> MasterInbox:
    return services.master_inbox_view()


@router.get("/api/master/shift")
async def shift_summary_view(at: datetime | None = None) -> ShiftSummary:
    return services.shift_summary_view(at)


# --- slice 9 -----------------------------------------------------------------------------
@router.get("/api/cameras/{camera_id}/calibration")
async def calibration_get(camera_id: int) -> Calibration | None:
    return services.calibration_get(camera_id)


@router.put("/api/cameras/{camera_id}/calibration")
async def calibration_set(camera_id: int, data: CalibrationIn, role: RoleDep) -> Calibration:
    return services.calibration_set(camera_id, data, role)


@router.delete("/api/cameras/{camera_id}/calibration", status_code=204)
async def calibration_delete(camera_id: int, role: RoleDep) -> None:
    services.calibration_delete(camera_id, role)


@router.get("/api/cameras/{camera_id}/zones")
async def zones_list(camera_id: int) -> list[Zone]:
    return services.zones_list(camera_id)


@router.post("/api/cameras/{camera_id}/zones", status_code=201)
async def zone_create(camera_id: int, data: ZoneIn, role: RoleDep) -> Zone:
    return services.zone_create(camera_id, data, role)


@router.patch("/api/zones/{zone_id}")
async def zone_update(zone_id: int, data: ZonePatch, role: RoleDep) -> Zone:
    return services.zone_update(zone_id, data, role)


@router.delete("/api/zones/{zone_id}", status_code=204)
async def zone_delete(zone_id: int, role: RoleDep) -> None:
    services.zone_delete(zone_id, role)


@router.get("/api/cameras/{camera_id}/rules")
async def camera_rules(camera_id: int) -> list[CameraRule]:
    return services.camera_rules(camera_id)


@router.put("/api/cameras/{camera_id}/rules/{scenario}")
async def camera_rule_set(
    camera_id: int, scenario: str, data: CameraRuleIn, role: RoleDep
) -> CameraRule:
    return services.camera_rule_set(camera_id, scenario, data, role)


@router.get("/api/ohs/rules")
async def rules_screen_view() -> RulesScreenView:
    return services.rules_screen_view()


# --- slices 12, 13 -----------------------------------------------------------------------
@router.get("/api/events")
async def events_list(f: FilterDep) -> EventPage:
    return services.events_list(f)


@router.get("/api/journal/facets")
async def journal_facets() -> JournalFacets:
    return services.journal_facets()


@router.get("/api/stats/ohs")
async def ohs_stats_view(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    sector_id: int | None = None,
    camera_id: int | None = None,
    include_demo: bool = True,
) -> OhsStats:
    return services.ohs_stats_view(date_from, date_to, sector_id, camera_id, include_demo)


@router.get("/api/stats/management")
async def management_view(weeks: int | None = None, include_demo: bool = True) -> ManagementStats:
    return services.management_view(weeks, include_demo)


# --- app ---------------------------------------------------------------------------------
def _error(status: int, code: str, message: str, details: dict[str, object]) -> JSONResponse:
    body = ApiError.model_validate({"code": code, "message": message, "details": details})
    return JSONResponse(body.model_dump(), status_code=status)


async def _app_error(request: Request, exc: Exception) -> JSONResponse:
    err = cast(AppError, exc)
    return _error(err.status, err.code, err.message, dict(err.details))


async def _not_implemented(request: Request, exc: Exception) -> JSONResponse:
    slice_no = str(exc).removeprefix("slice ").strip()
    message = texts.NOT_IMPLEMENTED.format(slice=slice_no)
    return _error(501, "not_implemented", message, {"slice": slice_no})


async def _invalid_request(request: Request, exc: Exception) -> JSONResponse:
    errors = cast(RequestValidationError, exc).errors()
    field = ".".join(str(part) for part in errors[0]["loc"]) if errors else None
    return _error(422, "validation", texts.REQUEST_INVALID, {"field": field})


class _Frontend(StaticFiles):
    """The built frontend; unknown paths get index.html for the client-side router."""

    async def get_response(self, path: str, scope: Scope) -> Response:
        try:
            return await super().get_response(path, scope)
        except HTTPException as exc:
            if exc.status_code != 404 or scope["path"].startswith("/api/"):
                raise
            return await super().get_response("index.html", scope)


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    stop = asyncio.Event()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker.run_forever(stop))
        yield
        stop.set()


def create_app(settings: Settings) -> FastAPI:
    registry.active_models(settings)  # an unknown model reference stops the start
    # The title is fixed: contract/openapi.json must not depend on the owner's config.
    app = FastAPI(title="SafeWatch API", version=CONTRACT_VERSION, lifespan=_lifespan)
    app.add_exception_handler(AppError, _app_error)
    app.add_exception_handler(NotImplementedError, _not_implemented)
    app.add_exception_handler(RequestValidationError, _invalid_request)
    app.include_router(router)
    if settings.server.static_dir.is_dir():
        app.mount("/", _Frontend(directory=settings.server.static_dir, html=True), name="frontend")
    return app
