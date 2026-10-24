import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { setRole } from "../../roles";
import { CalibrationTab } from "./CalibrationTab";
import { CameraRulesTab } from "./CameraRulesTab";
import { ZonesTab } from "./ZonesTab";

const meta = {
  product_name: "", contract: "1", fake: true, inference_backend: "linq", timezone: "Europe/Moscow", roles: [], statuses: [],
  levels: [{ id: "yellow", title: "Жёлтая опасность", color: "#FFC400", sound: "chime" }, { id: "red", title: "Красная опасность", color: "#FF3B30", sound: "siren" }],
  zone_kinds: [
    { id: "danger", title: "Опасная зона / механизм", color: "#FF453A", geometry: "polygon", description: "Станок" },
    { id: "fence", title: "Ограждение", color: "#FF9F0A", geometry: "line", description: "Линия" },
  ],
  scenarios: [
    { id: "running", title: "Бег и резкие перемещения", icon: "run", description: "Человек бежит", default_level: "yellow", status: "active", status_text: "Сценарий работает",
      required_classes: ["person"], zone_kinds: ["danger"], params: [{ key: "hold_s", title: "Удержание жёлтого", unit: "с", min: 0, max: 60, default: 1 }] },
    { id: "fire_smoking", title: "Курение и открытый огонь", icon: "fire", description: "Огонь", default_level: "red", status: "model_missing", status_text: "Нет модели с классами: fire",
      required_classes: ["fire"], zone_kinds: [], params: [] },
  ],
};
const zones = [
  { id: 1, camera_id: 1, kind: "danger", name: "Пресс", points: [[0.5, 0.3], [0.9, 0.3], [0.9, 0.8], [0.5, 0.8]] },
  { id: 2, camera_id: 1, kind: "fence", name: "Забор", points: [[0.1, 0.2], [0.1, 0.9]] },
];
const calibration = {
  camera_id: 1, image_points: [[0.1, 0.5], [0.9, 0.5], [0.95, 0.95], [0.05, 0.95]], world_points: [[0, 0], [6, 0], [6, 4], [0, 4]],
  control_points: [], fit_rmse_m: 0.012, control_rmse_m: null, grid: [[[0.1, 0.5], [0.05, 0.95]]], updated_at: "2026-10-24T09:00:00Z",
};
const rules = [
  { camera_id: 1, scenario: "running", enabled: true, params: {}, effective: { hold_s: 1 }, status: "active" },
  { camera_id: 1, scenario: "fire_smoking", enabled: false, params: {}, effective: {}, status: "model_missing" },
];

let calls: { method: string; path: string; body?: unknown }[] = [];
function backend(overrides: Record<string, (body: unknown) => Response> = {}) {
  calls = [];
  vi.stubGlobal("fetch", vi.fn(async (request: Request) => {
    const path = new URL(request.url).pathname;
    const body = request.method === "GET" ? undefined : await request.json().catch(() => undefined);
    calls.push({ method: request.method, path, body });
    const key = `${request.method} ${path}`;
    if (overrides[key]) return overrides[key](body);
    if (key === "GET /api/meta") return Response.json(meta);
    if (key === "GET /api/cameras/1/zones") return Response.json(zones);
    if (key === "GET /api/cameras/1/calibration") return Response.json(calibration);
    if (key === "GET /api/cameras/1/rules") return Response.json(rules);
    if (key === "GET /api/cameras/1/videos") return Response.json([]);
    return Response.json({ code: "not_found", message: "Нет", details: {} }, { status: 404 });
  }));
}

// jsdom has no PointerEvent: a MouseEvent carries clientX/Y and button for the editor.
if (!("PointerEvent" in window)) Object.assign(window, { PointerEvent: class extends MouseEvent { pointerId = 1; } });

beforeEach(() => { sessionStorage.clear(); window.history.replaceState({}, "", "/?review=real"); act(() => setRole("admin")); });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("ZonesTab", () => {
  it("lists zones, draws them on the frame and renames the selected one", async () => {
    backend({ "PATCH /api/zones/1": (body) => Response.json({ ...zones[0], ...(body as object) }) });
    render(<ZonesTab cameraId={1} />);
    expect(await screen.findByText("2 зоны")).toBeTruthy();
    expect(document.querySelectorAll(".geo-zone")).toHaveLength(2);
    fireEvent.click(screen.getByRole("button", { name: /Пресс/ }));
    expect(screen.getAllByTestId("vertex")).toHaveLength(4);
    fireEvent.change(screen.getByDisplayValue("Пресс"), { target: { value: "Пресс №2" } });
    fireEvent.click(screen.getByRole("button", { name: /Сохранить/ }));
    await waitFor(() => expect(calls.some((c) => c.method === "PATCH")).toBe(true));
    expect(calls.find((c) => c.method === "PATCH")).toEqual({ method: "PATCH", path: "/api/zones/1", body: { name: "Пресс №2" } });
    expect(await screen.findByTestId("recompute-notice")).toBeTruthy();
  });

  it("draws a new polygon with clicks, closes it with Enter and shows a 422 at its field", async () => {
    backend({ "POST /api/cameras/1/zones": () => Response.json({ code: "validation", message: "Название зоны: от 1 до 60 символов", details: { field: "name" } }, { status: 422 }) });
    render(<ZonesTab cameraId={1} />);
    await screen.findByText("2 зоны");
    fireEvent.click(screen.getByRole("button", { name: /Новая зона/ }));
    const svg = screen.getByTestId("geometry-editor");
    svg.getBoundingClientRect = () => ({ left: 0, top: 0, width: 1000, height: 500, right: 1000, bottom: 500, x: 0, y: 0, toJSON: () => ({}) });
    for (const [x, y] of [[100, 100], [400, 100], [400, 400]]) fireEvent.pointerDown(svg, { clientX: x, clientY: y, button: 0 });
    expect(screen.getAllByTestId("vertex")).toHaveLength(3);
    fireEvent.keyDown(window, { key: "Enter" });
    expect(screen.getByText("Полигон, замкнут")).toBeTruthy();
    fireEvent.change(screen.getByPlaceholderText(/Пресс №2/), { target: { value: " " } });
    fireEvent.change(screen.getByPlaceholderText(/Пресс №2/), { target: { value: "x" } });
    fireEvent.click(screen.getByRole("button", { name: /Добавить зону/ }));
    expect((await screen.findByRole("alert")).textContent).toContain("Название зоны");
    expect(calls.find((c) => c.method === "POST")?.body).toEqual({ kind: "danger", name: "x", points: [[0.1, 0.2], [0.4, 0.2], [0.4, 0.8]] });
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.queryByText("Новая зона", { selector: "b" })).toBeNull();
  });
});

