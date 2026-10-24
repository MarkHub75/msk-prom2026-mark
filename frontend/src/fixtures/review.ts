import type { ActionIn, ApiError, CameraLiveView, CameraState, CameraTile, EventDetail, EventSummary, HumanAction, MasterInbox, OperatorDashboard, Role, Schemas, SectorState, SectorView, TracksWindow, WsMessage } from "../api/types";
import { createFixtureEvents, FIXTURE_NOW, fixtureAnalysis, fixtureBroadcast, fixtureCameras, fixtureHudForCamera, fixtureImage, fixtureMeta, fixtureSectors, fixtureVideo, fixtureZones, statusTitles } from "./data";

export const REVIEW_SCENARIOS = ["critical", "normal", "error", "empty", "offline", "notimplemented", "disconnected"] as const;
export type ReviewScenario = typeof REVIEW_SCENARIOS[number];
const MODE_KEY = "safewatch.review.mode.v1";
const STATE_PREFIX = "safewatch.review.fixture.v2.";
const memory = new Map<ReviewScenario, EventDetail[]>();
const subscribers = new Set<{listener: (message: WsMessage) => void; role: Role}>();
let resetConsumed = false;
let active: ReviewScenario | undefined;
const knownRoles: Role[] = ["operator", "master", "ohs", "management", "admin"];

function storageRead(key: string): string | null {
  try { return sessionStorage.getItem(key); } catch { return null; }
}
function storageWrite(key: string, value: string | null): void {
  try {
    if (value === null) sessionStorage.removeItem(key);
    else sessionStorage.setItem(key, value);
  } catch { /* Review remains functional in memory when storage is disabled. */ }
}
function isScenario(value: string | null | undefined): value is ReviewScenario {
  return REVIEW_SCENARIOS.includes(value as ReviewScenario);
}

/** Review mode is explicit and visible. It is never enabled because a real API failed. */
export function getReviewScenario(): ReviewScenario | "" {
  const query = new URLSearchParams(location.search);
  const requested = query.get("review");
  if (["real", "live", "off"].includes(requested ?? "")) {
    active = undefined;
    storageWrite(MODE_KEY, null);
    return "";
  }
  const configured = import.meta.env.VITE_REVIEW_MODE as string | undefined;
  const selected = isScenario(requested) ? requested : isScenario(configured) ? configured : active ?? storageRead(MODE_KEY);
  if (!isScenario(selected)) return "";
  active = selected;
  storageWrite(MODE_KEY, selected);
  if (!resetConsumed && query.get("reset") === "1") {
    memory.delete(selected);
    storageWrite(STATE_PREFIX + selected, null);
    resetConsumed = true;
  }
  return selected;
}
export function isReviewMode(): boolean { return getReviewScenario() !== ""; }

function eventsFor(scenario: ReviewScenario): EventDetail[] {
  const existing = memory.get(scenario);
  if (existing) return existing;
  const saved = storageRead(STATE_PREFIX + scenario);
  if (saved) {
    try {
      const parsed: unknown = JSON.parse(saved);
      if (Array.isArray(parsed) && parsed.every((item) => item && typeof item === "object" && "event" in item && "actions" in item)) {
        memory.set(scenario, parsed as EventDetail[]);
        return parsed as EventDetail[];
      }
    } catch { /* A corrupt local review draft resets only the synthetic fixture. */ }
  }
  const fresh = scenario === "empty" ? [] : createFixtureEvents(scenario === "normal");
  memory.set(scenario, fresh);
  return fresh;
}

function emit(message: WsMessage): void {
  queueMicrotask(() => {
    for (const subscription of subscribers) {
      if (message.type === "notification" && !message.data.audience.includes(subscription.role)) continue;
      subscription.listener(message);
    }
  });
}
export function subscribeFixtureMessages(listener: (message: WsMessage) => void, role: Role): () => void {
  const subscription = {listener, role};
  subscribers.add(subscription);
  queueMicrotask(() => {
    if (subscribers.has(subscription)) listener({type: "hello", at: FIXTURE_NOW, data: {server_now: FIXTURE_NOW, contract: "1.0.0", role}});
  });
  return () => { subscribers.delete(subscription); };
}
export function resetReview(): void {
  const scenario = getReviewScenario();
  if (!scenario) return;
  memory.delete(scenario);
  storageWrite(STATE_PREFIX + scenario, null);
  emit({type: "hello", at: FIXTURE_NOW, data: {server_now: FIXTURE_NOW, contract: "1.0.0", role: "operator"}});
}

