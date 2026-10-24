// Tab «Правила» (tech.md 8.3, S9): scenarios of the camera, switches and parameters with units and ranges.
// Effective = defaults + stored overrides; the scenario status text comes from /api/meta.
import { useEffect, useMemo, useState, type ComponentType } from "react";
import {
  AlertTriangle, Ban, Box, CircleAlert, CircleCheck, Construction, Container, Fence, Flame, Footprints, HardHat, Lock, PersonStanding,
  RotateCcw, Save, ShieldAlert, Smartphone, Truck, type LucideProps,
} from "lucide-react";
import { api, apiError, type ApiFailure } from "../../api/client";
import type { Schemas } from "../../api/types";
import { useApi } from "../../api/useApi";
import { useRole } from "../../roles";
import { ErrorNotice, Loading } from "../../components/ui";
import { fmt, overrides, parseNumber } from "./geometry";
import { ICON, RecomputeNotice, useSetupMeta } from "./shared";
import "../../styles/geometry.css";

type Rule = Schemas["CameraRule"];
type Scenario = Schemas["ScenarioMeta"];
interface RowDraft { enabled: boolean; values: Record<string, string> }

const ICONS: Record<string, ComponentType<LucideProps>> = {
  run: Footprints, truck: Truck, phone: Smartphone, fall: PersonStanding, fence: Fence, conveyor: Container, fire: Flame, harness: HardHat, crane: Construction, box: Box,
};

const draftOf = (rule: Rule): RowDraft => ({ enabled: rule.enabled, values: Object.fromEntries(Object.entries(rule.effective).map(([k, v]) => [k, fmt(v, 4)])) });

/** Parsed values or the first out-of-range problem per key. */
export function paramProblems(s: Scenario, values: Record<string, string>): Record<string, string> {
  const out: Record<string, string> = {};
  for (const p of s.params) {
    const v = parseNumber(values[p.key] ?? "");
    if (v === null) out[p.key] = "Нужно число";
    else if (v < p.min || v > p.max) out[p.key] = `От ${fmt(p.min, 4)} до ${fmt(p.max, 4)}`;
  }
  return out;
}

