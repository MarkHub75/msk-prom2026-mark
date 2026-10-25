// Deterministic UI review fixtures. These are synthetic contract-shaped data,
// never fallback responses and never reported as real LinQ inference.
import type { Analysis, Broadcast, Camera, Episode, EventAction, EventDetail, EventSummary, HudObject, Meta, Sector, Video, Zone } from "../api/types";

export const FIXTURE_NOW = "2026-10-24T07:42:18.000Z";
export const FIXTURE_SHA = "4d1ba7e6b436b84ce5d1a9f9e51e22a2e5e6af87cedcbe90f22683225f84721f";
const WELDING_IMAGE_SHA = "069cf7588a5733eaf59131c05317ad0a39b6fee5fa458385daca6b503c8c9e95";
const CUTTING_VIDEO_SHA = "ef1e12b21d705f24e347d39b22540507ddb2f380c78658e0451e3c95f382008f";
const WELDING_VIDEO_SHA = "4193508a5198d52533692a5f6eb7558bdf60d120d59e60fae16a6bdb40ec0620";
function imageSha(cameraId: number): string { return cameraId % 3 === 0 ? WELDING_IMAGE_SHA : FIXTURE_SHA; }
function videoSha(cameraId: number): string { return cameraId % 3 === 0 ? WELDING_VIDEO_SHA : CUTTING_VIDEO_SHA; }
export const statusTitles: Record<EventSummary["status"], string> = {
  new: "Новое", viewed: "Просмотрено", confirmed: "Подтверждено",
  false_alarm: "Ложное срабатывание", sent_to_master: "Передано мастеру",
  master_accepted: "Принято мастером", resolved: "Решено",
  auto_finished: "Завершилось автоматически", superseded: "Пересчитано",
};
const terminal = new Set<EventSummary["status"]>(["false_alarm", "resolved", "auto_finished", "superseded"]);
export const fixtureMeta: Meta = {
  product_name: "SafeWatch", contract: "1.0.0", inference_backend: "local", fake: true, timezone: "Europe/Moscow",
  roles: [
    {id: "operator", title: "Оператор", actions: ["view", "confirm", "false_alarm", "send_to_master"]},
    {id: "master", title: "Мастер", actions: ["accept", "resolve"]},
    {id: "ohs", title: "Охрана труда", actions: []},
    {id: "management", title: "Руководство", actions: []},
    {id: "admin", title: "Администратор", actions: []},
  ],
  levels: [{id: "yellow", title: "Жёлтая опасность", color: "#f4c15b"}, {id: "red", title: "Красная опасность", color: "#f14b43"}],
  statuses: (Object.entries(statusTitles) as [EventSummary["status"], string][]).map(([id, title]) => ({id, title, terminal: terminal.has(id)})),
  zone_kinds: [{id: "danger", title: "Опасная зона", color: "#f14b43", geometry: "polygon", description: "Иллюстративная зона в review fixture"}],
  scenarios: [
    {id: "running", title: "Бег и резкие перемещения", description: "Демонстрационный сценарий", icon: "person", default_level: "yellow", status: "active", status_text: "Синтетический пример", required_classes: ["person"], zone_kinds: [], params: []},
    {id: "danger_zone", title: "Вход в опасную зону", description: "Демонстрационный сценарий", icon: "zone", default_level: "red", status: "active", status_text: "Синтетический пример", required_classes: ["person"], zone_kinds: ["danger"], params: []},
    {id: "lying", title: "Падение и неподвижность", description: "Демонстрационный сценарий", icon: "person", default_level: "red", status: "active", status_text: "Синтетический пример", required_classes: ["person"], zone_kinds: [], params: []},
  ],
};

export const fixtureSectors: Sector[] = [
  "Прессовый участок", "Склад и погрузка", "Сборочный цех", "Сварочный участок", "Ремонтная зона", "Отгрузка",
].map((name, index) => ({id: index + 1, name: `Сектор ${index + 1} · ${name}`, sort_order: index + 1, is_demo: true}));

export const fixtureCameras: Camera[] = fixtureSectors.flatMap((sector) => [0, 1].map((offset) => ({
  id: (sector.id - 1) * 2 + offset + 1, sector_id: sector.id,
  name: `Камера ${sector.id}.${offset + 1} · ${offset === 0 ? "Основной обзор" : "Проход"}`,
  description: "Локальный иллюстративный материал для review. Не прямой эфир.",
  is_demo: true, has_calibration: false, zones_count: 1, videos_count: 1,
})));

