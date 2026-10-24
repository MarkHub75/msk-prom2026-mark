import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { AlertTriangle, CheckCircle2, Clock3, Flame, RotateCw, ShieldCheck, Siren, UserCheck } from "lucide-react";
import { api } from "../api/client";
import type { CountRow, EventSummary, OhsStats } from "../api/types";
import { useApi } from "../api/useApi";
import { DemoBadge, GrowthContext, MSK_MS, Panel, Skeleton, mskDay, ruDay, shortDay, useSticky } from "../components/analytics/kit";
import { ErrorNotice, PageHeading } from "../components/ui";
import { AreaChart, Legend } from "../components/charts/AreaChart";
import { Delta, Donut, HBars, Meter, RangeBullet, Sparkline, StatTile, type BarRow } from "../components/charts/Figures";
import { Heatmap } from "../components/charts/Heatmap";
import { C, verdictSegments } from "../components/charts/palette";
import { fmt, linearFit, niceScale, pct, plural, seconds } from "../components/charts/scale";
import { ManagementPage } from "./ManagementStats";
import "../styles/analytics.css";

// OHS analytics (tech.md 8.13/8.14): GET /api/stats/ohs for every figure, the journal pages of the same
// slice only for the weekday × hour grid (the stats endpoint gives hours, not weekday × hour).
const PERIODS = [7, 30, 90] as const;
const DEFAULT_DAYS = 30;
const HORIZON: Record<number, number> = { 7: 7, 30: 14, 90: 28 };
const WEEKDAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];
// config/default.yaml escalation.timeout_s: a red event without operator action goes to the master after it.
const ESCALATION_S = 45;

interface Slice { days: number; from: string; to: string; sector?: number; camera?: number; demo: boolean }

function readSlice(search: URLSearchParams): Slice {
  const days = PERIODS.find(d => d === Number(search.get("days"))) ?? DEFAULT_DAYS;
  const id = (key: string) => { const v = Number(search.get(key)); return Number.isInteger(v) && v > 0 ? v : undefined; };
  return { days, from: mskDay(1 - days), to: mskDay(), sector: id("sector"), camera: id("camera"), demo: search.get("demo") !== "0" };
}

const apiRange = (s: Slice) => ({ date_from: `${s.from}T00:00:00+03:00`, date_to: `${s.to}T23:59:59.999+03:00` });

async function loadEvents(s: Slice) {
  const items: EventSummary[] = [];
  let cursor: string | undefined, total = 0;
  for (let page = 0; page < 10; page++) {
    const query = { ...apiRange(s), include_demo: s.demo, include_superseded: false, limit: 200, ...(s.sector ? { sector_id: s.sector } : {}), ...(s.camera ? { camera_id: s.camera } : {}), ...(cursor ? { cursor } : {}) };
    const r = await api.GET("/api/events", { params: { query } });
    if (r.error !== undefined || !r.data) return { error: r.error ?? { code: "network", message: "Сервер не отвечает" } };
    items.push(...r.data.items); total = r.data.total;
    if (!r.data.next_cursor) break;
    cursor = r.data.next_cursor;
  }
  return { data: { items, total } };
}

/** Weekday (Mon first) × hour counts by start time in Moscow. */
export function weekHourGrid(items: Pick<EventSummary, "started_at">[]): number[][] {
  const grid = WEEKDAYS.map(() => Array<number>(24).fill(0));
  for (const e of items) {
    const d = new Date(Date.parse(e.started_at) + MSK_MS);
    grid[(d.getUTCDay() + 6) % 7][d.getUTCHours()]++;
  }
  return grid;
}

/** How many times each weekday × hour occurred between the start of `from` (MSK) and `now`; 0 → no data yet. */
export function weekHourSlots(from: string, now = Date.now()): number[][] {
  const slots = WEEKDAYS.map(() => Array<number>(24).fill(0));
  for (let t = Date.parse(`${from}T00:00:00+03:00`); t <= now; t += 3600_000) {
    const d = new Date(t + MSK_MS);
    slots[(d.getUTCDay() + 6) % 7][d.getUTCHours()]++;
  }
  return slots;
}
const weekday = (date: string) => WEEKDAYS[(new Date(`${date}T12:00:00Z`).getUTCDay() + 6) % 7];

