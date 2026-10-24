import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../App";
import { createFixtureEvents, fixtureMeta } from "../fixtures/data";
import { setRole } from "../roles";
import type { EventDetail, EventSummary, HumanAction } from "../api/types";

class QuietSocket { onopen = null; onmessage = null; onclose = null; onerror = null; close() {} }
const details = createFixtureEvents();
const base = details[0].event;
const ago = (s: number) => new Date(Date.parse(base.published_at) - s * 1000).toISOString();
const fall = (id: number, s: number, extra: Partial<EventSummary> = {}): EventSummary => ({ ...base, id, published_at: ago(s), started_at: ago(s), camera_id: 8, camera_name: "Камера 5.1 · Публичный датасет падений", scenario: "fall", title: "Падение и неподвижность", level: "yellow", priority: 2, status: "new", status_title: "Новое", operator_verdict: "none", escalated_by_timeout: false, ...extra });
const other = (id: number): EventSummary => ({ ...base, id, camera_id: 1, scenario: "running", title: "Бег и резкие перемещения", level: "yellow", priority: 2, status: "new", status_title: "Новое" });

function serve(routes: Record<string, unknown>) {
  const posts: { path: string; action: HumanAction }[] = [];
  vi.stubGlobal("fetch", async (request: Request) => {
    const path = new URL(request.url).pathname;
    if (request.method === "POST") { const body = await request.json() as { action: HumanAction }; posts.push({ path, action: body.action }); return Response.json(routes[path.replace(/\/actions$/, "")] ?? {}); }
    if (path === "/api/meta") return Response.json(fixtureMeta);
    if (path in routes) return Response.json(routes[path]);
    return Response.json({ code: "not_found", message: `нет ${path}`, details: {} }, { status: 404 });
  });
  return posts;
}
const open = (path: string) => render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>);
const phone = () => vi.stubGlobal("matchMedia", (query: string) => ({ matches: query.includes("760"), media: query, addEventListener() {}, removeEventListener() {} }));
const feed = [fall(11, 150), fall(12, 60), fall(13, 0), other(20)];
const dashboard = { sectors: [], feed, server_now: base.published_at };

