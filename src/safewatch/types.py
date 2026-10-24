"""Contract types (tech.md 5.2) and protocols (tech.md 6.1). Names here are frozen."""

from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Literal, Protocol

from pydantic import BaseModel

Level = Literal["yellow", "red"]
Role = Literal["operator", "master", "ohs", "management", "admin"]
ActorRole = Literal["operator", "master", "ohs", "management", "admin", "system"]
EventStatus = Literal[
    "new",
    "viewed",
    "confirmed",
    "false_alarm",
    "sent_to_master",
    "master_accepted",
    "resolved",
    "auto_finished",
    "superseded",
]
Verdict = Literal["none", "confirmed", "false_alarm"]
HumanAction = Literal["view", "confirm", "false_alarm", "send_to_master", "accept", "resolve"]
LogAction = Literal[
    "published",
    "viewed",
    "confirmed",
    "false_alarm",
    "sent_to_master",
    "level_escalated",
    "timeout_escalated",
    "master_accepted",
    "resolved",
    "auto_finished",
    "superseded",
    "identified",
]
EventMode = Literal["replay", "demo"]
CameraStateKind = Literal["normal", "yellow", "red", "no_observation"]
NoObservationReason = Literal[
    "no_source", "processing", "failed", "ended", "stale", "dark", "obstructed"
]
VideoStatus = Literal["uploaded", "processing", "ready", "failed"]
JobKind = Literal["process", "recompute"]
JobStatus = Literal["queued", "running", "retry_wait", "done", "failed"]
JobStage = Literal["queued", "inference_detect", "inference_pose", "analysis", "evidence", "done"]
JobErrorCode = Literal[
    "linq_unavailable",
    "timeout",
    "remote_error",
    "bad_output",
    "model_missing",
    "video_unreadable",
    "artifacts_missing",
    "internal",
]
Fault = Literal["unavailable", "timeout", "remote_error", "bad_output"]
BackendName = Literal["linq", "local"]
BackendState = Literal["ok", "models_missing", "unreachable", "bad_answer", "unchecked"]
ModelTask = Literal["detect", "pose"]
ObsState = Literal["P", "N", "U"]
EndReason = Literal["observed_exit", "track_lost_timeout", "video_end"]
ScenarioStatus = Literal["active", "model_missing", "skeleton"]
BroadcastStatus = Literal["playing", "stopped", "ended"]
ZoneGeometry = Literal["polygon", "line"]
ObjectKind = Literal["person", "vehicle", "phone", "other"]
Posture = Literal["upright", "lying", "unknown"]
Sound = Literal["siren", "chime", "none"]
DeliveryKind = Literal["published", "escalated", "to_master"]
# m/s from the homography, m/s from autocal, body heights/s
SpeedSource = Literal["calibration", "auto", "relative"]
PassportVerdict = Literal["suitable", "partial", "unsuitable", "unknown"]
CalcTier = Literal["base", "extended", "max"]
WsType = Literal[
    "hello",
    "event.created",
    "event.updated",
    "event.escalated",
    "notification",
    "camera.state",
    "sector.state",
    "job.progress",
    "broadcast.state",
    "backend.status",
]

Point = tuple[float, float]  # normalized image coords (0..1) or meters on the floor
Box = tuple[float, float, float, float]  # x1, y1, x2, y2
Keypoint = tuple[float, float, float]  # x, y, conf


# --- common, meta ------------------------------------------------------------------------
class ApiError(BaseModel):
    code: str
    message: str  # Russian, shown to the user as is
    details: dict[str, str | int | float | None] = {}


class Health(BaseModel):
    status: Literal["ok"]
    contract: str


class LevelMeta(BaseModel):
    id: Level
    title: str
    color: str


class StatusMeta(BaseModel):
    id: EventStatus
    title: str
    terminal: bool


class RoleMeta(BaseModel):
    id: Role
    title: str
    actions: list[HumanAction]


class ZoneKindMeta(BaseModel):
    id: str
    title: str
    color: str
    geometry: ZoneGeometry
    description: str


class ScenarioParam(BaseModel):
    key: str
    title: str
    unit: str
    default: float
    min: float
    max: float


class ScenarioMeta(BaseModel):
    id: str
    title: str
    description: str
    icon: str
    default_level: Level
    status: ScenarioStatus
    status_text: str
    required_classes: list[str]
    zone_kinds: list[str]
    params: list[ScenarioParam]


