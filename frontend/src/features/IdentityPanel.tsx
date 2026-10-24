import { useEffect, useState } from "react";
import { api, apiError, type ApiFailure } from "../api/client";
import type { EventDetail, IdentityIn } from "../api/types";
import { useActorIdentity } from "../components/ActorIdentity";
import { Button, ErrorNotice, Field, TextInput, useToast } from "../components/ui";
import "../styles/v5.css";

// tech.md 8.27: OHS and management type who broke the rule (no face recognition). Fields are trimmed
// by the server, up to 80 characters, an empty field clears it; the status of the event does not change.
export const IDENTITY_MAX = 80;
const FIELDS: { key: keyof IdentityIn; label: string; placeholder: string }[] = [
  { key: "person_name", label: "ФИО", placeholder: "Иванов Иван Иванович" },
  { key: "person_position", label: "Должность", placeholder: "Слесарь-ремонтник" },
  { key: "crew", label: "Бригада", placeholder: "Бригада №3" },
];
// An older backend or a mock may omit the v5 fields: treat them as empty.
const pick = (e: Partial<IdentityIn>): IdentityIn => ({ person_name: e.person_name ?? "", person_position: e.person_position ?? "", crew: e.crew ?? "" });

/** Identity of the event as text; null when nothing was typed. */
export function identityText(e: EventDetail["event"]): string | null {
  const parts = [e.person_name, e.person_position, e.crew].filter(Boolean);
  return parts.length ? parts.join(" · ") : null;
}

export function IdentityPanel({ detail, onSaved }: { detail: EventDetail; onSaved: (next: EventDetail) => void }) {
  const event = detail.event;
  const saved = pick(event);
  const { ensureActor } = useActorIdentity();
  const toast = useToast();
  const [draft, setDraft] = useState<IdentityIn>(saved);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<ApiFailure>();
  // A new event or a change from elsewhere (WS event.updated) replaces the form.
  const { id, person_name, person_position, crew } = event;
  useEffect(() => { setDraft(pick({ person_name, person_position, crew })); setError(undefined); }, [id, person_name, person_position, crew]);

  const trimmed: IdentityIn = { person_name: draft.person_name.trim(), person_position: draft.person_position.trim(), crew: draft.crew.trim() };
  const changed = FIELDS.some(f => trimmed[f.key] !== saved[f.key]);
  const filled = FIELDS.some(f => saved[f.key]);

  const save = async (body: IdentityIn) => {
    setBusy(true); setError(undefined);
    try {
      if (!await ensureActor()) return;
      const r = await api.PATCH("/api/events/{event_id}/identity", { params: { path: { event_id: event.id } }, body });
      if (r.error !== undefined || !r.data) { setError({ ...apiError(r.error), status: r.response.status }); return; }
      onSaved(r.data);
      toast({ title: Object.values(body).some(Boolean) ? "Нарушитель указан" : "Идентификация очищена", text: `Событие #${event.id}`, tone: "neutral" });
    } catch (e) { setError(apiError(e)); } finally { setBusy(false); }
  };

  return <form className="v5-identity" data-testid="identity" onSubmit={e => { e.preventDefault(); if (changed) void save(trimmed); }}>
    {FIELDS.map(f => <Field key={f.key} label={f.label} error={draft[f.key].trim().length > IDENTITY_MAX ? `До ${IDENTITY_MAX} символов` : undefined}>
      <TextInput value={draft[f.key]} maxLength={IDENTITY_MAX} placeholder={f.placeholder} aria-label={f.label} onChange={e => setDraft(d => ({ ...d, [f.key]: e.target.value }))} />
    </Field>)}
    <div className="v5-identity-actions">
      <Button type="submit" size="sm" variant="primary" icon="check" busy={busy} disabled={busy || !changed}>Сохранить</Button>
      {filled && <Button type="button" size="sm" variant="ghost" disabled={busy} onClick={() => void save({ person_name: "", person_position: "", crew: "" })}>Очистить</Button>}
      <small>Статус события не меняется. Запись попадёт в историю действий.</small>
    </div>
    {error && <ErrorNotice error={error} compact />}
  </form>;
}
