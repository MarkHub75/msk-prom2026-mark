import { useState, type CSSProperties } from "react";
import { plural } from "./scale";

const HOURS = Array.from({ length: 24 }, (_, h) => h);

/**
 * Weekday × hour heat grid in one hue (light → strong = more events), with a marginal bar strip of
 * hour totals on top and weekday totals on the right. Hover or focus a cell to read it.
 */
export function Heatmap({ grid, rows, hourTotals, color = "var(--accent)" }: { grid: number[][]; rows: string[]; hourTotals: number[]; color?: string }) {
  const [cell, setCell] = useState<{ r: number; h: number } | null>(null);
  const max = Math.max(1, ...grid.flat());
  const hourMax = Math.max(1, ...hourTotals);
  const rowTotals = grid.map(r => r.reduce((s, v) => s + v, 0));
  const rowMax = Math.max(1, ...rowTotals);
  const readout = cell ? (() => { const v = grid[cell.r][cell.h]; return `${rows[cell.r]}, ${String(cell.h).padStart(2, "0")}:00–${String(cell.h).padStart(2, "0")}:59 — ${v} ${plural(v, "событие", "события", "событий")}`; })() : "Наведите на клетку, чтобы увидеть число событий";
  return <div className="an-heat" style={{ "--c": color } as CSSProperties}>
    <div className="an-heat-grid" role="grid" aria-label="События по дням недели и часам суток" onPointerLeave={() => setCell(null)}>
      <span className="an-heat-corner" />
      {HOURS.map(h => <span key={`m${h}`} className="an-heat-margin" title={`${String(h).padStart(2, "0")}:00 — ${hourTotals[h]} за период`}><i style={{ height: `${(hourTotals[h] / hourMax) * 100}%` }} /></span>)}
      <span className="an-heat-corner" />
      {grid.map((row, r) => <div key={rows[r]} role="row" className="an-heat-row">
        <span className="an-heat-day" role="rowheader">{rows[r]}</span>
        {row.map((v, h) => <span key={h} role="gridcell" tabIndex={-1} aria-label={`${rows[r]} ${h}:00 — ${v}`}
          className={`an-heat-cell${v ? "" : " is-zero"}${cell?.r === r && cell.h === h ? " is-hover" : ""}`}
          style={{ "--k": v ? 0.14 + 0.86 * (v / max) : 0 } as CSSProperties}
          onPointerEnter={() => setCell({ r, h })} onFocus={() => setCell({ r, h })} />)}
        <span className="an-heat-total" title={`${rows[r]}: ${rowTotals[r]}`}><i style={{ width: `${(rowTotals[r] / rowMax) * 100}%` }} /><b>{rowTotals[r]}</b></span>
      </div>)}
      <span className="an-heat-corner" />
      {HOURS.map(h => <span key={`h${h}`} className="an-heat-hour">{h % 3 === 0 ? String(h).padStart(2, "0") : ""}</span>)}
      <span className="an-heat-corner" />
    </div>
    <div className="an-heat-foot">
      <span className="an-heat-readout" aria-live="polite">{readout}</span>
      <span className="an-heat-scale"><span>0</span><i /><span>{max} в час</span></span>
    </div>
  </div>;
}
