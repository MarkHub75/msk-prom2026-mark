import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { createFixtureEvents, fixtureMeta } from "../fixtures/data";
import { eventQuery, exportUrl, JournalPage } from "./Journal";

vi.mock("../components/AppShell", () => ({ useMeta: () => fixtureMeta, useUpdates: () => 0, roleTitles: { operator: "Оператор", master: "Мастер", ohs: "Охрана труда", management: "Руководство", admin: "Администратор" } }));

const details = createFixtureEvents();
const event = details[0].event;
const facets = {
  levels: fixtureMeta.levels.map(item => ({ id: item.id, title: item.title })),
  statuses: fixtureMeta.statuses.map(item => ({ id: item.id, title: item.title })),
  sectors: [{ id: "1", title: "Сектор 1 · Прессовый участок" }],
  scenarios: [{ id: event.scenario, title: event.title }],
  cameras: [{ id: "2", title: "Камера 1.2 · Проход у прессов" }],
  zones: [{ id: "5", title: "Камера 1.2 · Проход у прессов · Проезд погрузчика" }],
};

beforeEach(() => { sessionStorage.clear(); window.history.replaceState({}, "", "/?review=real"); });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("journal filters", () => {
  it("maps camera, zone, demo and recomputed filters to the API and to the CSV export", () => {
    const search = new URLSearchParams("camera_id=2&zone_id=5&demo=0&superseded=1&level=red&cursor=abc");
    const query = eventQuery(search);
    expect(query).toMatchObject({ camera_id: 2, zone_id: 5, include_demo: false, include_superseded: true, level: "red", cursor: "abc" });
    const url = new URL(exportUrl(search));
    expect(url.pathname).toBe("/api/events/export.csv");
    expect(url.searchParams.get("camera_id")).toBe("2");
    expect(url.searchParams.get("include_demo")).toBe("false");
    expect(url.searchParams.has("cursor")).toBe(false);
    expect(url.searchParams.has("limit")).toBe(false);
  });

  it("shows X of Y, applies a camera filter, and opens a read-only preview with a link to the card", async () => {
    const queries: URLSearchParams[] = [];
    vi.stubGlobal("fetch", vi.fn(async (request: Request) => {
      const url = new URL(request.url);
      if (url.pathname === "/api/journal/facets") return Response.json(facets);
      if (url.pathname === `/api/events/${event.id}`) return Response.json({ ...details[0], actions: [], allowed_actions: [] });
      queries.push(url.searchParams);
      return Response.json({ items: [event], total: 7, next_cursor: null });
    }));
    render(<MemoryRouter initialEntries={["/ohs/journal"]}><JournalPage /></MemoryRouter>);
    await screen.findByRole("link", { name: `Открыть историю события ${event.id}` });
    expect(screen.getByText(/Показано/).textContent).toContain("1");
    expect(screen.getByText(/Показано/).textContent).toContain("7");
    await waitFor(() => expect((screen.getByLabelText("Камера") as HTMLSelectElement).disabled).toBe(false));
    fireEvent.change(screen.getByLabelText("Камера"), { target: { value: "2" } });
    fireEvent.click(screen.getByRole("button", { name: /Найти/ }));
    await waitFor(() => expect(queries.at(-1)?.get("camera_id")).toBe("2"));
    expect(screen.getByTestId("export-csv").getAttribute("href")).toContain("camera_id=2");
    fireEvent.click(await screen.findByRole("button", { name: event.title }));
    expect(await screen.findByTestId("journal-preview")).toBeTruthy();
    expect((await screen.findByRole("link", { name: /Открыть карточку события/ })).getAttribute("href")).toBe(`/events/${event.id}`);
    expect(screen.queryAllByRole("button").some(b => b.hasAttribute("data-action"))).toBe(false);
  });
});
