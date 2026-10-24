// Tab «Зоны» (tech.md 8.11, S9): zones of the camera drawn on its frame.
// Polygon or line by the geometry of the zone kind, normalized coordinates, soft delete.
import { useEffect, useMemo, useState } from "react";
import { Eye, EyeOff, Hexagon, Lock, MousePointer2, Plus, RotateCcw, Save, Spline, Trash2, Undo2 } from "lucide-react";
import { api, apiError, type ApiFailure } from "../../api/client";
import type { Zone } from "../../api/types";
import { useApi } from "../../api/useApi";
import { useRole } from "../../roles";
import { ErrorNotice, Loading } from "../../components/ui";
import { GeometryEditor, type EditTarget } from "./editor";
import { centroid, fmt, nameProblem, pct, polygonArea, samePoints, svgPoints, zoneProblem, ZONE_NAME_MAX, ZONE_POINTS_MAX, type Pt } from "./geometry";
import { ConfirmButton, FieldError, FormError, FrameStage, ICON, RecomputeNotice, useSetupMeta } from "./shared";
import "../../styles/geometry.css";

type KindMeta = { id: string; title: string; color: string; geometry: "polygon" | "line"; description: string };
interface Draft { id: number | "new"; kind: string; name: string; points: Pt[]; closed: boolean }

const fromZone = (z: Zone): Draft => ({ id: z.id, kind: z.kind, name: z.name, points: z.points.map((p) => [p[0], p[1]] as Pt), closed: true });

export function ZoneLabel({ x, y, text, sub, color, selected }: { x: number; y: number; text: string; sub?: string; color: string; selected?: boolean }) {
  const width = Math.max(text.length * 6.6, (sub?.length ?? 0) * 5.6) + 14;
  const height = sub ? 30 : 18;
  return (
    <g className={`geo-label ${selected ? "is-selected" : ""}`} transform={`translate(${Math.round(x - width / 2)},${Math.round(y - height / 2)})`} pointerEvents="none">
      <rect width={width} height={height} rx={1} />
      <rect width={2} height={height} fill={color} />
      <text x={8} y={12.5} className="geo-label-title">{text}</text>
      {sub && <text x={8} y={24.5} className="geo-label-sub">{sub}</text>}
    </g>
  );
}

/** A saved zone on the frame (not editable). */
export function ZoneShape({ zone, kind, w, h, selected, dim, onPick, showLabel = true }: {
  zone: { points: readonly (readonly number[])[]; name: string };
  kind?: KindMeta; w: number; h: number; selected?: boolean; dim?: boolean; onPick?: () => void; showLabel?: boolean;
}) {
  const color = kind?.color ?? "#9a9a9a";
  const line = kind?.geometry === "line";
  const c = line ? [(zone.points[0][0] + zone.points[1][0]) / 2, (zone.points[0][1] + zone.points[1][1]) / 2] : centroid(zone.points);
  return (
    <g
      className={`geo-zone ${line ? "is-line" : ""} ${selected ? "is-selected" : ""} ${dim ? "is-dim" : ""} ${onPick ? "is-pickable" : ""}`}
      style={{ color }}
      onPointerDown={onPick ? (e) => { e.stopPropagation(); onPick(); } : undefined}
    >
      {line ? (
        <>
          <polyline className="geo-zone-hit" points={svgPoints(zone.points, w, h)} />
          <polyline className="geo-zone-line" points={svgPoints(zone.points, w, h)} />
          {zone.points.map((p, i) => <rect key={i} className="geo-zone-end" x={p[0] * w - 3} y={p[1] * h - 3} width={6} height={6} />)}
        </>
      ) : (
        <polygon className="geo-zone-poly" points={svgPoints(zone.points, w, h)} />
      )}
      {showLabel && <ZoneLabel x={c[0] * w} y={c[1] * h} text={zone.name || "Без названия"} sub={kind?.title} color={color} selected={selected} />}
    </g>
  );
}

