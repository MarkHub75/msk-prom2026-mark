import { useState } from "react";
import { api } from "../../api/client";
import { useApi } from "../../api/useApi";
import { BarChartCard, LineChartCard } from "../../components/Charts";

const WEEKS = [4, 8, 12, 26, 52];

// /management: weekly trend, top sectors per camera, top scenarios, the yellow trend text.
export function ManagementDashboard() {
  const [weeks, setWeeks] = useState<number>();
  const [includeDemo, setIncludeDemo] = useState(true);
  const view = useApi(
    () => api.GET("/api/stats/management", { params: { query: { weeks, include_demo: includeDemo } } }),
    [weeks, includeDemo],
  );
  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!view.data) return <p>Загрузка…</p>;
  const m = view.data;
  return (
    <section>
      <h1>Тренды</h1>
      <div className="form-buttons">
        <label>
          Недель
          <select value={weeks ?? m.weeks.length} onChange={(e) => setWeeks(Number(e.target.value))}>
            {[...new Set([...WEEKS, m.weeks.length])].sort((a, b) => a - b).map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
        </label>
        <label>
          <input type="checkbox" checked={includeDemo} onChange={(e) => setIncludeDemo(e.target.checked)} /> демо
        </label>
      </div>
      {includeDemo && <p>Включая демо-данные</p>}
      <p>{m.yellow_trend.text}</p>
      <LineChartCard title="По неделям" weeks={m.weeks} />
      <BarChartCard
        title="Подтверждённые на камеру по секторам"
        data={m.top_sectors.map((r) => ({ name: r.title, value: r.per_camera ?? 0 }))}
      />
      <ul>
        {m.top_sectors.map((r) => (
          <li key={r.key}>
            {r.title}: {r.per_camera === null ? "нет камер" : `${r.per_camera.toFixed(2)} на камеру`} (подтверждено{" "}
            {r.confirmed}, камер: {r.cameras})
          </li>
        ))}
      </ul>
      <BarChartCard title="Сценарии" data={m.top_scenarios.map((r) => ({ name: r.title, value: r.count }))} />
    </section>
  );
}
