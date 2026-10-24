import { PRODUCT } from "../brand";
import { createContext, useContext, useEffect, useRef, useState, type ReactNode } from "react";
import { Link, matchPath, NavLink, useLocation, useNavigate } from "react-router-dom";
import { api } from "../api/client";
import type { BackendStatus, Meta } from "../api/types";
import { useApi } from "../api/useApi";
import { useWs, type WsStatus } from "../api/ws";
import { FIXTURE_NOW } from "../fixtures/data";
import { isReviewMode, getReviewScenario } from "../fixtures/review";
import { menuFor, NAV } from "../nav";
import { latestPack, packLabel, packList } from "../demoPacks";
import { ROLES, useRole, type Role } from "../roles";
import { duration, Icon, ToastProvider, type IconName } from "./ui";
import { ActorIdentityProvider, useActorIdentity } from "./ActorIdentity";
import { hasPhoneApp, PhoneTabs, PhoneTop, ProfileSheet } from "./PhoneChrome";
import { usePhone } from "./usePhone";
import { OfflineScreen } from "./OfflineScreen";
import { askNotifications, systemNotify } from "../pwa";

function navIcon(path: string): IconName {
  if (path === "/operator") return "monitor";
  if (path.startsWith("/master/shift")) return "clock";
  if (path.startsWith("/master")) return "inbox";
  if (path.startsWith("/ohs/journal")) return "journal";
  if (path.startsWith("/ohs/report")) return "file";
  if (path.startsWith("/ohs/rules")) return "rules";
  if (path.startsWith("/ohs/stats") || path.startsWith("/management")) return "chart";
  if (path.startsWith("/admin/cameras")) return "camera";
  if (path.startsWith("/admin/system")) return "server";
  if (path.startsWith("/admin/demo")) return "play";
  if (path.startsWith("/calculator")) return "calculator";
  if (path.startsWith("/ohs/dataset")) return "database";
  if (path.startsWith("/ohs/people")) return "users";
  return "settings";
}
const ROLE_ICON: Record<Role, IconName> = { operator: "monitor", master: "user", ohs: "shield", management: "chart", admin: "settings" };

const MetaContext = createContext<Meta | undefined>(undefined);
const UpdateContext = createContext(0);
export function useMeta() { return useContext(MetaContext); }
export function useUpdates() { return useContext(UpdateContext); }
export const roleTitles: Record<Role, string> = { operator: "Оператор", master: "Мастер", ohs: "Охрана труда", management: "Руководство", admin: "Администратор" };

const mskFormat = new Intl.DateTimeFormat("ru-RU", { hour: "2-digit", minute: "2-digit", second: "2-digit", timeZone: "Europe/Moscow" });
const mskDate = new Intl.DateTimeFormat("ru-RU", { day: "2-digit", month: "short", timeZone: "Europe/Moscow" });
function useNow() {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => { const timer = setInterval(() => setNow(Date.now()), 1000); return () => clearInterval(timer); }, []);
  return now;
}
function Clock({ reference }: { reference?: string }) {
  const now = useNow();
  const shown = reference ? new Date(reference) : new Date(now);
  return <time className="shell-clock ds-clock" title={reference ? "Время проверочного сценария" : "Московское время"}><span className="ds-clock-date">{mskDate.format(shown)}</span><span className="ds-clock-time">{mskFormat.format(shown)}</span><small>{reference ? "МСК · сценарий" : "МСК"}</small></time>;
}

/** Product mark: an aperture-eye (Argus, the many-eyed watchman). */
function BrandMark() {
  return <svg className="ds-brand-mark" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
    <path d="M2 12c2.6-4.6 6-7 10-7s7.4 2.4 10 7c-2.6 4.6-6 7-10 7s-7.4-2.4-10-7Z" fill="none" stroke="currentColor" strokeWidth="1.6" />
    <circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" strokeWidth="1.6" />
    <path d="M12 7.8v2.4M15.6 9.9l-2.1 1.2M15.6 14.1l-2.1-1.2M12 16.2v-2.4M8.4 14.1l2.1-1.2M8.4 9.9l2.1 1.2" stroke="currentColor" strokeWidth="1.2" />
  </svg>;
}