/** Linear trend over complete days from the first day with events; null when fewer than 5 such days. */
export function dailyTrend(totals: number[], partialLast: boolean) {
  const end = totals.length - (partialLast ? 1 : 0);
  const start = totals.findIndex(v => v > 0);
  if (start < 0 || end - start < 5) return null;
  const xs = Array.from({ length: end - start }, (_, i) => start + i);
  const fit = linearFit(xs, xs.map(i => totals[i]));
  return fit && { fit, start };
}

const journal = (s: Slice, extra: Record<string, string>) => `/ohs/journal?${new URLSearchParams({ from: s.from, to: s.to, ...(s.sector ? { sector_id: String(s.sector) } : {}), ...extra })}`;

function verdictRows(rows: CountRow[], to: (r: CountRow) => string | undefined): BarRow[] {
  return rows.map(r => ({ key: r.key, label: r.title, value: r.count, sub: `подтв. ${r.confirmed} · ложных ${r.false_alarm}`, to: to(r), segments: verdictSegments(r) }));
}

const VERDICT_LEGEND = [{ name: "Подтверждено", color: C.confirmed }, { name: "Ложное", color: C.falseAlarm }, { name: "Без вердикта", color: C.noVerdict }];

function Reaction({ stats }: { stats: OhsStats }) {
  const rows = [
    { id: "op", title: "Оператор: первая реакция", hint: "от публикации до подтверждения, «ложное» или передачи мастеру", p: stats.operator_reaction_s, color: C.confirmed, threshold: { value: ESCALATION_S, label: `Порог автоэскалации красных — ${ESCALATION_S} с (escalation.timeout_s)` } },
    { id: "acc", title: "Мастер: принял", hint: "от передачи мастеру до «Принял, иду»", p: stats.master_accept_s, color: C.master },
    { id: "res", title: "Мастер: решил", hint: "от «Принял» до «Решено»", p: stats.master_resolve_s, color: C.master },
  ];
  return <div className="an-react">
    {rows.map(r => {
      const max = niceScale(Math.max(r.p.p95 ?? 0, r.threshold?.value ?? 0) * 1.12 || 60, 4).max;
      return <div key={r.id} className="an-react-row" data-testid={`reaction-${r.id}`}>
        <div className="an-react-title"><b>{r.title}</b><small>{r.hint}</small></div>
        {r.p.n ? <div className="an-react-chart">
          <RangeBullet p50={r.p.p50} p95={r.p.p95} max={max} color={r.color} threshold={r.threshold} />
          <div className="an-react-scale"><span>0</span>{r.threshold && <span className="an-react-target" style={{ left: `${(r.threshold.value / max) * 100}%` }}>эскалация {r.threshold.value} с</span>}<span>{seconds(max)}</span></div>
        </div> : <p className="an-none">Нет завершённых реакций за период</p>}
        <dl className="an-react-nums">
          <div><dt>p50</dt><dd>{seconds(r.p.p50)}</dd></div>
          <div><dt>p95</dt><dd>{seconds(r.p.p95)}</dd></div>
          <div><dt>n</dt><dd>{r.p.n}</dd></div>
          <div className={r.p.pending ? "is-pending" : ""}><dt>ожидают</dt><dd>{r.p.pending}</dd></div>
        </dl>
      </div>;
    })}
  </div>;
}

