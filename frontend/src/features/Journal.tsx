import { Fragment, useEffect, useState, type FormEvent } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { ArrowRight, ChevronDown, Download, FileText, Filter, RotateCcw, Search, X } from "lucide-react";
import { api, mediaUrl } from "../api/client";
import type { paths } from "../api/schema";
import type { EventSummary } from "../api/types";
import { useApi } from "../api/useApi";
import { useMeta, useUpdates } from "../components/AppShell";
import { LevelTag } from "../components/operator/kit";
import { duration, Empty, ErrorNotice, Icon, Loading, Status, time } from "../components/ui";
import { EpisodeHistory, Evidence, History } from "./Incident";
import "../styles/journal.css";
import "../styles/operator-depth.css";
import "../styles/journal-depth.css";
import "../styles/mobile-repeats.css";
import { groupRepeats, repeatCount, type RepeatGroup } from "./repeats";

type EventQuery = NonNullable<paths["/api/events"]["get"]["parameters"]["query"]>;
const statuses: EventSummary["status"][] = ["new", "viewed", "confirmed", "false_alarm", "sent_to_master", "master_accepted", "resolved", "auto_finished", "superseded"];
const day = new Intl.DateTimeFormat("ru-RU", { day: "2-digit", month: "short", timeZone: "Europe/Moscow" });
const IC = { size: 15, strokeWidth: 1.75, "aria-hidden": true } as const;

// Period of the journal in Moscow time: YYYY-MM-DD in the URL, ISO with +03:00 to the API.
const MSK = "+03:00";
function mskDate(offsetDays = 0) {
  const now = new Date(Date.now() + 3 * 3600_000 + offsetDays * 86400_000);
  return now.toISOString().slice(0, 10);
}
const PRESETS = [["Сегодня", 0, 0], ["Вчера", 1, 1], ["7 дн", 6, 0], ["30 дн", 29, 0], ["90 дн", 89, 0]] as const;
const ruDay = (value: string) => value.split("-").reverse().join(".");
export function periodTitle(search: URLSearchParams) {
  const from = search.get("from"); const to = search.get("to");
  if (from && to) return from === to ? `За ${ruDay(from)}` : `Период ${ruDay(from)} — ${ruDay(to)}`;
  if (from) return `С ${ruDay(from)}`;
  if (to) return `По ${ruDay(to)}`;
  return "За всё время";
}
const positive = (value: string | null) => { const n = Number(value); return Number.isInteger(n) && n > 0 ? n : undefined; };
/** URL filters → /api/events query. `demo=0` hides demo events, `superseded=1` shows recomputed ones. */
export function eventQuery(search: URLSearchParams): EventQuery {
  const query: EventQuery = { limit: 50, include_demo: search.get("demo") !== "0", include_superseded: search.get("superseded") === "1" };
  const level = search.get("level");
  const status = statuses.find(value => value === search.get("status"));
  if (level === "red" || level === "yellow") query.level = level;
  if (status) query.status = status;
  const sector = positive(search.get("sector_id")); if (sector) query.sector_id = sector;
  const camera = positive(search.get("camera_id")); if (camera) query.camera_id = camera;
  const zone = positive(search.get("zone_id")); if (zone) query.zone_id = zone;
  if (search.get("scenario")) query.scenario = search.get("scenario")!;
  if (search.get("q")?.trim()) query.q = search.get("q")!.trim();
  if (search.get("cursor")) query.cursor = search.get("cursor")!;
  const from = search.get("from"); const to = search.get("to");
  if (from && /^\d{4}-\d{2}-\d{2}$/.test(from)) query.date_from = `${from}T00:00:00${MSK}`;
  if (to && /^\d{4}-\d{2}-\d{2}$/.test(to)) query.date_to = `${to}T23:59:59.999${MSK}`;
  return query;
}
/** Same filters for GET /api/events/export.csv (no page, no cursor). */
export function exportUrl(search: URLSearchParams) {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(eventQuery(search))) if (key !== "limit" && key !== "cursor" && value !== undefined && value !== null) params.set(key, String(value));
  return mediaUrl(`/api/events/export.csv?${params}`);
}

const FILTER_KEYS = ["q", "level", "status", "sector_id", "camera_id", "zone_id", "scenario", "from", "to", "demo", "superseded"] as const;
const CHIP_KEYS = ["q", "level", "status", "sector_id", "camera_id", "zone_id", "scenario"] as const;

