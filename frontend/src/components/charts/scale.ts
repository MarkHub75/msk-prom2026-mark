import { useLayoutEffect, useRef, useState } from "react";

/** Round axis maximum and 3–5 clean ticks from 0. */
export function niceScale(value: number, count = 4): { max: number; ticks: number[] } {
  if (!(value > 0)) return { max: 4, ticks: [0, 1, 2, 3, 4] };
  const raw = value / count;
  const pow = 10 ** Math.floor(Math.log10(raw));
  const step = ([1, 2, 2.5, 5, 10].map(m => m * pow).find(s => s >= raw) ?? raw);
  const clean = step < 1 ? 1 : step;
  const max = Math.ceil(value / clean) * clean;
  const ticks: number[] = [];
  for (let t = 0; t <= max + 1e-9; t += clean) ticks.push(Math.round(t * 100) / 100);
  return { max, ticks };
}

export interface Pt { x: number; y: number }

/** Monotone cubic (Fritsch–Carlson): smooth, never overshoots below zero between points. */
export function smoothPath(points: Pt[]): string {
  const n = points.length;
  if (!n) return "";
  if (n < 3) return points.map((p, i) => `${i ? "L" : "M"}${p.x},${p.y}`).join("");
  const dx: number[] = [], m: number[] = [];
  for (let i = 0; i < n - 1; i++) { dx.push(points[i + 1].x - points[i].x); m.push((points[i + 1].y - points[i].y) / dx[i]); }
  const t: number[] = [m[0]];
  for (let i = 1; i < n - 1; i++) t.push(m[i - 1] * m[i] <= 0 ? 0 : (3 * (dx[i - 1] + dx[i])) / ((2 * dx[i] + dx[i - 1]) / m[i - 1] + (dx[i] + 2 * dx[i - 1]) / m[i]));
  t.push(m[n - 2]);
  let d = `M${points[0].x},${points[0].y}`;
  for (let i = 0; i < n - 1; i++) {
    const h = dx[i] / 3;
    d += `C${points[i].x + h},${points[i].y + h * t[i]} ${points[i + 1].x - h},${points[i + 1].y - h * t[i + 1]} ${points[i + 1].x},${points[i + 1].y}`;
  }
  return d;
}

// Two-sided 95 % Student t for df 1..30 (df > 30 → 1.96 is close enough for a corridor).
const T95 = [12.71, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.16, 2.145, 2.131, 2.12, 2.11, 2.101, 2.093, 2.086, 2.08, 2.074, 2.069, 2.064, 2.06, 2.056, 2.052, 2.048, 2.045, 2.042];

export interface LinearFit {
  slope: number; intercept: number; n: number;
  at: (x: number) => number;
  /** Half-width of the 95 % confidence interval of the fitted line (not of single values) at x; null when n < 5. */
  ci: (x: number) => number | null;
}

/** Ordinary least squares y = a + b·x. Null below 3 points or with no spread in x. */
export function linearFit(xs: number[], ys: number[]): LinearFit | null {
  const n = xs.length;
  if (n < 3) return null;
  const mx = xs.reduce((s, v) => s + v, 0) / n, my = ys.reduce((s, v) => s + v, 0) / n;
  let sxx = 0, sxy = 0;
  for (let i = 0; i < n; i++) { sxx += (xs[i] - mx) ** 2; sxy += (xs[i] - mx) * (ys[i] - my); }
  if (!sxx) return null;
  const slope = sxy / sxx, intercept = my - slope * mx;
  const sse = xs.reduce((s, x, i) => s + (ys[i] - (intercept + slope * x)) ** 2, 0);
  const s = Math.sqrt(sse / (n - 2));
  const t = T95[n - 3] ?? 1.96;
  return {
    slope, intercept, n,
    at: x => intercept + slope * x,
    ci: x => n < 5 ? null : t * s * Math.sqrt(1 / n + (x - mx) ** 2 / sxx),
  };
}

/** Width of an element in CSS px; 800 until measured (and in jsdom, which has no ResizeObserver). */
export function useWidth<T extends HTMLElement>(fallback = 800) {
  const ref = useRef<T>(null);
  const [width, setWidth] = useState(fallback);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el || typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver(([entry]) => { const w = Math.round(entry.contentRect.width); if (w > 0) setWidth(w); });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return [ref, width] as const;
}

export const fmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 1 });
export const pct = (share: number | null | undefined, digits = 0) => share === null || share === undefined ? "—" : `${(share * 100).toFixed(digits).replace(".", ",")}%`;

/** Seconds as «38 с», «3 мин 33 с», «1 ч 05 мин». */
export function seconds(value: number | null | undefined): string {
  if (value === null || value === undefined) return "—";
  const s = Math.round(value);
  if (s < 90) return `${s} с`;
  if (s < 3600) { const m = Math.floor(s / 60), r = s % 60; return r ? `${m} мин ${r} с` : `${m} мин`; }
  const h = Math.floor(s / 3600), m = Math.round((s % 3600) / 60);
  return `${h} ч ${String(m).padStart(2, "0")} мин`;
}

export const plural = (n: number, one: string, few: string, many: string) => {
  const d = Math.abs(n) % 10, h = Math.abs(n) % 100;
  return d === 1 && h !== 11 ? one : d >= 2 && d <= 4 && (h < 12 || h > 14) ? few : many;
};
