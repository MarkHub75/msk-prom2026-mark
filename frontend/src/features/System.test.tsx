import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { BackendStatus, Job, Schemas } from "../api/types";
import { SystemPage } from "./System";

const status = (patch: Partial<BackendStatus> = {}): BackendStatus => ({ backend: "linq", fake: false, state: "unchecked", checked_at: null, latency_ms: null, present: [], missing: [], message: "Не проверено", ...patch });
const metrics = (task: "detect" | "pose"): Schemas["InferenceMetrics"] => ({
  backend: "linq", fake: false, model_id: `${task}-yolov8n`, model_version: "640", task, input_size: 640, step: 2, frames_processed: 375, wall_s: 1,
  throughput_fps: 41.5, preprocess_ms: 1.2, postprocess_ms: 3.4, tpu_rtt_p50_ms: 18.5, tpu_rtt_p90_ms: 24, upload_s: 1.5, total_s: 12.25, cached: false,
});
const job = (id: number, patch: Partial<Job> = {}): Job => ({
  id, kind: "process", video_id: id, camera_id: 1, backend: "linq", fake: false, status: "done", stage: "done", progress: 1, attempts: 1,
  next_attempt_at: null, error_code: null, error_text: null, status_text: "", metrics: [metrics("detect"), metrics("pose")], analysis_id: 1, analysis_ms: 50,
  created_at: "2026-10-24T09:00:00Z", started_at: "2026-10-24T09:00:01Z", finished_at: "2026-10-24T09:00:13Z", ...patch,
});
const VIEW: Schemas["SystemView"] = {
  backend: "linq", fake: false, backend_status: status(), queue: [job(9, { status: "running", stage: "inference_pose", progress: 0.4, metrics: [], finished_at: null })],
  recent_jobs: [job(1), job(2, { status: "failed", stage: "inference_detect", metrics: [], error_code: "linq_unavailable", error_text: "Jupyter не ответил за 10 с" })],
  cameras: [{ camera_id: 1, sector_id: 1, state: "no_observation", reason: "stale", reason_text: "Данные анализа устарели", freshness_ms: 4200, open_yellow: 1, open_red: 0 }],
  models: [], latency: { notify_delay_s: { n: 12, pending: 1, p50: 0.8, p95: 2.5 }, publish_lag_ms: { n: 12, pending: 0, p50: 120, p95: 300 } },
  channels: [{ name: "АСУ ТП", kind: "webhook", target: "scada.local", levels: ["red"] }], server_now: "2026-10-24T09:01:00Z",
};

const PACKS: Schemas["DemoPack"][] = [
  { id: 1, name: "rehearsal", backend: "linq", fake: true, cameras: 1, videos: 1, sha256: "0123456789abcdef0123", imported_at: "2026-10-24T08:00:00Z" },
  { id: 2, name: "argus", backend: "linq", fake: false, cameras: 3, videos: 4, sha256: "fedcba9876543210fedc", imported_at: "2026-10-24T09:00:00Z" },
];

let packs: Schemas["DemoPack"][] | null;
let posts: string[];
let sockets: FakeSocket[];
class FakeSocket {
  onopen: (() => void) | null = null; onmessage: ((e: { data: string }) => void) | null = null; onclose: ((e: { code: number }) => void) | null = null; onerror: (() => void) | null = null;
  constructor() { sockets.push(this); }
  close() {}
}
function serve(check: BackendStatus, fail = false) {
  posts = [];
  vi.stubGlobal("fetch", vi.fn(async (request: Request) => {
    const path = new URL(request.url).pathname;
    if (request.method === "POST") { posts.push(path); return path.endsWith("/retry") ? Response.json(job(2, { status: "queued" })) : Response.json(check); }
    if (path === "/api/system") return fail ? Response.json({ code: "internal", message: "База недоступна", details: {} }, { status: 500 }) : Response.json(VIEW);
    if (path === "/api/models") return Response.json({ backend: "linq", fake: false, active: [], available: [] });
    if (path === "/api/health") return Response.json({ status: "ok", contract: "1.0.0" });
    if (path === "/api/demo/packs") return packs ? Response.json(packs) : Response.json({ code: "not_implemented", message: "Нет", details: {} }, { status: 501 });
    if (path === "/api/admin/cameras") return Response.json({ sectors: [{ id: 1, name: "Прессы", sort_order: 1, is_demo: false }], cameras: [{ id: 1, sector_id: 1, name: "Пресс №2", description: "", is_demo: false, has_calibration: false, zones_count: 0, videos_count: 1 }] });
    return Response.json({ code: "not_found", message: "Нет", details: {} }, { status: 404 });
  }));
}
const show = () => render(<MemoryRouter initialEntries={["/admin/system"]}><SystemPage /></MemoryRouter>);

