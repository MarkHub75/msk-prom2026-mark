// Stateful mock of the SafeWatch critical path: REST on 4010, WS on 4011/ws (the ports of
// `npm run mock`, so frontend/.env.mock works as is). Do not run both at once.
// Director endpoints live under /__demo/ on the REST port; bin/demo.mjs calls them.
import { existsSync, readFileSync } from "node:fs";
import { createServer } from "node:http";
import { WebSocketServer } from "ws";
import { AppError, Mock, publicCamera } from "./state.mjs";
import {
  ACTOR_MAX, CONTRACT, HUMAN_ACTIONS, LEVEL_COLORS, LEVEL_TITLES, MSG, PRODUCT_TITLE, ROLES, ROLE_ACTIONS,
  ROLE_TITLES, SCENARIOS, SCENARIO_TITLES, STATUS_TITLES, TERMINAL, TIMEZONE, ZONE_KINDS,
} from "./world.mjs";

const args = process.argv.slice(2);
const flag = (name) => args.includes(name);
const opt = (name, def) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : def;
};
const HOST = "127.0.0.1";
const REST_PORT = Number(opt("--rest-port", process.env.SW_MOCK_REST_PORT ?? 4010));
const WS_PORT = Number(opt("--ws-port", process.env.SW_MOCK_WS_PORT ?? 4011));
const ESCALATION = flag("--escalation") || process.env.SW_MOCK_ESCALATION === "1";
const WITH_EPISODE = !flag("--no-episode");
const QUIET = flag("--quiet");

// --- WebSocket ---------------------------------------------------------------------------
const wss = new WebSocketServer({ host: HOST, port: WS_PORT, path: "/ws" });
const clients = new Set(); // {socket, role}

function send(socket, type, data) {
  socket.send(JSON.stringify({ type, at: new Date().toISOString(), data }));
}

function emit(type, data, audience = null) {
  for (const c of clients) {
    if (audience && !audience.includes(c.role)) continue;
    send(c.socket, type, data);
  }
  if (!QUIET) log(`ws  ${type}${audience ? ` → ${audience.join(",")}` : ""}${data.id != null ? ` #${data.id}` : ""}`);
}

wss.on("connection", (socket, request) => {
  const role = new URL(request.url ?? "/ws", "http://x").searchParams.get("role");
  if (!ROLES.includes(role)) {
    socket.close(4400, "unknown role");
    return;
  }
  const client = { socket, role };
  clients.add(client);
  const now = new Date().toISOString();
  send(socket, "hello", { server_now: now, contract: CONTRACT, role });
  socket.on("close", () => clients.delete(client));
  socket.on("error", () => clients.delete(client));
});

function dropWs() {
  const n = clients.size;
  for (const c of clients) c.socket.terminate();
  clients.clear();
  return n;
}

// --- state -------------------------------------------------------------------------------
const mock = new Mock({ emit, escalation: ESCALATION, withEpisode: WITH_EPISODE });
if (ESCALATION) setInterval(() => mock.escalationTick(), 500).unref();

// Routes of contract/openapi.json not served by the mock answer 501 not_implemented.
const OPENAPI = new URL("../../../contract/openapi.json", import.meta.url);
const contractRoutes = existsSync(OPENAPI)
  ? Object.entries(JSON.parse(readFileSync(OPENAPI, "utf8")).paths).map(([p, ops]) => ({
      re: new RegExp(`^${p.replace(/\{[^}]+\}/g, "[^/]+")}$`),
      methods: Object.keys(ops).map((m) => m.toUpperCase()),
    }))
  : [];

// --- helpers -----------------------------------------------------------------------------
function log(line) {
  const t = new Date().toLocaleTimeString("ru-RU", { timeZone: TIMEZONE });
  console.log(`${t} ${line}`);
}

function corsHeaders(origin) {
  const ok = origin && /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin);
  return ok
    ? {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-Role, X-Actor",
        "Access-Control-Max-Age": "600",
        Vary: "Origin",
      }
    : {};
}

