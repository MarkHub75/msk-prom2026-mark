// Tab «Калибровка» (tech.md 8.11, S9): 4–8 floor points on the frame with their meters,
// optional control points, the 1 m grid of the saved calibration and a browser preview of the draft.
import { useEffect, useMemo, useState } from "react";
import { Crosshair, Diamond, Eraser, Grid3x3, Lock, RotateCcw, Save, Trash2, X } from "lucide-react";
import { api, apiError, type ApiFailure } from "../../api/client";
import type { Calibration } from "../../api/types";
import { useApi } from "../../api/useApi";
import { useRole } from "../../roles";
import { ErrorNotice, Loading, time } from "../../components/ui";
import { GeometryEditor } from "./editor";
import { CAL_POINTS_MAX, CAL_POINTS_MIN, convexHull, fitHomography, fitRmse, fmt, gridPreview, parseNumber, svgPoints, type Pt } from "./geometry";
import { ConfirmButton, FieldError, FormError, FrameStage, ICON, RecomputeNotice } from "./shared";
import "../../styles/geometry.css";

interface Row { image: Pt; x: string; y: string }
type SetId = "fit" | "control";
interface Draft { fit: Row[]; control: Row[] }

const num = (v: number) => String(v).replace(".", ",");
function fromCalibration(c: Calibration | null | undefined): Draft {
  if (!c) return { fit: [], control: [] };
  return {
    fit: c.image_points.map((p, i) => ({ image: [p[0], p[1]], x: num(c.world_points[i]?.[0] ?? 0), y: num(c.world_points[i]?.[1] ?? 0) })),
    control: c.control_points.map((cp) => ({ image: [cp.image[0], cp.image[1]], x: num(cp.world[0]), y: num(cp.world[1]) })),
  };
}
const sameDraft = (a: Draft, b: Draft) => JSON.stringify(a) === JSON.stringify(b);
const world = (r: Row): Pt | null => { const x = parseNumber(r.x), y = parseNumber(r.y); return x === null || y === null ? null : [x, y]; };

/** Draft rows → CalibrationIn, or the first problem (backend texts). */
export function calibrationBody(d: Draft): { body?: { image_points: Pt[]; world_points: Pt[]; control_points: { image: Pt; world: Pt }[] }; problem?: string } {
  if (d.fit.length < CAL_POINTS_MIN || d.fit.length > CAL_POINTS_MAX) return { problem: `Нужно от ${CAL_POINTS_MIN} до ${CAL_POINTS_MAX} точек` };
  const fw = d.fit.map(world), cw = d.control.map(world);
  if (fw.some((p) => !p) || cw.some((p) => !p)) return { problem: "Заполните метры у всех точек: число, например 2,5" };
  return { body: { image_points: d.fit.map((r) => r.image), world_points: fw as Pt[], control_points: d.control.map((r, i) => ({ image: r.image, world: cw[i] as Pt })) } };
}

