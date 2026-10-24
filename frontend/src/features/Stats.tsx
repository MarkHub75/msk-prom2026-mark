import { useSearchParams } from "react-router-dom";
import { api } from "../api/client";
import type { CountRow, DayRow, EventSummary, OhsStats } from "../api/types";
import { useApi } from "../api/useApi";
import { ErrorNotice, Loading, PageHeading } from "../components/ui";
import { eventQuery, periodTitle } from "./Journal";
import { loadAll } from "./Report";
import "../styles/stats.css";

// Analytics of the OHS and management roles: GET /api/stats/ohs when the backend has it,
// otherwise the same figures counted over the journal of the period (all pages, see loadAll).
const PERIODS = [7, 30, 90] as const;
const DEFAULT_DAYS = 30;
const MSK_MS = 3 * 3600_000;
const mskDay = (offsetDays = 0) => new Date(Date.now() + MSK_MS + offsetDays * 86400_000).toISOString().slice(0, 10);
const eventDay = (iso: string) => new Date(Date.parse(iso) + MSK_MS).toISOString().slice(0, 10);
const eventHour = (iso: string) => new Date(Date.parse(iso) + MSK_MS).getUTCHours();
const shortDay = (date: string) => date.slice(5).split("-").reverse().join(".");

type Figures = Pick<OhsStats, "total" | "reviewed" | "false_alarm_share" | "by_day" | "by_hour" | "by_sector" | "by_scenario" | "by_status">;
interface Stats extends Figures { source: "server" | "journal"; loaded: number }

function countRows(items: EventSummary[], key: (e: EventSummary) => string, title: (e: EventSummary) => string): CountRow[] {
  const rows = new Map<string, CountRow>();
  for (const e of items) {
    const k = key(e);
    const row = rows.get(k) ?? { key: k, title: title(e), count: 0, confirmed: 0, false_alarm: 0 };
    row.count++;
    if (e.operator_verdict === "confirmed") row.confirmed++;
    if (e.operator_verdict === "false_alarm") row.false_alarm++;
    rows.set(k, row);
  }
  return [...rows.values()].sort((a, b) => b.count - a.count);
}

/** The OhsStats figures the screen shows, counted over journal events (time of start, Moscow). */
export function statsFromEvents(items: EventSummary[], total: number): Figures {
  const days = new Map<string, DayRow>();
  for (const e of items) {
    const date = eventDay(e.started_at);
    const row = days.get(date) ?? { date, red: 0, yellow: 0, confirmed: 0, false_alarm: 0 };
    row[e.level]++;
    if (e.operator_verdict === "confirmed") row.confirmed++;
    if (e.operator_verdict === "false_alarm") row.false_alarm++;
    days.set(date, row);
  }
  const reviewed = items.filter(e => e.operator_verdict !== "none").length;
  const falseAlarms = items.filter(e => e.operator_verdict === "false_alarm").length;
  return {
    total, reviewed,
    false_alarm_share: reviewed ? falseAlarms / reviewed : null,
    by_day: [...days.values()],
    by_hour: countRows(items, e => String(eventHour(e.started_at)), e => String(eventHour(e.started_at))),
    by_sector: countRows(items, e => String(e.sector_id), e => e.sector_name),
    by_scenario: countRows(items, e => e.scenario, e => e.title),
    by_status: countRows(items, e => e.status, e => e.status_title),
  };
}

async function loadStats(range: URLSearchParams): Promise<{ data?: Stats; error?: unknown }> {
  const { date_from, date_to } = eventQuery(range);
  const server = await api.GET("/api/stats/ohs", { params: { query: { date_from, date_to, include_demo: true } } }).catch(() => undefined);
  if (server?.data) return { data: { ...server.data, source: "server", loaded: server.data.total } };
  const journal = await loadAll(range);
  if (!journal.data) return { error: journal.error };
  return { data: { ...statsFromEvents(journal.data.items, journal.data.total), source: "journal", loaded: journal.data.items.length } };
}

interface Column { label: string; tip: string; parts: { value: number; tone: "red" | "yellow" | "grey" }[] }

