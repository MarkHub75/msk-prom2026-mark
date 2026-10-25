import { act, cleanup, render, screen, waitFor, within } from "@testing-library/react";
import { MemoryRouter, useLocation } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";
import { createFixtureEvents, fixtureMeta } from "./fixtures/data";
import { setRole } from "./roles";

class LiveSocket { static last?: LiveSocket; onopen = null; onmessage: ((e: { data: string }) => void) | null = null; onclose = null; onerror = null; constructor() { LiveSocket.last = this; } close() {} }
const details = createFixtureEvents();
const base = details[0].event;
function serve() {
  vi.stubGlobal("fetch", async (request: Request) => {
    const path = new URL(request.url).pathname;
    if (path === "/api/health") return Response.json({ status: "ok", contract: "1.1.0" });
    if (path === "/api/meta") return Response.json(fixtureMeta);
    if (path === "/api/operator/dashboard") return Response.json({ sectors: [], feed: [], server_now: base.published_at });
    const event = path.match(/^\/api\/events\/(\d+)$/);
    if (event) return Response.json({ ...details[0], event: { ...base, id: Number(event[1]) } });
    return Response.json({ code: "not_found", message: `нет ${path}`, details: {} }, { status: 404 });
  });
}
function Where() { const l = useLocation(); return <output data-testid="where">{l.pathname + l.search}</output>; }
const red = (id: number) => act(() => LiveSocket.last?.onmessage?.({ data: JSON.stringify({ type: "notification", at: base.published_at, data: { id: `e${id}:red`, event_id: id, level: "red", text: `Тревога ${id}`, audience: ["operator"], sound: "siren", takeover: true } }) }));

beforeEach(() => { localStorage.clear(); history.replaceState({}, "", "/?review=real"); vi.stubGlobal("WebSocket", LiveSocket); });
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("red alarm flood", () => {
  it("a new red does not yank the operator out of an open takeover: it waits in the bar", async () => {
    serve();
    act(() => setRole("operator"));
    render(<MemoryRouter initialEntries={["/operator"]}><App /><Where /></MemoryRouter>);
    await screen.findByTestId("operator-view");
    red(41);
    await waitFor(() => expect(screen.getByTestId("where").textContent).toBe("/events/41?takeover=1"));
    red(43);
    red(44);
    await waitFor(() => expect(screen.getByRole("alert", { name: "Тревога, событие 44" })).toBeTruthy());
    expect(screen.getByTestId("where").textContent).toBe("/events/41?takeover=1");
  });

  it("the open takeover survives WS refreshes and a repeat of its own red; one click acts once", async () => {
    // Every WS state message refetches the card; the takeover must not unmount while it reloads.
    let detail = { ...details[0], allowed_actions: ["view", "confirm", "false_alarm", "send_to_master"] as typeof details[0]["allowed_actions"] };
    let release: (() => void) | undefined;
    const posts: string[] = [];
    let reads = 0;
    vi.stubGlobal("fetch", async (request: Request) => {
      const path = new URL(request.url).pathname;
      if (path === "/api/health") return Response.json({ status: "ok", contract: "1.1.0" });
      if (path === "/api/meta") return Response.json(fixtureMeta);
      if (request.method === "POST") {
        const { action } = await request.json() as { action: string };
        posts.push(action);
        const status = action === "view" ? "viewed" : "sent_to_master";
        detail = { ...detail, event: { ...detail.event, status, status_title: status }, allowed_actions: action === "view" ? ["confirm", "false_alarm", "send_to_master"] : [] };
        return Response.json(detail);
      }
      if (path === "/api/events/41") {
        reads += 1;
        if (reads > 1) await new Promise<void>((resolve) => { release = resolve; });
        return Response.json(detail);
      }
      return Response.json({ code: "not_found", message: `нет ${path}`, details: {} }, { status: 404 });
    });
    localStorage.setItem("safewatch.actor", "Иван Петров");
    act(() => setRole("operator"));
    render(<MemoryRouter initialEntries={["/events/41?takeover=1"]}><App /><Where /></MemoryRouter>);
    const dialog = await screen.findByRole("alertdialog");
    await waitFor(() => expect(posts).toEqual(["view"]));
    const update = { type: "event.updated", at: base.published_at, data: { ...base, status: "viewed", status_title: "Просмотрено" } };
    act(() => LiveSocket.last?.onmessage?.({ data: JSON.stringify(update) }));
    red(41);
    await waitFor(() => expect(reads).toBeGreaterThan(1));
    expect(screen.getByRole("alertdialog")).toBe(dialog);
    expect(screen.queryByText(/Загружаем событие/)).toBeNull();
    act(() => within(dialog).getByRole("button", { name: /Подтвердить/ }).click());
    await waitFor(() => expect(posts).toEqual(["view", "confirm"]));
    act(() => release?.());
    await waitFor(() => expect(screen.queryByRole("alertdialog")).toBeNull());
    expect(posts).toEqual(["view", "confirm"]);
    // The closed takeover leaves the address: the next independent red takes over instead of queuing.
    await waitFor(() => expect(screen.getByTestId("where").textContent).toBe("/events/41"));
    red(45);
    await waitFor(() => expect(screen.getByTestId("where").textContent).toBe("/events/45?takeover=1"));
  });
});
