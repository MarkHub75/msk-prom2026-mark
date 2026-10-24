import { Link, useSearchParams } from "react-router-dom";
import { api } from "../api/client";
import type { EventSummary } from "../api/types";
import { useApi } from "../api/useApi";
import { useMeta } from "../components/AppShell";
import { ErrorNotice, Icon, Loading, time } from "../components/ui";
import { eventQuery, periodTitle } from "./Journal";
import "../styles/report.css";

const PAGE = 200;
const MAX_PAGES = 10;
const dateTime = new Intl.DateTimeFormat("ru-RU", { day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit", timeZone: "Europe/Moscow" });

/** Every event of the journal filter, page by page (the server owns filtering and order). */
export async function loadAll(search: URLSearchParams) {
  const items: EventSummary[] = [];
  let cursor: string | undefined;
  let total = 0;
  for (let i = 0; i < MAX_PAGES; i++) {
    const query = { ...eventQuery(search), limit: PAGE, ...(cursor ? { cursor } : {}) };
    const result = await api.GET("/api/events", { params: { query } });
    if (result.error !== undefined || !result.data) return { error: result.error ?? { code: "network", message: "Сервер не отвечает" } };
    items.push(...result.data.items);
    total = result.data.total;
    if (!result.data.next_cursor) break;
    cursor = result.data.next_cursor;
  }
  return { data: { items, total } };
}

function countBy(items: EventSummary[], key: (e: EventSummary) => string, title: (e: EventSummary) => string) {
  const rows = new Map<string, { title: string; total: number; red: number; yellow: number }>();
  for (const e of items) {
    const k = key(e);
    const row = rows.get(k) ?? { title: title(e), total: 0, red: 0, yellow: 0 };
    row.total++; row[e.level]++;
    rows.set(k, row);
  }
  return [...rows.values()].sort((a, b) => b.total - a.total);
}

function Breakdown({ title, rows }: { title: string; rows: ReturnType<typeof countBy> }) {
  return <section className="rp-block"><h2>{title}</h2><table className="rp-table rp-compact"><thead><tr><th>Значение</th><th>Всего</th><th>Красные</th><th>Жёлтые</th></tr></thead>
    <tbody>{rows.map(r => <tr key={r.title}><td>{r.title}</td><td>{r.total}</td><td>{r.red}</td><td>{r.yellow}</td></tr>)}</tbody></table></section>;
}

export function ReportPage() {
  const [search] = useSearchParams();
  const meta = useMeta();
  const report = useApi(() => loadAll(search), [search.toString()]);
  const statusTitle = (e: EventSummary) => meta?.statuses.find(s => s.id === e.status)?.title ?? e.status_title;
  const back = `/ohs/journal${search.toString() ? `?${search}` : ""}`;
  if (report.error) return <ErrorNotice error={report.error} retry={report.reload} />;
  if (!report.data) return <Loading text="Собираем отчёт по журналу" />;
  const { items, total } = report.data;
  const red = items.filter(e => e.level === "red").length;
  const falseAlarm = items.filter(e => e.status === "false_alarm").length;
  const resolved = items.filter(e => e.status === "resolved").length;
  const demo = items.some(e => e.is_demo);
  return <article className="rp" data-testid="report-view">
    <div className="rp-toolbar no-print">
      <Link className="button button-small" to={back}><Icon name="back" size={15} />К журналу</Link>
      <button className="button button-primary" onClick={() => window.print()}>Сохранить в PDF</button>
      <span>В окне печати выберите «Сохранить как PDF».</span>
    </div>
    <header className="rp-head">
      <div><h1>Отчёт по нарушениям охраны труда</h1><p>{periodTitle(search)} · время московское</p></div>
      <div className="rp-meta"><span>SafeWatch</span><span>Сформирован {dateTime.format(new Date())}</span></div>
    </header>
    {demo && <p className="rp-demo">В отчёт входят демонстрационные события: данные синтетические, не результат наблюдения на производстве.</p>}
    <section className="rp-kpis">
      <div><b>{total}</b><span>событий по фильтру</span></div>
      <div><b>{red}</b><span>красных</span></div>
      <div><b>{items.length - red}</b><span>жёлтых</span></div>
      <div><b>{resolved}</b><span>решено мастером</span></div>
      <div><b>{falseAlarm}</b><span>ложных срабатываний</span></div>
    </section>
    {items.length < total && <p className="rp-demo">В отчёт вошли первые {items.length} из {total} событий. Сузьте период или фильтры.</p>}
    <div className="rp-grid">
      <Breakdown title="По сценариям" rows={countBy(items, e => e.scenario, e => e.title)} />
      <Breakdown title="По секторам" rows={countBy(items, e => String(e.sector_id), e => e.sector_name)} />
      <Breakdown title="По состоянию" rows={countBy(items, e => e.status, statusTitle)} />
    </div>
    <section className="rp-block"><h2>События</h2>
      <table className="rp-table"><thead><tr><th>№</th><th>Дата и время</th><th>Событие</th><th>Причина</th><th>Место</th><th>Уровень</th><th>Состояние</th></tr></thead>
        <tbody>{items.map(e => <tr key={e.id}><td>{e.id}</td><td>{dateTime.format(new Date(e.started_at))}</td><td>{e.title}</td><td>{e.reason_text}</td><td>{e.sector_name}<br /><small>{e.camera_name}{e.zone_name ? ` · ${e.zone_name}` : ""}</small></td><td>{e.level === "red" ? "Красный" : "Жёлтый"}</td><td>{statusTitle(e)}</td></tr>)}</tbody></table>
    </section>
    <footer className="rp-foot">Источник: журнал событий SafeWatch, фильтр как в журнале на момент формирования. Время начала события — по Москве. Последнее обновление данных: {time(new Date().toISOString())}.</footer>
  </article>;
}