function niceMax(value: number) {
  if (value <= 4) return 4;
  const step = 10 ** Math.floor(Math.log10(value));
  return [1, 2, 2.5, 5, 10].map(m => m * step).find(m => m >= value) ?? value;
}

/** Hand-drawn column chart: stacked parts from the baseline, every `every`-th label on the x axis. */
function Columns({ columns, every, xTitle, label }: { columns: Column[]; every: number; xTitle: string; label: string }) {
  const W = 960, H = 210, left = 36, right = 6, top = 18, bottom = 40;
  const plotW = W - left - right, plotH = H - top - bottom;
  const max = niceMax(Math.max(0, ...columns.map(c => c.parts.reduce((s, p) => s + p.value, 0))));
  const band = plotW / Math.max(1, columns.length);
  const barW = Math.min(28, Math.max(2, band * 0.68));
  const y = (v: number) => top + plotH - (v / max) * plotH;
  const ticks = [0, max / 2, max].filter(t => Number.isInteger(t));
  return <svg className="st-chart" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={label}>
    <text className="st-axis-title" x={left - 8} y={10} textAnchor="end">событий</text>
    {ticks.map(t => <g key={t}><line className={t ? "st-grid" : "st-base"} x1={left} x2={W - right} y1={y(t)} y2={y(t)} /><text className="st-tick" x={left - 8} y={y(t) + 4} textAnchor="end">{t}</text></g>)}
    {columns.map((c, i) => {
      const x = left + i * band + (band - barW) / 2;
      let acc = 0;
      return <g key={c.label} className="st-col">
        <title>{c.tip}</title>
        <rect className="st-hit" x={left + i * band} y={top} width={band} height={plotH} />
        {c.parts.filter(p => p.value > 0).map((p, j) => {
          const y0 = y(acc), y1 = y(acc + p.value); acc += p.value;
          const gap = j > 0 ? 2 : 0; // 2px surface gap between stacked segments
          return <rect key={p.tone} className={`st-bar st-${p.tone}`} x={x} y={y1} width={barW} height={Math.max(1, y0 - y1 - gap)} />;
        })}
        {i % every === 0 && <text className="st-tick" x={x + barW / 2} y={H - bottom + 16} textAnchor="middle">{c.label}</text>}
      </g>;
    })}
    <text className="st-axis-title" x={W - right} y={H - 4} textAnchor="end">{xTitle}</text>
  </svg>;
}

function TopBars({ title, rows }: { title: string; rows: CountRow[] }) {
  const top = rows.slice(0, 5);
  const max = Math.max(1, ...top.map(r => r.count));
  return <section className="st-panel"><h2>{title}</h2>
    {top.length ? <ol className="st-bars">{top.map(r => <li key={r.key}>
      <span className="st-bars-label" title={r.title}>{r.title}</span>
      <span className="st-bars-track"><i style={{ width: `${(r.count / max) * 100}%` }} /></span>
      <b>{r.count}</b>
    </li>)}</ol> : <p className="st-none">Событий за период нет.</p>}
  </section>;
}

const plural = (n: number, one: string, few: string, many: string) => {
  const d = n % 10, h = n % 100;
  return d === 1 && h !== 11 ? one : d >= 2 && d <= 4 && (h < 12 || h > 14) ? few : many;
};