export function fixtureImage(cameraId: number): string {
  return cameraId % 3 === 0 ? "/fixtures/factory-welding.png" : "/fixtures/factory-cutting.png";
}

// Manually positioned synthetic review boxes on the exact supplied stills.
// Review clips repeat those same stills: every frame keeps the matching geometry.
// These are illustrative annotations, never model-backed detections.
export const fixtureHudObjects: HudObject[] = [{track_id: 1, kind: "person", label: "Человек · иллюстрация", score: 0,
  bbox: [0.633373, 0.377258, 0.686603, 0.609989], kpts: null,
  tags: [{code: "review_fixture", text: "Синтетическая разметка", level: null}]}];
export function fixtureHudForCamera(cameraId: number): HudObject[] {
  return structuredClone(cameraId % 3 === 0 ? [{...fixtureHudObjects[0], bbox: [0.633971, 0.369819, 0.714115, 0.765143] as [number, number, number, number]}] : fixtureHudObjects);
}

export function fixtureVideo(cameraId: number): Video {
  return {id: cameraId, camera_id: cameraId, filename: cameraId % 3 === 0 ? "factory-welding-replay.mp4" : "factory-replay.mp4", sha256: videoSha(cameraId),
    size_bytes: cameraId % 3 === 0 ? 2145524 : 2213485, width: 1672, height: 940, fps: 25, frame_count: 750, duration_ms: 30000,
    codec: "h264", browser_playable: true, web_playable: true, status: "ready", active_analysis_id: cameraId,
    created_at: "2026-10-24T07:00:00.000Z"};
}

export function fixtureBroadcast(cameraId: number): Broadcast {
  return {id: cameraId, camera_id: cameraId, video_id: cameraId, analysis_id: cameraId,
    status: "playing", loop: true, cycle: 0, started_at: "2026-10-24T07:42:00.000Z",
    position_ms: 18000, duration_ms: 30000, server_now: FIXTURE_NOW};
}

export function fixtureZones(cameraId: number): Zone[] {
  // Deliberately no spatial overlay on uncalibrated illustrative footage.
  void cameraId;
  return [];
}

function summary(id: number, cameraId: number, overrides: Partial<EventSummary>): EventSummary {
  const camera = fixtureCameras.find((item) => item.id === cameraId)!;
  const sector = fixtureSectors.find((item) => item.id === camera.sector_id)!;
  return {id, scenario: "danger_zone", title: "Вход в опасную зону", level: "red", status: "new", status_title: "Новое",
    operator_verdict: "none", escalated_by_timeout: false, mode: "demo", camera_id: camera.id, camera_name: camera.name,
    sector_id: sector.id, sector_name: sector.name, zone_id: null, zone_name: null,
    reason_text: "Человек в зоне работы оборудования", notification_text: `Красная опасность · Сектор ${sector.id} · Проверьте доказательный кадр`,
    started_at: "2026-10-24T07:41:52.000Z", published_at: "2026-10-24T07:42:00.000Z", red_at: "2026-10-24T07:42:00.000Z",
    ended_at: null, duration_s: 26, priority: 3, is_demo: true, crew: "", ...overrides} as EventSummary;
}

