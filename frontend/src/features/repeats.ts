import type { EventSummary } from "../api/types";

/** Repeats of one situation: the same camera and the same scenario, each next one within `gapMs` of the group. */
export interface RepeatGroup {
  key: string;
  latest: EventSummary;
  /** Newest first. */
  events: EventSummary[];
  spanMs: number;
  level: EventSummary["level"];
}

export const REPEAT_GAP_MS = 30 * 60_000;

/** Groups keep the order of their first event in `events` (the server's priority order); a lone event is a group of one. */
export function groupRepeats(events: EventSummary[], gapMs = REPEAT_GAP_MS): RepeatGroup[] {
  const order = new Map(events.map((e, i) => [e, i]));
  const buckets = new Map<string, EventSummary[]>();
  for (const event of events) {
    const key = `${event.camera_id}:${event.scenario}`;
    buckets.set(key, [...(buckets.get(key) ?? []), event]);
  }
  // Within a bucket, oldest first: a gap longer than gapMs starts a new group.
  const chains: { key: string; items: EventSummary[] }[] = [];
  for (const [key, bucket] of buckets) {
    const sorted = [...bucket].sort((a, b) => a.published_at.localeCompare(b.published_at) || a.id - b.id);
    let chain: EventSummary[] = [];
    for (const event of sorted) {
      const last = chain[chain.length - 1];
      if (last && Date.parse(event.published_at) - Date.parse(last.published_at) > gapMs) { chains.push({ key, items: chain }); chain = []; }
      chain.push(event);
    }
    chains.push({ key, items: chain });
  }
  const first = (items: EventSummary[]) => Math.min(...items.map(e => order.get(e)!));
  return chains.sort((a, b) => first(a.items) - first(b.items)).map(({ key, items }) => {
    const newest = [...items].reverse();
    return { key: `${key}:${newest[0].id}`, latest: newest[0], events: newest, spanMs: Date.parse(newest[0].published_at) - Date.parse(items[0].published_at), level: items.some(e => e.level === "red") ? "red" : "yellow" };
  });
}

/** "Камера 5.1 · Публичный датасет падений" -> "Камера 5.1" */
export function cameraShort(name: string) { return name.split(" · ")[0]; }

/** "за 30 мин", "за 1 ч 05 мин"; under a minute counts as one. */
export function spanText(ms: number) {
  const min = Math.max(1, Math.ceil(ms / 60_000));
  if (min < 60) return `за ${min} мин`;
  const h = Math.floor(min / 60); const rest = min % 60;
  return rest ? `за ${h} ч ${String(rest).padStart(2, "0")} мин` : `за ${h} ч`;
}

/** "×19 за 30 мин" */
export function repeatCount(group: RepeatGroup) { return `×${group.events.length} ${spanText(group.spanMs)}`; }

/** "Падение и неподвижность · Камера 5.1 · ×19 за 30 мин" */
export function repeatTitle(group: RepeatGroup) { return `${group.latest.title} · ${cameraShort(group.latest.camera_name)} · ${repeatCount(group)}`; }
