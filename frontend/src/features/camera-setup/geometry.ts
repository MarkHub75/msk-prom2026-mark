// Pure helpers of the camera setup tabs (tech.md 8.11): normalized frame coordinates [0, 1],
// polygon/line edits, client-side prechecks mirroring the backend rules, Russian number format.
import type { ApiFailure } from "../../api/client";

export type Pt = [number, number];
export type ZoneGeometry = "polygon" | "line";

// Backend limits (services.py / analysis/geometry.py); the backend stays the authority.
export const ZONE_POINTS_MAX = 32;
export const ZONE_NAME_MAX = 60;
export const CAL_POINTS_MIN = 4;
export const CAL_POINTS_MAX = 8;
export const MIN_AREA = 1e-4;

export const clamp01 = (v: number) => (v < 0 ? 0 : v > 1 ? 1 : v);
export const round4 = (v: number) => Math.round(v * 10000) / 10000;
export const norm = (p: Pt): Pt => [round4(clamp01(p[0])), round4(clamp01(p[1]))];

/** Client point → normalized frame point, clamped to the frame. */
export function toNorm(clientX: number, clientY: number, rect: { left: number; top: number; width: number; height: number }): Pt {
  if (!rect.width || !rect.height) return [0, 0];
  return norm([(clientX - rect.left) / rect.width, (clientY - rect.top) / rect.height]);
}

export function toPx(p: Pt | readonly number[], w: number, h: number): [number, number] {
  return [p[0] * w, p[1] * h];
}

export function svgPoints(points: readonly (readonly number[])[], w: number, h: number): string {
  return points.map((p) => `${(p[0] * w).toFixed(1)},${(p[1] * h).toFixed(1)}`).join(" ");
}

/** Shoelace area in normalized units (share of the frame). */
export function polygonArea(points: readonly (readonly number[])[]): number {
  let s = 0;
  for (let i = 0; i < points.length; i++) {
    const [x1, y1] = points[i];
    const [x2, y2] = points[(i + 1) % points.length];
    s += x1 * y2 - x2 * y1;
  }
  return Math.abs(s) / 2;
}

/** Label anchor: area centroid, falls back to the mean of the vertices for degenerate shapes. */
export function centroid(points: readonly (readonly number[])[]): Pt {
  if (points.length === 0) return [0.5, 0.5];
  const mean: Pt = [points.reduce((s, p) => s + p[0], 0) / points.length, points.reduce((s, p) => s + p[1], 0) / points.length];
  if (points.length < 3) return mean;
  let a = 0, cx = 0, cy = 0;
  for (let i = 0; i < points.length; i++) {
    const [x1, y1] = points[i];
    const [x2, y2] = points[(i + 1) % points.length];
    const f = x1 * y2 - x2 * y1;
    a += f; cx += (x1 + x2) * f; cy += (y1 + y2) * f;
  }
  if (Math.abs(a) < 1e-9) return mean;
  return [cx / (3 * a), cy / (3 * a)];
}

export function pointInPolygon(p: readonly number[], poly: readonly (readonly number[])[]): boolean {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, yi] = poly[i];
    const [xj, yj] = poly[j];
    if (yi > p[1] !== yj > p[1] && p[0] < ((xj - xi) * (p[1] - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}

/** Distance from p to the segment ab (same units as the input). */
export function distToSegment(p: readonly number[], a: readonly number[], b: readonly number[]): number {
  const dx = b[0] - a[0], dy = b[1] - a[1];
  const len = dx * dx + dy * dy;
  const t = len === 0 ? 0 : Math.max(0, Math.min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / len));
  return Math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dy));
}

/** Index of the vertex within `radius` px of p (frame w×h), or -1. */
export function hitVertex(points: readonly Pt[], p: Pt, w: number, h: number, radius = 7): number {
  let best = -1, bestD = radius;
  points.forEach((v, i) => {
    const d = Math.hypot((v[0] - p[0]) * w, (v[1] - p[1]) * h);
    if (d <= bestD) { best = i; bestD = d; }
  });
  return best;
}

/** Edge i (from vertex i to i+1) within `radius` px of p, or -1. */
export function hitEdge(points: readonly Pt[], p: Pt, w: number, h: number, closed: boolean, radius = 6): number {
  let best = -1, bestD = radius;
  const n = closed ? points.length : points.length - 1;
  for (let i = 0; i < n; i++) {
    const a = toPx(points[i], w, h), b = toPx(points[(i + 1) % points.length], w, h);
    const d = distToSegment(toPx(p, w, h), a, b);
    if (d <= bestD) { best = i; bestD = d; }
  }
  return best;
}

