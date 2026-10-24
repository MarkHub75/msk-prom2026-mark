import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "../App";
import { History } from "./Incident";
import { setActor } from "../api/client";
import { fileName } from "../api/download";
import { createFixtureEvents, fixtureMeta } from "../fixtures/data";
import { setRole, type Role } from "../roles";
import type { CalculatorDefaults, CameraPassport, DatasetView, EventDetail, PeopleStats, RolloutResult, ScaleResult, TierResult } from "../api/types";

class QuietSocket { onopen = null; onmessage = null; onclose = null; onerror = null; close() {} }
type Handler = (request: Request) => Response | undefined | Promise<Response | undefined>;
let requests: Request[];
function serve(handler: Handler) {
  requests = [];
  vi.stubGlobal("fetch", async (request: Request) => {
    requests.push(request.clone());
    const path = new URL(request.url).pathname;
    if (path === "/api/meta") return Response.json(fixtureMeta);
    const answer = await handler(request);
    return answer ?? Response.json({ code: "not_found", message: "Нет", details: {} }, { status: 404 });
  });
}
const notImplemented = (slice: number) => Response.json({ code: "not_implemented", message: `Функция появится в слайсе ${slice}`, details: { slice: String(slice) } }, { status: 501 });
function open(path: string, role: Role) {
  act(() => setRole(role));
  return render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>);
}
const path = (r: Request) => new URL(r.url).pathname;

beforeEach(() => {
  localStorage.clear(); sessionStorage.clear();
  history.replaceState({}, "", "/?review=real");
  vi.stubGlobal("WebSocket", QuietSocket);
});
afterEach(() => { cleanup(); vi.restoreAllMocks(); vi.unstubAllGlobals(); });

const assumption = (key: string, title: string, value: number, unit: string) => ({ key, title, value, unit, source: "допущение команды", editable: true });
const DEFAULTS: CalculatorDefaults = {
  rollout: { workshops: 2, cameras: 8, shifts_per_day: 2, workers: 200, operators: 2, incidents_per_year: 4, downtime_cost_rub: 500000, fine_cost_rub: 200000, treatment_cost_rub: 300000, lawsuit_cost_rub: 500000, overrides: {} },
  scale: { cameras_now: 8, new_cameras: 8, overrides: {} },
  assumptions: [assumption("accelerator.price_rub", "Цена ускорителя LinQ", 500000, "₽"), assumption("reduction.base", "Снижение инцидентов: базовый уровень", 0.2, "доля")],
  measured: [{ key: "throughput", title: "Пропускная способность", value: 12.4, unit: "кадр/с", source: "замер приложения: 3 задачи", editable: false }],
};
const tier = (t: TierResult["tier"], payback: number | null): TierResult => ({ tier: t, title: { base: "Базовый", extended: "Расширенный", max: "Максимальный" }[t], capex_rub: 1_150_000, opex_rub_year: 172_500, savings_rub_year: 1_200_000, payback_months: payback, accelerators: 2, servers: 1, items: [{ label: "Ускорители LinQ", value: "2 × 500 000 ₽" }] });
const ROLLOUT: RolloutResult = { incident_cost_rub: 1_500_000, incidents_per_1000_workers: 20, events_per_operator_shift: 3.5, assumptions: DEFAULTS.assumptions, tiers: [tier("base", 13.4), tier("extended", 9), tier("max", null)] };
const SCALE: ScaleResult = { cameras_total: 16, accelerators_now: 2, accelerators_total: 3, servers_total: 1, capex_rub: 980_000, capacity_fps: 12.4, capacity_source: "замер приложения: 3 задачи", analysis_fps: 5, assumptions: DEFAULTS.assumptions, items: [] };

