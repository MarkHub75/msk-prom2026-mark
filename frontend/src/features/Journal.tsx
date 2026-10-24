import type { FormEvent } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { api } from "../api/client";
import type { paths } from "../api/schema";
import type { EventSummary } from "../api/types";
import { useApi } from "../api/useApi";
import { useMeta, useUpdates } from "../components/AppShell";
import { Empty, ErrorNotice, Icon, Level, Loading, PageHeading, Status, time } from "../components/ui";
import "../styles/journal.css";

type EventQuery = NonNullable<paths["/api/events"]["get"]["parameters"]["query"]>;
const statuses: EventSummary["status"][] = ["new", "viewed", "confirmed", "false_alarm", "sent_to_master", "master_accepted", "resolved", "auto_finished", "superseded"];
const day = new Intl.DateTimeFormat("ru-RU", { day: "2-digit", month: "short", timeZone: "Europe/Moscow" });

// Period of the journal in Moscow time: YYYY-MM-DD in the URL, ISO with +03:00 to the API.
const MSK = "+03:00";
function mskDate(offsetDays = 0) {
  const now = new Date(Date.now() + 3 * 3600_000 + offsetDays * 86400_000);
  return now.toISOString().slice(0, 10);
}
const PRESETS = [["Сегодня", 0], ["7 дней", 6], ["30 дней", 29]] as const;
const ruDay = (value: string) => value.split("-").reverse().join(".");
export function periodTitle(search: URLSearchParams) {
  const from = search.get("from"); const to = search.get("to");
  if (from && to) return from === to ? `За ${ruDay(from)}` : `Период ${ruDay(from)} — ${ruDay(to)}`;
  if (from) return `С ${ruDay(from)}`;
  if (to) return `По ${ruDay(to)}`;
  return "За всё время";
}
export function eventQuery(search: URLSearchParams): EventQuery {
  const query: EventQuery = { limit: 25, include_demo: true, include_superseded: false };
  const level = search.get("level");
  const status = statuses.find(value => value === search.get("status"));
  const sector = Number(search.get("sector_id"));
  if (level === "red" || level === "yellow") query.level = level;
  if (status) query.status = status;
  if (Number.isInteger(sector) && sector > 0) query.sector_id = sector;
  if (search.get("scenario")) query.scenario = search.get("scenario")!;
  if (search.get("q")?.trim()) query.q = search.get("q")!.trim();
  if (search.get("cursor")) query.cursor = search.get("cursor")!;
  const from = search.get("from"); const to = search.get("to");
  if (from && /^\d{4}-\d{2}-\d{2}$/.test(from)) query.date_from = `${from}T00:00:00${MSK}`;
  if (to && /^\d{4}-\d{2}-\d{2}$/.test(to)) query.date_to = `${to}T23:59:59.999${MSK}`;
  return query;
}

