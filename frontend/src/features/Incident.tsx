import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";
import { useLevelTitle } from "../components/ops/levels";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, Check, Copy, Cpu, MessageSquareText, ShieldAlert } from "lucide-react";
import { api } from "../api/client";
import { useApi } from "../api/useApi";
import type { EventAction, EventDetail, EventSummary, HumanAction } from "../api/types";
import { useRole } from "../roles";
import { EventAlarm } from "../components/AlarmTakeover";
import { useMeta, useUpdates, roleTitles } from "../components/AppShell";
import { EvidenceFrame } from "../components/Media";
import { ClipPlayer } from "../components/ClipPlayer";
import { useActorIdentity } from "../components/ActorIdentity";
import { END_REASON, Into, LevelTag, since, StateBadge, useNow } from "../components/operator/kit";
import { LivePlayer } from "./Camera";
import { ACTIONS, useEventActions } from "./eventActions";
import { MasterEventPage } from "./MasterEvent";
import { IdentityPanel, identityText } from "./IdentityPanel";
import { PhoneEventPage } from "./OperatorPhone";
import { usePhone } from "../components/usePhone";
import "../styles/incident-review.css";
import "../styles/operator-depth.css";
import { duration, Empty, ErrorNotice, Loading, number, Status, time } from "../components/ui";

const IC = { size: 15, strokeWidth: 1.75, "aria-hidden": true } as const;
const HISTORY: Record<EventAction["action"], string> = {published:"Событие опубликовано",viewed:"Открыто оператором",confirmed:"Событие подтверждено",false_alarm:"Ложное срабатывание",sent_to_master:"Передано мастеру",level_escalated:"Повышен уровень",timeout_escalated:"Эскалация по таймауту",master_accepted:"Мастер принял в работу",resolved:"Меры приняты · завершено",auto_finished:"Автоматически завершено",superseded:"Заменено новым событием",identified:"Указан нарушитель"};
// tech.md 8.14: buttons «Подтверждаю», «Ложное срабатывание», «Передать мастеру» on keys 1, 2, 3.
const KEYS: Partial<Record<HumanAction, string>> = { confirm: "1", false_alarm: "2", send_to_master: "3" };
const BY_KEY: Record<string, HumanAction> = { "1": "confirm", "2": "false_alarm", "3": "send_to_master" };
const unconfirmed = (event: EventSummary) => event.escalated_by_timeout && event.operator_verdict === "none";

export function useEventDetail(id: number) {
  const [role] = useRole(); const updates = useUpdates();
  const { actor } = useActorIdentity();
  const request = useApi(() => api.GET("/api/events/{event_id}", {params:{path:{event_id:id}}}), [id,role], {refresh: [updates]});
  const [result, setResult] = useState<{ detail: EventDetail; rest: EventDetail | undefined; identity: string }>();
  const viewed = useRef(new Set<string>());
  const identity = `${role}:${id}`;
  const rest = useRef(request.data); rest.current = request.data;
  const current = result?.identity === identity && result.rest === request.data ? result.detail : request.data;
  const detail = !request.error && !request.loading && current?.event.id === id ? current : undefined;
  const { busy, actionError, send: post } = useEventActions(id, detail, identity);
  useEffect(() => { setResult(undefined); }, [id,role]);
  const send = useCallback(async (action: HumanAction, comment = "") => {
    const done = await post(action, comment);
    if (done && done.saved !== true) setResult({detail:done.saved,rest:rest.current,identity});
    return Boolean(done);
  }, [post,identity]);
  useEffect(() => {
    const key = `${identity}:${detail?.event.published_at}`;
    if (actor.trim() && detail?.allowed_actions.includes("view") && !viewed.current.has(key)) {
      viewed.current.add(key);
      void send("view").then(ok => { if (!ok) viewed.current.delete(key); });
    }
  }, [detail,identity,send,actor]);
  // A PATCH answer (identity) replaces the detail the same way an action answer does.
  const apply = useCallback((next: EventDetail) => setResult({detail:next,rest:rest.current,identity}), [identity]);
  return {detail,loading:request.loading,error:request.error,reload:request.reload,busy,actionError,send,apply};
}

