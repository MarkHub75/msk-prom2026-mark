import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { createFixtureEvents, fixtureMeta } from "../fixtures/data";
import { JournalPage } from "./Journal";

vi.mock("../components/AppShell", () => ({ useMeta: () => fixtureMeta, useUpdates: () => 0 }));

const events = createFixtureEvents().map(detail => detail.event);
const resolved = events.find(event => event.status === "resolved")!;
const assigned = events.find(event => event.status === "sent_to_master")!;
const facets = {
  levels: fixtureMeta.levels.map(item => ({ id: item.id, title: item.title })),
  statuses: fixtureMeta.statuses.map(item => ({ id: item.id, title: item.title })),
  sectors: [{ id: String(resolved.sector_id), title: resolved.sector_name }],
  scenarios: [{ id: resolved.scenario, title: resolved.title }],
  cameras: [], zones: [],
};

beforeEach(() => {
  sessionStorage.clear();
  window.history.replaceState({}, "", "/?review=real");
});
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

function show(path = "/ohs/journal") {
  render(<MemoryRouter initialEntries={[path]}><JournalPage /></MemoryRouter>);
}

describe("server journal queries", () => {
  it("uses an opaque server cursor and drops it when applying new filters", async () => {
    const queries: URLSearchParams[] = [];
    vi.stubGlobal("fetch", vi.fn(async (request: Request) => {
      const url = new URL(request.url);
      if (url.pathname === "/api/journal/facets") return Response.json(facets);
      queries.push(new URLSearchParams(url.search));
      const filtered = url.searchParams.has("q");
      const second = url.searchParams.has("cursor");
      return Response.json({ items: [second ? assigned : resolved], total: filtered ? 1 : 2, next_cursor: filtered || second ? null : "opaque/next?+x" });
    }));
    show();
    expect((await screen.findByRole("link", { name: `Открыть историю события ${resolved.id}` })).getAttribute("href")).toBe(`/events/${resolved.id}`);
    fireEvent.click(screen.getByRole("button", { name: "Следующая страница" }));
    await screen.findByRole("link", { name: `Открыть историю события ${assigned.id}` });
    expect(queries.at(-1)?.get("cursor")).toBe("opaque/next?+x");
    fireEvent.change(screen.getByLabelText("Поиск"), { target: { value: "Проверенный участок" } });
    fireEvent.change(screen.getByLabelText("Состояние"), { target: { value: "resolved" } });
    fireEvent.click(screen.getByRole("button", { name: "Найти" }));
    await screen.findByRole("link", { name: `Открыть историю события ${resolved.id}` });
    expect(queries.at(-1)?.get("q")).toBe("Проверенный участок");
    expect(queries.at(-1)?.get("status")).toBe("resolved");
    expect(queries.at(-1)?.has("cursor")).toBe(false);
    expect(screen.queryByRole("button", { name: "Следующая страница" })).toBeNull();
  });

  it("restores URL filters on a fresh load and shows the server error without stale rows", async () => {
    let failed = false;
    const queries: URLSearchParams[] = [];
    vi.stubGlobal("fetch", vi.fn(async (request: Request) => {
      const url = new URL(request.url);
      if (url.pathname === "/api/journal/facets") return Response.json(facets);
      queries.push(url.searchParams);
      return failed ? Response.json({ code: "internal", message: "Журнал временно недоступен", details: {} }, { status: 500 }) : Response.json({ items: [resolved], total: 1, next_cursor: null });
    }));
    show("/ohs/journal?status=resolved&q=участок");
    await screen.findByRole("link", { name: `Открыть историю события ${resolved.id}` });
    expect(queries[0].get("status")).toBe("resolved");
    expect(queries[0].get("q")).toBe("участок");
    expect((screen.getByLabelText("Состояние") as HTMLSelectElement).value).toBe("resolved");
    failed = true;
    fireEvent.click(screen.getByRole("button", { name: "Обновить" }));
    await waitFor(() => expect(screen.getByRole("alert").textContent).toContain("Журнал временно недоступен"));
    expect(screen.queryByRole("link", { name: `Открыть историю события ${resolved.id}` })).toBeNull();
  });
});