export function CameraRulesTab({ cameraId }: { cameraId: number }) {
  const [role] = useRole();
  const canEdit = role === "admin" || role === "ohs";
  const { meta, error: metaError } = useSetupMeta();
  const rules = useApi(() => api.GET("/api/cameras/{camera_id}/rules", { params: { path: { camera_id: cameraId } } }), [cameraId]);
  const zones = useApi(() => api.GET("/api/cameras/{camera_id}/zones", { params: { path: { camera_id: cameraId } } }), [cameraId]);
  const [drafts, setDrafts] = useState<Record<string, RowDraft>>({});
  const [errors, setErrors] = useState<Record<string, ApiFailure>>({});
  const [busy, setBusy] = useState(false);
  const [changed, setChanged] = useState<string>();

  const base = useMemo(() => Object.fromEntries((rules.data ?? []).map((r) => [r.scenario, draftOf(r)])), [rules.data]);
  useEffect(() => setDrafts(base), [base]);

  if (rules.error) return <ErrorNotice error={rules.error} retry={rules.reload} />;
  if (metaError) return <ErrorNotice error={metaError} />;
  if (!rules.data || !meta) return <Loading text="Загружаем сценарии камеры" />;

  const scenarios = meta.scenarios;
  const kinds = meta.zone_kinds;
  const zoneKinds = new Set((zones.data ?? []).map((z) => z.kind));
  const byId = Object.fromEntries(rules.data.map((r) => [r.scenario, r]));
  const isDirty = (id: string) => !!drafts[id] && !!base[id] && JSON.stringify(drafts[id]) !== JSON.stringify(base[id]);
  const dirtyIds = scenarios.map((s) => s.id).filter(isDirty);
  const invalid = dirtyIds.some((id) => Object.keys(paramProblems(scenarios.find((s) => s.id === id)!, drafts[id].values)).length > 0);

  const setValue = (id: string, key: string, v: string) => setDrafts((d) => ({ ...d, [id]: { ...d[id], values: { ...d[id].values, [key]: v } } }));
  const toDefault = (s: Scenario, key: string) => setValue(s.id, key, fmt(s.params.find((p) => p.key === key)!.default, 4));

  const save = async () => {
    setBusy(true);
    const next: Record<string, ApiFailure> = {};
    let saved = 0;
    for (const id of dirtyIds) {
      const s = scenarios.find((x) => x.id === id)!;
      const d = drafts[id];
      const defaults = Object.fromEntries(s.params.map((p) => [p.key, p.default]));
      const values = Object.fromEntries(s.params.map((p) => [p.key, parseNumber(d.values[p.key] ?? "") ?? p.default]));
      const r = await api.PUT("/api/cameras/{camera_id}/rules/{scenario}", {
        params: { path: { camera_id: cameraId, scenario: id } },
        body: { enabled: d.enabled, params: overrides(defaults, values) },
      });
      if (r.error) next[id] = apiError(r.error); else saved += 1;
    }
    setBusy(false);
    setErrors(next);
    if (saved) setChanged(`Сохранено сценариев: ${saved}`);
    rules.reload();
  };

  const active = scenarios.filter((s) => byId[s.id]?.enabled && s.status === "active").length;

  return (
    <div className="geo-rules" data-testid="rules-tab" data-panel="Сценарии камеры">
      <div className="geo-rules-head">
        <span><b>{active}</b> из {scenarios.length} сценариев работают на этой камере</span>
        {!canEdit && <span className="geo-readonly"><Lock {...ICON} size={13} /> Только просмотр</span>}
      </div>
      <ul className="geo-rule-list">
        {scenarios.map((s) => {
          const rule = byId[s.id];
          const d = drafts[s.id];
          if (!rule || !d) return null;
          const Icon = ICONS[s.icon] ?? ShieldAlert;
          const problems = paramProblems(s, d.values);
          const err = errors[s.id];
          const errField = typeof err?.details?.field === "string" ? err.details.field.replace(/^params\./, "") : undefined;
          const live = s.status === "active";
          return (
            <li key={s.id} className={`geo-rule ${d.enabled ? "is-on" : "is-off"} ${live ? "" : "is-unavailable"} ${isDirty(s.id) ? "is-dirty" : ""}`} data-testid={`rule-${s.id}`}>
              <div className="geo-rule-main">
                <label className="geo-switch" title={live ? "" : s.status_text}>
                  <input type="checkbox" role="switch" checked={d.enabled} disabled={!canEdit} aria-label={`${s.title}: ${d.enabled ? "включён" : "выключен"}`}
                    onChange={(e) => setDrafts((x) => ({ ...x, [s.id]: { ...x[s.id], enabled: e.target.checked } }))} />
                  <span aria-hidden="true" />
                </label>
                <Icon {...ICON} size={18} className="geo-rule-icon" />
                <div className="geo-rule-title">
                  <b>{s.title}</b>
                  <small>{s.description}</small>
                </div>
                <span className={`geo-level geo-level-${s.default_level}`}>
                  {s.default_level === "red" ? <ShieldAlert {...ICON} size={13} /> : <AlertTriangle {...ICON} size={13} />}
                  {meta.levels.find((l) => l.id === s.default_level)?.title ?? s.default_level}
                </span>
                <span className={`geo-status geo-status-${s.status}`}>
                  {s.status === "active" ? <CircleCheck {...ICON} size={13} /> : s.status === "model_missing" ? <CircleAlert {...ICON} size={13} /> : <Ban {...ICON} size={13} />}
                  {s.status_text}
                </span>
              </div>
              {(s.zone_kinds.length > 0 || !live && d.enabled) && (
                <div className="geo-rule-notes">
                  {s.zone_kinds.length > 0 && <span>Зоны: {s.zone_kinds.map((k) => {
                    const km = kinds.find((x) => x.id === k);
                    return <span key={k} className={`geo-zone-chip ${zoneKinds.has(k) ? "" : "is-missing"}`}><i style={{ background: km?.color }} />{km?.title ?? k}{zoneKinds.has(k) ? "" : " — нет на камере"}</span>;
                  })}</span>}
                  {!live && d.enabled && <span className="geo-bad">Включён, но в анализе не участвует: {s.status_text.toLowerCase()}</span>}
                </div>
              )}
              {s.params.length > 0 && (
                <div className="geo-params">
                  {s.params.map((p) => {
                    const stored = rule.params[p.key] !== undefined;
                    const v = parseNumber(d.values[p.key] ?? "");
                    const isDefault = v !== null && Math.abs(v - p.default) < 1e-9;
                    const bad = problems[p.key] ?? (errField === p.key ? err?.message : undefined);
                    return (
                      <label key={p.key} className={`geo-param ${bad ? "is-invalid" : ""} ${!isDefault ? "is-custom" : ""}`}>
                        <span className="geo-param-title" title={p.title}>{p.title}{stored && <i title="Задано для этой камеры">●</i>}</span>
                        <span className="geo-param-input">
                          <input inputMode="decimal" value={d.values[p.key] ?? ""} disabled={!canEdit} aria-label={`${s.title}: ${p.title}`} aria-invalid={!!bad}
                            onChange={(e) => setValue(s.id, p.key, e.target.value)} />
                          <em>{p.unit}</em>
                          {canEdit && !isDefault && <button type="button" className="geo-icon-btn" title={`По умолчанию: ${fmt(p.default, 4)}`} aria-label="Вернуть значение по умолчанию" onClick={() => toDefault(s, p.key)}><RotateCcw {...ICON} size={12} /></button>}
                        </span>
                        <small>{bad ?? `${fmt(p.min, 4)}…${fmt(p.max, 4)} · по умолч. ${fmt(p.default, 4)}`}</small>
                      </label>
                    );
                  })}
                </div>
              )}
              {err && !errField && <p className="geo-field-error" role="alert">{err.message}</p>}
            </li>
          );
        })}
      </ul>
      <div className={`geo-savebar ${dirtyIds.length ? "is-dirty" : ""}`}>
        <span>{dirtyIds.length ? `Изменено сценариев: ${dirtyIds.length}` : "Изменений нет"}</span>
        {canEdit && <>
          <button type="button" className="button button-small" disabled={!dirtyIds.length || busy} onClick={() => { setDrafts(base); setErrors({}); }}><RotateCcw {...ICON} size={13} /> Сбросить</button>
          <button type="button" className="button button-small button-primary" disabled={!dirtyIds.length || busy || invalid} onClick={() => void save()}><Save {...ICON} size={13} /> Сохранить</button>
        </>}
      </div>
      {changed && <RecomputeNotice key={changed} cameraId={cameraId} what={changed} />}
    </div>
  );
}