const terminalStatuses: EventSummary["status"][] = ["false_alarm", "resolved", "auto_finished", "superseded"];
function isTerminal(event: EventSummary): boolean { return terminalStatuses.includes(event.status); }

/** This is the synthetic server's copy of tech.md 8.6, never client-side business prediction. */
export function fixtureAllowedActions(event: EventSummary, role: Role): HumanAction[] {
  if (role === "master") return event.status === "sent_to_master" ? ["accept"] : event.status === "master_accepted" ? ["resolve"] : [];
  if (role !== "operator") return [];
  const initial = ["new", "viewed", "confirmed"].includes(event.status);
  const timeout = event.status === "sent_to_master" && event.escalated_by_timeout && event.operator_verdict === "none";
  const allowed: HumanAction[] = [];
  if (event.status === "new") allowed.push("view");
  if (["new", "viewed"].includes(event.status) || (event.level === "red" && (event.status === "confirmed" || timeout))) allowed.push("confirm");
  if (initial || timeout) allowed.push("false_alarm");
  if (initial) allowed.push("send_to_master");
  return allowed;
}
function detailFor(detail: EventDetail, role: Role): EventDetail {
  return structuredClone({...detail, allowed_actions: fixtureAllowedActions(detail.event, role)});
}

function cameraState(cameraId: number, events: EventDetail[]): CameraState {
  const camera = fixtureCameras.find((item) => item.id === cameraId)!;
  const open = events.map((item) => item.event).filter((item) => item.camera_id === cameraId && !isTerminal(item));
  const red = open.filter((item) => item.level === "red").length;
  const yellow = open.filter((item) => item.level === "yellow" && !item.ended_at).length;
  const missing = cameraId === 10;
  return {camera_id: cameraId, sector_id: camera.sector_id, state: red ? "red" : yellow ? "yellow" : missing ? "no_observation" : "normal",
    reason: missing ? "obstructed" : null, reason_text: missing ? "Камера закрыта или не в фокусе" : red ? "Есть критическое событие" : yellow ? "Требует внимания" : "Наблюдение доступно",
    freshness_ms: missing ? null : 80, open_red: red, open_yellow: yellow};
}
function sectorState(sectorId: number, events: EventDetail[]): SectorState {
  const sector = fixtureSectors.find((item) => item.id === sectorId)!;
  const cameras = fixtureCameras.filter((item) => item.sector_id === sectorId).map((item) => cameraState(item.id, events));
  const red = cameras.reduce((count, item) => count + item.open_red, 0);
  const yellow = cameras.reduce((count, item) => count + item.open_yellow, 0);
  const missing = cameras.filter((item) => item.state === "no_observation").length;
  return {sector_id: sectorId, name: sector.name, state: red ? "red" : yellow ? "yellow" : missing ? "no_observation" : "normal",
    reason_text: red ? "Требуется реакция оператора" : yellow ? "Есть события для проверки" : missing ? `Нет наблюдения: ${missing} из ${cameras.length} камер` : "Наблюдение доступно",
    cameras_total: cameras.length, cameras_no_observation: missing, open_yellow: yellow, open_red: red};
}
function cameraTile(cameraId: number, events: EventDetail[]): CameraTile {
  const camera = fixtureCameras.find((item) => item.id === cameraId)!;
  const state = cameraState(cameraId, events);
  return {camera, state, broadcast: state.state === "no_observation" ? null : fixtureBroadcast(cameraId), preview_url: state.state === "no_observation" ? null : fixtureImage(cameraId)};
}
function feedFor(events: EventDetail[]): EventSummary[] {
  return events.map((item) => structuredClone(item.event)).filter((item) => item.status !== "superseded").sort((a, b) => b.priority - a.priority || b.published_at.localeCompare(a.published_at));
}
function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {status, headers: {"Content-Type": "application/json", "X-SafeWatch-Review": "synthetic-fixture"}});
}
function error(code: string, message: string, status: number, details: ApiError["details"] = {}): Response {
  return json({code, message, details} satisfies ApiError, status);
}

