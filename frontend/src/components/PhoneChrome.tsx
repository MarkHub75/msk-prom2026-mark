import { useEffect, useState, type ReactNode } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { api } from "../api/client";
import { useApi } from "../api/useApi";
import type { WsStatus } from "../api/ws";
import type { Meta } from "../api/types";
import { ROLES, type Role } from "../roles";
import { Icon, type IconName } from "./ui";
import "../styles/mobile-shell.css";

interface Tab { to: string; label: string; icon: IconName; match: (path: string) => boolean }
const TABS: Partial<Record<Role, Tab[]>> = {
  operator: [
    { to: "/operator", label: "Тревоги", icon: "bell", match: p => p === "/operator" || p.startsWith("/events/") || p.startsWith("/operator/events/") },
    { to: "/operator/cameras", label: "Камеры", icon: "camera", match: p => p.startsWith("/operator/cameras") || p.startsWith("/operator/sectors") },
    { to: "/operator/shift", label: "Смена", icon: "clock", match: p => p.startsWith("/operator/shift") },
  ],
  master: [
    { to: "/master", label: "Поручения", icon: "inbox", match: p => p === "/master" || p.startsWith("/master/events") },
    { to: "/master/shift", label: "Смена", icon: "clock", match: p => p.startsWith("/master/shift") },
  ],
};
/** Screens with their own bottom action bar hide the tabs. */
export const isActionScreen = (path: string) => /^\/(?:master\/|m\/operator\/)?events\/\d+/.test(path);
/** tech.md 8.14 v5: an operator route on its /m/operator twin (`/events/7` -> `/m/operator/events/7`). */
export const toMobile = (path: string) => path.replace(/^\/(?:events\/|operator(?=\/|$))/, m => m === "/events/" ? "/m/operator/events/" : "/m/operator");
export const hasPhoneApp = (role: Role) => Boolean(TABS[role]);

const WS_DOT: Record<WsStatus, string> = { connected: "В сети", fixture: "Повтор", disconnected: "Нет связи", connecting: "Подключение" };

/** Badge of the first tab: what still waits for this role (operator verdict, master acceptance). */
function useWaiting(role: Role, updates: number) {
  const operator = useApi(() => role === "operator" ? api.GET("/api/operator/dashboard") : Promise.resolve({ data: undefined }), [role], { refresh: [updates] });
  const master = useApi(() => role === "master" ? api.GET("/api/master/inbox") : Promise.resolve({ data: undefined }), [role], { refresh: [updates] });
  if (role === "operator") return operator.data?.feed.filter(e => e.priority >= 2 || (e.escalated_by_timeout && e.operator_verdict === "none" && e.priority > 0)).length;
  if (role === "master") return master.data?.active.filter(e => e.status === "sent_to_master").length;
  return undefined;
}

export function PhoneTabs({ role, updates }: { role: Role; updates: number }) {
  const location = useLocation();
  const waiting = useWaiting(role, updates);
  const tabs = TABS[role];
  if (!tabs || isActionScreen(location.pathname)) return null;
  return <nav className="mb-tabs" aria-label="Разделы приложения" style={{ gridTemplateColumns: `repeat(${tabs.length}, 1fr)` }}>
    {tabs.map((tab, i) => {
      // Under /m/operator (tech.md 8.14 v5) every tab stays on the mobile routes.
      const mobile = location.pathname.startsWith("/m/");
      const active = tab.match(mobile ? location.pathname.slice(2) : location.pathname);
      const to = mobile ? toMobile(tab.to) : tab.to;
      return <NavLink key={tab.to} to={to} end className={() => active ? "active" : ""} aria-current={active ? "page" : undefined}>
        <span className="mb-tab-icon"><Icon name={tab.icon} size={22} />{i === 0 && waiting ? <b className="mb-badge" aria-label={`Ждут: ${waiting}`}>{waiting > 99 ? "99+" : waiting}</b> : null}</span>
        <span>{tab.label}</span>
      </NavLink>;
    })}
  </nav>;
}

const initials = (name: string) => name.trim().split(/\s+/).slice(0, 2).map(part => part[0]?.toUpperCase() ?? "").join("");

export function PhoneTop({ brand, home, ws, sound, onSound, actor, onProfile, alarm }: { brand: ReactNode; home: string; ws: WsStatus; sound: boolean; onSound: () => void; actor: string; onProfile: () => void; alarm?: ReactNode }) {
  return <header className="mb-top">
    <Link className="mb-brand" to={home}>{brand}</Link>
    <span className="mb-top-spacer" />
    {alarm}
    <span className="mb-live" data-status={ws} title={WS_DOT[ws]}><i />{WS_DOT[ws]}</span>
    <button className={`mb-icon ${sound ? "is-on" : ""}`} onClick={onSound} aria-pressed={sound} aria-label={sound ? "Звук тревог включён" : "Звук тревог выключен"}><Icon name={sound ? "sound" : "mute"} size={19} /></button>
    <button className="mb-avatar" onClick={onProfile} aria-label="Профиль и роль">{actor.trim() ? initials(actor) : <Icon name="user" size={18} />}</button>
  </header>;
}

/** Bottom sheet: who works on this phone, which role, what the system runs on. */
export function ProfileSheet({ open, onClose, role, roleTitle, onRole, actor, onActor, meta, source, server }: { open: boolean; onClose: () => void; role: Role; roleTitle: (role: Role) => string; onRole: (role: Role) => void; actor: string; onActor: (value: string) => void; meta?: Meta; source: string; server: string }) {
  const [shown, setShown] = useState(open);
  useEffect(() => { if (open) setShown(true); }, [open]);
  useEffect(() => { if (!open) return; const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); }; window.addEventListener("keydown", esc); return () => window.removeEventListener("keydown", esc); }, [open, onClose]);
  if (!shown) return null;
  return <div className={`mb-sheet-wrap ${open ? "is-open" : "is-closing"}`} onAnimationEnd={() => { if (!open) setShown(false); }}>
    <button className="mb-sheet-backdrop" aria-label="Закрыть" onClick={onClose} tabIndex={-1} />
    <section className="mb-sheet" role="dialog" aria-modal="true" aria-label="Профиль">
      <i className="mb-sheet-grip" aria-hidden />
      <div className="mb-profile">
        <span className="mb-profile-avatar">{actor.trim() ? initials(actor) : <Icon name="user" size={24} />}</span>
        <label className="mb-profile-name"><span>Сотрудник</span><input aria-label="Имя сотрудника" value={actor} maxLength={60} placeholder="Фамилия и имя" onChange={e => onActor(e.target.value)} /></label>
      </div>
      <h3 className="mb-sheet-h">Роль</h3>
      <div className="mb-roles" role="radiogroup" aria-label="Роль">
        {ROLES.map(id => <button key={id} role="radio" aria-checked={role === id} className={role === id ? "is-on" : ""} onClick={() => { onRole(id); onClose(); }}>
          <span>{meta?.roles.find(r => r.id === id)?.title ?? roleTitle(id)}</span>{role === id && <Icon name="check" size={18} />}
        </button>)}
      </div>
      <dl className="mb-sysinfo">
        <div><dt>Источник детекций</dt><dd>{source}</dd></div>
        <div><dt>Сервер</dt><dd>{server}</dd></div>
        <div><dt>Контракт</dt><dd className="mono">{meta?.contract ?? "—"}</dd></div>
      </dl>
      <button className="mb-sheet-close" onClick={onClose}>Готово</button>
    </section>
  </div>;
}
