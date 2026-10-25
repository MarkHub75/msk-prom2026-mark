import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../../App";
import { fixtureMeta } from "../../fixtures/data";
import { K14 } from "../../fixtures/calcV2";
import { setRole, type Role } from "../../roles";
import type { ResultV2 } from "../../api/calcV2";

// docs/CALCULATOR_CONTRACT_V2.md К14 fixtures against the screen; the backend of contract 2.0.0 is not ready yet.
class QuietSocket { onopen = null; onmessage = null; onclose = null; onerror = null; close() {} }
type Handler = (request: Request) => Response | undefined | Promise<Response | undefined>;
let requests: Request[];
function serve(handler: Handler) {
  requests = [];
  vi.stubGlobal("fetch", async (request: Request) => {
    requests.push(request.clone());
    const path = new URL(request.url).pathname;
    if (path === "/api/meta") return Response.json(fixtureMeta);
    return (await handler(request)) ?? Response.json({ code: "not_found", message: "Нет", details: {} }, { status: 404 });
  });
}
const url = (r: Request) => new URL(r.url);
const LEGACY = {
  rollout: { workshops: 2, cameras: 8, shifts_per_day: 2, workers: 200, operators: 2, incidents_per_year: 4, downtime_cost_rub: 500000, fine_cost_rub: 200000, treatment_cost_rub: 300000, lawsuit_cost_rub: 500000, overrides: {} },
  scale: { cameras_now: 8, new_cameras: 8, overrides: {} }, assumptions: [], measured: [],
};
const withV2 = { ...LEGACY, v2: K14.defaults };
const v2Posts = (mode = "rollout") => requests.filter(r => url(r).pathname === `/api/calculator/${mode}` && url(r).searchParams.get("format") === "v2");
function open(role: Role = "management") {
  act(() => setRole(role));
  return render(<MemoryRouter initialEntries={["/calculator"]}><App /></MemoryRouter>);
}

beforeEach(() => { localStorage.clear(); sessionStorage.clear(); history.replaceState({}, "", "/?review=real"); vi.stubGlobal("WebSocket", QuietSocket); });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("calculator v2 or legacy by the v2 field of defaults (К2)", () => {
  it("defaults with v2 open calculator v2 and POST ?format=v2 with the full body and the role", async () => {
    serve(r => url(r).pathname === "/api/calculator/defaults" ? Response.json(withV2) : url(r).pathname === "/api/calculator/rollout" ? Response.json(K14.rolloutResult) : undefined);
    open();
    expect(await screen.findByTestId("calculator-v2")).toBeTruthy();
    await screen.findByTestId("steps");
    const post = v2Posts()[0];
    expect(post.headers.get("X-Role")).toBe("management");
    expect(await post.clone().json()).toEqual(K14.defaults.rollout);
    expect(requests.some(r => url(r).pathname === "/api/calculator/rollout" && !url(r).searchParams.has("format"))).toBe(false);
  });

  it("defaults without v2 keep the legacy screen as it was", async () => {
    serve(r => url(r).pathname === "/api/calculator/defaults" ? Response.json(LEGACY) : url(r).pathname === "/api/calculator/rollout" ? Response.json({ incident_cost_rub: 1, incidents_per_1000_workers: null, events_per_operator_shift: null, assumptions: [], tiers: [] }) : undefined);
    open();
    expect(await screen.findByTestId("calculator")).toBeTruthy();
    expect(screen.queryByTestId("calculator-v2")).toBeNull();
    await waitFor(() => expect(requests.some(r => url(r).pathname === "/api/calculator/rollout")).toBe(true));
    expect(v2Posts()).toHaveLength(0);
  });
});

describe("steps of equipment (К6)", () => {
  it("reads «16 → 3 платы», signs the model and the vendor claim, tracker «недоступен»", async () => {
    serve(r => url(r).pathname === "/api/calculator/defaults" ? Response.json(withV2) : url(r).pathname === "/api/calculator/rollout" ? Response.json(K14.rolloutResult) : undefined);
    open();
    const steps = await screen.findByTestId("steps");
    expect(within(steps).getByLabelText("16 → 3 плат").textContent).toMatch(/16→3 платы/);
    expect(within(steps).getAllByText("модель нагрузки, не замер").length).toBeGreaterThan(0);
    expect(steps.textContent).toContain("Ёмкость платы — заявление производителя.");
    const items = within(steps).getAllByRole("listitem").filter(li => li.hasAttribute("data-step"));
    expect(items.map(li => li.getAttribute("data-step"))).toEqual(["naive", "dedicated_capacity", "scenario_models", "activity_pool", "tracker"]);
    expect(items.map(li => li.querySelector(".cv2-step-n")?.textContent)).toEqual(["16", "4", "4", "3", "—"]);
    expect(within(items[4]).getByText("недоступен")).toBeTruthy();
    expect(items[3].classList.contains("is-best")).toBe(true);
  });
});