function applyAction(detail: EventDetail, input: ActionIn, role: Role, actor: string): Response {
  const permittedRole = input.action === "accept" || input.action === "resolve" ? "master" : "operator";
  if (role !== permittedRole) return error("forbidden_role", "Действие недоступно для выбранной роли", 403);
  if (!fixtureAllowedActions(detail.event, role).includes(input.action)) return error("invalid_transition", "Состояние события изменилось. Обновите карточку", 409);
  const comment = input.comment ?? "";
  if (typeof comment !== "string" || comment.length > 500) return error("validation", "Комментарий должен содержать не больше 500 символов", 422, {field: "comment"});
  if (input.action === "resolve" && !comment.trim()) return error("validation", "Опишите принятые меры", 422, {field: "comment"});
  const event = detail.event;
  const previous = event.status;
  let logAction: EventDetail["actions"][number]["action"];
  if (input.action === "view") { event.status = "viewed"; logAction = "viewed"; }
  else if (input.action === "confirm") { event.operator_verdict = "confirmed"; event.status = event.level === "red" ? "sent_to_master" : "confirmed"; logAction = "confirmed"; }
  else if (input.action === "false_alarm") { event.operator_verdict = "false_alarm"; event.status = "false_alarm"; logAction = "false_alarm"; }
  else if (input.action === "send_to_master") { event.status = "sent_to_master"; if (event.operator_verdict === "none") event.operator_verdict = "confirmed"; logAction = "sent_to_master"; }
  else if (input.action === "accept") { event.status = "master_accepted"; logAction = "master_accepted"; }
  else { event.status = "resolved"; logAction = "resolved"; }
  event.status_title = statusTitles[event.status];
  event.priority = isTerminal(event) ? 0 : event.status === "viewed" ? event.level === "red" ? 3 : 2 : 1;
  // Frozen source timestamp plus monotonic fixture action seconds keeps review deterministic.
  const at = new Date(Date.parse(FIXTURE_NOW) + detail.actions.length * 1000).toISOString();
  const nextId = Math.max(0, ...detail.actions.map((item) => item.id)) + 1;
  const redConfirmation = input.action === "confirm" && event.level === "red" && previous !== "sent_to_master";
  detail.actions.push({id: nextId, at, actor_role: role, actor_name: actor, action: logAction, from_status: previous, to_status: redConfirmation ? "confirmed" : event.status, comment: comment.trim()});
  if (input.action === "confirm" && event.level === "red" && previous !== "sent_to_master") {
    detail.actions.push({id: nextId + 1, at, actor_role: role, actor_name: actor, action: "sent_to_master", from_status: "confirmed", to_status: "sent_to_master", comment: ""});
  }
  const scenario = getReviewScenario();
  if (scenario) storageWrite(STATE_PREFIX + scenario, JSON.stringify(eventsFor(scenario)));
  emit({type: "event.updated", at, data: structuredClone(event)});
  if (event.status === "sent_to_master" && previous !== "sent_to_master") emit({type: "notification", at,
    data: {id: `review-${event.id}-${nextId}`, event_id: event.id, level: event.level, text: event.notification_text, audience: ["master"], sound: "chime", takeover: false}});
  return json(detailFor(detail, role));
}

