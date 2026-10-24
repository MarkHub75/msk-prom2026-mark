import { Bar, BarChart, CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis } from "recharts";
import type { components } from "../api/schema";

type DayRow = components["schemas"]["DayRow"];
type WeekRow = components["schemas"]["WeekRow"];
type Percentiles = components["schemas"]["Percentiles"];

// Fixed size: ResponsiveContainer needs ResizeObserver, and the baseline front is one monitor wide.
const SIZE = { width: 640, height: 240 };
const AXIS = { stroke: "var(--text)", fontSize: 12 };

export function BarChartCard({ title, data }: { title: string; data: { name: string; value: number }[] }) {
  return (
    <figure>
      <figcaption>{title}</figcaption>
      {data.length === 0 ? (
        <p>Событий нет</p>
      ) : (
        <BarChart {...SIZE} data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--no-observation)" />
          <XAxis dataKey="name" tick={AXIS} />
          <YAxis allowDecimals={false} tick={AXIS} />
          <Tooltip />
          <Bar dataKey="value" name={title} fill="var(--accent)" />
        </BarChart>
      )}
    </figure>
  );
}

export function StackedDaysCard({ title, days }: { title: string; days: DayRow[] }) {
  return (
    <figure>
      <figcaption>{title}</figcaption>
      <BarChart {...SIZE} data={days}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--no-observation)" />
        <XAxis dataKey="date" tick={AXIS} />
        <YAxis allowDecimals={false} tick={AXIS} />
        <Tooltip />
        <Legend />
        <Bar dataKey="yellow" name="Жёлтые" stackId="level" fill="var(--yellow)" />
        <Bar dataKey="red" name="Красные" stackId="level" fill="var(--red)" />
      </BarChart>
    </figure>
  );
}

export function LineChartCard({ title, weeks }: { title: string; weeks: WeekRow[] }) {
  return (
    <figure>
      <figcaption>{title}</figcaption>
      <LineChart {...SIZE} data={weeks}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--no-observation)" />
        <XAxis dataKey="week_start" tick={AXIS} />
        <YAxis allowDecimals={false} tick={AXIS} />
        <Tooltip />
        <Legend />
        <Line dataKey="yellow" name="Жёлтые" stroke="var(--yellow)" />
        <Line dataKey="red" name="Красные" stroke="var(--red)" />
        <Line dataKey="confirmed" name="Подтверждены" stroke="var(--normal)" />
      </LineChart>
    </figure>
  );
}

const seconds = (v: number | null) => (v === null ? "—" : `${v.toFixed(1)} с`);

export function PercentilesCard({ title, value }: { title: string; value: Percentiles }) {
  return (
    <figure>
      <figcaption>{title}</figcaption>
      <p>
        p50 {seconds(value.p50)} · p95 {seconds(value.p95)} · n = {value.n} · ожидают {value.pending}
      </p>
    </figure>
  );
}