describe("calculator (tech.md 8.25)", () => {
  function calcServer() {
    serve(r => {
      if (path(r) === "/api/calculator/defaults") return Response.json(DEFAULTS);
      if (path(r) === "/api/calculator/rollout") return Response.json(ROLLOUT);
      if (path(r) === "/api/calculator/scale") return Response.json(SCALE);
    });
  }

  it("posts the plant and overrides, shows tiers and the honest «не окупается»", async () => {
    calcServer();
    open("/calculator", "management");
    expect(await screen.findByTestId("tier-base")).toBeTruthy();
    expect(within(screen.getByTestId("tier-max")).getByText("Не окупается при этих допущениях")).toBeTruthy();
    expect(within(screen.getByTestId("tier-extended")).getByText("быстрее окупается")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("Цена ускорителя LinQ"), { target: { value: "600000" } });
    await waitFor(async () => {
      const last = requests.filter(r => path(r) === "/api/calculator/rollout").at(-1)!;
      expect(await last.clone().json()).toMatchObject({ cameras: 8, workshops: 2, overrides: { "accelerator.price_rub": 600000 } });
    });
    expect(screen.getByText("своё значение", { selector: ".ds-badge" })).toBeTruthy();
    const breakEven = screen.getByTestId("break-even");
    expect(breakEven.textContent).toContain("расчёт от ваших допущений");
    expect(within(breakEven).getAllByRole("row")).toHaveLength(4);
    expect(screen.getByText(/1,17 на 1000 работников \(Росстат, 2025\): для 200 человек ≈ 0,23/)).toBeTruthy();
    const market = screen.getByTestId("market");
    expect(market.textContent).toContain("чужие цены, не цена Argus");
    expect(market.textContent).toContain("КоАП РФ, ред. 2026");
    expect(market.textContent).toContain("от 480 000 ₽");
  });

  it("a 422 with details.field marks that assumption and keeps the last result (live backend, slice 24)", async () => {
    serve(async r => {
      if (path(r) === "/api/calculator/defaults") return Response.json(DEFAULTS);
      if (path(r) === "/api/calculator/rollout") {
        const body = await r.json() as { overrides: Record<string, number> };
        if (body.overrides["accelerator.price_rub"] === 0) return Response.json({ code: "validation", message: "Неверное значение: overrides.accelerator.price_rub", details: { field: "overrides.accelerator.price_rub" } }, { status: 422 });
        return Response.json({ ...ROLLOUT, tiers: ROLLOUT.tiers.map(t => ({ ...t, items: [...t.items, { label: "Окупаемость", value: "13,4 мес." }] })) });
      }
    });
    open("/calculator", "management");
    await screen.findByTestId("tier-base");
    expect(within(screen.getByTestId("tier-base")).queryByText("Окупаемость", { selector: "dt" })).toBeNull();
    fireEvent.change(screen.getByLabelText("Цена ускорителя LinQ"), { target: { value: "0" } });
    expect(await screen.findByText("Сервер не принял это значение")).toBeTruthy();
    expect(screen.queryByText(/overrides.accelerator/)).toBeNull();
    expect(screen.getByTestId("tier-base")).toBeTruthy();
  });

  it("does not post an invalid field and says what to fix", async () => {
    calcServer();
    open("/calculator", "management");
    await screen.findByTestId("tier-base");
    const before = requests.filter(r => path(r) === "/api/calculator/rollout").length;
    fireEvent.change(screen.getByLabelText("Камер"), { target: { value: "0" } });
    expect(await screen.findByText("Не меньше 1")).toBeTruthy();
    await new Promise(done => setTimeout(done, 400));
    expect(requests.filter(r => path(r) === "/api/calculator/rollout").length).toBe(before);
  });

  it("scale accepts 0 current cameras: a new rollout (tech.md v7)", async () => {
    calcServer();
    open("/calculator", "admin");
    await screen.findByText("замер приложения: 3 задачи", { selector: "small" });
    fireEvent.change(screen.getByLabelText("Камер подключено сейчас"), { target: { value: "0" } });
    await waitFor(async () => {
      const last = requests.filter(r => path(r) === "/api/calculator/scale").at(-1)!;
      expect(await last.clone().json()).toMatchObject({ cameras_now: 0, new_cameras: 8 });
    });
  });

  it("admin gets the scale mode only", async () => {
    calcServer();
    open("/calculator", "admin");
    expect(await screen.findByText("замер приложения: 3 задачи", { selector: "small" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Внедрение" })).toBeNull();
    expect(requests.some(r => path(r) === "/api/calculator/rollout")).toBe(false);
  });

  it("501: a neutral notice and a labelled example on the tech.md 8.25 assumptions", async () => {
    serve(r => path(r).startsWith("/api/calculator") ? notImplemented(24) : undefined);
    open("/calculator", "management");
    const pending = await screen.findByTestId("pending");
    expect(pending.textContent).toContain("Функция появится в следующем обновлении сервера");
    expect(screen.getByTestId("calculator").textContent).not.toMatch(/слайс/);
    expect(screen.queryByRole("alert")).toBeNull();
    const example = screen.getByTestId("calc-example");
    expect(within(example).getByText("пример, сервер ещё не подключён")).toBeTruthy();
    expect(within(screen.getByTestId("tier-base")).getByText("Не окупается при этих допущениях")).toBeTruthy();
    expect(screen.getByTestId("tier-max").textContent).toMatch(/10\s040\s000 ₽/);
    fireEvent.click(screen.getByRole("button", { name: "Масштабирование" }));
    expect(await screen.findByText("докупить 15")).toBeTruthy();
  });

  it("a real failure stays red", async () => {
    serve(r => path(r) === "/api/calculator/defaults" ? Response.json({ code: "internal", message: "База недоступна", details: {} }, { status: 500 }) : undefined);
    open("/calculator", "management");
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("База недоступна");
    expect(alert.textContent).toContain("500");
    expect(screen.queryByTestId("pending")).toBeNull();
  });
});

describe("false alarm dataset (tech.md 8.26)", () => {
  const VIEW: DatasetView = { total: 2, frames: 48, items: [
    { event_id: 41, scenario: "running", frames: 24, label: "false_alarm", path: "datasets/false_alarms/41", created_at: "2026-10-24T09:00:00Z" },
    { event_id: 42, scenario: "running", frames: 24, label: "false_alarm", path: "datasets/false_alarms/42", created_at: "2026-10-24T10:00:00Z" },
  ] };

  it("lists items; the ZIP is a plain download of the export route (streamed by the browser, checked on slice 25)", async () => {
    serve(r => path(r) === "/api/datasets/false-alarms" ? Response.json(VIEW) : undefined);
    open("/ohs/dataset", "ohs");
    const table = await screen.findByTestId("dataset-items");
    expect(within(table).getAllByRole("row")).toHaveLength(3);
    expect(within(table).getByRole("link", { name: "#41" }).getAttribute("href")).toBe("/events/41");
    const zip = screen.getByTestId("export-zip");
    expect(zip.tagName).toBe("A");
    expect(new URL(zip.getAttribute("href")!).pathname).toBe("/api/datasets/false-alarms/export.zip");
    expect(zip.hasAttribute("download")).toBe(true);
  });

  it("an empty dataset has no download; a 501 list is a pending notice without actions", async () => {
    serve(r => path(r) === "/api/datasets/false-alarms" ? Response.json({ total: 0, frames: 0, items: [] }) : undefined);
    const first = open("/ohs/dataset", "ohs");
    expect(await screen.findByText("Ложных срабатываний пока нет")).toBeTruthy();
    expect((screen.getByTestId("export-zip") as HTMLButtonElement).disabled).toBe(true);
    first.unmount();
    serve(r => path(r) === "/api/datasets/false-alarms" ? notImplemented(25) : undefined);
    open("/ohs/dataset", "ohs");
    expect((await screen.findByTestId("pending")).textContent).toContain("датасет для дообучения");
    expect(screen.queryByTestId("export-zip")).toBeNull();
  });

  it("re-reads the list every 10 s: the worker adds items without a WS message", async () => {
    vi.useFakeTimers({ toFake: ["setInterval", "clearInterval"] });
    try {
      serve(r => path(r) === "/api/datasets/false-alarms" ? Response.json(VIEW) : undefined);
      open("/ohs/dataset", "ohs");
      await screen.findByTestId("dataset-items");
      const reads = () => requests.filter(r => path(r) === "/api/datasets/false-alarms").length;
      const before = reads();
      act(() => { vi.advanceTimersByTime(10_000); });
      await waitFor(() => expect(reads()).toBe(before + 1));
    } finally { vi.useRealTimers(); }
  });

});

describe("people stats (tech.md 8.27)", () => {
  it("counts identified events by person and crew as the server gives them", async () => {
    const stats: PeopleStats = { date_from: "2026-09-25", date_to: "2026-10-24", include_demo: true, total: 40, identified: 10,
      by_person: [{ key: "Петров П. П.", title: "Петров П. П.", count: 6, confirmed: 5, false_alarm: 1 }],
      by_crew: [{ key: "Бригада 3", title: "Бригада 3", count: 8, confirmed: 6, false_alarm: 0 }, { key: "Бригада 1", title: "Бригада 1", count: 2, confirmed: 2, false_alarm: 0 }] };
    serve(r => path(r) === "/api/stats/people" ? Response.json(stats) : undefined);
    open("/ohs/people", "ohs");
    expect(await screen.findByTestId("people-view")).toBeTruthy();
    expect(screen.getByTestId("tile-identified").textContent).toContain("10");
    expect(screen.getByTestId("tile-identified").textContent).toContain("25%");
    expect(within(screen.getByTestId("by-person")).getByText("Петров П. П.")).toBeTruthy();
    expect(within(screen.getByTestId("by-crew")).getByText("Бригада 1")).toBeTruthy();
    const query = new URL(requests.find(r => path(r) === "/api/stats/people")!.url).searchParams;
    expect(query.get("include_demo")).toBe("true");
  });
});

describe("camera passport (tech.md 8.28)", () => {
  it("shows the verdict and reason of every scenario, worst first", async () => {
    const passport: CameraPassport = { camera_id: 1, analysis_id: 7, frames: 900, person_height_px_p50: 64, small_object_px_p50: 9, person_frames_share: 0.8, dark_share: 0.05, empty_share: 0.1, shift_text: "",
      scenarios: [
        { scenario: "running", title: "Бег", verdict: "suitable", reason: "Годна" },
        { scenario: "phone", title: "Телефон при работе", verdict: "partial", reason: "Телефон виден плохо: 9 px" },
        { scenario: "no_helmet", title: "Без каски", verdict: "unknown", reason: "Модель не подключена" },
      ] };
    serve(r => {
      if (path(r) === "/api/admin/cameras/1") return Response.json({ camera: { id: 1, sector_id: 1, name: "Пресс №2", description: "", is_demo: false }, videos: [], jobs: [], calibration: null, zones: [], rules: [], broadcast: null });
      if (path(r) === "/api/cameras/1/passport") return Response.json(passport);
    });
    open("/admin/cameras/1?tab=passport", "admin");
    const box = await screen.findByTestId("passport");
    const rows = within(box).getAllByRole("row").slice(1);
    expect(rows.map(r => r.getAttribute("data-verdict"))).toEqual(["partial", "unknown", "suitable"]);
    expect(within(box).getByText("Телефон виден плохо: 9 px")).toBeTruthy();
    expect(within(box).getByText("64 px")).toBeTruthy();
    expect(within(box).getByText("анализ #7")).toBeTruthy();
  });
});

describe("camera passport on live answers (slice 27)", () => {
  const setup = { camera: { id: 1, sector_id: 1, name: "Пресс №2", description: "", is_demo: false }, videos: [], jobs: [], calibration: null, zones: [], rules: [], broadcast: null };
  const empty = { camera_id: 1, analysis_id: null, frames: 0, person_height_px_p50: null, small_object_px_p50: null, person_frames_share: null, dark_share: null, empty_share: null, shift_px: null, shift_text: "" };
  it("no ready video: one empty state with a way to the Video tab, not 12 identical rows", async () => {
    serve(r => path(r) === "/api/admin/cameras/1" ? Response.json(setup) : path(r) === "/api/cameras/1/passport" ? Response.json({ ...empty, scenarios: ["running", "phone"].map(id => ({ scenario: id, title: id, verdict: "unknown", reason: "Нет обработанного видео" })) }) : undefined);
    open("/admin/cameras/1?tab=passport", "admin");
    const box = await screen.findByTestId("passport");
    expect(within(box).getByText("Нет обработанной записи")).toBeTruthy();
    expect(within(box).queryByRole("table")).toBeNull();
    expect(within(box).getByRole("link", { name: /Видео/ }).getAttribute("href")).toBe("/admin/cameras/1?tab=video");
  });
  it("«Нет зон: …» leads to the Zones tab; a missing phone size says why", async () => {
    serve(r => path(r) === "/api/admin/cameras/1" ? Response.json(setup) : path(r) === "/api/cameras/1/passport" ? Response.json({ ...empty, analysis_id: 1, frames: 241, person_height_px_p50: 148.5, person_frames_share: 1, dark_share: 0, empty_share: 0, scenarios: [{ scenario: "fence_crossing", title: "Перелезание через ограждение", verdict: "partial", reason: "Нет зон: Ограждение" }, { scenario: "running", title: "Бег", verdict: "suitable", reason: "Годна" }] }) : undefined);
    open("/admin/cameras/1?tab=passport", "admin");
    const box = await screen.findByTestId("passport");
    expect(within(box).getByRole("link", { name: /Добавить зоны/ }).getAttribute("href")).toBe("/admin/cameras/1?tab=zones");
    expect(within(box).getByText("телефонов в записи не было")).toBeTruthy();
  });
});

describe("manual identification (tech.md 8.27)", () => {
  function eventServer(canIdentify: boolean) {
    let detail: EventDetail = { ...createFixtureEvents()[0], video_id: null, broadcast: null, allowed_actions: [], can_identify: canIdentify };
    serve(async r => {
      if (path(r) === "/api/events/41/identity" && r.method === "PATCH") {
        const body = await r.json() as { person_name: string; person_position: string; crew: string };
        detail = { ...detail, event: { ...detail.event, ...body } };
        return Response.json(detail);
      }
      if (path(r) === "/api/events/41") return Response.json(detail);
    });
  }

  it("OHS types who it was; the PATCH carries the actor and the card shows the answer", async () => {
    eventServer(true);
    setActor("Сидорова А. В.");
    open("/events/41", "ohs");
    const form = await screen.findByTestId("identity");
    fireEvent.change(within(form).getByLabelText("ФИО"), { target: { value: "  Петров Пётр  " } });
    fireEvent.change(within(form).getByLabelText("Бригада"), { target: { value: "Бригада 3" } });
    fireEvent.click(within(form).getByRole("button", { name: /Сохранить/ }));
    expect(await screen.findByTestId("identity-text")).toBeTruthy();
    expect(screen.getByTestId("identity-text").textContent).toBe("Петров Пётр · Бригада 3");
    const patch = requests.find(r => r.method === "PATCH")!;
    expect(await patch.json()).toEqual({ person_name: "Петров Пётр", person_position: "", crew: "Бригада 3" });
    expect(decodeURIComponent(patch.headers.get("X-Actor") ?? "")).toBe("Сидорова А. В.");
    expect(patch.headers.get("X-Role")).toBe("ohs");
  });

  it("history: «Указан нарушитель» keeps the status, so no «→ status» arrow (live backend, slice 26)", () => {
    const base = { id: 1, event_id: 242, at: "2026-10-24T20:18:51Z", actor_role: "ohs" as const, actor_name: "Сидорова А. В." };
    render(<MemoryRouter><History actions={[
      { ...base, id: 1, action: "identified", from_status: "sent_to_master", to_status: "sent_to_master", comment: "ФИО: Петров; должность: ; бригада: Бригада №3" },
      { ...base, id: 2, at: "2026-10-24T20:19:00Z", actor_role: "operator", action: "confirmed", from_status: "viewed", to_status: "confirmed", comment: "" },
    ]} /></MemoryRouter>);
    const rows = screen.getAllByRole("listitem");
    expect(rows[0].textContent).toContain("Указан нарушитель");
    expect(rows[0].textContent).not.toContain("→");
    expect(rows[1].textContent).toContain("→");
  });

  it("no identity form without can_identify", async () => {
    eventServer(false);
    open("/events/41", "operator");
    await screen.findByTestId("incident-focus");
    await screen.findAllByText(createFixtureEvents()[0].event.title);
    expect(screen.queryByTestId("identity")).toBeNull();
  });
});

describe("shift PDF (tech.md 8.31)", () => {
  it("asks shift.pdf for the shown shift; 501 is a pending notice", async () => {
    serve(r => {
      if (path(r) === "/api/master/shift") return Response.json({ title: "Смена 2", start: "2026-10-24T05:00:00Z", end: "2026-10-24T17:00:00Z", total: 0, by_sector: [], by_scenario: [], events: [] });
      if (path(r) === "/api/master/inbox") return Response.json({ active: [], recent_resolved: [], server_now: "2026-10-24T09:00:00Z" });
      if (path(r) === "/api/master/shift.pdf") return notImplemented(30);
    });
    open("/master/shift", "master");
    await screen.findByText("Смена 2");
    fireEvent.click(screen.getByTestId("shift-pdf"));
    expect((await screen.findByTestId("pending")).textContent).toContain("Функция появится в следующем обновлении сервера");
    expect(screen.getByTestId("master-shift").textContent).not.toMatch(/слайс/);
    expect(requests.some(r => path(r) === "/api/master/shift.pdf")).toBe(true);
  });

  it("file name comes from Content-Disposition", () => {
    expect(fileName('attachment; filename="shift-2026-10-24-2.pdf"', "x.pdf")).toBe("shift-2026-10-24-2.pdf");
    expect(fileName(null, "x.pdf")).toBe("x.pdf");
  });
});