const SOUND_KEY = "safewatch.sound";
function loadSound() { try { return localStorage.getItem(SOUND_KEY) === "1"; } catch { return false; } }
/** Short alert tone through WebAudio; the toggle click is the user gesture that unlocks audio. */
function useAlertSound() {
  const [on, setOn] = useState(loadSound);
  const ctx = useRef<AudioContext>();
  const toggle = () => {
    const next = !on; setOn(next);
    try { localStorage.setItem(SOUND_KEY, next ? "1" : "0"); } catch { /* storage blocked: the choice lives until reload */ }
    if (next && typeof AudioContext !== "undefined") { ctx.current = ctx.current ?? new AudioContext(); void ctx.current.resume(); }
    // The same tap allows system notifications: on a phone they carry the sound and vibration when the app is in the background.
    if (next) void askNotifications();
  };
  // A relaunched app (standalone) keeps «sound on» but the browser starts audio suspended: the first tap anywhere unlocks it.
  useEffect(() => {
    if (!on || typeof AudioContext === "undefined") return;
    const unlock = () => { ctx.current = ctx.current ?? new AudioContext(); void ctx.current.resume(); };
    window.addEventListener("pointerdown", unlock, { once: true });
    return () => window.removeEventListener("pointerdown", unlock);
  }, [on]);
  const beep = (kind: "siren" | "chime" | "none") => {
    if (!on || kind === "none" || typeof AudioContext === "undefined") return;
    const audio = ctx.current = ctx.current ?? new AudioContext();
    const tones = kind === "siren" ? [880, 660, 880] : [660];
    tones.forEach((frequency, i) => {
      const osc = audio.createOscillator(); const gain = audio.createGain(); const at = audio.currentTime + i * .18;
      osc.frequency.value = frequency; osc.connect(gain); gain.connect(audio.destination);
      gain.gain.setValueAtTime(.06, at); gain.gain.exponentialRampToValueAtTime(.001, at + .16); osc.start(at); osc.stop(at + .17);
    });
  };
  return { on, toggle, beep };
}

const WS_TEXT: Record<WsStatus, string> = { connected: "Канал событий: в сети", fixture: "Канал событий: повтор сценария", disconnected: "Канал событий: нет связи", connecting: "Канал событий: подключение…" };
const WS_SHORT: Record<WsStatus, string> = { connected: "В сети", fixture: "Повтор", disconnected: "Нет связи", connecting: "Подключение…" };
const BACKEND_STATE: Record<BackendStatus["state"], string> = { ok: "отвечает", models_missing: "нет моделей", unreachable: "недоступен", bad_answer: "ошибка ответа", unchecked: "не проверен" };

interface Alarm { eventId: number; text: string; received: number; collapsed: boolean }
/** Pinned red alarm under the top bar: level, place, reason, elapsed time; siren repeats while it is open. */
function AlarmBar({ alarm, siren, onOpen, onCollapse }: { alarm: Alarm; siren?: () => void; onOpen: () => void; onCollapse: () => void }) {
  const detail = useApi(() => api.GET("/api/events/{event_id}", { params: { path: { event_id: alarm.eventId } } }), [alarm.eventId]);
  const event = detail.data?.event;
  const now = useNow();
  const sirenRef = useRef(siren); sirenRef.current = siren;
  useEffect(() => { const timer = setInterval(() => sirenRef.current?.(), 2400); return () => clearInterval(timer); }, [alarm.eventId]);
  const since = event ? Date.parse(event.started_at) : alarm.received;
  const level = useMeta()?.levels.find(item => item.id === "red")?.title ?? "Красная опасность";
  return <div className="ds-alarm-bar" role="alert" aria-label={`Тревога, событие ${alarm.eventId}`}>
    <span className="ds-alarm-level"><Icon name="critical" size={16} />{level}</span>
    <span className="ds-alarm-what">
      <strong>{event?.title ?? alarm.text}</strong>
      <span>{event ? `${event.sector_name} · ${event.camera_name} · ${event.reason_text}` : alarm.text}</span>
    </span>
    <span className="ds-alarm-timer mono" title="Прошло с начала события">{duration(now - since)}</span>
    <button className="ds-btn ds-btn-sm ds-alarm-open" onClick={onOpen}>Открыть<Icon name="arrow" size={14} /></button>
    <button className="ds-btn ds-btn-sm ds-btn-ghost ds-alarm-collapse" onClick={onCollapse}>Свернуть</button>
  </div>;
}

