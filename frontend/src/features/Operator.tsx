import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, mediaUrl } from "../api/client";
import { useApi } from "../api/useApi";
import type { SectorState } from "../api/types";
import { EventAlarm } from "../components/AlarmTakeover";
import { useMeta, useUpdates } from "../components/AppShell";
import { EventFeed } from "../components/EventFeed";
import { VideoWithHud } from "../components/Media";
import { Breadcrumb, Empty, ErrorNotice, Icon, Loading, number, PageHeading, PanelHeading, time } from "../components/ui";
import "../styles/targeted-visual.css";

function SectorPanel({ sector, index }: { sector: SectorState; index: number }) {
  const updates = useUpdates();
  const view = useApi(() => api.GET("/api/sectors/{sector_id}/view", {params:{path:{sector_id:sector.sector_id}}}), [sector.sector_id, updates]);
  const tile = sector.state === "no_observation" ? view.data?.cameras.find(camera=>camera.state.state === "no_observation") ?? view.data?.cameras[0] : view.data?.cameras[0];
  return <article className={`sector-panel sector-${sector.state} ${index === 0 ? "sector-first" : ""}`}>
    <div className="sector-panel-heading"><Link to={`/operator/sectors/${sector.sector_id}`}><span className="sector-number">{number(sector.sector_id)}</span><h2 title={sector.name}>{sector.name.replace(/^Сектор\s+\d+\s*[·/–-]\s*/i, "")}</h2></Link><div className="sector-source">{tile ? tile.camera.name : `${sector.cameras_total} камер`}<small>{sector.state === "no_observation" ? "Нет наблюдения" : "Архивная запись"}</small></div></div>
    {tile?.preview_url ? <Link className="sector-media" to={`/operator/cameras/${tile.camera.id}`}><img src={mediaUrl(tile.preview_url)} alt={`${tile.camera.name}: обзор сектора ${sector.name}`} /><span className="sector-media-caption"><span>{tile.camera.name}</span><span>Открыть запись <Icon name="arrow" size={13} /></span></span></Link> : <Link className="sector-no-media" to={`/operator/sectors/${sector.sector_id}`}><Icon name="camera" size={36} /><strong>{view.loading ? "Загружаем кадр" : sector.state === "no_observation" ? "Нет наблюдения" : "Кадр недоступен"}</strong><span>{view.error?.message ?? sector.reason_text}</span></Link>}
    <div className="sector-panel-foot"><span>{sector.reason_text || "Состояние получено от сервера"}</span><Link to={`/operator/sectors/${sector.sector_id}`}>{sector.open_red ? <b className="critical-text">{sector.open_red} критических</b> : sector.open_yellow ? <b className="caution-text">{sector.open_yellow} требуют внимания</b> : <span>{sector.cameras_total - sector.cameras_no_observation} / {sector.cameras_total} наблюдаются</span>}<Icon name="chevron" size={14} /></Link></div>
  </article>;
}
export function OperatorPage() {
  const updates = useUpdates();
  const meta = useMeta();
  const dashboard = useApi(() => api.GET("/api/operator/dashboard"), [updates]);
  const [filter, setFilter] = useState<"all"|"red"|"yellow">("all");
  // operator_feed includes recently closed events (tech.md 8.8). Prefer the
  // backend's status metadata; its documented priority 0 is the closed fallback
  // while /meta is loading. Never change an event's status on the client.
  const isTerminal = (event: NonNullable<typeof dashboard.data>["feed"][number]) =>
    meta?.statuses.find(status => status.id === event.status)?.terminal ?? event.priority === 0;
  const active = dashboard.data?.feed.filter(event => !isTerminal(event)) ?? [];
  const history = dashboard.data?.feed.filter(isTerminal) ?? [];
  const critical = active.find(event => event.level === "red" && event.operator_verdict === "none");
  const sectors = dashboard.data?.sectors ?? [];
  const feed = active.filter(event => filter === "all" || event.level === filter);
  return <div className="operator-page" data-testid="operator-view">
    <PageHeading title="Сигнальный пост" meta={<><span>Обзор секторов</span><span className="meta-separator">/</span><span>{dashboard.data ? `Состояние на ${time(dashboard.data.server_now)}` : "Состояние не получено"}</span></>}><button className="button button-small" onClick={dashboard.reload} disabled={dashboard.loading}>Обновить <Icon name="arrow" size={15} /></button></PageHeading>
    {dashboard.error ? <ErrorNotice error={dashboard.error} retry={dashboard.reload} /> : dashboard.loading && !dashboard.data ? <Loading /> : dashboard.data && <div className="dispatch-layout"><section className="sector-matrix" aria-label="Секторы производства">{sectors.length ? sectors.map((sector,index) => <SectorPanel key={sector.sector_id} sector={sector} index={index} />) : <Empty title="Секторы не найдены" text="Сервер вернул пустой список секторов." />}</section><aside className="attention-rail"><PanelHeading aside={<span className="count" data-testid="active-event-count">{active.length}</span>}>Требует внимания</PanelHeading><div className="feed-filter" aria-label="Уровень активных событий">{([["all","Все"],["red","Критические"],["yellow","Внимание"]] as const).map(([id,label]) => <button key={id} className={filter===id?"selected":""} onClick={() => setFilter(id)} aria-pressed={filter===id}>{label}</button>)}</div>{active.length ? <EventFeed events={feed} compact /> : <Empty title="Активных тревог нет" text="Завершённые события хранятся отдельно в истории." />}<details className="closed-event-history"><summary><span>Недавно завершено</span><span data-testid="closed-event-count">{history.length}</span><Icon name="chevron" size={15} /></summary>{history.length ? <EventFeed events={history} compact /> : <p>Недавно завершённых событий в ответе сервера нет.</p>}<Link className="text-link" to="/ohs/journal">Открыть журнал <Icon name="arrow" size={14} /></Link></details></aside></div>}
    {dashboard.data && <div className="shift-ribbon"><div><Icon name="list" /><strong>Хронология событий</strong><span>Публикации и решения</span></div><div className="shift-events">{[...dashboard.data.feed].sort((a,b)=>a.published_at.localeCompare(b.published_at)).map(event => <Link to={`/events/${event.id}`} key={event.id} className={`ribbon-event ribbon-${event.level}${isTerminal(event) ? " ribbon-closed" : ""}`}><time>{time(event.published_at,false)}</time><span className="ribbon-tick" /><span>#{event.id} · {isTerminal(event) ? event.status_title : event.sector_name}</span></Link>)}</div></div>}
    <EventAlarm event={critical} />
  </div>;
}
export function SectorPage() {
  const { sectorId } = useParams(); const id = Number(sectorId); const updates = useUpdates();
  const view = useApi(() => api.GET("/api/sectors/{sector_id}/view", {params:{path:{sector_id:id}}}), [id, updates]);
  return <><Breadcrumb>Сектор {number(id)}</Breadcrumb><PageHeading title={view.data ? `${number(id)} / ${view.data.sector.name}` : `Сектор ${number(id)}`} meta={view.data?.sector.reason_text}><button className="button button-small" onClick={view.reload}>Обновить</button></PageHeading>{view.error ? <ErrorNotice error={view.error} retry={view.reload} /> : !view.data ? <Loading /> : <div className="sector-detail-layout"><section><PanelHeading aside={`${view.data.cameras.length} камер`}>Наблюдение сектора</PanelHeading><div className="camera-grid">{view.data.cameras.map(tile => <article className={`camera-tile sector-${tile.state.state}`} key={tile.camera.id}><Link to={`/operator/cameras/${tile.camera.id}`}><div className="camera-tile-title"><h2>{tile.camera.name}</h2><Icon name="arrow" /></div>{tile.preview_url ? <img src={mediaUrl(tile.preview_url)} alt={`Кадр камеры ${tile.camera.name}`} /> : <Empty title="Нет наблюдения" text={tile.state.reason_text} />}<div className="camera-tile-foot"><span>{tile.state.reason_text}</span><span>Архивная запись</span></div></Link></article>)}</div>{!view.data.cameras.length && <Empty title="Камер нет" text="В этом секторе пока нет доступных камер." />}</section><aside className="attention-rail"><PanelHeading>События сектора</PanelHeading><EventFeed events={view.data.feed} compact /></aside></div>}</>;
}
export function CameraPage() {
  const { cameraId } = useParams(); const id = Number(cameraId); const updates = useUpdates();
  const view = useApi(() => api.GET("/api/cameras/{camera_id}/view", {params:{path:{camera_id:id}}}), [id, updates]);
  const feed = useApi(() => api.GET("/api/operator/feed"), [updates]);
  return <div data-testid="camera-view"><Breadcrumb>{view.data && <><Link to={`/operator/sectors/${view.data.camera.sector_id}`}>Сектор {number(view.data.camera.sector_id)}</Link> / </> }Камера {number(id)}</Breadcrumb><PageHeading title={view.data?.camera.name ?? `Камера ${number(id)}`} meta={view.data?.state.reason_text}><span className="recording-label">Архивная запись</span><button className="button button-small" onClick={view.reload}>Обновить</button></PageHeading>{view.error ? <ErrorNotice error={view.error} retry={view.reload} /> : !view.data ? <Loading /> : <div className="camera-workspace"><section className="camera-stage"><PanelHeading aside={view.data.broadcast ? `Повтор · цикл ${view.data.broadcast.cycle}` : "Запись не запущена"}>Просмотр записи</PanelHeading>{view.data.video ? <VideoWithHud video={view.data.video} camera={view.data.camera.name} initialMs={view.data.broadcast?.position_ms ?? 0} broadcast={view.data.broadcast} episodes={view.data.analysis?.episodes} /> : <Empty title="Запись отсутствует" text={view.data.state.reason_text} />}<div className="camera-facts"><div><span>Сектор</span><Link to={`/operator/sectors/${view.data.camera.sector_id}`}>{number(view.data.camera.sector_id)}</Link></div><div><span>Наблюдение</span><strong>{view.data.state.reason_text}</strong></div><div><span>Описание</span><strong>{view.data.camera.description || "Не указано"}</strong></div></div></section><aside className="attention-rail"><PanelHeading>События камеры</PanelHeading>{feed.error ? <ErrorNotice error={feed.error} compact retry={feed.reload} /> : feed.loading ? <Loading /> : <EventFeed events={feed.data?.filter(event => event.camera_id===id) ?? []} compact />}</aside></div>}</div>;
}
