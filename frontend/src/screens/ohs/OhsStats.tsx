import { useState } from "react";
import { api } from "../../api/client";
import type { components, operations } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { BarChartCard, PercentilesCard, StackedDaysCard } from "../../components/Charts";

type CountRow = components["schemas"]["CountRow"];
type Query = NonNullable<operations["ohs_stats_view_api_stats_ohs_get"]["parameters"]["query"]>;

const bars = (rows: CountRow[]) => rows.map((r) => ({ name: r.title, value: r.count }));
const percent = (v: number | null) => (v === null ? "—" : `${Math.round(v * 100)} %`);
// A date input is a day in Moscow: its midnight; `date_to` is not included.
const toIso = (day: string) => (day ? new Date(`${day}T00:00:00+03:00`).toISOString() : undefined);

// /ohs/stats: counts by day, scenario, sector, camera, shift and hour; false share; reaction times.
export function OhsStats() {
  const [query, setQuery] = useState<Query>({});
  const facets = useApi(() => api.GET("/api/journal/facets"), []);
  const view = useApi(() => api.GET("/api/stats/ohs", { params: { query } }), [query]);
  const set = (patch: Query) => setQuery({ ...query, ...patch });
  const failure = facets.error ?? view.error;
  if (failure) return <p role="alert">{failure.message}</p>;
  if (!facets.data || !view.data) return <p>Загрузка…</p>;
  const s = view.data;
  return (
    <section>
      <h1>Статистика</h1>
      <div className="form-buttons">
        <label>
          С <input type="date" onChange={(e) => set({ date_from: toIso(e.target.value) })} />
        </label>
        <label>
          До (не включая) <input type="date" onChange={(e) => set({ date_to: toIso(e.target.value) })} />
        </label>
        <label>
          Сектор
          <select onChange={(e) => set({ sector_id: e.target.value ? Number(e.target.value) : undefined })}>
            <option value="">все</option>
            {facets.data.sectors.map((f) => (
              <option key={f.id} value={f.id}>
                {f.title}
              </option>
            ))}
          </select>
        </label>
        <label>
          Камера
          <select onChange={(e) => set({ camera_id: e.target.value ? Number(e.target.value) : undefined })}>
            <option value="">все</option>
            {facets.data.cameras.map((f) => (
              <option key={f.id} value={f.id}>
                {f.title}
              </option>
            ))}
          </select>
        </label>
        <label>
          <input
            type="checkbox"
            checked={s.include_demo}
            onChange={(e) => set({ include_demo: e.target.checked })}
          />{" "}
          демо
        </label>
      </div>
      <p>
        Всего событий: {s.total}
        {s.include_demo && " (включая демо-данные)"}
      </p>
      {s.total === 0 && <p>Событий нет — это не значит, что всё безопасно, если камера без наблюдения</p>}
      <p>
        Доля ложных: {percent(s.false_alarm_share)} (n = {s.reviewed}) · охват проверкой: {percent(s.review_coverage)}{" "}
        (n = {s.total})
      </p>
      <StackedDaysCard title="По дням" days={s.by_day} />
      <BarChartCard title="По сценариям" data={bars(s.by_scenario)} />
      <BarChartCard title="По секторам" data={bars(s.by_sector)} />
      <BarChartCard title="По камерам" data={bars(s.by_camera)} />
      <BarChartCard title="По сменам" data={bars(s.by_shift)} />
      <BarChartCard title="По часам (МСК)" data={bars(s.by_hour)} />
      <PercentilesCard title="Реакция оператора" value={s.operator_reaction_s} />
      <PercentilesCard title="Мастер принял" value={s.master_accept_s} />
      <PercentilesCard title="Мастер решил" value={s.master_resolve_s} />
    </section>
  );
}
