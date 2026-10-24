import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import { Check, ChevronDown, ChevronLeft, ChevronRight, Clock, Eye, EyeOff, Grid3x3, MapPin, MessageSquareText, Radio, ShieldAlert, Shapes, Timer, VideoOff } from "lucide-react";
import { api, mediaUrl } from "../api/client";
import { useApi } from "../api/useApi";
import type { CameraTile, EventDetail, EventSummary, HumanAction, SectorState } from "../api/types";
import { EventAlarm } from "../components/AlarmTakeover";
import { ClipPlayer } from "../components/ClipPlayer";
import { useMeta, useUpdates } from "../components/AppShell";
import { since, StateBadge, StateIcon, useNow } from "../components/operator/kit";
import { duration, ErrorNotice, number, Status, time, useToast } from "../components/ui";
import { LivePlayer } from "./Camera";
import { EpisodeHistory, Evidence, History, useEventDetail, type EventDetailState } from "./Incident";
import { LevelChip, ShiftSummary, unconfirmed, useBulkAction } from "./Master";
import { shortCamera, shortSector } from "./Operator";
import { toMobile } from "../components/PhoneChrome";
import { groupRepeats, repeatCount, type RepeatGroup } from "./repeats";
import "../styles/mobile-shell.css";
import "../styles/mobile-operator.css";
import "../styles/mobile-repeats.css";

const IC = { size: 16, strokeWidth: 1.75, "aria-hidden": true } as const;
// tech.md 8.14: previews refresh every preview.cache_s (default 2.0 s); off-screen tiles wait.
const PREVIEW_MS = 2000;
const RANK = { red: 0, yellow: 1, normal: 2, no_observation: 3 } as const;
const STATE_SHORT: Record<SectorState["state"], string> = { red: "Тревога", yellow: "Внимание", normal: "Норма", no_observation: "Нет наблюдения" };

/** tech.md 8.14 v5: under /m/operator every operator screen (feed, card, cameras, shift) stays on the mobile routes. */
export function useOperatorHref() { const mobile = useLocation().pathname.startsWith("/m/"); return (path: string) => mobile ? toMobile(path) : path; }
export function useEventHref() { const href = useOperatorHref(); return (id: number) => href(`/events/${id}`); }

/** Split of operator_feed exactly as the desktop dispatcher does it (tech.md 8.6, 8.8). */
function useOperatorFeed() {
  const updates = useUpdates(); const meta = useMeta();
  const dashboard = useApi(() => api.GET("/api/operator/dashboard"), [], { refresh: [updates] });
  const isTerminal = (e: EventSummary) => meta?.statuses.find(s => s.id === e.status)?.terminal ?? e.priority === 0;
  const feed = dashboard.data?.feed ?? [];
  const active = feed.filter(e => !isTerminal(e));
  const needsVerdict = (e: EventSummary) => e.priority >= 2 || (e.escalated_by_timeout && e.operator_verdict === "none");
  return {
    dashboard, active,
    waiting: active.filter(needsVerdict),
    inWork: active.filter(e => !needsVerdict(e)),
    history: feed.filter(isTerminal),
    critical: active.find(e => e.level === "red" && e.operator_verdict === "none"),
  };
}

function Repeats({ group, now }: { group: RepeatGroup; now: number }) {
  const [open, setOpen] = useState(false); const href = useEventHref();
  return <>
    <button className="rp-expand" aria-expanded={open} onClick={() => setOpen(v => !v)}>{open ? "Свернуть повторы" : `Все ${group.events.length} повторов`}<ChevronDown {...IC} /></button>
    {open && <ol className="rp-list">{group.events.map(e => <li key={e.id}><Link to={href(e.id)}>
      <time className="mono">{time(e.published_at)}</time><span className="mono rp-id">#{e.id}</span><span className="rp-status">{e.status_title}</span><b className="mono">{since(e.published_at, now)}</b><ChevronRight {...IC} size={15} />
    </Link></li>)}</ol>}
  </>;
}

