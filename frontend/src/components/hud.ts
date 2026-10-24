import type { components } from "../api/schema";

type HudFrame = components["schemas"]["HudFrame"];
type HudObject = components["schemas"]["HudObject"];
type Zone = components["schemas"]["Zone"];
type Segment = components["schemas"]["Calibration"]["grid"][number];

export interface Size {
  width: number;
  height: number;
}

// Pixels of the canvas; the backend sends 0..1 coordinates, the layout scales them.
export type DrawOp =
  | { kind: "rect"; x: number; y: number; w: number; h: number; color: string }
  | { kind: "label"; x: number; y: number; w: number; h: number; lines: string[]; color: string }
  | { kind: "path"; points: [number, number][]; closed: boolean; color: string };

// Theme colors of tech.md 8.14; a tag level outranks the kind of object.
const KIND_COLOR: Record<HudObject["kind"], string> = {
  person: "#3BA7FF",
  vehicle: "#E6EDF3",
  phone: "#E6EDF3",
  other: "#E6EDF3",
};
const LEVEL_COLOR = { yellow: "#FFC400", red: "#FF3B30" };
const ZONE_COLOR = "#FFC400";
const GRID_COLOR = "#7A8794";
export const CHAR_W = 7; // canvas font "12px sans-serif", wide enough for Cyrillic
export const LINE_H = 14;
export const PAD = 4;

function clamp(v: number, low: number, high: number): number {
  return Math.min(Math.max(v, low), Math.max(low, high));
}

function color(o: HudObject): string {
  const levels = o.tags.map((t) => t.level);
  if (levels.includes("red")) return LEVEL_COLOR.red;
  if (levels.includes("yellow")) return LEVEL_COLOR.yellow;
  return KIND_COLOR[o.kind];
}

export function layoutHud(
  frame: HudFrame | null,
  zones: Zone[],
  grid: Segment[],
  size: Size,
  visible: boolean,
): DrawOp[] {
  if (!visible) return [];
  const { width, height } = size;
  const px = ([x, y]: readonly number[]): [number, number] => [x * width, y * height];
  const ops: DrawOp[] = [];
  for (const segment of grid) ops.push({ kind: "path", points: segment.map(px), closed: false, color: GRID_COLOR });
  for (const zone of zones) {
    ops.push({ kind: "path", points: zone.points.map(px), closed: zone.points.length > 2, color: ZONE_COLOR });
  }
  for (const o of frame?.objects ?? []) {
    const [x1, y1] = px([o.bbox[0], o.bbox[1]]);
    const [x2, y2] = px([o.bbox[2], o.bbox[3]]);
    const c = color(o);
    ops.push({ kind: "rect", x: x1, y: y1, w: x2 - x1, h: y2 - y1, color: c });
    const title = o.track_id === null ? o.label : `${o.label} #${o.track_id}`;
    const lines = [title, ...o.tags.map((t) => t.text)];
    const w = Math.min(width, Math.max(...lines.map((l) => l.length)) * CHAR_W + 2 * PAD);
    const h = Math.min(height, lines.length * LINE_H + 2 * PAD);
    // Above the box when it fits, else below it; always inside the frame.
    const y = clamp(y1 - h >= 0 ? y1 - h : y2, 0, height - h);
    ops.push({ kind: "label", x: clamp(x1, 0, width - w), y, w, h, lines, color: c });
  }
  return ops;
}
