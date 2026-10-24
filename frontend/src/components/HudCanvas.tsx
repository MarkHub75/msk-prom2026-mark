import { useEffect, useRef } from "react";
import { LINE_H, PAD, type DrawOp, type Size } from "./hud";

// Draws the ops of `layoutHud`; all layout decisions stay in the pure function.
export function HudCanvas({ ops, size }: { ops: DrawOp[]; size: Size }) {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const ctx = ref.current?.getContext("2d");
    if (!ctx) return; // jsdom has no canvas
    ctx.clearRect(0, 0, size.width, size.height);
    ctx.lineWidth = 2;
    ctx.font = "12px sans-serif";
    ctx.textBaseline = "top";
    for (const op of ops) {
      ctx.strokeStyle = op.color;
      if (op.kind === "rect") {
        ctx.strokeRect(op.x, op.y, op.w, op.h);
      } else if (op.kind === "path") {
        ctx.beginPath();
        op.points.forEach(([x, y], n) => (n ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
        if (op.closed) ctx.closePath();
        ctx.stroke();
      } else {
        ctx.fillStyle = "rgba(11, 15, 20, 0.8)";
        ctx.fillRect(op.x, op.y, op.w, op.h);
        ctx.fillStyle = op.color;
        op.lines.forEach((line, n) => ctx.fillText(line, op.x + PAD, op.y + PAD + n * LINE_H));
      }
    }
  }, [ops, size]);

  return (
    <canvas
      ref={ref}
      width={size.width}
      height={size.height}
      aria-hidden="true"
      style={{ position: "absolute", left: 0, top: 0, pointerEvents: "none" }}
    />
  );
}
