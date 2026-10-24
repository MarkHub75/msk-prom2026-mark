import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { linearFit, niceScale, seconds } from "../components/charts/scale";
import { isoWeek, weeklyTrend } from "./ManagementStats";
import { StatsPage, dailyTrend, weekHourGrid, weekHourSlots } from "./Stats";

const row = (key: string, title: string, count: number, confirmed = 0, false_alarm = 0) => ({ key, title, count, confirmed, false_alarm });
const ohs = {
  date_from: "2026-09-25T00:00:00+03:00", date_to: "2026-10-24T23:59:59+03:00", include_demo: true,
  total: 57, reviewed: 40, false_alarm_share: 0.25, review_coverage: 40 / 57,
  by_day: [{ date: "2026-10-22", yellow: 6, red: 1, confirmed: 3, false_alarm: 1 }, { date: "2026-10-23", yellow: 9, red: 5, confirmed: 0, false_alarm: 0 }],
  by_hour: [row("09", "09:00", 12)], by_sector: [row("3", "Сектор 3 · Сборочный цех", 30, 10, 4)],
  by_scenario: [row("phone", "Телефон при работе", 20, 8, 2)], by_camera: [row("5", "Камера 3.1 · Конвейер", 26, 11, 6)],
  by_shift: [row("day", "Дневная смена", 40, 20, 8), row("night", "Ночная смена", 17, 10, 2)],
  by_status: [row("resolved", "Решено", 12)],
  operator_reaction_s: { n: 40, p50: 38, p95: 63, pending: 5 }, master_accept_s: { n: 9, p50: 213, p95: 288, pending: 2 }, master_resolve_s: { n: 0, p50: null, p95: null, pending: 0 },
};
const management = {
  weeks: [
    { week_start: "2026-09-21", yellow: 30, red: 4, confirmed: 18, false_alarm: 5 },
    { week_start: "2026-09-28", yellow: 28, red: 3, confirmed: 17, false_alarm: 4 },
    { week_start: "2026-10-05", yellow: 25, red: 6, confirmed: 15, false_alarm: 6 },
    { week_start: "2026-10-12", yellow: 22, red: 2, confirmed: 12, false_alarm: 3 },
    { week_start: "2026-10-19", yellow: 9, red: 1, confirmed: 5, false_alarm: 1 },
  ],
  top_sectors: [{ key: "1", title: "Сектор 1 · Прессовый участок", cameras: 2, confirmed: 22, per_camera: 11 }],
  top_scenarios: [row("fall", "Падение и неподвижность", 85, 5, 0)],
  yellow_trend: { previous: 120, recent: 92, change_pct: -23.3, text: "Жёлтых нарушений стало меньше на 23 % (4 недели к 4 неделям). Сравнение до и после не доказывает причину." },
};

beforeEach(() => {
  sessionStorage.clear();
  window.history.replaceState({}, "", "/?review=real");
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(new Date("2026-10-24T09:00:00Z")); // Saturday 12:00 MSK
});
afterEach(() => { cleanup(); vi.useRealTimers(); vi.unstubAllGlobals(); });

function backend() {
  const calls: URL[] = [];
  vi.stubGlobal("fetch", vi.fn(async (request: Request) => {
    const url = new URL(request.url);
    calls.push(url);
    if (url.pathname === "/api/stats/ohs") return Response.json(ohs);
    if (url.pathname === "/api/stats/management") return Response.json(management);
    if (url.pathname === "/api/journal/facets") return Response.json({ scenarios: [], levels: [], statuses: [], sectors: [{ id: "3", title: "Сектор 3" }], cameras: [], zones: [] });
    if (url.pathname === "/api/events") return Response.json({ items: [{ started_at: "2026-10-19T06:30:00Z" }, { started_at: "2026-10-19T06:59:00Z" }], total: 2, next_cursor: null });
    return Response.json({ code: "not_found", message: "Нет", details: {} }, { status: 404 });
  }));
  return calls;
}
const show = (path: string, managementView = false) => render(<MemoryRouter initialEntries={[path]}><StatsPage management={managementView} /></MemoryRouter>);

