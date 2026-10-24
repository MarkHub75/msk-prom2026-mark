import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { useMeta } from "./AppShell";
import type { EventSummary } from "../api/types";

export type IconName = "arrow" | "back" | "camera" | "play" | "pause" | "grid" | "list" | "sound" | "mute" | "check" | "chevron" | "cross" | "eye" | "monitor" | "bell" | "journal" | "rules" | "chart" | "settings" | "user" | "pin";
export function Icon({ name, size = 18 }: { name: IconName; size?: number }) {
  const paths: Record<IconName, ReactNode> = {
    monitor: <><rect x="3" y="4" width="18" height="12" rx="1" /><path d="M8 20h8M12 16v4" /></>,
    bell: <path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 21h4" />,
    journal: <><path d="M5 3h12l2 2v16H5z" /><path d="M9 8h6M9 12h6M9 16h4" /></>,
    rules: <><path d="M4 6h10M4 12h16M4 18h10" /><circle cx="18" cy="6" r="2" /><circle cx="18" cy="18" r="2" /></>,
    chart: <path d="M4 20V4M4 20h16M8 16v-5M12 16V8M16 16v-3" />,
    settings: <><circle cx="12" cy="12" r="3" /><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2" /></>,
    user: <><circle cx="12" cy="8" r="4" /><path d="M4 21c1-4 4-6 8-6s7 2 8 6" /></>,
    pin: <><path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11Z" /><circle cx="12" cy="10" r="2.5" /></>,
    arrow: <path d="M4 12h15M13 5l7 7-7 7" />, back: <path d="M20 12H5M11 5l-7 7 7 7" />,
    camera: <><rect x="3" y="6" width="13" height="12" rx="1" /><path d="m16 10 5-3v10l-5-3" /></>,
    play: <path d="m8 4 12 8-12 8z" />, pause: <path d="M8 4v16M16 4v16" />,
    grid: <><rect x="3" y="3" width="7" height="7" /><rect x="14" y="3" width="7" height="7" /><rect x="3" y="14" width="7" height="7" /><rect x="14" y="14" width="7" height="7" /></>,
    list: <path d="M8 5h13M8 12h13M8 19h13M3 5h1M3 12h1M3 19h1" />,
    sound: <path d="M4 9h4l5-4v14l-5-4H4zM17 8c3 2 3 6 0 8M20 5c5 4 5 10 0 14" />,
    mute: <path d="M4 9h4l5-4v14l-5-4H4zM17 9l5 6M22 9l-5 6" />,
    check: <path d="m4 12 5 5L20 6" />, chevron: <path d="m9 5 7 7-7 7" />, cross: <path d="m6 6 12 12M18 6 6 18" />,
    eye: <><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z" /><circle cx="12" cy="12" r="3" /></>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="square" strokeLinejoin="miter" aria-hidden="true">{paths[name]}</svg>;
}
export function time(value?: string | null, seconds = true) { return value ? new Intl.DateTimeFormat("ru-RU", { hour: "2-digit", minute: "2-digit", second: seconds ? "2-digit" : undefined, timeZone: "Europe/Moscow" }).format(new Date(value)) : "—"; }
export function duration(ms: number) { const s = Math.max(0, Math.floor(ms / 1000)); return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`; }
export function number(id: number) { return String(id).padStart(2, "0"); }
export function Status({ event }: { event: EventSummary }) { return <span data-testid="event-status" className={`status status-${event.level}`}><i />{event.status_title}</span>; }
export function Level({ level }: { level: "red" | "yellow" }) { const title=useMeta()?.levels.find(item=>item.id===level)?.title ?? level; return <span className={`level level-${level}`}>{title}</span>; }
export function PageHeading({ title, meta, children }: { title: string; meta?: ReactNode; children?: ReactNode }) { return <div className="page-heading"><div><h1>{title}</h1>{meta && <div className="heading-meta">{meta}</div>}</div>{children && <div className="heading-actions">{children}</div>}</div>; }
export function Breadcrumb({ children }: { children: ReactNode }) { return <div className="breadcrumb"><Link to="/operator"><Icon name="back" size={15} /> Диспетчерская</Link><span>{children}</span></div>; }
export function Empty({ title, text, children }: { title: string; text: string; children?: ReactNode }) { return <div className="empty-state"><Icon name="camera" size={34} /><h3>{title}</h3><p>{text}</p>{children}</div>; }
export function ErrorNotice({ error, retry, compact = false }: { error: {code: string; message: string}; retry?: () => void; compact?: boolean }) { return <div className={`error-notice ${compact ? "compact" : ""}`} role="alert"><span className="error-code">{error.code.includes("not_implemented") ? "501" : "!"}</span><div><h3>{error.code.includes("not_implemented") ? "Этот метод API ещё не реализован" : "Не удалось получить данные"}</h3><p>{error.message}</p><small>Код: {error.code}. Данные не подменяются демонстрационными.</small></div>{retry && <button className="button" onClick={retry}>Повторить</button>}</div>; }
export function Loading({ text = "Получаем данные с сервера" }: { text?: string }) { return <div className="loading-state" role="status"><span className="loading-bar" /><p>{text}</p></div>; }
export function PanelHeading({ children, aside }: { children: ReactNode; aside?: ReactNode }) { return <div className="panel-heading"><h2>{children}</h2>{aside && <span>{aside}</span>}</div>; }