/** Alarm card: evidence frame, how long it waits, place; repeats of the same camera and scenario are one card. */
function AlarmCard({ group, now }: { group: RepeatGroup; now: number }) {
  const e = group.latest; const many = group.events.length > 1; const href = useEventHref();
  const oldest = group.events[group.events.length - 1];
  return <li className={`mo-card is-${group.level} ${many ? "rp-stack" : ""}`} data-testid={many ? "repeat-group" : "alarm-card"}>
    <Link className="mo-card-main" to={href(e.id)} aria-label={`${e.title}, ${e.sector_name}, ${e.camera_name}`}>
      <div className="mb-frame">
        {e.evidence_url ? <img src={mediaUrl(e.evidence_url)} alt={`Кадр события #${e.id}`} loading="lazy" /> : <span className="mb-frame-none"><VideoOff size={24} strokeWidth={1.5} aria-hidden />Кадр не получен</span>}
        <LevelChip level={group.level} className="mb-ov-tl" />
        <span className="mb-ov mb-ov-tr mono">#{e.id}</span>
        <span className="mb-ov mb-ov-bl"><Timer {...IC} size={14} />ждёт <b>{since(oldest.published_at, now)}</b></span>
        {many && <span className="mb-ov mb-ov-br rp-count">{repeatCount(group)}</span>}
      </div>
      <div className="mo-card-body">
        <h2>{e.title}</h2>
        <p className="mo-place"><MapPin {...IC} size={14} />{shortSector(e.sector_name)} · {shortCamera(e.camera_name)}{e.zone_name ? ` · ${e.zone_name}` : ""}</p>
        <p className="mo-reason">{e.reason_text}</p>
        <p className="mo-foot"><span className={`mo-status is-${e.level}`}>{e.status_title}</span>{group.events.some(unconfirmed) && <span className="mo-flag"><ShieldAlert size={13} strokeWidth={1.75} aria-hidden />мастеру по таймауту</span>}<ChevronRight {...IC} /></p>
      </div>
    </Link>
    {many && <Repeats group={group} now={now} />}
  </li>;
}

function Row({ event, closed }: { event: EventSummary; closed?: boolean }) {
  const href = useEventHref();
  return <li><Link className="mo-row" to={href(event.id)}>
    <span className={`mm-dot is-${closed ? "closed" : event.level}`} aria-hidden />
    <span className="mo-row-main"><b>{event.title}</b><small>{shortSector(event.sector_name)} · {shortCamera(event.camera_name)}</small></span>
    <span className="mo-row-side"><small>{event.status_title}</small><time className="mono">{time(event.published_at, false)}</time></span>
  </Link></li>;
}

/** «Тревоги»: the operator queue on a phone. */
export function PhoneAlarms() {
  const now = useNow(1000);
  const { dashboard, waiting, inWork, history, critical } = useOperatorFeed();
  const [filter, setFilter] = useState<"all" | "red" | "yellow">("all");
  const groups = groupRepeats(waiting.filter(e => filter === "all" || e.level === filter));
  const sectors = dashboard.data?.sectors ?? [];
  const count = (level?: "red" | "yellow") => waiting.filter(e => !level || e.level === level).length;
  const href = useOperatorHref();
  return <div className="mb-screen mo-page" data-testid="operator-view">
    <header className="mb-hero">
      <div><h1>Тревоги</h1><p>{dashboard.data ? <>Ждут решения <b data-testid="active-event-count">{waiting.length}</b> · данные на <span className="mono">{time(dashboard.data.server_now)}</span></> : "Очередь оператора"}</p></div>
    </header>
    {dashboard.error ? <ErrorNotice error={dashboard.error} retry={dashboard.reload} /> : !dashboard.data ? <><div className="mb-skel" /><div className="mb-skel" /></> : <>
      {sectors.length > 0 && <nav className="mb-chips mo-sectors" aria-label="Секторы">{sectors.map(s => <Link key={s.sector_id} className={`mb-chip is-${s.state}`} to={href(`/operator/sectors/${s.sector_id}`)} title={s.reason_text}>
        <i /><span className="mono">{number(s.sector_id)}</span>{shortSector(s.name)}{s.open_red + s.open_yellow > 0 && <b>{s.open_red + s.open_yellow}</b>}
      </Link>)}</nav>}
      <div className="mb-chips" role="group" aria-label="Уровень">
        {([["all", "Все", undefined], ["red", "Тревога", "red"], ["yellow", "Внимание", "yellow"]] as const).map(([id, label, level]) => <button key={id} className={`mb-chip ${level ? `is-${level}` : ""}`} aria-pressed={filter === id} onClick={() => setFilter(id)}>{level && <i />}{label}<b>{count(level)}</b></button>)}
      </div>
      {groups.length ? <ol className="mo-cards">{groups.map(g => <AlarmCard key={g.key} group={g} now={now} />)}</ol>
        : <div className="mb-empty"><Check size={36} strokeWidth={1.75} aria-hidden /><strong>Активных тревог нет</strong><span>Камеры без наблюдения видны во вкладке «Камеры»: отсутствие тревог там не означает безопасность.</span></div>}
      {inWork.length > 0 && <details className="mb-more"><summary><span>В работе · ждём закрытия <b className="mono">{inWork.length}</b></span><ChevronRight {...IC} /></summary><div className="mb-more-body"><ol className="mo-rows">{inWork.slice(0, 30).map(e => <Row key={e.id} event={e} />)}</ol></div></details>}
      <details className="mb-more"><summary><span>Недавно завершено <b className="mono" data-testid="closed-event-count">{history.length}</b></span><ChevronRight {...IC} /></summary><div className="mb-more-body">{history.length ? <ol className="mo-rows">{history.map(e => <Row key={e.id} event={e} closed />)}</ol> : <p className="mb-muted">Завершённых событий за последние минуты нет.</p>}</div></details>
    </>}
    <EventAlarm event={critical} />
  </div>;
}

