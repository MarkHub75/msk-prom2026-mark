// Browser transport for the checkpoint mock. No API requests leave this page.
import { Mock, AppError, previewBytes } from "./mock/state.mjs";
import { CONTRACT, HUMAN_ACTIONS, ROLES } from "./mock/world.mjs";
import { createRoutes } from "./routes.mjs";

const clients = new Set();
const base = import.meta.env.BASE_URL;
const asset = (path) => `${base}demo/${path}`;
const unavailable = "Недоступно в статическом демо";
let installed = false;
let networkFetch;

// Image elements do not use window.fetch: expose static URLs in REST and WS payloads.
function serialize(value) {
  return JSON.stringify(value, (_key, item) => {
    if (typeof item !== "string") return item;
    let match = item.match(/^\/api\/evidence\/([12])\/image$/);
    if (match) return asset(`evidence/${match[1] === "1" ? "yellow" : "red"}.jpg`);
    match = item.match(/^\/api\/cameras\/([1-7])\/preview$/);
    return match ? asset(`previews/cam-${match[1]}.jpg`) : item;
  });
}
function send(socket, type, data) {
  if (socket.readyState !== 1) return;
  const event = new MessageEvent("message", { data: serialize({type, at: new Date().toISOString(), data}) });
  socket.dispatchEvent(event);
  socket.onmessage?.(event);
}
function emit(type, data, audience = null) {
  // Match a real socket: mutations return before subscribers refetch their state.
  queueMicrotask(() => {
    for (const socket of clients) if (!audience || audience.includes(socket.role)) send(socket, type, data);
  });
}
const mock = new Mock({ emit, escalation: true });
const routes = createRoutes(mock);
const json = (body, status = 200) => new Response(serialize(body), {status, headers: {"Content-Type": "application/json; charset=utf-8"}});

async function api(request, url) {
  const p = url.pathname.startsWith(`${base}api/`) ? url.pathname.slice(base.length - 1) : url.pathname;
  const m = request.method;
  const q = url.searchParams;
  const req = {headers: Object.fromEntries(request.headers)};
  let match;
  if (m === "GET" && p === "/api/health") return json({ status: "ok", contract: CONTRACT });
  if (m === "GET" && p === "/api/meta") return json(routes.meta());
  if (m === "GET" && p === "/api/operator/dashboard") return json(mock.dashboard());
  if (m === "GET" && p === "/api/operator/feed") return json(mock.feed());
  if (m === "GET" && (match = p.match(/^\/api\/sectors\/(\d+)\/view$/))) return json(mock.sectorView(Number(match[1])));
  if (m === "GET" && p === "/api/sectors") return json(mock.sectors);
  if (m === "GET" && p === "/api/cameras") {
    const sid = q.has("sector_id") ? routes.intParam(q.get("sector_id"), "sector_id") : null;
    if (sid !== null && !mock.sector(sid)) throw new AppError(404, "not_found", "Сектор не найден");
    return json(mock.cameras.filter(c => sid === null || c.sector_id === sid).map(routes.publicCamera));
  }
  if (m === "GET" && p === "/api/events") return json(routes.eventsList(q));
  if (m === "GET" && p === "/api/journal/facets") return json(routes.facets());
  if (m === "GET" && p === "/api/master/inbox") return json(mock.masterInbox());
  if (m === "GET" && p === "/api/master/shift") return json(routes.shift(q));
  if (m === "GET" && (match = p.match(/^\/api\/events\/(\d+)$/))) return json(mock.detail(Number(match[1]), routes.roleOf(req)));
  if (m === "POST" && (match = p.match(/^\/api\/events\/(\d+)\/actions$/))) {
    let body;
    try { body = await request.json(); } catch { throw routes.validation("body"); }
    if (!body || typeof body !== "object" || Array.isArray(body)) throw routes.validation("body");
    if (!HUMAN_ACTIONS.includes(body.action)) throw routes.validation("body.action");
    if (body.comment != null && typeof body.comment !== "string") throw routes.validation("body.comment");
    return json(mock.act(Number(match[1]), {...body, comment: body.comment ?? ""}, routes.roleOf(req), routes.actorOf(req)));
  }
  if (m === "GET" && p === "/api/admin/cameras") return json({sectors: mock.sectors, cameras: mock.cameras.map(routes.publicCamera)});
  if (m === "GET" && (match = p.match(/^\/api\/cameras\/(\d+)$/))) {
    const camera = mock.camera(Number(match[1]));
    if (!camera) throw new AppError(404, "not_found", "Камера не найдена");
    return json(routes.publicCamera(camera));
  }
  if (m === "GET" && (match = p.match(/^\/api\/evidence\/([12])\/image$/))) {
    return networkFetch(asset(`evidence/${match[1] === "1" ? "yellow" : "red"}.jpg`), {signal: request.signal});
  }
  if (m === "GET" && (match = p.match(/^\/api\/cameras\/(\d+)\/preview$/))) {
    const id = Number(match[1]);
    if (!mock.camera(id)?.observed || !previewBytes(id)) throw new AppError(404, "not_found", "Кадр камеры недоступен");
    return networkFetch(asset(`previews/cam-${id}.jpg`), {signal: request.signal});
  }
  return json({ code: "not_implemented", message: unavailable, details: {path: p, method: m} }, 501);
}

