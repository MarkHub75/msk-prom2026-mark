import { createContext, useCallback, useContext, useEffect, useId, useRef, useState, type ButtonHTMLAttributes, type InputHTMLAttributes, type ReactNode, type SelectHTMLAttributes } from "react";
import { Link } from "react-router-dom";
import {
  Activity, ArrowLeft, ArrowRight, BarChart3, Bell, Calculator, Check, ChevronDown, ChevronRight, CircleCheck, CircleDashed, Clock, Cpu, Database, Download,
  Ellipsis, ExternalLink, Eye, EyeOff, FileText, Filter, Inbox, Info, LayoutGrid, List, LoaderCircle, MapPin, MonitorPlay, OctagonAlert, Pause, Play,
  RefreshCw, ScrollText, Search, Server, Settings2, ShieldCheck, SlidersHorizontal, TriangleAlert, User, Users, Video, VideoOff, Volume2, VolumeX,
  Wifi, WifiOff, X, type LucideIcon,
} from "lucide-react";
import { useMeta } from "./AppShell";
import type { EventSummary } from "../api/types";

/* ---------- Icons: lucide-react behind the old `Icon name=...` API ---------- */
const ICONS = {
  arrow: ArrowRight, back: ArrowLeft, camera: Video, "camera-off": VideoOff, play: Play, pause: Pause, grid: LayoutGrid, list: List,
  sound: Volume2, mute: VolumeX, check: Check, chevron: ChevronRight, "chevron-down": ChevronDown, cross: X, eye: Eye, "eye-off": EyeOff,
  monitor: MonitorPlay, bell: Bell, journal: ScrollText, rules: SlidersHorizontal, chart: BarChart3, settings: Settings2, user: User, users: Users,
  pin: MapPin, alert: TriangleAlert, critical: OctagonAlert, info: Info, ok: CircleCheck, "no-observation": CircleDashed, clock: Clock,
  refresh: RefreshCw, search: Search, filter: Filter, download: Download, external: ExternalLink, more: Ellipsis, file: FileText,
  server: Server, cpu: Cpu, wifi: Wifi, "wifi-off": WifiOff, activity: Activity, shield: ShieldCheck, inbox: Inbox, spinner: LoaderCircle,
  calculator: Calculator, database: Database,
} satisfies Record<string, LucideIcon>;
export type IconName = keyof typeof ICONS;
export function Icon({ name, size = 16, className }: { name: IconName; size?: number; className?: string }) {
  const Svg = ICONS[name];
  return <Svg size={size} strokeWidth={1.75} aria-hidden="true" className={className} />;
}

