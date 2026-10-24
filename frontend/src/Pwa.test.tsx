import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { MemoryRouter, useLocation } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";
import { createFixtureEvents, fixtureMeta } from "./fixtures/data";
import { setRole } from "./roles";

class LiveSocket { static last?: LiveSocket; onopen = null; onmessage: ((e: { data: string }) => void) | null = null; onclose = null; onerror = null; constructor() { LiveSocket.last = this; } close() {} }
const details = createFixtureEvents();
const base = details[0].event;
let healthDown = false;
function serve(routes: Record<string, unknown>) {
  vi.stubGlobal("fetch", async (request: Request) => {
    const path = new URL(request.url).pathname;
    if (path === "/api/health") { if (healthDown) throw new TypeError("Failed to fetch"); return Response.json({ status: "ok", contract: "1.1.0" }); }
    if (path === "/api/meta") return Response.json(fixtureMeta);
    if (path in routes) return Response.json(routes[path]);
    return Response.json({ code: "not_found", message: `нет ${path}`, details: {} }, { status: 404 });
  });
}
function Where() { return <output data-testid="where">{useLocation().pathname}</output>; }
const open = (path: string) => render(<MemoryRouter initialEntries={[path]}><App /><Where /></MemoryRouter>);
const phone = () => vi.stubGlobal("matchMedia", (query: string) => ({ matches: query.includes("760"), media: query, addEventListener() {}, removeEventListener() {} }));
const dashboard = { sectors: [], feed: [], server_now: base.published_at };
const send = (data: object) => act(() => LiveSocket.last?.onmessage?.({ data: JSON.stringify({ type: "notification", at: base.published_at, data }) }));

beforeEach(() => { localStorage.clear(); healthDown = false; history.replaceState({}, "", "/?review=real"); vi.stubGlobal("WebSocket", LiveSocket); });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); Reflect.deleteProperty(navigator, "serviceWorker"); Reflect.deleteProperty(navigator, "userAgent"); });

describe("installable app", () => {
  it("start_url /m/ opens the start screen of the saved role", async () => {
    serve({ "/api/operator/dashboard": dashboard, "/api/master/inbox": { server_now: base.published_at, active: [], recent_resolved: [] } });
    act(() => setRole("operator"));
    open("/m/");
    await waitFor(() => expect(screen.getByTestId("where").textContent).toBe("/m/operator"));
    cleanup();
    act(() => setRole("master"));
    open("/m/");
    await waitFor(() => expect(screen.getByTestId("where").textContent).toBe("/master"));
  });

  it("no answer from the server: the offline screen instead of data, back after a successful check", async () => {
    phone();
    act(() => setRole("operator"));
    healthDown = true;
    serve({ "/api/operator/dashboard": dashboard });
    open("/m/operator");
    expect(await screen.findByRole("heading", { name: "Нет связи с сервером — данные не показываются" })).toBeTruthy();
    expect(screen.queryByTestId("operator-view")).toBeNull();
    healthDown = false;
    fireEvent.click(screen.getByRole("button", { name: "Проверить связь" }));
    expect(await screen.findByTestId("operator-view")).toBeTruthy();
    expect(screen.queryByTestId("offline-screen")).toBeNull();
  });

  it("phone: a new red for the operator and a hand-over for the master come as system notifications through the worker", async () => {
    phone();
    const showNotification = vi.fn(async () => undefined);
    Object.defineProperty(navigator, "serviceWorker", { configurable: true, value: { getRegistration: async () => ({ showNotification }) } });
    vi.stubGlobal("Notification", Object.assign(function Notification() { throw new TypeError("Illegal constructor"); }, { permission: "granted" }));
    const vibrate = vi.fn(); Object.defineProperty(navigator, "vibrate", { configurable: true, value: vibrate });
    serve({ "/api/operator/dashboard": dashboard, "/api/master/inbox": { server_now: base.published_at, active: [], recent_resolved: [] }, "/api/events/41": details[0] });
    act(() => setRole("operator"));
    open("/m/operator");
    await screen.findByTestId("operator-view");
    send({ id: "e41:red", event_id: 41, level: "red", text: "Человек в зоне пресса", audience: ["operator"], sound: "siren", takeover: true });
    await waitFor(() => expect(showNotification).toHaveBeenCalledTimes(1));
    expect(showNotification).toHaveBeenCalledWith("АРГУС: красная тревога", expect.objectContaining({ body: "Человек в зоне пресса", tag: "event-41", requireInteraction: true, data: { url: "/m/operator/events/41" } }));
    expect(vibrate).toHaveBeenCalledWith([300, 120, 300]);
    cleanup();
    act(() => setRole("master"));
    open("/master/shift");
    await screen.findByTestId("master-shift").catch(() => undefined);
    send({ id: "e42:to_master", event_id: 42, level: "yellow", text: "Падение · Сектор 4", audience: ["master"], sound: "chime", takeover: false });
    await waitFor(() => expect(showNotification).toHaveBeenCalledTimes(2));
    expect(showNotification).toHaveBeenLastCalledWith("АРГУС: новое поручение", expect.objectContaining({ tag: "event-42", data: { url: "/master/events/42" } }));
  });

  it("profile sheet: «Установить на телефон» from Chrome's prompt; on iOS the Share hint", async () => {
    phone();
    serve({ "/api/operator/dashboard": dashboard });
    act(() => setRole("operator"));
    open("/m/operator");
    await screen.findByTestId("operator-view");
    const prompt = vi.fn(async () => undefined);
    act(() => { window.dispatchEvent(Object.assign(new Event("beforeinstallprompt", { cancelable: true }), { prompt, userChoice: Promise.resolve({ outcome: "accepted" }) })); });
    fireEvent.click(screen.getByRole("button", { name: "Профиль и роль" }));
    fireEvent.click(await screen.findByRole("button", { name: "Установить на телефон" }));
    await waitFor(() => expect(prompt).toHaveBeenCalled());
    await waitFor(() => expect(screen.queryByRole("button", { name: "Установить на телефон" })).toBeNull());
    cleanup();
    Object.defineProperty(navigator, "userAgent", { configurable: true, value: "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1" });
    open("/m/operator");
    await screen.findByTestId("operator-view");
    fireEvent.click(screen.getByRole("button", { name: "Профиль и роль" }));
    expect((await screen.findByTestId("ios-install-hint")).textContent).toContain("«Поделиться» → «На экран „Домой“»");
  });
});

