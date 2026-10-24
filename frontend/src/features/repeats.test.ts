import { describe, expect, it } from "vitest";
import { createFixtureEvents } from "../fixtures/data";
import type { EventSummary } from "../api/types";
import { groupRepeats, repeatCount, repeatTitle, spanText } from "./repeats";

const base = createFixtureEvents()[0].event;
const at = (minute: number) => new Date(Date.parse("2026-10-24T12:00:00Z") + minute * 60_000).toISOString();
const ev = (id: number, minute: number, extra: Partial<EventSummary> = {}): EventSummary => ({ ...base, id, published_at: at(minute), started_at: at(minute), camera_id: 8, camera_name: "Камера 5.1 · Публичный датасет падений", scenario: "fall", title: "Падение и неподвижность", level: "yellow", ...extra });

describe("groupRepeats", () => {
  it("merges open events of the same camera and scenario into one group, newest first", () => {
    const events = Array.from({ length: 19 }, (_, i) => ev(100 + i, i * 30 / 18));
    const groups = groupRepeats(events);
    expect(groups).toHaveLength(1);
    expect(groups[0].events).toHaveLength(19);
    expect(groups[0].latest.id).toBe(118);
    expect(groups[0].events.map(e => e.id)).toEqual(events.map(e => e.id).reverse());
    expect(repeatCount(groups[0])).toBe("×19 за 30 мин");
    expect(repeatTitle(groups[0])).toBe("Падение и неподвижность · Камера 5.1 · ×19 за 30 мин");
  });

  it("keeps a different camera or a different scenario apart", () => {
    const groups = groupRepeats([ev(1, 0), ev(2, 1, { camera_id: 9, camera_name: "Камера 5.2" }), ev(3, 2, { scenario: "running", title: "Бег" }), ev(4, 3)]);
    expect(groups.map(g => g.events.map(e => e.id))).toEqual([[4, 1], [2], [3]]);
  });

  it("splits repeats separated by more than 30 minutes", () => {
    const groups = groupRepeats([ev(1, 0), ev(2, 20), ev(3, 49), ev(4, 80)]);
    expect(groups.map(g => g.events.map(e => e.id))).toEqual([[3, 2, 1], [4]]);
  });

  it("chains in any input order and keeps the order of first appearance", () => {
    const groups = groupRepeats([ev(5, 40, { scenario: "phone", title: "Телефон" }), ev(3, 25), ev(1, 0), ev(2, 10)]);
    expect(groups.map(g => g.latest.id)).toEqual([5, 3]);
    expect(groups[1].events.map(e => e.id)).toEqual([3, 2, 1]);
    expect(groupRepeats([ev(1, 0), ev(2, 50), ev(3, 25)]).map(g => g.events.length)).toEqual([3]);
  });

  it("a group is red when any repeat is red; a lone event is a group of one", () => {
    const [red, lone] = groupRepeats([ev(1, 0), ev(2, 1, { level: "red" }), ev(3, 2, { camera_id: 3 })]);
    expect(red.level).toBe("red");
    expect(lone.events).toHaveLength(1);
    expect(lone.level).toBe("yellow");
  });

  it("span text", () => {
    expect(spanText(0)).toBe("за 1 мин");
    expect(spanText(150_000)).toBe("за 3 мин");
    expect(spanText(65 * 60_000)).toBe("за 1 ч 05 мин");
    expect(spanText(120 * 60_000)).toBe("за 2 ч");
  });
});
