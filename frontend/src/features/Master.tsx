import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { Bell, BellRing, ChevronRight, ClipboardCheck, ShieldAlert, Timer } from "lucide-react";
import { api, mediaUrl } from "../api/client";
import { useApi } from "../api/useApi";
import type { CountRow, EventSummary } from "../api/types";
import { useRole } from "../roles";
import { PRODUCT } from "../brand";
import { useMeta, useUpdates } from "../components/AppShell";
import { LevelTag, since, useNow } from "../components/operator/kit";
import { duration, ErrorNotice, Loading, time } from "../components/ui";
import "../styles/master.css";

const IC = { size: 16, strokeWidth: 1.75, "aria-hidden": true } as const;
const PAGE = 20;
const unconfirmed = (e: EventSummary) => e.escalated_by_timeout && e.operator_verdict === "none";

/** Sound, vibration and a browser notification for a new assignment (tech.md 8.14). Audio needs one tap first. */
function useAlerts() {
  const audio = useRef<AudioContext>();
  const [enabled, setEnabled] = useState(false);
  const enable = async () => {
    try { audio.current = audio.current ?? new AudioContext(); await audio.current.resume(); } catch { /* no audio in this browser */ }
    if ("Notification" in window && Notification.permission === "default") { try { await Notification.requestPermission(); } catch { /* denied */ } }
    setEnabled(true);
  };
  const alert = (events: EventSummary[]) => {
    const ctx = audio.current;
    if (ctx && ctx.state === "running") {
      [0, .22].forEach(offset => { const osc = ctx.createOscillator(); const gain = ctx.createGain(); osc.connect(gain); gain.connect(ctx.destination); osc.frequency.value = 880; gain.gain.setValueAtTime(.08, ctx.currentTime + offset); gain.gain.exponentialRampToValueAtTime(.001, ctx.currentTime + offset + .18); osc.start(ctx.currentTime + offset); osc.stop(ctx.currentTime + offset + .2); });
    }
    navigator.vibrate?.([200, 100, 200]);
    if ("Notification" in window && Notification.permission === "granted") {
      const first = events[0];
      try { new Notification(`${PRODUCT}: новое поручение`, { body: first.notification_text || `${first.title} · ${first.sector_name}`, tag: `event-${first.id}` }); } catch { /* mobile browsers need a service worker */ }
    }
  };
  return { enabled, enable, alert };
}

function Card({ event, now, fresh }: { event: EventSummary; now: number; fresh: boolean }) {
  const accepted = event.status === "master_accepted";
  return <li className={`ms-card ms-${event.level} ${fresh ? "is-fresh" : ""}`}>
    <Link to={`/master/events/${event.id}`}>
      <div className="ms-card-media">
        {event.evidence_url ? <img src={mediaUrl(event.evidence_url)} alt={`Кадр события #${event.id}`} loading="lazy" /> : <span className="ms-noimg">Кадр не получен</span>}
        <span className="ms-card-level"><LevelTag level={event.level} /></span>
        {fresh && <span className="ms-card-new">Новое</span>}
      </div>
      <div className="ms-card-body">
        <div className="ms-card-top"><span className={`ms-status ${accepted ? "is-accepted" : ""}`}>{accepted ? "Вы приняли" : "Ждёт принятия"}</span><span className="ms-timer"><Timer {...IC} size={15} /><b className="mono">{since(event.published_at, now)}</b></span></div>
        <h2>{event.title}</h2>
        <p className="ms-place">{event.sector_name}<span>{event.camera_name}{event.zone_name ? ` · ${event.zone_name}` : ""}</span></p>
        <p className="ms-reason">{event.reason_text}</p>
        {unconfirmed(event) && <p className="ms-unconfirmed"><ShieldAlert size={15} strokeWidth={1.75} aria-hidden />Не подтверждено оператором</p>}
        <span className="ms-card-go">{accepted ? "Отчитаться о мерах" : "Открыть и принять"}<ChevronRight {...IC} /></span>
      </div>
    </Link>
  </li>;
}