/* ---------- Formatting ---------- */
export function time(value?: string | null, seconds = true) { return value ? new Intl.DateTimeFormat("ru-RU", { hour: "2-digit", minute: "2-digit", second: seconds ? "2-digit" : undefined, timeZone: "Europe/Moscow" }).format(new Date(value)) : "—"; }
export function duration(ms: number) { const s = Math.max(0, Math.floor(ms / 1000)); return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`; }
export function number(id: number) { return String(id).padStart(2, "0"); }

/* ---------- Existing page parts (API unchanged) ---------- */
const LEVEL_ICON: Record<"red" | "yellow", IconName> = { red: "critical", yellow: "alert" };
export function Status({ event }: { event: EventSummary }) { return <span data-testid="event-status" className={`status status-${event.level}`}><i />{event.status_title}</span>; }
export function Level({ level }: { level: "red" | "yellow" }) { const title = useMeta()?.levels.find(item => item.id === level)?.title ?? level; return <span className={`level level-${level}`}><Icon name={LEVEL_ICON[level]} size={13} />{title}</span>; }
export function PageHeading({ title, meta, children }: { title: string; meta?: ReactNode; children?: ReactNode }) { return <div className="page-heading"><div><h1>{title}</h1>{meta && <div className="heading-meta">{meta}</div>}</div>{children && <div className="heading-actions">{children}</div>}</div>; }
export function Breadcrumb({ children }: { children: ReactNode }) { return <div className="breadcrumb"><Link to="/operator"><Icon name="back" size={15} /> Диспетчерская</Link><span>{children}</span></div>; }
export function Empty({ title, text, children, icon = "camera" }: { title: string; text: string; children?: ReactNode; icon?: IconName }) { return <div className="empty-state"><span className="empty-icon"><Icon name={icon} size={22} /></span><h3>{title}</h3><p>{text}</p>{children}</div>; }
export const EmptyState = Empty;
export function ErrorNotice({ error, retry, compact = false }: { error: { code: string; message: string }; retry?: () => void; compact?: boolean }) { return <div className={`error-notice ${compact ? "compact" : ""}`} role="alert"><span className="error-code">{error.code.includes("not_implemented") ? "501" : "!"}</span><div><h3>{error.code.includes("not_implemented") ? "Этот метод API ещё не реализован" : "Не удалось получить данные"}</h3><p>{error.message}</p><small>Код: {error.code}. Данные не подменяются демонстрационными.</small></div>{retry && <button className="button" onClick={retry}>Повторить</button>}</div>; }
export function Loading({ text = "Получаем данные с сервера" }: { text?: string }) { return <div className="loading-state" role="status"><span className="loading-bar" /><p>{text}</p></div>; }
export function PanelHeading({ children, aside }: { children: ReactNode; aside?: ReactNode }) { return <div className="panel-heading"><h2>{children}</h2>{aside && <span>{aside}</span>}</div>; }

/* ---------- Design system primitives (see components/DS.md) ---------- */
const cx = (...names: (string | false | undefined | null)[]) => names.filter(Boolean).join(" ");

/** Panel with a tab-like title (or several tabs) on the left and a toolbar on the right. */
export function Panel({ title, tabs, active, onTab, tools, children, className, flush, ...rest }: { title?: ReactNode; tabs?: { id: string; label: ReactNode }[]; active?: string; onTab?: (id: string) => void; tools?: ReactNode; children: ReactNode; className?: string; flush?: boolean; "aria-label"?: string; "data-testid"?: string }) {
  return <section className={cx("ds-panel", className)} {...rest}>
    <header className="ds-panel-head">
      <div className="ds-panel-tabs" role={tabs ? "tablist" : undefined}>
        {tabs ? tabs.map(tab => <button key={tab.id} role="tab" aria-selected={tab.id === active} className={cx("ds-panel-tab", tab.id === active && "is-active")} onClick={() => onTab?.(tab.id)}>{tab.label}</button>) : <h2 className="ds-panel-tab is-active">{title}</h2>}
      </div>
      {tools && <div className="ds-panel-tools">{tools}</div>}
    </header>
    <div className={cx("ds-panel-body", flush && "is-flush")}>{children}</div>
  </section>;
}

export type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";
export type ButtonSize = "sm" | "md";
/** Class string for links that look like buttons: `<Link className={buttonClass("primary")}>`. */
export function buttonClass(variant: ButtonVariant = "secondary", size: ButtonSize = "md") { return cx("ds-btn", `ds-btn-${variant}`, size === "sm" && "ds-btn-sm"); }
export function Button({ variant = "secondary", size = "md", icon, iconRight, children, className, busy, ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: ButtonVariant; size?: ButtonSize; icon?: IconName; iconRight?: IconName; busy?: boolean }) {
  return <button type="button" {...props} aria-busy={busy || undefined} className={cx(buttonClass(variant, size), className)}>{busy ? <Icon name="spinner" size={size === "sm" ? 14 : 16} className="ds-spin" /> : icon && <Icon name={icon} size={size === "sm" ? 14 : 16} />}{children}{iconRight && <Icon name={iconRight} size={size === "sm" ? 14 : 16} />}</button>;
}
/** Square button with an icon only; `label` becomes aria-label and the tooltip. */
export function IconButton({ icon, label, size = "md", variant = "ghost", pressed, className, ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { icon: IconName; label: string; size?: ButtonSize; variant?: ButtonVariant; pressed?: boolean }) {
  return <button type="button" {...props} aria-label={label} title={label} aria-pressed={pressed} className={cx("ds-icon-btn", `ds-btn-${variant}`, size === "sm" && "ds-btn-sm", className)}><Icon name={icon} size={size === "sm" ? 14 : 16} /></button>;
}

/** Segmented control: one of a few mutually exclusive options. */
export function Segmented<T extends string>({ options, value, onChange, label, size = "md" }: { options: { id: T; label: ReactNode; icon?: IconName; count?: number }[]; value: T; onChange: (id: T) => void; label: string; size?: ButtonSize }) {
  return <div className={cx("ds-seg", size === "sm" && "ds-seg-sm")} role="group" aria-label={label}>
    {options.map(option => <button key={option.id} type="button" aria-pressed={option.id === value} className={option.id === value ? "is-active" : undefined} onClick={() => onChange(option.id)}>{option.icon && <Icon name={option.icon} size={14} />}{option.label}{option.count !== undefined && <span className="ds-seg-count">{option.count}</span>}</button>)}
  </div>;
}

/** Label + control + hint/error. Children is the control. */
export function Field({ label, hint, error, children, className }: { label: ReactNode; hint?: ReactNode; error?: ReactNode; children: ReactNode; className?: string }) {
  return <label className={cx("ds-field", error ? "has-error" : undefined, className)}><span className="ds-field-label">{label}</span>{children}{error ? <span className="ds-field-error">{error}</span> : hint && <span className="ds-field-hint">{hint}</span>}</label>;
}
export function TextInput({ icon, className, ...props }: InputHTMLAttributes<HTMLInputElement> & { icon?: IconName }) {
  return icon ? <span className={cx("ds-input-wrap", className)}><Icon name={icon} size={14} /><input {...props} className="ds-input" /></span> : <input {...props} className={cx("ds-input", className)} />;
}
export function Select({ className, children, ...props }: SelectHTMLAttributes<HTMLSelectElement>) {
  return <span className={cx("ds-select", className)}><select {...props}>{children}</select><Icon name="chevron-down" size={14} /></span>;
}
export function Checkbox({ label, className, ...props }: Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & { label: ReactNode }) {
  return <label className={cx("ds-check", className)}><input type="checkbox" {...props} /><span className="ds-check-box" aria-hidden="true"><Icon name="check" size={12} /></span><span>{label}</span></label>;
}
export function Switch({ label, checked, onChange, disabled }: { label: ReactNode; checked: boolean; onChange: (next: boolean) => void; disabled?: boolean }) {
  return <label className="ds-switch"><input type="checkbox" role="switch" checked={checked} disabled={disabled} onChange={e => onChange(e.target.checked)} /><span className="ds-switch-track" aria-hidden="true" /><span>{label}</span></label>;
}

export type Tone = "neutral" | "accent" | "red" | "amber" | "green" | "grey";
/** Small label; tone colours it, the icon and text carry the meaning. */
export function Badge({ tone = "neutral", icon, children, solid, title }: { tone?: Tone; icon?: IconName; children: ReactNode; solid?: boolean; title?: string }) {
  return <span className={cx("ds-badge", `ds-tone-${tone}`, solid && "is-solid")} title={title}>{icon && <Icon name={icon} size={12} />}{children}</span>;
}
export function Kbd({ children }: { children: ReactNode }) { return <kbd className="ds-kbd">{children}</kbd>; }
/** Monospace timecode or clock value. */
export function Timecode({ children, tone }: { children: ReactNode; tone?: "accent" }) { return <span className={cx("ds-tc", tone === "accent" && "is-accent")}>{children}</span>; }

/** Inline SVG sparkline of a small series (values from the API only). */
export function Sparkline({ values, tone = "accent", label }: { values: number[]; tone?: Tone; label?: string }) {
  if (values.length < 2) return null;
  const max = Math.max(...values), min = Math.min(...values), span = max - min || 1;
  const points = values.map((v, i) => `${(i / (values.length - 1)) * 100},${28 - ((v - min) / span) * 26}`).join(" ");
  return <svg className={cx("ds-spark", `ds-tone-${tone}`)} viewBox="0 0 100 30" preserveAspectRatio="none" role={label ? "img" : undefined} aria-label={label} aria-hidden={label ? undefined : true}><polyline points={points} fill="none" vectorEffect="non-scaling-stroke" /></svg>;
}
/** KPI tile: value, label, optional delta and a sparkline slot. */
export function Kpi({ label, value, unit, delta, deltaTone = "neutral", hint, spark, tone }: { label: ReactNode; value: ReactNode; unit?: ReactNode; delta?: ReactNode; deltaTone?: Tone; hint?: ReactNode; spark?: ReactNode; tone?: Tone }) {
  return <div className={cx("ds-kpi", tone && `ds-tone-${tone}`)}>
    <span className="ds-kpi-label">{label}</span>
    <span className="ds-kpi-value">{value}{unit && <small>{unit}</small>}</span>
    {(delta || hint) && <span className="ds-kpi-foot">{delta && <span className={`ds-kpi-delta ds-tone-${deltaTone}`}>{delta}</span>}{hint && <span className="ds-kpi-hint">{hint}</span>}</span>}
    {spark && <span className="ds-kpi-spark">{spark}</span>}
  </div>;
}

/** Hover/focus tooltip for any inline content. */
export function Tooltip({ content, children, side = "top" }: { content: ReactNode; children: ReactNode; side?: "top" | "bottom" | "right" }) {
  const id = useId();
  return <span className={`ds-tip-host ds-tip-${side}`} aria-describedby={id}>{children}<span role="tooltip" id={id} className="ds-tip">{content}</span></span>;
}

/** Loading placeholder lines/blocks. */
export function Skeleton({ lines = 3, height }: { lines?: number; height?: number }) {
  return <div className="ds-skeleton" aria-hidden="true">{height ? <span style={{ height }} /> : Array.from({ length: lines }, (_, i) => <span key={i} style={{ width: `${92 - (i % 3) * 18}%` }} />)}</div>;
}

/** Modal confirmation. Escape and the backdrop cancel; focus moves into the dialog and returns after. */
export function ConfirmDialog({ open, title, text, confirmLabel = "Подтвердить", cancelLabel = "Отмена", tone = "primary", busy, onConfirm, onCancel, children }: { open: boolean; title: string; text?: ReactNode; confirmLabel?: string; cancelLabel?: string; tone?: "primary" | "danger"; busy?: boolean; onConfirm: () => void; onCancel: () => void; children?: ReactNode }) {
  const box = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!open) return;
    const previous = document.activeElement as HTMLElement | null;
    box.current?.querySelector<HTMLElement>("[data-autofocus]")?.focus();
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") onCancel(); };
    document.addEventListener("keydown", onKey);
    return () => { document.removeEventListener("keydown", onKey); previous?.focus(); };
  }, [open, onCancel]);
  if (!open) return null;
  return <div className="ds-backdrop" onMouseDown={e => { if (e.target === e.currentTarget) onCancel(); }}>
    <div ref={box} className="ds-dialog" role="dialog" aria-modal="true" aria-label={title}>
      <header><Icon name={tone === "danger" ? "alert" : "info"} size={18} /><h2>{title}</h2></header>
      {text && <p>{text}</p>}{children}
      <footer><Button onClick={onCancel}>{cancelLabel}</Button><Button data-autofocus variant={tone} busy={busy} disabled={busy} onClick={onConfirm}>{confirmLabel}</Button></footer>
    </div>
  </div>;
}

/* ---------- Toasts ---------- */
export interface ToastInput { title: string; text?: string; tone?: "neutral" | "green" | "amber" | "red" }
interface ToastItem extends ToastInput { id: number }
const ToastContext = createContext<(toast: ToastInput) => void>(() => undefined);
/** `const toast = useToast(); toast({ tone: "green", title: "Сохранено" })`. Works only under ToastProvider (AppShell has it). */
export function useToast() { return useContext(ToastContext); }
const TOAST_ICON: Record<NonNullable<ToastInput["tone"]>, IconName> = { neutral: "info", green: "ok", amber: "alert", red: "critical" };
export function ToastProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<ToastItem[]>([]);
  const next = useRef(0);
  const close = useCallback((id: number) => setItems(list => list.filter(item => item.id !== id)), []);
  const push = useCallback((toast: ToastInput) => {
    const id = ++next.current;
    setItems(list => [...list.slice(-3), { ...toast, id }]);
    setTimeout(() => close(id), 5000);
  }, [close]);
  return <ToastContext.Provider value={push}>{children}
    <div className="ds-toasts" aria-live="polite">{items.map(item => <div key={item.id} className={`ds-toast ds-tone-${item.tone ?? "neutral"}`}><Icon name={TOAST_ICON[item.tone ?? "neutral"]} size={16} /><div><strong>{item.title}</strong>{item.text && <p>{item.text}</p>}</div><button type="button" aria-label="Закрыть" onClick={() => close(item.id)}><Icon name="cross" size={14} /></button></div>)}</div>
  </ToastContext.Provider>;
}
