import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../App";
import { createFixtureEvents, fixtureCameras, fixtureMeta, fixtureSectors, fixtureVideo, fixtureZones } from "../fixtures/data";
import { setRole } from "../roles";
import type { CameraTile, EventDetail, EventSummary, HumanAction } from "../api/types";

class QuietSocket { onopen = null; onmessage = null; onclose = null; onerror = null; close() {} }
const details = createFixtureEvents();
const summary = details[0].event;
const tile = (id: number, state: CameraTile["state"]["state"], reason_text: string, preview: boolean): CameraTile => ({
  camera: fixtureCameras.find(c => c.id === id) ?? { ...fixtureCameras[0], id },
  state: { camera_id: id, sector_id: 1, state, reason: state === "no_observation" ? "no_source" : null, reason_text, freshness_ms: state === "no_observation" ? null : 40, open_red: 1, open_yellow: 0 },
  preview_url: preview ? `/api/cameras/${id}/preview` : null, broadcast: null,
});

function serve(routes: Record<string, unknown>) {
  const posts: { path: string; body: { action: HumanAction; comment: string } }[] = [];
  vi.stubGlobal("fetch", async (request: Request) => {
    const path = new URL(request.url).pathname;
    if (request.method === "POST") { const body = await request.json() as { action: HumanAction; comment: string }; posts.push({ path, body }); return Response.json(routes[`POST ${path}`] ?? routes[path]); }
    if (path === "/api/meta") return Response.json(fixtureMeta);
    if (path in routes) return Response.json(routes[path]);
    return Response.json({ code: "not_found", message: `нет ${path}`, details: {} }, { status: 404 });
  });
  return posts;
}
const open = (path: string) => render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>);

beforeEach(() => { localStorage.clear(); sessionStorage.clear(); history.replaceState({}, "", "/?review=real"); vi.stubGlobal("WebSocket", QuietSocket); });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("operator depth", () => {
  it("sector screen shows camera tiles with the no-observation reason and the sector feed", async () => {
    act(() => setRole("operator"));
    serve({
      "/api/sectors": fixtureSectors,
      "/api/sectors/1/view": { sector: { sector_id: 1, name: "Сектор 1 · Прессовый участок", state: "no_observation", reason_text: "Нет наблюдения: 1 из 2 камер", cameras_total: 2, cameras_no_observation: 1, open_yellow: 0, open_red: 1 }, cameras: [tile(1, "red", "Красная опасность", true), tile(2, "no_observation", "Нет источника видео", false)], feed: [summary] },
    });
    open("/operator/sectors/1");
    expect(await screen.findByTestId("sector-view")).toBeTruthy();
    expect((await screen.findAllByTestId("sector-camera")).length).toBe(2);
    expect(screen.getAllByText("Нет источника видео").length).toBeGreaterThan(0);
    expect(screen.getByText("Нет наблюдения: 1 из 2")).toBeTruthy();
    expect(screen.getAllByText(summary.title).length).toBeGreaterThan(0);
  });

  it("camera screen shows the player panel, properties and the episode timeline", async () => {
    act(() => setRole("operator"));
    const camera = fixtureCameras[0];
    serve({
      "/api/sectors": fixtureSectors,
      [`/api/cameras/${camera.id}/view`]: { camera, state: tile(camera.id, "normal", "Норма", true).state, video: { ...fixtureVideo(camera.id), browser_playable: false }, broadcast: null, analysis: null, zones: fixtureZones(camera.id), calibration: null },
      "/api/events": { items: [summary], total: 1, next_cursor: null },
    });
    open(`/operator/cameras/${camera.id}`);
    expect(await screen.findByText("Скрыть HUD")).toBeTruthy();
    expect(screen.getByLabelText("Таймлайн эпизодов")).toBeTruthy();
    expect(screen.getByText("нет · меры в ростах человека")).toBeTruthy();
  });

  it("event card orders actions 1-2-3 and shows the episode history", async () => {
    act(() => setRole("operator"));
    const detail: EventDetail = { ...details[0], allowed_actions: ["confirm", "false_alarm", "send_to_master"], video_id: null, broadcast: null };
    serve({ [`/api/events/${detail.event.id}`]: detail });
    const view = open(`/events/${detail.event.id}`);
    expect(await screen.findByText("История эпизода")).toBeTruthy();
    const keys = [...view.container.querySelectorAll("button[data-action] kbd")].map(k => k.textContent);
    expect(keys).toEqual(["1", "2", "3"]);
    expect(screen.getByText("Начало эпизода")).toBeTruthy();
    expect(screen.getByText("Происхождение")).toBeTruthy();
  });
});

describe("master", () => {
  const escalated: EventSummary = { ...summary, id: 77, status: "sent_to_master", status_title: "Передано мастеру", escalated_by_timeout: true, operator_verdict: "none" };
  it("inbox shows big active cards with the unconfirmed mark and resolved below", async () => {
    act(() => setRole("master"));
    serve({ "/api/master/inbox": { server_now: summary.published_at, active: [escalated], recent_resolved: [{ ...summary, id: 78, status: "resolved", status_title: "Решено" }] } });
    open("/master");
    expect(await screen.findByText("Открыть и принять")).toBeTruthy();
    expect(screen.getByText("Не подтверждено оператором")).toBeTruthy();
    expect(screen.getByText("Решено")).toBeTruthy();
    expect(screen.getByTestId("master-inbox")).toBeTruthy();
  });

  it("master card requires the measures before «Решено»", async () => {
    act(() => setRole("master"));
    localStorage.setItem("safewatch.actor", "Мастер Петров");
    const detail: EventDetail = { ...details[0], event: { ...escalated, status: "master_accepted", status_title: "Мастер принял" }, allowed_actions: ["resolve"] };
    const posts = serve({ "/api/events/77": detail });
    open("/master/events/77");
    const done = await screen.findByRole("button", { name: /Решено/ });
    expect(done.hasAttribute("disabled")).toBe(true);
    fireEvent.change(screen.getByTestId("measures"), { target: { value: "Пресс остановлен, сотрудник осмотрен" } });
    expect(done.hasAttribute("disabled")).toBe(false);
    fireEvent.click(done);
    await waitFor(() => expect(posts.some(p => p.body.action === "resolve")).toBe(true));
    expect(posts.find(p => p.body.action === "resolve")?.body.comment).toBe("Пресс остановлен, сотрудник осмотрен");
  });

  it("shift summary shows totals by sector and scenario from the server", async () => {
    act(() => setRole("master"));
    serve({ "/api/master/shift": { shift_id: "day", title: "Дневная смена", start: "2026-10-24T05:00:00Z", end: "2026-10-24T17:00:00Z", total: 9, by_sector: [{ key: "1", title: "Сектор 1 · Прессовый участок", count: 9, confirmed: 4, false_alarm: 2 }], by_scenario: [{ key: "fall", title: "Падение и неподвижность", count: 9, confirmed: 4, false_alarm: 2 }], events: [] } });
    open("/master/shift");
    expect(await screen.findByText("Дневная смена")).toBeTruthy();
    expect(screen.getByText("9", { selector: ".ms-kpi-main b" })).toBeTruthy();
    expect(screen.getByText("Падение и неподвижность")).toBeTruthy();
    expect(screen.getByText("3", { selector: ".ms-kpis b" })).toBeTruthy();
  });
});
