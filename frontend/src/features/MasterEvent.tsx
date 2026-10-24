import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Check, ChevronLeft, ChevronRight, Clock, Footprints, MapPin, ShieldAlert, Timer } from "lucide-react";
import { api } from "../api/client";
import { useApi } from "../api/useApi";
import type { EventDetail, HumanAction } from "../api/types";
import { useMeta, useUpdates } from "../components/AppShell";
import { since, useNow } from "../components/operator/kit";
import { duration, ErrorNotice, Status, time, useToast } from "../components/ui";
import { Evidence, History, type EventDetailState } from "./Incident";
import { LevelChip, unconfirmed, useBulkAction } from "./Master";
import { groupRepeats } from "./repeats";
import "../styles/mobile-shell.css";
import "../styles/mobile-master.css";

const IC = { size: 16, strokeWidth: 1.75, "aria-hidden": true } as const;

/** Ready phrases for «Принятые меры»: by scenario first, then the usual ones. A tap adds or removes a phrase. */
const MEASURES: Record<string, string[]> = {
  fall: ["Сотрудник осмотрен, вызван медпункт", "Оказана первая помощь", "Место падения огорожено"],
  running: ["Работник остановлен, проведён инструктаж", "Проход у техники перекрыт"],
  proximity: ["Техника остановлена", "Опасная зона огорожена", "Работник выведен из зоны"],
  phone: ["Проведена беседа, телефон убран", "Работник отстранён до инструктажа"],
  fence_crossing: ["Ограждение восстановлено", "Работник выведен за ограждение"],
  restricted_under: ["Конвейер остановлен", "Проход под грузом закрыт"],
  fire_smoking: ["Огонь потушен", "Курение пресечено, составлен акт"],
  no_harness: ["Работы на высоте остановлены", "Выдана и проверена страховочная привязь"],
  suspended_load: ["Груз опущен, зона очищена", "Проведён инструктаж стропальщика"],
  load_carrying: ["Груз перераспределён, выдана тележка"],
};
const COMMON = ["Проведён инструктаж на месте", "Работы приостановлены", "Нарушение устранено", "Нарушения нет: ложное срабатывание"];
const MAX = 500;

function toggleMeasure(text: string, phrase: string) {
  const parts = text.split(/\.\s+|\.$/).map(p => p.trim()).filter(Boolean);
  const next = parts.includes(phrase) ? parts.filter(p => p !== phrase) : [...parts, phrase];
  return next.length ? `${next.join(". ")}.` : "";
}

function Measures({ value, onChange, scenario }: { value: string; onChange: (value: string) => void; scenario: string }) {
  const phrases = [...(MEASURES[scenario] ?? []), ...COMMON];
  return <section className="mm-measures">
    <label className="mm-measures-label" htmlFor="mm-measures">Принятые меры <span>обязательно</span></label>
    <div className="mm-suggest" role="group" aria-label="Подсказки мер">
      {phrases.map(p => { const on = value.includes(p); return <button key={p} type="button" className={on ? "is-on" : ""} aria-pressed={on} onClick={() => onChange(toggleMeasure(value, p).slice(0, MAX))}>{on && <Check size={14} strokeWidth={2.4} aria-hidden />}{p}</button>; })}
    </div>
    <textarea id="mm-measures" data-testid="measures" value={value} onChange={e => onChange(e.target.value)} rows={4} placeholder="Что сделано на месте: остановил пресс, сотрудник осмотрен, ограждение восстановлено" maxLength={MAX} required />
    <small className="mm-count mono">{value.length}/{MAX}</small>
  </section>;
}

/** Master's card of one assignment (tech.md 8.14): what and where, «Принял, иду», then the measures and «Решено». */
export function MasterEventPage({ id, state }: { id: number; state: EventDetailState }) {
  const detail = state.detail;
  return <div className="mb-screen mb-push mm-page mm-detail-page" data-testid="master-detail">
    <nav className="mb-navbar"><Link className="mb-back ms-back" to="/master"><ChevronLeft size={24} strokeWidth={2} aria-hidden />Поручения</Link><span className="mb-navbar-title mono">#{id}{detail ? ` · ${time(detail.event.published_at, false)}` : ""}</span></nav>
    {state.error && <ErrorNotice error={state.error} retry={state.reload} />}
    {detail ? <MasterEvent detail={detail} state={state} /> : !state.error && <><div className="mb-skel" /><div className="mb-skel" style={{ height: 120 }} /></>}
  </div>;
}