export function AppShell({ children }: { children: ReactNode }) {
  return <ActorIdentityProvider><ToastProvider><ShellContent>{children}</ShellContent></ToastProvider></ActorIdentityProvider>;
}
function ShellContent({ children }: { children: ReactNode }) {
  const [role, setRole] = useRole();
  const location = useLocation();
  const navigate = useNavigate();
  const review = isReviewMode();
  // A deep link switches the role only when the current role cannot open that route (NAV roles), e.g. ohs stays ohs on /admin/cameras/:id.
  useEffect(() => {
    const route = NAV.find(item => matchPath({ path: item.path, end: true }, location.pathname));
    if (route && !route.roles.includes(role)) setRole(route.roles[0]);
  }, [location.pathname, role, setRole]);
  const meta = useApi(() => api.GET("/api/meta"), [role]).data;
  // No route (mock, older backend) or no pack: the header simply shows no pack chip.
  const packs = useApi(() => review ? Promise.resolve({ data: [] }) : api.GET("/api/demo/packs"), [role, review]).data;
  const pack = latestPack(packs);
  const [updates, setUpdates] = useState(0);
  const [notification, setNotification] = useState<string>();
  const [alarm, setAlarm] = useState<Alarm>();
  const dismissedAlarms = useRef(new Set<number>());
  const closeAlarm = () => { if (alarm) dismissedAlarms.current.add(alarm.eventId); setAlarm(undefined); };
  const [serverOffset, setServerOffset] = useState<number>();
  const [backendStatus, setBackendStatus] = useState<BackendStatus>();
  const sound = useAlertSound();
  // On a phone the operator and the master get an app: own top bar, bottom tabs, profile sheet instead of the rail.
  const phoneApp = (usePhone() || location.pathname.startsWith("/m/")) && hasPhoneApp(role);
  const [profile, setProfile] = useState(false);
  const ws = useWs(message => {
    if (message.type === "hello") setServerOffset(Date.parse(message.data.server_now) - Date.now());
    if (message.type === "backend.status") setBackendStatus(message.data);
    if (message.type === "hello" || message.type.startsWith("event.") || message.type === "sector.state" || message.type === "camera.state" || message.type === "broadcast.state") setUpdates(n => n + 1);
    if (message.type === "notification" && message.data.audience.includes(role)) {
      const n = message.data;
      if (phoneApp) navigator.vibrate?.(n.level === "red" ? [300, 120, 300] : 150);
      // System notification (sound and vibration of the phone even with the app in the background): a new red for the operator, a hand-over for the master.
      if (phoneApp || document.hidden) {
        if (role === "operator" && n.level === "red") void systemNotify(`${PRODUCT}: красная тревога`, n.text, { tag: `event-${n.event_id}`, url: phoneApp ? `/m/operator/events/${n.event_id}` : `/events/${n.event_id}`, urgent: true });
        if (role === "master" && n.id.endsWith(":to_master")) void systemNotify(`${PRODUCT}: новое поручение`, n.text, { tag: `event-${n.event_id}`, url: `/master/events/${n.event_id}`, urgent: n.level === "red" });
      }
      // tech.md 8.24: the master's inbox opens the card handed over to him by itself.
      if (role === "master" && n.id.endsWith(":to_master") && location.pathname === "/master") { sound.beep(n.sound); navigate(`/master/events/${n.event_id}`); return; }
      // The operator is already in front of another red takeover: the new red does not yank him away, it waits in the bar (pill on the phone) and the queue.
      const busy = role === "operator" && new URLSearchParams(location.search).get("takeover") === "1" && /\/events\/\d+$/.test(location.pathname) && !location.pathname.endsWith(`/events/${n.event_id}`);
      if (busy && n.takeover && n.level === "red") {
        if (alarm?.eventId === n.event_id || dismissedAlarms.current.has(n.event_id)) return;
        sound.beep(n.sound);
        setAlarm({ eventId: n.event_id, text: n.text, received: Date.now(), collapsed: phoneApp });
        return;
      }
      if (role === "operator" && n.takeover && n.level === "red" && location.pathname.startsWith("/m/operator")) { sound.beep(n.sound); navigate(`/m/operator/events/${n.event_id}?takeover=1`); return; }
      if (role === "operator" && n.takeover && n.level === "red") {
        // tech.md 8.8: a red notification takes over the dispatcher and an open event card; sector and camera views get the bar.
        if (location.pathname === "/operator" || location.pathname.startsWith("/events/") || (phoneApp && location.pathname.startsWith("/operator"))) { sound.beep(n.sound); navigate(`/events/${n.event_id}?takeover=1`); return; }
        if (location.pathname === `/events/${n.event_id}` || alarm?.eventId === n.event_id || dismissedAlarms.current.has(n.event_id)) return;
        sound.beep(n.sound);
        setAlarm({ eventId: n.event_id, text: n.text, received: Date.now(), collapsed: false });
        return;
      }
      sound.beep(n.sound);
      setNotification(n.text);
    }
  });
  const wsStatus = ws.status;
  const [healthTick, setHealthTick] = useState(0);
  const health = useApi(() => review ? Promise.resolve({ data: undefined }) : api.GET("/api/health"), [healthTick, review]);
  // No answer from the server (or no network at all): the screen shows no data rather than stale alarms.
  const [serverDown, setServerDown] = useState(false);
  const [browserOnline, setBrowserOnline] = useState(() => typeof navigator === "undefined" || navigator.onLine !== false);
  useEffect(() => { if (health.data) setServerDown(false); else if (health.error) setServerDown(health.error.code === "network"); }, [health.data, health.error]);
  useEffect(() => {
    const sync = () => { setBrowserOnline(navigator.onLine !== false); setHealthTick(n => n + 1); };
    window.addEventListener("online", sync); window.addEventListener("offline", sync);
    return () => { window.removeEventListener("online", sync); window.removeEventListener("offline", sync); };
  }, []);
  const offline = !review && (serverDown || !browserOnline);
  useEffect(() => { if (review) return; const timer = setInterval(() => setHealthTick(n => n + 1), offline ? 5000 : 15000); return () => clearInterval(timer); }, [review, offline]);
  const scenarioTitle: Record<string, string> = { critical: "Критическое событие", normal: "Без активных тревог", error: "Ошибка API", empty: "Пустые данные", offline: "Нет сети", notimplemented: "Метод не реализован", disconnected: "Канал событий отключён" };
  const { actor, setActor } = useActorIdentity();
  const changeRole = (next: Role) => {
    setRole(next);
    const match = location.pathname.match(/\/(?:events|master\/events)\/(\d+)/);
    navigate(match && next === "master" ? `/master/events/${match[1]}` : match && next === "operator" ? `/events/${match[1]}` : menuFor(next)[0]?.path ?? "/operator");
  };
  const synthetic = Boolean(meta?.fake || review);
  const source = review ? "Проверочный сценарий" : meta?.fake ? "Демо · синтетические детекции" : meta ? meta.inference_backend === "linq" ? "LinQ TPU" : "CPU · local" : "Источник не получен";
  const backendTitle = meta ? meta.inference_backend === "linq" ? "LinQ TPU" : "CPU · local" : "—";
  const now = useNow();
  const serverOnline = review ? undefined : health.data ? true : health.error ? false : undefined;
  const home = menuFor(role)[0]?.path ?? "/operator";
  return <MetaContext.Provider value={meta}><UpdateContext.Provider value={updates}>
    <div className={`app app-cr ds-app ${role === "master" ? "is-master" : ""} ${phoneApp ? "is-phone-app" : ""}`}>
      <a className="skip-link" href="#workspace">Перейти к содержимому</a>
      {phoneApp ? <PhoneTop brand={<><BrandMark /><span>{PRODUCT}</span></>} home={home} ws={wsStatus} sound={sound.on} onSound={sound.toggle} actor={actor} onProfile={() => setProfile(true)}
        alarm={alarm?.collapsed && role === "operator" ? <button className="mb-alarm-pill" onClick={() => setAlarm({ ...alarm, collapsed: false })}><Icon name="critical" size={14} />#{alarm.eventId}</button> : undefined} />
      : <header className="shell-header cr-top ds-topbar">
        <Link className="brand ds-brand" to={home} aria-label={PRODUCT}><BrandMark /><span>{PRODUCT}</span></Link>
        <nav className="cr-roles ds-roles" aria-label="Выбор роли">{ROLES.map(id => <button key={id} onClick={() => changeRole(id)} className={role === id ? "active" : ""} aria-current={role === id ? "page" : undefined}><Icon name={ROLE_ICON[id]} size={15} />{roleTitles[id]}</button>)}</nav>
        <div className="cr-top-right ds-top-right">
          {alarm?.collapsed && role === "operator" && <button className="ds-alarm-pill" onClick={() => setAlarm({ ...alarm, collapsed: false })} title="Показать тревогу"><Icon name="critical" size={14} />Тревога #{alarm.eventId}</button>}
          <span className={`cr-source ds-source ${synthetic ? "is-synthetic" : ""}`} data-testid="backend" title="Источник детекций">{source}</span>
          {pack && <span className={`cr-source ds-source ds-pack ${pack.fake ? "is-synthetic" : ""}`} data-testid="demo-pack" title={packList(packs).map(packLabel).join(" · ")}>{packLabel(pack)}{packList(packs).length > 1 ? ` +${packList(packs).length - 1}` : ""}</span>}
          <span className="connection cr-live ds-live" data-status={wsStatus} title={WS_TEXT[wsStatus]}><i />{WS_SHORT[wsStatus]}</span>
          <button className={`ds-icon-btn ds-btn-ghost ds-sound ${sound.on ? "is-on" : ""}`} onClick={sound.toggle} aria-pressed={sound.on} aria-label={sound.on ? "Звук тревог включён" : "Звук тревог выключен"} title={sound.on ? "Звук тревог включён" : "Звук тревог выключен"}><Icon name={sound.on ? "sound" : "mute"} size={16} /></button>
          <label className="actor-field cr-actor ds-actor"><Icon name="user" size={14} /><span className="sr-only">Сотрудник</span><input aria-label="Имя сотрудника" value={actor} maxLength={60} placeholder="Указать имя" onChange={e => setActor(e.target.value)} /></label>
          <Clock reference={review ? FIXTURE_NOW : undefined} />
        </div>
      </header>}
      {!phoneApp && <aside className="cr-rail ds-rail">
        <nav className="workspace-nav cr-nav ds-nav" aria-label="Разделы">{menuFor(role).map(item => <NavLink key={item.path} to={item.path} end title={item.title}><Icon name={navIcon(item.path)} size={18} /><span>{item.title}</span></NavLink>)}</nav>
        <label className="mobile-role cr-role"><span><Icon name="user" size={16} />Роль</span><select aria-label="Роль" value={role} onChange={e => changeRole(e.target.value as Role)}>{ROLES.map(id => <option key={id} value={id}>{meta?.roles.find(r => r.id === id)?.title ?? roleTitles[id]}</option>)}</select></label>
      </aside>}
      <div className="cr-body ds-body">
        {review && <div className="review-strip"><span className="review-square" />Проверочный сценарий · {scenarioTitle[getReviewScenario()] ?? "Проверка интерфейса"} · изображения созданы для проверки интерфейса</div>}
        {!review && !offline && wsStatus === "disconnected" && <div className="offline-strip" role="status"><Icon name="wifi-off" size={15} />Нет связи с каналом событий. Данные на экране могут быть устаревшими — нажмите «Обновить».</div>}
        {!offline && alarm && !alarm.collapsed && role === "operator" && location.pathname !== `/events/${alarm.eventId}` && <AlarmBar alarm={alarm} siren={sound.on ? () => sound.beep("siren") : undefined} onOpen={() => { const id = alarm.eventId; closeAlarm(); navigate(`/events/${id}`); }} onCollapse={() => setAlarm({ ...alarm, collapsed: true })} />}
        {!offline && notification && <div className="notification-strip" role="status"><Icon name="bell" size={15} /><span>{notification}</span><button aria-label="Закрыть уведомление" onClick={() => setNotification(undefined)}><Icon name="cross" size={14} /></button></div>}
        {offline ? <OfflineScreen network={browserOnline} onRetry={() => setHealthTick(n => n + 1)} /> : <main key={role} id="workspace" className="shell-main">{children}</main>}
      </div>
      {!phoneApp && <footer className="ds-statusbar" aria-label="Состояние системы">
        <span className={`ds-sb-item ${serverOnline === false ? "is-bad" : serverOnline ? "is-ok" : ""}`}><Icon name="server" size={13} />Сервер: {serverOnline === undefined ? review ? "проверочный режим" : "проверка…" : serverOnline ? "на связи" : "нет ответа"}</span>
        <span className={`ds-sb-item ${wsStatus === "connected" ? "is-ok" : wsStatus === "disconnected" ? "is-warn" : ""}`}><Icon name={wsStatus === "disconnected" ? "wifi-off" : "wifi"} size={13} />{WS_TEXT[wsStatus]}</span>
        <span className="ds-sb-item"><Icon name="cpu" size={13} />Инференс: {backendTitle}{meta?.fake ? " · фейк-режим" : ""}{backendStatus && !meta?.fake ? ` · ${BACKEND_STATE[backendStatus.state]}${backendStatus.latency_ms !== null ? ` · ${Math.round(backendStatus.latency_ms)} мс` : ""}` : ""}</span>
        {synthetic && <span className="ds-sb-item is-demo"><Icon name="info" size={13} />{review ? "Проверочные данные" : "Демо-данные: синтетические детекции"}</span>}
        <span className="ds-sb-spacer" />
        <span className="ds-sb-item" title="Время сервера по сообщению hello канала событий"><Icon name="clock" size={13} />Сервер <span className="mono">{serverOffset === undefined ? "—" : mskFormat.format(new Date(now + serverOffset))}</span></span>
        <span className="ds-sb-item">Контракт <span className="mono">{health.data?.contract ?? meta?.contract ?? "—"}</span></span>
        <span className="ds-sb-item">{PRODUCT} · {meta?.roles.find(r => r.id === role)?.title ?? roleTitles[role]}</span>
      </footer>}
      {phoneApp && <PhoneTabs role={role} updates={updates} />}
      {phoneApp && <ProfileSheet open={profile} onClose={() => setProfile(false)} role={role} roleTitle={id => roleTitles[id]} onRole={changeRole} actor={actor} onActor={setActor} meta={meta} source={source}
        server={serverOnline === undefined ? review ? "проверочный режим" : "проверка…" : serverOnline ? "на связи" : "нет ответа"} />}
      {role === "master" && !phoneApp && <nav className="mobile-bottom-nav" aria-label="Рабочее место мастера"><NavLink to="/master" end><Icon name="list" />Поручения</NavLink><NavLink to="/master/shift"><Icon name="grid" />Моя смена</NavLink></nav>}
    </div>
  </UpdateContext.Provider></MetaContext.Provider>;
}