describe("states (К5, К10 п.5)", () => {
  it("partial with missing: the reason by message, unknown money is «нужно значение», the hardware stays", async () => {
    serve(r => url(r).pathname === "/api/calculator/defaults" ? Response.json(withV2) : url(r).pathname === "/api/calculator/rollout" ? Response.json(K14.partialResult) : undefined);
    open();
    expect((await screen.findByTestId("result-status")).getAttribute("data-status")).toBe("partial");
    expect(within(screen.getByTestId("missing")).getByText(/Цена покупаемой HP неизвестна/)).toBeTruthy();
    const base = screen.getByTestId("tier-base");
    expect(within(base).getAllByText("нужно значение").length).toBeGreaterThan(0);
    expect(base.querySelector("[data-payback]")?.getAttribute("data-payback")).toBe("insufficient_data");
    expect(screen.getByTestId("hardware").textContent).toContain("3 × HP");
    expect(screen.getByTestId("hardware").textContent).toContain("техническая комплектация");
  });

  it("a 422 marks details.field and keeps the last result", async () => {
    serve(async r => {
      if (url(r).pathname === "/api/calculator/defaults") return Response.json(withV2);
      if (url(r).pathname !== "/api/calculator/rollout") return undefined;
      const body = await r.json() as { load: { activity_share: number } };
      return body.load.activity_share > 1 ? Response.json(K14.error422, { status: 422 }) : Response.json(K14.rolloutResult);
    });
    open();
    await screen.findByTestId("steps");
    const input = screen.getByLabelText("Доля времени с людьми в кадре");
    fireEvent.change(input, { target: { value: "1,2" } });
    expect(await screen.findByText(/Не больше 1/)).toBeTruthy();
    // the server is the judge too: limits from defaults may be wider than the server's rule
    serve(async r => url(r).pathname === "/api/calculator/rollout" ? Response.json(K14.error422, { status: 422 }) : url(r).pathname === "/api/calculator/defaults" ? Response.json(withV2) : undefined);
    fireEvent.change(input, { target: { value: "0,7" } });
    await waitFor(() => expect(input.getAttribute("aria-invalid")).toBe("true"));
    expect(screen.getByTestId("field-error").textContent).toContain("Неверное значение: load.activity_share");
    expect(screen.getByTestId("steps")).toBeTruthy();
  });

  it("a late answer of an older request does not replace the newer one", async () => {
    let releaseFirst!: () => void;
    const first = new Promise<void>(done => { releaseFirst = done; });
    const newer: ResultV2 = { ...K14.rolloutResult, steps: K14.rolloutResult.steps.map(s => s.id === "naive" ? { ...s, chips: 20 } : s) };
    let n = 0;
    serve(async r => {
      if (url(r).pathname === "/api/calculator/defaults") return Response.json(withV2);
      if (url(r).pathname !== "/api/calculator/rollout") return undefined;
      n += 1;
      if (n === 1) { await first; return Response.json(K14.rolloutResult); }
      return Response.json(newer);
    });
    open();
    await waitFor(() => expect(n).toBe(1));
    fireEvent.change(screen.getByLabelText("Работников"), { target: { value: "250" } });
    const steps = await screen.findByTestId("steps");
    await waitFor(() => expect(within(steps).getByLabelText("20 → 3 плат")).toBeTruthy());
    releaseFirst();
    await new Promise(done => setTimeout(done, 50));
    expect(within(screen.getByTestId("steps")).queryByLabelText("16 → 3 плат")).toBeNull();
    expect(within(screen.getByTestId("steps")).getByLabelText("20 → 3 плат")).toBeTruthy();
  });

  it("while recounting the previous result stays with a mark", async () => {
    let release!: () => void;
    const hold = new Promise<void>(done => { release = done; });
    let n = 0;
    serve(async r => {
      if (url(r).pathname === "/api/calculator/defaults") return Response.json(withV2);
      if (url(r).pathname !== "/api/calculator/rollout") return undefined;
      n += 1;
      if (n > 1) await hold;
      return Response.json(K14.rolloutResult);
    });
    open();
    await screen.findByTestId("steps");
    fireEvent.change(screen.getByLabelText("Работников"), { target: { value: "300" } });
    expect(await screen.findByText("пересчитываем — показан прошлый результат")).toBeTruthy();
    expect(screen.getByTestId("steps")).toBeTruthy();
    release();
    await waitFor(() => expect(screen.queryByText("пересчитываем — показан прошлый результат")).toBeNull());
  });

  it("empty: no project, no purchase", async () => {
    const empty: ResultV2 = { ...K14.rolloutResult, status: "empty" };
    serve(r => url(r).pathname === "/api/calculator/defaults" ? Response.json(withV2) : url(r).pathname === "/api/calculator/rollout" ? Response.json(empty) : undefined);
    open();
    expect((await screen.findByTestId("result-status")).textContent).toContain("Нет проекта");
  });

  it("admin gets scale only; no PDF while features.pdf_available=false", async () => {
    serve(r => url(r).pathname === "/api/calculator/defaults" ? Response.json(withV2) : url(r).pathname === "/api/calculator/scale" ? Response.json(K14.scaleResult) : undefined);
    open("admin");
    await screen.findByTestId("steps");
    expect(v2Posts("scale")).toHaveLength(1);
    expect(v2Posts("rollout")).toHaveLength(0);
    expect(screen.queryByTestId("calc-pdf")).toBeNull();
    expect(screen.getByTestId("hardware").textContent).toContain("Было");
  });
});