function MasterEvent({ detail, state }: { detail: EventDetail; state: EventDetailState }) {
  const event = detail.event; const meta = useMeta(); const now = useNow(1000); const updates = useUpdates();
  const navigate = useNavigate(); const toast = useToast();
  const [report, setReport] = useState(""); const [notice, setNotice] = useState("");
  const [withRepeats, setWithRepeats] = useState(true);
  useEffect(() => { setReport(""); setNotice(""); setWithRepeats(true); }, [event.id]);
  const canAccept = detail.allowed_actions.includes("accept");
  const canResolve = detail.allowed_actions.includes("resolve");
  const terminal = meta?.statuses.find(s => s.id === event.status)?.terminal;
  // Repeats of this situation (same camera and scenario) waiting in the inbox in the same state get the same action.
  const inbox = useApi(() => canAccept || canResolve ? api.GET("/api/master/inbox") : Promise.resolve({ data: undefined }), [canAccept, canResolve], { refresh: [updates] });
  const repeats = useMemo(() => {
    const group = groupRepeats(inbox.data?.active ?? []).find(g => g.events.some(e => e.id === event.id));
    const status = canAccept ? "sent_to_master" : "master_accepted";
    return group?.events.filter(e => e.id !== event.id && e.status === status) ?? [];
  }, [inbox.data, event.id, canAccept]);
  const bulk = useBulkAction(inbox.reload);
  const busy = Boolean(state.busy || bulk.busy);
  const act = async (action: HumanAction) => {
    if (action === "resolve" && !report.trim()) { setNotice("Опишите принятые меры перед отправкой."); return; }
    const comment = action === "resolve" ? report : "";
    if (!await state.send(action, comment)) return;
    const others = withRepeats ? repeats : [];
    if (others.length) await bulk.run(`detail:${event.id}`, others, action, comment);
    if (action === "resolve") { toast({ tone: "green", title: `Отчёт сохранён · #${event.id} закрыто` }); setReport(""); navigate("/master"); }
    else setNotice("Принято. Сервер сохранил, что вы идёте на участок.");
  };
  return <>
    <div className={`mm-hero-frame is-${event.level}`}><Evidence detail={detail} compact /></div>
    <header className={`mm-head is-${event.level}`}>
      <div className="mm-head-row"><LevelChip level={event.level} /><Status event={event} /></div>
      <h1>{event.title}</h1>
      {!terminal && <p className="mm-wait"><Timer {...IC} size={18} /><span>{event.status === "master_accepted" ? "В работе" : "Ждёт"}</span><b className="mono">{since(event.published_at, now)}</b><small>с публикации</small></p>}
      {unconfirmed(event) && <p className="mm-flag"><ShieldAlert size={16} strokeWidth={1.75} aria-hidden />Не подтверждено оператором</p>}
    </header>
    <dl className="mb-card mb-facts">
      <div><dt><MapPin {...IC} size={15} />Где</dt><dd>{event.sector_name}<small>{event.camera_name}{event.zone_name ? ` · зона «${event.zone_name}»` : ""}</small></dd></div>
      <div><dt><Footprints {...IC} size={15} />Причина</dt><dd>{event.reason_text}</dd></div>
      <div><dt><Clock {...IC} size={15} />Начало</dt><dd className="mono">{time(event.started_at)} · {duration(event.duration_s * 1000)}</dd></div>
    </dl>
    {canResolve && <Measures value={report} onChange={setReport} scenario={event.scenario} />}
    {(canAccept || canResolve) && repeats.length > 0 && <label className="mm-repeats-opt"><input type="checkbox" checked={withRepeats} onChange={e => setWithRepeats(e.target.checked)} /><span><b>{canAccept ? "Принять" : "Закрыть"} и повторы: ещё {repeats.length}</b><small>Та же камера и тот же сценарий{canResolve ? ", те же меры" : ""}</small></span></label>}
    {state.actionError && <ErrorNotice error={state.actionError} compact retry={state.reload} />}
    {notice && <p className="action-notice mm-notice" role="status">{notice}</p>}
    {!canAccept && !canResolve && <p className="mm-done"><Check {...IC} />{terminal ? "Поручение закрыто." : "Действий для мастера сейчас нет."}</p>}
    <details className="mb-more"><summary>Почему и история<ChevronRight {...IC} /></summary>
      <div className="mb-more-body">
        {detail.why.length > 0 && <dl className="od-facts">{detail.why.map((item, i) => <div key={`${item.label}-${i}`}><dt>{item.label}</dt><dd>{item.value}</dd></div>)}</dl>}
        <History actions={detail.actions} />
      </div>
    </details>
    {(canAccept || canResolve) && <div className="mb-actionbar mm-actionbar">
      {canAccept && <button data-action="accept" className="mb-btn mb-btn-red" disabled={busy} onClick={() => void act("accept")}>{state.busy === "accept" || bulk.busy ? "Сохраняем…" : withRepeats && repeats.length ? `Принял, иду · ×${repeats.length + 1}` : "Принял, иду"}</button>}
      {canResolve && <button data-action="resolve" className="mb-btn mb-btn-green" disabled={busy || !report.trim()} onClick={() => void act("resolve")}><Check size={21} strokeWidth={2.2} aria-hidden />{state.busy === "resolve" || bulk.busy ? "Сохраняем…" : withRepeats && repeats.length ? `Решено · ×${repeats.length + 1}` : "Решено"}</button>}
    </div>}
  </>;
}