beforeEach(() => { localStorage.clear(); sessionStorage.clear(); history.replaceState({}, "", "/?review=real"); sockets = []; packs = PACKS; vi.stubGlobal("WebSocket", FakeSocket); });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("system panel", () => {
  it("shows measurements, queue, freshness and channels as the API gives them", async () => {
    serve(status());
    show();
    await screen.findByTestId("system-view");
    expect(screen.getByTestId("backend-state").textContent).toContain("Не проверено");
    expect(screen.getAllByText("41,5")).toHaveLength(2);
    expect(screen.getAllByText("18,5").length).toBeGreaterThan(0);
    expect(screen.getByText("Выполняется")).toBeTruthy();
    expect(screen.getByText("Данные анализа устарели")).toBeTruthy();
    expect(screen.getByText("4,2 с")).toBeTruthy();
    expect(screen.getByText("АСУ ТП")).toBeTruthy();
    expect(screen.getByText("p95 2,5 с · n = 12")).toBeTruthy();
    expect(screen.getByText("Пресс №2", { selector: "a" })).toBeTruthy();
  });

  it("checks LinQ and shows an unreachable backend honestly", async () => {
    serve(status({ state: "unreachable", checked_at: "2026-10-24T09:01:05Z", message: "Jupyter не отвечает: таймаут 10 с", missing: ["mosprom_det.tpu"] }));
    show();
    fireEvent.click(await screen.findByTestId("backend-check"));
    await waitFor(() => expect(screen.getByTestId("backend-state").textContent).toContain("Не отвечает"));
    expect(screen.getByTestId("check-result").textContent).toContain("Jupyter не отвечает: таймаут 10 с");
    expect(screen.getByText("mosprom_det.tpu")).toBeTruthy();
    expect(posts).toEqual(["/api/system/backend-check"]);
  });

  it("updates the backend tile from the backend.status WS message", async () => {
    serve(status());
    show();
    await screen.findByTestId("system-view");
    const message = { type: "backend.status", at: "2026-10-24T09:02:00Z", data: status({ state: "ok", checked_at: "2026-10-24T09:02:00Z", latency_ms: 184, message: "LinQ отвечает" }) };
    act(() => { sockets.forEach(s => s.onopen?.()); sockets.forEach(s => s.onmessage?.({ data: JSON.stringify(message) })); });
    await waitFor(() => expect(screen.getByTestId("backend-state").textContent).toContain("Отвечает"));
    expect(screen.getByText("Живое обновление")).toBeTruthy();
  });

  it("retries a failed job and shows the API error of the whole screen", async () => {
    serve(status());
    show();
    await screen.findByText("Jupyter не ответил за 10 с");
    fireEvent.click(screen.getByRole("button", { name: "Повторить" }));
    await waitFor(() => expect(posts).toEqual(["/api/jobs/2/retry"]));
    cleanup();
    serve(status(), true);
    show();
    expect((await screen.findByRole("alert")).textContent).toContain("База недоступна");
  });

  it("lists the imported demo packs newest first and says where their detections come from", async () => {
    serve(status());
    show();
    const panel = await screen.findByTestId("system-packs");
    await waitFor(() => expect(panel.querySelectorAll("tbody tr")).toHaveLength(2));
    const rows = [...panel.querySelectorAll("tbody tr")].map(r => r.textContent);
    expect(rows[0]).toContain("argus");
    expect(rows[0]).toContain("детекции LinQ");
    expect(rows[0]).toContain("последний");
    expect(rows[1]).toContain("rehearsal");
    expect(rows[1]).toContain("фейк");
    expect(panel.getAttribute("data-panel")).toBe("Демо-пакеты · 2");
  });

  it("says so when the backend has no demo packs route", async () => {
    packs = null;
    serve(status());
    show();
    expect((await screen.findByTestId("system-packs")).textContent).toMatch(/Список пакетов недоступен \(501\)/);
  });
});
