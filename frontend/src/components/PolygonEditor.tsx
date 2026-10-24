import type { MouseEvent } from "react";
import type { components } from "../api/schema";

type Point = [number, number];
type Segment = components["schemas"]["Calibration"]["grid"][number];

interface Props {
  image: string;
  mode: "points" | "polygon" | "line";
  value: Point[];
  onChange: (points: Point[]) => void;
  maxPoints: number;
  grid?: Segment[]; // the 1 m floor grid of the calibration, drawn under the points
}

const WIDTH = 640;
const HEIGHT = 360;

// Points in normalized frame coordinates (0..1), placed by clicks on the camera frame.
export function PolygonEditor({ image, mode, value, onChange, maxPoints, grid = [] }: Props) {
  const add = (e: MouseEvent<SVGSVGElement>) => {
    if (value.length >= maxPoints) return;
    const box = e.currentTarget.getBoundingClientRect();
    const x = Math.min(1, Math.max(0, (e.clientX - box.left) / (box.width || WIDTH)));
    const y = Math.min(1, Math.max(0, (e.clientY - box.top) / (box.height || HEIGHT)));
    onChange([...value, [Number(x.toFixed(4)), Number(y.toFixed(4))]]);
  };
  const path = value.map(([x, y]) => `${x * WIDTH},${y * HEIGHT}`).join(" ");
  return (
    <div>
      <svg
        width={WIDTH}
        height={HEIGHT}
        viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
        onClick={add}
        role="img"
        aria-label="Кадр камеры"
      >
        <image href={image} width={WIDTH} height={HEIGHT} preserveAspectRatio="none" />
        {grid.map(([a, b], n) => (
          <line key={n} x1={a[0] * WIDTH} y1={a[1] * HEIGHT} x2={b[0] * WIDTH} y2={b[1] * HEIGHT} stroke="var(--accent)" />
        ))}
        {mode === "polygon" && value.length > 2 && <polygon points={path} fill="none" stroke="var(--yellow)" />}
        {mode !== "points" && value.length > 1 && <polyline points={path} fill="none" stroke="var(--yellow)" />}
        {value.map(([x, y], n) => (
          <g key={n}>
            <circle cx={x * WIDTH} cy={y * HEIGHT} r={5} fill="var(--yellow)" />
            <text x={x * WIDTH + 8} y={y * HEIGHT - 8} fill="var(--text)">
              {n + 1}
            </text>
          </g>
        ))}
      </svg>
      <p>
        Точек: {value.length} из {maxPoints}{" "}
        <button type="button" onClick={() => onChange([])}>
          Сбросить точки
        </button>
      </p>
    </div>
  );
}