const ORDER: HumanAction[] = ["confirm", "false_alarm", "send_to_master"];
// tech.md 8.14: «Подтверждаю», «Ложное срабатывание», «Передать мастеру».
const TITLE: Partial<Record<HumanAction, string>> = { confirm: "Подтверждаю", false_alarm: "Ложное срабатывание", send_to_master: "Передать мастеру" };
const DONE: Partial<Record<HumanAction, string>> = { confirm: "Подтверждено", false_alarm: "Отмечено как ложное", send_to_master: "Передано мастеру" };

function LiveSection({ cameraId }: { cameraId: number }) {
  const updates = useUpdates();
  const view = useApi(() => api.GET("/api/cameras/{camera_id}/view", { params: { path: { camera_id: cameraId } } }), [cameraId], { refresh: [updates] });
  if (view.error) return <ErrorNotice error={view.error} compact retry={view.reload} />;
  if (!view.data) return <div className="mb-skel" style={{ height: 180 }} />;
  return <div className="mo-player"><LivePlayer view={view.data} compact /></div>;
}

/** Event card of the operator on a phone: frame with the box, why, where; the three decisions under the thumb. */
export function PhoneEventPage({ id, state }: { id: number; state: EventDetailState }) {
  const detail = state.detail; const href = useOperatorHref();
  return <div className="mb-screen mb-push mo-page mo-event" data-testid="incident-focus">
    <nav className="mb-navbar"><Link className="mb-back" to={href("/operator")}><ChevronLeft size={24} strokeWidth={2} aria-hidden />Тревоги</Link><span className="mb-navbar-title mono">#{id}{detail ? ` · ${time(detail.event.started_at)}` : ""}</span></nav>
    {state.error && <ErrorNotice error={state.error} retry={state.reload} />}
    {detail ? <PhoneEvent detail={detail} state={state} /> : !state.error && <><div className="mb-skel" /><div className="mb-skel" style={{ height: 140 }} /></>}
  </div>;
}

