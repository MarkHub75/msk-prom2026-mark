import { useEffect, useRef, useState, type ReactNode } from "react";
import { Link } from "react-router-dom";
import { Bell, BellRing, Check, ChevronDown, ChevronRight, ClipboardCheck, FileDown, MapPin, ShieldAlert, Timer } from "lucide-react";
import { api, apiError, mediaUrl, type ApiFailure } from "../api/client";
import { useApi } from "../api/useApi";
import { saveDownload } from "../api/download";
import type { CountRow, EventSummary, HumanAction } from "../api/types";
import { useRole } from "../roles";
import { PRODUCT } from "../brand";
import { askNotifications, systemNotify } from "../pwa";
import { useMeta, useUpdates } from "../components/AppShell";
import { useActorIdentity } from "../components/ActorIdentity";
import { since, StateIcon, useNow } from "../components/operator/kit";
import { useLevelTitle } from "../components/ops/levels";
import { duration, ErrorNotice, time, useToast } from "../components/ui";
import { groupRepeats, repeatCount, type RepeatGroup } from "./repeats";
import "../styles/mobile-shell.css";
import "../styles/mobile-master.css";
import "../styles/mobile-repeats.css";
import "../styles/v5.css";

const IC = { size: 16, strokeWidth: 1.75, "aria-hidden": true } as const;
const PAGE = 20;
export const unconfirmed = (e: EventSummary) => e.escalated_by_timeout && e.operator_verdict === "none";

/** Sound, vibration and a browser notification for a new assignment (tech.md 8.14). Audio needs one tap first. */
function useAlerts() {
  const audio = useRef<AudioContext>();
  const [enabled, setEnabled] = useState(false);
  const enable = async () => {
    try { audio.current = audio.current ?? new AudioContext(); await audio.current.resume(); } catch { /* no audio in this browser */ }
    await askNotifications();
    setEnabled(true);
  };
  const alert = (events: EventSummary[]) => {
    const ctx = audio.current;
    if (ctx && ctx.state === "running") {
      [0, .22].forEach(offset => { const osc = ctx.createOscillator(); const gain = ctx.createGain(); osc.connect(gain); gain.connect(ctx.destination); osc.frequency.value = 880; gain.gain.setValueAtTime(.08, ctx.currentTime + offset); gain.gain.exponentialRampToValueAtTime(.001, ctx.currentTime + offset + .18); osc.start(ctx.currentTime + offset); osc.stop(ctx.currentTime + offset + .2); });
    }
    navigator.vibrate?.([200, 100, 200]);
    // Same tag as the shell's hand-over notification: one notification per event, not two.
    const first = events[0];
    void systemNotify(`${PRODUCT}: новое поручение`, first.notification_text || `${first.title} · ${first.sector_name}`, { tag: `event-${first.id}`, url: `/master/events/${first.id}`, urgent: first.level === "red" });
  };
  return { enabled, enable, alert };
}

const BULK_TITLE: Partial<Record<HumanAction, string>> = { accept: "Принято в работу", resolve: "Закрыто с теми же мерами", confirm: "Подтверждено повторов", false_alarm: "Отмечено ложными", send_to_master: "Передано мастеру" };

/** One action for several events (a group of repeats): POST each, the server checks every transition. */
export function useBulkAction(onDone: () => void) {
  const { ensureActor } = useActorIdentity();
  const toast = useToast();
  const [busy, setBusy] = useState<string>();
  const run = async (key: string, events: EventSummary[], action: HumanAction, comment = "") => {
    if (busy || !events.length) return 0;
    setBusy(key);
    let saved = 0; let failure: ApiFailure | undefined;
    try {
      if (!await ensureActor()) return 0;
      for (const event of events) {
        try {
          const result = await api.POST("/api/events/{event_id}/actions", { params: { path: { event_id: event.id } }, body: { action, comment: comment.trim() } });
          if (result.error) failure = apiError(result.error); else saved++;
        } catch (error) { failure = apiError(error); }
      }
      if (saved) toast({ tone: "green", title: `${BULK_TITLE[action]}: ${saved}` });
      if (failure) toast({ tone: "red", title: saved ? `Не сохранено: ${events.length - saved}` : "Не сохранено", text: failure.message });
      return saved;
    } finally { setBusy(undefined); onDone(); }
  };
  return { busy, run };
}

export function LevelChip({ level, className = "" }: { level: EventSummary["level"]; className?: string }) {
  const title = useLevelTitle();
  return <span className={`mb-ov is-${level} ${className}`}><StateIcon state={level} size={14} />{title(level).replace(/ опасность$/, "")}</span>;
}

