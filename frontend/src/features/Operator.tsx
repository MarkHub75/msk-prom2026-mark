import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, mediaUrl } from "../api/client";
import { useApi } from "../api/useApi";
import type { CameraTile, EventSummary, HumanAction, SectorState } from "../api/types";
import { useRole } from "../roles";
import { ACTIONS, useEventActions } from "./eventActions";
import { EventAlarm } from "../components/AlarmTakeover";
import { useMeta, useUpdates } from "../components/AppShell";
import { EventFeed } from "../components/EventFeed";
import { EvidenceFrame, VideoWithHud } from "../components/Media";
import { Breadcrumb, duration, Empty, ErrorNotice, Icon, Loading, number, PageHeading, PanelHeading, time } from "../components/ui";
import "../styles/targeted-visual.css";

// "Сектор 1 · Прессовый участок" -> "Прессовый участок"
export function shortSector(name: string) { return name.replace(/^Сектор\s+\d+\s*[·/–-]\s*/i, ""); }
export function shortCamera(name: string) { return name.replace(/^Камера\s+/i, "Кам "); }
const STATE_TITLE: Record<SectorState["state"], string> = { red: "Тревога", yellow: "Внимание", normal: "Норма", no_observation: "Нет наблюдения" };

function StateChip({ state, text }: { state: SectorState["state"]; text?: string }) {
  return <span className={`cr-chip cr-chip-${state}`}><i />{text ?? STATE_TITLE[state]}</span>;
}

/** Main camera of the wall: live replay with HUD when the backend has it, otherwise the latest still. */
function Stage({ tile, sector, event }: { tile?: CameraTile; sector?: SectorState; event?: EventSummary }) {
  const updates = useUpdates();
  const live = useApi(() => tile ? api.GET("/api/cameras/{camera_id}/view", { params: { path: { camera_id: tile.camera.id } } }) : Promise.resolve({ data: undefined }), [tile?.camera.id, updates]);
  const detail = useApi(() => event && event.camera_id === tile?.camera.id ? api.GET("/api/events/{event_id}", { params: { path: { event_id: event.id } } }) : Promise.resolve({ data: undefined }), [event?.id, tile?.camera.id]);
  if (!tile) return <div className="cr-stage cr-stage-empty"><Empty title="Камера не выбрана" text={sector ? sector.reason_text : "Выберите сектор внизу экрана."} /></div>;
  const state = tile.state.state;
  const evidence = detail.data?.episode?.evidence[0];
  return <section className={`cr-stage cr-frame-${state}`} aria-label={`Камера ${tile.camera.name}`}>
    <div className="cr-stage-media">
      {live.data?.video ? <VideoWithHud video={live.data.video} camera={tile.camera.name} broadcast={live.data.broadcast} episodes={live.data.analysis?.episodes} initialMs={live.data.broadcast?.position_ms ?? 0} />
        : tile.preview_url ? <div className="cr-still"><img src={mediaUrl(tile.preview_url)} alt={`Кадр камеры ${tile.camera.name}`} /><span className="cr-still-note">Последний кадр записи</span></div>
        : evidence ? <EvidenceFrame evidence={evidence} camera={tile.camera.name} level={event!.level} />
        : <Empty title={state === "no_observation" ? "Нет наблюдения" : "Кадр не получен"} text={tile.state.reason_text || "Сервер не передал изображение для этой камеры."} />}
    </div>
    <div className="cr-stage-tags"><span className="cr-tag">{tile.camera.name}</span><StateChip state={state} text={state === "no_observation" ? tile.state.reason_text || undefined : undefined} /></div>
  </section>;
}

function WallTile({ tile, selected, onSelect }: { tile: CameraTile; selected: boolean; onSelect: () => void }) {
  const state = tile.state.state;
  return <button className={`cr-tile cr-frame-${state} ${selected ? "is-selected" : ""}`} onClick={onSelect} aria-pressed={selected} aria-label={`Показать ${tile.camera.name}`}>
    {tile.preview_url ? <img src={mediaUrl(tile.preview_url)} alt="" /> : <span className="cr-tile-empty"><Icon name="camera" size={22} />{state === "no_observation" ? "Нет наблюдения" : "Нет кадра"}</span>}
    <span className="cr-tag">{shortCamera(tile.camera.name)}</span>
    {state !== "normal" && <StateChip state={state} />}
  </button>;
}

