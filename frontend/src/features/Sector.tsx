import { useEffect, useMemo, useState } from "react";
import { Link, NavLink, useParams } from "react-router-dom";
import { ArrowLeft, ArrowRight, Camera as CameraIcon, VideoOff } from "lucide-react";
import { api, mediaUrl } from "../api/client";
import { useApi } from "../api/useApi";
import type { CameraTile, EventSummary } from "../api/types";
import { useMeta, useUpdates } from "../components/AppShell";
import { LevelTag, StateBadge, useNow } from "../components/operator/kit";
import { duration, Empty, ErrorNotice, Loading, number, time } from "../components/ui";
import { usePhone } from "../components/usePhone";
import { PhoneCameras } from "./OperatorPhone";
import "../styles/operator-depth.css";

const IC = { size: 15, strokeWidth: 1.75, "aria-hidden": true } as const;
// tech.md 8.14: previews refresh every preview.cache_s. /api/meta does not carry it, so the default of config/default.yaml (2.0 s) is used.
const PREVIEW_MS = 2000;
const short = (name: string) => name.replace(/^Сектор\s+\d+\s*[·/–-]\s*/i, "");

function Tile({ tile, tick }: { tile: CameraTile; tick: number }) {
  const [failed, setFailed] = useState(false);
  const s = tile.state;
  const next = tile.preview_url ? `${mediaUrl(tile.preview_url)}${tile.preview_url.includes("?") ? "&" : "?"}t=${tick}` : undefined;
  // Double buffer: keep the last decoded frame on screen until the next one has loaded, so the tile never blinks.
  const [src, setSrc] = useState(next);
  useEffect(() => {
    if (!next) { setSrc(undefined); return; }
    const image = new Image(); let live = true;
    image.onload = () => { if (live) { setSrc(next); setFailed(false); } };
    image.onerror = () => { if (live) setFailed(true); };
    image.src = next;
    return () => { live = false; };
  }, [next]);
  return <article className={`od-tile od-frame-${s.state}`} data-testid="sector-camera">
    <Link to={`/operator/cameras/${tile.camera.id}`} aria-label={`Открыть ${tile.camera.name}`}>
      <div className="od-tile-media">
        {src && !failed ? <img src={src} alt={`Кадр камеры ${tile.camera.name}`} /> : <div className="od-tile-none"><VideoOff size={28} strokeWidth={1.5} aria-hidden /><strong>{s.state === "no_observation" ? "Нет наблюдения" : "Кадр не получен"}</strong><span>{s.reason_text}</span></div>}
        <span className="od-tile-name">{tile.camera.name}</span>
        <span className="od-tile-state"><StateBadge state={s.state} text={s.state === "no_observation" ? s.reason_text : undefined} /></span>
        {tile.broadcast?.status === "playing" && <span className="od-tile-live"><i />Эфир</span>}
      </div>
      <div className="od-tile-foot">
        <span className="od-counts">{s.open_red || s.open_yellow ? <>Открыто: <b className={s.open_red ? "od-n-red" : undefined}>{s.open_red}</b> красн. · <b className={s.open_yellow ? "od-n-yellow" : undefined}>{s.open_yellow}</b> жёлт.</> : "Открытых событий нет"}</span>
        <span title="Сколько прошло от кадра до результата анализа">{s.freshness_ms === null ? "Эфира нет" : <>Задержка анализа <span className="mono">{s.freshness_ms} мс</span></>}</span>
        <span className="od-tile-go">Камера<ArrowRight {...IC} /></span>
      </div>
    </Link>
  </article>;
}