export const insertVertex = (points: readonly Pt[], edge: number, p: Pt): Pt[] => [...points.slice(0, edge + 1), norm(p), ...points.slice(edge + 1)];
export const removeVertex = (points: readonly Pt[], i: number): Pt[] => points.filter((_, k) => k !== i);
export const moveVertex = (points: readonly Pt[], i: number, p: Pt): Pt[] => points.map((v, k) => (k === i ? norm(p) : v));

/** Moves all points by (dx, dy), keeping the whole shape inside the frame. */
export function translate(points: readonly Pt[], dx: number, dy: number): Pt[] {
  if (points.length === 0) return [];
  const xs = points.map((p) => p[0]), ys = points.map((p) => p[1]);
  const cx = Math.max(-Math.min(...xs), Math.min(1 - Math.max(...xs), dx));
  const cy = Math.max(-Math.min(...ys), Math.min(1 - Math.max(...ys), dy));
  return points.map((p) => norm([p[0] + cx, p[1] + cy]));
}

export function samePoints(a: readonly (readonly number[])[], b: readonly (readonly number[])[]): boolean {
  return a.length === b.length && a.every((p, i) => Math.abs(p[0] - b[i][0]) < 1e-6 && Math.abs(p[1] - b[i][1]) < 1e-6);
}

/** Precheck of the zone geometry with the backend texts; null — looks valid. */
export function zoneProblem(geometry: ZoneGeometry, points: readonly Pt[]): string | null {
  if (points.some((p) => p[0] < 0 || p[0] > 1 || p[1] < 0 || p[1] > 1)) return "Точки вне кадра";
  if (geometry === "line") return points.length === 2 && !samePoints([points[0]], [points[1]]) ? null : "Линия — ровно 2 точки";
  if (points.length < 3 || points.length > ZONE_POINTS_MAX) return `Полигон: от 3 до ${ZONE_POINTS_MAX} точек`;
  if (polygonArea(points) < MIN_AREA) return "Полигон без площади: точки на одной прямой";
  return null;
}

export function nameProblem(name: string): string | null {
  const n = name.trim().length;
  return n >= 1 && n <= ZONE_NAME_MAX ? null : `Название зоны: от 1 до ${ZONE_NAME_MAX} символов`;
}

/** "1,5" or "1.5" → 1.5; empty or garbage → null. */
export function parseNumber(text: string): number | null {
  const t = text.trim().replace(/\s/g, "").replace(",", ".");
  if (!t || !/^[-+]?(\d+\.?\d*|\.\d+)$/.test(t)) return null;
  const v = Number(t);
  return Number.isFinite(v) ? v : null;
}

export function fmt(v: number | null | undefined, digits = 2): string {
  if (v === null || v === undefined || !Number.isFinite(v)) return "—";
  return new Intl.NumberFormat("ru-RU", { maximumFractionDigits: digits, minimumFractionDigits: 0 }).format(v);
}

/** Normalized coordinate as a percentage of the frame, e.g. "45,2 %". */
export const pct = (v: number) => `${fmt(v * 100, 1)} %`;

/** Field of a 422 `validation` error (`details.field`), e.g. "points", "params.hold_s". */
export function errorField(error?: ApiFailure): string | undefined {
  const field = error?.details?.field;
  return typeof field === "string" ? field : undefined;
}

/** Points of the calibration hull (meters are valid only inside it, tech.md 8.11). */
export function convexHull(points: readonly Pt[]): Pt[] {
  const p = [...points].sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  if (p.length < 3) return p;
  const cross = (o: Pt, a: Pt, b: Pt) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const lower: Pt[] = [];
  for (const q of p) { while (lower.length >= 2 && cross(lower[lower.length - 2], lower[lower.length - 1], q) <= 0) lower.pop(); lower.push(q); }
  const upper: Pt[] = [];
  for (const q of [...p].reverse()) { while (upper.length >= 2 && cross(upper[upper.length - 2], upper[upper.length - 1], q) <= 0) upper.pop(); upper.push(q); }
  return [...lower.slice(0, -1), ...upper.slice(0, -1)];
}

export type H3 = number[]; // row-major 3×3