function SectorCell({ sector, selected, onSelect }: { sector: SectorState; selected: boolean; onSelect: () => void }) {
  const observed = sector.cameras_total - sector.cameras_no_observation;
  return <button className={`cr-sector cr-sector-${sector.state} ${selected ? "is-selected" : ""}`} onClick={onSelect} aria-pressed={selected}>
    <span className="cr-sector-top"><b>{number(sector.sector_id)}</b><span>{shortSector(sector.name)}</span></span>
    <span className="cr-sector-bottom"><StateChip state={sector.state} /><span className="cr-counts">{sector.open_red > 0 && <em className="cr-n-red">{sector.open_red}</em>}{sector.open_yellow > 0 && <em className="cr-n-yellow">{sector.open_yellow}</em>}<span className="mono">{observed}/{sector.cameras_total}</span></span></span>
  </button>;
}

function QueueRow({ event, selected, onSelect, closed }: { event: EventSummary; selected: boolean; onSelect: () => void; closed?: boolean }) {
  return <li className={`cr-q cr-q-${closed ? "closed" : event.level} ${selected ? "is-selected" : ""}`}>
    <button onClick={onSelect} aria-pressed={selected}>
      <span className="cr-q-top"><time className="mono">{time(event.published_at)}</time><span className="mono">#{event.id}</span></span>
      <strong>{event.title}</strong>
      <span className="cr-q-place">{shortSector(event.sector_name)} · {shortCamera(event.camera_name)}</span>
      <span className="cr-q-foot"><span className={`cr-status cr-status-${closed ? "closed" : event.level}`}>{event.status_title}</span><span className="mono">{duration(event.duration_s * 1000)}</span></span>
    </button>
  </li>;
}

// Quick decisions of the operator; the server's allowed_actions decides which of them are shown.
const QUICK: HumanAction[] = ["confirm", "false_alarm", "send_to_master"];

function SelectedEvent({ event, onDone }: { event: EventSummary; onDone: () => void }) {
  const [role] = useRole();
  const detail = useApi(() => api.GET("/api/events/{event_id}", { params: { path: { event_id: event.id } } }), [event.id, event.status]);
  const shown = detail.data?.event.id === event.id ? detail.data : undefined;
  const { busy, actionError, send } = useEventActions(event.id, shown, `${role}:${event.id}`);
  const actions = shown?.allowed_actions.filter(action => QUICK.includes(action)) ?? [];
  const act = async (action: HumanAction) => { if (await send(action)) onDone(); };
  const evidence = detail.data?.episode?.evidence[0];
  return <section className="cr-selected" aria-label="Выбранное событие">
    <h2>Выбранное событие</h2>
    <div className="cr-selected-media">{evidence ? <EvidenceFrame evidence={evidence} camera={event.camera_name} level={event.level} /> : <span className="cr-tile-empty"><Icon name="camera" size={22} />{detail.loading ? "Загружаем кадр" : "Кадр не получен"}</span>}</div>
    <dl className="cr-facts">
      <dt>Событие</dt><dd>{event.title}</dd>
      <dt>Причина</dt><dd>{event.reason_text}</dd>
      <dt>Время</dt><dd className="mono">{time(event.started_at)}</dd>
      <dt>Место</dt><dd>{shortSector(event.sector_name)} · {event.camera_name}{event.zone_name ? ` · ${event.zone_name}` : ""}</dd>
      <dt>Статус</dt><dd><span className={`cr-status cr-status-${event.level}`}>{event.status_title}</span></dd>
    </dl>
    {actions.length > 0 && <div className="cr-quick" aria-label="Быстрые действия">{actions.map(action => <button key={action} data-action={action} disabled={Boolean(busy)} onClick={() => void act(action)} className={`button button-small ${action === "confirm" ? event.level === "red" ? "button-danger" : "button-primary" : "button-light"}`}>{busy === action ? "Сохраняем…" : ACTIONS[action]}</button>)}</div>}
    {actionError && <ErrorNotice error={actionError} compact retry={detail.reload} />}
    <Link className={`button cr-open ${event.level === "red" ? "button-danger" : "button-primary"}`} to={`/events/${event.id}`}>Открыть событие <Icon name="arrow" size={16} /></Link>
  </section>;
}