class Meta(BaseModel):
    product_name: str
    contract: str
    inference_backend: BackendName
    fake: bool
    timezone: str
    roles: list[RoleMeta]
    levels: list[LevelMeta]
    statuses: list[StatusMeta]
    zone_kinds: list[ZoneKindMeta]
    scenarios: list[ScenarioMeta]


class SeedReport(BaseModel):
    skipped: bool
    sectors: int
    cameras: int
    zones: int
    events: int
    videos: int


# --- sectors, cameras --------------------------------------------------------------------
class Sector(BaseModel):
    id: int
    name: str
    sort_order: int
    is_demo: bool


class SectorIn(BaseModel):
    name: str
    sort_order: int = 0


class Camera(BaseModel):
    id: int
    sector_id: int
    name: str
    description: str
    is_demo: bool
    has_calibration: bool
    zones_count: int
    videos_count: int


class CameraIn(BaseModel):
    sector_id: int
    name: str
    description: str = ""


class CameraPatch(BaseModel):
    sector_id: int | None = None
    name: str | None = None
    description: str | None = None


class CamerasAdminView(BaseModel):
    sectors: list[Sector]
    cameras: list[Camera]


# --- v5: used by the types below (tech.md 6.11.2) ---------------------------------------
class AutoCalibration(BaseModel):  # analyses.autocal_json (S19, tech.md 8.21)
    ok: bool
    reason: str  # Russian; "" when ok
    samples: int  # standing people kept after outlier rejection
    a_px: float  # person height in px at foot y = 0
    b: float  # px of height per px of foot y
    rmse_px: float
    r2: float
    person_height_m: float


class Clip(BaseModel):  # window of the source video (S18, tech.md 8.20)
    video_id: int
    url: str  # /api/videos/<id>/file#t=<start_s>,<end_s>
    start_ms: int
    end_ms: int
    playable: bool  # the served file plays in a browser


# --- videos, jobs, models ----------------------------------------------------------------
class Video(BaseModel):
    id: int
    camera_id: int
    filename: str
    sha256: str
    size_bytes: int
    width: int
    height: int
    fps: float
    frame_count: int
    duration_ms: int
    codec: str
    browser_playable: bool
    status: VideoStatus
    active_analysis_id: int | None
    created_at: datetime
    web_playable: bool = False


class InferenceMetrics(BaseModel):
    backend: BackendName
    fake: bool
    model_id: str
    model_version: str
    task: ModelTask
    input_size: int
    step: int
    frames_processed: int
    wall_s: float  # processing time without upload and polling
    throughput_fps: float
    preprocess_ms: float | None
    postprocess_ms: float | None
    tpu_rtt_p50_ms: float | None  # linq only
    tpu_rtt_p90_ms: float | None
    upload_s: float | None  # linq only
    total_s: float  # end to end: upload, start, polling, download
    cached: bool


class Job(BaseModel):
    id: int
    kind: JobKind
    video_id: int
    camera_id: int
    backend: BackendName
    fake: bool
    status: JobStatus
    stage: JobStage
    progress: float
    attempts: int
    next_attempt_at: datetime | None
    error_code: JobErrorCode | None
    error_text: str | None
    metrics: list[InferenceMetrics]
    analysis_id: int | None
    analysis_ms: int | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    status_text: str = ""
    eta_s: float | None = None
    rate_fps: float | None = None


class UploadResult(BaseModel):
    video: Video
    job: Job | None  # None: the same file is already processed for this camera
    reused: bool


class ModelSpec(BaseModel):
    id: str
    version: str
    task: ModelTask
    input_size: int
    conf: float  # floor written to JSONL; rule thresholds live in class_conf
    iou: float
    classes: dict[int, str]  # kept classes: id -> name used by rules
    linq_program: str | None
    linq_tail: str | None  # local path of the tail ONNX, uploaded next to the worker
    local_onnx: str | None
    nc: int | None = None
    input_name: str = "images"


class ModelsView(BaseModel):
    backend: BackendName
    fake: bool
    active: list[ModelSpec]
    available: list[ModelSpec]


class BackendStatus(BaseModel):
    backend: BackendName
    fake: bool
    state: BackendState
    checked_at: datetime | None
    latency_ms: float | None
    present: list[str]  # programs or model files found
    missing: list[str]
    message: str