export function StatsPage({ management = false }: { management?: boolean }) {
  const [search, setSearch] = useSearchParams();
  const days = PERIODS.find(d => d === Number(search.get("days"))) ?? DEFAULT_DAYS;
  const range = new URLSearchParams({ from: mskDay(1 - days), to: mskDay() });
  const stats = useApi(() => loadStats(range), [range.toString()]);
  const dates = Array.from({ length: days }, (_, i) => mskDay(i + 1 - days));

  const periodButtons = <div className="st-periods" role="group" aria-label="Период">
    {PERIODS.map(d => <button key={d} className={`button button-small${d === days ? " is-selected" : ""}`} aria-pressed={d === days} onClick={() => setSearch(d === DEFAULT_DAYS ? {} : { days: String(d) })}>{d} дней</button>)}
  </div>;
  const heading = (source?: Stats["source"]) => <PageHeading title="Аналитика" meta={<>{periodTitle(range)} · время московское{source === "journal" && <span className="st-source">Рассчитано по данным журнала</span>}</>}>{periodButtons}</PageHeading>;

  if (stats.error) return <div className="st-page">{heading()}<ErrorNotice error={stats.error} retry={stats.reload} /></div>;
  if (!stats.data) return <div className="st-page">{heading()}<Loading text="Считаем события за период" /></div>;
  const s = stats.data;

  const byDay = new Map(s.by_day.map(r => [r.date.slice(0, 10), r]));
  const dayRows = dates.map(date => byDay.get(date) ?? { date, red: 0, yellow: 0, confirmed: 0, false_alarm: 0 });
  const red = s.by_day.reduce((sum, r) => sum + r.red, 0);
  const resolved = s.by_status.find(r => r.key === "resolved")?.count ?? 0;
  const share = s.false_alarm_share === null ? "—" : `${Math.round(s.false_alarm_share * 100)}%`;
  const yellowIn = (from: number, to: number) => dayRows.slice(from, to).reduce((sum, r) => sum + r.yellow, 0);
  const hours = new Map(s.by_hour.map(r => [Number(r.key), r.count]));

  return <div className="st-page" data-testid="stats-view">
    {heading(s.source)}
    <section className="st-tiles" aria-label="Итоги периода">
      <div><span>Событий</span><b>{s.total}</b></div>
      <div><span><i className="st-key st-red" />Красных</span><b>{red}</b></div>
      <div><span>Доля ложных срабатываний</span><b>{share}</b><small>ложные из {s.reviewed} с вердиктом оператора</small></div>
      <div><span>Решено мастером</span><b>{resolved}</b></div>
    </section>
    {s.loaded < s.total && <p className="st-partial">Посчитаны первые {s.loaded} из {s.total} событий периода: журнал отдаёт не больше 2000 событий за один расчёт.</p>}

    <section className="st-panel">
      <div className="st-panel-head"><h2>События по дням</h2>
        <span className="st-legend"><span><i className="st-key st-yellow" />Жёлтые</span><span><i className="st-key st-red" />Красные</span></span></div>
      {management && <p className="st-trend" data-testid="yellow-trend">Жёлтых за последние 7 дней: <b>{yellowIn(days - 7, days)}</b>, {days >= 14 ? <>за предыдущие 7: <b>{yellowIn(days - 14, days - 7)}</b></> : "за предыдущие 7: вне выбранного периода, выберите 30 или 90 дней"}</p>}
      <Columns label="Жёлтые и красные события по дням" xTitle="Дата, МСК" every={days <= 7 ? 1 : days <= 30 ? 3 : 7}
        columns={dayRows.map(r => ({ label: shortDay(r.date), tip: `${shortDay(r.date)}: жёлтых ${r.yellow}, красных ${r.red}`, parts: [{ value: r.yellow, tone: "yellow" }, { value: r.red, tone: "red" }] }))} />
    </section>

    <div className="st-pair">
      <TopBars title="Топ-5 секторов" rows={s.by_sector} />
      <TopBars title="Топ-5 сценариев" rows={s.by_scenario} />
    </div>

    {!management && <section className="st-panel"><h2>По часам суток</h2>
      <Columns label="События по часам суток" xTitle="Час суток, МСК" every={1}
        columns={Array.from({ length: 24 }, (_, h) => { const n = hours.get(h) ?? 0; return { label: String(h), tip: `${String(h).padStart(2, "0")}:00–${String(h).padStart(2, "0")}:59: ${n} ${plural(n, "событие", "события", "событий")}`, parts: [{ value: n, tone: "grey" }] }; })} />
    </section>}

    <p className="st-foot">Демо-данные: события синтетические. Время реакции оператора и мастера появится после подключения статистики бэкенда.</p>
  </div>;
}
