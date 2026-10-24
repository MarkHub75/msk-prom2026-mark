// Smoke of the SafeWatch critical path against the demo mock or the real backend.
//   node bin/smoke.mjs --target mock|real [--rest URL] [--ws URL] [--timeout-s N]
//   [--contract DIR] [--json FILE]
// Prints a PASS/FAIL/SKIP table; exit 0 = ready, 1 = some FAIL, 3 = SKIPs only, 2 = bad arguments.
// Every REST answer and WS message is validated by contract/*.json when the files exist.
import { spawnSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import WebSocket from "ws";

const args = process.argv.slice(2);
const opt = (name, def) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : def;
};
const TARGET = opt("--target", "mock");
const DEFAULTS = {
  mock: { rest: "http://127.0.0.1:4010", ws: "ws://127.0.0.1:4011/ws" },
  real: { rest: "http://127.0.0.1:8000", ws: "ws://127.0.0.1:8000/ws" },
};
if (!DEFAULTS[TARGET]) {
  console.error("--target mock | real");
  process.exit(2);
}
const REST = opt("--rest", DEFAULTS[TARGET].rest);
const WS_URL = opt("--ws", DEFAULTS[TARGET].ws);
const WAIT_MS = Number(opt("--timeout-s", TARGET === "real" ? 90 : 5)) * 1000;
const MOCK = TARGET === "mock";

// --- contract validation -----------------------------------------------------------------
// --contract DIR: validate by another copy of contract/ (the watch loop passes the one of main).
const CONTRACT_DIR = opt("--contract", fileURLToPath(new URL("../../../contract/", import.meta.url)));
const OPENAPI_FILE = join(CONTRACT_DIR, "openapi.json");
const WS_SCHEMA_FILE = join(CONTRACT_DIR, "ws.schema.json");
const ajv = new Ajv2020({ strict: false, allErrors: false });
addFormats(ajv);
let openapi = null;
let validateWs = null;
if (existsSync(OPENAPI_FILE)) {
  openapi = JSON.parse(readFileSync(OPENAPI_FILE, "utf8"));
  ajv.addSchema({ $id: "sw-openapi", components: openapi.components });
}
if (existsSync(WS_SCHEMA_FILE)) validateWs = ajv.compile(JSON.parse(readFileSync(WS_SCHEMA_FILE, "utf8")));
const contractErrors = []; // [where, message]
const checked = { rest: 0, ws: 0 };

function responseSchema(method, url, status) {
  if (!openapi) return null;
  const path = new URL(url).pathname;
  for (const [tpl, ops] of Object.entries(openapi.paths)) {
    if (!new RegExp(`^${tpl.replace(/\{[^}]+\}/g, "[^/]+")}$`).test(path)) continue;
    const op = ops[method.toLowerCase()];
    if (!op) continue;
    const r = op.responses[String(status)] ?? op.responses[`${String(status)[0]}XX`] ?? op.responses.default;
    const schema = r?.content?.["application/json"]?.schema;
    if (!schema) return null;
    return JSON.parse(JSON.stringify(schema).replaceAll('"#/components/', '"sw-openapi#/components/'));
  }
  return null;
}

const compiled = new Map();
function checkRest(method, url, status, body) {
  const schema = responseSchema(method, url, status);
  if (!schema) return;
  const key = JSON.stringify(schema);
  if (!compiled.has(key)) compiled.set(key, ajv.compile(schema));
  const v = compiled.get(key);
  checked.rest += 1;
  if (!v(body)) contractErrors.push([`${method} ${new URL(url).pathname} ${status}`, ajv.errorsText(v.errors)]);
}

function checkWs(msg) {
  if (validateWs) checked.ws += 1;
  if (validateWs && !validateWs(msg)) contractErrors.push([`ws ${msg.type}`, ajv.errorsText(validateWs.errors)]);
}

