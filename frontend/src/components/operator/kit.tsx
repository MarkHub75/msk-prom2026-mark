import { useEffect, useLayoutEffect, useState, type ReactNode, type RefObject } from "react";
import { useLevelTitle } from "../ops/levels";
import { createPortal } from "react-dom";
import { CircleCheck, EyeOff, OctagonAlert, TriangleAlert } from "lucide-react";
import type { Calibration, CameraState, Episode, Meta, Zone } from "../../api/types";

const ICON = { size: 15, strokeWidth: 1.75 } as const;
type State = CameraState["state"];
export const STATE_TITLE: Record<State, string> = { red: "Тревога", yellow: "Внимание", normal: "Норма", no_observation: "Нет наблюдения" };

/** State is always text + icon, never color alone (tech.md 8.14). */
export function StateIcon({ state, size = 15 }: { state: State; size?: number }) {
  const props = { ...ICON, size, "aria-hidden": true };
  return state === "red" ? <OctagonAlert {...props} /> : state === "yellow" ? <TriangleAlert {...props} /> : state === "normal" ? <CircleCheck {...props} /> : <EyeOff {...props} />;
}
export function StateBadge({ state, text }: { state: State; text?: string }) {
  const levelTitle = useLevelTitle();
  return <span className={`od-state od-state-${state}`}><StateIcon state={state} />{text ?? (state === "red" || state === "yellow" ? levelTitle(state) : STATE_TITLE[state])}</span>;
}
export function LevelTag({ level, title }: { level: "red" | "yellow"; title?: string }) {
  const levelTitle = useLevelTitle();
  return <span className={`od-level od-level-${level}`}><StateIcon state={level} size={14} />{title ?? levelTitle(level)}</span>;
}

export const END_REASON: Record<Episode["end_reason"], string> = { observed_exit: "Человек вышел из ситуации", track_lost_timeout: "Трек потерян, ожидание истекло", video_end: "Запись закончилась" };

/** Ticks every `ms` so timers ("ждёт 04:12") stay live without refetching. */
export function useNow(ms = 1000) {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => { const timer = setInterval(() => setNow(Date.now()), ms); return () => clearInterval(timer); }, [ms]);
  return now;
}
export function since(iso: string | null | undefined, now: number) {
  if (!iso) return "—";
  const s = Math.max(0, Math.floor((now - Date.parse(iso)) / 1000));
  if (s < 3600) return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
  const h = Math.floor(s / 3600);
  return h < 48 ? `${h} ч ${Math.floor((s % 3600) / 60)} мин` : `${Math.floor(h / 24)} дн`;
}

/** Renders children inside the first `selector` match under `host` (e.g. into the player's .video-frame). */
export function Into({ host, selector, deps, children }: { host: RefObject<HTMLElement>; selector: string; deps: unknown[]; children: ReactNode }) {
  const [target, setTarget] = useState<Element | null>(null);
  useLayoutEffect(() => {
    const find = () => setTarget(host.current?.querySelector(selector) ?? null);
    find();
    if (!host.current) return;
    const observer = new MutationObserver(find);
    observer.observe(host.current, { childList: true, subtree: true });
    return () => observer.disconnect();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  return target ? createPortal(children, target) : null;
}

/** Zones and the 1 m calibration grid in normalized frame coordinates, drawn over the frame. */
export function SceneOverlay({ zones, calibration, meta, showZones, showGrid }: { zones: Zone[]; calibration?: Calibration | null; meta?: Meta; showZones: boolean; showGrid: boolean }) {
  const color = (kind: string) => meta?.zone_kinds.find(k => k.id === kind)?.color ?? "#3BA7FF";
  return <>
    <svg className="od-scene" viewBox="0 0 1000 1000" preserveAspectRatio="none" aria-label="Зоны и сетка калибровки">
      {showGrid && calibration?.grid.map(([[x1, y1], [x2, y2]], i) => <line key={`g${i}`} className="od-grid" x1={x1 * 1000} y1={y1 * 1000} x2={x2 * 1000} y2={y2 * 1000} vectorEffect="non-scaling-stroke" />)}
      {showZones && zones.map(zone => zone.points.length === 2
        ? <line key={zone.id} className="od-zone-line" x1={zone.points[0][0] * 1000} y1={zone.points[0][1] * 1000} x2={zone.points[1][0] * 1000} y2={zone.points[1][1] * 1000} stroke={color(zone.kind)} vectorEffect="non-scaling-stroke" />
        : <polygon key={zone.id} className="od-zone" points={zone.points.map(([x, y]) => `${x * 1000},${y * 1000}`).join(" ")} stroke={color(zone.kind)} fill={color(zone.kind)} vectorEffect="non-scaling-stroke" />)}
    </svg>
    {showZones && <div className="od-zone-labels" aria-hidden="true">{zones.map(zone => { const x = Math.min(...zone.points.map(p => p[0])); const y = Math.min(...zone.points.map(p => p[1])); return <span key={zone.id} style={{ left: `${x * 100}%`, top: `${y * 100}%`, borderColor: color(zone.kind) }}>{zone.name}</span>; })}</div>}
  </>;
}
