import { useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { LevelBadge } from "../../components/Badges";
import { place } from "./MasterInbox";

type CountRow = components["schemas"]["CountRow"];

const TIME = new Intl.DateTimeFormat("ru-RU", { timeZone: "Europe/Moscow", dateStyle: "short", timeStyle: "short" });

function Counts({ title, rows }: { title: string; rows: CountRow[] }) {
  return (
    <>
      <h2>{title}</h2>
      {rows.length === 0 && <p>Событий нет</p>}
      <dl className="facts">
        {rows.map((r) => (
          <div key={r.key}>
            <dt>{r.title}</dt>
            <dd>
              {r.count} (подтверждено {r.confirmed}, ложных {r.false_alarm})
            </dd>
          </div>
        ))}
      </dl>
    </>
  );
}

// /master/shift: the current or an earlier shift: totals by sector and scenario, confirmed events.
export function ShiftSummaryScreen() {
  const [at, setAt] = useState<string>(); // empty: the current shift
  const view = useApi(() => api.GET("/api/master/shift", { params: { query: { at } } }), [at]);
  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!view.data) return <p>Загрузка…</p>;
  const s = view.data;
  return (
    <section className="master">
      <h1>{s.title}</h1>
      <p>
        {TIME.format(new Date(s.start))} – {TIME.format(new Date(s.end))}
      </p>
      <p>Всего событий: {s.total}</p>
      <div className="form-buttons">
        <button type="button" onClick={() => setAt(new Date(Date.parse(s.start) - 1).toISOString())}>
          Предыдущая смена
        </button>
        {at && (
          <button type="button" onClick={() => setAt(undefined)}>
            Текущая смена
          </button>
        )}
      </div>
      <Counts title="По секторам" rows={s.by_sector} />
      <Counts title="По сценариям" rows={s.by_scenario} />
      <h2>Подтверждённые</h2>
      {s.events.length === 0 && <p>Подтверждённых нет</p>}
      {s.events.map((e) => (
        <Link key={e.id} className="master-card" to={`/master/events/${e.id}`}>
          <span>
            <LevelBadge level={e.level} /> {e.title}
          </span>
          <span>{place(e)}</span>
        </Link>
      ))}
    </section>
  );
}