export function CalibrationTab({ cameraId }: { cameraId: number }) {
  const [role] = useRole();
  const canEdit = role === "admin";
  const cal = useApi(() => api.GET("/api/cameras/{camera_id}/calibration", { params: { path: { camera_id: cameraId } } }), [cameraId]);
  const saved = cal.data ?? null;
  const base = useMemo(() => fromCalibration(saved), [saved]);
  const [draft, setDraft] = useState<Draft>(base);
  const [active, setActive] = useState<SetId>("fit");
  const [selected, setSelected] = useState<number | null>(null);
  const [error, setError] = useState<ApiFailure>();
  const [problem, setProblem] = useState<string>();
  const [busy, setBusy] = useState(false);
  const [showGrid, setShowGrid] = useState(true);
  const [changed, setChanged] = useState<string>();
  const [cursor, setCursor] = useState<Pt | null>(null);

  useEffect(() => { setDraft(base); setSelected(null); }, [base]);

  const dirty = !sameDraft(draft, base);
  const rows = draft[active];
  const other: SetId = active === "fit" ? "control" : "fit";

  const preview = useMemo(() => {
    const image = draft.fit.map((r) => r.image), w = draft.fit.map(world);
    if (image.length < CAL_POINTS_MIN || w.some((p) => !p)) return null;
    const h = fitHomography(image, w as Pt[]);
    if (!h) return null;
    const cw = draft.control.map(world);
    const controlOk = draft.control.length > 0 && cw.every(Boolean);
    return { grid: gridPreview(h, w as Pt[]), fit: fitRmse(h, image, w as Pt[]), control: controlOk ? fitRmse(h, draft.control.map((r) => r.image), cw as Pt[]) : null };
  }, [draft]);

  const setRows = (set: SetId, next: Row[]) => setDraft((d) => ({ ...d, [set]: next }));
  const onPoints = (points: Pt[]) => {
    // Points added, moved or removed on the frame; meters stay with their row.
    setRows(active, points.map((p, i) => {
      const old = rows[i];
      if (points.length < rows.length) {
        // A removed vertex: keep the meters of the remaining ones by position.
        const k = rows.findIndex((r) => r.image[0] === p[0] && r.image[1] === p[1]);
        return k >= 0 ? rows[k] : { image: p, x: "", y: "" };
      }
      return old ? { ...old, image: p } : { image: p, x: "", y: "" };
    }));
  };
  const edit = (set: SetId, i: number, axis: "x" | "y", value: string) => setDraft((d) => ({ ...d, [set]: d[set].map((r, k) => (k === i ? { ...r, [axis]: value } : r)) }));
  const removeRow = (set: SetId, i: number) => { setRows(set, draft[set].filter((_, k) => k !== i)); setSelected(null); };

  const save = async () => {
    setError(undefined); setProblem(undefined);
    const { body, problem: p } = calibrationBody(draft);
    if (!body) { setProblem(p); return; }
    setBusy(true);
    const r = await api.PUT("/api/cameras/{camera_id}/calibration", { params: { path: { camera_id: cameraId } }, body });
    setBusy(false);
    if (r.error) { setError(apiError(r.error)); return; }
    setChanged("Калибровка сохранена");
    cal.reload();
  };
  const remove = async () => {
    setError(undefined); setBusy(true);
    const r = await api.DELETE("/api/cameras/{camera_id}/calibration", { params: { path: { camera_id: cameraId } } });
    setBusy(false);
    if (r.error) { setError(apiError(r.error)); return; }
    setChanged("Калибровка удалена: скорость и дистанции снова в ростах человека");
    cal.reload();
  };

  if (cal.error) return <ErrorNotice error={cal.error} retry={cal.reload} />;
  if (cal.loading && cal.data === undefined) return <Loading text="Загружаем калибровку" />;

  const label = (set: SetId) => (i: number) => {
    const r = draft[set][i];
    const m = r && world(r);
    return `${set === "fit" ? i + 1 : `К${i + 1}`}${m ? ` · ${fmt(m[0])}; ${fmt(m[1])} м` : ""}`;
  };
  const hull = convexHull(draft.fit.map((r) => r.image));
  const gridLines = !dirty && saved ? saved.grid : preview?.grid ?? [];
  const gridKind = !dirty && saved ? "saved" : preview ? "preview" : null;
  const fieldErr = (f: string) => error?.details?.field === f;

  return (
    <div className="geo-workspace geo-ws-cal" data-testid="calibration-tab">
      <FrameStage
        cameraId={cameraId}
        className="geo-center geo-center-wide"
        toolbar={<>
          <div className="geo-seg" role="radiogroup" aria-label="Какие точки ставить">
            <button type="button" role="radio" aria-checked={active === "fit"} className={active === "fit" ? "is-active" : ""} onClick={() => { setActive("fit"); setSelected(null); }}>
              <Crosshair {...ICON} size={14} /> Опорные {draft.fit.length}/{CAL_POINTS_MAX}
            </button>
            <button type="button" role="radio" aria-checked={active === "control"} className={active === "control" ? "is-active" : ""} onClick={() => { setActive("control"); setSelected(null); }}>
              <Diamond {...ICON} size={14} /> Контрольные {draft.control.length}/{CAL_POINTS_MAX}
            </button>
          </div>
          <span className="geo-toolbar-sep" />
          <label className="geo-check"><input type="checkbox" checked={showGrid} onChange={(e) => setShowGrid(e.target.checked)} /> <Grid3x3 {...ICON} size={13} /> Сетка 1 м</label>
          {gridKind === "preview" && showGrid && <span className="geo-chip geo-chip-amber">предпросмотр, не сохранено</span>}
          {gridKind === "saved" && showGrid && <span className="geo-chip">сохранённая калибровка</span>}
          {!canEdit && <span className="geo-readonly"><Lock {...ICON} size={13} /> Калибровку меняет администратор</span>}
        </>}
        statusbar={<>
          <span className="geo-hint">{canEdit
            ? `Щелчок по полу — ${active === "fit" ? "опорная" : "контрольная"} точка · тяните точку · ПКМ или Delete — удалить · метры введите справа`
            : "Только просмотр"}</span>
          <span className="geo-coords">{cursor ? `x ${fmt(cursor[0], 3)} · y ${fmt(cursor[1], 3)}` : "x — · y —"}</span>
        </>}
      >
        {({ w, h }) => (
          <GeometryEditor
            w={w} h={h} readOnly={!canEdit}
            edit={{ points: rows.map((r) => r.image), geometry: "points", closed: false, color: active === "fit" ? "#5aa9f6" : "#e8a33d" }}
            onChange={onPoints}
            onCancel={dirty ? () => setDraft(base) : undefined}
            onCursor={setCursor}
            selected={selected} onSelect={setSelected}
            maxPoints={CAL_POINTS_MAX}
            labels={label(active)}
          >
            {hull.length >= 3 && <polygon className="geo-hull" points={svgPoints(hull, w, h)} />}
            {showGrid && gridLines.length > 0 && (
              <g className={`geo-grid ${gridKind === "preview" ? "is-preview" : ""}`} data-testid="calibration-grid">
                {gridLines.map(([a, b], i) => <line key={i} x1={a[0] * w} y1={a[1] * h} x2={b[0] * w} y2={b[1] * h} />)}
              </g>
            )}
            <g className={`geo-static-points ${other === "control" ? "is-control" : ""}`}>
              {draft[other].map((r, i) => (
                <g key={i} transform={`translate(${r.image[0] * w},${r.image[1] * h})`}>
                  {other === "control" ? <rect x={-4} y={-4} width={8} height={8} transform="rotate(45)" /> : <rect x={-4} y={-4} width={8} height={8} />}
                  <text x={8} y={-7}>{label(other)(i)}</text>
                </g>
              ))}
            </g>
          </GeometryEditor>
        )}
      </FrameStage>

      <aside className="geo-side geo-props geo-props-wide" data-panel="Точки и метры">
        <PointTable title="Опорные точки" note={`${CAL_POINTS_MIN}–${CAL_POINTS_MAX} точек на полу; метры — в своей системе координат пола (например, от угла цеха)`}
          rows={draft.fit} set="fit" active={active} selected={selected} canEdit={canEdit} invalid={fieldErr("image_points") || fieldErr("world_points")}
          onPick={(i) => { setActive("fit"); setSelected(i); }} onEdit={edit} onRemove={removeRow} />
        <FieldError error={error} field="image_points" />
        <FieldError error={error} field="world_points" />
        <PointTable title="Контрольные точки" note="Не участвуют в подгонке: по ним проверяется точность"
          rows={draft.control} set="control" active={active} selected={selected} canEdit={canEdit} invalid={fieldErr("control_points")}
          onPick={(i) => { setActive("control"); setSelected(i); }} onEdit={edit} onRemove={removeRow} />
        <FieldError error={error} field="control_points" />

        <div className="geo-result">
          <h3>Точность</h3>
          {saved ? (
            <dl className="geo-facts">
              <dt>СКО подгонки</dt><dd>{fmt(saved.fit_rmse_m, 3)} м</dd>
              <dt>Контрольные</dt><dd>{saved.control_rmse_m === null ? "нет контрольных точек: точность не проверена" : `${fmt(saved.control_rmse_m, 3)} м`}</dd>
              <dt>Сохранена</dt><dd>{time(saved.updated_at, false)} МСК</dd>
            </dl>
          ) : <p className="geo-muted">Калибровки нет: система работает в ростах человека, и это нормальный режим.</p>}
          {dirty && preview && (
            <p className="geo-preview-note">Оценка в браузере до сохранения: подгонка {fmt(preview.fit, 3)} м{preview.control !== null ? `, контрольные ${fmt(preview.control, 3)} м` : ""}. Итог считает сервер.</p>
          )}
          <p className="geo-muted">Метры и м/с считаются только внутри контура опорных точек (подсвечен на кадре).</p>
        </div>

        {problem && <p className="geo-field-error" role="alert">{problem}</p>}
        <FormError error={error} fields={["image_points", "world_points", "control_points"]} />
        {canEdit && (
          <div className="geo-actions">
            <button type="button" className="button button-small button-primary" disabled={!dirty || busy} onClick={() => void save()}><Save {...ICON} size={13} /> Сохранить</button>
            <button type="button" className="button button-small" disabled={!dirty || busy} onClick={() => { setDraft(base); setError(undefined); setProblem(undefined); }}><RotateCcw {...ICON} size={13} /> Сбросить</button>
            <button type="button" className="button button-small" disabled={busy || (!draft.fit.length && !draft.control.length)} onClick={() => setDraft({ fit: [], control: [] })}><Eraser {...ICON} size={13} /> Очистить</button>
            {saved && <ConfirmButton label="Удалить" icon={<Trash2 {...ICON} size={13} />} disabled={busy} confirm="Удалить калибровку? Скорость и дистанции снова будут в ростах человека." onConfirm={() => void remove()} />}
          </div>
        )}
        {changed && <RecomputeNotice key={changed} cameraId={cameraId} what={changed} />}
      </aside>
    </div>
  );
}