/** All plant cameras in one row, alarming first: the operator sees the whole plant, not only the focused sector. */
function PlantStrip({ sectors, focusCamera, onPick }: { sectors: SectorState[]; focusCamera?: number; onPick: (sector: number, camera: number) => void }) {
  const updates = useUpdates();
  const ids = sectors.map(s => s.sector_id).join(",");
  const views = useApi(async () => {
    const results = await Promise.all(sectors.map(s => api.GET("/api/sectors/{sector_id}/view", { params: { path: { sector_id: s.sector_id } } })));
    const failed = results.find(r => r.error !== undefined);
    return failed ? { error: failed.error } : { data: results.flatMap(r => r.data?.cameras ?? []) };
  }, [ids, updates]);
  const rank = { red: 0, yellow: 1, normal: 2, no_observation: 3 } as const;
  const tiles = [...(views.data ?? [])].sort((a, b) => rank[a.state.state] - rank[b.state.state] || a.camera.id - b.camera.id);
  if (!tiles.length) return null;
  return <section className="cr-strip" aria-label="Все камеры завода">
    <div className="cr-strip-head"><h2>Камеры завода</h2><span className="mono">{tiles.filter(t => t.state.state !== "no_observation").length}/{tiles.length} наблюдаются</span></div>
    <div className="cr-strip-row">{tiles.map(tile => <WallTile key={tile.camera.id} tile={tile} selected={tile.camera.id === focusCamera} onSelect={() => onPick(tile.camera.sector_id, tile.camera.id)} />)}</div>
  </section>;
}