function PhoneEvent({ detail, state }: { detail: EventDetail; state: EventDetailState }) {
  const event = detail.event; const meta = useMeta(); const now = useNow(1000); const updates = useUpdates();
  const navigate = useNavigate(); const toast = useToast(); const href = useOperatorHref();
  const [comment, setComment] = useState(""); const [live, setLive] = useState(false); const [withRepeats, setWithRepeats] = useState(true);
  useEffect(() => { setComment(""); setLive(false); setWithRepeats(true); }, [event.id]);
  const actions = ORDER.filter(a => detail.allowed_actions.includes(a));
  const terminal = meta?.statuses.find(s => s.id === event.status)?.terminal;
  const feed = useApi(() => actions.length ? api.GET("/api/operator/dashboard") : Promise.resolve({ data: undefined }), [actions.length > 0], { refresh: [updates] });
  // Repeats of this situation still waiting for a verdict get the same decision when the operator wants it.
  const repeats = useMemo(() => {
    const waiting = (feed.data?.feed ?? []).filter(e => e.priority >= 2 || (e.escalated_by_timeout && e.operator_verdict === "none" && e.priority > 0));
    return groupRepeats(waiting).find(g => g.events.some(e => e.id === event.id))?.events.filter(e => e.id !== event.id) ?? [];
  }, [feed.data, event.id]);
  const bulk = useBulkAction(feed.reload);
  const busy = Boolean(state.busy || bulk.busy);
  const act = async (action: HumanAction) => {
    if (!await state.send(action, comment)) return;
    if (withRepeats && repeats.length) await bulk.run(`event:${event.id}`, repeats, action, comment);
    toast({ tone: action === "false_alarm" ? "neutral" : "green", title: `${DONE[action]} · #${event.id}` });
    navigate(href("/operator"));
  };
  const verdict = event.operator_verdict === "none" ? "Не зафиксирован" : meta?.statuses.find(s => s.id === event.operator_verdict)?.title ?? event.operator_verdict;
  return <>
    <EventAlarm event={event} actions={actions.map(a => ({ id: a, title: TITLE[a] ?? a, danger: a === "confirm" }))} busy={state.busy} onAct={a => void act(a as HumanAction)} media={detail.episode?.evidence[0] ? <Evidence detail={detail} compact /> : undefined} />
    <div className={`mo-hero-frame is-${event.level}`}><Evidence detail={detail} compact /></div>
    {event.clip && <ClipPlayer clip={event.clip} />}
    <header className={`mo-head is-${event.level}`}>
      <div className="mo-head-row"><LevelChip level={event.level} /><Status event={event} />{!terminal && <span className="mo-wait"><Timer {...IC} size={15} /><b className="mono">{since(event.published_at, now)}</b></span>}</div>
      <h1>{event.title}</h1>
      <p className="mo-reason-big">{event.reason_text}</p>
      {unconfirmed(event) && <p className="mm-flag"><ShieldAlert size={15} strokeWidth={1.75} aria-hidden />Передано мастеру по таймауту, ждёт вашего вердикта</p>}
    </header>
    <dl className="mb-card mb-facts">
      <div><dt><MapPin {...IC} size={15} />Место</dt><dd><Link to={href(`/operator/sectors/${event.sector_id}`)}>{event.sector_name}</Link><small><Link to={href(`/operator/cameras/${event.camera_id}`)}>{event.camera_name}</Link>{event.zone_name ? ` · зона «${event.zone_name}»` : ""}</small></dd></div>
      <div><dt><Clock {...IC} size={15} />Начало</dt><dd className="mono">{time(event.started_at)}<small>длится {duration(event.duration_s * 1000)}{event.ended_at ? "" : " · идёт"}</small></dd></div>
      <div><dt><Check {...IC} size={15} />Вердикт</dt><dd>{verdict}</dd></div>
    </dl>
    {actions.length > 0 && repeats.length > 0 && <label className="mm-repeats-opt"><input type="checkbox" checked={withRepeats} onChange={e => setWithRepeats(e.target.checked)} /><span><b>То же решение для повторов: ещё {repeats.length}</b><small>Та же камера и тот же сценарий</small></span></label>}
    {actions.length > 0 && <label className="mo-comment"><MessageSquareText {...IC} /><input aria-label="Комментарий к действию" value={comment} onChange={e => setComment(e.target.value)} placeholder="Комментарий (необязательно)" maxLength={500} /></label>}
    {state.actionError && <ErrorNotice error={state.actionError} compact retry={state.reload} />}
    {!actions.length && <p className="mm-done"><Check {...IC} />{terminal ? `Событие закрыто: ${event.status_title.toLowerCase()}.` : event.status === "sent_to_master" || event.status === "master_accepted" ? `Решение принято, событие у мастера: ${event.status_title.toLowerCase()}.` : "Для вашей роли действий по событию нет."}</p>}
    <details className="mb-more" onToggle={e => setLive((e.currentTarget as HTMLDetailsElement).open)}><summary><span><Radio {...IC} /> Эфир камеры сейчас</span><ChevronRight {...IC} /></summary><div className="mb-more-body">{live && <LiveSection cameraId={event.camera_id} />}<Link className="mo-link" to={href(`/operator/cameras/${event.camera_id}`)}>Открыть камеру<ChevronRight {...IC} /></Link></div></details>
    <details className="mb-more"><summary>Почему<ChevronRight {...IC} /></summary><div className="mb-more-body">{detail.why.length ? <dl className="od-facts">{detail.why.map((item, i) => <div key={`${item.label}-${i}`}><dt>{item.label}</dt><dd>{item.value}</dd></div>)}</dl> : <p className="mb-muted">Объяснение не получено.</p>}</div></details>
    <details className="mb-more"><summary>История эпизода<ChevronRight {...IC} /></summary><div className="mb-more-body"><EpisodeHistory detail={detail} /></div></details>
    <details className="mb-more"><summary><span>Действия людей <b className="mono">{detail.actions.length}</b></span><ChevronRight {...IC} /></summary><div className="mb-more-body"><History actions={detail.actions} /></div></details>
    {actions.length > 0 && <div className="mb-actionbar mo-actionbar">
      {actions.includes("confirm") && <button data-action="confirm" className="mb-btn mb-btn-accent" disabled={busy} onClick={() => void act("confirm")}>{state.busy === "confirm" ? "Сохраняем…" : withRepeats && repeats.length ? `${TITLE.confirm} · ×${repeats.length + 1}` : TITLE.confirm}</button>}
      <div className="mb-actionbar-row">
        {actions.filter(a => a !== "confirm").map(a => <button key={a} data-action={a} className="mb-btn mb-btn-s mb-btn-line" disabled={busy} onClick={() => void act(a)}>{state.busy === a ? "Сохраняем…" : TITLE[a]}</button>)}
      </div>
    </div>}
  </>;
}

