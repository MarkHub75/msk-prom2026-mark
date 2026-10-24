import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { Link, NavLink, useLocation, useNavigate } from "react-router-dom";
import { api } from "../api/client";
import type { Meta } from "../api/types";
import { useApi } from "../api/useApi";
import { useWs } from "../api/ws";
import { FIXTURE_NOW } from "../fixtures/data";
import { isReviewMode, getReviewScenario } from "../fixtures/review";
import { menuFor } from "../nav";
import { ROLES, useRole, type Role } from "../roles";
import { Icon, type IconName } from "./ui";

function navIcon(path: string): IconName {
  if (path === "/operator") return "monitor";
  if (path.startsWith("/master/shift")) return "grid";
  if (path.startsWith("/master")) return "bell";
  if (path.startsWith("/ohs/journal")) return "journal";
  if (path.startsWith("/ohs/rules")) return "rules";
  if (path.startsWith("/ohs/stats") || path.startsWith("/management")) return "chart";
  if (path.startsWith("/admin/cameras")) return "camera";
  return "settings";
}
import { ActorIdentityProvider, useActorIdentity } from "./ActorIdentity";

const MetaContext = createContext<Meta | undefined>(undefined);
const UpdateContext = createContext(0);
export function useMeta() { return useContext(MetaContext); }
export function useUpdates() { return useContext(UpdateContext); }
export const roleTitles: Record<Role, string> = { operator: "Оператор", master: "Мастер", ohs: "Охрана труда", management: "Руководство", admin: "Администратор" };
function Clock({reference}:{reference?:string}) {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => { const timer = setInterval(() => setNow(new Date()), 1000); return () => clearInterval(timer); }, []);
  const shown = reference ? new Date(reference) : now;
  return <time className="shell-clock">{new Intl.DateTimeFormat("ru-RU", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit", second: "2-digit", timeZone: "Europe/Moscow" }).format(shown)}<small>{reference?"МСК · время сценария":"МСК"}</small></time>;
}
export function AppShell({ children }: { children: ReactNode }) {
  return <ActorIdentityProvider><ShellContent>{children}</ShellContent></ActorIdentityProvider>;
}
function ShellContent({ children }: { children: ReactNode }) {
  const [role, setRole] = useRole();
  const location = useLocation();
  const navigate = useNavigate();
  const review = isReviewMode();
  useEffect(() => { const routeRole = location.pathname.split("/")[1]; if(ROLES.includes(routeRole as Role) && role !== routeRole) setRole(routeRole as Role); }, [location.pathname,role,setRole]);
  const meta = useApi(() => api.GET("/api/meta"), [role]).data;
  const [updates, setUpdates] = useState(0);
  const [notification, setNotification] = useState<string>();
  const ws = useWs(message => {
    if (message.type === "hello" || message.type.startsWith("event.") || message.type === "sector.state" || message.type === "camera.state" || message.type === "broadcast.state") setUpdates(n => n + 1);
    if (message.type === "notification" && message.data.audience.includes(role)) {
      setNotification(message.data.text);
      if(role === "operator" && message.data.takeover && message.data.level === "red") navigate(`/events/${message.data.event_id}?takeover=1`);
    }
  });
  const wsStatus = ws.status;
  const scenarioTitle: Record<string,string> = {critical:"Критическое событие",normal:"Без активных тревог",error:"Ошибка API",empty:"Пустые данные",offline:"Нет сети",notimplemented:"Метод не реализован",disconnected:"Канал событий отключён"};
  const { actor, setActor } = useActorIdentity();
  const changeRole = (next: Role) => {
    setRole(next);
    const match = location.pathname.match(/\/(?:events|master\/events)\/(\d+)/);
    navigate(match && next === "master" ? `/master/events/${match[1]}` : match && next === "operator" ? `/events/${match[1]}` : menuFor(next)[0]?.path ?? "/operator");
  };
  const actorChange = (value: string) => setActor(value);
  const source = review ? "Проверочный сценарий" : meta?.fake ? "Демо · синтетические детекции" : meta ? meta.inference_backend === "linq" ? "LinQ TPU" : "CPU · local" : "Источник не получен";
  const live = wsStatus === "connected" ? "В сети" : wsStatus === "fixture" ? "Повтор" : wsStatus === "disconnected" ? "Нет связи" : "Подключение…";
  return <MetaContext.Provider value={meta}><UpdateContext.Provider value={updates}>
    <div className={`app app-cr ${role === "master" ? "is-master" : ""}`}>
      <a className="skip-link" href="#workspace">Перейти к содержимому</a>
      <aside className="cr-rail">
        <Link className="cr-logo" to={menuFor(role)[0]?.path ?? "/operator"} aria-label="SafeWatch"><span className="brand-mark" /></Link>
        <nav className="workspace-nav cr-nav" aria-label="Разделы">{menuFor(role).map(item => <NavLink key={item.path} to={item.path} end title={item.title}><Icon name={navIcon(item.path)} size={20} /><span>{item.title}</span></NavLink>)}</nav>
        <label className="mobile-role cr-role"><span><Icon name="user" size={16} />Роль</span><select aria-label="Роль" value={role} onChange={e => changeRole(e.target.value as Role)}>{ROLES.map(id => <option key={id} value={id}>{meta?.roles.find(r => r.id === id)?.title ?? roleTitles[id]}</option>)}</select></label>
      </aside>
      <div className="cr-body">
        <header className="shell-header cr-top">
          <Link className="brand" to={menuFor(role)[0]?.path ?? "/operator"}>SafeWatch</Link>
          <span className="cr-plant">{roleTitles[role]}</span>
          <div className="cr-top-right">
            <span className={`cr-source ${meta?.fake || review ? "is-synthetic" : ""}`} data-testid="backend">{source}</span>
            <span className="connection cr-live" data-status={wsStatus} title="Канал событий"><i />{live}</span>
            <label className="actor-field cr-actor"><span>Сотрудник</span><input aria-label="Имя сотрудника" value={actor} maxLength={60} placeholder="Указать имя" onChange={e => actorChange(e.target.value)} /></label>
            <Clock reference={review?FIXTURE_NOW:undefined} />
          </div>
        </header>
        {review && <div className="review-strip"><span className="review-square" />Проверочный сценарий · {scenarioTitle[getReviewScenario()] ?? "Проверка интерфейса"} · изображения созданы для проверки интерфейса</div>}
        {!review && wsStatus === "disconnected" && <div className="offline-strip" role="status">Нет связи с каналом событий. Данные на экране могут быть устаревшими — нажмите «Обновить».</div>}
        {notification && <div className="notification-strip" role="status"><span>{notification}</span><button aria-label="Закрыть уведомление" onClick={()=>setNotification(undefined)}><Icon name="cross" size={14} /></button></div>}
        <main key={role} id="workspace" className="shell-main">{children}</main>
      </div>
      {role === "master" && <nav className="mobile-bottom-nav" aria-label="Рабочее место мастера"><NavLink to="/master" end><Icon name="list" />Поручения</NavLink><NavLink to="/master/shift"><Icon name="grid" />Моя смена</NavLink></nav>}
    </div>
  </UpdateContext.Provider></MetaContext.Provider>;
}
