import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DemoConsolePage, isMockApi } from "./DemoConsole";
import { menuFor } from "../nav";
import { latestPack, packLabel } from "../demoPacks";
import type { DemoPack } from "../api/types";
import { setRole } from "../roles";

vi.mock("../api/ws", () => ({ useWs: () => ({ status: "connected" }) }));

const sectors = [{ id: 1, name: "Сектор 1 · Прессовый участок", sort_order: 1, is_demo: true }];
const cam = (id: number, name: string, videos_count = 1) => ({ id, sector_id: 1, name, description: "", is_demo: true, has_calibration: true, zones_count: 1, videos_count });
const video = (id: number, camera_id: number, over: object = {}) => ({ id, camera_id, filename: `clip-${id}.mp4`, sha256: "x", size_bytes: 1, width: 1280, height: 720, fps: 25, frame_count: 750, duration_ms: 30000, codec: "h264", browser_playable: true, status: "ready", active_analysis_id: id * 10, created_at: "2026-10-24T11:00:00Z", ...over });
const playing = { id: 4, camera_id: 2, video_id: 21, analysis_id: 210, status: "playing", loop: true, cycle: 0, started_at: "2026-10-24T11:00:00Z", position_ms: 5000, duration_ms: 30000, server_now: "2026-10-24T11:00:05Z" };

const packs = [
  { id: 1, name: "argus", sha256: "a1b2c3d4e5f6a7b8", backend: "linq", fake: false, cameras: 3, videos: 3, imported_at: "2026-10-24T14:00:00Z" },
  { id: 2, name: "rehearsal", sha256: "ffff0000ffff0000", backend: "linq", fake: true, cameras: 1, videos: 1, imported_at: "2026-10-24T15:00:00Z" },
];

interface Call { method: string; path: string; body?: unknown; role: string | null }

function stub() {
  const calls: Call[] = [];
  vi.stubGlobal("fetch", vi.fn(async (input: Request | URL | string, init?: RequestInit) => {
    const request = input instanceof Request ? input : new Request(input, init);
    const url = new URL(request.url);
    const body = request.method === "POST" && url.pathname.startsWith("/api") ? await request.json() : undefined;
    calls.push({ method: request.method, path: url.pathname, body, role: request.headers.get("X-Role") });
    if (url.pathname === "/api/admin/cameras") return Response.json({ sectors, cameras: [cam(1, "Камера 1.1 · Пресс"), cam(2, "Камера 1.2 · Склад"), cam(3, "Камера 1.3 · Пусто", 0)] });
    if (url.pathname === "/api/cameras/1/videos") return Response.json([video(11, 1, { status: "failed", active_analysis_id: null }), video(12, 1)]);
    if (url.pathname === "/api/cameras/2/videos") return Response.json([video(21, 2)]);
    if (url.pathname === "/api/cameras/1/broadcast" && request.method === "GET") return Response.json(null);
    if (url.pathname === "/api/cameras/2/broadcast" && request.method === "GET") return Response.json(playing);
    if (url.pathname.endsWith("/broadcast") && request.method === "POST") return Response.json({ ...playing, camera_id: 1, video_id: 12, loop: false }, { status: 201 });
    if (url.pathname.endsWith("/broadcast") && request.method === "DELETE") return new Response(null, { status: 204 });
    if (url.pathname === "/api/demo/packs") return Response.json(packs);
    if (url.pathname === "/__demo/status") return Response.json({ step: 1, story: ["yellow", "red"], open: 3 });
    if (url.pathname === "/__demo/next") return Response.json({ published: { id: 77, notification_text: "Красное событие: падение" } });
    if (url.pathname === "/__demo/reset") return Response.json({ reset: true, ws_dropped: 2 });
    return Response.json({ code: "not_found", message: "нет", details: {} }, { status: 404 });
  }));
  return calls;
}