/** Card of an assignment: the frame, how long it waits, where to go, and the thumb-sized next step. A group of repeats is one card. */
function TaskCard({ group, now, fresh, bulk }: { group: RepeatGroup; now: number; fresh: boolean; bulk: ReturnType<typeof useBulkAction> }) {
  const event = group.latest; const many = group.events.length > 1;
  const waiting = group.events.filter(e => e.status === "sent_to_master");
  const accepted = waiting.length === 0;
  const oldest = group.events[group.events.length - 1];
  const [open, setOpen] = useState(false);
  return <li className={`mm-card is-${group.level} ${many ? "rp-stack" : ""} ${fresh ? "is-fresh" : ""}`} data-testid={many ? "repeat-group" : undefined}>
    <Link className="mm-card-main" to={`/master/events/${event.id}`} aria-label={`${event.title}, ${event.sector_name}`}>
      <div className="mb-frame">
        {event.evidence_url ? <img src={mediaUrl(event.evidence_url)} alt={`Кадр события #${event.id}`} loading="lazy" /> : <span className="mb-frame-none">Кадр не получен</span>}
        <LevelChip level={group.level} className="mb-ov-tl" />
        {fresh && <span className="mb-ov mb-ov-tr is-accent">Новое</span>}
        <span className={`mb-ov mb-ov-bl mm-timer ${accepted ? "" : "is-wait"}`}><Timer {...IC} size={14} />{accepted ? "в работе" : "ждёт"} <b>{since(oldest.published_at, now)}</b></span>
        {many && <span className="mb-ov mb-ov-br rp-count" title="Повторы той же камеры и сценария">{repeatCount(group)}</span>}
      </div>
      <div className="mm-card-body">
        <span className={`mm-state ${accepted ? "is-accepted" : ""}`}>{accepted ? "Вы приняли" : "Ждёт принятия"}</span>
        <h2>{event.title}</h2>
        <p className="mm-place"><MapPin {...IC} size={15} /><span>{event.sector_name}<small>{event.camera_name}{event.zone_name ? ` · ${event.zone_name}` : ""}</small></span></p>
        <p className="mm-reason">{event.reason_text}</p>
        {group.events.some(unconfirmed) && <p className="mm-flag"><ShieldAlert size={15} strokeWidth={1.75} aria-hidden />Не подтверждено оператором</p>}
      </div>
    </Link>
    <div className="mm-card-actions">
      {accepted
        ? <Link className="mb-btn mb-btn-s mb-btn-accent" to={`/master/events/${event.id}`}><Check size={19} strokeWidth={2.2} aria-hidden />Решено · отчитаться</Link>
        : <>
          <button className="mb-btn mb-btn-s mb-btn-accent" data-quick="accept" disabled={Boolean(bulk.busy)} onClick={() => void bulk.run(group.key, waiting, "accept")}>{bulk.busy === group.key ? "Сохраняем…" : waiting.length > 1 ? `Принял, иду · ×${waiting.length}` : "Принял, иду"}</button>
          <Link className="mb-btn mb-btn-s mb-btn-line mm-open" to={`/master/events/${event.id}`}>Открыть и принять</Link>
        </>}
    </div>
    {many && <>
      <button className="rp-expand" aria-expanded={open} onClick={() => setOpen(v => !v)}>{open ? "Свернуть повторы" : `Все ${group.events.length} повторов`}<ChevronDown {...IC} /></button>
      {open && <ol className="rp-list">{group.events.map(e => <li key={e.id}><Link to={`/master/events/${e.id}`}>
        <time className="mono">{time(e.published_at)}</time><span className="mono rp-id">#{e.id}</span><span className="rp-status">{e.status_title}</span><b className="mono">{since(e.published_at, now)}</b><ChevronRight {...IC} size={15} />
      </Link></li>)}</ol>}
    </>}
  </li>;
}