/** Keeps the last decoded preview until the next one loads; off-screen tiles stop refreshing. */
function PreviewTile({ tile }: { tile: CameraTile }) {
  const host = useRef<HTMLAnchorElement>(null);
  const [visible, setVisible] = useState(true);
  useEffect(() => {
    const el = host.current; if (!el || typeof IntersectionObserver === "undefined") return;
    const observer = new IntersectionObserver(([entry]) => setVisible(entry.isIntersecting), { rootMargin: "160px" });
    observer.observe(el); return () => observer.disconnect();
  }, []);
  const tick = Math.floor(useNow(PREVIEW_MS) / PREVIEW_MS);
  const next = tile.preview_url && visible ? `${mediaUrl(tile.preview_url)}${tile.preview_url.includes("?") ? "&" : "?"}t=${tick}` : undefined;
  const [src, setSrc] = useState<string>();
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    if (!next) return;
    const image = new Image(); let live = true;
    image.onload = () => { if (live) { setSrc(next); setFailed(false); } };
    image.onerror = () => { if (live) setFailed(true); };
    image.src = next;
    return () => { live = false; };
  }, [next]);
  const s = tile.state; const href = useOperatorHref();
  const shown = Boolean(tile.preview_url && src && !failed);
  return <Link ref={host} className={`mo-tile is-${s.state}`} to={href(`/operator/cameras/${tile.camera.id}`)} aria-label={`Открыть ${tile.camera.name}`} data-testid="phone-camera">
    <div className="mb-frame">
      {shown ? <img src={src} alt="" /> : <span className="mb-frame-none"><VideoOff size={22} strokeWidth={1.5} aria-hidden />{s.state === "no_observation" ? "Нет наблюдения" : "Нет кадра"}</span>}
      {tile.broadcast?.status === "playing" && <span className="mb-ov mb-ov-tl mo-onair"><i />Эфир</span>}
      {/* Without a frame the placeholder already says «Нет наблюдения»: no second badge over it. */}
      {s.state !== "normal" && (shown || s.state !== "no_observation") && <span className={`mb-ov mb-ov-tr is-${s.state === "no_observation" ? "grey" : s.state}`}><StateIcon state={s.state} size={13} />{STATE_SHORT[s.state]}</span>}
      <span className="mo-tile-name">{shortCamera(tile.camera.name)}</span>
    </div>
    {(s.open_red > 0 || s.open_yellow > 0) && <span className="mo-tile-counts">{s.open_red > 0 && <b className="is-red">{s.open_red}</b>}{s.open_yellow > 0 && <b className="is-yellow">{s.open_yellow}</b>}</span>}
  </Link>;
}

