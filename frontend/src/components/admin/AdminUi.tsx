import { useEffect, useRef, type FormEvent, type ReactNode } from "react";
import { useLevelTitle } from "../ops/levels";
import { CircleAlert, CircleCheck, CircleSlash, Octagon, TriangleAlert, X } from "lucide-react";
import type { ApiFailure } from "../../api/client";
import type { CameraState } from "../../api/types";

// A 422 answer names its field in details.field ("name" or "body.sector_id"): the error goes under that field.
export function fieldOf(error?: ApiFailure): string | undefined {
  const field = error?.details?.field;
  return typeof field === "string" ? field.split(".").pop() : undefined;
}

export function Modal({ title, children, onClose, onSubmit, submitText, busy, danger, error, errorShown }: {
  title: string; children: ReactNode; onClose: () => void; onSubmit: () => void; submitText: string;
  busy?: boolean; danger?: boolean; error?: ApiFailure; errorShown?: boolean;
}) {
  const box = useRef<HTMLFormElement>(null);
  useEffect(() => {
    box.current?.querySelector<HTMLElement>("input,select,textarea,button[type=submit]")?.focus();
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", onKey); return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);
  const submit = (e: FormEvent) => { e.preventDefault(); if (!busy) onSubmit(); };
  return <div className="adm-backdrop" onMouseDown={(e) => { if (e.target === e.currentTarget) onClose(); }}>
    <form ref={box} className="adm-modal" role="dialog" aria-modal="true" aria-label={title} onSubmit={submit} noValidate>
      <header><h2>{title}</h2><button type="button" className="adm-icon" onClick={onClose} aria-label="Закрыть"><X size={16} strokeWidth={1.75} /></button></header>
      <div className="adm-modal-body">
        {children}
        {error && !errorShown && <p className="adm-form-error" role="alert"><CircleAlert size={15} strokeWidth={1.75} />{error.message}</p>}
      </div>
      <footer>
        <button type="button" className="button" onClick={onClose}>Отмена</button>
        <button type="submit" className={`button ${danger ? "button-danger" : "button-primary"}`} disabled={busy}>{busy ? "Сохраняем…" : submitText}</button>
      </footer>
    </form>
  </div>;
}

export function Field({ label, name, error, hint, children }: { label: string; name: string; error?: ApiFailure; hint?: string; children: ReactNode }) {
  const own = fieldOf(error) === name;
  return <label className={`adm-field ${own ? "adm-field-invalid" : ""}`}>
    <span>{label}</span>
    {children}
    {own ? <small className="adm-field-error" role="alert"><CircleAlert size={13} strokeWidth={1.75} />{error!.message}</small> : hint ? <small>{hint}</small> : null}
  </label>;
}

const STATE: Record<CameraState["state"], { title: string; icon: ReactNode }> = {
  normal: { title: "Норма", icon: <CircleCheck size={14} strokeWidth={1.75} /> },
  yellow: { title: "Жёлтый", icon: <TriangleAlert size={14} strokeWidth={1.75} /> },
  red: { title: "Красный", icon: <Octagon size={14} strokeWidth={1.75} /> },
  no_observation: { title: "Нет наблюдения", icon: <CircleSlash size={14} strokeWidth={1.75} /> },
};
export function StateBadge({ state, reason }: { state: CameraState["state"]; reason?: string }) {
  const s = STATE[state]; const levelTitle = useLevelTitle();
  const title = state === "red" || state === "yellow" ? levelTitle(state) : s.title;
  return <span className={`adm-state adm-state-${state}`} title={reason || title}>{s.icon}<b>{title}</b>{reason && state !== "normal" && <em>{reason}</em>}</span>;
}

export function Bar({ value, tone = "accent", label }: { value: number; tone?: "accent" | "red" | "ok"; label: string }) {
  const pct = Math.max(0, Math.min(1, value)) * 100;
  return <span className={`adm-bar adm-bar-${tone}`} role="progressbar" aria-label={label} aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(pct)}><i style={{ width: `${pct}%` }} /></span>;
}

export const fmt = (x: number | null | undefined, digits = 1) => x === null || x === undefined || !Number.isFinite(x) ? "—" : x.toFixed(digits).replace(".", ",");
export function bytes(n: number) { return n >= 1 << 20 ? `${fmt(n / (1 << 20))} МБ` : `${fmt(n / 1024, 0)} КБ`; }