export function ZonesTab({ cameraId }: { cameraId: number }) {
  const [role] = useRole();
  const { meta, error: metaError } = useSetupMeta();
  const zones = useApi(() => api.GET("/api/cameras/{camera_id}/zones", { params: { path: { camera_id: cameraId } } }), [cameraId]);
  const kinds = useMemo(() => (meta?.zone_kinds ?? []) as KindMeta[], [meta]);
  const kindOf = (id: string) => kinds.find((k) => k.id === id);
  const canEdit = role === "admin" || role === "ohs";

  const [draft, setDraft] = useState<Draft | null>(null);
  const [vertex, setVertex] = useState<number | null>(null);
  const [hidden, setHidden] = useState<Set<number>>(new Set());
  const [labels, setLabels] = useState(true);
  const [cursor, setCursor] = useState<Pt | null>(null);
  const [error, setError] = useState<ApiFailure>();
  const [busy, setBusy] = useState(false);
  const [changed, setChanged] = useState<string>();

  const list = zones.data ?? [];
  const saved = draft && draft.id !== "new" ? list.find((z) => z.id === draft.id) : undefined;
  const kind = draft ? kindOf(draft.kind) : undefined;
  const dirty = !!draft && (draft.id === "new" || !saved || saved.name !== draft.name || !samePoints(saved.points, draft.points));
  const geometryProblem = draft && kind && (draft.closed || kind.geometry === "line") ? zoneProblem(kind.geometry, draft.points) : null;

  // The selected zone disappeared (deleted elsewhere): drop the draft.
  useEffect(() => { if (draft && draft.id !== "new" && zones.data && !saved) setDraft(null); }, [draft, saved, zones.data]);

  const select = (z: Zone | null) => { setDraft(z ? fromZone(z) : null); setVertex(null); setError(undefined); };
  const startNew = (kindId?: string) => {
    const k = kindOf(kindId ?? "") ?? kinds.find((x) => x.geometry === "polygon") ?? kinds[0];
    if (!k) return;
    setDraft({ id: "new", kind: k.id, name: "", points: [], closed: false });
    setVertex(null); setError(undefined);
  };
  const cancel = () => {
    if (!draft) return;
    if (draft.id === "new") setDraft(null);
    else if (saved) setDraft(fromZone(saved));
    setVertex(null); setError(undefined);
  };

  const save = async () => {
    if (!draft || !kind) return;
    setBusy(true); setError(undefined);
    const name = draft.name.trim();
    const r = draft.id === "new"
      ? await api.POST("/api/cameras/{camera_id}/zones", { params: { path: { camera_id: cameraId } }, body: { kind: draft.kind, name, points: draft.points } })
      : await api.PATCH("/api/zones/{zone_id}", {
        params: { path: { zone_id: draft.id } },
        body: { ...(saved?.name !== name ? { name } : {}), ...(saved && samePoints(saved.points, draft.points) ? {} : { points: draft.points }) },
      });
    setBusy(false);
    if (r.error || !r.data) { setError(apiError(r.error)); return; }
    setDraft(fromZone(r.data));
    setChanged(draft.id === "new" ? `Зона «${r.data.name}» добавлена` : `Зона «${r.data.name}» сохранена`);
    zones.reload();
  };

  const remove = async () => {
    if (!draft || draft.id === "new") return;
    setBusy(true); setError(undefined);
    const r = await api.DELETE("/api/zones/{zone_id}", { params: { path: { zone_id: draft.id } } });
    setBusy(false);
    if (r.error) { setError(apiError(r.error)); return; }
    setChanged(`Зона «${draft.name}» удалена`);
    setDraft(null);
    zones.reload();
  };

  if (zones.error) return <ErrorNotice error={zones.error} retry={zones.reload} />;
  if (metaError) return <ErrorNotice error={metaError} />;
  if (zones.loading && !zones.data) return <Loading text="Загружаем зоны камеры" />;

  const edit: EditTarget | null = draft && canEdit ? { points: draft.points, geometry: kind?.geometry ?? "polygon", closed: draft.closed, color: kind?.color ?? "#fff" } : null;
  const drawingNew = draft?.id === "new";
  const hint = !draft
    ? (canEdit ? "Выберите зону на кадре или в списке. «Новая зона» — начать рисовать." : "Только просмотр")
    : kind?.geometry === "line"
      ? (draft.points.length < 2 ? `Линия: щёлкните ${draft.points.length ? "конец" : "начало"} ограждения · Esc — отмена` : "Тяните концы линии · Esc — вернуть")
      : !draft.closed
        ? `Щелчок — точка (${draft.points.length}/${ZONE_POINTS_MAX}) · двойной щелчок, Enter или первая точка — замкнуть · Esc — отмена`
        : "Тяните вершины и зону целиком · ⊕ на ребре — новая вершина · ПКМ или Delete — удалить вершину · стрелки — сдвиг на 1 px";

  return (
    <div className="geo-workspace geo-ws-zones" data-testid="zones-tab">
      <aside className="geo-side geo-layers" data-panel="Зоны камеры">
        <div className="geo-side-head">
          <span>{list.length ? `${list.length} ${plural(list.length, "зона", "зоны", "зон")}` : "Зон нет"}</span>
          {canEdit && <button type="button" className="button button-small button-primary" onClick={() => startNew()} disabled={!kinds.length}><Plus {...ICON} size={13} /> Новая зона</button>}
        </div>
        {list.length === 0 && !drawingNew && <p className="geo-empty">Без зон работают только сценарии, которым зоны не нужны: бег, сближение с техникой, телефон, падение.</p>}
        <ul className="geo-layer-list">
          {drawingNew && draft && (
            <li className="is-selected"><span className="geo-swatch" style={{ background: kind?.color }} /><span className="geo-layer-name"><b>Новая зона</b><small>{kind?.title} · рисуется</small></span></li>
          )}
          {list.map((z) => {
            const k = kindOf(z.kind);
            const off = hidden.has(z.id);
            return (
              <li key={z.id} className={`${draft?.id === z.id ? "is-selected" : ""} ${off ? "is-off" : ""}`}>
                <button type="button" className="geo-layer-main" onClick={() => select(z)}>
                  <span className="geo-swatch" style={{ background: k?.color }} />
                  {k?.geometry === "line" ? <Spline {...ICON} size={14} /> : <Hexagon {...ICON} size={14} />}
                  <span className="geo-layer-name"><b>{z.name}</b><small>{k?.title ?? z.kind} · {z.points.length} {plural(z.points.length, "точка", "точки", "точек")}</small></span>
                  {draft?.id === z.id && dirty && <span className="geo-dirty" title="Есть несохранённые изменения">●</span>}
                </button>
                <button type="button" className="geo-icon-btn" aria-label={off ? "Показать зону" : "Скрыть зону"} title={off ? "Показать" : "Скрыть"}
                  onClick={() => setHidden((s) => { const n = new Set(s); if (n.has(z.id)) n.delete(z.id); else n.add(z.id); return n; })}>
                  {off ? <EyeOff {...ICON} size={14} /> : <Eye {...ICON} size={14} />}
                </button>
              </li>
            );
          })}
        </ul>
        <div className="geo-legend">
          {kinds.map((k) => (
            <button type="button" key={k.id} className="geo-legend-item" disabled={!canEdit} onClick={() => startNew(k.id)} title={canEdit ? `Нарисовать: ${k.description}` : k.description}>
              <span className="geo-swatch" style={{ background: k.color }} />{k.title}{k.geometry === "line" && <small>линия</small>}
            </button>
          ))}
        </div>
      </aside>

      <FrameStage
        cameraId={cameraId}
        className="geo-center"
        toolbar={<>
          <span className={`geo-tool ${!drawingNew ? "is-active" : ""}`}><MousePointer2 {...ICON} size={14} /> Выбор</span>
          <span className={`geo-tool ${drawingNew ? "is-active" : ""}`}>{kind?.geometry === "line" ? <Spline {...ICON} size={14} /> : <Hexagon {...ICON} size={14} />} {drawingNew ? `Рисуем: ${kind?.title}` : "Рисование"}</span>
          <span className="geo-toolbar-sep" />
          <label className="geo-check"><input type="checkbox" checked={labels} onChange={(e) => setLabels(e.target.checked)} /> Подписи</label>
          {!canEdit && <span className="geo-readonly"><Lock {...ICON} size={13} /> Только просмотр</span>}
        </>}
        statusbar={<>
          <span className="geo-hint">{hint}</span>
          <span className="geo-coords">{cursor ? `x ${fmt(cursor[0], 3)} · y ${fmt(cursor[1], 3)}` : "x — · y —"}</span>
        </>}
      >
        {({ w, h }) => (
          <GeometryEditor
            w={w} h={h} edit={edit} readOnly={!canEdit}
            onChange={(points, closed) => setDraft((d) => (d ? { ...d, points, closed } : d))}
            onCancel={draft ? cancel : undefined}
            onCursor={setCursor}
            selected={vertex} onSelect={setVertex}
            maxPoints={kind?.geometry === "line" ? 2 : ZONE_POINTS_MAX}
            onBackground={() => { if (draft && draft.id !== "new" && !dirty) select(null); }}
          >
            {list.filter((z) => !hidden.has(z.id)).map((z) => draft?.id === z.id && canEdit
              ? labels && <ZoneLabelFor key={z.id} draft={draft} kind={kind} w={w} h={h} />
              : <ZoneShape key={z.id} zone={z} kind={kindOf(z.kind)} w={w} h={h} dim={!!draft} showLabel={labels} onPick={dirty ? undefined : () => select(z)} />)}
            {drawingNew && draft && draft.closed && labels && <ZoneLabelFor draft={draft} kind={kind} w={w} h={h} />}
          </GeometryEditor>
        )}
      </FrameStage>

      <aside className="geo-side geo-props" data-panel="Свойства">
        {!draft ? (
          <div className="geo-props-empty">
            <p>Зона не выбрана.</p>
            <p className="geo-muted">Координаты хранятся в долях кадра (0…1), поэтому разметка не зависит от разрешения видео. Правила анализа видят зоны снимка конфигурации на момент анализа.</p>
          </div>
        ) : (
          <form className="geo-form" onSubmit={(e) => { e.preventDefault(); if (canEdit && dirty && !busy) void save(); }}>
            <div className="geo-props-title">
              <span className="geo-swatch" style={{ background: kind?.color }} />
              <b>{draft.id === "new" ? "Новая зона" : `Зона №${draft.id}`}</b>
              {dirty && <span className="geo-badge-dirty">не сохранено</span>}
            </div>
            <label className="geo-field">
              <span>Название</span>
              <input value={draft.name} maxLength={ZONE_NAME_MAX} disabled={!canEdit} placeholder="Например, «Пресс №2»" aria-invalid={error?.details?.field === "name"}
                onChange={(e) => setDraft({ ...draft, name: e.target.value })} />
              <FieldError error={error} field="name" />
            </label>
            <label className="geo-field">
              <span>Тип</span>
              <select value={draft.kind} disabled={!canEdit || draft.id !== "new"} aria-invalid={error?.details?.field === "kind"}
                onChange={(e) => {
                  const next = kindOf(e.target.value);
                  const keep = next?.geometry === kind?.geometry;
                  setDraft({ ...draft, kind: e.target.value, points: keep ? draft.points : [], closed: keep ? draft.closed : false });
                }}>
                {kinds.map((k) => <option key={k.id} value={k.id}>{k.title}{k.geometry === "line" ? " (линия)" : ""}</option>)}
              </select>
              {draft.id !== "new" && <small className="geo-muted">Тип сохранённой зоны не меняется: удалите зону и нарисуйте новую.</small>}
              {kind && <small className="geo-muted">{kind.description}</small>}
              <FieldError error={error} field="kind" />
            </label>
            <div className="geo-field">
              <span>Геометрия</span>
              <dl className="geo-facts">
                <dt>Форма</dt><dd>{kind?.geometry === "line" ? "Линия" : draft.closed ? "Полигон, замкнут" : "Полигон, рисуется"}</dd>
                <dt>Точек</dt><dd>{draft.points.length}{kind?.geometry === "line" ? " из 2" : ` (3…${ZONE_POINTS_MAX})`}</dd>
                {kind?.geometry !== "line" && <><dt>Площадь</dt><dd>{draft.points.length >= 3 ? pct(polygonArea(draft.points)) + " кадра" : "—"}</dd></>}
              </dl>
              <FieldError error={error} field="points" also={geometryProblem} />
            </div>
            {draft.points.length > 0 && (
              <div className="geo-field">
                <span>Вершины</span>
                <ol className="geo-vertices">
                  {draft.points.map((p, i) => (
                    <li key={i} className={vertex === i ? "is-selected" : ""}>
                      <button type="button" onClick={() => setVertex(i)}><b>{i + 1}</b><span>{fmt(p[0], 3)}</span><span>{fmt(p[1], 3)}</span></button>
                    </li>
                  ))}
                </ol>
              </div>
            )}
            <FormError error={error} fields={["name", "kind", "points"]} />
            {canEdit && (
              <div className="geo-actions">
                <button type="submit" className="button button-small button-primary" disabled={!dirty || busy || !!geometryProblem || !draft.closed || !!nameProblem(draft.name)}
                  title={nameProblem(draft.name) ?? geometryProblem ?? (draft.closed ? "" : "Сначала замкните полигон")}>
                  <Save {...ICON} size={13} /> {draft.id === "new" ? "Добавить зону" : "Сохранить"}
                </button>
                <button type="button" className="button button-small" disabled={!dirty || busy} onClick={cancel}>
                  {draft.id === "new" ? <><Undo2 {...ICON} size={13} /> Отменить</> : <><RotateCcw {...ICON} size={13} /> Вернуть</>}
                </button>
                {draft.id !== "new" && (
                  <ConfirmButton label="Удалить" icon={<Trash2 {...ICON} size={13} />} disabled={busy}
                    confirm={`Удалить зону «${saved?.name ?? draft.name}»? Прошлые события сохранят ссылку на неё.`} onConfirm={() => void remove()} />
                )}
              </div>
            )}
          </form>
        )}
        {changed && <RecomputeNotice key={changed} cameraId={cameraId} what={changed} />}
      </aside>
    </div>
  );
}

function ZoneLabelFor({ draft, kind, w, h }: { draft: Draft; kind?: KindMeta; w: number; h: number }) {
  if (draft.points.length < 2) return null;
  const line = kind?.geometry === "line";
  const c = line ? [(draft.points[0][0] + draft.points[1][0]) / 2, (draft.points[0][1] + draft.points[1][1]) / 2] : centroid(draft.points);
  return <ZoneLabel x={c[0] * w} y={c[1] * h} text={draft.name || "Без названия"} sub={kind?.title} color={kind?.color ?? "#fff"} selected />;
}

export function plural(n: number, one: string, few: string, many: string): string {
  const a = Math.abs(n) % 100, b = a % 10;
  if (a > 10 && a < 20) return many;
  if (b === 1) return one;
  if (b >= 2 && b <= 4) return few;
  return many;
}