export function JournalPage() {
  const [search, setSearch] = useSearchParams();
  const meta = useMeta();
  const updates = useUpdates();
  const queryKey = search.toString();
  const page = useApi(() => api.GET("/api/events", { params: { query: eventQuery(search) } }), [queryKey], {refresh: [updates]});
  const facets = useApi(() => api.GET("/api/journal/facets"), []);
  const filtersApplied = ["q", "level", "status", "sector_id", "scenario", "from", "to"].some(key => search.has(key));
  const levelOptions = facets.data?.levels ?? meta?.levels.map(item => ({ id: item.id, title: item.title })) ?? [];
  const statusOptions = facets.data?.statuses ?? meta?.statuses.map(item => ({ id: item.id, title: item.title })) ?? [];

  function applyFilters(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const values = new FormData(event.currentTarget);
    const next = new URLSearchParams();
    for (const key of ["q", "level", "status", "sector_id", "scenario", "from", "to"]) {
      const value = String(values.get(key) ?? "").trim();
      if (value) next.set(key, value);
    }
    setSearch(next);
  }

  function preset(days: number) {
    const next = new URLSearchParams(search);
    next.delete("cursor"); next.set("from", mskDate(-days)); next.set("to", mskDate());
    setSearch(next);
  }
  const reportQuery = (() => { const q = new URLSearchParams(search); q.delete("cursor"); return q.toString(); })();

  function changePage(cursor?: string) {
    const next = new URLSearchParams(search);
    if (cursor) next.set("cursor", cursor);
    else next.delete("cursor");
    setSearch(next);
  }

  return <div className="journal-page" data-testid="journal-view">
    <PageHeading title="Журнал событий" meta="События и история реакции · МСК">
      <Link className="button button-small button-primary" to={`/ohs/report${reportQuery ? `?${reportQuery}` : ""}`} data-testid="report-link">Отчёт PDF за период</Link>
      <button className="button button-small" disabled={page.loading} onClick={() => { page.reload(); facets.reload(); }}>Обновить <Icon name="arrow" size={15} /></button>
    </PageHeading>
    <form className="journal-filters" key={queryKey} onSubmit={applyFilters} aria-label="Фильтры журнала">
      <label className="journal-search">Поиск<input aria-label="Поиск" name="q" type="search" defaultValue={search.get("q") ?? ""} placeholder="Причина, камера или сектор" /></label>
      <label>Уровень<select aria-label="Уровень" name="level" defaultValue={search.get("level") ?? ""}><option value="">Все уровни</option>{levelOptions.map(item => <option key={item.id} value={item.id}>{meta?.levels.find(level => level.id === item.id)?.title ?? item.title}</option>)}</select></label>
      <label>Состояние<select aria-label="Состояние" name="status" defaultValue={search.get("status") ?? ""}><option value="">Все состояния</option>{statusOptions.map(item => <option key={item.id} value={item.id}>{meta?.statuses.find(status => status.id === item.id)?.title ?? item.title}</option>)}</select></label>
      <label>Сектор<select aria-label="Сектор" name="sector_id" defaultValue={search.get("sector_id") ?? ""} disabled={!facets.data}><option value="">Все секторы</option>{facets.data?.sectors.map(item => <option key={item.id} value={item.id}>{item.title}</option>)}</select></label>
      <label>Сценарий<select aria-label="Сценарий" name="scenario" defaultValue={search.get("scenario") ?? ""} disabled={!facets.data}><option value="">Все сценарии</option>{facets.data?.scenarios.map(item => <option key={item.id} value={item.id}>{item.title}</option>)}</select></label>
      <fieldset className="journal-period"><legend>Период</legend><input aria-label="Период с" name="from" type="date" defaultValue={search.get("from") ?? ""} /><span>—</span><input aria-label="Период по" name="to" type="date" defaultValue={search.get("to") ?? ""} /><div className="journal-presets">{PRESETS.map(([label, days]) => <button key={label} type="button" className="button button-small" onClick={() => preset(days)}>{label}</button>)}</div></fieldset>
      <div className="journal-filter-actions"><button className="button button-light" type="submit">Найти</button>{(filtersApplied || search.has("cursor")) && <button className="button" type="button" onClick={() => setSearch({})}>Сбросить</button>}</div>
    </form>
    {facets.error && <ErrorNotice error={facets.error} compact retry={facets.reload} />}
    <div className="journal-result-heading" aria-live="polite"><h2>{filtersApplied ? "Результаты поиска" : "Все события"} · <span className="journal-period-title">{periodTitle(search)}</span></h2><span>{page.data ? `${page.data.total} событий` : page.loading ? "Получаем данные" : "Данные не получены"}</span></div>
    {page.error ? <ErrorNotice error={page.error} retry={page.reload} /> : !page.data ? <Loading text="Загружаем журнал событий" /> : !page.data.items.length ? <Empty title="События не найдены" text={filtersApplied ? "Попробуйте изменить или сбросить фильтры." : "Сервер вернул пустой журнал событий."} /> : <table className="journal-table">
      <caption className="sr-only">Журнал событий. Дата и время указаны по Москве.</caption>
      <thead><tr><th scope="col">Опубликовано</th><th scope="col">Событие</th><th scope="col">Место</th><th scope="col">Уровень</th><th scope="col">Состояние</th><th scope="col"><span className="sr-only">История события</span></th></tr></thead>
      <tbody>{page.data.items.map(event => <tr key={event.id} data-event-id={event.id}>
        <td className="journal-date" data-label="Опубликовано"><time dateTime={event.published_at}><span>{day.format(new Date(event.published_at))}</span><strong>{time(event.published_at)}</strong></time></td>
        <td className="journal-event"><div className="journal-event-id">#{event.id}{event.is_demo && <span>Демо</span>}</div><Link to={`/events/${event.id}`} className="journal-event-title">{event.title}</Link><p>{event.reason_text}</p></td>
        <td className="journal-place" data-label="Место"><strong>{event.sector_name}</strong><span>{event.camera_name}</span>{event.zone_name && <span>{event.zone_name}</span>}</td>
        <td className="journal-level" data-label="Уровень"><Level level={event.level} /></td>
        <td className="journal-status" data-label="Состояние"><Status event={{ ...event, status_title: meta?.statuses.find(item => item.id === event.status)?.title ?? event.status_title }} /></td>
        <td className="journal-open"><Link to={`/events/${event.id}`} aria-label={`Открыть историю события ${event.id}`}>Открыть историю <Icon name="arrow" size={15} /></Link></td>
      </tr>)}</tbody>
    </table>}
    {page.data && <div className="journal-pagination"><span>На странице: {page.data.items.length} · Всего по фильтрам: {page.data.total}</span><div>{search.has("cursor") && <button className="button button-small" onClick={() => changePage()}>К началу</button>}{page.data.next_cursor !== null && <button className="button button-small" onClick={() => changePage(page.data!.next_cursor!)}>Следующая страница <Icon name="arrow" size={15} /></button>}</div></div>}
  </div>;
}