export function MasterPage() {
  const updates = useUpdates(); const [role] = useRole(); const now = useNow(1000);
  const inbox = useApi(() => api.GET("/api/master/inbox"), [role], { refresh: [updates] });
  const { enabled, enable, alert } = useAlerts();
  const known = useRef<Set<number>>();
  const [fresh, setFresh] = useState<Set<number>>(new Set());
  const [limit, setLimit] = useState(PAGE);
  useEffect(() => {
    const active = inbox.data?.active; if (!active) return;
    const ids = new Set(active.map(e => e.id));
    if (known.current) { const added = active.filter(e => !known.current!.has(e.id)); if (added.length) { alert(added); setFresh(prev => new Set([...prev, ...added.map(e => e.id)])); } }
    known.current = ids;
  }, [inbox.data]); // eslint-disable-line react-hooks/exhaustive-deps
  const active = [...(inbox.data?.active ?? [])].sort((a, b) => Number(a.status === "master_accepted") - Number(b.status === "master_accepted") || Number(b.level === "red") - Number(a.level === "red") || b.published_at.localeCompare(a.published_at));
  const waiting = active.filter(e => e.status === "sent_to_master").length;
  return <div className="ms-page" data-testid="master-inbox">
    <header className="ms-head">
      <div><h1>Поручения</h1><p>{inbox.data ? <>Ждут принятия <b>{waiting}</b> · в работе <b>{active.length - waiting}</b></> : "Рабочее место мастера"}</p></div>
      <button className={`ms-bell ${enabled ? "is-on" : ""}`} onClick={() => void enable()} aria-pressed={enabled} aria-label={enabled ? "Звук и уведомления включены" : "Включить звук и уведомления"}>{enabled ? <BellRing {...IC} size={20} /> : <Bell {...IC} size={20} />}<span>{enabled ? "Звук вкл." : "Включить звук"}</span></button>
    </header>
    {inbox.error ? <ErrorNotice error={inbox.error} retry={inbox.reload} /> : !inbox.data ? <Loading text="Получаем поручения" /> : <>
      {active.length ? <ol className="ms-cards">{active.slice(0, limit).map(e => <Card key={e.id} event={e} now={now} fresh={fresh.has(e.id)} />)}</ol>
        : <div className="ms-empty"><ClipboardCheck size={34} strokeWidth={1.5} aria-hidden /><strong>Активных поручений нет</strong><span>Новое придёт со звуком и вибрацией, если они включены.</span></div>}
      {active.length > limit && <button className="ms-more-btn" onClick={() => setLimit(l => l + PAGE)}>Показать ещё {Math.min(PAGE, active.length - limit)} из {active.length - limit}</button>}
      <section className="ms-resolved">
        <h2>Недавно решено <span className="mono">{inbox.data.recent_resolved.length}</span></h2>
        {inbox.data.recent_resolved.length ? <ol>{inbox.data.recent_resolved.map(e => <li key={e.id}><Link to={`/master/events/${e.id}`}><LevelTag level={e.level} /><span><b>{e.title}</b><small>{e.sector_name} · {time(e.published_at, false)}</small></span><span className="ms-res-status">{e.status_title}</span></Link></li>)}</ol> : <p className="ms-muted">Решённых поручений пока нет.</p>}
        <Link className="ms-link" to="/master/shift">Сводка смены<ChevronRight {...IC} /></Link>
      </section>
      <p className="ms-asof">Данные на <span className="mono">{time(inbox.data.server_now)}</span></p>
    </>}
  </div>;
}

function Bars({ rows }: { rows: CountRow[] }) {
  const max = Math.max(1, ...rows.map(r => r.count));
  if (!rows.length) return <p className="ms-muted">Событий нет.</p>;
  return <ul className="ms-bars">{[...rows].sort((a, b) => b.count - a.count).map(row => <li key={row.key}>
    <div className="ms-bar-top"><span>{row.title}</span><b className="mono">{row.count}</b></div>
    <div className="ms-bar"><i style={{ width: `${row.count / max * 100}%` }} /><em style={{ width: `${row.confirmed / max * 100}%` }} /></div>
    <small>подтверждено {row.confirmed} · ложных {row.false_alarm}</small>
  </li>)}</ul>;
}

export function ShiftPage() {
  const updates = useUpdates(); const [role] = useRole(); const meta = useMeta();
  const [at, setAt] = useState<string>();
  const shift = useApi(() => api.GET("/api/master/shift", { params: { query: at ? { at } : {} } }), [role, at], { refresh: [updates] });
  const data = shift.data;
  const confirmed = data?.by_sector.reduce((s, r) => s + r.confirmed, 0) ?? 0;
  const falseAlarm = data?.by_sector.reduce((s, r) => s + r.false_alarm, 0) ?? 0;
  const previous = () => { if (data) setAt(new Date(Date.parse(data.start) - 60_000).toISOString()); };
  const day = (iso: string) => new Intl.DateTimeFormat("ru-RU", { day: "numeric", month: "short", timeZone: meta?.timezone ?? "Europe/Moscow" }).format(new Date(iso));
  return <div className="ms-page ms-shift" data-testid="master-shift">
    <header className="ms-head">
      <div><h1>{data?.title ?? "Смена"}</h1><p>{data ? <><span className="mono">{day(data.start)} {time(data.start, false)} – {time(data.end, false)}</span>{at ? " · прошедшая" : " · текущая"}</> : "Сводка смены"}</p></div>
    </header>
    <div className="ms-seg" role="group" aria-label="Какая смена"><button className={!at ? "selected" : ""} aria-pressed={!at} onClick={() => setAt(undefined)}>Текущая</button><button className={at ? "selected" : ""} aria-pressed={Boolean(at)} onClick={previous} disabled={!data}>Предыдущая</button></div>
    {shift.error ? <ErrorNotice error={shift.error} retry={shift.reload} /> : !data ? <Loading text="Считаем смену" /> : <>
      <div className="ms-kpis">
        <div className="ms-kpi-main"><span>Всего событий</span><b>{data.total}</b></div>
        <div><span>Подтверждено</span><b>{confirmed}</b></div>
        <div><span>Ложных</span><b>{falseAlarm}</b></div>
        <div><span>Без вердикта</span><b>{Math.max(0, data.total - confirmed - falseAlarm)}</b></div>
      </div>
      <section className="ms-block"><h2>По секторам</h2><Bars rows={data.by_sector} /></section>
      <section className="ms-block"><h2>По сценариям</h2><Bars rows={data.by_scenario} /></section>
      <section className="ms-block"><h2>Подтверждённые <span className="mono">{data.events.length}</span></h2>
        {data.events.length ? <ol className="ms-confirmed">{data.events.map(e => <li key={e.id}><Link to={`/master/events/${e.id}`}><time className="mono">{time(e.started_at, false)}</time><span><b>{e.title}</b><small>{e.sector_name} · {e.reason_text}</small></span><span className="ms-res-status">{e.status_title}<small className="mono">{duration(e.duration_s * 1000)}</small></span></Link></li>)}</ol>
          : <p className="ms-muted">Подтверждённых событий в эту смену нет. Это не значит, что нарушений не было: часть событий может ждать вердикта.</p>}
      </section>
      <p className="ms-asof">Счётчики — с сервера, без пересчёта на устройстве.</p>
    </>}
  </div>;
}
