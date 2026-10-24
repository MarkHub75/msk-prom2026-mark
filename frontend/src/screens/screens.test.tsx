import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { api } from "../api/client";
import { CamerasScreen } from "./admin/CamerasScreen";

// One smoke test per screen (tech.md 10.1): the screen renders with a stubbed `api`.
vi.mock("../api/client", () => ({
  api: { GET: vi.fn(), POST: vi.fn(), PUT: vi.fn(), PATCH: vi.fn(), DELETE: vi.fn() },
  apiError: (e: { code: string; message: string }) => e,
}));

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe("screens", () => {
  it("cameras_screen_renders", async () => {
    vi.mocked(api.GET).mockResolvedValue({
      data: {
        sectors: [{ id: 1, name: "Прессовый участок", sort_order: 0, is_demo: false }],
        cameras: [
          {
            id: 7, sector_id: 1, name: "Пресс №2", description: "", is_demo: false,
            has_calibration: false, zones_count: 0, videos_count: 0,
          },
        ],
      },
    } as never);
    const taken = { code: "name_taken", message: "Сектор с таким названием уже есть" };
    vi.mocked(api.POST).mockResolvedValue({ error: taken } as never);
    render(<CamerasScreen />);
    expect(await screen.findByText("Пресс №2")).toBeTruthy();
    expect(screen.getAllByText("Прессовый участок").length).toBe(2); // sector row, camera row

    fireEvent.click(screen.getByText("Новый сектор"));
    fireEvent.change(screen.getByLabelText("Название"), { target: { value: "Прессовый участок" } });
    fireEvent.click(screen.getByText("Сохранить"));
    expect((await screen.findByRole("alert")).textContent).toBe(taken.message);

    fireEvent.click(screen.getByText("Отмена"));
    fireEvent.click(screen.getAllByText("Удалить")[1]);
    expect(screen.getByText(/Удалить камеру «Пресс №2»/)).toBeTruthy();
  });
});