/** The same openapi-fetch client invokes this transport only after explicit review opt-in. */
export async function reviewFetch(request: Request): Promise<Response> {
  const scenario = getReviewScenario();
  if (!scenario) throw new Error("Review transport called without explicit review mode");
  const url = new URL(request.url);
  const path = url.pathname;
  const method = request.method;
  if (request.signal.aborted) throw new DOMException("Request aborted", "AbortError");
  if (method !== "GET" && !(method === "POST" && /^\/api\/events\/\d+\/actions$/.test(path))) return error("not_implemented", "Изменение не входит в текущий review fixture", 501);
  const roleHeader = request.headers.get("X-Role");
  const role: Role = knownRoles.includes(roleHeader as Role) ? roleHeader as Role : "operator";
  if (roleHeader && !knownRoles.includes(roleHeader as Role)) return error("role_required", "Выберите роль", 400);
  if (path === "/api/meta") return json(fixtureMeta);
  if (path === "/api/health") return json({status: "ok", contract: "1.0.0"});
  if (scenario === "offline") throw new TypeError("Review fixture: network unavailable");
  if (scenario === "error") return error("unavailable", "Не удалось загрузить данные. Повторите запрос", 503);
  if (scenario === "notimplemented") return error("not_implemented", "Функция появится в слайсе 6", 501, {slice: "6"});
  const events = eventsFor(scenario);
  if (path === "/api/operator/dashboard") return json({sectors: scenario === "empty" ? [] : fixtureSectors.map((sector) => sectorState(sector.id, events)), feed: feedFor(events), server_now: FIXTURE_NOW} satisfies OperatorDashboard);
  if (path === "/api/operator/feed") return json(feedFor(events));
  if (path === "/api/events") {
    const q = url.searchParams.get("q")?.toLocaleLowerCase("ru-RU");
    const items = events.map(item => item.event).filter(event => {
      for (const key of ["level", "scenario", "status", "sector_id", "camera_id", "zone_id"] as const) {
        const wanted = url.searchParams.get(key);
        if (wanted !== null && String(event[key]) !== wanted) return false;
      }
      if (url.searchParams.get("include_demo") === "false" && event.is_demo) return false;
      if (url.searchParams.get("include_superseded") !== "true" && event.status === "superseded") return false;
      if (q && ![event.title, event.reason_text, event.camera_name, event.sector_name, String(event.id)].some(value => value.toLocaleLowerCase("ru-RU").includes(q))) return false;
      const from = url.searchParams.get("date_from"), to = url.searchParams.get("date_to");
      return (!from || event.started_at >= from) && (!to || event.started_at <= to);
    }).sort((a,b) => b.published_at.localeCompare(a.published_at));
    const offset = Number(url.searchParams.get("cursor") ?? 0), limit = Number(url.searchParams.get("limit") ?? 50);
    if (!Number.isInteger(offset) || offset < 0 || !Number.isInteger(limit) || limit < 1 || limit > 200) return error("validation", "Проверьте страницу журнала", 422);
    return json({items:items.slice(offset,offset+limit),total:items.length,next_cursor:offset+limit<items.length?String(offset+limit):null} satisfies Schemas["EventPage"]);
  }
  if (path === "/api/journal/facets") return json({
    scenarios:fixtureMeta.scenarios.map(item=>({id:item.id,title:item.title})),
    levels:fixtureMeta.levels.map(item=>({id:item.id,title:item.title})),
    statuses:fixtureMeta.statuses.map(item=>({id:item.id,title:item.title})),
    sectors:fixtureSectors.map(item=>({id:String(item.id),title:item.name})),
    cameras:fixtureCameras.map(item=>({id:String(item.id),title:item.name})), zones:[],
  } satisfies Schemas["JournalFacets"]);
  if (path === "/api/sectors") return json(scenario === "empty" ? [] : fixtureSectors);
  if (path === "/api/cameras") return json(scenario === "empty" ? [] : fixtureCameras.filter((camera) => !url.searchParams.has("sector_id") || camera.sector_id === Number(url.searchParams.get("sector_id"))));
  if (path === "/api/master/inbox") return json({active: feedFor(events).filter((event) => event.status === "sent_to_master" || event.status === "master_accepted"), recent_resolved: feedFor(events).filter((event) => event.status === "resolved"), server_now: FIXTURE_NOW} satisfies MasterInbox);
  let match = path.match(/^\/api\/sectors\/(\d+)\/view$/);
  if (match) {
    const id = Number(match[1]);
    if (!fixtureSectors.some((sector) => sector.id === id)) return error("not_found", "Сектор не найден", 404);
    return json({sector: sectorState(id, events), cameras: fixtureCameras.filter((camera) => camera.sector_id === id).map((camera) => cameraTile(camera.id, events)), feed: feedFor(events).filter((event) => event.sector_id === id)} satisfies SectorView);
  }
  match = path.match(/^\/api\/cameras\/(\d+)(?:\/(view|broadcast|preview|zones|calibration))?$/);
  if (match) {
    const id = Number(match[1]);
    const camera = fixtureCameras.find((item) => item.id === id);
    if (!camera) return error("not_found", "Камера не найдена", 404);
    if (!match[2]) return json(camera);
    if (match[2] === "preview") return new Response(null, {status: 307, headers: {Location: fixtureImage(id)}});
    if (match[2] === "zones") return json(fixtureZones(id));
    if (match[2] === "calibration") return json(null);
    const state = cameraState(id, events);
    const broadcast = state.state === "no_observation" ? null : fixtureBroadcast(id);
    if (match[2] === "broadcast") return json(broadcast);
    return json({camera, state, broadcast, video: broadcast ? fixtureVideo(id) : null, analysis: broadcast ? fixtureAnalysis(id, events) : null, zones: fixtureZones(id), calibration: null} satisfies CameraLiveView);
  }
  match = path.match(/^\/api\/events\/(\d+)(\/actions)?$/);
  if (match) {
    const detail = events.find((item) => item.event.id === Number(match![1]));
    if (!detail) return error("not_found", "Событие не найдено", 404);
    if (!match[2] && method === "GET") return json(detailFor(detail, role));
    if (match[2] && method === "POST") {
      if (!roleHeader) return error("role_required", "Выберите роль", 400);
      let actor = "";
      try { actor = decodeURIComponent(request.headers.get("X-Actor") ?? "").trim(); } catch { return error("validation", "Проверьте имя участника", 422); }
      if (!actor || actor.length > 60) return error("validation", "Имя должно содержать от 1 до 60 символов", 422);
      let input: unknown;
      try { input = await request.json(); } catch { return error("validation", "Проверьте данные действия", 422); }
      if (!input || typeof input !== "object" || !("action" in input) || !["view", "confirm", "false_alarm", "send_to_master", "accept", "resolve"].includes(String(input.action))) return error("validation", "Неизвестное действие", 422);
      return applyAction(detail, input as ActionIn, role, actor);
    }
  }
  match = path.match(/^\/api\/videos\/(\d+)(?:\/(tracks|analysis|file))?$/);
  if (match) {
    const id = Number(match[1]);
    if (!fixtureCameras.some((camera) => camera.id === id)) return error("not_found", "Запись не найдена", 404);
    if (!match[2]) return json(fixtureVideo(id));
    if (match[2] === "analysis") return json(fixtureAnalysis(id, events));
    if (match[2] === "file") return new Response(null, {status: 307, headers: {Location: id % 3 === 0 ? "/fixtures/factory-welding-replay.mp4" : "/fixtures/factory-replay.mp4"}});
    const from = Number(url.searchParams.get("from_ms") ?? 0), to = Number(url.searchParams.get("to_ms") ?? 30000);
    if (!Number.isFinite(from) || !Number.isFinite(to) || from < 0 || to < from) return error("validation", "Проверьте диапазон кадров", 422);
    const frames = [];
    for (let frame = Math.ceil(from / 40); frame * 40 <= Math.min(to, 29960); frame++) frames.push({frame_idx: frame, ts_ms: frame * 40, objects: fixtureHudForCamera(id)});
    return json({video_id: id, analysis_id: id, from_ms: from, to_ms: to, frames} satisfies TracksWindow);
  }
  match = path.match(/^\/api\/evidence\/(\d+)\/image$/);
  if (match) {
    const detail = events.find((item) => item.episode?.evidence.some((evidence) => evidence.id === Number(match![1])));
    return detail ? new Response(null, {status: 307, headers: {Location: fixtureImage(detail.event.camera_id)}}) : error("not_found", "Доказательный кадр не найден", 404);
  }
  return error("not_implemented", "Этот маршрут не входит в текущий review fixture", 501);
}

/** Media elements cannot use a custom fetch; keep their URLs same-origin in review. */
export function reviewMediaUrl(url: string): string {
  const parsed = new URL(url, location.origin);
  const video = parsed.pathname.match(/^\/api\/videos\/(\d+)\/file$/);
  if (video) return Number(video[1]) % 3 === 0 ? "/fixtures/factory-welding-replay.mp4" : "/fixtures/factory-replay.mp4";
  const camera = parsed.pathname.match(/^\/api\/cameras\/(\d+)\/preview$/);
  if (camera) return fixtureImage(Number(camera[1]));
  const evidence = parsed.pathname.match(/^\/api\/evidence\/(\d+)\/image$/);
  if (evidence) {
    const scenario = getReviewScenario();
    const detail = scenario && eventsFor(scenario).find((item) => item.episode?.evidence.some((frame) => frame.id === Number(evidence[1])));
    return detail ? fixtureImage(detail.event.camera_id) : url;
  }
  return url;
}
