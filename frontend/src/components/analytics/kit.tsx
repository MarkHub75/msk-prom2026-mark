import { useRef, type ReactNode } from "react";
import { Database } from "lucide-react";
import type { ApiState } from "../../api/useApi";

/** Keep the last loaded data while a refetch runs, so filters do not blank the screen. */
export function useSticky<T>(state: ApiState<T>): T | undefined {
  const last = useRef<T>();
  if (state.data !== undefined) last.current = state.data;
  return state.error ? undefined : last.current;
}

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
