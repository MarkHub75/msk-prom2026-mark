import { useEffect, useRef, useState } from "react";
import { api } from "../api/client";
import type { components } from "../api/schema";
import { HudCanvas } from "./HudCanvas";
import { layoutHud, type Size } from "./hud";

type HudFrame = components["schemas"]["HudFrame"];
type Zone = components["schemas"]["Zone"];
type Segment = components["schemas"]["Calibration"]["grid"][number];

const CHUNK_MS = 5000; // one /tracks window; the server allows up to hud.window_max_ms
const WIDTH = 640;

interface Props {
  videoId: number;
  src: string;
  positionMs?: number;
  zones: Zone[];
  grid: Segment[];
}

export function VideoWithHud({ videoId, src, positionMs, zones, grid }: Props) {
  const video = useRef<HTMLVideoElement>(null);
  const [visible, setVisible] = useState(true);
  const [timeMs, setTimeMs] = useState(0);
  const [size, setSize] = useState<Size>({ width: WIDTH, height: 360 });
  const [frames, setFrames] = useState<HudFrame[]>([]);
  const chunk = Math.floor(timeMs / CHUNK_MS) * CHUNK_MS;

  useEffect(() => {
    let alive = true;
    void api
      .GET("/api/videos/{video_id}/tracks", {
        params: { path: { video_id: videoId }, query: { from_ms: chunk, to_ms: chunk + CHUNK_MS } },
      })
      // openapi-fetch widens the tuples of the schema (bbox, kpts) to arrays; the server sends tuples.
      .then((result) => alive && setFrames((result.data?.frames ?? []) as HudFrame[]));
    return () => {
      alive = false;
    };
  }, [videoId, chunk]);

  useEffect(() => {
    if (positionMs !== undefined && video.current) video.current.currentTime = positionMs / 1000;
  }, [positionMs]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "h" || e.key === "H" || e.key === "р" || e.key === "Р") setVisible((v) => !v);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  // timeupdate fires about 4 times a second: too coarse for a box on a running person.
  useEffect(() => {
    if (typeof requestAnimationFrame !== "function") return;
    let id = 0;
    const tick = () => {
      if (video.current) setTimeMs(video.current.currentTime * 1000);
      id = requestAnimationFrame(tick);
    };
    id = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(id);
  }, []);

  const frame = frames.filter((f) => f.ts_ms <= timeMs).at(-1) ?? null;
  const ops = layoutHud(frame, zones, grid, size, visible);

  return (
    <div>
      <div style={{ position: "relative", display: "inline-block" }}>
        <video
          ref={video}
          src={src}
          controls
          width={size.width}
          height={size.height}
          onTimeUpdate={(e) => setTimeMs(e.currentTarget.currentTime * 1000)}
          onLoadedMetadata={(e) => {
            const v = e.currentTarget;
            if (v.videoWidth) setSize({ width: WIDTH, height: Math.round((WIDTH * v.videoHeight) / v.videoWidth) });
          }}
        />
        <HudCanvas ops={ops} size={size} />
      </div>
      <div>
        <button type="button" onClick={() => setVisible((v) => !v)}>
          {visible ? "Скрыть HUD" : "Показать HUD"}
        </button>{" "}
        клавиша H
      </div>
    </div>
  );
}
