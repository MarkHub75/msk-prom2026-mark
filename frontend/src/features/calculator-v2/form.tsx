import type { ReactNode } from "react";
import type { FieldLimit } from "../../api/calcV2";
import { Field, TextInput } from "../../components/ui";

// Form state is the request body itself (К10 п.1: the body is authoritative); inputs keep a text draft per path
// so «0,» or an empty nullable field can be typed. Paths are the contract's field names, as in details.field.

export function getAt(obj: unknown, path: string): unknown {
  return path.split(".").reduce<unknown>((o, k) => (o && typeof o === "object" ? (o as Record<string, unknown>)[k] : undefined), obj);
}

/** Immutable set; `undefined` deletes the key (board_price_overrides: absent key = catalogue price). */
export function setAt<T>(obj: T, path: string, value: unknown): T {
  const [head, ...rest] = path.split(".");
  const src = (obj ?? {}) as Record<string, unknown>;
  const next: Record<string, unknown> = Array.isArray(src) ? [...src] as unknown as Record<string, unknown> : { ...src };
  if (rest.length) next[head] = setAt(src[head], rest.join("."), value);
  else if (value === undefined) delete next[head];
  else next[head] = value;
  return next as T;
}

export interface NumOptions { nullable?: boolean; integer?: boolean; min?: number; max?: number; unit?: string; hint?: ReactNode; /** empty removes the key instead of null (board price: absent = catalogue) */ emptyDeletes?: boolean }

/** Limit of a path from defaults.v2.limits; profile paths of scale (current./added.) share the cameras limits. */
export function limitFor(limits: FieldLimit[], path: string): FieldLimit | undefined {
  return limits.find(l => l.field === path) ?? limits.find(l => l.field === path.replace(/^(current|added)\./, "cameras."));
}

export function parseNum(raw: string, o: NumOptions): { value?: number | null; error?: string } {
  const text = raw.replace(/\s/g, "").replace(",", ".");
  if (text === "") return o.nullable ? { value: null } : { error: "Нужно число" };
  const n = Number(text);
  if (!Number.isFinite(n)) return { error: "Нужно число" };
  if (o.integer && !Number.isInteger(n)) return { error: "Нужно целое число" };
  if (o.min !== undefined && n < o.min) return { error: `Не меньше ${String(o.min).replace(".", ",")}` };
  if (o.max !== undefined && n > o.max) return { error: `Не больше ${String(o.max).replace(".", ",")}` };
  return { value: n };
}

export const show = (v: unknown) => (v === null || v === undefined ? "" : String(v).replace(".", ","));

export function NumField({ id, label, value, draft, error, options, onDraft }: { id: string; label: string; value: unknown; draft?: string; error?: string; options: NumOptions; onDraft: (text: string) => void }) {
  const hint = options.nullable && value === null && draft === undefined ? "пусто — «нужно значение», не ноль" : options.hint;
  return <Field label={label} error={error} hint={hint}>
    <span className="v5-num-input"><TextInput id={id} inputMode="decimal" aria-label={label} aria-invalid={Boolean(error)} value={draft ?? show(value)} placeholder={options.nullable ? "не задано" : undefined} onChange={e => onDraft(e.target.value)} />{options.unit && <small>{options.unit}</small>}</span>
  </Field>;
}