/** «Камеры»: previews of every camera by sector; a sector chip narrows the grid. */
export function PhoneCameras({ sectorId }: { sectorId?: number }) {
  const updates = useUpdates(); const navigate = useNavigate(); const href = useOperatorHref();
  const dashboard = useApi(() => api.GET("/api/operator/dashboard"), [], { refresh: [updates] });
  const sectors = dashboard.data?.sectors ?? [];
  const ids = sectors.map(s => s.sector_id).join(",");
  const views = useApi(async () => {
    const results = await Promise.all(sectors.map(s => api.GET("/api/sectors/{sector_id}/view", { params: { path: { sector_id: s.sector_id } } })));
    const failed = results.find(r => r.error !== undefined);
    return failed ? { error: failed.error } : { data: results.flatMap(r => r.data?.cameras ?? []) };
  }, [ids], { refresh: [updates] });
  const tiles = views.data ?? [];
  const shownSectors = sectors.filter(s => !sectorId || s.sector_id === sectorId);
  const observed = tiles.filter(t => t.state.state !== "no_observation").length;
  return <div className="mb-screen mo-page mo-cameras" data-testid={sectorId ? "sector-view" : "cameras-view"}>
    <header className="mb-hero">
      <div><h1>Камеры</h1><p>{views.data ? <>Наблюдаются <b>{observed}</b> из <b>{tiles.length}</b> · превью каждые {PREVIEW_MS / 1000} с</> : "Превью камер по секторам"}</p></div>
    </header>
    {sectors.length > 0 && <nav className="mb-chips" aria-label="Секторы">
      <button className="mb-chip" aria-pressed={!sectorId} onClick={() => navigate(href("/operator/cameras"), { replace: true })}>Все<b>{tiles.length}</b></button>
      {sectors.map(s => <button key={s.sector_id} className={`mb-chip is-${s.state}`} aria-pressed={s.sector_id === sectorId} onClick={() => navigate(href(`/operator/sectors/${s.sector_id}`), { replace: true })}><i /><span className="mono">{number(s.sector_id)}</span>{shortSector(s.name)}</button>)}
    </nav>}
    {dashboard.error ? <ErrorNotice error={dashboard.error} retry={dashboard.reload} /> : views.error ? <ErrorNotice error={views.error} retry={views.reload} /> : !views.data ? <><div className="mb-skel" /><div className="mb-skel" /></>
      : shownSectors.map(sector => {
        const own = tiles.filter(t => t.camera.sector_id === sector.sector_id).sort((a, b) => RANK[a.state.state] - RANK[b.state.state] || a.camera.id - b.camera.id);
        return <section key={sector.sector_id} className={`mo-sector is-${sector.state}`} aria-label={sector.name}>
          <header className="mo-sector-head">
            <span className="mo-sector-num mono">{number(sector.sector_id)}</span>
            <span className="mo-sector-name"><b>{shortSector(sector.name)}</b><small>{sector.state === "no_observation" ? sector.reason_text : `${sector.cameras_total - sector.cameras_no_observation}/${sector.cameras_total} камер наблюдаются`}</small></span>
            <span className="mo-sector-counts">{sector.open_red > 0 && <b className="is-red">{sector.open_red}</b>}{sector.open_yellow > 0 && <b className="is-yellow">{sector.open_yellow}</b>}</span>
          </header>
          {own.length ? <div className="mo-grid">{own.map(tile => <PreviewTile key={tile.camera.id} tile={tile} />)}</div> : <p className="mb-muted">В секторе нет камер. Это не значит, что в нём безопасно.</p>}
        </section>;
      })}
  </div>;
}

