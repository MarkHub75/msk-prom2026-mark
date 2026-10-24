import { useEffect, useMemo, useRef, useState, type ReactNode, type RefObject } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, Eye, EyeOff, Grid3x3, Layers, Radio, RotateCcw, Shapes } from "lucide-react";
import { api } from "../api/client";
import { useApi } from "../api/useApi";
import type { CameraLiveView, EventSummary, Meta } from "../api/types";
import { useMeta, useUpdates } from "../components/AppShell";
import { VideoWithHud } from "../components/Media";
import { Into, LevelTag, SceneOverlay, StateBadge, useNow } from "../components/operator/kit";
import { duration, Empty, ErrorNotice, Loading, number, time } from "../components/ui";
import { usePhone } from "../components/usePhone";
import { PhoneCameraPage } from "./OperatorPhone";
import "../styles/operator-depth.css";

const IC = { size: 15, strokeWidth: 1.75, "aria-hidden": true } as const;
const WINDOW_MIN = 30;

function backendTitle(meta?: Meta) {
  if (!meta) return "Не получен";
  return `${meta.inference_backend === "linq" ? "LinQ TPU" : "CPU · local"}${meta.fake ? " · синтетические детекции" : ""}`;
}

/** Hides the player's HUD through its own H shortcut, so the button, the key and the player stay in one state. */
function pressH() { document.body.dispatchEvent(new KeyboardEvent("keydown", { key: "h", bubbles: true })); }

/** Live player of a camera with HUD, zones and calibration grid on top. Used by the camera page and the event card. */
export function LivePlayer({ view, reviewMs, zones = true, grid = true, compact = false }: { view: CameraLiveView; reviewMs?: number; zones?: boolean; grid?: boolean; compact?: boolean }) {
  const meta = useMeta();
  const host = useRef<HTMLDivElement>(null);
  if (!view.video) return <Empty title="Эфира нет" text={view.state.reason_text || "Для камеры нет готовой записи."} />;
  const review = reviewMs !== undefined;
  return <div ref={host} className={`od-player ${compact ? "is-compact" : ""}`}>
    <VideoWithHud key={review ? "review" : "live"} video={view.video} camera={view.camera.name} broadcast={review ? null : view.broadcast} initialMs={review ? reviewMs : view.broadcast?.position_ms ?? 0} episodes={view.analysis?.episodes} />
    <Into host={host} selector=".video-frame" deps={[view.video.id, review]}>
      <SceneOverlay zones={view.zones} calibration={view.calibration} meta={meta} showZones={zones} showGrid={grid} />
    </Into>
  </div>;
}

/** Position of the <video> under `host`, polled for the timeline playhead. */
function usePlayhead(host: RefObject<HTMLElement>) {
  const [ms, setMs] = useState(0);
  useEffect(() => { const timer = setInterval(() => { const video = host.current?.querySelector("video"); if (video) setMs(video.currentTime * 1000); }, 250); return () => clearInterval(timer); }, [host]);
  return ms;
}

function EpisodeTimeline({ view, events, playhead, onSeek, onOpen, now }: { view: CameraLiveView; events: EventSummary[]; playhead: number; onSeek: (ms: number) => void; onOpen: (id: number) => void; now: number }) {
  const total = view.video?.duration_ms || view.analysis?.duration_ms || 0;
  const episodes = view.analysis?.episodes ?? [];
  const gaps = view.analysis?.gaps ?? [];
  const from = now - WINDOW_MIN * 60_000;
  const recent = events.filter(e => Date.parse(e.published_at) >= from);
  const pct = (ms: number) => `${Math.max(0, Math.min(100, ms / total * 100))}%`;
  const wall = (iso: string) => `${Math.max(0, Math.min(100, (Date.parse(iso) - from) / (WINDOW_MIN * 600)))}%`;
  const ticks = total ? [0, .25, .5, .75, 1].map(f => f * total) : [];
  return <section className="od-timeline" data-panel="Таймлайн эпизодов" aria-label="Таймлайн эпизодов">
    <div className="od-tl-row">
      <span className="od-tl-label">Запись<small>{total ? duration(total) : "—"}</small></span>
      <div className="od-tl-track" onClick={e => { if (!total) return; const r = e.currentTarget.getBoundingClientRect(); onSeek((e.clientX - r.left) / r.width * total); }}>
        {gaps.map((gap, i) => <span key={`gap${i}`} className="od-tl-gap" style={{ left: pct(gap.start_ms), width: pct(gap.end_ms - gap.start_ms) }} title={`Нет наблюдения: ${gap.reason}`} />)}
        {episodes.map(ep => <button key={ep.id} className={`od-tl-ep od-tl-${ep.level_max}`} style={{ left: pct(ep.start_ms), width: `max(6px, ${pct(ep.end_ms - ep.start_ms)})` }} onClick={e => { e.stopPropagation(); onSeek(ep.confirm_ms); }} title={`${ep.scenario_title}: ${ep.reason_text}`} aria-label={`Эпизод: ${ep.scenario_title}, ${duration(ep.start_ms)}`}>
          {ep.escalate_ms !== null && <i style={{ left: `${(ep.escalate_ms - ep.start_ms) / Math.max(1, ep.end_ms - ep.start_ms) * 100}%` }} />}
          <span>{ep.scenario_title}</span>
        </button>)}
        {total > 0 && <span className="od-tl-head" style={{ left: pct(playhead) }} />}
      </div>
    </div>
    <div className="od-tl-scale">{ticks.map(t => <span key={t}>{duration(t)}</span>)}</div>
    <div className="od-tl-row">
      <span className="od-tl-label">События<small>{WINDOW_MIN} мин</small></span>
      <div className="od-tl-track od-tl-wall">
        {recent.map(e => <button key={e.id} className={`od-tl-ev od-tl-${e.level}`} style={{ left: wall(e.published_at) }} onClick={() => onOpen(e.id)} title={`#${e.id} · ${time(e.published_at)} · ${e.title} · ${e.status_title}`} aria-label={`Событие #${e.id}, ${time(e.published_at)}`} />)}
        {!recent.length && <span className="od-tl-none">За {WINDOW_MIN} минут событий нет</span>}
      </div>
    </div>
    <div className="od-tl-scale">{[0, 10, 20, 30].map(m => <span key={m}>{time(new Date(from + m * 60_000).toISOString(), false)}</span>)}</div>
  </section>;
}