# --- HUD, analysis -----------------------------------------------------------------------
class HudTag(BaseModel):
    code: (
        str  # "speed", "zone", "lying", "still", "phone", "feet_hidden", "too_small", "<scenario>"
    )
    text: str  # "бег 3,1 м/с"
    level: Level | None


class HudObject(BaseModel):
    track_id: int | None
    kind: ObjectKind
    label: str  # "человек", "грузовик", "телефон"
    score: float
    bbox: Box  # normalized 0..1
    kpts: list[Keypoint] | None  # normalized x, y and conf, 17 COCO points
    tags: list[HudTag]
    projection: list[Point] | None = None


class HudFrame(BaseModel):
    frame_idx: int
    ts_ms: int
    objects: list[HudObject]


class TracksWindow(BaseModel):
    video_id: int
    analysis_id: int
    from_ms: int
    to_ms: int
    frames: list[HudFrame]


class ObservabilityGap(BaseModel):
    start_ms: int
    end_ms: int
    reason: NoObservationReason  # stale | dark | obstructed


class Evidence(BaseModel):
    id: int
    kind: Literal["confirm", "escalate"]
    frame_idx: int
    ts_ms: int
    url: str
    sha256: str
    objects: list[HudObject]


class Episode(BaseModel):
    id: int
    analysis_id: int
    scenario: str
    scenario_title: str
    subject: str
    zone_id: int | None
    level_initial: Level
    level_max: Level
    start_ms: int
    confirm_ms: int
    escalate_ms: int | None
    end_ms: int
    end_reason: EndReason
    reason_code: str
    reason_text: str
    method: str
    confidence: float
    metrics: dict[str, float]
    uncertain_ms: int
    evidence: list[Evidence]


class Analysis(BaseModel):
    id: int
    video_id: int
    version: int
    created_at: datetime
    duration_ms: int
    pose_used: bool
    episodes: list[Episode]
    gaps: list[ObservabilityGap]
    auto_calibration: AutoCalibration | None = None


# --- calibration, zones, rules -----------------------------------------------------------
class ControlPoint(BaseModel):
    image: Point
    world: Point


class CalibrationIn(BaseModel):
    image_points: list[Point]
    world_points: list[Point]
    control_points: list[ControlPoint] = []


class Calibration(BaseModel):
    camera_id: int
    image_points: list[Point]
    world_points: list[Point]
    control_points: list[ControlPoint]
    fit_rmse_m: float
    control_rmse_m: float | None
    grid: list[tuple[Point, Point]]  # normalized segments of the 1 m floor grid
    updated_at: datetime


class Zone(BaseModel):
    id: int
    camera_id: int
    kind: str
    name: str
    points: list[Point]


class ZoneIn(BaseModel):
    kind: str
    name: str
    points: list[Point]


class ZonePatch(BaseModel):
    name: str | None = None
    points: list[Point] | None = None


class CameraRule(BaseModel):
    camera_id: int
    scenario: str
    enabled: bool
    params: dict[str, float]  # overrides
    effective: dict[str, float]  # defaults from config + overrides
    status: ScenarioStatus


class CameraRuleIn(BaseModel):
    enabled: bool
    params: dict[str, float] = {}


class RulesScreenRow(BaseModel):
    camera: Camera
    rules: list[CameraRule]


class RulesScreenView(BaseModel):
    scenarios: list[ScenarioMeta]
    rows: list[RulesScreenRow]


# --- broadcast, states -------------------------------------------------------------------
class Broadcast(BaseModel):
    id: int
    camera_id: int
    video_id: int
    analysis_id: int
    status: BroadcastStatus
    loop: bool
    cycle: int
    started_at: datetime
    position_ms: int
    duration_ms: int
    server_now: datetime


class BroadcastIn(BaseModel):
    video_id: int | None = None  # None: the latest ready video of the camera
    loop: bool | None = None  # None: broadcast.loop_default


class CameraState(BaseModel):
    camera_id: int
    sector_id: int
    state: CameraStateKind
    reason: NoObservationReason | None
    reason_text: str
    freshness_ms: int | None
    open_yellow: int
    open_red: int


class SectorState(BaseModel):
    sector_id: int
    name: str
    state: CameraStateKind
    reason_text: str
    cameras_total: int
    cameras_no_observation: int
    open_yellow: int
    open_red: int


class CameraSetupView(BaseModel):
    camera: Camera
    videos: list[Video]
    jobs: list[Job]
    calibration: Calibration | None
    zones: list[Zone]
    rules: list[CameraRule]
    broadcast: Broadcast | None
    auto_calibration: AutoCalibration | None = None