/** Camera on a phone: live video with HUD, layers, facts and its open events (repeats grouped). */
export function PhoneCameraPage({ id }: { id: number }) {
  const updates = useUpdates(); const meta = useMeta(); const now = useNow(1000); const href = useOperatorHref();
  const view = useApi(() => api.GET("/api/cameras/{camera_id}/view", { params: { path: { camera_id: id } } }), [id], { refresh: [updates] });
  const events = useApi(() => api.GET("/api/events", { params: { query: { camera_id: id, limit: 200, include_demo: true } } }), [id], { refresh: [updates] });
  const [hud, setHud] = useState(true); const [zones, setZones] = useState(true); const [grid, setGrid] = useState(true);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if ((e.target as HTMLElement)?.closest?.("input,textarea,select,[contenteditable=true]")) return; if (e.key.toLowerCase() === "h") setHud(v => !v); };
    window.addEventListener("keydown", onKey); return () => window.removeEventListener("keydown", onKey);
  }, []);
  // The player's HUD listens to its own H key: one keypress keeps the chip, the key and the player in one state.
  const toggleHud = () => document.body.dispatchEvent(new KeyboardEvent("keydown", { key: "h", bubbles: true }));
  const list = events.data?.items ?? [];
  const open = list.filter(e => !meta?.statuses.find(s => s.id === e.status)?.terminal);
  const groups = groupRepeats(open);
  const data = view.data;
  return <div className="mb-screen mb-push mo-page mo-camera" data-testid="camera-view">
    <nav className="mb-navbar"><Link className="mb-back" to={href(data ? `/operator/sectors/${data.camera.sector_id}` : "/operator/cameras")}><ChevronLeft size={24} strokeWidth={2} aria-hidden />{data ? `Сектор ${number(data.camera.sector_id)}` : "Камеры"}</Link><span className="mb-navbar-title">{data ? shortCamera(data.camera.name) : ""}</span></nav>
    {view.error ? <ErrorNotice error={view.error} retry={view.reload} /> : !data ? <div className="mb-skel" /> : <>
      <div className="mo-player mo-player-main"><LivePlayer view={data} zones={hud && zones} grid={hud && grid} /></div>
      <div className="mb-chips" role="group" aria-label="Слои">
        <button className="mb-chip" aria-pressed={hud} onClick={toggleHud}>{hud ? <Eye {...IC} /> : <EyeOff {...IC} />}HUD</button>
        <button className="mb-chip" aria-pressed={hud && zones} disabled={!hud} onClick={() => setZones(v => !v)}><Shapes {...IC} />Зоны<b>{data.zones.length}</b></button>
        <button className="mb-chip" aria-pressed={hud && grid && Boolean(data.calibration)} disabled={!hud || !data.calibration} onClick={() => setGrid(v => !v)}><Grid3x3 {...IC} />Сетка 1 м</button>
      </div>
      <header className="mo-head">
        <div className="mo-head-row"><StateBadge state={data.state.state} text={data.state.state === "no_observation" ? data.state.reason_text : undefined} />{data.broadcast && <span className={`mo-onair-chip ${data.broadcast.status === "playing" ? "is-on" : ""}`}><Radio {...IC} size={14} />{data.broadcast.status === "playing" ? "Эфир" : "Эфир остановлен"}</span>}</div>
        <h1>{data.camera.name}</h1>
      </header>
      <dl className="mb-card mb-facts">
        <div><dt>Свежесть</dt><dd className="mono">{data.state.freshness_ms === null ? "нет эфира" : `${data.state.freshness_ms} мс`}</dd></div>
        <div><dt>Запись</dt><dd className="mono">{data.video ? `${data.video.width}×${data.video.height} · ${Number(data.video.fps.toFixed(1))} к/с` : "нет"}</dd></div>
        <div><dt>Калибровка</dt><dd>{data.calibration ? <span className="mono">RMSE {data.calibration.fit_rmse_m.toFixed(2)} м</span> : "нет · меры в ростах человека"}</dd></div>
        <div><dt>Открыто</dt><dd><span><b className="mo-n is-red">{data.state.open_red}</b> красных · <b className="mo-n is-yellow">{data.state.open_yellow}</b> жёлтых</span></dd></div>
      </dl>
      <h2 className="mb-section-h">Открытые события<b>{open.length}</b></h2>
      {events.error ? <ErrorNotice error={events.error} compact retry={events.reload} /> : groups.length ? <ol className="mo-cards is-compact">{groups.map(g => <AlarmCard key={g.key} group={g} now={now} />)}</ol>
        : <p className="mb-muted">Открытых событий нет{data.state.state === "no_observation" ? " — камера без наблюдения, это не значит, что всё безопасно" : ""}.</p>}
    </>}
  </div>;
}

/** /m/operator/events/:eventId (tech.md 8.14 v5): the phone card at any width; opening sends `view`. */
export function MobileEventRoute() {
  const { eventId } = useParams(); const id = Number(eventId);
  const state = useEventDetail(id);
  return <PhoneEventPage id={id} state={state} />;
}

export function OperatorShiftPage() {
  const href = useEventHref();
  return <ShiftSummary eventLink={href} testId="operator-shift" />;
}

/** /m/operator/sectors/:sectorId and /m/operator/cameras/:cameraId: the phone screens at any width. */
export function MobileSectorRoute() { const { sectorId } = useParams(); return <PhoneCameras sectorId={Number(sectorId)} />; }
export function MobileCameraRoute() { const { cameraId } = useParams(); return <PhoneCameraPage id={Number(cameraId)} />; }