export function MasterPage() {
  const updates = useUpdates(); const [role] = useRole(); const now = useNow(1000);
  const inbox = useApi(() => api.GET("/api/master/inbox"), [role], { refresh: [updates] });
  const { enabled, enable, alert } = useAlerts();
  const bulk = useBulkAction(inbox.reload);
  const known = useRef<Set<number>>();
  const [fresh, setFresh] = useState<Set<number>>(new Set());
  const [limit, setLimit] = useState(PAGE);
  useEffect(() => {
    const active = inbox.data?.active; if (!active) return;
    const ids = new Set(active.map(e => e.id));
    if (known.current) { const added = active.filter(e => !known.current!.has(e.id)); if (added.length) { alert(added); setFresh(prev => new Set([...prev, ...added.map(e => e.id)])); } }
    known.current = ids;
  }, [inbox.data]); // eslint-disable-line react-hooks/exhaustive-deps
  const active = [...(inbox.data?.active ?? [])].sort((a, b) => Number(b.level === "red") - Number(a.level === "red") || b.published_at.localeCompare(a.published_at));
  const waitingCount = active.filter(e => e.status === "sent_to_master").length;
  const waiting = groupRepeats(active.filter(e => e.status === "sent_to_master"));
  const working = groupRepeats(active.filter(e => e.status !== "sent_to_master"));
  const shownWaiting = waiting.slice(0, limit);
  const shownWorking = working.slice(0, Math.max(0, limit - waiting.length));
  const card = (group: RepeatGroup) => <TaskCard key={group.key} group={group} now={now} fresh={group.events.some(e => fresh.has(e.id))} bulk={bulk} />;
  return <div className="mb-screen mm-page" data-testid="master-inbox">
    <header className="mb-hero">
      <div><h1>Поручения</h1><p>{inbox.data ? <>Ждут принятия <b>{waitingCount}</b> · в работе <b>{active.length - waitingCount}</b></> : "Рабочее место мастера"}</p></div>
      <button className={`mm-bell ${enabled ? "is-on" : ""}`} onClick={() => void enable()} aria-pressed={enabled} aria-label={enabled ? "Звук и уведомления включены" : "Включить звук и уведомления"}>{enabled ? <BellRing {...IC} size={20} /> : <Bell {...IC} size={20} />}<span>{enabled ? "Звук вкл." : "Звук"}</span></button>
    </header>
    {inbox.error ? <ErrorNotice error={inbox.error} retry={inbox.reload} /> : !inbox.data ? <><div className="mb-skel" /><div className="mb-skel" /></> : <>
      {active.length ? <>
        {shownWaiting.length > 0 && <><h2 className="mb-section-h">Ждут принятия<b>{waitingCount}</b></h2><ol className="mm-cards">{shownWaiting.map(card)}</ol></>}
        {shownWorking.length > 0 && <><h2 className="mb-section-h">В работе<b>{active.length - waitingCount}</b></h2><ol className="mm-cards">{shownWorking.map(card)}</ol></>}
      </> : <div className="mb-empty"><ClipboardCheck size={36} strokeWidth={1.5} aria-hidden /><strong>Активных поручений нет</strong><span>Новое придёт со звуком и вибрацией, если они включены.</span></div>}
      {waiting.length + working.length > limit && <button className="mm-more-btn" onClick={() => setLimit(l => l + PAGE)}>Показать ещё {Math.min(PAGE, waiting.length + working.length - limit)}</button>}
      <h2 className="mb-section-h">Недавно решено<b>{inbox.data.recent_resolved.length}</b></h2>
      <section className="mb-card mm-resolved">
        {inbox.data.recent_resolved.length ? <ol>{inbox.data.recent_resolved.map(e => <li key={e.id}><Link to={`/master/events/${e.id}`}>
          <span className={`mm-dot is-${e.level}`} aria-hidden /><span className="mm-res-main"><b>{e.title}</b><small>{e.sector_name} · {time(e.published_at, false)}</small></span><span className="mm-res-status">{e.status_title}</span>
        </Link></li>)}</ol> : <p className="mb-muted mm-pad">Решённых поручений пока нет.</p>}
        <Link className="mm-link" to="/master/shift">Сводка смены<ChevronRight {...IC} /></Link>
      </section>
      <p className="mb-asof">Данные на <span className="mono">{time(inbox.data.server_now)}</span></p>
    </>}
  </div>;
}

function Bars({ rows }: { rows: CountRow[] }) {
  const max = Math.max(1, ...rows.map(r => r.count));
  if (!rows.length) return <p className="mb-muted">За смену событий нет.</p>;
  return <ul className="mm-bars">{[...rows].sort((a, b) => b.count - a.count).map(row => <li key={row.key}>
    <div className="mm-bar-top"><span>{row.title}</span><b className="mono">{row.count}</b></div>
    <div className="mm-bar" role="img" aria-label={`${row.title}: ${row.count}, подтверждено ${row.confirmed}, ложных ${row.false_alarm}`}><i style={{ width: `${row.count / max * 100}%` }} /><em style={{ width: `${row.confirmed / max * 100}%` }} /></div>
    <small>подтверждено {row.confirmed} · ложных {row.false_alarm}</small>
  </li>)}</ul>;
}