/** Least-squares homography image → world with h33 = 1 (browser preview only; the backend fits its own). */
export function fitHomography(image: readonly Pt[], world: readonly Pt[]): H3 | null {
  if (image.length < 4 || image.length !== world.length) return null;
  const ata = Array.from({ length: 8 }, () => new Array<number>(8).fill(0));
  const atb = new Array<number>(8).fill(0);
  const add = (row: number[], b: number) => {
    for (let i = 0; i < 8; i++) { atb[i] += row[i] * b; for (let j = 0; j < 8; j++) ata[i][j] += row[i] * row[j]; }
  };
  image.forEach(([x, y], k) => {
    const [X, Y] = world[k];
    add([x, y, 1, 0, 0, 0, -x * X, -y * X], X);
    add([0, 0, 0, x, y, 1, -x * Y, -y * Y], Y);
  });
  const h = solve(ata, atb);
  return h ? [...h, 1] : null;
}

function solve(a: number[][], b: number[]): number[] | null {
  const n = b.length, m = a.map((row, i) => [...row, b[i]]);
  for (let c = 0; c < n; c++) {
    let piv = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(m[r][c]) > Math.abs(m[piv][c])) piv = r;
    if (Math.abs(m[piv][c]) < 1e-12) return null;
    [m[c], m[piv]] = [m[piv], m[c]];
    for (let r = 0; r < n; r++) {
      if (r === c) continue;
      const f = m[r][c] / m[c][c];
      for (let k = c; k <= n; k++) m[r][k] -= f * m[c][k];
    }
  }
  return m.map((row, i) => row[n] / row[i]);
}

export function applyH(h: H3, p: readonly number[]): Pt | null {
  const w = h[6] * p[0] + h[7] * p[1] + h[8];
  if (Math.abs(w) < 1e-12) return null;
  return [(h[0] * p[0] + h[1] * p[1] + h[2]) / w, (h[3] * p[0] + h[4] * p[1] + h[5]) / w];
}

export function invertH(h: H3): H3 | null {
  const [a, b, c, d, e, f, g, i, k] = h;
  const det = a * (e * k - f * i) - b * (d * k - f * g) + c * (d * i - e * g);
  if (Math.abs(det) < 1e-12) return null;
  return [e * k - f * i, c * i - b * k, b * f - c * e, f * g - d * k, a * k - c * g, c * d - a * f, d * i - e * g, b * g - a * i, a * e - b * d].map((v) => v / det);
}

/** RMSE in meters of the fitted points (same idea as `fit_rmse_m`). */
export function fitRmse(h: H3, image: readonly Pt[], world: readonly Pt[]): number | null {
  if (!image.length) return null;
  let s = 0;
  for (let k = 0; k < image.length; k++) {
    const q = applyH(h, image[k]);
    if (!q) return null;
    s += (q[0] - world[k][0]) ** 2 + (q[1] - world[k][1]) ** 2;
  }
  return Math.sqrt(s / image.length);
}

/** 1 m grid over the world bounding box, mapped back to the frame (segments, may leave [0, 1]: the SVG clips). */
export function gridPreview(h: H3, world: readonly Pt[], step = 1, maxLines = 60): [Pt, Pt][] {
  const inv = invertH(h);
  if (!inv || world.length < 2) return [];
  const xs = world.map((p) => p[0]), ys = world.map((p) => p[1]);
  const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const out: [Pt, Pt][] = [];
  // The side of the horizon where the calibration points are.
  const sign = Math.sign(inv[6] * world[0][0] + inv[7] * world[0][1] + inv[8]) || 1;
  const seg = (a: Pt, b: Pt) => {
    // Sample the line so that points behind the horizon (w ≤ 0) are dropped instead of drawn across the frame.
    const n = 16;
    let prev: Pt | null = null;
    for (let t = 0; t <= n; t++) {
      const w: Pt = [a[0] + ((b[0] - a[0]) * t) / n, a[1] + ((b[1] - a[1]) * t) / n];
      const den = inv[6] * w[0] + inv[7] * w[1] + inv[8];
      const q = den * sign > 0 ? applyH(inv, w) : null;
      if (prev && q) out.push([prev, q]);
      prev = q;
    }
  };
  while ((x1 - x0) / step + (y1 - y0) / step > maxLines) step *= 2;
  for (let x = Math.ceil(x0 / step - 1e-9) * step; x <= x1 + 1e-9; x += step) seg([x, y0], [x, y1]);
  for (let y = Math.ceil(y0 / step - 1e-9) * step; y <= y1 + 1e-9; y += step) seg([x0, y], [x1, y]);
  return out;
}

/** Rule params to send: the stored overrides plus edits; a value equal to the default is not an override. */
export function overrides(defaults: Record<string, number>, edited: Record<string, number>): Record<string, number> {
  const out: Record<string, number> = {};
  for (const [k, v] of Object.entries(edited)) if (defaults[k] === undefined || Math.abs(defaults[k] - v) > 1e-9) out[k] = v;
  return out;
}