function verdict(event: EventSummary, title: (id: string) => string) {
  if (event.operator_verdict !== "none") return <span className={`jd-verdict jd-verdict-${event.operator_verdict}`}>{title(event.operator_verdict)}</span>;
  if (event.escalated_by_timeout) return <span className="jd-verdict jd-verdict-timeout">Без оператора · таймаут</span>;
  return <span className="jd-verdict">Нет вердикта</span>;
}

/** Read-only preview: frame, why, episode and people history; the card itself is one click away. */
function Preview({ id, onClose }: { id: number; onClose: () => void }) {
  const detail = useApi(() => api.GET("/api/events/{event_id}", { params: { path: { event_id: id } } }), [id]);
  const d = detail.data?.event.id === id ? detail.data : undefined;
  useEffect(() => { const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); }; window.addEventListener("keydown", esc); return () => window.removeEventListener("keydown", esc); }, [onClose]);
  return <aside className="jd-preview" data-panel={`Событие #${id}`} aria-label={`Предпросмотр события ${id}`} data-testid="journal-preview">
    <button className="jd-close" onClick={onClose} aria-label="Закрыть предпросмотр"><X {...IC} /></button>
    {detail.error ? <ErrorNotice error={detail.error} compact retry={detail.reload} /> : !d ? <Loading text="Загружаем событие" /> : <div className="jd-preview-body">
      <Evidence detail={d} compact />
      <div className="jd-preview-head"><div className="jd-row"><LevelTag level={d.event.level} /><Status event={d.event} /></div><h3>{d.event.title}</h3><p>{d.event.reason_text}</p></div>
      <dl className="od-facts">
        <div><dt>Место</dt><dd>{d.event.sector_name}<br /><small>{d.event.camera_name}{d.event.zone_name ? ` · ${d.event.zone_name}` : ""}</small></dd></div>
        <div><dt>Начало</dt><dd className="mono">{day.format(new Date(d.event.started_at))} {time(d.event.started_at)} · {duration(d.event.duration_s * 1000)}</dd></div>
        <div><dt>Реакция оператора</dt><dd>{reaction(d.event.published_at, d.actions)}</dd></div>
      </dl>
      {d.why.length > 0 && <section className="ic-panel"><h2>Почему</h2><dl className="od-facts">{d.why.map((w, i) => <div key={i}><dt>{w.label}</dt><dd>{w.value}</dd></div>)}</dl></section>}
      <section className="ic-panel"><h2>История эпизода</h2><EpisodeHistory detail={d} /></section>
      <section className="ic-panel"><h2>Действия людей<span>{d.actions.length}</span></h2><History actions={d.actions} /></section>
      <Link className="button jd-open" to={`/events/${id}`}>Открыть карточку события<ArrowRight {...IC} /></Link>
    </div>}
  </aside>;
}
/** Time from publication to the first operator decision (tech.md 8.13 operator_reaction_s). */
function reaction(published: string, actions: { action: string; at: string; actor_role: string }[]) {
  const first = actions.filter(a => a.actor_role === "operator" && ["confirmed", "false_alarm", "sent_to_master"].includes(a.action)).sort((a, b) => a.at.localeCompare(b.at))[0];
  if (!first) return "решения оператора нет";
  return `${duration(Date.parse(first.at) - Date.parse(published))} до решения`;
}

const GROUP_KEY = "safewatch.journal.group";
function loadGrouped() { try { return localStorage.getItem(GROUP_KEY) === "1"; } catch { return false; } }

