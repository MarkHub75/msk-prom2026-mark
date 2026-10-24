import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { Schemas } from "../api/types";
import { RulesPage } from "./Rules";

type Rule = Schemas["CameraRule"];
const scenario = (id: string, title: string, status: Schemas["ScenarioMeta"]["status"], level: "yellow" | "red" = "yellow"): Schemas["ScenarioMeta"] => ({
  id, title, description: `Описание ${title}`, icon: id === "running" ? "run" : "fire", default_level: level, status,
  status_text: status === "active" ? "Сценарий работает" : "Нет модели с классами: fire", required_classes: ["person"], zone_kinds: [],
  params: [{ key: "hold_s", title: "Удержание жёлтого", unit: "с", default: 1, min: 0, max: 60 }],
});
const camera = (id: number, sector_id: number): Schemas["Camera"] => ({ id, sector_id, name: `Камера ${id}`, description: "", is_demo: false, has_calibration: false, zones_count: 0, videos_count: 0 });
const rule = (camera_id: number, sc: string, enabled: boolean, status: Rule["status"] = "active", params: Record<string, number> = {}): Rule => ({ camera_id, scenario: sc, enabled, params, effective: {}, status });

let puts: { path: string; body: { enabled: boolean; params: Record<string, number> } }[];
function serve(view?: Schemas["RulesScreenView"], fail = false) {
  puts = [];
  vi.stubGlobal("fetch", vi.fn(async (request: Request) => {
    const path = new URL(request.url).pathname;
    if (request.method === "PUT") {
      const body = await request.json() as { enabled: boolean; params: Record<string, number> };
      puts.push({ path, body });
      const [, , , cam, , sc] = path.split("/");
      return Response.json(rule(Number(cam), sc, body.enabled, "active", body.params));
    }
    if (path === "/api/sectors") return Response.json([{ id: 2, name: "Склад", sort_order: 2, is_demo: false }, { id: 1, name: "Прессы", sort_order: 1, is_demo: false }]);
    if (fail) return Response.json({ code: "internal", message: "База недоступна", details: {} }, { status: 500 });
    return Response.json(view);
  }));
}
const VIEW: Schemas["RulesScreenView"] = {
  scenarios: [scenario("running", "Бег", "active"), scenario("fire_smoking", "Курение", "model_missing", "red")],
  rows: [
    { camera: camera(3, 2), rules: [rule(3, "running", false), rule(3, "fire_smoking", false, "model_missing")] },
    { camera: camera(1, 1), rules: [rule(1, "running", true, "active", { hold_s: 2 }), rule(1, "fire_smoking", false, "model_missing")] },
  ],
};
const show = () => render(<MemoryRouter initialEntries={["/ohs/rules"]}><RulesPage /></MemoryRouter>);

beforeEach(() => { localStorage.clear(); sessionStorage.clear(); history.replaceState({}, "", "/?review=real"); });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("rules matrix", () => {
  it("groups cameras by sector order and shows the scenario status from the API", async () => {
    serve(VIEW);
    show();
    await screen.findByTestId("rules-view");
    const sectors = screen.getAllByRole("rowheader").filter(h => h.closest(".ops-sector-row")).map(h => h.textContent);
    expect(sectors[0]).toContain("Прессы");
    expect(sectors[1]).toContain("Склад");
    expect(screen.getAllByText("Модель не подключена").length).toBeGreaterThan(0);
    // No switch for a scenario without a model: only active scenarios can be toggled.
    expect(screen.getAllByRole("switch")).toHaveLength(2);
    expect(screen.getByRole("link", { name: "Параметры камеры «Камера 1»" }).getAttribute("href")).toBe("/admin/cameras/1?tab=rules");
  });

  it("toggles one cell with PUT and keeps the camera's own params", async () => {
    serve(VIEW);
    show();
    const cell = await screen.findByRole("switch", { name: "Бег на камере Камера 1" });
    expect(cell.getAttribute("aria-checked")).toBe("true");
    fireEvent.click(cell);
    await waitFor(() => expect(screen.getByRole("switch", { name: "Бег на камере Камера 1" }).getAttribute("aria-checked")).toBe("false"));
    expect(puts).toEqual([{ path: "/api/cameras/1/rules/running", body: { enabled: false, params: { hold_s: 2 } } }]);
  });

  it("switches a whole column on, skips cells already on, and can undo", async () => {
    serve(VIEW);
    show();
    fireEvent.click(await screen.findByRole("button", { name: "Включить «Бег» на всех камерах" }));
    await screen.findByText("«Бег» включён: 1 правило");
    expect(puts.map(p => p.path)).toEqual(["/api/cameras/3/rules/running"]);
    fireEvent.click(screen.getByRole("button", { name: "Отменить" }));
    await waitFor(() => expect(puts).toHaveLength(2));
    expect(puts[1]).toEqual({ path: "/api/cameras/3/rules/running", body: { enabled: false, params: {} } });
  });

  it("shows the API error and an honest empty state", async () => {
    serve(undefined, true);
    show();
    expect((await screen.findByRole("alert")).textContent).toContain("База недоступна");
    cleanup();
    serve({ scenarios: VIEW.scenarios, rows: [] });
    show();
    expect(within(await screen.findByTestId("rules-view")).getByText("Камер нет")).toBeTruthy();
  });
});