function OhsPage() {
  const [search, setSearch] = useSearchParams();
  const navigate = useNavigate();
  const s = readSlice(search);
  const key = JSON.stringify(s);
  const state = useApi(() => api.GET("/api/stats/ohs", { params: { query: { ...apiRange(s), include_demo: s.demo, ...(s.sector ? { sector_id: s.sector } : {}), ...(s.camera ? { camera_id: s.camera } : {}) } } }), [key]);
  const events = useApi(() => loadEvents(s), [key]);
  const facets = useApi(() => api.GET("/api/journal/facets"), []);
  const stats = useSticky(state);
  const evData = useSticky(events);

  const set = (patch: Record<string, string | null>) => {
    const next = new URLSearchParams(search);
    for (const [k, v] of Object.entries(patch)) { if (v === null || v === "") next.delete(k); else next.set(k, v); }
    setSearch(next);
  };
  const filtered = !!(s.sector || s.camera || !s.demo || s.days !== DEFAULT_DAYS);

  const filters = <div className="an-filters" role="group" aria-label="Период и фильтры">
    <div className="an-seg" role="group" aria-label="Период">
      {PERIODS.map(d => <button key={d} type="button" className={d === s.days ? "is-on" : ""} aria-pressed={d === s.days} onClick={() => set({ days: d === DEFAULT_DAYS ? null : String(d) })}>{d} дней</button>)}
    </div>
    <label className="an-select"><span>Сектор</span>
      <select aria-label="Сектор" value={s.sector ?? ""} onChange={e => set({ sector: e.target.value })} disabled={!facets.data}>
        <option value="">Все секторы</option>{facets.data?.sectors.map(o => <option key={o.id} value={o.id}>{o.title}</option>)}
      </select></label>
    <label className="an-select"><span>Камера</span>
      <select aria-label="Камера" value={s.camera ?? ""} onChange={e => set({ camera: e.target.value })} disabled={!facets.data}>
        <option value="">Все камеры</option>{facets.data?.cameras.map(o => <option key={o.id} value={o.id}>{o.title}</option>)}
      </select></label>
    <label className="an-toggle"><input type="checkbox" checked={s.demo} onChange={e => set({ demo: e.target.checked ? null : "0" })} /><span>Демо-данные</span></label>
    {filtered && <button type="button" className="button button-small" onClick={() => setSearch({})}>Сбросить</button>}
    <span className="an-filters-gap" />
    <button type="button" className="button button-small" onClick={() => { state.reload(); events.reload(); }} disabled={state.loading}><RotateCw size={14} strokeWidth={1.75} />Обновить</button>
  </div>;

  const heading = <PageHeading title="Аналитика охраны труда" meta={<><span>Период {ruDay(s.from)} — {ruDay(s.to)} · время московское</span><DemoBadge on={s.demo} /></>}>
    <Link className="button button-small" to={journal(s, {})}>Журнал за период</Link>
  </PageHeading>;

  if (state.error) return <div className="an-page">{heading}{filters}<ErrorNotice error={state.error} retry={state.reload} /></div>;
  if (!stats) return <div className="an-page">{heading}{filters}<Skeleton /></div>;

  const dates = Array.from({ length: s.days }, (_, i) => mskDay(i + 1 - s.days));
  const byDay = new Map(stats.by_day.map(r => [r.date.slice(0, 10), r]));
  const days = dates.map(date => byDay.get(date) ?? { date, red: 0, yellow: 0, confirmed: 0, false_alarm: 0 });
  const yellow = days.map(d => d.yellow), red = days.map(d => d.red), totals = days.map(d => d.yellow + d.red);
  const redSum = red.reduce((a, b) => a + b, 0);
  const n = days.length;
  const horizon = HORIZON[s.days];
  const trend = dailyTrend(totals, true);
  const future = Array.from({ length: horizon }, (_, i) => mskDay(i + 1));
  const week = (arr: number[], back: number) => arr.slice(Math.max(0, n - 1 - 7 * (back + 1)), n - 1 - 7 * back).reduce((a, b) => a + b, 0);
  const hasWeeks = s.days >= 15;
  const falseCount = Math.round((stats.false_alarm_share ?? 0) * stats.reviewed);
  const hours = Array.from({ length: 24 }, (_, h) => stats.by_hour.find(r => Number(r.key) === h)?.count ?? 0);
  const verdicts = verdictSegments({ count: stats.total, confirmed: stats.by_shift.reduce((a, r) => a + r.confirmed, 0), false_alarm: stats.by_shift.reduce((a, r) => a + r.false_alarm, 0) });
  const empty = stats.total === 0;
  const stale = state.loading ? " is-stale" : "";

  return <div className="an-page" data-testid="stats-view">
    {heading}{filters}
    <section className={`an-tiles${stale}`} aria-label="Итоги периода">
      <StatTile testId="tile-total" label="Событий" icon={<AlertTriangle size={15} strokeWidth={1.75} />} value={fmt.format(stats.total)}
        spark={<Sparkline values={totals} color={C.yellow} label="События по дням" partialLast />}
        delta={hasWeeks ? <Delta now={week(totals, 0)} prev={week(totals, 1)} direction="up_bad" vs="7 дн. к пред. 7" /> : undefined}
        foot={!hasWeeks ? "сравнение неделя к неделе — на периоде 30 или 90 дней" : undefined} />
      <StatTile testId="tile-red" label="Красных" icon={<Siren size={15} strokeWidth={1.75} />} value={fmt.format(redSum)}
        spark={<Sparkline values={red} color={C.red} label="Красные по дням" partialLast />}
        delta={hasWeeks ? <Delta now={week(red, 0)} prev={week(red, 1)} direction="up_bad" vs="7 дн. к пред. 7" /> : undefined} />
      <StatTile testId="tile-false" label="Доля ложных" icon={<ShieldCheck size={15} strokeWidth={1.75} />} value={pct(stats.false_alarm_share)}
        delta={<span title={`ложных ${falseCount} из ${stats.reviewed} с вердиктом`}><Meter share={stats.false_alarm_share} color={C.falseAlarm} label="Доля ложных срабатываний" /></span>}
        foot={<>ложных <b>{falseCount}</b> из <b>n = {stats.reviewed}</b> с вердиктом оператора</>} />
      <StatTile testId="tile-coverage" label="Охват проверкой" icon={<CheckCircle2 size={15} strokeWidth={1.75} />} value={pct(stats.review_coverage)}
        delta={<span title={`с вердиктом ${stats.reviewed} из ${stats.total}`}><Meter share={stats.review_coverage} color={C.confirmed} label="Охват проверкой" /></span>}
        foot={<>с вердиктом <b>{stats.reviewed}</b> из <b>{stats.total}</b> событий</>} />
      <StatTile testId="tile-reaction" label="Реакция оператора, p50" icon={<Clock3 size={15} strokeWidth={1.75} />} value={seconds(stats.operator_reaction_s.p50)}
        spark={<span className="an-tile-side" title={`p95 по ${stats.operator_reaction_s.n} реакциям`}><small>p95</small><b>{seconds(stats.operator_reaction_s.p95)}</b></span>}
        foot={<>n = <b>{stats.operator_reaction_s.n}</b> завершённых · ожидают <b>{stats.operator_reaction_s.pending}</b></>} />
    </section>

    {empty && <div className="an-empty"><Flame size={18} strokeWidth={1.75} /><div><b>Событий за период нет</b><p>Это не значит, что всё безопасно, если камера без наблюдения. Проверьте фильтры и состояние камер.</p></div></div>}

    <Panel className={`an-wide${stale}`} title="События по дням" testId="by-day"
      sub={<>Жёлтые и красные, сложены · клик по дню — журнал за этот день{trend ? ` · пунктир — линейная экстраполяция на ${horizon} дн.` : ""}</>}
      aside={<Legend items={[{ name: "Жёлтые", color: C.yellow }, { name: "Красные", color: C.red }, ...(trend ? [{ name: "Линейная экстраполяция, не прогноз модели", color: C.trend, kind: "trend" as const }, ...(trend.fit.ci(0) !== null ? [{ name: "Интервал 95 % линейной модели", color: C.trend, kind: "band" as const }] : [])] : [])]} />}>
      <AreaChart ariaLabel="Жёлтые и красные события по дням" unit="событий в день" height={290} stacked
        labels={dates.map(shortDay)} tipLabels={dates.map(d => `${weekday(d)}, ${ruDay(d)} · МСК${d === s.to ? " · день идёт" : ""}`)} futureLabels={trend ? future.map(shortDay) : []}
        tickEvery={s.days <= 7 ? 1 : s.days <= 30 ? 3 : 10} partialLast="сегодня"
        series={[{ id: "yellow", name: "жёлтых", values: yellow, color: C.yellow }, { id: "red", name: "красных", values: red, color: C.red }]}
        projection={trend && { from: trend.start, to: n - 1 + horizon, at: trend.fit.at, ci: trend.fit.ci, name: "экстраполяция", color: C.trend, note: `линейная экстраполяция, не прогноз модели · +${horizon} дн.` }}
        onPick={i => navigate(journal(s, { from: dates[i], to: dates[i] }))} />
      {!trend && <p className="an-note">Экстраполяция не показана: меньше 5 полных дней с событиями.</p>}
      <GrowthContext sectorId={s.sector} confirmed={days.reduce((a, d) => a + d.confirmed, 0)} total={totals.reduce((a, b) => a + b, 0)} per="по дням"
        shares={days.slice(0, -1).map((d, i) => totals[i] ? d.confirmed / totals[i] : 0)} />
    </Panel>

    <div className="an-grid an-grid-heat">
      <Panel title="Когда случаются события" testId="heatmap" className={events.loading && evData ? "is-stale" : ""}
        sub={<>День недели × час начала, МСК · сверху — итог по часам из статистики, справа — по дням недели</>}
        aside={evData && <span className="an-chip">по журналу: {evData.items.length}{evData.items.length < evData.total ? ` из ${evData.total}` : ""} {plural(evData.items.length, "событие", "события", "событий")}</span>}>
        {events.error ? <ErrorNotice error={events.error} compact retry={events.reload} /> : !evData ? <i className="an-sk-block" /> : <Heatmap grid={weekHourGrid(evData.items)} slots={weekHourSlots(s.from)} color={C.confirmed} rows={WEEKDAYS} hourTotals={hours} />}
      </Panel>
      <div className="an-stack">
        <Panel title="По сменам" testId="by-shift" aside={<Legend items={VERDICT_LEGEND} />}>
          <HBars rows={verdictRows(stats.by_shift, () => undefined)} color={C.confirmed} />
        </Panel>
        <Panel title="Состояния событий" sub="клик — журнал с этим состоянием">
          <HBars rows={stats.by_status.map(r => ({ key: r.key, label: r.title, value: r.count, to: journal(s, { status: r.key }) }))} color={C.neutral} />
        </Panel>
      </div>
    </div>

    <div className="an-grid an-grid-3">
      <Panel title="По сценариям" sub="клик — журнал по сценарию" testId="by-scenario">
        <div className="an-donut-wrap">
          <Donut parts={verdicts} total={stats.total} caption="событий" />
          <ul className="an-donut-legend">{verdicts.map(v => <li key={v.name}><i style={{ background: v.color }} /><span>{v.name}</span><b>{v.value}</b><small>{stats.total ? pct(v.value / stats.total) : "—"}</small></li>)}</ul>
        </div>
        <HBars rows={verdictRows(stats.by_scenario, r => journal(s, { scenario: r.key }))} color={C.confirmed} />
      </Panel>
      <Panel title="По секторам" sub="клик — журнал по сектору" aside={<Legend items={VERDICT_LEGEND} />} testId="by-sector">
        <HBars rows={verdictRows(stats.by_sector, r => journal(s, { sector_id: r.key }))} color={C.confirmed} />
      </Panel>
      <Panel title="По камерам" sub="клик — журнал по камере" aside={<Legend items={VERDICT_LEGEND} />} testId="by-camera">
        <HBars rows={verdictRows(stats.by_camera, r => journal(s, { q: r.title }))} color={C.confirmed} />
      </Panel>
    </div>

    <Panel className={`an-wide${stale}`} title="Скорость реакции" testId="reaction"
      sub={<>Медиана (p50) — сплошная часть, до p95 — градиент; n — завершённые, ожидают — без действия. Шкала у каждой строки своя.</>}
      aside={<Legend items={[{ name: "Оператор", color: C.confirmed }, { name: "Мастер", color: C.master }, { name: `Порог эскалации ${ESCALATION_S} с`, color: C.red, kind: "trend" }]} />}>
      <Reaction stats={stats} />
    </Panel>

    <p className="an-foot"><UserCheck size={14} strokeWidth={1.75} />Все цифры — из статистики бэкенда за выбранный срез{s.demo ? ", включая демо-данные" : ""}. Пунктир — линейная экстраполяция: прямая наименьших квадратов по полным дням с первого дня с событиями, продолженная от последнего дня факта; полоса — 95 % интервал для отдельного дня при той же линейной модели. Это не прогноз модели.</p>
  </div>;
}

export function StatsPage({ management = false }: { management?: boolean }) {
  return management ? <ManagementPage /> : <OhsPage />;
}
