// Browser port of checkpoint server.mjs; no HTTP server or backend proxy.
import { AppError, publicCamera } from "./mock/state.mjs";
import {
  ACTOR_MAX, CONTRACT, HUMAN_ACTIONS, LEVEL_COLORS, LEVEL_TITLES, MSG, PRODUCT_TITLE, ROLES, ROLE_ACTIONS,
  ROLE_TITLES, SCENARIOS, SCENARIO_TITLES, STATUS_TITLES, TERMINAL, TIMEZONE, ZONE_KINDS,
} from "./mock/world.mjs";


export function createRoutes(mock) {
const apiError = (status, code, message, details = {}) => new AppError(status, code, message, details);
const validation = (field) => apiError(422, "validation", MSG.requestInvalid, { field });

function intParam(value, field) {
  if (!/^-?\d+$/.test(value)) throw validation(field);
  return Number(value);
}

// X-Role: unknown value → 400 role_required (tech.md 6.4); absent → null.
function roleOf(req) {
  const r = req.headers["x-role"];
  if (!r) return null;
  if (!ROLES.includes(r)) throw apiError(400, "role_required", MSG.roleRequired);
  return r;
}

// X-Actor: percent-encoded UTF-8, 1..60 characters after decoding (api._actor).
function actorOf(req) {
  const raw = req.headers["x-actor"];
  if (raw == null) return null;
  let name;
  try {
    name = decodeURIComponent(raw).trim();
  } catch {
    name = String(raw).trim();
  }
  if (name.length < 1 || [...name].length > ACTOR_MAX) throw apiError(422, "validation", MSG.actorInvalid, { field: "X-Actor" });
  return name;
}

function meta() {
  return {
    product_name: PRODUCT_TITLE, contract: CONTRACT, inference_backend: "linq", fake: true, timezone: TIMEZONE,
    roles: ROLES.map((id) => ({ id, title: ROLE_TITLES[id], actions: ROLE_ACTIONS[id] })),
    levels: ["yellow", "red"].map((id) => ({ id, title: LEVEL_TITLES[id], color: LEVEL_COLORS[id] })),
    statuses: Object.keys(STATUS_TITLES).map((id) => ({ id, title: STATUS_TITLES[id], terminal: TERMINAL.has(id) })),
    zone_kinds: ZONE_KINDS,
    scenarios: SCENARIOS,
  };
}

// Moscow is UTC+3 all year.
const MSK = 3 * 3600 * 1000;
function shiftAt(at) {
  const local = new Date(at + MSK);
  const h = local.getUTCHours();
  const day = Date.UTC(local.getUTCFullYear(), local.getUTCMonth(), local.getUTCDate()) - MSK;
  const H = 3600 * 1000;
  if (h >= 8 && h < 20) return { id: "day", title: "Дневная смена", start: day + 8 * H, end: day + 20 * H };
  const start = h >= 20 ? day + 20 * H : day - 4 * H;
  return { id: "night", title: "Ночная смена", start, end: start + 12 * H };
}

function countRows(events, keyOf, titleOf) {
  const rows = new Map();
  for (const e of events) {
    const key = String(keyOf(e));
    const row = rows.get(key) ?? { key, title: titleOf(e), count: 0, confirmed: 0, false_alarm: 0 };
    row.count += 1;
    if (e.operator_verdict === "confirmed") row.confirmed += 1;
    if (e.operator_verdict === "false_alarm") row.false_alarm += 1;
    rows.set(key, row);
  }
  return [...rows.values()].sort((a, b) => b.count - a.count);
}

function shift(query) {
  let at = Date.now();
  if (query.has("at")) {
    at = Date.parse(query.get("at"));
    if (Number.isNaN(at)) throw validation("at");
  }
  const s = shiftAt(at);
  const events = mock.events.filter((e) => e.status !== "superseded" && e.started_at >= s.start && e.started_at < s.end);
  const date = new Date(s.start + MSK).toISOString().slice(0, 10);
  return {
    shift_id: `${s.id}:${date}`, title: `${s.title} ${date.slice(8, 10)}.${date.slice(5, 7)}`,
    start: new Date(s.start).toISOString(), end: new Date(s.end).toISOString(), total: events.length,
    by_sector: countRows(events, (e) => e.sector_id, (e) => mock.sector(e.sector_id).name),
    by_scenario: countRows(events, (e) => e.scenario, (e) => SCENARIO_TITLES[e.scenario]),
    events: events.sort((a, b) => b.published_at - a.published_at).map((e) => mock.summary(e)),
  };
}

const LIST_MAX = 200;
function eventsList(q) {
  const one = (k, list) => {
    if (!q.has(k)) return null;
    const v = q.get(k);
    if (list && !list.includes(v)) throw validation(k);
    return v;
  };
  const int = (k) => (q.has(k) ? intParam(q.get(k), k) : null);
  const date = (k) => {
    if (!q.has(k)) return null;
    const t = Date.parse(q.get(k));
    if (Number.isNaN(t)) throw validation(k);
    return t;
  };
  const bool = (k, def) => {
    if (!q.has(k)) return def;
    const v = q.get(k);
    if (!["true", "false", "1", "0"].includes(v)) throw validation(k);
    return v === "true" || v === "1";
  };
  const f = {
    level: one("level", ["yellow", "red"]), scenario: one("scenario"), status: one("status", Object.keys(STATUS_TITLES)),
    sector_id: int("sector_id"), camera_id: int("camera_id"), zone_id: int("zone_id"),
    date_from: date("date_from"), date_to: date("date_to"), q: one("q")?.toLowerCase() ?? null,
    include_demo: bool("include_demo", true), include_superseded: bool("include_superseded", false),
    limit: q.has("limit") ? intParam(q.get("limit"), "limit") : 50,
    offset: q.has("cursor") ? intParam(q.get("cursor"), "cursor") : 0,
  };
  if (f.limit < 1 || f.limit > LIST_MAX) throw validation("limit");
  const items = mock.events
    .filter((e) =>
      (f.level == null || e.level === f.level) && (f.scenario == null || e.scenario === f.scenario) &&
      (f.status == null || e.status === f.status) && (f.sector_id == null || e.sector_id === f.sector_id) &&
      (f.camera_id == null || e.camera_id === f.camera_id) && (f.zone_id == null || e.zone_id === f.zone_id) &&
      (f.date_from == null || e.started_at >= f.date_from) && (f.date_to == null || e.started_at <= f.date_to) &&
      (f.include_demo || !e.is_demo) && (f.include_superseded || e.status !== "superseded"))
    .map((e) => mock.summary(e))
    .filter((s) => f.q == null || [s.reason_text, s.title, s.camera_name, s.sector_name, s.zone_name ?? ""].some((t) => t.toLowerCase().includes(f.q)))
    .sort((a, b) => b.published_at.localeCompare(a.published_at));
  const page = items.slice(f.offset, f.offset + f.limit);
  const nextOffset = f.offset + page.length;
  return { items: page, total: items.length, next_cursor: nextOffset < items.length ? String(nextOffset) : null };
}

function facets() {
  const item = (id, title) => ({ id: String(id), title });
  return {
    scenarios: Object.entries(SCENARIO_TITLES).map(([id, t]) => item(id, t)),
    levels: ["yellow", "red"].map((id) => item(id, LEVEL_TITLES[id])),
    statuses: Object.entries(STATUS_TITLES).map(([id, t]) => item(id, t)),
    sectors: mock.sectors.map((s) => item(s.id, s.name)),
    cameras: mock.cameras.map((c) => item(c.id, c.name)),
    zones: mock.zones.map((z) => item(z.id, `${z.name} · ${mock.camera(z.camera_id).name}`)),
  };
}


return { meta, shift, eventsList, facets, roleOf, actorOf, intParam, validation, publicCamera };
}
