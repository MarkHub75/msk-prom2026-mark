import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, apiError } from "../api/client";
import { useApi } from "../api/useApi";
import type { EventAction, EventDetail, HumanAction } from "../api/types";
import { useRole } from "../roles";
import { EventAlarm } from "../components/AlarmTakeover";
import { useMeta, useUpdates, roleTitles } from "../components/AppShell";
import { EvidenceFrame, RecordedVideo } from "../components/Media";
import { useActorIdentity } from "../components/ActorIdentity";
import "../styles/incident-review.css";
import { Breadcrumb, duration, Empty, ErrorNotice, Icon, Level, Loading, number, PageHeading, PanelHeading, Status, time } from "../components/ui";

const ACTIONS: Record<HumanAction, string> = {view:"Отметить просмотр",confirm:"Подтвердить",false_alarm:"Ложное срабатывание",send_to_master:"Передать мастеру",accept:"Принять в работу",resolve:"Отправить отчёт и завершить"};
const HISTORY: Record<EventAction["action"], string> = {published:"Событие опубликовано",viewed:"Открыто оператором",confirmed:"Событие подтверждено",false_alarm:"Ложное срабатывание",sent_to_master:"Передано мастеру",level_escalated:"Повышен уровень",timeout_escalated:"Эскалация по таймауту",master_accepted:"Мастер принял в работу",resolved:"Меры приняты · завершено",auto_finished:"Автоматически завершено",superseded:"Заменено новым событием"};

