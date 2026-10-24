import type { CSSProperties } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { ArrowDownRight, ArrowRight, ArrowUpRight, CheckCircle2, CircleSlash, RotateCw, Siren, TriangleAlert, Info } from "lucide-react";
import { api } from "../api/client";
import type { Schemas } from "../api/types";
import { useApi } from "../api/useApi";
import { ErrorNotice, PageHeading } from "../components/ui";
import { DemoBadge, GrowthContext, Panel, Skeleton, mskDay, ruDay } from "../components/analytics/kit";
import { AreaChart, Legend } from "../components/charts/AreaChart";
import { Delta, HBars, Sparkline, StatTile, type Direction } from "../components/charts/Figures";
import { C, verdictSegments } from "../components/charts/palette";
import { fmt, linearFit } from "../components/charts/scale";

type WeekRow = Schemas["WeekRow"];
const WEEKS = [8, 12, 26] as const;
const DEFAULT_WEEKS = 8;
const AHEAD = 4; // weeks of the dashed projection after the last complete week
/** ISO week number of a Monday date. */
export function isoWeek(monday: string) {
  const d = new Date(Date.parse(`${monday}T00:00:00Z`) + 3 * 86400_000); // Thursday of that week
  const jan1 = Date.UTC(d.getUTCFullYear(), 0, 1);
  return Math.floor((d.getTime() - jan1) / 86400_000 / 7) + 1;
}
const addDays = (date: string, d: number) => new Date(Date.parse(`${date}T00:00:00Z`) + d * 86400_000).toISOString().slice(0, 10);

/** Weekly linear trend of one series over complete weeks from the first non-empty one; null below 4 weeks. */
export function weeklyTrend(values: number[], lastFull: number) {
  const start = values.findIndex(v => v > 0);
  if (start < 0 || lastFull - start + 1 < 4) return null;
  const xs = Array.from({ length: lastFull - start + 1 }, (_, i) => start + i);
  const fit = linearFit(xs, xs.map(i => values[i]));
  return fit && { fit, start };
}

const KPI: { id: keyof Omit<WeekRow, "week_start">; title: string; color: string; direction: Direction; icon: JSX.Element }[] = [
  { id: "yellow", title: "Жёлтые", color: C.yellow, direction: "up_bad", icon: <TriangleAlert size={15} strokeWidth={1.75} /> },
  { id: "red", title: "Красные", color: C.red, direction: "up_bad", icon: <Siren size={15} strokeWidth={1.75} /> },
  { id: "confirmed", title: "Подтверждено оператором", color: C.confirmed, direction: "neutral", icon: <CheckCircle2 size={15} strokeWidth={1.75} /> },
  { id: "false_alarm", title: "Ложные срабатывания", color: C.falseAlarm, direction: "up_bad", icon: <CircleSlash size={15} strokeWidth={1.75} /> },
];