describe("chart maths", () => {
  it("fits a line with a corridor only from 5 points", () => {
    const fit = linearFit([0, 1, 2, 3, 4], [1, 3, 5, 7, 9.5])!;
    expect(fit.slope).toBeCloseTo(2.1);
    expect(fit.ci(2)).toBeGreaterThan(0);
    expect(linearFit([0, 1, 2], [1, 2, 3])!.ci(1)).toBeNull();
    expect(linearFit([0, 1], [1, 2])).toBeNull();
  });

  it("starts the daily trend at the first day with events and skips today", () => {
    expect(dailyTrend([0, 0, 2, 3, 4, 5, 90], true)).toBeNull(); // 4 complete days with events
    const t = dailyTrend([0, 0, 2, 3, 4, 5, 6, 7, 90], true)!;
    expect(t.start).toBe(2);
    expect(t.fit.n).toBe(6);
    expect(t.fit.slope).toBeCloseTo(1);
  });

  it("fits the weekly trend over complete weeks only", () => {
    const t = weeklyTrend([0, 30, 28, 25, 22, 9], 4)!;
    expect(t.start).toBe(1);
    expect(t.fit.n).toBe(4);
    expect(weeklyTrend([0, 0, 5, 6, 1], 3)).toBeNull();
  });

  it("puts events into Moscow weekday and hour", () => {
    const grid = weekHourGrid([{ started_at: "2026-10-18T21:30:00Z" }]); // Monday 00:30 MSK
    expect(grid[0][0]).toBe(1);
    const slots = weekHourSlots("2026-10-24", Date.parse("2026-10-24T09:00:00Z")); // Sat 00:00–12:00 MSK
    expect(slots[5][12]).toBe(1);
    expect(slots[5][13]).toBe(0); // not yet happened: «нет данных», not zero
    expect(slots[0][0]).toBe(0);
    expect(isoWeek("2026-10-19")).toBe(43);
    expect(niceScale(57).max).toBe(60);
    expect(seconds(213)).toBe("3 мин 33 с");
  });
});

describe("OHS analytics", () => {
  it("shows the backend figures with n, demo mark and journal links", async () => {
    const calls = backend();
    show("/ohs/stats?days=7&sector=3");
    await screen.findByTestId("stats-view");
    expect(screen.getByTestId("tile-total").textContent).toContain("57");
    expect(screen.getByTestId("tile-red").textContent).toContain("6");
    expect(screen.getByTestId("tile-false").textContent).toContain("25%");
    expect(screen.getByTestId("tile-false").textContent).toContain("n = 40");
    expect(screen.getByTestId("demo-badge").textContent).toBe("включая демо-данные");
    const stats = calls.find(u => u.pathname === "/api/stats/ohs")!;
    expect(stats.searchParams.get("sector_id")).toBe("3");
    expect(stats.searchParams.get("date_from")).toBe("2026-10-18T00:00:00+03:00");
    const scenario = within(screen.getByTestId("by-scenario")).getByRole("link", { name: /Телефон при работе/ });
    expect(scenario.getAttribute("href")).toBe("/ohs/journal?from=2026-10-18&to=2026-10-24&sector_id=3&scenario=phone");
    const op = screen.getByTestId("reaction-op");
    expect(op.textContent).toContain("38 с");
    expect(op.textContent).toContain("эскалация 45 с");
    expect(screen.getByTestId("reaction-res").textContent).toContain("Нет завершённых реакций");
    expect(await screen.findByText(/по журналу: 2/)).toBeTruthy();
  });

  it("drops demo data from every request when the toggle is off", async () => {
    const calls = backend();
    show("/ohs/stats");
    fireEvent.click(await screen.findByRole("checkbox", { name: "Демо-данные" }));
    await screen.findByText("без демо-данных");
    const last = calls.filter(u => u.pathname === "/api/stats/ohs").at(-1)!;
    expect(last.searchParams.get("include_demo")).toBe("false");
  });

  it("shows the API error message instead of charts", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => Response.json({ code: "db_unavailable", message: "База недоступна", details: {} }, { status: 503 })));
    show("/ohs/stats");
    expect((await screen.findByRole("alert")).textContent).toContain("База недоступна");
    expect(screen.queryByTestId("stats-view")).toBeNull();
  });
});

describe("management analytics", () => {
  it("shows the yellow trend text, last complete week and per-camera ranking", async () => {
    backend();
    show("/management", true);
    expect((await screen.findByTestId("yellow-trend-text")).textContent).toBe(management.yellow_trend.text);
    expect(screen.getByTestId("yellow-trend").textContent).toContain("−23%");
    const yellow = screen.getByTestId("kpi-yellow");
    expect(yellow.textContent).toContain("22");
    expect(yellow.textContent).toContain("−3");
    expect(yellow.textContent).toContain("текущая идёт: 9");
    const sector = within(screen.getByTestId("top-sectors")).getByRole("link", { name: /Сектор 1/ });
    expect(sector.textContent).toContain("11");
    expect(sector.getAttribute("href")).toContain("sector_id=1");
    expect(screen.getByRole("img", { name: "События по неделям" })).toBeTruthy();
  });
});
