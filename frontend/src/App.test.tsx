import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";
import { api } from "./api/client";
import { menuFor } from "./nav";
import { setRole } from "./roles";

function stubFetch() {
  const body = { code: "not_implemented", message: "Функция появится в слайсе 6", details: { slice: "6" } };
  const fetch = vi.fn<(request: Request) => Promise<Response>>(
    async () => new Response(JSON.stringify(body), { status: 501 }),
  );
  vi.stubGlobal("fetch", fetch);
  return fetch;
}
class QuietSocket {
  onopen = null;
  onmessage = null;
  onclose = null;
  onerror = null;
  close() {}
}
beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
  window.history.replaceState({}, "", "/?review=real");
  stubFetch();
  vi.stubGlobal("WebSocket", QuietSocket);
  act(() => setRole("operator"));
});
afterEach(() => { cleanup(); vi.unstubAllGlobals(); });
function renderAt(path: string) { return render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>); }

describe("real-mode shell and contract boundary", () => {
  it("surfaces an unfinished backend route without substituting fixtures", async () => {
    renderAt("/operator");
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("Функция появится в слайсе 6");
    expect(alert.textContent).toContain("501");
    expect(screen.queryByText(/Синтетический сценарий/)).toBeNull();
    expect(screen.getByTestId("backend").textContent).not.toBe("REVIEW");
  });
  it("role switching changes the working navigation and landing", async () => {
    renderAt("/operator");
    fireEvent.change(screen.getByLabelText("Роль"), { target: { value: "master" } });
    const nav = screen.getByRole("navigation", { name: "Разделы" });
    const links = within(nav).getAllByRole("link").map(link => link.getAttribute("href"));
    expect(links).toEqual(menuFor("master").map(item => item.path));
    expect(await screen.findByTestId("master-inbox")).toBeTruthy();
  });
  it("names the imported demo pack and its detection source in the header (tech.md 8.19)", async () => {
    const pack = { id: 1, name: "argus", sha256: "a1", backend: "linq", fake: false, cameras: 3, videos: 3, imported_at: "2026-10-24T14:00:00Z" };
    vi.stubGlobal("fetch", vi.fn(async (request: Request) => new URL(request.url).pathname === "/api/demo/packs"
      ? Response.json([pack])
      : Response.json({ code: "not_implemented", message: "нет", details: {} }, { status: 501 })));
    renderAt("/operator");
    expect((await screen.findByTestId("demo-pack")).textContent).toBe("Демо-пакет argus: детекции LinQ");
  });
  it("sends the active role and encoded actor through the real transport", async () => {
    const fetch = stubFetch();
    act(() => setRole("ohs"));
    localStorage.setItem("safewatch.actor", "Егор Иванов");
    await api.GET("/api/health");
    const request = fetch.mock.calls[0][0];
    expect(request.headers.get("X-Role")).toBe("ohs");
    expect(request.headers.get("X-Actor")).toBe(encodeURIComponent("Егор Иванов"));
  });
});