# --- events ------------------------------------------------------------------------------
class EventSummary(BaseModel):
    id: int
    scenario: str
    title: str
    level: Level
    status: EventStatus
    status_title: str
    operator_verdict: Verdict
    escalated_by_timeout: bool
    mode: EventMode
    camera_id: int
    camera_name: str
    sector_id: int
    sector_name: str
    zone_id: int | None
    zone_name: str | None
    reason_text: str
    notification_text: str
    started_at: datetime
    published_at: datetime
    red_at: datetime | None
    ended_at: datetime | None
    duration_s: float  # until ended_at, or until now while the episode lasts
    priority: int
    is_demo: bool
    evidence_url: str | None = None  # confirm frame of the episode (GAP S12), None for demo
    clip: Clip | None = None
    person_name: str = ""
    person_position: str = ""
    crew: str = ""


class OperatorDashboard(BaseModel):
    sectors: list[SectorState]
    feed: list[EventSummary]
    server_now: datetime


class CameraTile(BaseModel):
    camera: Camera
    state: CameraState
    broadcast: Broadcast | None
    preview_url: str | None


class SectorView(BaseModel):
    sector: SectorState
    cameras: list[CameraTile]
    feed: list[EventSummary]


class CameraLiveView(BaseModel):
    camera: Camera
    state: CameraState
    broadcast: Broadcast | None
    video: Video | None
    analysis: Analysis | None
    zones: list[Zone]
    calibration: Calibration | None


class WhyItem(BaseModel):
    label: str
    value: str


class EventAction(BaseModel):
    id: int
    at: datetime
    actor_role: ActorRole
    actor_name: str
    action: LogAction
    from_status: EventStatus | None
    to_status: EventStatus | None
    comment: str


class Provenance(BaseModel):
    backend: BackendName | None
    fake: bool
    det_model: str | None  # "det-yolov8n@640-ap9999"
    pose_model: str | None
    job_id: int | None
    video_sha256: str | None
    analysis_version: int | None
    rule_params: dict[str, float]
    evidence_sha256: str | None


class Delivery(BaseModel):
    channel: str
    kind: DeliveryKind
    status: Literal["sent", "failed"]
    http_status: int | None
    error: str
    at: datetime
    delivered_at: datetime | None = None
    status_text: str = ""


class EventDetail(BaseModel):
    event: EventSummary
    episode: Episode | None  # None for demo events
    why: list[WhyItem]
    actions: list[EventAction]
    allowed_actions: list[HumanAction]  # for the X-Role of the request
    provenance: Provenance
    deliveries: list[Delivery]
    video_id: int | None
    video_start_ms: int | None
    video_end_ms: int | None
    broadcast: Broadcast | None  # current broadcast of the camera, for the live half
    can_identify: bool = False


class ActionIn(BaseModel):
    action: HumanAction
    comment: str = ""


class EventFilter(BaseModel):
    level: Level | None = None
    scenario: str | None = None
    status: EventStatus | None = None
    sector_id: int | None = None
    camera_id: int | None = None
    zone_id: int | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    q: str | None = None
    include_demo: bool = True
    include_superseded: bool = False
    limit: int = 50
    cursor: str | None = None


class EventPage(BaseModel):
    items: list[EventSummary]
    total: int
    next_cursor: str | None


class FacetItem(BaseModel):
    id: str
    title: str


class JournalFacets(BaseModel):
    scenarios: list[FacetItem]
    levels: list[FacetItem]
    statuses: list[FacetItem]
    sectors: list[FacetItem]
    cameras: list[FacetItem]
    zones: list[FacetItem]


class MasterInbox(BaseModel):
    active: list[EventSummary]  # sent_to_master, master_accepted
    recent_resolved: list[EventSummary]
    server_now: datetime


class CountRow(BaseModel):
    key: str
    title: str
    count: int
    confirmed: int
    false_alarm: int


class ShiftSummary(BaseModel):
    shift_id: str
    title: str
    start: datetime
    end: datetime
    total: int
    by_sector: list[CountRow]
    by_scenario: list[CountRow]
    events: list[EventSummary]


# --- stats, system -----------------------------------------------------------------------
class Percentiles(BaseModel):
    n: int
    pending: int
    p50: float | None
    p95: float | None


