import { act, cleanup, fireEvent, render, renderHook, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";
import { api } from "./api/client";
import { useWs } from "./api/ws";
import { LevelBadge, StatusBadge } from "./components/Badges";
import { NAV, menuFor } from "./nav";
import { setRole } from "./roles";

// Until slice 1 the backend answers /api/meta with 501; the shell must still render.
function stubFetch() {
  const body = { code: "not_implemented", message: "Функция появится в слайсе 1", details: {} };
  const fetch = vi.fn<(request: Request) => Promise<Response>>(
    async () => new Response(JSON.stringify(body), { status: 501 }),
  );
  vi.stubGlobal("fetch", fetch);
  return fetch;
}

function renderAt(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <App />
    </MemoryRouter>,
  );
}

// The shell listens to `backend.status` (slice 3): no real socket in jsdom.
class SilentSocket {
  onopen = null;
  onmessage = null;
  onclose = null;
  close() {}
}

beforeEach(() => {
  stubFetch();
  vi.stubGlobal("WebSocket", SilentSocket);
  act(() => setRole("operator"));
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("app shell", () => {
  it("role_switcher_changes_nav", async () => {
    renderAt("/operator");
    const nav = screen.getByRole("navigation", { name: "Навигация" });
    expect(within(nav).getByText("Секторы")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("Роль"), { target: { value: "master" } });
    const links = within(nav).getAllByRole("link").map((a) => a.getAttribute("href"));
    expect(links).toEqual(menuFor("master").map((item) => item.path));
    expect(within(nav).queryByText("Секторы")).toBeNull();
    expect(await screen.findByText("нет данных")).toBeTruthy();
  });

  it("stub_screens_show_slice", () => {
    // Since slice 13 every route has its screen; a route left without one would show the stub.
    expect(NAV.filter((i) => !i.screen).map((i) => i.path)).toEqual([]);
  });

  it("client_sends_role_header", async () => {
    const fetch = stubFetch();
    act(() => setRole("ohs"));
    await api.GET("/api/health");
    const request = fetch.mock.calls[0][0];
    expect(request.headers.get("X-Role")).toBe("ohs");
  });

  it("ws_connects_with_role", () => {
    const urls: string[] = [];
    class FakeSocket {
      onopen = null;
      onmessage = null;
      onclose = null;
      constructor(url: string) {
        urls.push(url);
      }
      close() {}
    }
    vi.stubGlobal("WebSocket", FakeSocket);
    act(() => setRole("master"));
    const hook = renderHook(() => useWs(() => {}));
    expect(urls).toEqual([`ws://${location.host}/ws?role=master`]);
    hook.unmount();
  });

  it("badges_show_text_and_icon", () => {
    const { container } = render(
      <>
        <LevelBadge level="red" />
        <StatusBadge status="new" />
      </>,
    );
    const [level, status] = container.querySelectorAll(".badge");
    expect(level.className).toContain("badge-red");
    expect(level.textContent).toBe("■red");
    expect(screen.getByText("■").getAttribute("aria-hidden")).toBe("true");
    expect(status.textContent).toBe("●new");
  });
});