export function ManagementPage() {
  const [search, setSearch] = useSearchParams();
  const navigate = useNavigate();
  const weeks = WEEKS.find(w => w === Number(search.get("weeks"))) ?? DEFAULT_WEEKS;
  const demo = search.get("demo") !== "0";
  const state = useApi(() => api.GET("/api/stats/management", { params: { query: { weeks, include_demo: demo } } }), [], { refresh: [weeks, demo] });
  const data = state.data;
  const set = (k: string, v: string | null) => { const next = new URLSearchParams(search); if (v === null) next.delete(k); else next.set(k, v); setSearch(next); };

  const filters = <div className="an-filters" role="group" aria-label="Период и фильтры">
    <div className="an-seg" role="group" aria-label="Период">
      {WEEKS.map(w => <button key={w} type="button" className={w === weeks ? "is-on" : ""} aria-pressed={w === weeks} onClick={() => set("weeks", w === DEFAULT_WEEKS ? null : String(w))}>{w} недель</button>)}
    </div>
    <label className="an-toggle"><input type="checkbox" checked={demo} onChange={e => set("demo", e.target.checked ? null : "0")} /><span>Демо-данные</span></label>
    <span className="an-filters-gap" />
    <button type="button" className="button button-small" onClick={state.reload} disabled={state.loading}><RotateCw size={14} strokeWidth={1.75} />Обновить</button>
  </div>;
  const heading = <PageHeading title="Аналитика для руководства" meta={<><span>Последние {weeks} недель, включая текущую · недели с понедельника, МСК</span><DemoBadge on={demo} /></>} />;

  if (state.error) return <div className="an-page">{heading}{filters}<ErrorNotice error={state.error} retry={state.reload} /></div>;
  if (!data) return <div className="an-page">{heading}{filters}<Skeleton tiles={4} /></div>;

  const rows = data.weeks;
  const n = rows.length;
  const today = mskDay();
  const partial = n > 0 && addDays(rows[n - 1].week_start, 7) > today;
  const lastFull = partial ? n - 2 : n - 1;
  const series = (id: keyof Omit<WeekRow, "week_start">) => rows.map(r => r[id]);
  const yellow = series("yellow");
  const trend = weeklyTrend(yellow, lastFull);
  const futureCount = trend ? Math.max(0, lastFull + AHEAD - (n - 1)) : 0;
  const future = Array.from({ length: futureCount }, (_, i) => addDays(rows[n - 1].week_start, 7 * (i + 1)));
  const weekTitle = (start: string) => `${ruDay(start)} — ${ruDay(addDays(start, 6))}`;
  const tr = data.yellow_trend;
  const up = (tr.change_pct ?? 0) > 0, flat = !tr.change_pct;
  const TrendIcon = flat ? ArrowRight : up ? ArrowUpRight : ArrowDownRight;
  const trMax = Math.max(1, tr.recent, tr.previous);
  const stale = state.loading ? " is-stale" : "";
  const recent = { from: mskDay(-27), to: today };

  return <div className="an-page" data-testid="stats-view">
    {heading}{filters}
    <div className={`an-mgmt-top${stale}`}>
      <section className={`an-hero an-hero-${flat ? "flat" : up ? "bad" : "good"}`} aria-label="Тренд жёлтых" data-testid="yellow-trend">
        <span className="an-tile-label"><TriangleAlert size={15} strokeWidth={1.75} />Жёлтые нарушения без ложных</span>
        <div className="an-hero-value"><TrendIcon size={34} strokeWidth={1.75} aria-hidden /><b>{tr.change_pct === null ? "—" : `${up ? "+" : tr.change_pct < 0 ? "−" : ""}${fmt.format(Math.abs(Math.round(tr.change_pct)))}%`}</b></div>
        <div className="an-hero-bars">
          <div><span>Последний период</span><i style={{ width: `${(tr.recent / trMax) * 100}%`, "--c": C.yellow } as CSSProperties} /><b>{tr.recent}</b></div>
          <div><span>Период до него</span><i style={{ width: `${(tr.previous / trMax) * 100}%`, "--c": C.neutral } as CSSProperties} /><b>{tr.previous}</b></div>
        </div>
        <p className="an-hero-text" data-testid="yellow-trend-text">{tr.text}</p>
        <p className="an-hero-caveat"><Info size={14} strokeWidth={1.75} />Рост или спад — повод разобраться, а не доказательство эффекта мер.</p>
      </section>
      <section className="an-tiles an-tiles-2" aria-label="Итоги последней полной недели">
        {KPI.map(k => {
          const v = series(k.id);
          const now = lastFull >= 0 ? v[lastFull] : 0, prev = lastFull >= 1 ? v[lastFull - 1] : 0;
          return <StatTile key={k.id} testId={`kpi-${k.id}`} label={`${k.title} за неделю`} icon={k.icon} value={fmt.format(now)}
            spark={<Sparkline values={v} color={k.color} label={`${k.title} по неделям`} partialLast={partial} />}
            delta={lastFull >= 1 ? <Delta now={now} prev={prev} direction={k.direction} vs="к прошлой неделе" /> : undefined}
            foot={<>неделя {lastFull >= 0 ? weekTitle(rows[lastFull].week_start) : "—"}{partial && <> · текущая идёт: <b>{v[n - 1]}</b></>}</>} />;
        })}
      </section>
    </div>

    <Panel className={`an-wide${stale}`} title="Тренд по неделям" testId="weeks"
      sub={<>Жёлтые и красные — заливка, подтверждённые и ложные — линии · пунктир — линейная экстраполяция жёлтых на {AHEAD} недели от последней полной · клик — журнал за неделю</>}
      aside={<Legend items={[{ name: "Жёлтые", color: C.yellow }, { name: "Красные", color: C.red }, { name: "Подтверждено", color: C.confirmed, kind: "line" }, { name: "Ложные", color: C.falseAlarm, kind: "line" }, ...(trend ? [{ name: "Линейная экстраполяция жёлтых, не прогноз модели", color: C.yellow, kind: "trend" as const }, ...(trend.fit.ci(0) !== null ? [{ name: "Интервал 95 % линейной модели", color: C.yellow, kind: "band" as const }] : [])] : [])]} />}>
      <AreaChart ariaLabel="События по неделям" unit="событий в неделю" height={310}
        labels={rows.map(r => `Нед ${isoWeek(r.week_start)}`)} tipLabels={rows.map((r, i) => `Нед ${isoWeek(r.week_start)} · ${weekTitle(r.week_start)}${partial && i === n - 1 ? " · идёт" : ""}`)}
        futureLabels={future.map(d => `Нед ${isoWeek(d)}`)} partialLast={partial ? "неделя идёт" : undefined}
        series={[
          { id: "yellow", name: "жёлтых", values: yellow, color: C.yellow },
          { id: "red", name: "красных", values: series("red"), color: C.red },
          { id: "confirmed", name: "подтверждено", values: series("confirmed"), color: C.confirmed, kind: "line" },
          { id: "false", name: "ложных", values: series("false_alarm"), color: C.falseAlarm, kind: "line" },
        ]}
        projection={trend && { from: trend.start, to: lastFull + AHEAD, at: trend.fit.at, ci: trend.fit.ci, name: "экстраполяция жёлтых", color: C.yellow, note: `линейная экстраполяция, не прогноз модели · +${AHEAD} нед.` }}
        onPick={i => navigate(`/ohs/journal?${new URLSearchParams({ from: rows[i].week_start, to: addDays(rows[i].week_start, 6) })}`)} pickHint="Клик — журнал за неделю" />
      {!trend && <p className="an-note">Экстраполяция не показана: меньше 4 полных недель с событиями.</p>}
      <GrowthContext confirmed={rows.reduce((a, r) => a + r.confirmed, 0)} total={rows.reduce((a, r) => a + r.yellow + r.red, 0)} per="по неделям"
        shares={rows.slice(0, lastFull + 1).map(r => r.yellow + r.red ? r.confirmed / (r.yellow + r.red) : 0)} />
    </Panel>

    <div className="an-grid an-grid-2">
      <Panel title="Секторы: подтверждённые на камеру" testId="top-sectors"
        sub="Последние 4 недели. Делим на число камер: сектор с 8 камерами не должен выглядеть хуже сектора с двумя.">
        <HBars rows={data.top_sectors.map(r => ({ key: r.key, label: r.title, value: r.per_camera ?? 0, display: r.per_camera === null ? "—" : fmt.format(r.per_camera), sub: `подтверждено ${r.confirmed} · ${r.cameras} кам.`, to: `/ohs/journal?${new URLSearchParams({ ...recent, sector_id: r.key })}` }))}
          color={C.confirmed} unit=" на кам." empty="Подтверждённых нарушений за 4 недели нет" />
      </Panel>
      <Panel title="Топ сценариев" testId="top-scenarios" sub={<>Все события за {weeks} недель, разбивка по вердикту оператора</>}
        aside={<Legend items={[{ name: "Подтверждено", color: C.confirmed }, { name: "Ложное", color: C.falseAlarm }, { name: "Без вердикта", color: C.noVerdict }]} />}>
        <HBars rows={data.top_scenarios.map(r => ({ key: r.key, label: r.title, value: r.count, sub: `подтв. ${r.confirmed} · ложных ${r.false_alarm}`, segments: verdictSegments(r), to: `/ohs/journal?${new URLSearchParams({ scenario: r.key })}` }))} color={C.confirmed} />
      </Panel>
    </div>
    <p className="an-foot"><Info size={14} strokeWidth={1.75} />Цифры — из статистики бэкенда{demo ? ", включая демо-данные" : ""}. Пунктир — линейная экстраполяция: прямая наименьших квадратов по полным неделям с первой недели с событиями, продолженная от границы факта; полоса — 95 % интервал для отдельной недели при той же линейной модели. Это не прогноз модели. <Link to="/ohs/journal">Журнал событий</Link></p>
  </div>;
}