function Panel({ title, aside, children, className = "" }: { title: string; aside?: ReactNode; children: ReactNode; className?: string }) {
  return <section className={`ic-panel ${className}`}><h2>{title}{aside !== undefined && <span>{aside}</span>}</h2>{children}</section>;
}

/** Who did what: people and the system, oldest first. */
export function History({ actions }: { actions: EventAction[] }) {
  const meta = useMeta();
  if (!actions.length) return <p className="ic-muted">Действий пока нет.</p>;
  return <ol className="ic-rail">{[...actions].sort((a,b)=>a.at.localeCompare(b.at)).map(action => {
    const who = action.actor_role === "system" ? "Система" : action.actor_name || roleTitles[action.actor_role];
    return <li key={action.id} className={`ic-rail-${action.actor_role}`}>
      <time className="mono">{time(action.at)}</time><i />
      <div><strong>{HISTORY[action.action]}</strong><span>{who}{action.actor_role !== "system" && <> · {roleTitles[action.actor_role]}</>}{action.to_status && <> → {meta?.statuses.find(s=>s.id===action.to_status)?.title ?? action.to_status}</>}</span>{action.comment && <blockquote>{action.comment}</blockquote>}</div>
    </li>;
  })}</ol>;
}

/** Episode life: start → published (yellow/red) → escalated to red → end. Video positions next to wall time. */
export function EpisodeHistory({ detail }: { detail: EventDetail }) {
  const meta = useMeta(); const event = detail.event; const ep = detail.episode;
  const level = (id: "red" | "yellow") => meta?.levels.find(l => l.id === id)?.title ?? (id === "red" ? "Красная опасность" : "Жёлтая опасность");
  const steps: { key: string; at?: string | null; ms?: number | null; tone: "red" | "yellow" | "neutral"; title: string; note?: string }[] = [];
  steps.push({ key: "start", at: event.started_at, ms: ep?.start_ms, tone: "neutral", title: "Начало эпизода", note: ep ? `${ep.scenario_title} · трек ${ep.subject}` : undefined });
  const initial = ep?.level_initial ?? (event.red_at && event.red_at === event.published_at ? "red" : "yellow");
  steps.push({ key: "pub", at: event.published_at, ms: ep?.confirm_ms, tone: initial, title: `Подтверждено правилом: ${level(initial)}`, note: ep?.reason_text });
  if (event.red_at && (initial === "yellow" || ep?.escalate_ms != null)) steps.push({ key: "red", at: event.red_at, ms: ep?.escalate_ms, tone: "red", title: `Повышено до: ${level("red")}` });
  if (ep && ep.uncertain_ms > 0) steps.push({ key: "unc", tone: "neutral", title: `Потеря видимости ${Math.round(ep.uncertain_ms / 1000)} с`, note: "Кадры без наблюдения внутри эпизода" });
  steps.push(event.ended_at ? { key: "end", at: event.ended_at, ms: ep?.end_ms, tone: "neutral", title: "Эпизод закончился", note: ep ? END_REASON[ep.end_reason] : undefined } : { key: "end", tone: event.level, title: "Эпизод продолжается", note: `Идёт ${duration(event.duration_s * 1000)}` });
  return <ol className="ic-episode">{steps.map(step => <li key={step.key} className={`ic-ep-${step.tone}`}>
    <i />
    <div><strong>{step.title}</strong>{step.note && <span>{step.note}</span>}</div>
    <time className="mono">{step.at ? time(step.at) : ""}{step.ms != null && <small>запись {duration(step.ms)}</small>}</time>
  </li>)}</ol>;
}

function Hash({ value }: { value: string | null }) {
  const [copied, setCopied] = useState(false);
  if (!value) return <>не получен</>;
  const copy = () => { void navigator.clipboard?.writeText(value).then(() => { setCopied(true); setTimeout(() => setCopied(false), 1200); }); };
  return <span className="ic-hash"><span className="mono" title={value}>{value.slice(0, 12)}…{value.slice(-6)}</span><button type="button" onClick={copy} aria-label="Скопировать хеш">{copied ? <Check {...IC} size={13} /> : <Copy {...IC} size={13} />}</button></span>;
}