export function createFixtureEvents(normal = false): EventDetail[] {
  const events = [
    summary(41, 1, {}),
    summary(42, 3, {scenario: "running", title: "Бег и резкие перемещения", level: "yellow", status: "viewed", status_title: "Просмотрено", red_at: null, priority: 2,
      reason_text: "Резкое перемещение в проходе", notification_text: "Жёлтая опасность · Сектор 2 · Резкое перемещение", started_at: "2026-10-24T07:39:10.000Z", published_at: "2026-10-24T07:39:18.000Z", duration_s: 188}),
    summary(43, 5, {scenario: "lying", title: "Падение и неподвижность", status: "sent_to_master", status_title: "Передано мастеру", operator_verdict: "confirmed", priority: 1,
      reason_text: "Требуется проверка на месте", started_at: "2026-10-24T07:36:28.000Z", published_at: "2026-10-24T07:36:36.000Z", red_at: "2026-10-24T07:36:36.000Z", duration_s: 350}),
    summary(44, 7, {level: "yellow", status: "resolved", status_title: "Решено", operator_verdict: "confirmed", priority: 0, ended_at: "2026-10-24T07:22:00.000Z",
      reason_text: "Проход освобождён, мастер подтвердил меры", started_at: "2026-10-24T07:20:00.000Z", published_at: "2026-10-24T07:20:08.000Z", red_at: null, duration_s: 120}),
  ];
  return events.map((event) => {
    if (normal && event.id !== 44) {
      event.level = "yellow"; event.status = "auto_finished"; event.status_title = statusTitles.auto_finished;
      event.priority = 0; event.ended_at = FIXTURE_NOW; event.red_at = null;
    }
    // The available illustrative still shows a standing person. It cannot serve
    // as evidence of a fall, nor as subsequent footage for that same scenario.
    const missingScenarioMedia = event.scenario === "lying";
    const episode: Episode = {id: event.id, analysis_id: event.camera_id, scenario: event.scenario, scenario_title: event.title,
      subject: "Иллюстративный эпизод", zone_id: null, level_initial: event.level, level_max: event.level,
      start_ms: 0, confirm_ms: 0, escalate_ms: null, end_ms: 30000, end_reason: "video_end", reason_code: "review_fixture",
      reason_text: event.reason_text, method: "Синтетический UI fixture, не результат модели", confidence: 0,
      metrics: {}, uncertain_ms: 0,
      evidence: missingScenarioMedia ? [] : [{id: event.id, kind: "confirm", frame_idx: 0, ts_ms: 0, url: fixtureImage(event.camera_id), sha256: imageSha(event.camera_id), objects: fixtureHudForCamera(event.camera_id)}]};
    const actions: EventAction[] = [{id: event.id * 10, at: event.published_at, actor_role: "system", actor_name: "Review fixture", action: "published", from_status: null, to_status: "new", comment: "Синтетический пример для проверки интерфейса"}];
    if (event.status === "sent_to_master" || event.status === "resolved") {
      actions.push({id: event.id * 10 + 1, at: event.id === 44 ? "2026-10-24T07:21:00.000Z" : "2026-10-24T07:37:00.000Z", actor_role: "operator", actor_name: "Оператор · демо", action: "sent_to_master", from_status: "new", to_status: "sent_to_master", comment: "Проверьте участок"});
    }
    if (event.status === "resolved") {
      actions.push({id: event.id * 10 + 2, at: "2026-10-24T07:21:20.000Z", actor_role: "master", actor_name: "Мастер · демо", action: "master_accepted", from_status: "sent_to_master", to_status: "master_accepted", comment: ""},
        {id: event.id * 10 + 3, at: "2026-10-24T07:22:00.000Z", actor_role: "master", actor_name: "Мастер · демо", action: "resolved", from_status: "master_accepted", to_status: "resolved", comment: "Проверил участок. Проход освобождён, работа продолжена."});
    }
    if (event.status === "viewed") actions.push({id: event.id * 10 + 1, at: "2026-10-24T07:39:20.000Z", actor_role: "operator", actor_name: "Оператор · демо", action: "viewed", from_status: "new", to_status: "viewed", comment: ""});
    if (event.status === "auto_finished") actions.push({id: event.id * 10 + 1, at: FIXTURE_NOW, actor_role: "system", actor_name: "Review fixture", action: "auto_finished", from_status: "new", to_status: "auto_finished", comment: "Иллюстративное завершение эпизода"});
    return {event, episode, why: [{label: "Наблюдение", value: event.reason_text}, {label: "Источник", value: "Локальные синтетические fixtures. Не результат LinQ."}, ...(missingScenarioMedia ? [{label: "Доказательный материал", value: "Подходящий кадр падения не подготовлен. Иллюстрация стоящего человека не используется как доказательство."}] : [{label: "Материал", value: "Иллюстрация интерфейса: не подтверждает движение или классификацию сценария."}])],
      actions, allowed_actions: [], can_identify: false, provenance: {backend: "local", fake: true, det_model: null, pose_model: null, job_id: null, video_sha256: videoSha(event.camera_id),
        analysis_version: 1, rule_params: {}, evidence_sha256: missingScenarioMedia ? null : imageSha(event.camera_id)}, deliveries: [],
      video_id: missingScenarioMedia ? null : event.camera_id, video_start_ms: missingScenarioMedia ? null : 0, video_end_ms: missingScenarioMedia ? null : 30000, broadcast: missingScenarioMedia ? null : fixtureBroadcast(event.camera_id)};
  });
}

export function fixtureAnalysis(cameraId: number, events: EventDetail[]): Analysis {
  return {id: cameraId, video_id: cameraId, version: 1, created_at: "2026-10-24T07:00:00.000Z", duration_ms: 30000,
    pose_used: false, episodes: events.filter((item) => item.event.camera_id === cameraId).flatMap((item) => item.episode ? [item.episode] : []), gaps: []};
}