describe("GeometryEditor in ZonesTab", () => {
  it("inserts a vertex on an edge midpoint, drags it and deletes a vertex with Delete", async () => {
    backend();
    render(<ZonesTab cameraId={1} />);
    await screen.findByText("2 зоны");
    fireEvent.click(screen.getByRole("button", { name: /Пресс/ }));
    const svg = screen.getByTestId("geometry-editor");
    svg.getBoundingClientRect = () => ({ left: 0, top: 0, width: 1000, height: 500, right: 1000, bottom: 500, x: 0, y: 0, toJSON: () => ({}) });
    // Midpoint of the top edge (0.5,0.3)–(0.9,0.3) is (700, 150) px.
    fireEvent.pointerDown(svg, { clientX: 700, clientY: 150, button: 0 });
    fireEvent.pointerMove(svg, { clientX: 700, clientY: 100 });
    fireEvent.pointerUp(svg, { clientX: 700, clientY: 100 });
    expect(screen.getAllByTestId("vertex")).toHaveLength(5);
    expect(screen.getByText("не сохранено")).toBeTruthy();
    fireEvent.keyDown(window, { key: "Delete" });
    expect(screen.getAllByTestId("vertex")).toHaveLength(4);
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.queryByText("не сохранено")).toBeNull();
  });
});

describe("CalibrationTab", () => {
  it("shows the saved points, grid and accuracy; ohs sees it read-only", async () => {
    backend();
    act(() => setRole("ohs"));
    render(<CalibrationTab cameraId={1} />);
    expect(await screen.findByText("нет контрольных точек: точность не проверена")).toBeTruthy();
    expect(screen.getByTestId("calibration-grid")).toBeTruthy();
    expect((screen.getByLabelText("X, м точки 2") as HTMLInputElement).value).toBe("6");
    expect(screen.getByText("Калибровку меняет администратор")).toBeTruthy();
    expect(screen.queryByRole("button", { name: /Сохранить/ })).toBeNull();
  });

  it("saves edited meters with PUT", async () => {
    backend({ "PUT /api/cameras/1/calibration": (body) => Response.json({ ...calibration, ...(body as object) }) });
    render(<CalibrationTab cameraId={1} />);
    const x = await screen.findByLabelText("X, м точки 2");
    fireEvent.change(x, { target: { value: "6,5" } });
    expect(screen.getByText(/Оценка в браузере/)).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /Сохранить/ }));
    await waitFor(() => expect(calls.some((c) => c.method === "PUT")).toBe(true));
    expect((calls.find((c) => c.method === "PUT")?.body as { world_points: number[][] }).world_points[1]).toEqual([6.5, 0]);
  });
});

describe("CameraRulesTab", () => {
  it("shows statuses from meta, blocks out-of-range values and saves overrides", async () => {
    backend({ "PUT /api/cameras/1/rules/running": (body) => Response.json({ ...rules[0], ...(body as object) }) });
    render(<CameraRulesTab cameraId={1} />);
    expect(await screen.findByText("Нет модели с классами: fire")).toBeTruthy();
    expect(document.querySelector(".geo-rules-head")?.textContent).toContain("1 из 2 сценариев работают");
    const input = screen.getByLabelText("Бег и резкие перемещения: Удержание жёлтого");
    fireEvent.change(input, { target: { value: "99" } });
    expect(screen.getByText("От 0 до 60")).toBeTruthy();
    expect((screen.getByRole("button", { name: /Сохранить/ }) as HTMLButtonElement).disabled).toBe(true);
    fireEvent.change(input, { target: { value: "2,5" } });
    fireEvent.click(screen.getByRole("button", { name: /Сохранить/ }));
    await waitFor(() => expect(calls.some((c) => c.method === "PUT")).toBe(true));
    expect(calls.find((c) => c.method === "PUT")).toEqual({ method: "PUT", path: "/api/cameras/1/rules/running", body: { enabled: true, params: { hold_s: 2.5 } } });
  });
});
