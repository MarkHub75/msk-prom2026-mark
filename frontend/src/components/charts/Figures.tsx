import { useId, type CSSProperties, type ReactNode } from "react";
import { Link } from "react-router-dom";
import { ArrowDownRight, ArrowRight, ArrowUpRight } from "lucide-react";
import { fmt, smoothPath } from "./scale";

/** 12-ish point sparkline: gradient wash, smooth line, last point dot in the accent ring. */
export function Sparkline({ values, color, label, partialLast = false }: { values: number[]; color: string; label: string; partialLast?: boolean }) {
  const uid = useId().replace(/:/g, "");
  const W = 132, H = 30, pad = 4;
  // An unfinished last value is left out: it would set the scale and look like a collapse or a burst.
  const shown = partialLast && values.length > 2 ? values.slice(0, -1) : values;
  const max = Math.max(1, ...shown);
  const solid = shown.map((v, i) => ({ x: pad + (shown.length > 1 ? (i / (shown.length - 1)) * (W - pad * 2) : 0), y: H - pad - (v / max) * (H - pad * 2) }));
  if (!solid.length) return null;
  const last = solid[solid.length - 1];
  return <svg className="an-spark" width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="img" aria-label={label}>
    <defs><linearGradient id={`${uid}-g`} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={color} stopOpacity={0.12} /><stop offset="100%" stopColor={color} stopOpacity={0} /></linearGradient></defs>
    <path d={`${smoothPath(solid)}L${last.x},${H}L${solid[0].x},${H}Z`} fill={`url(#${uid}-g)`} />
    <path d={smoothPath(solid)} fill="none" stroke={color} strokeWidth={1.75} strokeLinecap="round" />
    <circle cx={last.x} cy={last.y} r={3.5} fill={color} stroke="var(--surface)" strokeWidth={2} />
  </svg>;
}

export type Direction = "up_bad" | "up_good" | "neutral";

/** Signed change vs a named period with arrow icon and text; colour by whether up is good. */
export function Delta({ now, prev, direction, vs }: { now: number; prev: number; direction: Direction; vs: string }) {
  const diff = now - prev;
  const tone = diff === 0 || direction === "neutral" ? "flat" : (diff > 0) === (direction === "up_good") ? "good" : "bad";
  const Icon = diff > 0 ? ArrowUpRight : diff < 0 ? ArrowDownRight : ArrowRight;
  const rel = prev ? ` · ${diff > 0 ? "+" : diff < 0 ? "−" : ""}${Math.round(Math.abs(diff) / prev * 100)}%` : "";
  return <span className={`an-delta an-delta-${tone}`}><Icon size={14} strokeWidth={1.75} aria-hidden /><b>{diff > 0 ? "+" : diff < 0 ? "−" : "±"}{fmt.format(Math.abs(diff))}{rel}</b> {vs}</span>;
}

export function StatTile({ label, value, unit, icon, delta, spark, foot, testId }: { label: string; value: ReactNode; unit?: string; icon?: ReactNode; delta?: ReactNode; spark?: ReactNode; foot?: ReactNode; testId?: string }) {
  const m = typeof value === "string" ? /^([−+]?[\d\s,]+)\s?(%|с|мин)$/.exec(value) : null;
  if (m && !unit) { value = m[1].trim(); unit = m[2]; }
  return <div className="an-tile" data-testid={testId}>
    <span className="an-tile-label">{icon}{label}</span>
    <div className="an-tile-main"><b className="an-tile-value">{value}{unit && <small>{unit}</small>}</b>{spark}</div>
    {delta && <div className="an-tile-delta">{delta}</div>}
    {foot && <div className="an-tile-foot">{foot}</div>}
  </div>;
}

/** Share meter: filled part of a track of the same hue, value and n written out. */
export function Meter({ share, color, label }: { share: number | null; color: string; label: string }) {
  return <div className="an-meter" role="meter" aria-label={label} aria-valuemin={0} aria-valuemax={100} aria-valuenow={share === null ? undefined : Math.round(share * 100)} style={{ "--c": color } as CSSProperties}>
    <i style={{ width: `${share === null ? 0 : Math.min(100, share * 100)}%` }} />
  </div>;
}

export interface BarSegment { value: number; color: string; name: string }
export interface BarRow { key: string; label: string; value: number; display?: string; sub?: string; to?: string; segments?: BarSegment[] }

