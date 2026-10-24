import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { NavLink } from "react-router-dom";
import { api } from "../api/client";
import type { components } from "../api/schema";
import { useApi } from "../api/useApi";
import { useWs } from "../api/ws";
import { menuFor } from "../nav";
import { useRole } from "../roles";
import { RoleSwitcher } from "./RoleSwitcher";
import { soundBlocked, unlockSound } from "./sound";
import { TakeoverOverlay } from "./TakeoverOverlay";
import { Toasts } from "./Toasts";

type Meta = components["schemas"]["Meta"];
type BackendStatus = components["schemas"]["BackendStatus"];

const MetaContext = createContext<Meta | undefined>(undefined);

export function useMeta(): Meta | undefined {
  return useContext(MetaContext);
}

function backendLabel(meta: Meta | undefined): string {
  if (!meta) return "нет данных";
  if (meta.fake) return "Фейк: детекции синтетические";
  return meta.inference_backend === "linq" ? "LinQ TPU" : "CPU (local)";
}

function Clock({ timezone }: { timezone: string }) {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);
  const time = new Intl.DateTimeFormat("ru-RU", { timeZone: timezone, timeStyle: "medium" });
  return <span>{time.format(now)} МСК</span>;
}

export function AppShell({ children }: { children: ReactNode }) {
  const [role] = useRole();
  const meta = useApi(() => api.GET("/api/meta"), []).data;
  const [backend, setBackend] = useState<BackendStatus>();
  const [muted, setMuted] = useState(soundBlocked);
  useWs((message) => {
    if (message.type === "backend.status") setBackend(message.data as BackendStatus);
  });
  return (
    <MetaContext.Provider value={meta}>
      <header className="shell-header">
        <strong>{meta?.product_name ?? "SafeWatch"}</strong>
        <nav aria-label="Навигация">
          {menuFor(role).map((item) => (
            <NavLink key={item.path} to={item.path}>
              {item.title}
            </NavLink>
          ))}
        </nav>
        <span className="badge" data-testid="backend">
          {backendLabel(meta)}
        </span>
        {backend && (
          <span className="badge" data-testid="backend-state" title={backend.message}>
            {backend.state === "ok" ? "● " : "▲ "}
            {backend.message}
          </span>
        )}
        <Clock timezone={meta?.timezone ?? "Europe/Moscow"} />
        {muted && (
          <button
            type="button"
            onClick={() => {
              unlockSound();
              setMuted(false);
            }}
          >
            Включить звук
          </button>
        )}
        <RoleSwitcher />
      </header>
      <main className="shell-main">{children}</main>
      <Toasts />
      {role === "operator" && <TakeoverOverlay />}
    </MetaContext.Provider>
  );
}
