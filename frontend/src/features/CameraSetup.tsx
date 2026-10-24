import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import { ChevronRight, ClipboardCheck, Cpu, Crosshair, Film, ListChecks, Radio, Shapes } from "lucide-react";
import { api } from "../api/client";
import type { Broadcast, CameraState, Job } from "../api/types";
import { useApi } from "../api/useApi";
import { useWs } from "../api/ws";
import { useMeta } from "../components/AppShell";
import { ErrorNotice, Loading } from "../components/ui";
import { StateBadge } from "../components/admin/AdminUi";
import { useRole } from "../roles";
import { VideoTab } from "./camera-setup/VideoTab";
import { BroadcastTab } from "./camera-setup/BroadcastTab";
import { CalibrationTab } from "./camera-setup/CalibrationTab";
import { ZonesTab } from "./camera-setup/ZonesTab";
import { CameraRulesTab } from "./camera-setup/CameraRulesTab";
import { PassportTab } from "./camera-setup/PassportTab";
import "../styles/admin.css";

const I = { size: 15, strokeWidth: 1.75 } as const;
const TABS = [
  { id: "video", title: "Видео", icon: <Film {...I} /> },
  { id: "broadcast", title: "Эфир", icon: <Radio {...I} /> },
  { id: "calibration", title: "Калибровка", icon: <Crosshair {...I} /> },
  { id: "zones", title: "Зоны", icon: <Shapes {...I} /> },
  { id: "rules", title: "Правила", icon: <ListChecks {...I} /> },
  { id: "passport", title: "Пригодность", icon: <ClipboardCheck {...I} /> },
] as const;
type TabId = typeof TABS[number]["id"];

