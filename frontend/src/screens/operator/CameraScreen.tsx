import { useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import { api, videoUrl } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { useWs } from "../../api/ws";
import { STATE_ICON } from "../../components/SectorTile";
import { Timeline } from "../../components/Timeline";
import { VideoWithHud } from "../../components/VideoWithHud";

type Broadcast = components["schemas"]["Broadcast"];
type CameraLiveView = components["schemas"]["CameraLiveView"];

const DRIFT_S = 0.5; // tech.md 8.5: a larger gap to the server position is fixed by a seek

// Position of the broadcast now: the server clock at the answer plus the time since it came.
function position(b: Broadcast, received: number): number {
  const t = Date.parse(b.server_now) - Date.parse(b.started_at) + performance.now() - received;
  return (b.loop ? t % b.duration_ms : Math.min(t, b.duration_ms)) / 1000;
}

// /operator/cameras/:cameraId: the broadcast in sync with the server, HUD and the episode timeline.
export function CameraScreen() {
  const cameraId = Number(useParams().cameraId);
  const view = useApi(
    () => api.GET("/api/cameras/{camera_id}/view", { params: { path: { camera_id: cameraId } } }),
    [cameraId],
  );
  const box = useRef<HTMLDivElement>(null);
  useWs((message) => {
    if (message.type === "broadcast.state" && (message.data as Broadcast).camera_id === cameraId) view.reload();
  });
  // openapi-fetch widens the tuples of the schema (bbox, points) to arrays; the server sends tuples.
  const data = view.data as CameraLiveView | undefined;
  const broadcast = data?.broadcast;

  useEffect(() => {
    if (!broadcast || broadcast.status !== "playing") return;
    const received = performance.now();
    const timer = setInterval(() => {
      const player = box.current?.querySelector("video");
      if (!player) return;
      const want = position(broadcast, received);
      if (Math.abs(player.currentTime - want) > DRIFT_S) player.currentTime = want;
      if (player.paused) void player.play()?.catch(() => undefined);
    }, 1000);
    return () => clearInterval(timer);
  }, [broadcast]);

  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!data) return <p>Загрузка…</p>;
  const { camera, state, video, analysis } = data;
  return (
    <section>
      <h1>{camera.name}</h1>
      <p>
        {STATE_ICON[state.state]} {state.reason_text}
      </p>
      {video ? (
        <div ref={box}>
          <VideoWithHud
            key={video.id}
            videoId={video.id}
            src={videoUrl(video.id)}
            zones={data.zones}
            grid={data.calibration?.grid ?? []}
          />
        </div>
      ) : (
        <p>Нет видео: эфир не идёт</p>
      )}
      {analysis && <Timeline episodes={analysis.episodes} durationMs={analysis.duration_ms} onSeek={() => undefined} />}
    </section>
  );
}