beforeEach(() => setRole("admin"));
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("demo console", () => {
  it("is an admin menu item and detects the mock by its port", () => {
    expect(menuFor("admin").map((i) => i.path)).toContain("/admin/demo");
    expect(menuFor("operator").map((i) => i.path)).not.toContain("/admin/demo");
    expect(isMockApi("http://127.0.0.1:4010")).toBe(true);
    expect(isMockApi("http://127.0.0.1:8000")).toBe(false);
    expect(isMockApi("")).toBe(false);
  });

  it("plays a camera once, stops one and stops every broadcast", async () => {
    const calls = stub();
    render(<MemoryRouter><DemoConsolePage /></MemoryRouter>);
    expect(await screen.findByText("Камера 1.1 · Пресс")).toBeTruthy();
    expect(screen.getByText(/Пульт ведущего: управляет повтором записей, события создаёт конвейер/)).toBeTruthy();
    expect(screen.queryByText("Камера 1.3 · Пусто")).toBeNull();
    expect(screen.getByText("clip-12.mp4")).toBeTruthy();
    expect(screen.getByText("Идёт")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Следующий шаг" })).toBeNull();
    expect((screen.getByRole("button", { name: "Остановить: Камера 1.1 · Пресс" }) as HTMLButtonElement).disabled).toBe(true);

    fireEvent.click(screen.getByRole("button", { name: "Проиграть один раз: Камера 1.1 · Пресс" }));
    await waitFor(() => expect(calls.some((c) => c.method === "POST")).toBe(true));
    expect(calls.find((c) => c.method === "POST")).toMatchObject({ path: "/api/cameras/1/broadcast", body: { loop: false, video_id: 12 }, role: "admin" });

    fireEvent.click(screen.getByRole("button", { name: "Остановить: Камера 1.2 · Склад" }));
    await waitFor(() => expect(calls.some((c) => c.method === "DELETE" && c.path === "/api/cameras/2/broadcast")).toBe(true));

    await waitFor(() => expect((screen.getByRole("button", { name: "Остановить все эфиры" }) as HTMLButtonElement).disabled).toBe(false));
    const before = calls.filter((c) => c.method === "DELETE").length;
    fireEvent.click(screen.getByRole("button", { name: "Остановить все эфиры" }));
    expect(await screen.findByText("Остановлено эфиров: 1")).toBeTruthy();
    expect(calls.filter((c) => c.method === "DELETE").slice(before).map((c) => c.path)).toEqual(["/api/cameras/2/broadcast"]);
  });

  it("lists the imported demo packs with the source of their detections", async () => {
    stub();
    render(<MemoryRouter><DemoConsolePage /></MemoryRouter>);
    expect(await screen.findByText("Демо-пакет argus: детекции LinQ")).toBeTruthy();
    expect(screen.getByText("Демо-пакет rehearsal: фейк")).toBeTruthy();
    expect(packLabel({ name: "cpu", backend: "local", fake: false })).toBe("Демо-пакет cpu: детекции CPU (local)");
    expect(latestPack(packs as DemoPack[])?.name).toBe("rehearsal");
  });

  it("drives the mock scenario with next and reset", async () => {
    const calls = stub();
    render(<MemoryRouter><DemoConsolePage mockBase="http://127.0.0.1:4010" /></MemoryRouter>);
    expect(await screen.findByText("1 / 2")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Следующий шаг" }));
    expect(await screen.findByText("Опубликовано событие #77: Красное событие: падение")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Сбросить сценарий" }));
    expect(await screen.findByText(/Сценарий сброшен/)).toBeTruthy();
    expect(calls.filter((c) => c.path.startsWith("/__demo/") && c.method === "POST").map((c) => c.path)).toEqual(["/__demo/next", "/__demo/reset"]);
    expect(screen.queryByText(/Сброса мира через API нет/)).toBeNull();
  });

  it("disables the scenario buttons when the mock has no director", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => Response.json({ code: "not_found", message: "нет", details: {} }, { status: 404 })));
    render(<MemoryRouter><DemoConsolePage mockBase="http://127.0.0.1:4010" /></MemoryRouter>);
    expect(await screen.findByText(/Режиссёр не отвечает/)).toBeTruthy();
    expect((screen.getByRole("button", { name: "Следующий шаг" }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole("button", { name: "Сбросить сценарий" }) as HTMLButtonElement).disabled).toBe(true);
  });
});