describe("service worker (public/sw.js)", () => {
  function loadWorker() {
    const handlers: Record<string, (event: unknown) => void> = {};
    const self = { location: new URL("http://app.test/"), addEventListener: (type: string, fn: (event: unknown) => void) => { handlers[type] = fn; }, clients: {}, skipWaiting: async () => undefined };
    const cache = { match: async () => undefined, put: async () => undefined, add: async () => undefined, keys: async () => [], delete: async () => true };
    new Function("self", "caches", "fetch", readFileSync("public/sw.js", "utf8"))(self, { open: async () => cache, keys: async () => [] }, async () => new Response("", { headers: { "Content-Type": "text/html" } }));
    const fetchEvent = (url: string, init: { method?: string; mode?: string } = {}) => {
      const respondWith = vi.fn();
      handlers.fetch({ request: { url: `http://app.test${url}`, method: init.method ?? "GET", mode: init.mode ?? "cors" }, respondWith });
      return respondWith;
    };
    return { handlers, fetchEvent };
  }
  it("never answers /api or /ws from a cache; serves the shell and hashed assets", () => {
    const { handlers, fetchEvent } = loadWorker();
    expect(Object.keys(handlers).sort()).toEqual(["activate", "fetch", "install", "notificationclick"]);
    for (const url of ["/api/events?limit=50", "/api/events/41", "/api/videos/4/file", "/ws", "/ws/events"]) expect(fetchEvent(url)).not.toHaveBeenCalled();
    expect(fetchEvent("/api/events/41/actions", { method: "POST" })).not.toHaveBeenCalled();
    expect(fetchEvent("/api/health", { mode: "navigate" })).not.toHaveBeenCalled();
    expect(fetchEvent("/m/operator", { mode: "navigate" })).toHaveBeenCalled();
    expect(fetchEvent("/assets/index-abc123.js")).toHaveBeenCalled();
    expect(fetchEvent("/icons/icon-192.png")).toHaveBeenCalled();
  });
});