// --- HTTP and WS helpers -----------------------------------------------------------------
async function http(method, path, { role, actor, body, raw } = {}) {
  const headers = {};
  if (role) headers["X-Role"] = role;
  if (actor != null) headers["X-Actor"] = actor;
  let payload;
  if (body instanceof FormData) payload = body;
  else if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }
  const url = REST + path;
  const res = await fetch(url, { method, headers, body: payload });
  const type = res.headers.get("content-type") ?? "";
  if (raw || !type.includes("json")) return { status: res.status, type, bytes: Buffer.from(await res.arrayBuffer()) };
  const data = await res.json();
  checkRest(method, url, res.status, data);
  return { status: res.status, type, data };
}

class WsClient {
  constructor(role) {
    this.role = role;
    this.messages = [];
    this.waiters = [];
    this.closeCode = null;
    this.socket = new WebSocket(`${WS_URL}?role=${encodeURIComponent(role)}`);
    this.socket.on("message", (raw) => {
      const msg = JSON.parse(String(raw));
      checkWs(msg);
      this.messages.push(msg);
      this.waiters = this.waiters.filter((w) => !w(msg));
    });
    this.closed = new Promise((resolve) => this.socket.on("close", (code) => resolve((this.closeCode = code))));
    this.socket.on("error", () => {});
  }
  // Resolves with the first message matching `pred`, or null; `fresh` ignores the ones already
  // received (on the backend the loop publishes the scene again every cycle).
  waitFor(pred, ms = WAIT_MS, fresh = false) {
    const seen = fresh ? null : this.messages.find(pred);
    if (seen) return Promise.resolve(seen);
    return new Promise((resolve) => {
      const timer = setTimeout(() => resolve(null), ms);
      this.waiters.push((m) => (pred(m) ? (clearTimeout(timer), resolve(m), true) : false));
    });
  }
  close() {
    this.socket.close();
  }
}

// --- reporting ---------------------------------------------------------------------------
const rows = [];
const skipReason = new Map(); // gate name -> reason; later steps of that gate SKIP
function record(result, step, detail = "") {
  rows.push({ result, step, detail });
}
class Skip extends Error {}
class Fail extends Error {}
const must = (cond, msg) => {
  if (!cond) throw new Fail(msg);
};

async function step(name, fn, { gate, needs = [] } = {}) {
  const blocked = [gate, ...needs].find((g) => g && skipReason.has(g));
  if (blocked) {
    if (gate && !skipReason.has(gate)) skipReason.set(gate, skipReason.get(blocked));
    return record("SKIP", name, skipReason.get(blocked));
  }
  try {
    const detail = await fn();
    record("PASS", name, detail ?? "");
    return true;
  } catch (e) {
    if (e instanceof Skip) {
      record("SKIP", name, e.message);
      if (gate) skipReason.set(gate, e.message);
    } else {
      record("FAIL", name, e instanceof Fail ? e.message : `${e.name}: ${e.message}`);
      if (gate) skipReason.set(gate, `зависит от «${name}»`);
    }
    return false;
  }
}

