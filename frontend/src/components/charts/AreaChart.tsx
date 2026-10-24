import { useId, useState, type CSSProperties, type KeyboardEvent, type PointerEvent } from "react";
import { fmt, niceScale, smoothPath, useWidth, type Pt } from "./scale";

export interface Series { id: string; name: string; values: number[]; color: string; kind?: "area" | "line" }

/** Linear trend drawn dashed over x-slots [from, to]; `ci` is the half-width of a corridor, omitted when not computed. */
export interface Projection { from: number; to: number; at: (i: number) => number; ci?: (i: number) => number | null; name: string; color: string; note: string }

interface Props {
  labels: string[];
  tipLabels?: string[];
  futureLabels?: string[];
  series: Series[];
  stacked?: boolean;
  projection?: Projection | null;
  partialLast?: string;
  height?: number;
  tickEvery?: number;
  unit: string;
  ariaLabel: string;
  onPick?: (index: number) => void;
  pickHint?: string;
}

const L = 44, R = 18, T = 22, B = 30;

function bandPath(top: Pt[], bottom: Pt[]) {
  const back = smoothPath([...bottom].reverse()).replace(/^M/, "L");
  return `${smoothPath(top)}${back}Z`;
}

/**
 * Smooth area/line chart over categorical x-slots: vertical gradient fills, dashed recessive grid,
 * crosshair tooltip (pointer and arrow keys), optional dashed linear projection into future slots.
 */
