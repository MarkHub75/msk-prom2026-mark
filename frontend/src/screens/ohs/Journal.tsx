import { useState } from "react";
import { Link } from "react-router-dom";
import { api, apiError, apiUrl } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { LevelBadge } from "../../components/Badges";
import { DataTable } from "../../components/DataTable";
import { FiltersBar, type JournalFilter } from "../../components/FiltersBar";

type EventSummary = components["schemas"]["EventSummary"];

const TIME = new Intl.DateTimeFormat("ru-RU", { timeZone: "Europe/Moscow", dateStyle: "short", timeStyle: "medium" });

const COLUMNS = [
  {
    title: "Кадр",
    cell: (e: EventSummary) =>
      e.evidence_url ? <img className="thumb" src={apiUrl(e.evidence_url)} alt="Кадр события" width={96} /> : "—",
  },
  { title: "Начало", cell: (e: EventSummary) => <Link to={`/events/${e.id}`}>{TIME.format(new Date(e.started_at))}</Link> },
  { title: "Уровень", cell: (e: EventSummary) => <LevelBadge level={e.level} /> },
  { title: "Сценарий", cell: (e: EventSummary) => e.title },
  { title: "Место", cell: (e: EventSummary) => [e.sector_name, e.camera_name, e.zone_name].filter(Boolean).join(" · ") },
  { title: "Причина", cell: (e: EventSummary) => e.reason_text },
  { title: "Статус", cell: (e: EventSummary) => (e.is_demo ? `${e.status_title} (демо)` : e.status_title) },
];

// Query string of the filter for the CSV link: empty fields stay out.
function query(f: JournalFilter): string {
  const pairs = Object.entries(f).filter(([, v]) => v !== null && v !== undefined && v !== "");
  return new URLSearchParams(pairs.map(([k, v]) => [k, String(v)])).toString();
}

// /ohs/journal: every event with filters; a row opens the event card, read-only for this role.
export function Journal() {
  const [filter, setFilter] = useState<JournalFilter>({});
  const [more, setMore] = useState<{ items: EventSummary[]; cursor: string | null }>();
  const facets = useApi(() => api.GET("/api/journal/facets"), []);
  const first = useApi(() => api.GET("/api/events", { params: { query: filter } }), [filter]);
  const [error, setError] = useState<string>();
  const change = (f: JournalFilter) => {
    setMore(undefined);
    setFilter(f);
  };
  const failure = facets.error ?? first.error;
  if (failure) return <p role="alert">{failure.message}</p>;
  if (!facets.data || !first.data) return <p>Загрузка…</p>;
  const items = [...first.data.items, ...(more?.items ?? [])];
  const cursor = more ? more.cursor : first.data.next_cursor;
  const loadMore = async () => {
    const r = await api.GET("/api/events", { params: { query: { ...filter, cursor } } });
    if (r.error || !r.data) return setError(apiError(r.error).message);
    setMore({ items: [...(more?.items ?? []), ...r.data.items], cursor: r.data.next_cursor });
  };
  return (
    <section>
      <h1>Журнал</h1>
      <FiltersBar
        facets={facets.data}
        value={filter}
        onChange={change}
        onReset={() => change({})}
        shown={items.length}
        total={first.data.total}
      />
      <p>
        <a href={apiUrl(`/api/events/export.csv?${query(filter)}`)} download="journal.csv">
          Экспорт CSV
        </a>
      </p>
      {error && <p role="alert">{error}</p>}
      <DataTable columns={COLUMNS} rows={items} empty="Событий нет" />
      {cursor && (
        <button type="button" onClick={() => void loadMore()}>
          Показать ещё
        </button>
      )}
    </section>
  );
}
