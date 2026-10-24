import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { fixtureMeta } from "../fixtures/data";
import { AdminCamerasPage } from "./AdminCameras";
import { CameraSetupPage } from "./CameraSetup";
import { setRole } from "../roles";

vi.mock("../components/AppShell", () => ({ useMeta: () => fixtureMeta, useUpdates: () => 0 }));
vi.mock("../api/ws", () => ({ useWs: () => ({ status: "connected" }) }));

const sectors = [
  { id: 1, name: "Сектор 1 · Прессовый участок", sort_order: 1, is_demo: false },
  { id: 2, name: "Сектор 2 · Склад", sort_order: 2, is_demo: false },
];
const camera = { id: 7, sector_id: 1, name: "Камера 1.1 · Пресс", description: "Обзор пресса", is_demo: false, has_calibration: false, zones_count: 1, videos_count: 1 };
const state = { camera_id: 7, sector_id: 1, state: "no_observation", reason: "no_source", reason_text: "Нет источника видео", freshness_ms: null, open_yellow: 0, open_red: 0 };
const sectorState = (id: number, name: string) => ({ sector_id: id, name, state: "normal", reason_text: "", cameras_total: 1, cameras_no_observation: 0, open_yellow: 0, open_red: 0 });
const video = { id: 3, camera_id: 7, filename: "press.mp4", sha256: "x", size_bytes: 2_000_000, width: 1280, height: 720, fps: 25, frame_count: 200, duration_ms: 8000, codec: "h264", browser_playable: true, status: "failed", active_analysis_id: null, created_at: "2026-10-24T11:00:00Z" };
const metric = { backend: "linq", fake: true, model_id: "det-yolov8n", model_version: "640", task: "detect", input_size: 640, step: 2, frames_processed: 100, wall_s: 1, throughput_fps: 42.5, preprocess_ms: 1.2, postprocess_ms: 0.8, tpu_rtt_p50_ms: 10, tpu_rtt_p90_ms: 14, upload_s: 0.01, total_s: 2.4, cached: false };
const job = (over: object) => ({ id: 11, kind: "process", video_id: 3, camera_id: 7, backend: "linq", fake: true, status: "failed", stage: "inference_detect", progress: 0.2, attempts: 1, next_attempt_at: null, error_code: "model_missing", error_text: "нет хвоста модели", metrics: [], analysis_id: null, analysis_ms: null, created_at: "2026-10-24T11:00:00Z", started_at: null, finished_at: null, ...over });

afterEach(() => { cleanup(); vi.unstubAllGlobals(); setRole("admin"); });
beforeEach(() => { window.history.replaceState({}, "", "/"); });

