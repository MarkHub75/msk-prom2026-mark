import type { ReactNode } from "react";
import { Database, Info } from "lucide-react";
import { api } from "../../api/client";
import { useApi } from "../../api/useApi";
import { Sparkline } from "../charts/Figures";
import { C } from "../charts/palette";

export function Panel({ title, sub, aside, children, className = "", testId }: { title: string; sub?: ReactNode; aside?: ReactNode; children: ReactNode; className?: string; testId?: string }) {
  return <section className={`an-panel ${className}`} data-testid={testId} aria-label={title}>
    <header className="an-panel-head"><div><h2>{title}</h2>{sub && <p>{sub}</p>}</div>{aside}</header>
    {children}
  </section>;
}

export function DemoBadge({ on }: { on: boolean }) {
  return on
    ? <span className="an-chip an-chip-demo" data-testid="demo-badge"><Database size={13} strokeWidth={1.75} />включая демо-данные</span>
    : <span className="an-chip"><Database size={13} strokeWidth={1.75} />без демо-данных</span>;
}

export function Skeleton({ tiles = 5 }: { tiles?: number }) {
  return <div className="an-skeleton" role="status" aria-label="Загружаем аналитику">
    <div className="an-sk-tiles" style={{ gridTemplateColumns: `repeat(${tiles}, minmax(0, 1fr))` }}>{Array.from({ length: tiles }, (_, i) => <i key={i} />)}</div>
    <i className="an-sk-chart" />
    <div className="an-sk-row"><i /><i /><i /></div>
  </div>;
}

export const MSK_MS = 3 * 3600_000;
export const mskDay = (offsetDays = 0, base = Date.now()) => new Date(base + MSK_MS + offsetDays * 86400_000).toISOString().slice(0, 10);
export const shortDay = (date: string) => date.slice(5, 10).split("-").reverse().join(".");
export const ruDay = (date: string) => date.slice(0, 10).split("-").reverse().join(".");

/**
 * More events is not the same as more danger: cameras get connected, sensitivity changes.
 * Next to a dynamics chart: cameras observing right now (operator dashboard) and the confirmed share.
 */
export function GrowthContext({ sectorId, confirmed, total, shares, per }: { sectorId?: number; confirmed: number; total: number; shares: number[]; per: string }) {
  const dash = useApi(() => api.GET("/api/operator/dashboard"), []);
  const sectors = (dash.data?.sectors ?? []).filter(x => !sectorId || x.sector_id === sectorId);
  const cams = sectors.reduce((a, x) => a + x.cameras_total, 0), blind = sectors.reduce((a, x) => a + x.cameras_no_observation, 0);
  return <div className="an-context" data-testid="growth-context">
    <p><Info size={14} strokeWidth={1.75} />Больше событий — не обязательно больше опасности: могли подключить камеры или поменять чувствительность. Смотрите вместе с охватом и долей подтверждённых.</p>
    <div className="an-context-fig" title="Данные диспетчерской на текущий момент, истории охвата API не отдаёт">
      <span>Камер наблюдают сейчас</span>
      <b>{dash.data ? <>{cams - blind}<small> из {cams}</small></> : dash.error ? "—" : "…"}</b>
    </div>
    <div className="an-context-fig" title={`Подтверждено оператором ${confirmed} из ${total} событий`}>
      <span>Доля подтверждённых {per}</span>
      <b>{total ? `${Math.round((confirmed / total) * 100)}%` : "—"}<small> {confirmed} из {total}</small></b>
      <Sparkline values={shares} color={C.confirmed} label={`Доля подтверждённых ${per}`} />
    </div>
  </div>;
}
