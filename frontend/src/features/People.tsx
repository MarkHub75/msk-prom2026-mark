import { useSearchParams } from "react-router-dom";
import { RotateCw, UserCheck, Users, UsersRound } from "lucide-react";
import { api } from "../api/client";
import type { CountRow } from "../api/types";
import { useApi } from "../api/useApi";
import { DemoBadge, Panel, Skeleton, mskDay, ruDay } from "../components/analytics/kit";
import { ErrorNotice, PageHeading } from "../components/ui";
import { Legend } from "../components/charts/AreaChart";
import { HBars, Meter, StatTile, type BarRow } from "../components/charts/Figures";
import { C, verdictSegments } from "../components/charts/palette";
import { fmt, pct } from "../components/charts/scale";
import "../styles/analytics.css";
import "../styles/v5.css";

// tech.md 8.27: who broke the rule is typed by OHS in the event card (no face recognition);
// GET /api/stats/people counts only events where a name or a crew was filled in.
const PERIODS = [7, 30, 90] as const;
const DEFAULT_DAYS = 30;
const VERDICT_LEGEND = [{ name: "Подтверждено", color: C.confirmed }, { name: "Ложное", color: C.falseAlarm }, { name: "Без вердикта", color: C.noVerdict }];

const rows = (list: CountRow[]): BarRow[] => list.map(r => ({ key: r.key, label: r.title || r.key, value: r.count, sub: `подтв. ${r.confirmed} · ложных ${r.false_alarm}`, segments: verdictSegments(r) }));

export function PeoplePage() {
  const [search, setSearch] = useSearchParams();
  const days = PERIODS.find(d => d === Number(search.get("days"))) ?? DEFAULT_DAYS;
  const demo = search.get("demo") !== "0";
  const from = mskDay(1 - days), to = mskDay();
  const key = `${days}:${demo}`;
  const state = useApi(() => api.GET("/api/stats/people", { params: { query: { date_from: `${from}T00:00:00+03:00`, date_to: `${to}T23:59:59.999+03:00`, include_demo: demo } } }), [], { refresh: [key] });
  const set = (patch: Record<string, string | null>) => {
    const next = new URLSearchParams(search);
    for (const [k, v] of Object.entries(patch)) { if (v === null) next.delete(k); else next.set(k, v); }
    setSearch(next);
  };

  const heading = <PageHeading title="Нарушители и бригады" meta={<><span>Период {ruDay(from)} — {ruDay(to)} · время московское</span><DemoBadge on={demo} /></>} />;
  const filters = <div className="an-filters" role="group" aria-label="Период и фильтры">
    <div className="an-seg" role="group" aria-label="Период">
      {PERIODS.map(d => <button key={d} type="button" className={d === days ? "is-on" : ""} aria-pressed={d === days} onClick={() => set({ days: d === DEFAULT_DAYS ? null : String(d) })}>{d} дней</button>)}
    </div>
    <label className="an-toggle"><input type="checkbox" checked={demo} onChange={e => set({ demo: e.target.checked ? null : "0" })} /><span>Демо-данные</span></label>
    <span className="an-filters-gap" />
    <button type="button" className="button button-small" onClick={state.reload} disabled={state.loading}><RotateCw size={14} strokeWidth={1.75} />Обновить</button>
  </div>;

  if (state.error) return <div className="an-page">{heading}{filters}<ErrorNotice error={state.error} retry={state.reload} pending="Покажет, в скольких событиях указан нарушитель, и разбивку по людям и бригадам." /></div>;
  const stats = state.data;
  if (!stats) return <div className="an-page">{heading}{filters}<Skeleton tiles={4} /></div>;
  const share = stats.total ? stats.identified / stats.total : null;
  const stale = state.loading ? " is-stale" : "";

  return <div className="an-page" data-testid="people-view">
    {heading}{filters}
    <section className={`an-tiles v5-tiles-4${stale}`} aria-label="Итоги периода">
      <StatTile testId="tile-identified" label="Нарушитель указан" icon={<UserCheck size={15} strokeWidth={1.75} />} value={fmt.format(stats.identified)}
        delta={<Meter share={share} color={C.confirmed} label="Доля событий с указанным нарушителем" />}
        foot={<>из <b>{stats.total}</b> событий за период · {pct(share)}</>} />
      <StatTile testId="tile-unknown" label="Без нарушителя" icon={<Users size={15} strokeWidth={1.75} />} value={fmt.format(Math.max(0, stats.total - stats.identified))} foot="ФИО и бригада не внесены" />
      <StatTile testId="tile-people" label="Людей" icon={<UserCheck size={15} strokeWidth={1.75} />} value={fmt.format(stats.by_person.length)} foot="разных ФИО в событиях" />
      <StatTile testId="tile-crews" label="Бригад" icon={<UsersRound size={15} strokeWidth={1.75} />} value={fmt.format(stats.by_crew.length)} foot="разных бригад в событиях" />
    </section>
    {stats.identified === 0 && <div className="an-empty"><UserCheck size={18} strokeWidth={1.75} /><div><b>Нарушители за период не указаны</b><p>ФИО, должность и бригаду вносит охрана труда в карточке события, блок «Нарушитель». Распознавания лиц в системе нет.</p></div></div>}
    <div className={`an-grid an-grid-2${stale}`}>
      <Panel title="По людям" sub="События с указанным ФИО, по убыванию" aside={<Legend items={VERDICT_LEGEND} />} testId="by-person">
        <HBars rows={rows(stats.by_person)} color={C.confirmed} empty="ФИО не указано ни в одном событии" />
      </Panel>
      <Panel title="По бригадам" sub="События с указанной бригадой, по убыванию" aside={<Legend items={VERDICT_LEGEND} />} testId="by-crew">
        <HBars rows={rows(stats.by_crew)} color={C.confirmed} empty="Бригада не указана ни в одном событии" />
      </Panel>
    </div>
    <p className="an-foot"><UserCheck size={14} strokeWidth={1.75} />Цифры — из статистики бэкенда: только события, где охрана труда вручную указала ФИО или бригаду. Пустые значения в строки не попадают. Это учёт для разбора и обучения, а не рейтинг наказаний.</p>
  </div>;
}