function useEventDetail(id: number) {
  const [role] = useRole(); const updates = useUpdates();
  const { actor, ensureActor } = useActorIdentity();
  const request = useApi(() => api.GET("/api/events/{event_id}", {params:{path:{event_id:id}}}), [id,role,updates]);
  const [result, setResult] = useState<{ detail: EventDetail; rest: EventDetail | undefined; identity: string }>();
  const [busy, setBusy] = useState<HumanAction>();
  const [actionError, setActionError] = useState<{code:string;message:string}>();
  const guard = useRef(false);
  const viewed = useRef(new Set<string>());
  const identity = `${role}:${id}`;
  const currentIdentity = useRef(identity); currentIdentity.current = identity;
  const rest = useRef(request.data); rest.current = request.data;
  const current = result?.identity === identity && result.rest === request.data ? result.detail : request.data;
  const detail = !request.error && !request.loading && current?.event.id === id ? current : undefined;
  const latestDetail = useRef(detail); latestDetail.current = detail;
  useEffect(() => { setResult(undefined); setActionError(undefined); }, [id,role]);
  const send = useCallback(async (action: HumanAction, comment = "") => {
    if (guard.current) return false;
    guard.current = true; setBusy(action); setActionError(undefined);
    const sendingIdentity = identity;
    try {
      if (!await ensureActor() || currentIdentity.current !== sendingIdentity) return false;
      if (!latestDetail.current?.allowed_actions.includes(action)) {
        setActionError({code:"state_changed",message:"Состояние изменилось. Обновите событие и выберите доступное действие."});
        return false;
      }
      const response = await api.POST("/api/events/{event_id}/actions", { params:{path:{event_id:id}},body:{action,comment:comment.trim()} });
      if (currentIdentity.current !== sendingIdentity) return false;
      if (response.error) { setActionError(apiError(response.error)); return false; }
      if (response.data) setResult({detail:response.data,rest:rest.current,identity:sendingIdentity});
      return true;
    } catch (error) { if (currentIdentity.current===sendingIdentity) setActionError(apiError(error)); return false; }
    finally { guard.current = false; setBusy(undefined); }
  }, [id,identity,ensureActor]);
  useEffect(() => {
    const key = `${identity}:${detail?.event.published_at}`;
    if (actor.trim() && detail?.allowed_actions.includes("view") && !viewed.current.has(key)) {
      viewed.current.add(key);
      void send("view").then(ok => { if (!ok) viewed.current.delete(key); });
    }
  }, [detail,identity,send,actor]);
  return {detail,loading:request.loading,error:request.error,reload:request.reload,busy,actionError,send};
}
function History({ actions }: { actions: EventAction[] }) {
  const meta = useMeta();
  return <section className="history-panel"><PanelHeading aside={`${actions.length} записей`}>Маршрут реакции</PanelHeading>{actions.length ? <ol className="history-rail">{[...actions].sort((a,b)=>a.at.localeCompare(b.at)).map(action => <li key={action.id}><time>{time(action.at)}</time><span className={`history-node ${action.actor_role === "master" ? "node-master" : ""}`} /><div><h3>{HISTORY[action.action]}</h3><p>{action.actor_name || (action.actor_role === "system" ? "Система" : roleTitles[action.actor_role])}<span> / {action.actor_role === "system" ? "Система" : roleTitles[action.actor_role]}</span></p>{action.comment && <blockquote>{action.comment}</blockquote>}{action.to_status && <small>{meta?.statuses.find(status=>status.id===action.to_status)?.title ?? action.to_status}</small>}</div></li>)}</ol> : <Empty title="История пока пуста" text="Действия появятся после ответа сервера." />}</section>;
}
function Provenance({ detail }: {detail:EventDetail}) {
  const p = detail.provenance;
  return <details className="provenance"><summary>Происхождение и воспроизводимость <Icon name="chevron" size={15} /></summary><dl><div><dt>Источник результата</dt><dd>{p.fake ? "Синтетический результат" : p.backend === "linq" ? "LinQ TPU" : p.backend === "local" ? "Локальный backend" : "Не указан"}</dd></div><div><dt>Модель детекции</dt><dd>{p.det_model ?? "Не указана"}</dd></div><div><dt>Анализ / версия</dt><dd>{detail.episode?.analysis_id ?? "—"} / {p.analysis_version ?? "—"}</dd></div><div><dt>SHA-256 кадра</dt><dd className="hash">{p.evidence_sha256 ?? "Не получен"}</dd></div><div><dt>SHA-256 видео</dt><dd className="hash">{p.video_sha256 ?? "Не получен"}</dd></div></dl>{Object.entries(p.rule_params).length > 0 && <dl>{Object.entries(p.rule_params).map(([key,value])=><div key={key}><dt>{key}</dt><dd>{value}</dd></div>)}</dl>}</details>;
}
export function IncidentPage({ master = false }: { master?: boolean }) {
  const {eventId} = useParams(); const id = Number(eventId); const [role] = useRole(); const meta=useMeta();
  const state = useEventDetail(id); const detail = state.detail; const event = detail?.event;
  const isMaster = master || role === "master";
  const [comment, setComment] = useState(""); const [report, setReport] = useState("");
  const [actionNotice, setActionNotice] = useState("");
  useEffect(()=>{setComment("");setReport("");setActionNotice("");},[id]);
  const act = useCallback(async (action:HumanAction) => {
    if (action === "resolve" && !report.trim()) { setActionNotice("Опишите принятые меры перед отправкой отчёта."); return; }
    const ok = await state.send(action,action === "resolve" ? report : comment);
    if (ok) {setComment("");setActionNotice(action === "resolve" ? "Отчёт сохранён сервером." : "Действие сохранено сервером.");}
  },[state,report,comment]);
  useEffect(()=>{
    const handler=(key:KeyboardEvent)=>{ if (key.altKey||key.ctrlKey||key.metaKey||(key.target as HTMLElement)?.closest("input,textarea,select,[contenteditable=true],button,a")) return; const action = ({"1":"confirm","2":"send_to_master","3":"false_alarm"} as const)[key.key as "1"|"2"|"3"]; if (action && !isMaster && detail?.allowed_actions.includes(action) && !state.busy) {key.preventDefault();void act(action);} };
    window.addEventListener("keydown",handler);return()=>window.removeEventListener("keydown",handler);
  },[detail,isMaster,state.busy,act]);
  if (!event || !detail) return <div data-testid={isMaster?"master-detail":"incident-focus"}>{isMaster ? <Link className="mobile-back" to="/master"><Icon name="back" />К поручениям</Link> : <Breadcrumb>Событие #{id}</Breadcrumb>}{state.error ? <ErrorNotice error={state.error} retry={state.reload} /> : <Loading text="Загружаем событие и доступные действия" />}</div>;
  const evidence = detail.episode?.evidence[0];
  const actions = detail.allowed_actions.filter(action=>action!=="view" && (isMaster ? action==="accept"||action==="resolve" : action!=="accept"&&action!=="resolve"));
  const reportRequired = actions.includes("resolve");
  const actionElements = actions.map(action=><button key={action} data-action={action} disabled={Boolean(state.busy) || (action === "resolve" && !report.trim())} onClick={()=>void act(action)} className={`button action-button ${action==="send_to_master"||action==="accept"||action==="resolve" ? event.level==="red"?"button-danger":"button-light" : ""}`}><span>{state.busy===action?"Сохраняем…":ACTIONS[action]}</span>{!isMaster && <kbd>{action==="confirm"?"1":action==="send_to_master"?"2":"3"}</kbd>}{isMaster && <Icon name={action==="resolve"?"check":"arrow"} />}</button>);
  return <div className={`incident-page event-${event.level} ${isMaster?"master-detail":""}`} data-testid={isMaster?"master-detail":"incident-focus"}>
    {isMaster ? <Link className="mobile-back" to="/master"><Icon name="back" size={16} />К поручениям<span>Событие #{event.id}</span></Link> : <Breadcrumb><Link to={`/operator/sectors/${event.sector_id}`}>Сектор {number(event.sector_id)} / {event.sector_name}</Link><span> / </span><Link to={`/operator/cameras/${event.camera_id}`}>{event.camera_name}</Link></Breadcrumb>}
    <PageHeading title={event.title} meta={<><span>{isMaster?`Сектор ${number(event.sector_id)} / ${event.sector_name}`:`Событие #${event.id}`}</span><span className="meta-separator">/</span><span>{time(event.started_at)}</span></>}><Level level={event.level} /><button className="button button-small" onClick={state.reload} disabled={state.loading}>Обновить</button></PageHeading>
    {state.error && <ErrorNotice error={state.error} retry={state.reload} />}<div className="incident-workspace"><section className="evidence-panel"><PanelHeading aside={evidence?`Кадр ${evidence.frame_idx} · ${duration(evidence.ts_ms)}`:"Кадр не получен"}>Доказательный кадр</PanelHeading>{evidence ? <EvidenceFrame evidence={evidence} camera={event.camera_name} level={event.level} /> : <Empty title="Доказательство отсутствует" text="Сервер не передал кадр для этого события." />}<div className="evidence-caption"><span>{event.camera_name} · {time(event.started_at)}</span><span>Зафиксированный кадр события</span></div></section>
    <aside className="decision-panel"><PanelHeading aside={`#${event.id}`}>Состояние и решение</PanelHeading><div className="server-state"><span>Серверное состояние</span><div><Status event={event} /></div><p>{event.reason_text}</p><div className="operator-verdict"><span>Вердикт оператора</span><strong>{event.operator_verdict === "none" ? "Не зафиксирован" : meta?.statuses.find(item=>item.id===event.operator_verdict)?.title ?? event.operator_verdict}</strong></div></div><div className="why-section"><h3>Почему возникло событие</h3><dl>{detail.why.map((item,i)=><div key={`${item.label}-${i}`}><dt>{item.label}</dt><dd>{item.value}</dd></div>)}</dl>{!detail.why.length && <p className="muted">Объяснение не получено.</p>}</div>
    <div className="decision-actions"><h3>{isMaster?"Ваше поручение":"Доступные действия"}</h3>{isMaster && <p className="assignment-copy">{event.notification_text || event.reason_text}</p>}{!isMaster && actions.length>0 && <details className="comment-disclosure"><summary>Добавить комментарий <span>необязательно</span></summary><label className="comment-label"><span className="sr-only">Комментарий к действию</span><textarea aria-label="Комментарий к действию" value={comment} onChange={e=>setComment(e.target.value)} rows={2} placeholder="Уточнение для истории события" maxLength={500} /></label></details>}{reportRequired && <label className="report-label">Принятые меры <span>Обязательно</span><textarea data-testid="measures" value={report} onChange={e=>setReport(e.target.value)} rows={4} placeholder="Что проверено и какие меры приняты на участке" maxLength={500} required /></label>}
    {!actions.length && <div className="no-actions"><Icon name="check" size={19} /><p>Нет доступных действий для текущей роли и состояния.</p></div>}
    <div className={isMaster?"master-primary-actions":"operator-actions"}>{actionElements}</div>{state.actionError && <ErrorNotice error={state.actionError} compact retry={state.reload} />}{actionNotice && <p className="action-notice" role="status">{actionNotice}</p>}<small className="server-authority">Действия и переходы определяет сервер.</small></div><Provenance detail={detail} /></aside>
    <section className="observation-panel"><PanelHeading aside={detail.broadcast?`Позиция повтора ${duration(detail.broadcast.position_ms)}`:"Архивный фрагмент"}>Последующее наблюдение</PanelHeading>{detail.video_id ? <RecordedVideo videoId={detail.video_id} camera={event.camera_name} initialMs={detail.broadcast?.position_ms ?? detail.video_start_ms ?? 0} broadcast={detail.broadcast} episodes={detail.episode?[detail.episode]:[]} /> : <Empty title="Запись не привязана" text="У события нет связанного видео." />}<p className="observation-note">Кадр доказательства закреплён выше. Позиция записи изменяется независимо.</p></section><History actions={detail.actions} /></div>
    {!isMaster && <EventAlarm event={event} />}
    {detail.deliveries.length>0 && <details className="deliveries"><summary>Доставка уведомлений · {detail.deliveries.length}</summary><ul>{detail.deliveries.map((delivery,i)=><li key={i}><time>{time(delivery.at)}</time><span>{delivery.channel}</span><span>{delivery.status === "sent" ? "Доставлено" : "Ошибка доставки"}</span>{delivery.error && <span>{delivery.error}</span>}</li>)}</ul></details>}
  </div>;
}
