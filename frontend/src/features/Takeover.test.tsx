import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { EventAlarm } from "../components/AlarmTakeover";
import { createFixtureEvents } from "../fixtures/data";
import type { EventSummary } from "../api/types";

const base = createFixtureEvents()[0].event;
const red = (status: EventSummary["status"]): EventSummary => ({ ...base, level: "red", status });
const show = (event: EventSummary, onAct = vi.fn()) => render(<MemoryRouter initialEntries={["/events/1?takeover=1"]}>
  <EventAlarm event={event} actions={[{ id: "confirm", title: "Подтвердить", key: "1", danger: true }]} onAct={onAct} />
</MemoryRouter>);
afterEach(cleanup);

describe("takeover", () => {
  it("offers the allowed actions with their keys", () => {
    const onAct = vi.fn();
    show(red("new"), onAct);
    fireEvent.click(screen.getByRole("button", { name: /Подтвердить/ }));
    expect(onAct).toHaveBeenCalledWith("confirm");
  });
  it("closes once the operator has acted", () => {
    show(red("sent_to_master"));
    expect(screen.queryByRole("alertdialog")).toBeNull();
  });
});