export function OperatorPage() {
  const updates = useUpdates();
  const meta = useMeta();
  const dashboard = useApi(() => api.GET("/api/operator/dashboard"), [updates]);
  const [filter, setFilter] = useState<"all" | "red" | "yellow">("all");
  const [pickedSector, setPickedSector] = useState<number>();
  const [pickedCamera, setPickedCamera] = useState<number>();
  const [pickedEvent, setPickedEvent] = useState<number>();
  // operator_feed includes recently closed events (tech.md 8.8). Never change an event's status on the client.
  const isTerminal = (event: EventSummary) => meta?.statuses.find(status => status.id === event.status)?.terminal ?? event.priority === 0;
  const feedAll = dashboard.data?.feed ?? [];
  const active = feedAll.filter(event => !isTerminal(event));
  const history = feedAll.filter(isTerminal);
  const critical = active.find(event => event.level === "red" && event.operator_verdict === "none");
  const sectors = dashboard.data?.sectors ?? [];
  // Backend priority (tech.md 8.8): 3 red and 2 yellow still waiting for the operator, 1 other open (already handled, with the master).
  const waiting = active.filter(event => event.priority >= 2);
  const inWork = active.filter(event => event.priority < 2);
  const queue = waiting.filter(event => filter === "all" || event.level === filter);
  const focusSector = sectors.find(s => s.sector_id === pickedSector) ?? sectors.find(s => s.state === "red") ?? sectors.find(s => s.state === "yellow") ?? sectors[0];
  const selectedEvent = feedAll.find(e => e.id === pickedEvent) ?? queue[0];
  const sectorView = useApi(() => focusSector ? api.GET("/api/sectors/{sector_id}/view", { params: { path: { sector_id: focusSector.sector_id } } }) : Promise.resolve({ data: undefined }), [focusSector?.sector_id, updates]);
  const tiles = sectorView.data?.cameras ?? [];
  const rank = { red: 0, yellow: 1, normal: 2, no_observation: 3 } as const;
  const focusTile = tiles.find(t => t.camera.id === pickedCamera) ?? [...tiles].sort((a, b) => rank[a.state.state] - rank[b.state.state])[0];
  const stageEvent = active.find(e => e.camera_id === focusTile?.camera.id) ?? (selectedEvent?.camera_id === focusTile?.camera.id ? selectedEvent : undefined);
  const selectSector = (id: number) => { setPickedSector(id); setPickedCamera(undefined); };
  const selectEvent = (event: EventSummary) => { setPickedEvent(event.id); setPickedSector(event.sector_id); setPickedCamera(event.camera_id); };

  if (dashboard.error) return <div className="cr-page"><ErrorNotice error={dashboard.error} retry={dashboard.reload} /></div>;
  if (!dashboard.data) return <div className="cr-page"><Loading /></div>;
  return <div className="cr-page" data-testid="operator-view">
    <div className="cr-head">
      <h1>Диспетчерская</h1>
      {focusSector && <span className="cr-crumb"><Icon name="pin" size={15} />Сектор {number(focusSector.sector_id)} · {shortSector(focusSector.name)}</span>}
      <span className="cr-asof">Данные на <span className="mono">{time(dashboard.data.server_now)}</span></span>
      <button className="button button-small cr-refresh" onClick={dashboard.reload} disabled={dashboard.loading}>Обновить</button>
    </div>
    <div className="cr-grid">
      <div className="cr-wall">
        <Stage tile={focusTile} sector={focusSector} event={stageEvent} />
        <div className="cr-side">
          {sectorView.error ? <ErrorNotice error={sectorView.error} compact retry={sectorView.reload} /> : tiles.map(tile => <WallTile key={tile.camera.id} tile={tile} selected={tile.camera.id === focusTile?.camera.id} onSelect={() => setPickedCamera(tile.camera.id)} />)}
          {focusSector && <Link className="cr-side-link" to={`/operator/sectors/${focusSector.sector_id}`}>Все камеры сектора <Icon name="chevron" size={14} /></Link>}
        </div>
      </div>
      <aside className="cr-queue" aria-label="Очередь тревог">
        <div className="cr-queue-head"><h2>Очередь тревог</h2><span className="cr-count" data-testid="active-event-count">{waiting.length}</span></div>
        <div className="feed-filter cr-filter" aria-label="Уровень активных событий">{([["all", "Все"], ["red", "Тревога"], ["yellow", "Внимание"]] as const).map(([id, label]) => <button key={id} className={filter === id ? "selected" : ""} onClick={() => setFilter(id)} aria-pressed={filter === id}>{label}</button>)}</div>
        {queue.length ? <ol className="cr-q-list">{queue.map(event => <QueueRow key={event.id} event={event} selected={event.id === selectedEvent?.id} onSelect={() => selectEvent(event)} />)}</ol> : <div className="cr-quiet"><strong>Активных тревог нет</strong><span>Камеры без наблюдения показаны в полосе секторов: отсутствие тревог там не означает безопасность.</span></div>}
        {selectedEvent && !isTerminal(selectedEvent) && <SelectedEvent event={selectedEvent} onDone={dashboard.reload} />}
        {inWork.length > 0 && <details className="cr-history cr-inwork"><summary><span>В работе: решение принято, ждём закрытия</span><span className="mono">{inWork.length}</span></summary><ol className="cr-q-list">{inWork.slice(0, 30).map(event => <QueueRow key={event.id} event={event} selected={event.id === selectedEvent?.id} onSelect={() => selectEvent(event)} />)}</ol>{inWork.length > 30 && <Link className="text-link" to="/ohs/journal">Ещё {inWork.length - 30} — в журнале <Icon name="arrow" size={14} /></Link>}</details>}
        <details className="cr-history"><summary><span>Недавно завершено</span><span className="mono" data-testid="closed-event-count">{history.length}</span></summary>{history.length ? <ol className="cr-q-list">{history.map(event => <QueueRow key={event.id} event={event} closed selected={false} onSelect={() => selectEvent(event)} />)}</ol> : <p>Завершённых событий за последние минуты нет.</p>}<Link className="text-link" to="/ohs/journal">Открыть журнал <Icon name="arrow" size={14} /></Link></details>
      </aside>
      <section className="cr-sectors" aria-label="Секторы производства">
        {sectors.length ? sectors.map(sector => <SectorCell key={sector.sector_id} sector={sector} selected={sector.sector_id === focusSector?.sector_id} onSelect={() => selectSector(sector.sector_id)} />) : <Empty title="Секторы не найдены" text="Сервер вернул пустой список секторов." />}
      </section>
      <PlantStrip sectors={sectors} focusCamera={focusTile?.camera.id} onPick={(sector, camera) => { setPickedSector(sector); setPickedCamera(camera); }} />
    </div>
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
