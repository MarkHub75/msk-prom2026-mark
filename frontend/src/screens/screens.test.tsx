import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { api } from "../api/client";
import { CameraSetup } from "./admin/CameraSetup";
import { CamerasScreen } from "./admin/CamerasScreen";
import { SystemScreen } from "./admin/SystemScreen";

// One smoke test per screen (tech.md 10.1): the screen renders with a stubbed `api`.
vi.mock("../api/client", () => ({
  api: { GET: vi.fn(), POST: vi.fn(), PUT: vi.fn(), PATCH: vi.fn(), DELETE: vi.fn() },
  apiError: (e: { code: string; message: string }) => e,
  uploadVideo: vi.fn(),
  videoUrl: (id: number) => `/api/videos/${id}/file`,
  apiUrl: (path: string) => path,
}));
vi.mock("../api/ws", () => ({ useWs: vi.fn() }));

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe("screens", () => {
  it("cameras_screen_renders", async () => {
    vi.mocked(api.GET).mockResolvedValue({
      data: {
        sectors: [{ id: 1, name: "Прессовый участок", sort_order: 0, is_demo: false }],
        cameras: [
          {
            id: 7, sector_id: 1, name: "Пресс №2", description: "", is_demo: false,
            has_calibration: false, zones_count: 0, videos_count: 0,
          },
        ],
      },
    } as never);
    const taken = { code: "name_taken", message: "Сектор с таким названием уже есть" };
    vi.mocked(api.POST).mockResolvedValue({ error: taken } as never);
    render(<CamerasScreen />);
    expect(await screen.findByText("Пресс №2")).toBeTruthy();
    expect(screen.getAllByText("Прессовый участок").length).toBe(2); // sector row, camera row

    fireEvent.click(screen.getByText("Новый сектор"));
    fireEvent.change(screen.getByLabelText("Название"), { target: { value: "Прессовый участок" } });
    fireEvent.click(screen.getByText("Сохранить"));
    expect((await screen.findByRole("alert")).textContent).toBe(taken.message);

    fireEvent.click(screen.getByText("Отмена"));
    fireEvent.click(screen.getAllByText("Удалить")[1]);
    expect(screen.getByText(/Удалить камеру «Пресс №2»/)).toBeTruthy();
  });

  it("camera_setup_renders", async () => {
    const metrics = {
      backend: "linq", fake: true, model_id: "det-yolov8n", model_version: "640-ap9999", task: "detect",
      input_size: 640, step: 2, frames_processed: 38, wall_s: 1, throughput_fps: 21.5, preprocess_ms: 1,
      postprocess_ms: 1, tpu_rtt_p50_ms: 160, tpu_rtt_p90_ms: 180, upload_s: 0.5, total_s: 3, cached: false,
    };
    vi.mocked(api.GET).mockResolvedValue({
      data: {
        camera: {
          id: 7, sector_id: 1, name: "Пресс №2", description: "", is_demo: false,
          has_calibration: false, zones_count: 0, videos_count: 1,
        },
        videos: [
          {
            id: 3, camera_id: 7, filename: "run.mp4", sha256: "ab", size_bytes: 10, width: 320, height: 240,
            fps: 25, frame_count: 75, duration_ms: 3000, codec: "mp4v", browser_playable: false,
            status: "ready", active_analysis_id: null, created_at: "2026-10-24T09:00:00.000Z",
          },
        ],
        jobs: [
          {
            id: 5, kind: "process", video_id: 3, camera_id: 7, backend: "linq", fake: true, status: "done",
            stage: "done", progress: 1, attempts: 1, next_attempt_at: null, error_code: null, error_text: null,
            metrics: [metrics], analysis_id: null, analysis_ms: null, created_at: "2026-10-24T09:00:00.000Z",
            started_at: null, finished_at: null,
          },
        ],
        calibration: null, zones: [], rules: [], broadcast: null,
      },
    } as never);
    render(
      <MemoryRouter initialEntries={["/admin/cameras/7"]}>
        <Routes>
          <Route path="/admin/cameras/:cameraId" element={<CameraSetup />} />
        </Routes>
      </MemoryRouter>,
    );
    expect(await screen.findByText("run.mp4")).toBeTruthy();
    expect(screen.getByText("Браузер может не воспроизвести кодек mp4v: нужен H.264")).toBeTruthy();
    expect(screen.getByText("21,5")).toBeTruthy();
    expect(screen.getByText("linq (фейк)")).toBeTruthy();
  });

  it("camera_setup_player_renders", async () => {
    vi.spyOn(HTMLCanvasElement.prototype, "getContext").mockReturnValue(null); // jsdom has no canvas
    const camera = {
      id: 7, sector_id: 1, name: "Пресс №2", description: "", is_demo: false,
      has_calibration: false, zones_count: 0, videos_count: 1,
    };
    const video = {
      id: 3, camera_id: 7, filename: "walk.mp4", sha256: "ab", size_bytes: 10, width: 320, height: 240,
      fps: 25, frame_count: 75, duration_ms: 3000, codec: "avc1", browser_playable: true,
      status: "ready", active_analysis_id: 11, created_at: "2026-10-24T09:00:00.000Z",
    };
    const frame = {
      frame_idx: 0, ts_ms: 0,
      objects: [
        {
          track_id: 1, kind: "person", label: "человек", score: 0.9, bbox: [0.1, 0.2, 0.3, 0.9], kpts: null,
          tags: [{ code: "speed", text: "бег 2,4 роста/с", level: "yellow" }],
        },
      ],
    };
    vi.mocked(api.GET).mockImplementation(((path: string) =>
      Promise.resolve(
        path === "/api/videos/{video_id}/tracks"
          ? { data: { video_id: 3, analysis_id: 11, from_ms: 0, to_ms: 5000, frames: [frame] } }
          : path === "/api/videos/{video_id}/analysis"
            ? { error: { code: "video_not_ready", message: "Анализ видео ещё не готов" } }
            : { data: { camera, videos: [video], jobs: [], calibration: null, zones: [], rules: [], broadcast: null } },
      )) as never);
    render(
      <MemoryRouter initialEntries={["/admin/cameras/7"]}>
        <Routes>
          <Route path="/admin/cameras/:cameraId" element={<CameraSetup />} />
        </Routes>
      </MemoryRouter>,
    );
    expect(await screen.findByText("Скрыть HUD")).toBeTruthy();
    expect(document.querySelector("video")?.getAttribute("src")).toBe("/api/videos/3/file");
    expect(vi.mocked(api.GET)).toHaveBeenCalledWith("/api/videos/{video_id}/tracks", {
      params: { path: { video_id: 3 }, query: { from_ms: 0, to_ms: 5000 } },
    });
    fireEvent.keyDown(window, { key: "h" });
    expect(screen.getByText("Показать HUD")).toBeTruthy();
  });

  it("camera_setup_timeline_renders", async () => {
    vi.spyOn(HTMLCanvasElement.prototype, "getContext").mockReturnValue(null); // jsdom has no canvas
    const camera = {
      id: 7, sector_id: 1, name: "Пресс №2", description: "", is_demo: false,
      has_calibration: false, zones_count: 0, videos_count: 1,
    };
    const video = {
      id: 3, camera_id: 7, filename: "demo.mp4", sha256: "ab", size_bytes: 10, width: 320, height: 240,
      fps: 10, frame_count: 200, duration_ms: 20000, codec: "avc1", browser_playable: true,
      status: "ready", active_analysis_id: 11, created_at: "2026-10-24T09:00:00.000Z",
    };
    const shot = { id: 4, kind: "confirm", frame_idx: 45, ts_ms: 4500, url: "/api/evidence/4/image", sha256: "cd", objects: [] };
    const episode = {
      id: 21, analysis_id: 11, scenario: "running", scenario_title: "Бег и резкие перемещения", subject: "track:1",
      zone_id: null, level_initial: "yellow", level_max: "yellow", start_ms: 3500, confirm_ms: 4500,
      escalate_ms: null, end_ms: 6500, end_reason: "observed_exit", reason_code: "running",
      reason_text: "Бег 2,5 роста/с", method: "relative", confidence: 0.9, metrics: {}, uncertain_ms: 0,
      evidence: [shot],
    };
    const analysis = {
      id: 11, video_id: 3, version: 1, created_at: "2026-10-24T09:00:00.000Z", duration_ms: 20000,
      pose_used: true, episodes: [episode], gaps: [],
    };
    vi.mocked(api.GET).mockImplementation(((path: string) =>
      Promise.resolve(
        path === "/api/videos/{video_id}/analysis"
          ? { data: analysis }
          : path === "/api/videos/{video_id}/tracks"
            ? { data: { video_id: 3, analysis_id: 11, from_ms: 0, to_ms: 5000, frames: [] } }
            : { data: { camera, videos: [video], jobs: [], calibration: null, zones: [], rules: [], broadcast: null } },
      )) as never);
    vi.mocked(api.POST).mockResolvedValue({ data: {} } as never);
    render(
      <MemoryRouter initialEntries={["/admin/cameras/7"]}>
        <Routes>
          <Route path="/admin/cameras/:cameraId" element={<CameraSetup />} />
        </Routes>
      </MemoryRouter>,
    );
    const item = await screen.findByText(/Бег и резкие перемещения: Бег 2,5 роста\/с/);
    expect(screen.getByText("yellow")).toBeTruthy(); // the level as text, not by color alone
    expect(document.querySelector("img")?.getAttribute("src")).toBe("/api/evidence/4/image");
    fireEvent.click(item);
    expect(document.querySelector("video")?.currentTime).toBe(3.5);
    fireEvent.click(screen.getByText("Пересчитать события"));
    expect(vi.mocked(api.POST)).toHaveBeenCalledWith("/api/videos/{video_id}/recompute", {
      params: { path: { video_id: 3 } },
    });
  });

  it("system_screen_renders", async () => {
    const status = {
      backend: "linq", fake: false, state: "ok", checked_at: "2026-10-24T09:00:00.000Z", latency_ms: 40,
      present: ["a.tpu", "b.tpu"], missing: [], message: "LinQ доступен, 2 из 2 программ",
    };
    const metrics = {
      backend: "linq", fake: false, model_id: "det-yolov8n", model_version: "640-ap9999", task: "detect",
      input_size: 640, step: 2, frames_processed: 38, wall_s: 1, throughput_fps: 21.5, preprocess_ms: 1.5,
      postprocess_ms: 2.5, tpu_rtt_p50_ms: 160, tpu_rtt_p90_ms: 180, upload_s: 0.5, total_s: 3, cached: false,
    };
    const job = {
      id: 5, kind: "process", video_id: 3, camera_id: 7, backend: "linq", fake: false, status: "done",
      stage: "done", progress: 1, attempts: 1, next_attempt_at: null, error_code: null, error_text: null,
      metrics: [metrics], analysis_id: null, analysis_ms: null, created_at: "2026-10-24T09:00:00.000Z",
      started_at: null, finished_at: null,
    };
    const failed = { ...job, id: 6, status: "failed", metrics: [], error_code: "bad_output", error_text: "summary" };
    const pct = { n: 0, pending: 0, p50: null, p95: null };
    vi.mocked(api.GET).mockResolvedValue({
      data: {
        backend: "linq", fake: false, backend_status: status, queue: [], recent_jobs: [job, failed],
        cameras: [], channels: [], server_now: "2026-10-24T09:00:00.000Z",
        latency: { notify_delay_s: pct, publish_lag_ms: pct },
        models: [
          {
            id: "det-yolov8n", version: "640-ap9999", task: "detect", input_size: 640, conf: 0.1, iou: 0.45,
            classes: { 0: "person" }, linq_program: "mosprom_det640.tpu", linq_tail: "tail.onnx", local_onnx: null,
          },
        ],
      },
    } as never);
    const down = { ...status, state: "unreachable", message: "LinQ недоступен: туннель или VPN" };
    vi.mocked(api.POST).mockResolvedValue({ data: down } as never);
    render(<SystemScreen />);
    expect(await screen.findByText(/LinQ доступен, 2 из 2 программ/)).toBeTruthy();
    expect(screen.getByText("21,5")).toBeTruthy();
    expect(screen.getByText("160 / 180")).toBeTruthy();
    expect(screen.getByText("mosprom_det640.tpu")).toBeTruthy();
    expect(screen.getByText("Повторить")).toBeTruthy();
    fireEvent.click(screen.getByText("Проверить LinQ"));
    expect(await screen.findByText(/LinQ недоступен: туннель или VPN/)).toBeTruthy();
  });
});