export function JournalPage() {
  const [search, setSearch] = useSearchParams();
  const meta = useMeta();
  const updates = useUpdates();
  const queryKey = search.toString();
  const page = useApi(() => api.GET("/api/events", { params: { query: eventQuery(search) } }), [queryKey], {refresh: [updates]});
  const facets = useApi(() => api.GET("/api/journal/facets"), []);
  const [picked, setPicked] = useState<number>();
  // «Группировать повторы»: rows of the same camera and scenario within 30 minutes fold into one; the choice is kept on this device.
  const [grouped, setGrouped] = useState(loadGrouped);
  const [unfolded, setUnfolded] = useState<Set<string>>(new Set());
  const toggleGrouped = (next: boolean) => { setGrouped(next); try { localStorage.setItem(GROUP_KEY, next ? "1" : "0"); } catch { /* storage blocked: the choice lives until reload */ } };
  const unfold = (key: string) => setUnfolded(prev => { const next = new Set(prev); if (next.has(key)) next.delete(key); else next.add(key); return next; });
  const filtersApplied = FILTER_KEYS.some(key => search.has(key));
  const levelOptions = facets.data?.levels ?? meta?.levels.map(item => ({ id: item.id, title: item.title })) ?? [];
  const statusOptions = facets.data?.statuses ?? meta?.statuses.map(item => ({ id: item.id, title: item.title })) ?? [];
  const statusTitle = (id: string) => meta?.statuses.find(s => s.id === id)?.title ?? id;

  function applyFilters(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const values = new FormData(event.currentTarget);
    const next = new URLSearchParams();
    for (const key of FILTER_KEYS) {
      if (key === "demo") { if (!values.get("demo")) next.set("demo", "0"); continue; }
      if (key === "superseded") { if (values.get("superseded")) next.set("superseded", "1"); continue; }
      const value = String(values.get(key) ?? "").trim();
      if (value) next.set(key, value);
    }
    setSearch(next);
  }
  function update(change: (next: URLSearchParams) => void) { const next = new URLSearchParams(search); next.delete("cursor"); change(next); setSearch(next); }
  const preset = (from: number, to: number) => update(next => { next.set("from", mskDate(-from)); next.set("to", mskDate(-to)); });
  const activePreset = PRESETS.find(([, from, to]) => search.get("from") === mskDate(-from) && search.get("to") === mskDate(-to))?.[0];
  const reportQuery = (() => { const q = new URLSearchParams(search); q.delete("cursor"); return q.toString(); })();
  function changePage(cursor?: string) { const next = new URLSearchParams(search); if (cursor) next.set("cursor", cursor); else next.delete("cursor"); setSearch(next); }
  const chipTitle = (key: typeof CHIP_KEYS[number], value: string) => {
    const find = (list?: { id: string; title: string }[]) => list?.find(item => item.id === value)?.title ?? value;
    return { q: `«${value}»`, level: find(levelOptions), status: statusTitle(value), sector_id: find(facets.data?.sectors), camera_id: find(facets.data?.cameras), zone_id: find(facets.data?.zones), scenario: find(facets.data?.scenarios) }[key];
  };
  const items = page.data?.items ?? [];
  const row = (event: EventSummary, child = false) => <tr key={event.id} data-event-id={event.id} className={`jd-row-${event.level} ${selected === event.id ? "is-selected" : ""} ${child ? "rp-child" : ""}`} onClick={() => setPicked(event.id)}>
            <td className="jd-thumb">{event.evidence_url ? <img src={mediaUrl(event.evidence_url)} alt="" loading="lazy" /> : <span>нет кадра</span>}</td>
            <td className="jd-time"><time dateTime={event.published_at}><span>{day.format(new Date(event.published_at))}</span><strong className="mono">{time(event.published_at)}</strong></time></td>
            <td className="jd-event"><button type="button" className="jd-title" onClick={e => { e.stopPropagation(); setPicked(event.id); }}>{event.title}</button><p>{event.reason_text}</p><span className="mono jd-id">#{event.id}{event.is_demo && <em>демо</em>}</span></td>
            <td className="jd-place"><strong>{event.sector_name}</strong><span>{event.camera_name}{event.zone_name ? ` · ${event.zone_name}` : ""}</span></td>
            <td><LevelTag level={event.level} /></td>
            <td><Status event={{ ...event, status_title: statusTitle(event.status) || event.status_title }} /></td>
            <td className="mono jd-dur">{duration(event.duration_s * 1000)}</td>
            <td>{verdict(event, statusTitle)}</td>
            <td className="jd-open"><Link to={`/events/${event.id}`} onClick={e => e.stopPropagation()} aria-label={`Открыть историю события ${event.id}`}><ArrowRight {...IC} /></Link></td>
          </tr>;
  const groupRow = (group: RepeatGroup) => { const event = group.latest; const first = group.events[group.events.length - 1]; const open = unfolded.has(group.key); return <tr key={`g${group.key}`} data-testid="repeat-group" className={`jd-row-${group.level} rp-group-row ${group.events.some(e => e.id === selected) && !open ? "is-selected" : ""}`} onClick={() => unfold(group.key)}>
    <td className="jd-thumb">{event.evidence_url ? <img src={mediaUrl(event.evidence_url)} alt="" loading="lazy" /> : <span>нет кадра</span>}</td>
    <td className="jd-time"><time dateTime={event.published_at}><span>{day.format(new Date(event.published_at))}</span><strong className="mono">{time(event.published_at)}</strong></time><span className="rp-range mono">с {time(first.published_at)}</span></td>
    <td className="jd-event"><span className="rp-group-title"><button type="button" className="jd-title" onClick={e => { e.stopPropagation(); setPicked(event.id); }}>{event.title}</button><span className="rp-tag">{repeatCount(group)}</span></span><p>{event.reason_text}</p><button type="button" className="rp-open-btn" aria-expanded={open} onClick={e => { e.stopPropagation(); unfold(group.key); }}>{open ? "Свернуть" : `Показать все ${group.events.length}`}<ChevronDown {...IC} size={13} /></button></td>
    <td className="jd-place"><strong>{event.sector_name}</strong><span>{event.camera_name}{event.zone_name ? ` · ${event.zone_name}` : ""}</span></td>
    <td><LevelTag level={group.level} /></td>
    <td><Status event={{ ...event, status_title: statusTitle(event.status) || event.status_title }} /></td>
    <td className="mono jd-dur">{duration(event.duration_s * 1000)}</td>
    <td>{verdict(event, statusTitle)}</td>
    <td className="jd-open"><Link to={`/events/${event.id}`} onClick={e => e.stopPropagation()} aria-label={`Открыть историю события ${event.id}`}><ArrowRight {...IC} /></Link></td>
  </tr>; };
  const selected = picked !== undefined && items.some(e => e.id === picked) ? picked : undefined;

  return <div className="jd-page" data-testid="journal-view">
    <header className="od-bar jd-bar">
      <h1>Журнал событий</h1>
      <span className="jd-period">{periodTitle(search)} · МСК</span>
      <span className="od-bar-spacer" />
      <span className="jd-count" aria-live="polite">{page.data ? <>Показано <b>{page.data.items.length}</b> из <b>{page.data.total}</b></> : page.loading ? "Получаем данные" : "Данные не получены"}</span>
      <label className="rp-switch"><input type="checkbox" checked={grouped} onChange={e => toggleGrouped(e.target.checked)} />Группировать повторы</label>
      <a className="button button-small" href={exportUrl(search)} download data-testid="export-csv"><Download {...IC} />Экспорт CSV</a>
      <Link className="button button-small" to={`/ohs/report${reportQuery ? `?${reportQuery}` : ""}`} data-testid="report-link"><FileText {...IC} />Отчёт PDF за период</Link>
      <button className="button button-small" disabled={page.loading} onClick={() => { page.reload(); facets.reload(); }}><Icon name="refresh" size={14} />Обновить</button>
    </header>
    <div className={`jd-layout ${selected !== undefined ? "has-preview" : ""}`}>
      <form className="jd-filters" data-panel="Фильтры" key={queryKey} onSubmit={applyFilters} aria-label="Фильтры журнала">
        <label className="jd-search"><Search {...IC} /><span className="sr-only">Поиск</span><input aria-label="Поиск" name="q" type="search" defaultValue={search.get("q") ?? ""} placeholder="Причина, камера, сектор" /></label>
        <fieldset className="jd-period-set"><legend>Период</legend>
          <div className="jd-presets">{PRESETS.map(([label, from, to]) => <button key={label} type="button" className={activePreset === label ? "selected" : ""} aria-pressed={activePreset === label} onClick={() => preset(from, to)}>{label}</button>)}</div>
          <div className="jd-dates"><input aria-label="Период с" name="from" type="date" defaultValue={search.get("from") ?? ""} /><span>—</span><input aria-label="Период по" name="to" type="date" defaultValue={search.get("to") ?? ""} /></div>
        </fieldset>
        <label>Уровень<select aria-label="Уровень" name="level" defaultValue={search.get("level") ?? ""}><option value="">Все уровни</option>{levelOptions.map(item => <option key={item.id} value={item.id}>{meta?.levels.find(level => level.id === item.id)?.title ?? item.title}</option>)}</select></label>
        <label>Состояние<select aria-label="Состояние" name="status" defaultValue={search.get("status") ?? ""}><option value="">Все состояния</option>{statusOptions.map(item => <option key={item.id} value={item.id}>{statusTitle(item.id) || item.title}</option>)}</select></label>
        <label>Тип нарушения<select aria-label="Сценарий" name="scenario" defaultValue={search.get("scenario") ?? ""} disabled={!facets.data}><option value="">Все типы</option>{facets.data?.scenarios.map(item => <option key={item.id} value={item.id}>{item.title}</option>)}</select></label>
        <label>Сектор<select aria-label="Сектор" name="sector_id" defaultValue={search.get("sector_id") ?? ""} disabled={!facets.data}><option value="">Все секторы</option>{facets.data?.sectors.map(item => <option key={item.id} value={item.id}>{item.title}</option>)}</select></label>
        <label>Камера<select aria-label="Камера" name="camera_id" defaultValue={search.get("camera_id") ?? ""} disabled={!facets.data}><option value="">Все камеры</option>{facets.data?.cameras.map(item => <option key={item.id} value={item.id}>{item.title}</option>)}</select></label>
        <label>Зона<select aria-label="Зона" name="zone_id" defaultValue={search.get("zone_id") ?? ""} disabled={!facets.data}><option value="">Все зоны</option>{facets.data?.zones.map(item => <option key={item.id} value={item.id}>{item.title}</option>)}</select></label>
        <label className="jd-check"><input type="checkbox" name="demo" value="1" defaultChecked={search.get("demo") !== "0"} />Демо-события</label>
        <label className="jd-check"><input type="checkbox" name="superseded" value="1" defaultChecked={search.get("superseded") === "1"} />Пересчитанные</label>
        <div className="jd-filter-actions"><button className="button button-primary" type="submit"><Filter {...IC} />Найти</button>{(filtersApplied || search.has("cursor")) && <button className="button" type="button" onClick={() => setSearch({})}><RotateCcw {...IC} />Сбросить</button>}</div>
        {facets.error && <ErrorNotice error={facets.error} compact retry={facets.reload} />}
      </form>
      <section className="jd-results" data-panel="События">
        {CHIP_KEYS.some(k => search.get(k)) && <div className="jd-chips" aria-label="Активные фильтры">{CHIP_KEYS.filter(k => search.get(k)).map(k => <button key={k} onClick={() => update(next => next.delete(k))} aria-label={`Убрать фильтр ${chipTitle(k, search.get(k)!)}`}>{chipTitle(k, search.get(k)!)}<X {...IC} size={13} /></button>)}{search.get("demo") === "0" && <span>без демо</span>}{search.get("superseded") === "1" && <span>с пересчитанными</span>}</div>}
        {page.error ? <ErrorNotice error={page.error} retry={page.reload} /> : !page.data ? <Loading text="Загружаем журнал событий" /> : !items.length ? <Empty title="События не найдены" text={filtersApplied ? "По этим фильтрам событий нет. Измените или сбросьте фильтры." : "За период событий нет. Камеры без наблюдения событий не дают: тишина не означает безопасность."} /> : <div className="jd-table-wrap"><table className="jd-table">
          <caption className="sr-only">Журнал событий. Дата и время указаны по Москве.</caption>
          <thead><tr><th scope="col"><span className="sr-only">Кадр</span></th><th scope="col">Время</th><th scope="col">Событие</th><th scope="col">Место</th><th scope="col">Уровень</th><th scope="col">Состояние</th><th scope="col">Длит.</th><th scope="col">Вердикт оператора</th><th scope="col"><span className="sr-only">История события</span></th></tr></thead>
          <tbody>{grouped ? groupRepeats(items).map(group => group.events.length > 1 ? <Fragment key={group.key}>{groupRow(group)}{unfolded.has(group.key) && group.events.map(e => row(e, true))}</Fragment> : row(group.latest)) : items.map(event => row(event))}</tbody>
        </table></div>}
        {page.data && <div className="jd-pagination"><span>На странице: {page.data.items.length} · Всего по фильтрам: {page.data.total}</span><div>{search.has("cursor") && <button className="button button-small" onClick={() => changePage()}>К началу</button>}{page.data.next_cursor !== null && <button className="button button-small" onClick={() => changePage(page.data!.next_cursor!)}>Следующая страница <Icon name="arrow" size={15} /></button>}</div></div>}
      </section>
      {selected !== undefined && <Preview id={selected} onClose={() => setPicked(undefined)} />}
    </div>
  </div>;
}
