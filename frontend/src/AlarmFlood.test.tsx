import { act, cleanup, render, screen, waitFor } from "@testing-library/react";
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
});