function Fact({ k, children }: { k: string; children: ReactNode }) { return <div><dt>{k}</dt><dd>{children}</dd></div>; }

export function CameraPage() {
  const { cameraId } = useParams();
  return usePhone() ? <PhoneCameraPage id={Number(cameraId)} /> : <CameraDesk id={Number(cameraId)} />;
}

function CameraDesk({ id }: { id: number }) {
  const updates = useUpdates(); const meta = useMeta();
  const navigate = useNavigate(); const now = useNow(5000);
  const view = useApi(() => api.GET("/api/cameras/{camera_id}/view", { params: { path: { camera_id: id } } }), [id], { refresh: [updates] });
  const events = useApi(() => api.GET("/api/events", { params: { query: { camera_id: id, limit: 200, include_demo: true } } }), [id], { refresh: [updates] });
  const sectors = useApi(() => api.GET("/api/sectors"), []);
  const [hud, setHud] = useState(true);
  const [zones, setZones] = useState(true);
  const [grid, setGrid] = useState(true);
  const [reviewMs, setReviewMs] = useState<number>();
  const host = useRef<HTMLDivElement>(null);
  const playhead = usePlayhead(host);
  useEffect(() => { setReviewMs(undefined); }, [id]);
  // The player remounts between live and review and starts with HUD on again.
  const reviewing = reviewMs !== undefined;
  useEffect(() => { setHud(true); }, [reviewing]);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if ((e.target as HTMLElement)?.closest?.("input,textarea,select,[contenteditable=true]")) return; if (e.key.toLowerCase() === "h") setHud(v => !v); };
    window.addEventListener("keydown", onKey); return () => window.removeEventListener("keydown", onKey);
  }, []);
  const list = useMemo(() => events.data?.items ?? [], [events.data]);
  const data = view.data;
  const sector = sectors.data?.find(s => s.id === data?.camera.sector_id);
  if (view.error) return <div className="od-page" data-testid="camera-view"><ErrorNotice error={view.error} retry={view.reload} /></div>;
  if (!data) return <div className="od-page" data-testid="camera-view"><Loading text="Получаем эфир камеры" /></div>;
  const { camera, state, video, analysis, broadcast, calibration } = data;
  const open = list.filter(e => !meta?.statuses.find(s => s.id === e.status)?.terminal);
  return <div className="od-page od-camera" data-testid="camera-view">
    <header className="od-bar">
      <Link className="od-back" to={`/operator/sectors/${camera.sector_id}`}><ArrowLeft {...IC} />Сектор {number(camera.sector_id)}</Link>
      <h1>{camera.name}</h1>
      <StateBadge state={state.state} text={state.state === "no_observation" ? state.reason_text : undefined} />
      {camera.is_demo && <span className="od-demo">Демо-камера</span>}
      <span className="od-bar-spacer" />
      {broadcast && <span className={`od-onair ${broadcast.status === "playing" ? "is-on" : ""}`}><Radio {...IC} />{broadcast.status === "playing" ? "Эфир" : "Эфир остановлен"} · цикл {broadcast.cycle}</span>}
      {reviewMs !== undefined && <button className="button button-small" onClick={() => setReviewMs(undefined)}><RotateCcw {...IC} />Вернуться в эфир</button>}
      <button className={`button button-small od-hud-btn ${hud ? "" : "is-off"}`} onClick={pressH} aria-pressed={!hud}>{hud ? <EyeOff {...IC} /> : <Eye {...IC} />}{hud ? "Скрыть HUD" : "Показать HUD"}<kbd>H</kbd></button>
      <button className="button button-small" onClick={view.reload} disabled={view.loading}>Обновить</button>
    </header>
    <div className="od-cam-grid">
      <section className="od-cam-stage" data-panel={reviewMs !== undefined ? "Просмотр эпизода" : "Эфир"} ref={host}>
        <LivePlayer view={data} reviewMs={reviewMs} zones={hud && zones} grid={hud && grid} />
        {reviewMs !== undefined && <p className="od-review-note">Просмотр эпизода с {duration(reviewMs)}. Эфир продолжается на сервере.</p>}
      </section>
      <aside className="od-cam-side">
        <section data-panel="Свойства камеры" className="od-props">
          <dl>
            <Fact k="Сектор"><Link to={`/operator/sectors/${camera.sector_id}`}>{number(camera.sector_id)} · {sector?.name.replace(/^Сектор\s+\d+\s*·\s*/, "") ?? "—"}</Link></Fact>
            <Fact k="Состояние"><StateBadge state={state.state} text={state.reason_text} /></Fact>
            <Fact k="Бэкенд анализа">{backendTitle(meta)}</Fact>
            <Fact k="Свежесть анализа"><span className="mono">{state.freshness_ms === null ? "нет эфира" : `${state.freshness_ms} мс`}</span></Fact>
            <Fact k="Запись">{video ? <span className="mono">{video.width}×{video.height} · {video.fps} к/с · {video.codec}</span> : "нет"}</Fact>
            <Fact k="Длительность">{video ? <span className="mono">{duration(video.duration_ms)} · {video.frame_count} кадров</span> : "—"}</Fact>
            <Fact k="Анализ">{analysis ? <>версия {analysis.version}{analysis.pose_used ? " · с позой" : " · без позы"}</> : "нет"}</Fact>
            <Fact k="Калибровка">{calibration ? <span className="mono">RMSE {calibration.fit_rmse_m.toFixed(2)} м{calibration.control_rmse_m === null ? " · без контроля" : ` · контроль ${calibration.control_rmse_m.toFixed(2)} м`}</span> : "нет · меры в ростах человека"}</Fact>
            <Fact k="Открыто событий"><span className="od-counts"><b className="od-n-red">{state.open_red}</b> красных · <b className="od-n-yellow">{state.open_yellow}</b> жёлтых</span></Fact>
            {camera.description && <Fact k="Описание">{camera.description}</Fact>}
          </dl>
        </section>
        <section data-panel="Слои" className="od-layers">
          <label><input type="checkbox" checked={hud} onChange={pressH} /><Layers {...IC} />HUD: объекты анализа<kbd>H</kbd></label>
          <label><input type="checkbox" checked={zones} disabled={!hud} onChange={e => setZones(e.target.checked)} /><Shapes {...IC} />Зоны<span className="mono">{data.zones.length}</span></label>
          <label><input type="checkbox" checked={grid} disabled={!hud || !calibration} onChange={e => setGrid(e.target.checked)} /><Grid3x3 {...IC} />Сетка 1 м{!calibration && <span>нет калибровки</span>}</label>
          {data.zones.length > 0 && <ul className="od-legend">{data.zones.map(z => { const kind = meta?.zone_kinds.find(k => k.id === z.kind); return <li key={z.id}><i style={{ background: kind?.color }} />{z.name}<span>{kind?.title ?? z.kind}</span></li>; })}</ul>}
        </section>
        <section data-panel="События камеры" className="od-cam-events">
          {events.error ? <ErrorNotice error={events.error} compact retry={events.reload} /> : !events.data ? <Loading /> : list.length ? <ol className="od-feed">{list.slice(0, 40).map(e => <li key={e.id}><Link to={`/events/${e.id}`} className={`od-feed-row od-feed-${e.level}`}><time className="mono">{time(e.published_at)}</time><span className="od-feed-main"><strong>{e.title}</strong><small>{e.reason_text}</small></span><span className="od-feed-side"><LevelTag level={e.level} /><small>{e.status_title}</small></span></Link></li>)}</ol> : <Empty title="Событий нет" text="Событий нет — это не значит, что всё безопасно, если камера без наблюдения." />}
          {list.length > 0 && <p className="od-foot-note">Открыто {open.length} из {events.data?.total ?? list.length}</p>}
        </section>
      </aside>
      <EpisodeTimeline view={data} events={list} playhead={playhead} now={now} onSeek={ms => setReviewMs(Math.round(ms))} onOpen={eid => navigate(`/events/${eid}`)} />
    </div>
  </div>;
}
