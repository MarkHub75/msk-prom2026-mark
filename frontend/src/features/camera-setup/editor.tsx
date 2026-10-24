// Vertex editor over the camera frame: draw a polygon / line / point set, drag vertices,
// insert on edge midpoints, delete with right click or Delete, Enter closes, Esc cancels.
import { useEffect, useRef, useState, type PointerEvent as ReactPointerEvent, type ReactNode } from "react";
import { hitEdge, hitVertex, insertVertex, moveVertex, pointInPolygon, removeVertex, samePoints, svgPoints, toNorm, toPx, translate, type Pt } from "./geometry";

export type EditGeometry = "polygon" | "line" | "points";

export interface EditTarget {
  points: Pt[];
  geometry: EditGeometry;
  /** Polygon finished (Enter / double click / click on the first vertex); a line is closed with 2 points. */
  closed: boolean;
  color: string;
}

type Drag = { kind: "vertex"; i: number; moved: boolean } | { kind: "shape"; start: Pt; orig: Pt[] } | null;

export function minPoints(g: EditGeometry): number {
  return g === "polygon" ? 3 : g === "line" ? 2 : 0;
}

export function GeometryEditor({
  w, h, edit, onChange, onCancel, onCursor, selected, onSelect, maxPoints, readOnly = false, labels, children, onBackground,
}: {
  w: number; h: number;
  edit: EditTarget | null;
  onChange: (points: Pt[], closed: boolean) => void;
  onCancel?: () => void;
  onCursor?: (p: Pt | null) => void;
  selected: number | null;
  onSelect: (i: number | null) => void;
  maxPoints: number;
  readOnly?: boolean;
  /** Vertex captions (calibration numbers). */
  labels?: (i: number) => string;
  /** Static layers under the editable shape. */
  children?: ReactNode;
  /** Click on empty frame when there is nothing to draw. */
  onBackground?: (p: Pt) => void;
}) {
  const svg = useRef<SVGSVGElement>(null);
  const [cursor, setCursor] = useState<Pt | null>(null);
  const [drag, setDrag] = useState<Drag>(null);
  const pts = edit?.points ?? [];
  const drawing = !!edit && !readOnly && (edit.geometry === "points" ? pts.length < maxPoints : !edit.closed);
  const canDelete = (n: number) => !!edit && (edit.geometry === "points" || (edit.geometry === "polygon" && (!edit.closed || n > 3)));

  const at = (e: { clientX: number; clientY: number }): Pt => toNorm(e.clientX, e.clientY, svg.current!.getBoundingClientRect());

  // Keyboard while an editable shape is on the frame; typing in the side panel is not intercepted.
  const latest = useRef({ edit, selected, drawing, onChange, onCancel, onSelect, canDelete, w, h });
  latest.current = { edit, selected, drawing, onChange, onCancel, onSelect, canDelete, w, h };
  useEffect(() => {
    if (readOnly) return;
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.tagName === "SELECT" || t.isContentEditable)) return;
      const { edit: ed, selected: sel, onChange: change, onCancel: cancel, onSelect: select, canDelete: del, w: W, h: H } = latest.current;
      if (e.key === "Escape") { if (cancel) { e.preventDefault(); cancel(); } return; }
      if (!ed) return;
      if (e.key === "Enter" && ed.geometry === "polygon" && !ed.closed && ed.points.length >= 3) { e.preventDefault(); change(ed.points, true); return; }
      if ((e.key === "Delete" || e.key === "Backspace") && sel !== null && del(ed.points.length)) {
        e.preventDefault();
        change(removeVertex(ed.points, sel), ed.closed);
        select(null);
        return;
      }
      const arrows: Record<string, Pt> = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] };
      if (arrows[e.key] && sel !== null && ed.points[sel]) {
        e.preventDefault();
        const k = e.shiftKey ? 10 : 1;
        const p = ed.points[sel];
        change(moveVertex(ed.points, sel, [p[0] + (arrows[e.key][0] * k) / W, p[1] + (arrows[e.key][1] * k) / H]), ed.closed);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [readOnly]);

  const down = (e: ReactPointerEvent<SVGSVGElement>) => {
    if (readOnly || e.button !== 0 || !svg.current) return;
    const p = at(e);
    if (!edit) { onBackground?.(p); return; }
    const vi = hitVertex(pts, p, w, h);
    if (vi >= 0) {
      if (edit.geometry === "polygon" && !edit.closed && vi === 0 && pts.length >= 3) { onChange(pts, true); return; }
      onSelect(vi);
      setDrag({ kind: "vertex", i: vi, moved: false });
      svg.current.setPointerCapture?.(e.pointerId);
      return;
    }
    if (drawing) {
      const last = pts[pts.length - 1];
      // The second click of a double click lands on the last point: not a new vertex.
      if (last && Math.hypot((last[0] - p[0]) * w, (last[1] - p[1]) * h) < 4) return;
      if (pts.length >= maxPoints) return;
      const next = [...pts, p];
      onChange(next, edit.geometry === "line" ? next.length === 2 : false);
      onSelect(next.length - 1);
      return;
    }
    if (edit.geometry !== "points" && edit.closed) {
      const edge = (edit.geometry === "polygon" && pts.length < maxPoints) ? midpointHit(pts, p, w, h) : -1;
      if (edge >= 0) {
        onChange(insertVertex(pts, edge, p), true);
        onSelect(edge + 1);
        setDrag({ kind: "vertex", i: edge + 1, moved: false });
        svg.current.setPointerCapture?.(e.pointerId);
        return;
      }
      const inside = edit.geometry === "polygon" ? pointInPolygon(p, pts) : hitEdge(pts, p, w, h, false) >= 0;
      if (inside) {
        setDrag({ kind: "shape", start: p, orig: pts });
        svg.current.setPointerCapture?.(e.pointerId);
        return;
      }
    }
    onSelect(null);
    onBackground?.(p);
  };

  const move = (e: ReactPointerEvent<SVGSVGElement>) => {
    if (!svg.current) return;
    const p = at(e);
    setCursor(p);
    onCursor?.(p);
    if (!drag || !edit) return;
    if (drag.kind === "vertex") {
      if (!samePoints([pts[drag.i]], [p])) { onChange(moveVertex(pts, drag.i, p), edit.closed); if (!drag.moved) setDrag({ ...drag, moved: true }); }
    } else {
      onChange(translate(drag.orig, p[0] - drag.start[0], p[1] - drag.start[1]), edit.closed);
    }
  };

  const up = (e: ReactPointerEvent<SVGSVGElement>) => {
    if (drag) svg.current?.releasePointerCapture?.(e.pointerId);
    setDrag(null);
  };

  const dbl = (e: React.MouseEvent<SVGSVGElement>) => {
    if (readOnly || !edit || !svg.current) return;
    if (edit.geometry === "polygon" && !edit.closed && pts.length >= 3) { e.preventDefault(); onChange(pts, true); return; }
    if (edit.geometry === "polygon" && edit.closed && pts.length < maxPoints) {
      const p = at(e);
      const edge = hitVertex(pts, p, w, h) < 0 ? hitEdge(pts, p, w, h, true) : -1;
      if (edge >= 0) { onChange(insertVertex(pts, edge, p), true); onSelect(edge + 1); }
    }
  };

  const context = (e: React.MouseEvent<SVGSVGElement>) => {
    if (readOnly || !edit || !svg.current) return;
    const vi = hitVertex(pts, at(e), w, h);
    if (vi < 0) return;
    e.preventDefault();
    if (canDelete(pts.length)) { onChange(removeVertex(pts, vi), edit.closed); onSelect(null); }
  };

  const nearFirst = drawing && edit?.geometry === "polygon" && pts.length >= 3 && cursor && hitVertex([pts[0]], cursor, w, h, 9) === 0;
  const color = edit?.color ?? "#fff";
  const px = (p: Pt) => toPx(p, w, h);
  const showMid = edit && !readOnly && edit.geometry === "polygon" && edit.closed && pts.length < maxPoints;

  return (
    <svg
      ref={svg}
      className={`geo-overlay ${drawing ? "is-drawing" : ""} ${drag?.kind === "shape" ? "is-moving" : ""}`}
      width={w} height={h} viewBox={`0 0 ${w} ${h}`}
      onPointerDown={down} onPointerMove={move} onPointerUp={up} onPointerCancel={up}
      onPointerLeave={() => { setCursor(null); onCursor?.(null); }}
      onDoubleClick={dbl} onContextMenu={context}
      data-testid="geometry-editor"
    >
      <defs>
        <clipPath id="geo-frame-clip"><rect x="0" y="0" width={w} height={h} /></clipPath>
      </defs>
      <g clipPath="url(#geo-frame-clip)">
        {children}
        {edit && pts.length > 0 && (
          <g className="geo-edit" style={{ color }}>
            {edit.geometry === "polygon" && (edit.closed
              ? <polygon className="geo-edit-shape" points={svgPoints(pts, w, h)} />
              : <polyline className="geo-edit-path" points={svgPoints(pts, w, h)} />)}
            {edit.geometry === "line" && pts.length === 2 && <polyline className="geo-edit-path" points={svgPoints(pts, w, h)} />}
            {drawing && cursor && edit.geometry !== "points" && (
              <>
                <line className="geo-rubber" x1={px(pts[pts.length - 1])[0]} y1={px(pts[pts.length - 1])[1]} x2={px(cursor)[0]} y2={px(cursor)[1]} />
                {edit.geometry === "polygon" && pts.length >= 2 && <line className="geo-rubber geo-rubber-close" x1={px(cursor)[0]} y1={px(cursor)[1]} x2={px(pts[0])[0]} y2={px(pts[0])[1]} />}
              </>
            )}
            {showMid && pts.map((p, i) => {
              const q = pts[(i + 1) % pts.length];
              const [mx, my] = px([(p[0] + q[0]) / 2, (p[1] + q[1]) / 2]);
              return <circle key={`m${i}`} className="geo-mid" cx={mx} cy={my} r={3.5} />;
            })}
            {pts.map((p, i) => {
              const [x, y] = px(p);
              const first = i === 0 && nearFirst;
              return (
                <g key={i} className={`geo-handle ${selected === i ? "is-selected" : ""} ${first ? "is-closer" : ""}`} data-testid="vertex">
                  {first && <circle cx={x} cy={y} r={9} className="geo-closer-ring" />}
                  <rect x={x - 4} y={y - 4} width={8} height={8} />
                  {labels && <text x={x + 8} y={y - 7} className="geo-handle-label">{labels(i)}</text>}
                </g>
              );
            })}
          </g>
        )}
        {!readOnly && cursor && drawing && (
          <g className="geo-crosshair" aria-hidden="true">
            <line x1={0} y1={px(cursor)[1]} x2={w} y2={px(cursor)[1]} />
            <line x1={px(cursor)[0]} y1={0} x2={px(cursor)[0]} y2={h} />
          </g>
        )}
      </g>
    </svg>
  );
}

/** Edge whose midpoint handle is under p (polygon closed), or -1. */
function midpointHit(points: readonly Pt[], p: Pt, w: number, h: number): number {
  for (let i = 0; i < points.length; i++) {
    const a = points[i], b = points[(i + 1) % points.length];
    if (hitVertex([[(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]], p, w, h, 6) === 0) return i;
  }
  return -1;
}
