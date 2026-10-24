import type { components, operations } from "../api/schema";

export type JournalFilter = NonNullable<operations["events_list_api_events_get"]["parameters"]["query"]>;
type Facets = components["schemas"]["JournalFacets"];
type FacetItem = components["schemas"]["FacetItem"];

interface Props {
  facets: Facets;
  value: JournalFilter;
  onChange: (value: JournalFilter) => void;
  onReset: () => void;
  shown: number;
  total: number;
}

// A date of the picker is a Moscow day (tech.md 2): its midnight in UTC, and back.
const toIso = (day: string) => (day ? new Date(`${day}T00:00:00+03:00`).toISOString() : null);
const toDay = (iso: string | null | undefined) =>
  iso ? new Date(Date.parse(iso) + 3 * 3600_000).toISOString().slice(0, 10) : "";

function Select({ label, items, value, onChange }: {
  label: string;
  items: FacetItem[];
  value: string | number | null | undefined;
  onChange: (id: string | null) => void;
}) {
  return (
    <label>
      {label}
      <select value={value ?? ""} onChange={(e) => onChange(e.target.value || null)}>
        <option value="">Все</option>
        {items.map((i) => (
          <option key={i.id} value={i.id}>
            {i.title}
          </option>
        ))}
      </select>
    </label>
  );
}

// Filters of the journal; the lists come from /api/journal/facets.
export function FiltersBar({ facets, value, onChange, onReset, shown, total }: Props) {
  const set = (patch: Partial<JournalFilter>) => onChange({ ...value, ...patch });
  const id = (v: string | null) => (v === null ? null : Number(v));
  return (
    <div className="filters">
      <Select label="Тип" items={facets.scenarios} value={value.scenario} onChange={(v) => set({ scenario: v })} />
      <Select label="Уровень" items={facets.levels} value={value.level}
        onChange={(v) => set({ level: v as JournalFilter["level"] })} />
      <Select label="Статус" items={facets.statuses} value={value.status}
        onChange={(v) => set({ status: v as JournalFilter["status"] })} />
      <Select label="Сектор" items={facets.sectors} value={value.sector_id} onChange={(v) => set({ sector_id: id(v) })} />
      <Select label="Камера" items={facets.cameras} value={value.camera_id} onChange={(v) => set({ camera_id: id(v) })} />
      <Select label="Зона" items={facets.zones} value={value.zone_id} onChange={(v) => set({ zone_id: id(v) })} />
      <label>
        С
        <input type="date" value={toDay(value.date_from)} onChange={(e) => set({ date_from: toIso(e.target.value) })} />
      </label>
      <label>
        До (не включая)
        <input type="date" value={toDay(value.date_to)} onChange={(e) => set({ date_to: toIso(e.target.value) })} />
      </label>
      <label>
        Поиск
        <input type="search" maxLength={100} value={value.q ?? ""} onChange={(e) => set({ q: e.target.value || null })} />
      </label>
      <label>
        <input type="checkbox" checked={value.include_demo ?? true}
          onChange={(e) => set({ include_demo: e.target.checked })} />
        Демо
      </label>
      <label>
        <input type="checkbox" checked={value.include_superseded ?? false}
          onChange={(e) => set({ include_superseded: e.target.checked })} />
        Пересчитанные
      </label>
      <button type="button" onClick={onReset}>
        Сбросить
      </button>
      <span>
        показано {shown} из {total}
      </span>
    </div>
  );
}