function FeedRow({ event, now, terminal }: { event: EventSummary; now: number; terminal: boolean }) {
  return <li><Link to={`/events/${event.id}`} className={`od-feed-row od-feed-${terminal ? "closed" : event.level}`}>
    <time className="mono">{time(event.published_at)}</time>
    <span className="od-feed-main"><strong>{event.title}</strong><small>{event.camera_name}{event.zone_name ? ` · ${event.zone_name}` : ""} · {event.reason_text}</small></span>
    <span className="od-feed-side"><LevelTag level={event.level} /><small>{event.status_title} · {terminal ? <>длилось <span className="mono">{duration(event.duration_s * 1000)}</span></> : <>{ago(event.published_at, now)} назад</>}</small></span>
  </Link></li>;
}
/** Coarse age for the feed: minutes, then hours, then days. */
function ago(iso: string, now: number) {
  const s = Math.max(0, Math.floor((now - Date.parse(iso)) / 1000));
  return s < 3600 ? `${Math.max(1, Math.floor(s / 60))} мин` : s < 172_800 ? `${Math.floor(s / 3600)} ч` : `${Math.floor(s / 86_400)} дн`;
}
/** Latest evidence frames of the sector: one per event, newest first, straight from EventSummary.evidence_url. */
function EvidenceStrip({ events }: { events: EventSummary[] }) {
  const shots = events.filter(e => e.evidence_url).sort((a, b) => b.published_at.localeCompare(a.published_at)).slice(0, 8);
  return <section data-panel="Последние доказательства" className="od-evidence-strip">
    {shots.length ? <ol>{shots.map(e => <li key={e.id}><Link to={`/events/${e.id}`}><img src={mediaUrl(e.evidence_url!)} alt={`Кадр события #${e.id}`} loading="lazy" /><LevelTag level={e.level} /><span className="od-ev-cap"><b>{e.title}</b><span className="mono">#{e.id} · {time(e.published_at)}</span></span></Link></li>)}</ol>
      : <Empty title="Кадров нет" text="У событий сектора пока нет доказательных кадров." />}
  </section>;
}

export function SectorPage() {
  const { sectorId } = useParams();
  return usePhone() ? <PhoneCameras sectorId={Number(sectorId)} /> : <SectorDesk id={Number(sectorId)} />;
}

function SectorDesk({ id }: { id: number }) {
  const updates = useUpdates(); const meta = useMeta();
  const tick = Math.floor(useNow(PREVIEW_MS) / PREVIEW_MS);
  const now = useNow(1000);
  const view = useApi(() => api.GET("/api/sectors/{sector_id}/view", { params: { path: { sector_id: id } } }), [id], { refresh: [updates] });
  const sectors = useApi(() => api.GET("/api/sectors"), []);
  const [filter, setFilter] = useState<"open" | "all">("open");
  const terminal = (e: EventSummary) => meta?.statuses.find(s => s.id === e.status)?.terminal ?? e.priority === 0;
  const feed = useMemo(() => (view.data?.feed ?? []).filter(e => filter === "all" || !terminal(e)), [view.data, filter, meta]); // eslint-disable-line react-hooks/exhaustive-deps
  const data = view.data;
  const observed = data ? data.sector.cameras_total - data.sector.cameras_no_observation : 0;
  return <div className="od-page od-sector" data-testid="sector-view">
    <header className="od-bar">
      <Link className="od-back" to="/operator"><ArrowLeft {...IC} />Диспетчерская</Link>
      <h1><span className="od-num">{number(id)}</span>{data ? short(data.sector.name) : `Сектор ${number(id)}`}</h1>
      {data && <StateBadge state={data.sector.state} text={data.sector.state === "no_observation" ? data.sector.reason_text : undefined} />}
      <span className="od-bar-spacer" />
      {sectors.data && <nav className="od-sector-tabs" aria-label="Секторы">{sectors.data.map(s => <NavLink key={s.id} to={`/operator/sectors/${s.id}`}>{number(s.id)}<span>{short(s.name)}</span></NavLink>)}</nav>}
      <button className="button button-small" onClick={view.reload} disabled={view.loading}>Обновить</button>
    </header>
    {view.error ? <ErrorNotice error={view.error} retry={view.reload} /> : !data ? <Loading text="Получаем камеры сектора" /> : <>
      <div className="od-kpis">
        <div className={data.sector.open_red ? "is-red" : ""}><span>Красные события, открыто</span><b>{data.sector.open_red}</b></div>
        <div className={data.sector.open_yellow ? "is-yellow" : ""}><span>Жёлтые события, открыто</span><b>{data.sector.open_yellow}</b></div>
        <div className={data.sector.cameras_no_observation ? "is-muted" : ""}><span>Камеры под наблюдением</span><b>{observed}<small> из {data.sector.cameras_total}</small></b>{data.sector.cameras_no_observation > 0 && <em>Нет наблюдения: {data.sector.cameras_no_observation} из {data.sector.cameras_total}</em>}</div>
      </div>
      <div className="od-sector-grid">
        <div className="od-sector-main">
          <section data-panel="Камеры сектора" className="od-tiles-panel">
            {data.cameras.length ? <div className={`od-tiles od-tiles-${Math.min(data.cameras.length, 4)}`}>{data.cameras.map(tile => <Tile key={tile.camera.id} tile={tile} tick={tick} />)}</div> : <Empty title="Камер нет" text="В секторе нет камер. Это не значит, что в нём безопасно." />}
          </section>
          <EvidenceStrip events={data.feed} />
        </div>
        <aside data-panel="События сектора" className="od-sector-feed">
          <div className="od-seg" role="group" aria-label="Какие события показать">
            <button className={filter === "open" ? "selected" : ""} aria-pressed={filter === "open"} onClick={() => setFilter("open")}>Открытые</button>
            <button className={filter === "all" ? "selected" : ""} aria-pressed={filter === "all"} onClick={() => setFilter("all")}>Все <span className="mono">{data.feed.length}</span></button>
          </div>
          {feed.length ? <ol className="od-feed">{feed.map(e => <FeedRow key={e.id} event={e} now={now} terminal={terminal(e)} />)}</ol>
            : <Empty title={filter === "open" ? "Открытых событий нет" : "Событий нет"} text={data.sector.cameras_no_observation ? "Часть камер без наблюдения: тишина там не означает безопасность." : "Новые события сектора появятся здесь."} />}
          <Link className="od-foot-link" to="/ohs/journal"><CameraIcon {...IC} />Журнал событий<ArrowRight {...IC} /></Link>
        </aside>
      </div>
    </>}
  </div>;
}