/** Shift totals from GET /api/master/shift (the operator may read it too): counters come from the server, never recounted. */
export function ShiftSummary({ eventLink, testId, children }: { eventLink: (id: number) => string; testId: string; children?: ReactNode }) {
  const updates = useUpdates(); const [role] = useRole(); const meta = useMeta();
  const [at, setAt] = useState<string>();
  const shift = useApi(() => api.GET("/api/master/shift", { params: { query: at ? { at } : {} } }), [role, at], { refresh: [updates] });
  const data = shift.data;
  const confirmed = data?.by_sector.reduce((s, r) => s + r.confirmed, 0) ?? 0;
  const falseAlarm = data?.by_sector.reduce((s, r) => s + r.false_alarm, 0) ?? 0;
  const open = Math.max(0, (data?.total ?? 0) - confirmed - falseAlarm);
  const pct = (n: number) => `${data?.total ? n / data.total * 100 : 0}%`;
  const previous = () => { if (data) setAt(new Date(Date.parse(data.start) - 60_000).toISOString()); };
  // tech.md 8.31: the same summary as A4 PDF; ?at= of the shown shift, the name from Content-Disposition.
  const [pdf, setPdf] = useState<{ busy: boolean; error?: ApiFailure }>({ busy: false });
  useEffect(() => { setPdf({ busy: false }); }, [at]);
  const savePdf = async () => {
    if (!data) return;
    setPdf({ busy: true });
    const error = await saveDownload(() => api.GET("/api/master/shift.pdf", { params: { query: at ? { at } : {} }, parseAs: "blob" }), `shift-${data.start.slice(0, 10)}.pdf`);
    setPdf({ busy: false, error });
  };
  const day = (iso: string) => new Intl.DateTimeFormat("ru-RU", { day: "numeric", month: "short", timeZone: meta?.timezone ?? "Europe/Moscow" }).format(new Date(iso));
  return <div className="mb-screen mm-page mm-shift" data-testid={testId}>
    <header className="mb-hero">
      <div><h1>{data?.title ?? "Смена"}</h1><p>{data ? <><span className="mono">{day(data.start)} {time(data.start, false)} – {time(data.end, false)}</span>{at ? " · прошедшая" : " · текущая"}</> : "Сводка смены"}</p></div>
      <button type="button" className="v5-pdf" onClick={() => void savePdf()} disabled={!data || pdf.busy} aria-busy={pdf.busy} data-testid="shift-pdf"><FileDown {...IC} />{pdf.busy ? "Готовим…" : "PDF"}</button>
    </header>
    {pdf.error && <ErrorNotice error={pdf.error} compact retry={() => void savePdf()} pending="Отдаст сводку смены одним файлом A4 для печати и рассылки." />}
    <div className="mm-seg" role="group" aria-label="Какая смена"><button className={!at ? "selected" : ""} aria-pressed={!at} onClick={() => setAt(undefined)}>Текущая</button><button className={at ? "selected" : ""} aria-pressed={Boolean(at)} onClick={previous} disabled={!data}>Предыдущая</button></div>
    {shift.error ? <ErrorNotice error={shift.error} retry={shift.reload} /> : !data ? <div className="mb-skel" /> : <>
      <section className="mb-card mm-total">
        <div className="mm-total-top"><span>Событий за смену</span><b className="mm-total-n">{data.total}</b></div>
        <div className="mm-split" aria-hidden><i className="is-confirmed" style={{ width: pct(confirmed) }} /><i className="is-false" style={{ width: pct(falseAlarm) }} /><i className="is-open" style={{ width: pct(open) }} /></div>
        <ul className="mm-legend">
          <li className="is-confirmed"><i /><span>Подтверждено</span><b>{confirmed}</b></li>
          <li className="is-false"><i /><span>Ложных</span><b>{falseAlarm}</b></li>
          <li className="is-open"><i /><span>Без вердикта</span><b>{open}</b></li>
        </ul>
      </section>
      <h2 className="mb-section-h">По секторам</h2>
      <section className="mb-card mm-block"><Bars rows={data.by_sector} /></section>
      <h2 className="mb-section-h">По сценариям</h2>
      <section className="mb-card mm-block"><Bars rows={data.by_scenario} /></section>
      <h2 className="mb-section-h">Подтверждённые<b>{data.events.length}</b></h2>
      <section className="mb-card mm-resolved">
        {data.events.length ? <ol>{data.events.map(e => <li key={e.id}><Link to={eventLink(e.id)}>
          <time className="mono mm-res-time">{time(e.started_at, false)}</time><span className="mm-res-main"><b>{e.title}</b><small>{e.sector_name} · {e.reason_text}</small></span><span className="mm-res-status">{e.status_title}<small className="mono">{duration(e.duration_s * 1000)}</small></span>
        </Link></li>)}</ol>
          : <p className="mb-muted mm-pad">Подтверждённых событий в эту смену нет. Это не значит, что нарушений не было: часть событий может ждать вердикта.</p>}
      </section>
      {children}
    </>}
  </div>;
}

export function ShiftPage() { return <ShiftSummary eventLink={id => `/master/events/${id}`} testId="master-shift" />; }