function PointTable({ title, note, rows, set, active, selected, canEdit, invalid, onPick, onEdit, onRemove }: {
  title: string; note: string; rows: Row[]; set: SetId; active: SetId; selected: number | null; canEdit: boolean; invalid: boolean;
  onPick: (i: number) => void; onEdit: (set: SetId, i: number, axis: "x" | "y", v: string) => void; onRemove: (set: SetId, i: number) => void;
}) {
  return (
    <section className={`geo-points ${invalid ? "is-invalid" : ""}`}>
      <h3>{title} <small>{rows.length}</small></h3>
      <p className="geo-muted">{note}</p>
      {rows.length === 0 ? <p className="geo-empty">{canEdit ? "Щёлкните по кадру, выбрав этот набор вверху." : "Точек нет."}</p> : (
        <table className="geo-table">
          <thead><tr><th>№</th><th>Кадр x</th><th>Кадр y</th><th>X, м</th><th>Y, м</th><th aria-label="Удалить" /></tr></thead>
          <tbody>
            {rows.map((r, i) => {
              const bx = parseNumber(r.x) === null, by = parseNumber(r.y) === null;
              return (
                <tr key={i} className={active === set && selected === i ? "is-selected" : ""} onClick={() => onPick(i)}>
                  <td className="geo-num">{set === "fit" ? i + 1 : `К${i + 1}`}</td>
                  <td className="geo-mono">{fmt(r.image[0], 3)}</td>
                  <td className="geo-mono">{fmt(r.image[1], 3)}</td>
                  <td><input aria-label={`X, м точки ${set === "fit" ? i + 1 : `К${i + 1}`}`} inputMode="decimal" value={r.x} disabled={!canEdit} aria-invalid={bx} onFocus={() => onPick(i)} onChange={(e) => { onPick(i); onEdit(set, i, "x", e.target.value); }} /></td>
                  <td><input aria-label={`Y, м точки ${set === "fit" ? i + 1 : `К${i + 1}`}`} inputMode="decimal" value={r.y} disabled={!canEdit} aria-invalid={by} onFocus={() => onPick(i)} onChange={(e) => { onPick(i); onEdit(set, i, "y", e.target.value); }} /></td>
                  <td>{canEdit && <button type="button" className="geo-icon-btn" aria-label="Удалить точку" onClick={(e) => { e.stopPropagation(); onRemove(set, i); }}><X {...ICON} size={13} /></button>}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </section>
  );
}