beforeEach(() => { localStorage.clear(); sessionStorage.clear(); history.replaceState({}, "", "/?review=real"); vi.stubGlobal("WebSocket", QuietSocket); });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("repeats of one camera and scenario", () => {
  it("desktop operator queue shows them as one row with the latest and expands to the list", async () => {
    act(() => setRole("operator"));
    serve({ "/api/operator/dashboard": dashboard });
    open("/operator");
    const group = await screen.findByTestId("repeat-group");
    expect(group.textContent).toContain("Падение и неподвижность · Камера 5.1 · ×3 за 3 мин");
    expect(group.textContent).toContain("#13");
    expect(screen.getAllByText("Бег и резкие перемещения").length).toBeGreaterThan(0);
    fireEvent.click(within(group).getByRole("button", { name: /Все 3 повторов/ }));
    expect([...group.querySelectorAll(".cr-q-sub > li")].map(li => li.textContent?.match(/#(\d+)/)?.[1])).toEqual(["13", "12", "11"]);
  });

  it("master accepts the whole group with one «Принял, иду»", async () => {
    act(() => setRole("master"));
    localStorage.setItem("safewatch.actor", "Мастер Петров");
    const waiting = feed.slice(0, 3).map(e => ({ ...e, status: "sent_to_master" as const, status_title: "Передано мастеру", escalated_by_timeout: true }));
    const posts = serve({ "/api/master/inbox": { server_now: base.published_at, active: waiting, recent_resolved: [] } });
    open("/master");
    const group = await screen.findByTestId("repeat-group");
    expect(group.textContent).toContain("×3 за 3 мин");
    fireEvent.click(within(group).getByRole("button", { name: "Принял, иду · ×3" }));
    await waitFor(() => expect(posts.map(p => p.path).sort()).toEqual(["/api/events/11/actions", "/api/events/12/actions", "/api/events/13/actions"]));
    expect(posts.every(p => p.action === "accept")).toBe(true);
  });

  it("journal folds repeats with «Группировать повторы» and remembers the choice", async () => {
    act(() => setRole("ohs"));
    const closed = feed.map(e => ({ ...e, status: "resolved" as const, status_title: "Решено", priority: 0 }));
    serve({ "/api/events": { items: closed, total: closed.length, next_cursor: null } });
    const view = open("/ohs/journal");
    await waitFor(() => expect(view.container.querySelectorAll("tr[data-event-id]").length).toBe(4));
    fireEvent.click(screen.getByLabelText("Группировать повторы"));
    const group = await screen.findByTestId("repeat-group");
    expect(group.textContent).toContain("×3 за 3 мин");
    expect(view.container.querySelectorAll("tr[data-event-id]").length).toBe(1);
    expect(localStorage.getItem("safewatch.journal.group")).toBe("1");
    fireEvent.click(within(group).getByRole("button", { name: /Показать все 3/ }));
    expect(view.container.querySelectorAll("tr[data-event-id]").length).toBe(4);
  });
});

describe("operator on a phone", () => {
  it("is an app with bottom tabs and grouped alarm cards", async () => {
    phone();
    act(() => setRole("operator"));
    serve({ "/api/operator/dashboard": dashboard });
    open("/operator");
    expect(await screen.findByRole("heading", { name: "Тревоги" })).toBeTruthy();
    const tabs = screen.getByRole("navigation", { name: "Разделы приложения" });
    expect(within(tabs).getAllByRole("link").map(a => a.getAttribute("href"))).toEqual(["/operator", "/operator/cameras", "/operator/shift"]);
    expect((await screen.findByTestId("repeat-group")).textContent).toContain("×3 за 3 мин");
    expect(screen.getAllByTestId("alarm-card").length).toBe(1);
    expect(screen.queryByRole("navigation", { name: "Разделы" })).toBeNull();
  });

  it("event card puts the three decisions at the bottom and can apply one to all repeats", async () => {
    phone();
    act(() => setRole("operator"));
    localStorage.setItem("safewatch.actor", "Оператор Иванова");
    const detail: EventDetail = { ...details[0], event: feed[2], allowed_actions: ["confirm", "false_alarm", "send_to_master"], video_id: null, broadcast: null };
    const posts = serve({ "/api/events/13": detail, "/api/operator/dashboard": dashboard });
    const view = open("/events/13");
    const confirm = await screen.findByRole("button", { name: "Подтверждаю · ×3" });
    expect([...view.container.querySelectorAll(".mb-actionbar button[data-action]")].map(b => b.textContent)).toEqual(["Подтверждаю · ×3", "Ложное срабатывание", "Передать мастеру"]);
    fireEvent.click(confirm);
    await waitFor(() => expect(posts.map(p => p.path).sort()).toEqual(["/api/events/11/actions", "/api/events/12/actions", "/api/events/13/actions"]));
    expect(posts.every(p => p.action === "confirm")).toBe(true);
  });
});

class LiveSocket { static last?: LiveSocket; onopen = null; onmessage: ((e: { data: string }) => void) | null = null; onclose = null; onerror = null; constructor() { LiveSocket.last = this; } close() {} }

describe("tech.md v5 mobile routes", () => {
  it("/m/operator is the one-column feed at any width; cards open /m/operator/events/:id with the clip", async () => {
    act(() => setRole("operator"));
    const clip = { video_id: 3, url: "/api/videos/3/file#t=1.5,9.0", start_ms: 1500, end_ms: 9000, playable: true };
    const withClip = { ...feed[3], clip };
    const detail: EventDetail = { ...details[0], event: withClip, allowed_actions: ["confirm", "false_alarm", "send_to_master"], video_id: null, broadcast: null };
    serve({ "/api/operator/dashboard": { ...dashboard, feed: [...feed.slice(0, 3), withClip] }, "/api/events/20": detail });
    open("/m/operator");
    expect(await screen.findByRole("heading", { name: "Тревоги" })).toBeTruthy();
    const card = await screen.findByTestId("alarm-card");
    expect(within(card).getAllByRole("link")[0].getAttribute("href")).toBe("/m/operator/events/20");
    fireEvent.click(within(card).getAllByRole("link")[0]);
    const player = await screen.findByTestId("clip-player");
    expect(player.querySelector("video")?.getAttribute("src")).toContain("/api/videos/3/file#t=1.5,9.0");
    expect(screen.getByRole("link", { name: /Тревоги/ }).getAttribute("href")).toBe("/m/operator");
  });

  it("/master opens the card itself when an event is handed over (to_master)", async () => {
    vi.stubGlobal("WebSocket", LiveSocket);
    act(() => setRole("master"));
    const handed = { ...feed[2], status: "sent_to_master" as const, status_title: "Передано мастеру" };
    serve({ "/api/master/inbox": { server_now: base.published_at, active: [handed], recent_resolved: [] }, "/api/events/13": { ...details[0], event: handed, allowed_actions: ["accept"], video_id: null, broadcast: null } });
    open("/master");
    await screen.findByTestId("master-inbox");
    act(() => LiveSocket.last?.onmessage?.({ data: JSON.stringify({ type: "notification", at: base.published_at, data: { id: "e13:to_master", event_id: 13, level: "yellow", text: "Падение", audience: ["master"], sound: "chime", takeover: false } }) }));
    expect(await screen.findByTestId("master-detail")).toBeTruthy();
    expect(await screen.findByRole("button", { name: "Принял, иду" })).toBeTruthy();
  });
});