class DayRow(BaseModel):
    date: str  # YYYY-MM-DD in Europe/Moscow
    yellow: int
    red: int
    confirmed: int
    false_alarm: int


class OhsStats(BaseModel):
    date_from: datetime
    date_to: datetime
    include_demo: bool
    total: int
    by_status: list[CountRow]
    by_scenario: list[CountRow]
    by_sector: list[CountRow]
    by_camera: list[CountRow]
    by_shift: list[CountRow]
    by_hour: list[CountRow]
    by_day: list[DayRow]
    reviewed: int
    false_alarm_share: float | None
    review_coverage: float | None
    operator_reaction_s: Percentiles
    master_accept_s: Percentiles
    master_resolve_s: Percentiles


class WeekRow(BaseModel):
    week_start: str  # Monday, YYYY-MM-DD in Europe/Moscow
    yellow: int
    red: int
    confirmed: int
    false_alarm: int


class RateRow(BaseModel):
    key: str
    title: str
    cameras: int
    confirmed: int
    per_camera: float | None


class TrendSummary(BaseModel):
    previous: int
    recent: int
    change_pct: float | None
    text: str


class ManagementStats(BaseModel):
    weeks: list[WeekRow]
    top_sectors: list[RateRow]
    top_scenarios: list[CountRow]
    yellow_trend: TrendSummary


class LatencyStats(BaseModel):
    notify_delay_s: Percentiles  # published_at - started_at
    publish_lag_ms: Percentiles  # published_at - planned confirm wall time


class Channel(BaseModel):
    name: str
    kind: Literal["ws", "webhook", "call"]
    target: str  # host only, never a full URL with secrets
    levels: list[Level]


class SystemView(BaseModel):
    backend: BackendName
    fake: bool
    backend_status: BackendStatus
    queue: list[Job]
    recent_jobs: list[Job]
    cameras: list[CameraState]
    models: list[ModelSpec]
    latency: LatencyStats
    channels: list[Channel]
    server_now: datetime


# --- realtime ----------------------------------------------------------------------------
class Notification(BaseModel):
    id: str
    event_id: int
    level: Level
    text: str
    audience: list[Role]
    sound: Sound
    takeover: bool


class WsHello(BaseModel):
    server_now: datetime
    contract: str
    role: Role


class WsMessage(BaseModel):
    type: WsType
    at: datetime
    data: (
        WsHello
        | EventSummary
        | Notification
        | CameraState
        | SectorState
        | Job
        | Broadcast
        | BackendStatus
    )


# --- v5 (tech.md 6.11.2) -----------------------------------------------------------------
class DemoArtifact(BaseModel):  # one model run of one video inside a demo pack (S17)
    model: str  # id@version
    task: ModelTask
    input_size: int
    step: int
    backend: BackendName
    fake: bool
    file: str  # artifacts/<cache_key>.jsonl, relative to the pack
    frames: int
    metrics: InferenceMetrics


class DemoVideo(BaseModel):
    file: str  # videos/<name> in a pack; a path under --videos in a layout
    sha256: str = ""
    artifacts: list[DemoArtifact] = []


class DemoCamera(BaseModel):
    sector: str  # matched by name, created when missing
    name: str  # matched by name inside the sector, created when missing
    description: str = ""
    videos: list[DemoVideo]
    calibration: CalibrationIn | None = None
    zones: list[ZoneIn] = []
    rules: dict[str, CameraRuleIn] = {}


class DemoManifest(BaseModel):  # data/demo/<name>/manifest.json
    name: str
    created_at: datetime
    contract: str
    cameras: list[DemoCamera]


class DemoLayout(BaseModel):  # config/demo.example.yaml: input of `safewatch demo build`
    name: str
    cameras: list[DemoCamera]


class DemoPack(BaseModel):  # GET /api/demo/packs
    id: int
    name: str
    sha256: str
    backend: BackendName
    fake: bool
    cameras: int
    videos: int
    imported_at: datetime


class DemoImportReport(BaseModel):
    skipped: bool  # the pack with this name is already imported
    name: str
    cameras: int
    videos: int
    jobs: int


# Every number of the calculator is one of these (S24, tech.md 8.25).
class CalcAssumption(BaseModel):
    key: str
    title: str
    value: float
    unit: str
    source: str  # where the number comes from, Russian
    editable: bool = True


