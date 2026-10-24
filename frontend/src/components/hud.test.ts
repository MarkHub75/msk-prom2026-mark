import { describe, expect, it } from "vitest";
import type { components } from "../api/schema";
import { layoutHud, type DrawOp } from "./hud";

type HudObject = components["schemas"]["HudObject"];

const SIZE = { width: 320, height: 240 };

function person(bbox: [number, number, number, number]): HudObject {
  const tags = [
    { code: "speed", text: "бег 2,4 роста/с", level: "yellow" as const },
    { code: "feet_hidden", text: "ноги не видны", level: null },
  ];
  return { track_id: 12, kind: "person", label: "человек", score: 0.9, bbox, kpts: null, tags };
}

describe("hud", () => {
  it("callouts_stay_inside_frame", () => {
    const corners: [number, number, number, number][] = [
      [0, 0, 0.1, 0.2], // top left: no room above
      [0.9, 0.8, 1, 1], // bottom right: no room below or to the right
      [0.45, 0.4, 0.55, 0.6],
    ];
    const frame = { frame_idx: 0, ts_ms: 0, objects: corners.map(person) };
    const ops = layoutHud(frame, [], [], SIZE, true);
    const labels = ops.filter((op): op is Extract<DrawOp, { kind: "label" }> => op.kind === "label");
    expect(labels).toHaveLength(3);
    for (const op of labels) {
      expect(op.x).toBeGreaterThanOrEqual(0);
      expect(op.y).toBeGreaterThanOrEqual(0);
      expect(op.x + op.w).toBeLessThanOrEqual(SIZE.width);
      expect(op.y + op.h).toBeLessThanOrEqual(SIZE.height);
      expect(op.lines).toEqual(["человек #12", "бег 2,4 роста/с", "ноги не видны"]);
      expect(op.color).toBe("#FFC400");
    }
  });

  it("hidden_hud_draws_nothing", () => {
    const frame = { frame_idx: 0, ts_ms: 0, objects: [person([0.1, 0.1, 0.2, 0.5])] };
    const zone = { id: 1, camera_id: 7, kind: "danger", name: "Пресс", points: [[0, 0], [1, 0], [1, 1]] as [number, number][] };
    expect(layoutHud(frame, [zone], [], SIZE, false)).toEqual([]);
    expect(layoutHud(frame, [zone], [], SIZE, true).map((op) => op.kind)).toEqual(["path", "rect", "label"]);
  });
});