export function Provenance({ detail }: { detail: EventDetail }) {
  const p = detail.provenance; const ep = detail.episode;
  return <dl className="od-facts ic-prov">
    <div><dt>Бэкенд</dt><dd><Cpu {...IC} size={13} /> {p.backend === "linq" ? "LinQ TPU" : p.backend === "local" ? "CPU · local" : "не указан"}{p.fake && <span className="ic-fake">синтетические детекции</span>}</dd></div>
    <div><dt>Режим</dt><dd>{detail.event.mode === "replay" ? "Запись · повтор эфира" : "Демо"}{detail.event.is_demo && <span className="ic-fake">демо-данные</span>}</dd></div>
    <div><dt>Детекция</dt><dd className="mono">{p.det_model ?? "не указана"}</dd></div>
    <div><dt>Поза</dt><dd className="mono">{p.pose_model ?? "не использовалась"}</dd></div>
    <div><dt>Задача · анализ</dt><dd className="mono">{p.job_id !== null ? `#${p.job_id}` : "—"} · {ep ? `#${ep.analysis_id}` : "—"} v{p.analysis_version ?? "—"}</dd></div>
    {ep && <div><dt>Метод · уверенность</dt><dd>{ep.method} · <span className="mono">{ep.confidence.toFixed(2)}</span></dd></div>}
    <div><dt>SHA-256 кадра</dt><dd><Hash value={p.evidence_sha256} /></dd></div>
    <div><dt>SHA-256 видео</dt><dd><Hash value={p.video_sha256} /></dd></div>
    {Object.keys(p.rule_params).length > 0 && <div><dt>Параметры правила</dt><dd className="mono ic-params">{Object.entries(p.rule_params).map(([k, v]) => <span key={k}>{k}={v}</span>)}</dd></div>}
  </dl>;
}

/** Evidence frame with a callout pinned to the object that triggered the event. */
export function Evidence({ detail, compact = false }: { detail: EventDetail; compact?: boolean }) {
  const host = useRef<HTMLDivElement>(null);
  const event = detail.event; const evidence = detail.episode?.evidence[0];
  if (!evidence) return <Empty title="Доказательство отсутствует" text="Сервер не передал кадр для этого события." />;
  const target = evidence.objects.find(o => o.tags.some(t => t.level === event.level)) ?? evidence.objects.find(o => o.tags.some(t => t.level)) ?? evidence.objects[0];
  const left = target ? target.bbox[2] < .62 : true;
  return <div ref={host} className={`ic-evidence ${compact ? "is-compact" : ""}`}>
    <EvidenceFrame evidence={evidence} camera={event.camera_name} level={event.level} />
    {target && <Into host={host} selector=".evidence-image-wrap" deps={[evidence.id]}>
      <div className={`ic-callout ic-callout-${event.level} ${left ? "to-right" : "to-left"}`} style={left ? { left: `${target.bbox[2] * 100}%`, top: `${target.bbox[1] * 100}%` } : { right: `${(1 - target.bbox[0]) * 100}%`, top: `${target.bbox[1] * 100}%` }}>
        <b>{event.title}</b><span>{event.reason_text}</span>
      </div>
    </Into>}
  </div>;
}

function LiveCamera({ cameraId }: { cameraId: number }) {
  const updates = useUpdates();
  const view = useApi(() => api.GET("/api/cameras/{camera_id}/view", { params: { path: { camera_id: cameraId } } }), [cameraId], { refresh: [updates] });
  if (view.error) return <ErrorNotice error={view.error} compact retry={view.reload} />;
  if (!view.data) return <Loading text="Подключаем эфир камеры" />;
  if (!view.data.camera || !view.data.state) return <Empty title="Эфира нет" text="Сервер не вернул состояние камеры." />;
  return <LivePlayer view={view.data} compact />;
}

export type EventDetailState = ReturnType<typeof useEventDetail>;