export function CameraSetupPage() {
  const cameraId = Number(useParams().cameraId);
  const [role] = useRole();
  const meta = useMeta();
  const [params, setParams] = useSearchParams();
  const tab: TabId = TABS.find((t) => t.id === params.get("tab"))?.id ?? "video";
  const setup = useApi(() => api.GET("/api/admin/cameras/{camera_id}", { params: { path: { camera_id: cameraId } } }), [cameraId]);
  // A reload keeps the previous snapshot on screen: the tabs, the player and the upload note stay mounted.
  const last = useRef(setup.data);
  if (setup.data) last.current = setup.data;
  if (last.current && last.current.camera.id !== cameraId) last.current = undefined;
  const camView = useApi(() => api.GET("/api/cameras/{camera_id}/view", { params: { path: { camera_id: cameraId } } }), [cameraId]);
  const sectors = useApi(() => api.GET("/api/sectors"), []);
  const [jobs, setJobs] = useState<Record<number, Job>>({});
  const [state, setState] = useState<CameraState>();
  const [broadcast, setBroadcast] = useState<Broadcast | null>();
  useEffect(() => { setJobs({}); setState(undefined); setBroadcast(undefined); }, [cameraId]);
  const reload = setup.reload;
  const reloadView = camView.reload;

  useWs(useCallback((m) => {
    if (m.type === "job.progress" && m.data.camera_id === cameraId) {
      setJobs((all) => ({ ...all, [m.data.id]: m.data }));
      if (m.data.status === "done" || m.data.status === "failed") { reload(); reloadView(); }
    }
    if (m.type === "camera.state" && m.data.camera_id === cameraId) setState(m.data);
    if (m.type === "broadcast.state" && m.data.camera_id === cameraId) setBroadcast(m.data);
  }, [cameraId, reload, reloadView]));

  const refresh = useCallback(() => { setBroadcast(undefined); setJobs({}); reload(); reloadView(); }, [reload, reloadView]);
  const pick = (id: TabId) => setParams((p) => { p.set("tab", id); return p; }, { replace: true });

  const back = role === "admin" ? <Link to="/admin/cameras">Камеры и секторы</Link> : <Link to="/ohs/rules">Правила наблюдения</Link>;
  if (!Number.isInteger(cameraId) || cameraId <= 0) return <ErrorNotice error={{ code: "not_found", message: "В адресе нет номера камеры" }} />;
  if (setup.error && !last.current) return <div className="adm-page"><nav className="adm-crumbs">{back}</nav><ErrorNotice error={setup.error} retry={setup.reload} /></div>;
  if (!last.current) return <div className="adm-page"><nav className="adm-crumbs">{back}</nav><Loading text="Загружаем настройки камеры" /></div>;

  const data = last.current;
  const camera = data.camera;
  const liveState = state ?? camView.data?.state;
  const liveBroadcast = broadcast !== undefined ? broadcast : (camView.data?.broadcast ?? data.broadcast);
  // WS progress overrides the REST snapshot until the next reload clears it.
  const merged = data.jobs.map((j) => jobs[j.id] ?? j);
  for (const j of Object.values(jobs)) if (!merged.some((m) => m.id === j.id)) merged.unshift(j);
  const sector = sectors.data?.find((s) => s.id === camera.sector_id);
  const backend = meta ? `${meta.inference_backend === "linq" ? "LinQ TPU" : "Локально, CPU"}${meta.fake ? " · фейк-режим" : ""}` : "—";

  const panels: Record<TabId, ReactNode> = {
    video: <VideoTab camera={camera} videos={data.videos} jobs={merged} onJob={(j) => setJobs((all) => ({ ...all, [j.id]: j }))} onChange={refresh} />,
    broadcast: <BroadcastTab camera={camera} videos={data.videos} broadcast={liveBroadcast ?? null} onChange={refresh} />,
    calibration: <CalibrationTab cameraId={cameraId} />,
    zones: <ZonesTab cameraId={cameraId} />,
    rules: <CameraRulesTab cameraId={cameraId} />,
    passport: <PassportTab cameraId={cameraId} />,
  };

  return <div className="adm-page adm-setup">
    <header className="adm-setup-head">
      <nav className="adm-crumbs" aria-label="Путь">{back}<ChevronRight size={13} strokeWidth={1.75} /><span>{sector?.name ?? `Сектор ${camera.sector_id}`}</span></nav>
      <div className="adm-setup-title">
        <h1>{camera.name}</h1>
        {camera.is_demo && <i className="adm-demo">демо</i>}
        {liveState ? <StateBadge state={liveState.state} reason={liveState.reason_text} /> : camView.error ? <span className="adm-muted">состояние недоступно</span> : null}
      </div>
      <dl className="adm-facts">
        <div><dt>Описание</dt><dd>{camera.description || "—"}</dd></div>
        <div><dt>Бэкенд инференса</dt><dd><Cpu {...I} />{backend}</dd></div>
        <div><dt>Эфир</dt><dd>{liveBroadcast?.status === "playing" ? <span className="adm-live"><Radio {...I} />идёт</span> : liveBroadcast ? "остановлен" : "не запущен"}</dd></div>
        <div><dt>Записей</dt><dd>{data.videos.length}</dd></div>
        <div><dt>Калибровка</dt><dd>{data.calibration ? "есть" : "нет"}</dd></div>
        <div><dt>Зон</dt><dd>{data.zones.length}</dd></div>
        <div><dt>Правил включено</dt><dd>{data.rules.filter((r) => r.enabled).length} из {data.rules.length}</dd></div>
      </dl>
    </header>
    <div className="adm-tabs" role="tablist" aria-label="Настройка камеры">
      {TABS.map((t) => <button key={t.id} role="tab" id={`tab-${t.id}`} aria-selected={tab === t.id} aria-controls={`panel-${t.id}`} className={tab === t.id ? "selected" : ""} onClick={() => pick(t.id)}>{t.icon}{t.title}
        {t.id === "video" && merged.some((j) => j.status === "running" || j.status === "queued" || j.status === "retry_wait") && <i className="adm-dot" aria-label="идёт обработка" />}
        {t.id === "broadcast" && liveBroadcast?.status === "playing" && <i className="adm-dot adm-dot-live" aria-label="эфир идёт" />}
      </button>)}
    </div>
    <div className="adm-tabpanel" role="tabpanel" id={`panel-${tab}`} aria-labelledby={`tab-${tab}`}>{panels[tab]}</div>
  </div>;
}