export function AreaChart({ labels, tipLabels = labels, futureLabels = [], series, stacked = false, projection, partialLast, height = 260, tickEvery = 1, unit, ariaLabel, onPick, pickHint }: Props) {
  const uid = useId().replace(/:/g, "");
  const [wrap, width] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<number | null>(null);
  const n = labels.length, slots = n + futureLabels.length;
  const W = Math.max(320, width), H = height, plotW = W - L - R, plotH = H - T - B;
  const x = (i: number) => L + (slots > 1 ? (i / (slots - 1)) * plotW : plotW / 2);
  const step = slots > 1 ? plotW / (slots - 1) : plotW;

  // Stack area series in order; lines sit on the same single axis, unstacked.
  const areas = series.filter(s => s.kind !== "line"), lines = series.filter(s => s.kind === "line");
  const cum: number[][] = [];
  areas.forEach((s, k) => cum.push(s.values.map((v, i) => v + (stacked && k ? cum[k - 1][i] : 0))));
  // The scale follows the trend line; a wide corridor is cut at the top rather than flattening the data.
  const projHi = projection ? Array.from({ length: projection.to - projection.from + 1 }, (_, j) => { const i = projection.from + j; return projection.at(i); }) : [];
  // An unfinished last slot (today, the current week) is not joined to the series and does not set
  // the axis: it is a ghost column at the right edge with «идёт: N». The axis follows complete slots.
  const done = partialLast && n > 1 ? n - 1 : n;
  const last = done - 1;
  const peak = (i: number) => Math.max(0, ...cum.map(c => c[i] ?? 0), ...lines.map(s => s.values[i] ?? 0));
  const peaks = Array.from({ length: done }, (_, i) => peak(i));
  const { max, ticks } = niceScale(Math.max(1, ...peaks, ...projHi));
  const y = (v: number) => Math.max(T, T + plotH - (Math.max(0, v) / max) * plotH);
  const pts = (vals: number[]) => vals.slice(0, done).map((v, i) => ({ x: x(i), y: y(v) }));

  const pick = (e: PointerEvent<SVGRectElement>) => {
    const box = e.currentTarget.getBoundingClientRect();
    const px = ((e.clientX - box.left) / box.width) * plotW;
    setHover(Math.max(0, Math.min(slots - 1, Math.round(px / step))));
  };
  const keys = (e: KeyboardEvent<SVGRectElement>) => {
    if (e.key === "ArrowRight" || e.key === "ArrowLeft") { e.preventDefault(); setHover(h => Math.max(0, Math.min(slots - 1, (h ?? n - 1) + (e.key === "ArrowRight" ? 1 : -1)))); }
    if (e.key === "Enter" && hover !== null && hover < n) onPick?.(hover);
  };

  // The extrapolation starts at the boundary of fact (the last actual slot), never over the history.
  const projFrom = projection ? Math.min(projection.to, Math.max(projection.from, last)) : 0;
  const inProj = (i: number) => !!projection && i >= projFrom && i <= projection.to;
  const tipX = hover === null ? 0 : x(hover);
  const flip = tipX > W * 0.62;
  const sum = (i: number) => areas.reduce((s, a) => s + (a.values[i] ?? 0), 0);

  return <div className="an-area" ref={wrap}>
    <svg width={W} height={H} role="img" aria-label={ariaLabel} className="an-svg">
      <defs>
        {series.map(s => <linearGradient key={s.id} id={`${uid}-${s.id}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={s.color} stopOpacity={0.12} />
          <stop offset="100%" stopColor={s.color} stopOpacity={0} />
        </linearGradient>)}
        <pattern id={`${uid}-future`} width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <line x1="0" y1="0" x2="0" y2="6" className="an-hatch" />
        </pattern>
      </defs>
      <text className="an-unit" x={4} y={10}>{unit}</text>
      {ticks.map(t => <g key={t}>
        <line className={t ? "an-gridline" : "an-base"} x1={L} x2={W - R} y1={y(t)} y2={y(t)} />
        <text className="an-tick" x={L - 8} y={y(t) + 4} textAnchor="end">{fmt.format(t)}</text>
      </g>)}
      {(futureLabels.length > 0 || done < n) && <g>
        <rect x={x(last)} y={T} width={x(slots - 1) - x(last) + R / 2} height={plotH} fill={`url(#${uid}-future)`} />
        <line className="an-now" x1={x(last)} x2={x(last)} y1={T - 6} y2={T + plotH} />
        {futureLabels.length > 0 && <text className="an-now-label" x={W - R} y={T - 8} textAnchor="end">проекция →</text>}
      </g>}
      {done < n && (() => {
        // Ghost column of the unfinished slot: stacked level parts, dashed outline, ▲ when above the axis.
        const total = sum(n - 1), bw = Math.max(8, Math.min(22, step * 0.55)), cx = x(n - 1);
        let acc = 0;
        return <g className="an-ghost" aria-label={`${partialLast}: ${total}`}>
          {areas.map(a => { const v = a.values[n - 1] ?? 0, y0 = y(acc), y1 = y(acc + v); acc += v; return v > 0 && y0 - y1 > 0.5 ? <rect key={a.id} x={cx - bw / 2} y={y1} width={bw} height={Math.max(1, y0 - y1 - 1)} fill={a.color} opacity={0.28} /> : null; })}
          <rect className="an-ghost-frame" x={cx - bw / 2} y={y(total)} width={bw} height={Math.max(1, y(0) - y(total))} rx={3} />
          {total > max && <text className="an-ghost-up" x={cx} y={T + 12} textAnchor="middle">▲</text>}
          <text className="an-ghost-label" x={cx} y={y(total) - 8} textAnchor={cx > W - 60 ? "end" : "middle"} dx={cx > W - 60 ? bw / 2 : 0}>идёт: {fmt.format(total)}</text>
        </g>;
      })()}

      {areas.map((s, k) => {
        const top = pts(cum[k]);
        const bottom = stacked && k ? pts(cum[k - 1]) : top.map(p => ({ x: p.x, y: y(0) }));
        return <g key={s.id}>
          <path d={bandPath(top, bottom)} fill={`url(#${uid}-${s.id})`} />
          <path d={smoothPath(top)} className="an-line" stroke={s.color} />
        </g>;
      })}
      {lines.map(s => <g key={s.id}>
        <path d={smoothPath(pts(s.values))} className="an-line an-line-2" stroke={s.color} />
      </g>)}

      {projection && (() => {
        // The corridor is drawn where it matters: from the last actual slot into the future.
        const bandFrom = projFrom;
        const idx = Array.from({ length: projection.to - bandFrom + 1 }, (_, j) => bandFrom + j);
        const ci = idx.map(i => projection.ci?.(i) ?? null);
        const hasBand = ci.every(c => c !== null);
        const end = { x: x(projection.to), y: y(projection.at(projection.to)) };
        return <g className="an-proj">
          {hasBand && <path d={`${idx.map((i, j) => `${j ? "L" : "M"}${x(i)},${y(projection.at(i) + ci[j]!)}`).join("")}${[...idx].reverse().map((i, j) => `L${x(i)},${y(projection.at(i) - ci[idx.length - 1 - j]!)}`).join("")}Z`} fill={projection.color} opacity={0.1} />}
          <path d={`M${x(projFrom)},${y(projection.at(projFrom))}L${end.x},${end.y}`} stroke={projection.color} className="an-trend" />
          <circle cx={end.x} cy={end.y} r={4} fill="var(--surface)" stroke={projection.color} strokeWidth={2} />
          <text className="an-trend-label" x={end.x - 4} y={end.y - 12} textAnchor="end">{projection.note}</text>
        </g>;
      })()}

      {labels.map((l, i) => i % tickEvery === 0 && <text key={`l${i}`} className="an-tick" x={x(i)} y={H - B + 18} textAnchor="middle">{l}</text>)}
      {futureLabels.map((l, j) => (n + j) % tickEvery === 0 && <text key={`f${j}`} className="an-tick an-tick-future" x={x(n + j)} y={H - B + 18} textAnchor="middle">{l}</text>)}

      {hover !== null && <g pointerEvents="none">
        <line className="an-cross" x1={tipX} x2={tipX} y1={T} y2={T + plotH} />
        {hover < done && areas.map((s, k) => <circle key={s.id} cx={tipX} cy={y(cum[k][hover])} r={3.5} fill={s.color} className="an-dot" />)}
        {hover < done && lines.map(s => <circle key={s.id} cx={tipX} cy={y(s.values[hover])} r={3.5} fill={s.color} className="an-dot" />)}
        {inProj(hover) && <circle cx={tipX} cy={y(projection!.at(hover))} r={4} fill="var(--surface)" stroke={projection!.color} strokeWidth={2} />}
      </g>}
      <rect className={`an-overlay${onPick ? " is-pickable" : ""}`} x={L} y={T} width={plotW} height={plotH} tabIndex={0}
        aria-label={`${ariaLabel}: стрелки — по точкам${onPick ? ", Enter — открыть в журнале" : ""}`}
        onPointerMove={pick} onPointerLeave={() => setHover(null)} onBlur={() => setHover(null)} onKeyDown={keys}
        onClick={() => { if (hover !== null && hover < n) onPick?.(hover); }} />
    </svg>
    {hover !== null && <div className="an-tip" style={{ left: tipX + (flip ? -14 : 14), top: T + 4, transform: flip ? "translateX(-100%)" : undefined }} role="status">
      <div className="an-tip-title">{hover < n ? tipLabels[hover] : futureLabels[hover - n]}{hover >= n && <span> · проекция</span>}</div>
      {hover < n && <>
        {[...series].reverse().map(s => <div key={s.id} className="an-tip-row"><i style={{ background: s.color }} /><b>{fmt.format(s.values[hover] ?? 0)}</b><span>{s.name}</span></div>)}
        {stacked && areas.length > 1 && <div className="an-tip-row an-tip-sum"><i /><b>{fmt.format(sum(hover))}</b><span>всего</span></div>}
      </>}
      {inProj(hover) && (() => { const c = projection!.ci?.(hover); const v = projection!.at(hover); return <div className="an-tip-row an-tip-proj"><i style={{ borderColor: projection!.color }} /><b>≈ {fmt.format(Math.max(0, v))}</b><span>{projection!.name}{c != null && ` · 95 %: ${fmt.format(Math.max(0, v - c))}–${fmt.format(v + c)}`}</span></div>; })()}
      {hover < n && onPick && <div className="an-tip-hint">{pickHint ?? "Клик — открыть в журнале"}</div>}
    </div>}
  </div>;
}

/** Legend with keys shaped like the marks: filled band for areas, stroke for lines, dashed stroke for a trend. */
export function Legend({ items }: { items: { name: string; color: string; kind?: "area" | "line" | "trend" | "band" }[] }) {
  return <ul className="an-legend">{items.map(it => <li key={it.name}><i className={`an-key an-key-${it.kind ?? "area"}`} style={{ "--c": it.color } as CSSProperties} />{it.name}</li>)}</ul>;
}