/**
 * Horizontal bars: a gradient bar (or verdict segments with 2px gaps) per row, value at the tip,
 * the whole row a link when `to` is given.
 */
export function HBars({ rows, color, max: fixedMax, empty = "Нет данных за период", unit }: { rows: BarRow[]; color: string; max?: number; empty?: string; unit?: string }) {
  if (!rows.length) return <p className="an-none">{empty}</p>;
  const max = fixedMax ?? Math.max(1, ...rows.map(r => r.value));
  return <ol className="an-bars">{rows.map(r => {
    const width = `${(r.value / max) * 100}%`;
    const bar = <>
      <span className="an-bars-label"><span title={r.label}>{r.label}</span>{r.sub && <small>{r.sub}</small>}</span>
      <span className="an-bars-track">
        {r.segments ? <span className="an-bars-stack" style={{ width }}>{r.segments.filter(s => s.value > 0).map(s => <i key={s.name} title={`${s.name}: ${s.value}`} style={{ flexGrow: s.value, "--c": s.color } as CSSProperties} />)}</span>
          : <i className="an-bars-fill" style={{ width, "--c": color } as CSSProperties} />}
      </span>
      <b>{r.display ?? fmt.format(r.value)}{unit && <small>{unit}</small>}</b>
    </>;
    return <li key={r.key}>{r.to ? <Link to={r.to} className="an-bars-row is-link" title={`${r.label} — открыть в журнале`}>{bar}</Link> : <div className="an-bars-row">{bar}</div>}</li>;
  })}</ol>;
}

/** Part-to-whole donut (≤ 4 segments) with a 2px surface gap and the total in the hole. */
export function Donut({ parts, total, caption, size = 168 }: { parts: BarSegment[]; total: number; caption: string; size?: number }) {
  const r = size / 2 - 12, c = 2 * Math.PI * r, sum = parts.reduce((s, p) => s + p.value, 0);
  let acc = 0;
  return <svg className="an-donut" width={size} height={size} viewBox={`0 0 ${size} ${size}`} role="img" aria-label={`${caption}: ${parts.map(p => `${p.name} ${p.value}`).join(", ")}`}>
    <circle cx={size / 2} cy={size / 2} r={r} className="an-donut-track" />
    {sum > 0 && parts.filter(p => p.value > 0).map(p => {
      const len = (p.value / sum) * c, gap = parts.filter(q => q.value > 0).length > 1 ? 3 : 0;
      const el = <circle key={p.name} cx={size / 2} cy={size / 2} r={r} fill="none" stroke={p.color} strokeWidth={16}
        strokeDasharray={`${Math.max(0, len - gap)} ${c}`} strokeDashoffset={-acc} transform={`rotate(-90 ${size / 2} ${size / 2})`}><title>{`${p.name}: ${p.value}`}</title></circle>;
      acc += len;
      return el;
    })}
    <text x="50%" y="47%" textAnchor="middle" className="an-donut-value">{fmt.format(total)}</text>
    <text x="50%" y="62%" textAnchor="middle" className="an-donut-caption">{caption}</text>
  </svg>;
}

/** Range of a duration: 0–p50 solid, p50–p95 gradient, ticks at both, optional threshold line from config. */
export function RangeBullet({ p50, p95, max, color, threshold }: { p50: number | null; p95: number | null; max: number; color: string; threshold?: { value: number; label: string } }) {
  const at = (v: number) => `${Math.min(100, (v / max) * 100)}%`;
  return <div className="an-range" style={{ "--c": color } as CSSProperties}>
    <div className="an-range-track">
      {p50 !== null && <i className="an-range-core" style={{ width: at(p50) }} />}
      {p50 !== null && p95 !== null && <i className="an-range-tail" style={{ left: at(p50), width: `calc(${at(p95)} - ${at(p50)})` }} />}
      {p50 !== null && <span className="an-range-tick" style={{ left: at(p50) }} />}
      {p95 !== null && <span className="an-range-tick is-p95" style={{ left: at(p95) }} />}
      {threshold && <span className="an-range-target" style={{ left: at(threshold.value) }} title={threshold.label} />}
    </div>
  </div>;
}

export function TrendNote({ children }: { children: ReactNode }) {
  return <span className="an-trend-note"><i />{children}</span>;
}