class RolloutIn(BaseModel):
    workshops: int
    cameras: int
    shifts_per_day: int
    workers: int
    operators: int
    incidents_per_year: float
    downtime_cost_rub: float  # per incident
    fine_cost_rub: float
    treatment_cost_rub: float
    lawsuit_cost_rub: float
    overrides: dict[str, float] = {}  # CalcAssumption.key -> value


class TierResult(BaseModel):
    tier: CalcTier
    title: str
    accelerators: int
    servers: int
    capex_rub: float
    opex_rub_year: float
    savings_rub_year: float
    payback_months: float | None  # None: savings do not exceed opex
    items: list[WhyItem]  # breakdown lines


class RolloutResult(BaseModel):
    incident_cost_rub: float
    incidents_per_1000_workers: float | None
    events_per_operator_shift: float | None  # from the journal, None without data
    tiers: list[TierResult]
    assumptions: list[CalcAssumption]


class ScaleIn(BaseModel):
    cameras_now: int
    new_cameras: int
    overrides: dict[str, float] = {}


class ScaleResult(BaseModel):
    cameras_total: int
    analysis_fps: float
    capacity_fps: float  # per accelerator
    capacity_source: str
    accelerators_now: int
    accelerators_total: int
    servers_total: int
    capex_rub: float  # for the added part only
    items: list[WhyItem]
    assumptions: list[CalcAssumption]


class CalculatorDefaults(BaseModel):
    rollout: RolloutIn
    scale: ScaleIn
    assumptions: list[CalcAssumption]
    measured: list[CalcAssumption]  # numbers from LinQ runs and the journal, editable=False


class DatasetItem(BaseModel):  # S25, tech.md 8.26
    event_id: int
    scenario: str
    label: Literal["false_alarm"]
    frames: int
    path: str
    created_at: datetime


class DatasetView(BaseModel):
    items: list[DatasetItem]
    total: int
    frames: int


class IdentityIn(BaseModel):  # S26, tech.md 8.27; empty string clears the field
    person_name: str = ""
    person_position: str = ""
    crew: str = ""


class PeopleStats(BaseModel):
    date_from: datetime
    date_to: datetime
    include_demo: bool
    total: int
    identified: int
    by_person: list[CountRow]
    by_crew: list[CountRow]


class PassportScenario(BaseModel):  # S27, tech.md 8.28
    scenario: str
    title: str
    verdict: PassportVerdict
    reason: str


class CameraPassport(BaseModel):
    camera_id: int
    analysis_id: int | None
    frames: int
    person_height_px_p50: float | None
    small_object_px_p50: float | None
    person_frames_share: float | None
    dark_share: float | None
    empty_share: float | None
    shift_px: float | None = None  # S32
    shift_text: str = ""  # S32
    scenarios: list[PassportScenario]


# --- pipeline (internal) -----------------------------------------------------------------
class Detection(BaseModel):  # one item of an artifact JSONL line, pixels of the source frame
    cls: int
    name: str
    score: float
    bbox_xyxy: Box
    kpts: list[Keypoint] | None = None


class FrameDetections(BaseModel):  # one artifact JSONL line
    frame_idx: int
    ts_ms: float
    detections: list[Detection]


class PersonState(BaseModel):
    track_id: int
    bbox: Box  # pixels
    score: float
    foot: Point  # pixels, bbox bottom center
    anchor: Point  # pixels: lowest visible ankle, else foot
    feet_visible: bool
    ground: Point | None  # meters, only inside the calibrated hull
    height_px: float
    ref_height_px: float  # H_ref: median upright height, frozen while lying
    speed_bh_s: float | None
    speed_m_s: float | None
    posture: Posture
    posture_method: Literal["pose", "bbox"]
    torso_deg: float | None  # torso angle from vertical, pose only
    last_upright_ms: int | None  # last frame where posture was upright
    lying_since_ms: int | None  # start of the current continuous lying run
    still_since_ms: int | None  # since when the bbox center stays within features.still_motion_bh
    prev_anchor: Point | None  # anchor at the previous observation of this track
    prev_ts_ms: int | None
    kpts: list[Keypoint] | None  # pixels
    speed_source: SpeedSource = "relative"


class VehicleState(BaseModel):
    track_id: int
    name: str
    bbox: Box
    score: float
    footprint: tuple[Point, Point] | None  # meters: bottom edge on the floor
    height_px: float
    speed_vh_s: float | None  # own bbox heights per second
    speed_m_s: float | None
    speed_source: SpeedSource = "relative"