function OperatorIncident({ detail, state }: { detail: EventDetail; state: EventDetailState }) {
  const event = detail.event; const meta = useMeta(); const now = useNow(1000);
  const [comment, setComment] = useState(""); const [notice, setNotice] = useState("");
  useEffect(() => { setComment(""); setNotice(""); }, [event.id]);
  const actions: HumanAction[] = detail.allowed_actions.filter(a => a === "confirm" || a === "false_alarm" || a === "send_to_master");
  const act = useCallback(async (action: HumanAction) => { if (await state.send(action, comment)) { setComment(""); setNotice("Сохранено."); } }, [state, comment]);
  useEffect(() => {
    const handler = (key: KeyboardEvent) => { if (key.altKey || key.ctrlKey || key.metaKey || (key.target as HTMLElement)?.closest?.("input,textarea,select,[contenteditable=true]")) return; const action = BY_KEY[key.key]; if (action && actions.includes(action) && !state.busy) { key.preventDefault(); void act(action); } };
    window.addEventListener("keydown", handler); return () => window.removeEventListener("keydown", handler);
  }, [actions, state.busy, act]);
  const order: HumanAction[] = ["confirm", "false_alarm", "send_to_master"];
  const terminal = meta?.statuses.find(s => s.id === event.status)?.terminal;
  const verdict = event.operator_verdict === "none" ? "Не зафиксирован" : meta?.statuses.find(s => s.id === event.operator_verdict)?.title ?? event.operator_verdict;
  return <div className={`ic-op event-${event.level}`}>
    <EventAlarm event={event} actions={order.filter(a => actions.includes(a)).map(a => ({ id: a, title: ACTIONS[a], key: KEYS[a], danger: a === "confirm" }))} busy={state.busy} onAct={id => void act(id as HumanAction)} media={detail.episode?.evidence[0] ? <Evidence detail={detail} compact /> : undefined} />
    <div className="ic-left">
      <section className="ic-stage" data-panel="Доказательный кадр">
        <Evidence detail={detail} />
        <div className="ic-stage-cap"><span>{event.camera_name}</span><span className="mono">{detail.episode?.evidence[0] ? `кадр ${detail.episode.evidence[0].frame_idx} · запись ${duration(detail.episode.evidence[0].ts_ms)}` : ""}</span></div>
      </section>
      {event.clip && <ClipPlayer clip={event.clip} />}
      <section className="ic-live" data-panel="Эфир камеры сейчас">
        <LiveCamera cameraId={event.camera_id} />
      </section>
    </div>
    <aside className="ic-right" data-panel={`Событие #${event.id}`}>
      <div className="ic-head">
        <div className="ic-head-top"><LevelTag level={event.level} title={meta?.levels.find(l => l.id === event.level)?.title} /><Status event={event} />{unconfirmed(event) && <span className="ic-flag"><ShieldAlert {...IC} />Не подтверждено оператором</span>}</div>
        <h2>{event.title}</h2>
        <p>{event.reason_text}</p>
      </div>
      <dl className="od-facts ic-facts">
        <div><dt>Сектор</dt><dd><Link to={`/operator/sectors/${event.sector_id}`}>{event.sector_name}</Link></dd></div>
        <div><dt>Камера</dt><dd><Link to={`/operator/cameras/${event.camera_id}`}>{event.camera_name}</Link>{event.zone_name && <> · зона «{event.zone_name}»</>}</dd></div>
        <div><dt>Начало</dt><dd className="mono">{time(event.started_at)}</dd></div>
        <div><dt>Длительность</dt><dd className="mono">{duration(event.duration_s * 1000)}{!event.ended_at && " · идёт"}</dd></div>
        <div><dt>Вердикт оператора</dt><dd>{verdict}</dd></div>
        {identityText(event) && <div><dt>Нарушитель</dt><dd data-testid="identity-text">{identityText(event)}</dd></div>}
        {!terminal && <div><dt>Открыто</dt><dd className="ds-num">{since(event.published_at, now)}</dd></div>}
      </dl>
      <div className="ic-actions">
        {actions.length ? <>
          <div className="ic-action-row">{order.filter(a => actions.includes(a)).map(action => <button key={action} data-action={action} disabled={Boolean(state.busy)} onClick={() => void act(action)} className={`button ic-act ic-act-${action} ${action === "confirm" ? "button-primary" : ""}`}><span>{state.busy === action ? "Сохраняем…" : ACTIONS[action]}</span><kbd>{KEYS[action]}</kbd></button>)}</div>
          <label className="ic-comment"><MessageSquareText {...IC} /><input aria-label="Комментарий к действию" value={comment} onChange={e => setComment(e.target.value)} placeholder="Комментарий к действию (необязательно)" maxLength={500} /></label>
        </> : <p className="ic-muted"><Check {...IC} /> {terminal ? `Событие закрыто: ${event.status_title.toLowerCase()}.` : event.status === "sent_to_master" || event.status === "master_accepted" ? `Решение принято, событие у мастера: ${event.status_title.toLowerCase()}.` : "Для вашей роли действий по событию нет."}</p>}
        {state.actionError && <ErrorNotice error={state.actionError} compact retry={state.reload} />}
        {notice && <p className="action-notice" role="status">{notice}</p>}
      </div>
      {detail.can_identify && <Panel title="Нарушитель" aside={identityText(event) ? "указан" : "не указан"}><IdentityPanel detail={detail} onSaved={state.apply} /></Panel>}
      <Panel title="Почему">{detail.why.length ? <dl className="od-facts">{detail.why.map((item, i) => <div key={`${item.label}-${i}`}><dt>{item.label}</dt><dd>{item.value}</dd></div>)}</dl> : <p className="ic-muted">Объяснение не получено.</p>}</Panel>
      <Panel title="История эпизода"><EpisodeHistory detail={detail} /></Panel>
      <Panel title="Действия людей" aside={detail.actions.length}><History actions={detail.actions} /></Panel>
      <Panel title="Происхождение"><Provenance detail={detail} /></Panel>
      {detail.deliveries.length > 0 && <Panel title="Доставка уведомлений" aside={detail.deliveries.length}><ul className="ic-deliveries">{detail.deliveries.map((d, i) => <li key={i}><time className="mono">{time(d.at)}</time><span>{d.channel}</span><span>{d.status_text || (d.status === "sent" ? "доставлено" : "ошибка")}</span>{d.error && <small>{d.error}</small>}</li>)}</ul></Panel>}
    </aside>
  </div>;
}