export function nextStep() {
  // The director explicitly advances time: the unhandled yellow ends before the red.
  return mock.publishNext({force: true});
}
export function resetDemo() {
  mock.reset();
  window.dispatchEvent(new Event("argus:demo-reset"));
  for (const socket of clients) send(socket, "hello", {server_now: new Date().toISOString(), contract: CONTRACT, role: socket.role});
}

export function installStaticDemo() {
  if (installed) return;
  installed = true;
  networkFetch = globalThis.fetch.bind(globalThis);
  globalThis.fetch = async (input, init) => {
    const url = new URL(input instanceof Request ? input.url : input, location.href);
    if (!url.pathname.startsWith("/api/") && !url.pathname.startsWith(`${base}api/`)) return networkFetch(input, init);
    const effective = new Request(input instanceof Request ? input : url, init);
    if (effective.signal.aborted) throw effective.signal.reason ?? new DOMException("Aborted", "AbortError");
    try { return await api(effective, url); }
    catch (error) {
      if (error instanceof AppError) return json({code: error.code, message: error.message, details: error.details}, error.status);
      console.error("Static demo error", error);
      return json({code: "internal", message: "Ошибка статического демо", details: {}}, 500);
    }
  };
  const NativeWebSocket = globalThis.WebSocket;
  class DemoWebSocket extends EventTarget {
    static CONNECTING = 0; static OPEN = 1; static CLOSING = 2; static CLOSED = 3;
    CONNECTING = 0; OPEN = 1; CLOSING = 2; CLOSED = 3;
    readyState = 0;
    onopen = null; onmessage = null; onclose = null; onerror = null;
    bufferedAmount = 0; extensions = ""; protocol = ""; binaryType = "blob";
    constructor(url, protocols) {
      super();
      const parsed = new URL(url, location.href);
      if (parsed.pathname !== "/ws" && parsed.pathname !== `${base}ws`) return new NativeWebSocket(url, protocols);
      this.url = parsed.href;
      this.role = parsed.searchParams.get("role");
      setTimeout(() => {
        if (this.readyState !== 0) return;
        if (!ROLES.includes(this.role)) { this.close(4400, "unknown role"); return; }
        this.readyState = 1;
        clients.add(this);
        const event = new Event("open"); this.dispatchEvent(event); this.onopen?.(event);
        send(this, "hello", {server_now: new Date().toISOString(), contract: CONTRACT, role: this.role});
      }, 0);
    }
    send() {
      if (this.readyState !== 1) throw new DOMException("WebSocket is not open", "InvalidStateError");
    }
    close(code = 1000, reason = "") {
      if (this.readyState === 3) return;
      this.readyState = 3;
      clients.delete(this);
      queueMicrotask(() => {
        const event = new CloseEvent("close", {code, reason, wasClean: true});
        this.dispatchEvent(event); this.onclose?.(event);
      });
    }
  }
  globalThis.WebSocket = DemoWebSocket;
  setInterval(() => mock.escalationTick(), 500);
}