// 501 from a slice that is not done yet is a SKIP of the step, not a failure of the test.
function notReady(r, what) {
  if (r.status === 501) throw new Skip(`${what}: 501 ${r.data?.message ?? "not_implemented"}`);
  if (r.status === 404 && r.data?.detail === "Not Found") throw new Skip(`${what}: маршрута нет`);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// --- story sources: the director on the mock, the fake mode on the backend ---------------
const story = { cameraId: null, yellow: null, red: null, redStatus: null }; // redStatus: the last status the smoke reached

async function mockNext() {
  const r = await fetch(`${REST}/__demo/next`, { method: "POST" });
  must(r.status === 200, `__demo/next → ${r.status}`);
}

function makeVideo() {
  const dir = mkdtempSync(join(tmpdir(), "sw-smoke-"));
  // "synthetic" in the name, no run/fall words: FakeRemoteShell picks the scene `demo` (6.1).
  const file = join(dir, `synthetic_demo_${Date.now()}.mp4`);
  const r = spawnSync("ffmpeg", [
    "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc2=size=640x360:rate=25", "-t", "20",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-metadata", `comment=safewatch synthetic smoke ${Date.now()}`, file,
  ]);
  if (r.status !== 0) throw new Skip(`ffmpeg не смог собрать ролик: ${String(r.stderr).slice(0, 120)}`);
  return file;
}

async function realUploadAndBroadcast() {
  // Never start a real LinQ run from a smoke: the upload goes only to the fake or the CPU backend.
  const meta = await http("GET", "/api/meta");
  notReady(meta, "GET /api/meta");
  if (meta.data.inference_backend === "linq" && meta.data.fake !== true) {
    throw new Skip("бэкенд на настоящем LinQ (fake=false): запустите с SAFEWATCH_FAKE=1, загрузку не делаю");
  }
  const cams = await http("GET", "/api/cameras");
  notReady(cams, "GET /api/cameras");
  must(cams.status === 200 && Array.isArray(cams.data), `GET /api/cameras → ${cams.status}`);
  if (!cams.data.length) throw new Skip("камер нет: запустите бэкенд с --seed");
  const cam = cams.data.find((c) => c.name.startsWith("Камера 1.1")) ?? cams.data[0];
  story.cameraId = cam.id;
  const file = makeVideo();
  const form = new FormData();
  form.append("file", new Blob([readFileSync(file)], { type: "video/mp4" }), file.split(/[\\/]/).pop());
  const up = await http("POST", `/api/cameras/${cam.id}/videos`, { role: "admin", body: form });
  notReady(up, "загрузка видео");
  must(up.status === 201, `загрузка видео → ${up.status} ${up.data?.code ?? ""}`);
  const video = up.data.video;
  if (up.data.job) {
    const deadline = Date.now() + 180000;
    let job = up.data.job;
    while (!["done", "failed"].includes(job.status) && Date.now() < deadline) {
      await sleep(1000);
      const j = await http("GET", `/api/jobs/${job.id}`);
      notReady(j, "GET /api/jobs/{id}");
      job = j.data;
    }
    must(job.status === "done", `задача ${job.id}: ${job.status} ${job.error_code ?? ""}`);
  }
  const b = await http("GET", `/api/cameras/${cam.id}/broadcast`);
  notReady(b, "эфир");
  if (!b.data || b.data.status !== "playing" || b.data.video_id !== video.id) {
    const s = await http("POST", `/api/cameras/${cam.id}/broadcast`, { role: "admin", body: { video_id: video.id, loop: true } });
    notReady(s, "старт эфира");
    must(s.status === 201, `старт эфира → ${s.status} ${s.data?.code ?? ""}`);
  }
  return `камера ${cam.id}, видео ${video.id}`;
}

// --- the scenario ------------------------------------------------------------------------
const isCreated = (level) => (m) => m.type === "event.created" && m.data.level === level && (!story.cameraId || m.data.camera_id === story.cameraId);
const isNotif = (id, pred = () => true) => (m) => m.type === "notification" && m.data.event_id === id && pred(m.data);

async function main() {
  console.log(`SafeWatch smoke · target=${TARGET} · REST ${REST} · WS ${WS_URL}`);
  console.log(`контракт: ${openapi ? "contract/openapi.json" : "нет openapi.json"}, ${validateWs ? "contract/ws.schema.json" : "нет ws.schema.json"}`);
  let op;
  let master;

  await step("health", async () => {
    let r;
    try {
      r = await http("GET", "/api/health");
    } catch {
      throw new Fail(`сервер не отвечает на ${REST}`);
    }
    must(r.status === 200 && r.data.status === "ok", `health → ${r.status}`);
    return `contract ${r.data.contract}`;
  }, { gate: "server" });

  await step("meta", async () => {
    const r = await http("GET", "/api/meta");
    notReady(r, "GET /api/meta");
    must(r.status === 200, `meta → ${r.status}`);
    const active = r.data.scenarios.filter((s) => s.status === "active").map((s) => s.id);
    if (!MOCK && !r.data.scenarios.length) throw new Skip("meta.scenarios пусто: плагины running/fall ещё не подключены (S5)");
    must(active.includes("running") && active.includes("fall"), `active: ${active.join(",")}`);
    if (MOCK) must(r.data.fake === true, "fake должен быть true");
    return `fake=${r.data.fake}, active=${active.join(",")}`;
  }, { gate: "meta", needs: ["server"] });

  if (MOCK) {
    await step("reset мира (mock)", async () => {
      const r = await fetch(`${REST}/__demo/reset`, { method: "POST" });
      must(r.status === 200, `__demo/reset → ${r.status}`);
    }, { gate: "server" });
  }

  await step("dashboard", async () => {
    const r = await http("GET", "/api/operator/dashboard", { role: "operator" });
    notReady(r, "GET /api/operator/dashboard");
    must(r.status === 200 && Array.isArray(r.data.sectors), `dashboard → ${r.status}`);
    if (MOCK) must(r.data.sectors.length === 4, `секторов ${r.data.sectors.length}`);
    return `секторов ${r.data.sectors.length}, в ленте ${r.data.feed.length}`;
  }, { gate: "dashboard", needs: ["server"] });

  await step("WS operator: hello", async () => {
    op = new WsClient("operator");
    master = new WsClient("master");
    const h = await op.waitFor((m) => m.type === "hello", 5000);
    must(h && h.data.role === "operator", "нет hello у operator");
    must(await master.waitFor((m) => m.type === "hello", 5000), "нет hello у master");
    return `contract ${h.data.contract}`;
  }, { gate: "ws", needs: ["server"] });

  // ---- yellow ----
  await step(MOCK ? "жёлтое событие (demo next)" : "жёлтое событие (загрузка, задача, эфир)", async () => {
    if (MOCK) await mockNext();
    else return await realUploadAndBroadcast();
  }, { gate: "story", needs: ["server", "ws"] });

  await step("event.created + notification у operator", async () => {
    const created = await op.waitFor(isCreated("yellow"));
    must(created, `нет event.created жёлтого за ${WAIT_MS / 1000} с`);
    story.yellow = created.data;
    story.cameraId ??= created.data.camera_id;
    const n = await op.waitFor(isNotif(created.data.id), 3000);
    must(n, "нет notification у operator");
    must(n.data.sound === "chime" && n.data.takeover === false, `sound=${n.data.sound} takeover=${n.data.takeover}`);
    if (MOCK) must(created.data.reason_text === "Бег 2,4 роста/с", `reason ${created.data.reason_text}`);
    return `#${created.data.id} ${created.data.notification_text}`;
  }, { gate: "yellow", needs: ["server", "ws", "story"] });

  await step("жёлтое: notification НЕ у master", async () => {
    await sleep(500);
    must(!master.messages.some(isNotif(story.yellow.id)), "master получил жёлтое уведомление");
  }, { gate: "yellow", needs: ["server", "ws", "story"] });

  await step("карточка жёлтого + view сектора", async () => {
    const d = await http("GET", `/api/events/${story.yellow.id}`, { role: "operator" });
    notReady(d, "GET /api/events/{id}");
    must(d.status === 200, `карточка → ${d.status}`);
    must(d.data.allowed_actions.includes("confirm"), `allowed ${d.data.allowed_actions}`);
    const v = await http("GET", `/api/sectors/${story.yellow.sector_id}/view`, { role: "operator" });
    notReady(v, "GET /api/sectors/{id}/view");
    must(v.status === 200 && v.data.feed.some((e) => e.id === story.yellow.id), "события нет в ленте сектора");
    if (MOCK) must(v.data.sector.state === "yellow", `сектор ${v.data.sector.state}`);
    return `allowed=${d.data.allowed_actions.join(",")}, сектор ${v.data.sector.state}`;
  }, { gate: "yellow", needs: ["server", "ws", "story"] });

  await step("operator confirm жёлтого → confirmed", async () => {
    const r = await http("POST", `/api/events/${story.yellow.id}/actions`, { role: "operator", body: { action: "confirm" } });
    notReady(r, "POST actions");
    must(r.status === 200 && r.data.event.status === "confirmed", `→ ${r.status} ${r.data.event?.status ?? r.data.code}`);
    must(await op.waitFor((m) => m.type === "event.updated" && m.data.id === story.yellow.id && m.data.status === "confirmed", 3000), "нет event.updated");
  }, { gate: "yellow", needs: ["server", "ws", "story"] });

  // ---- red ----
  await step("красное событие", async () => {
    // A fresh red one: an older one may be timeout-escalated already (8.7, 45 s) while we waited.
    const fresh = op.waitFor(isCreated("red"), WAIT_MS, true);
    if (MOCK) await mockNext();
    const created = await fresh;
    must(created, `нет event.created красного за ${WAIT_MS / 1000} с`);
    story.red = created.data;
    story.redStatus = created.data.status;
    if (MOCK) must(created.data.reason_text === "Зафиксировано падение", `reason ${created.data.reason_text}`);
    return `#${created.data.id} ${created.data.notification_text}`;
  }, { gate: "red", needs: ["server", "ws", "story"] });

  await step("takeover-notification у operator, не у master", async () => {
    const n = await op.waitFor(isNotif(story.red.id), 3000);
    must(n && n.data.sound === "siren" && n.data.takeover === true, `notification ${JSON.stringify(n?.data)}`);
    must(n.data.audience.length === 1 && n.data.audience[0] === "operator", `audience ${n.data.audience}`);
    await sleep(300);
    must(!master.messages.some(isNotif(story.red.id)), "master получил уведомление до подтверждения");
  }, { gate: "red", needs: ["server", "ws", "story"] });

  await step("master: нет confirm в allowed_actions", async () => {
    const d = await http("GET", `/api/events/${story.red.id}`, { role: "master" });
    must(d.status === 200, `→ ${d.status}`);
    must(!d.data.allowed_actions.includes("confirm"), `allowed ${d.data.allowed_actions}`);
    return `allowed=[${d.data.allowed_actions.join(",")}]`;
  }, { gate: "red", needs: ["server", "ws", "story"] });

  await step("operator «Подтверждаю» → sent_to_master", async () => {
    const r = await http("POST", `/api/events/${story.red.id}/actions`, { role: "operator", actor: encodeURIComponent("Иван Петров"), body: { action: "confirm" } });
    must(r.status === 200 && r.data.event.status === "sent_to_master", `→ ${r.status} ${r.data.event?.status ?? r.data.code}`);
    story.redStatus = "sent_to_master";
  }, { gate: "red", needs: ["server", "ws", "story"] });

  await step("master получает notification (chime)", async () => {
    const n = await master.waitFor(isNotif(story.red.id), 3000);
    must(n && n.data.sound === "chime" && n.data.takeover === false && n.data.audience.includes("master"), `notification ${JSON.stringify(n?.data)}`);
    return n.data.text;
  }, { gate: "red", needs: ["server", "ws", "story"] });

  await step("событие во входящих мастера", async () => {
    const r = await http("GET", "/api/master/inbox", { role: "master" });
    notReady(r, "GET /api/master/inbox");
    must(r.status === 200 && r.data.active.some((e) => e.id === story.red.id), "нет в active");
  }, { gate: "inbox", needs: ["server", "ws", "story", "red"] });

  await step("master accept → master_accepted", async () => {
    const r = await http("POST", `/api/events/${story.red.id}/actions`, { role: "master", body: { action: "accept" } });
    must(r.status === 200 && r.data.event.status === "master_accepted", `→ ${r.status} ${r.data.event?.status ?? r.data.code}`);
    story.redStatus = "master_accepted";
  }, { gate: "red", needs: ["server", "ws", "story"] });

  await step("НЕГАТИВ resolve без комментария → 422", async () => {
    const r = await http("POST", `/api/events/${story.red.id}/actions`, { role: "master", body: { action: "resolve", comment: "  " } });
    must(r.status === 422, `→ ${r.status} ${r.data.code}`);
    return r.data.message;
  }, { gate: "red", needs: ["server", "ws", "story"] });

  await step("master resolve с комментарием → resolved", async () => {
    const r = await http("POST", `/api/events/${story.red.id}/actions`, { role: "master", body: { action: "resolve", comment: "Пострадавших нет, рабочее место осмотрено" } });
    must(r.status === 200 && r.data.event.status === "resolved", `→ ${r.status} ${r.data.event?.status ?? r.data.code}`);
    story.redStatus = "resolved";
  }, { gate: "red", needs: ["server", "ws", "story"] });

  await step("полная история actions в карточке", async () => {
    const d = await http("GET", `/api/events/${story.red.id}`, { role: "ohs" });
    const got = d.data.actions.map((a) => a.action);
    const want = ["published", "confirmed", "sent_to_master", "master_accepted", "resolved"];
    must(want.every((a) => got.includes(a)), `actions ${got.join(",")}`);
    must(got.indexOf("confirmed") < got.indexOf("sent_to_master"), "confirmed должно идти до sent_to_master");
    const op1 = d.data.actions.find((a) => a.action === "confirmed");
    must(op1.actor_name === "Иван Петров", `actor_name ${op1.actor_name}`);
    const res = d.data.actions.find((a) => a.action === "resolved");
    must(res.comment.length > 0, "у resolved нет комментария");
    return got.join(" → ");
  }, { gate: "red", needs: ["server", "ws", "story"] });

  await step("событие в журнале /api/events", async () => {
    const r = await http("GET", "/api/events?limit=200");
    notReady(r, "GET /api/events");
    must(r.status === 200 && r.data.items.some((e) => e.id === story.red.id && e.status === "resolved"), "нет в журнале");
    const f = await http("GET", "/api/journal/facets");
    notReady(f, "GET /api/journal/facets");
    must(f.status === 200, `facets → ${f.status}`);
    return `всего ${r.data.total}`;
  }, { gate: "journal", needs: ["server", "ws", "story", "red"] });

  // ---- negatives ----
  const anyEvent = () => story.red?.id ?? story.yellow?.id ?? 1;
  await step("НЕГАТИВ неизвестная X-Role → 400 role_required", async () => {
    const r = await http("GET", `/api/events/${anyEvent()}`, { role: "hacker" });
    notReady(r, "GET /api/events/{id}");
    must(r.status === 400 && r.data.code === "role_required", `→ ${r.status} ${r.data.code}`);
    const p = await http("POST", `/api/events/${anyEvent()}/actions`, { role: "hacker", body: { action: "view" } });
    must(p.status === 400 && p.data.code === "role_required", `POST → ${p.status} ${p.data.code}`);
  }, { needs: ["server"] });

  await step("НЕГАТИВ WS с неизвестной ролью → 4400", async () => {
    const c = new WsClient("hacker");
    const code = await Promise.race([c.closed, sleep(5000).then(() => null)]);
    must(code === 4400, `close ${code}`);
  }, { needs: ["server", "ws"] });

  await step("НЕГАТИВ неверный переход → 409 invalid_transition", async () => {
    const id = story.yellow?.id ?? 1; // without the story: event 1 of the seed, terminal
    const r = await http("POST", `/api/events/${id}/actions`, { role: "operator", body: { action: "view" } });
    notReady(r, "POST actions");
    must(r.status === 409 && r.data.code === "invalid_transition", `→ ${r.status} ${r.data.code}`);
  }, { needs: ["server"] });

  await step("НЕГАТИВ действие чужой роли → 403", async () => {
    const id = story.yellow?.id ?? 1;
    const r = await http("POST", `/api/events/${id}/actions`, { role: "master", body: { action: "confirm" } });
    notReady(r, "POST actions");
    must(r.status === 403, `→ ${r.status} ${r.data.code}`);
  }, { needs: ["server"] });

  await step("НЕГАТИВ X-Actor длиннее 60 → 422", async () => {
    const id = story.yellow?.id ?? 1;
    const r = await http("POST", `/api/events/${id}/actions`, { role: "operator", actor: encodeURIComponent("Я".repeat(61)), body: { action: "false_alarm" } });
    must(r.status === 422, `→ ${r.status} ${r.data.code}`);
  }, { needs: ["server"] });

  await step("evidence: кадр image/jpeg, затем 404 при fault", async () => {
    const d = await http("GET", `/api/events/${story.red?.id ?? anyEvent()}`, { role: "operator" });
    const ev = d.data?.episode?.evidence?.[0];
    if (!ev) throw new Skip("у события нет episode.evidence");
    const ok = await http("GET", ev.url, { raw: true });
    must(ok.status === 200 && ok.type.startsWith("image/jpeg"), `кадр → ${ok.status} ${ok.type}`);
    const unknown = await http("GET", "/api/evidence/999999/image");
    must(unknown.status === 404, `неизвестный кадр → ${unknown.status}`);
    if (!MOCK) return "fault evidence-404: только в моке";
    await fetch(`${REST}/__demo/fault/evidence-404`, { method: "POST" });
    const miss = await http("GET", ev.url);
    await fetch(`${REST}/__demo/fault/off`, { method: "POST" });
    must(miss.status === 404 && miss.data.code === "not_found", `при fault → ${miss.status}`);
    return `${ok.bytes.length} байт, fault → 404`;
  }, { needs: ["server"] });

  if (MOCK) await step("fault 500 → ApiError, затем off", async () => {
    await fetch(`${REST}/__demo/fault/500`, { method: "POST" });
    const r = await http("GET", "/api/operator/dashboard");
    await fetch(`${REST}/__demo/fault/off`, { method: "POST" });
    must(r.status === 500 && r.data.code === "internal", `→ ${r.status}`);
    const back = await http("GET", "/api/operator/dashboard");
    must(back.status === 200, `после off → ${back.status}`);
  }, { needs: ["server"] });

  await step("WS-разрыв → переподключение, hello, REST совпадает", async () => {
    if (MOCK) {
      await fetch(`${REST}/__demo/ws-drop`, { method: "POST" });
      const code = await Promise.race([op.closed, sleep(3000).then(() => null)]);
      must(code != null, "сервер не разорвал соединение");
    } else op.close();
    const again = new WsClient("operator");
    must(await again.waitFor((m) => m.type === "hello", 5000), "нет hello после переподключения");
    again.close();
    if (story.red && story.redStatus) {
      const d = await http("GET", `/api/events/${story.red.id}`, { role: "operator" });
      must(d.data.event.status === story.redStatus, `статус после разрыва ${d.data.event.status}, ожидался ${story.redStatus}`);
    }
    if (MOCK) {
      const dash = await http("GET", "/api/operator/dashboard");
      const s1 = dash.data.sectors.find((s) => s.sector_id === 1);
      must(s1.state === "normal" && s1.open_red === 0, `сектор 1: ${s1.state}, red ${s1.open_red}`);
    }
    return MOCK ? "server drop" : "client drop";
  }, { needs: ["server", "ws"] });

  await step("контракт: ответы и WS-сообщения по схемам", async () => {
    if (!openapi && !validateWs) throw new Skip("contract/*.json нет");
    must(!contractErrors.length, contractErrors.slice(0, 3).map(([w, m]) => `${w}: ${m}`).join(" | "));
    return `ответов ${checked.rest}, WS-сообщений ${checked.ws}: расхождений нет`;
  });

  op?.close();
  master?.close();
  if (MOCK) await fetch(`${REST}/__demo/reset`, { method: "POST" }).catch(() => {});
}

await main();
const width = Math.max(...rows.map((r) => r.step.length));
console.log("");
for (const r of rows) console.log(`${r.result.padEnd(4)}  ${r.step.padEnd(width)}  ${r.detail}`);
const count = (k) => rows.filter((r) => r.result === k).length;
console.log(`\nPASS ${count("PASS")} · FAIL ${count("FAIL")} · SKIP ${count("SKIP")} · target=${TARGET}`);
// 0: every step passed, the target is ready for the show; 1: a step failed; 3: no failures,
// but skipped steps (a slice is not done yet): not ready.
const verdict = count("FAIL") ? 1 : count("SKIP") ? 3 : 0;
console.log(
  verdict === 0 ? "ГОТОВ К ПОКАЗУ: весь сценарий прошёл"
    : verdict === 1 ? "НЕ ГОТОВ: есть FAIL"
      : "НЕ ГОТОВ: часть шагов SKIP (слайсы не закрыты), FAIL нет",
);
const jsonOut = opt("--json", null);
if (jsonOut) writeFileSync(jsonOut, JSON.stringify({ target: TARGET, verdict, rows, contract_errors: contractErrors }, null, 2));
process.exit(verdict);
