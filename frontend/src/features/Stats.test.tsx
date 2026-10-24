import { cleanup, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { createFixtureEvents } from "../fixtures/data";
import type { EventSummary } from "../api/types";
import { StatsPage, statsFromEvents } from "./Stats";

const base = createFixtureEvents().map(detail => detail.event)[0];
const at = (iso: string, patch: Partial<EventSummary>): EventSummary => ({ ...base, started_at: iso, published_at: iso, ...patch });
// Now is 2026-10-24 12:00 MSK; the last 7 days are 18.10–24.10, the previous 7 are 11.10–17.10.
const events = [
  at("2026-10-24T06:00:00Z", { id: 1, level: "yellow", operator_verdict: "false_alarm", status: "false_alarm" }),
  at("2026-10-20T06:00:00Z", { id: 2, level: "yellow", operator_verdict: "confirmed", status: "resolved" }),
  at("2026-10-15T21:30:00Z", { id: 3, level: "red", operator_verdict: "confirmed", status: "resolved", sector_id: 9, sector_name: "Сектор 9" }),
  at("2026-10-12T06:00:00Z", { id: 4, level: "yellow", operator_verdict: "none", status: "new" }),
];

beforeEach(() => {
  sessionStorage.clear();
  window.history.replaceState({}, "", "/?review=real");
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(new Date("2026-10-24T09:00:00Z"));
});
afterEach(() => { cleanup(); vi.useRealTimers(); vi.unstubAllGlobals(); });

function show(management = false, path = "/ohs/stats") {
  render(<MemoryRouter initialEntries={[path]}><StatsPage management={management} /></MemoryRouter>);
}

describe("analytics", () => {
  it("counts journal figures by Moscow day and hour", () => {
    const s = statsFromEvents(events, 4);
    expect(s.false_alarm_share).toBeCloseTo(1 / 3);
    expect(s.by_day.find(r => r.date === "2026-10-16")).toMatchObject({ red: 1, yellow: 0 });
    expect(s.by_hour.find(r => r.key === "0")?.count).toBe(1);
    expect(s.by_sector[0].count).toBe(3);
  });

  it("falls back to the journal pages when /api/stats/ohs is not implemented", async () => {
    const queries: URLSearchParams[] = [];
    vi.stubGlobal("fetch", vi.fn(async (request: Request) => {
      const url = new URL(request.url);
      if (url.pathname === "/api/stats/ohs") return Response.json({ code: "not_implemented", message: "Нет", details: {} }, { status: 501 });
      queries.push(url.searchParams);
      const second = url.searchParams.has("cursor");
      return Response.json({ items: second ? events.slice(2) : events.slice(0, 2), total: 4, next_cursor: second ? null : "next" });
    }));
    show(true, "/management?days=90");
    expect((await screen.findByTestId("yellow-trend")).textContent).toBe("Жёлтых за последние 7 дней: 2, за предыдущие 7: 1");
    expect(screen.getByText("Рассчитано по данным журнала")).toBeTruthy();
    expect(screen.getByText("33%")).toBeTruthy();
    expect(screen.queryByText("По часам суток")).toBeNull();
    expect(queries).toHaveLength(2);
    expect(queries[0].get("limit")).toBe("200");
    expect(queries[0].get("date_from")).toBe("2026-07-27T00:00:00+03:00");
    expect(queries[1].get("cursor")).toBe("next");
  });

  it("shows the backend statistics as is when the endpoint answers", async () => {
    const fetch = vi.fn(async () => Response.json({
      total: 57, reviewed: 40, false_alarm_share: 0.25, review_coverage: null, include_demo: true,
      date_from: "2026-09-25T00:00:00+03:00", date_to: "2026-10-24T23:59:59+03:00",
      by_day: [{ date: "2026-10-23", red: 5, yellow: 9, confirmed: 0, false_alarm: 0 }],
      by_hour: [], by_sector: [], by_scenario: [], by_camera: [], by_shift: [],
      by_status: [{ key: "resolved", title: "Решено", count: 12, confirmed: 0, false_alarm: 0 }],
      operator_reaction_s: { n: 0, p50: null, p95: null, pending: 0 }, master_accept_s: { n: 0, p50: null, p95: null, pending: 0 }, master_resolve_s: { n: 0, p50: null, p95: null, pending: 0 },
    }));
    vi.stubGlobal("fetch", fetch);
    show();
    await screen.findByTestId("stats-view");
    expect(screen.getByRole("region", { name: "Итоги периода" }).textContent).toBe("Событий57Красных5Доля ложных срабатываний25%ложные из 40 с вердиктом оператораРешено мастером12");
    expect(screen.queryByText("Рассчитано по данным журнала")).toBeNull();
    expect(screen.getByText("По часам суток")).toBeTruthy();
    expect(fetch).toHaveBeenCalledTimes(1);
  });
});