function json(res, status, body) {
  res.writeHead(status, { ...res.cors, "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(body));
}

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

async function body(req) {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const text = Buffer.concat(chunks).toString("utf8");
  try {
    return text ? JSON.parse(text) : undefined;
  } catch {
    throw validation("body");
  }
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

// --- routing -----------------------------------------------------------------------------
async function api(req, res, url) {
  const p = url.pathname;
  const m = req.method;
  const q = url.searchParams;
  let match;
  if (mock.faults.error500) throw apiError(500, "internal", MSG.internal);
  if (m === "GET" && p === "/api/health") return json(res, 200, { status: "ok", contract: CONTRACT });
  if (m === "GET" && p === "/api/meta") return json(res, 200, meta());
  if (m === "GET" && p === "/api/operator/dashboard") return json(res, 200, mock.dashboard());
  if (m === "GET" && p === "/api/operator/feed") return json(res, 200, mock.feed());
  if (m === "GET" && (match = p.match(/^\/api\/sectors\/([^/]+)\/view$/))) return json(res, 200, mock.sectorView(intParam(match[1], "sector_id")));
  if (m === "GET" && p === "/api/sectors") return json(res, 200, mock.sectors);
  if (m === "GET" && p === "/api/cameras") {
    const sid = q.has("sector_id") ? intParam(q.get("sector_id"), "sector_id") : null;
    if (sid != null && !mock.sector(sid)) throw apiError(404, "not_found", "Сектор не найден", { sector_id: sid });
    return json(res, 200, mock.cameras.filter((c) => sid == null || c.sector_id === sid).map(publicCamera));
  }
  if (m === "GET" && p === "/api/events") return json(res, 200, eventsList(q));
  if (m === "GET" && p === "/api/journal/facets") return json(res, 200, facets());
  if (m === "GET" && p === "/api/master/inbox") return json(res, 200, mock.masterInbox());
  if (m === "GET" && p === "/api/master/shift") return json(res, 200, shift(q));
  if (m === "GET" && (match = p.match(/^\/api\/events\/([^/]+)$/)) && match[1] !== "export.csv") {
    const role = roleOf(req);
    return json(res, 200, mock.detail(intParam(match[1], "event_id"), role));
  }
  if (m === "POST" && (match = p.match(/^\/api\/events\/([^/]+)\/actions$/))) {
    const role = roleOf(req);
    const actor = actorOf(req);
    const id = intParam(match[1], "event_id");
    const b = await body(req);
    if (!b || typeof b !== "object" || Array.isArray(b)) throw validation("body");
    if (!HUMAN_ACTIONS.includes(b.action)) throw validation("body.action");
    if (b.comment != null && typeof b.comment !== "string") throw validation("body.comment");
    return json(res, 200, mock.act(id, { action: b.action, comment: b.comment ?? "" }, role, actor));
  }
  if (m === "GET" && (match = p.match(/^\/api\/evidence\/([^/]+)\/image$/))) {
    const id = intParam(match[1], "evidence_id");
    const ev = mock.evidenceById(id);
    if (mock.faults.evidence404 || !ev?.bytes) throw apiError(404, "not_found", MSG.notFound, { evidence_id: id });
    res.writeHead(200, { ...res.cors, "Content-Type": "image/jpeg", "Cache-Control": "no-store" });
    return res.end(ev.bytes);
  }
  const route = contractRoutes.find((r) => r.re.test(p));
  if (route && route.methods.includes(m)) throw apiError(501, "not_implemented", MSG.notImplemented, { path: p });
  if (route) throw apiError(405, "method_not_allowed", MSG.requestInvalid, { method: m });
  throw apiError(404, "not_found", MSG.notFound, { path: p });
}

async function director(req, res, url) {
  const p = url.pathname.replace(/^\/__demo\/?/, "");
  if (req.method === "GET" && p === "status") return json(res, 200, mock.status());
  if (req.method !== "POST") throw apiError(405, "method_not_allowed", "POST");
  if (p === "next") {
    const out = mock.publishNext({ force: url.searchParams.get("force") === "1" });
    log(`demo next: ${out.published ? `#${out.published.id} ${out.published.notification_text}` : out.message}`);
    return json(res, out.refused ? 409 : 200, out);
  }
  if (p === "reset") {
    mock.reset();
    const dropped = dropWs(); // clients reconnect, get hello and reread their screens
    log(`demo reset: мир восстановлен, разорвано WS: ${dropped}`);
    return json(res, 200, { reset: true, ws_dropped: dropped, status: mock.status() });
  }
  if (p === "ws-drop") {
    const dropped = dropWs();
    log(`demo ws-drop: ${dropped}`);
    return json(res, 200, { ws_dropped: dropped });
  }
  const fault = p.match(/^fault\/(evidence-404|500|off)$/);
  if (fault) {
    mock.faults = { evidence404: fault[1] === "evidence-404", error500: fault[1] === "500" };
    log(`demo fault: ${fault[1]}`);
    return json(res, 200, { faults: mock.faults });
  }
  throw apiError(404, "not_found", MSG.notFound, { path: url.pathname });
}

const server = createServer(async (req, res) => {
  res.cors = corsHeaders(req.headers.origin);
  const url = new URL(req.url, `http://${HOST}`);
  if (req.method === "OPTIONS") {
    res.writeHead(204, res.cors);
    return res.end();
  }
  try {
    if (url.pathname.startsWith("/__demo")) await director(req, res, url);
    else await api(req, res, url);
  } catch (err) {
    if (!(err instanceof AppError)) {
      console.error(err);
      err = apiError(500, "internal", "Внутренняя ошибка мока");
    }
    json(res, err.status, { code: err.code, message: err.message, details: err.details });
  }
  if (!QUIET && !url.pathname.startsWith("/__demo")) log(`${req.method} ${url.pathname}${url.search} ${res.statusCode}`);
});

server.on("error", (e) => {
  console.error(e.code === "EADDRINUSE" ? `Порт ${REST_PORT} занят: остановите npm run mock или прежний мок` : e);
  process.exit(2);
});
wss.on("error", (e) => {
  console.error(e.code === "EADDRINUSE" ? `Порт ${WS_PORT} занят: остановите npm run mock или прежний мок` : e);
  process.exit(2);
});
server.listen(REST_PORT, HOST, () => {
  console.log(`SafeWatch demo mock: REST http://${HOST}:${REST_PORT}  WS ws://${HOST}:${WS_PORT}/ws`);
  console.log(`  автоэскалация 8.7: ${ESCALATION ? "ВКЛ (45 с)" : "выкл"}; синтетический эпизод с кадром: ${WITH_EPISODE ? "да" : "нет"}`);
  console.log(`  контракт для 501: ${contractRoutes.length ? "contract/openapi.json" : "не найден"}; режиссёр: node bin/demo.mjs next|reset|status|ws-drop|fault`);
});