describe("admin cameras", () => {
  it("lists sectors with counters and shows a 422 under its field", async () => {
    const posts: unknown[] = [];
    vi.stubGlobal("fetch", vi.fn(async (request: Request) => {
      const url = new URL(request.url);
      if (url.pathname === "/api/admin/cameras") return Response.json({ sectors, cameras: [camera] });
      const view = url.pathname.match(/^\/api\/sectors\/(\d+)\/view$/);
      if (view) { const s = sectors.find((x) => x.id === Number(view[1]))!; return Response.json({ sector: sectorState(s.id, s.name), cameras: s.id === 1 ? [{ camera, state, broadcast: null, preview_url: null }] : [] }); }
      if (url.pathname === "/api/sectors" && request.method === "POST") { posts.push(await request.json()); return Response.json({ code: "validation", message: "Название: от 1 до 80 символов", details: { field: "name" } }, { status: 422 }); }
      return Response.json({ code: "not_found", message: "нет", details: {} }, { status: 404 });
    }));
    render(<MemoryRouter initialEntries={["/admin/cameras"]}><AdminCamerasPage /></MemoryRouter>);
    expect(await screen.findByRole("link", { name: "Камера 1.1 · Пресс" })).toBeTruthy();
    await screen.findByText("Нет источника видео");
    fireEvent.click(screen.getByRole("button", { name: /^Сектор 2 · Склад/ }));
    await screen.findByText("В секторе нет камер");

    fireEvent.click(screen.getByRole("button", { name: "Новый сектор" }));
    const dialog = screen.getByRole("dialog", { name: "Новый сектор" });
    fireEvent.change(within(dialog).getByLabelText(/Название/), { target: { value: "  " } });
    fireEvent.click(within(dialog).getByRole("button", { name: "Создать сектор" }));
    await waitFor(() => expect(within(dialog).getByRole("alert").textContent).toContain("от 1 до 80 символов"));
    expect(posts).toEqual([{ name: "", sort_order: 3 }]);
    expect(within(dialog).getByRole("alert").closest(".adm-field")).toBeTruthy();
  });

  it("shows job metrics and retries a failed job", async () => {
    let retried = false;
    vi.stubGlobal("fetch", vi.fn(async (request: Request) => {
      const url = new URL(request.url);
      if (url.pathname === "/api/admin/cameras/7") return Response.json({ camera, videos: [video], jobs: [retried ? job({ status: "queued", error_code: null, error_text: null, progress: 0 }) : job({}), job({ id: 10, status: "done", stage: "done", progress: 1, error_code: null, error_text: null, metrics: [metric], created_at: "2026-10-24T10:00:00Z" })], calibration: null, zones: [], rules: [], broadcast: null });
      if (url.pathname === "/api/cameras/7/view") return Response.json({ camera, state, broadcast: null, video: null, analysis: null, zones: [], calibration: null });
      if (url.pathname === "/api/sectors") return Response.json(sectors);
      if (url.pathname === "/api/jobs/11/retry" && request.method === "POST") { retried = true; return Response.json(job({ status: "queued", error_code: null, error_text: null, progress: 0 })); }
      return Response.json({ code: "not_found", message: "нет", details: {} }, { status: 404 });
    }));
    render(<MemoryRouter initialEntries={["/admin/cameras/7"]}><Routes><Route path="/admin/cameras/:cameraId" element={<CameraSetupPage />} /></Routes></MemoryRouter>);
    expect(await screen.findByRole("heading", { name: "Камера 1.1 · Пресс" })).toBeTruthy();
    expect(screen.getByText("Анализ записи не удался")).toBeTruthy();
    expect(screen.getByText("нет хвоста модели")).toBeTruthy();
    expect(screen.getByText("42,5")).toBeTruthy();
    expect(screen.getByText("10 / 14")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Повторить задачу" }));
    await waitFor(() => expect(screen.queryByText("нет хвоста модели")).toBeNull());
    expect(retried).toBe(true);
    fireEvent.click(screen.getByRole("tab", { name: /Калибровка/ }));
    expect(screen.getByRole("tab", { name: /Калибровка/ }).getAttribute("aria-selected")).toBe("true");
  });
  it("opens the camera setup for the ohs role with its own breadcrumb and X-Role", async () => {
    setRole("ohs");
    const roles: (string | null)[] = [];
    vi.stubGlobal("fetch", vi.fn(async (request: Request) => {
      roles.push(request.headers.get("X-Role"));
      const url = new URL(request.url);
      if (url.pathname === "/api/admin/cameras/7") return Response.json({ camera, videos: [], jobs: [], calibration: null, zones: [], rules: [], broadcast: null });
      if (url.pathname === "/api/cameras/7/view") return Response.json({ camera, state, broadcast: null, video: null, analysis: null, zones: [], calibration: null });
      if (url.pathname === "/api/sectors") return Response.json(sectors);
      return Response.json({ code: "not_found", message: "нет", details: {} }, { status: 404 });
    }));
    render(<MemoryRouter initialEntries={["/admin/cameras/7"]}><Routes><Route path="/admin/cameras/:cameraId" element={<CameraSetupPage />} /></Routes></MemoryRouter>);
    expect(await screen.findByRole("heading", { name: "Камера 1.1 · Пресс" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Правила наблюдения" }).getAttribute("href")).toBe("/ohs/rules");
    expect(screen.getByText("Записей ещё нет")).toBeTruthy();
    expect(new Set(roles)).toEqual(new Set(["ohs"]));
  });
});
