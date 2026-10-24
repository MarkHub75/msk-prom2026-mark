import { useState, type CSSProperties } from "react";
import { plural } from "./scale";

const HOURS = Array.from({ length: 24 }, (_, h) => h);

const sub = (a: number[][], b?: number[][]) => a.map((row, r) => row.map((v, h) => v - (b?.[r][h] ?? 0)));

/**
 * Weekday × hour heat grid in one hue (light → strong = more events), with a marginal bar strip of
 * hour totals on top and weekday totals on the right. Hover or focus a cell to read it.
 * `slots[r][h]` — how many such weekday-hours the period really had; 0 means «нет данных», not zero events.
 * `today` — the part of `grid` from the current, unfinished day: it does not set the scale (a live burst
 * would burn it); cells above the scale take the full colour with ▲, today's cells are outlined.
 */
export function Heatmap({ grid, slots, today, todayRow, rows, hourTotals, color = "var(--accent)" }: { grid: number[][]; slots?: number[][]; today?: number[][]; todayRow?: number; rows: string[]; hourTotals: number[]; color?: string }) {
  const [cell, setCell] = useState<{ r: number; h: number } | null>(null);
  const base = sub(grid, today);
  const max = Math.max(1, ...base.flat());
  const todayHour = Array.from({ length: 24 }, (_, h) => (today ?? []).reduce((a, row) => a + row[h], 0));
  const hourMax = Math.max(1, ...hourTotals.map((v, h) => v - todayHour[h]));
  const rowTotals = grid.map(r => r.reduce((s, v) => s + v, 0));
  const rowMax = Math.max(1, ...base.map(r => r.reduce((s, v) => s + v, 0)));
  const pctOf = (v: number, m: number) => `${Math.min(100, (v / m) * 100)}%`;
  const hh = (h: number) => `${String(h).padStart(2, "0")}:00–${String(h).padStart(2, "0")}:59`;
  const tip = (r: number, h: number) => {
    const v = grid[r][h], k = slots?.[r][h];
    if (k === 0) return `${rows[r]}, ${hh(h)} МСК — нет данных: такого часа в периоде ещё не было`;
    const t = today?.[r][h] ?? 0;
    return `${rows[r]}, ${hh(h)} МСК — ${v} ${plural(v, "событие", "события", "событий")}${k ? ` за ${k} ${plural(k, "такой час", "таких часа", "таких часов")}` : ""}${t ? `, из них сегодня ${t}` : ""}${v > max ? " · выше шкалы" : ""}`;
  };
  const readout = cell ? tip(cell.r, cell.h) : "Наведите на клетку, чтобы увидеть число событий";
  return <div className="an-heat" style={{ "--c": color } as CSSProperties}>
    <div className="an-heat-grid" role="grid" aria-label="События по дням недели и часам суток" onPointerLeave={() => setCell(null)}>
      <span className="an-heat-corner" />
      {HOURS.map(h => <span key={`m${h}`} title={`${String(h).padStart(2, "0")}:00 — ${hourTotals[h]} за период${todayHour[h] ? `, из них сегодня ${todayHour[h]}` : ""}`} className={`an-heat-margin${hourTotals[h] > hourMax ? " is-over" : ""}`}><i style={{ height: pctOf(hourTotals[h], hourMax) }} /></span>)}
      <span className="an-heat-corner" />
      {grid.map((row, r) => <div key={rows[r]} role="row" className="an-heat-row">
        <span className={`an-heat-day${r === todayRow ? " is-today" : ""}`} role="rowheader" title={r === todayRow ? "Сегодня, день идёт" : undefined}>{rows[r]}</span>
        {row.map((v, h) => <span key={h} role="gridcell" tabIndex={-1} aria-label={tip(r, h)} data-tip={`${slots?.[r][h] === 0 ? "нет данных" : v}`}
          className={`an-heat-cell${slots?.[r][h] === 0 ? " is-nodata" : v ? "" : " is-zero"}${today?.[r][h] ? " is-today" : ""}${v > max ? " is-over" : ""}${cell?.r === r && cell.h === h ? " is-hover" : ""}${h > 20 ? " is-right" : ""}`}
          style={{ "--k": v ? 0.14 + 0.86 * Math.min(1, v / max) : 0 } as CSSProperties}
          onPointerEnter={() => setCell({ r, h })} onFocus={() => setCell({ r, h })} />)}
        <span className={`an-heat-total${rowTotals[r] > rowMax ? " is-over" : ""}`} title={`${rows[r]}: ${rowTotals[r]}`}><i style={{ width: pctOf(rowTotals[r], rowMax) }} /><b>{rowTotals[r]}</b></span>
      </div>)}
      <span className="an-heat-corner" />
      {HOURS.map(h => <span key={`h${h}`} className="an-heat-hour">{h % 3 === 0 ? String(h).padStart(2, "0") : ""}</span>)}
      <span className="an-heat-corner" />
    </div>
    <div className="an-heat-foot">
      <span className="an-heat-readout" aria-live="polite">{readout}</span>
      <span className="an-heat-scale"><i className="an-heat-nodata" />нет данных<i className="an-heat-zero" />0<i /><span>{max} в час{today ? " · без сегодняшнего дня" : ""}</span>{today && <><i className="an-heat-todaykey" />сегодня, идёт · ▲ выше шкалы</>}</span>
    </div>
  </div>;
}