export function IncidentPage({ master = false }: { master?: boolean }) {
  const { eventId } = useParams(); const id = Number(eventId); const [role] = useRole(); const phone = usePhone();
  const state = useEventDetail(id); const detail = state.detail; const event = detail?.event;
  const levelTitle = useLevelTitle();
  if (master || role === "master") return <MasterEventPage id={id} state={state} />;
  if (phone) return <PhoneEventPage id={id} state={state} />;
  const back = <header className="od-bar"><Link className="od-back" to="/operator"><ArrowLeft {...IC} />Диспетчерская</Link>{event ? <><Link className="ic-crumb" to={`/operator/sectors/${event.sector_id}`}>{number(event.sector_id)} · {event.sector_name.replace(/^Сектор\s+\d+\s*·\s*/, "")}</Link><span className="ic-sep">/</span><Link className="ic-crumb" to={`/operator/cameras/${event.camera_id}`}>{event.camera_name}</Link><h1><span className="od-num">#{event.id}</span>{event.title}</h1><StateBadge state={event.level} text={`${levelTitle(event.level)} · ${time(event.started_at)}`} /></> : <h1>Событие #{id}</h1>}<span className="od-bar-spacer" /><button className="button button-small" onClick={state.reload} disabled={state.loading}>Обновить</button></header>;
  if (!event || !detail) return <div className="od-page" data-testid="incident-focus">{back}{state.error ? <ErrorNotice error={state.error} retry={state.reload} /> : <Loading text="Загружаем событие и доступные действия" />}</div>;
  return <div className="od-page ic-page" data-testid="incident-focus">
    {back}
    {state.error && <ErrorNotice error={state.error} retry={state.reload} />}
    <OperatorIncident detail={detail} state={state} />
  </div>;
}