class ObjectState(BaseModel):  # untracked objects: phones and extra-model classes
    name: str
    bbox: Box
    score: float


class FrameContext(BaseModel):
    frame_idx: int
    ts_ms: int
    width: int
    height: int
    persons: list[PersonState]
    vehicles: list[VehicleState]
    objects: list[ObjectState]
    zones: list[Zone]
    calibrated: bool
    auto_calibration: AutoCalibration | None = None  # fit of this video (S19, 8.21)


class Observation(BaseModel):
    scenario: str
    subject: str
    state: ObsState
    level: Level
    hold_s: float  # how long P must last before the episode is confirmed at this level
    reason_code: str
    reason_text: str
    method: str
    confidence: float
    metrics: dict[str, float]
    zone_id: int | None
    anchor: Point | None  # pixels, used to merge a track id switch
    ref_height_px: float | None


class AnalysisConfig(BaseModel):  # snapshot stored in analyses.config_json
    width: int
    height: int
    fps: float
    step: int
    duration_ms: int  # videos.duration_ms: an episode active at the end closes here
    calibration: Calibration | None
    zones: list[Zone]
    rules: dict[str, CameraRule]  # by scenario
    class_conf: dict[str, float]
    active_classes: list[str]  # class names provided by the active models
    extra_artifact_ids: list[int] = []  # artifacts of pipeline.extra, read by a recompute


class EpisodeDraft(BaseModel):
    scenario: str
    subject: str
    zone_id: int | None
    level_initial: Level
    level_max: Level
    start_ms: int
    confirm_ms: int
    escalate_ms: int | None
    end_ms: int
    end_reason: EndReason
    reason_code: str
    reason_text: str
    method: str
    confidence: float
    metrics: dict[str, float]
    uncertain_ms: int
    confirm_frame_idx: int
    escalate_frame_idx: int | None


class AnalysisResult(BaseModel):
    hud: list[HudFrame]
    episodes: list[EpisodeDraft]
    gaps: list[ObservabilityGap]
    pose_used: bool
    auto_calibration: AutoCalibration | None = None


# --- evaluation (slice 14) ---------------------------------------------------------------
class ExpectedEvent(BaseModel):
    scenario: str
    start_s: float
    end_s: float


class EvalVideo(BaseModel):
    path: str
    camera_id: int | None = None  # take calibration, zones, rules of this camera; None: defaults
    expected: list[ExpectedEvent]


class EvalLabels(BaseModel):
    deadline_s: float | None = None  # None: eval.deadline_s
    videos: list[EvalVideo]


class EvalMetrics(BaseModel):
    scenario: str  # "*" for the total row
    expected: int
    episodes: int
    tp: int
    fn: int
    fp: int
    duplicates: int
    late: int
    precision: float | None
    recall: float | None
    f1: float | None
    fp_per_hour: float | None
    delay_s: Percentiles


class EvalReport(BaseModel):
    created_at: datetime
    labels: str
    hours: float
    deadline_s: float
    rows: list[EvalMetrics]
    out_dir: str


# --- protocols (tech.md 6.1) -------------------------------------------------------------
# LinQ Jupyter: inference/linq.JupyterShell, fakes/remote.FakeRemoteShell
class RemoteShell(Protocol):
    def upload(self, local: Path, remote: str) -> None: ...
    def download(self, remote: str, local: Path) -> int: ...
    def exec(self, cmd: str, timeout: float) -> tuple[int, str, str]: ...
    def size(self, remote: str) -> int | None: ...
    def close(self) -> None: ...  # v5, S28 (tech.md 8.29)


class InferenceBackend(Protocol):  # inference/linq.LinqBackend, inference/local.LocalBackend
    name: BackendName

    def run(
        self,
        video: Path,
        video_sha256: str,
        model: ModelSpec,
        step: int,
        out: Path,
        progress: Callable[[float], None],
    ) -> InferenceMetrics: ...
    def check(self) -> BackendStatus: ...
    def close(self) -> None: ...  # v5, S28 (tech.md 8.29)


class ScenarioPlugin(Protocol):  # rules/*.py
    meta: ScenarioMeta  # status and status_text are filled by rules.scenario_metas()

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]: ...
    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]: ...


class DeliveryChannel(Protocol):  # delivery.WebhookChannel
    name: str

    def deliver(self, event: EventSummary, kind: DeliveryKind) -> tuple[bool, int | None, str]: ...
