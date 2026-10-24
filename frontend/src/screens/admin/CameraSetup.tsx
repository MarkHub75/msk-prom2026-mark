import { useState } from "react";
import { useParams } from "react-router-dom";
import { api, uploadVideo, videoUrl } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { useWs } from "../../api/ws";
import { DataTable } from "../../components/DataTable";
import { EvidenceImage } from "../../components/EvidenceImage";
import { Timeline } from "../../components/Timeline";
import { VideoWithHud } from "../../components/VideoWithHud";

type Analysis = components["schemas"]["Analysis"];
type Broadcast = components["schemas"]["Broadcast"];
type Job = components["schemas"]["Job"];
type Video = components["schemas"]["Video"];
type Metrics = components["schemas"]["InferenceMetrics"] & { id: number };

const VIDEO_STATUS: Record<Video["status"], string> = {
  uploaded: "в очереди",
  processing: "обрабатывается",
  ready: "готово",
  failed: "ошибка",
};

function percent(share: number): string {
  return `${Math.round(share * 100)} %`;
}

function num(x: number | null | undefined, digits = 1): string {
  return x === null || x === undefined ? "—" : x.toFixed(digits).replace(".", ",");
}

// Episodes of the active analysis: timeline, evidence thumbnails, «Пересчитать события».
function Episodes({ video, onSeek, onRecompute }: { video: Video; onSeek: (ms: number) => void; onRecompute: () => void }) {
  const analysis = useApi(
    () => api.GET("/api/videos/{video_id}/analysis", { params: { path: { video_id: video.id } } }),
    [video.id, video.active_analysis_id],
  );
  // openapi-fetch widens the tuples of the schema (bbox, kpts) to arrays; the server sends tuples.
  const data = analysis.data as Analysis | undefined;
  const [error, setError] = useState<string>();
  const recompute = async () => {
    setError(undefined);
    const result = await api.POST("/api/videos/{video_id}/recompute", { params: { path: { video_id: video.id } } });
    if (result.error) setError(result.error.message);
    onRecompute();
  };
  return (
    <>
      <h2>Эпизоды</h2>
      <button type="button" onClick={() => void recompute()}>
        Пересчитать события
      </button>
      {error && <p role="alert">{error}</p>}
      {analysis.error && <p role="alert">{analysis.error.message}</p>}
      {data && (
        <>
          <p>Версия анализа {data.version}</p>
          <Timeline episodes={data.episodes} durationMs={data.duration_ms} onSeek={onSeek} />
          <div>
            {data.episodes.flatMap((e) =>
              e.evidence.map((ev) => <EvidenceImage key={ev.id} evidence={ev} hudVisible />),
            )}
          </div>
        </>
      )}
    </>
  );
}

const BROADCAST_STATUS: Record<Broadcast["status"], string> = {
  playing: "идёт",
  stopped: "остановлен",
  ended: "запись закончилась",
};

// Tab «Эфир» (slice 6): start the latest ready video, stop, repeat in a loop.
function BroadcastPanel({ cameraId, broadcast, onChange }: { cameraId: number; broadcast: Broadcast | null; onChange: () => void }) {
  const [loop, setLoop] = useState(true);
  const [error, setError] = useState<string>();
  const path = { params: { path: { camera_id: cameraId } } };
  const start = async () => {
    setError(undefined);
    const result = await api.POST("/api/cameras/{camera_id}/broadcast", { ...path, body: { loop } });
    if (result.error) setError(result.error.message);
    onChange();
  };
  const stop = async () => {
    setError(undefined);
    const result = await api.DELETE("/api/cameras/{camera_id}/broadcast", path);
    if (result.error) setError(result.error.message);
    onChange();
  };
  return (
    <>
      <h2>Эфир</h2>
      <p>
        {broadcast
          ? `Эфир ${BROADCAST_STATUS[broadcast.status]}, цикл ${broadcast.cycle + 1}, повтор: ${broadcast.loop ? "да" : "нет"}`
          : "Эфира нет"}
      </p>
      <label>
        <input type="checkbox" checked={loop} onChange={(e) => setLoop(e.target.checked)} /> Повтор по кругу
      </label>{" "}
      <button type="button" onClick={() => void start()}>
        Запустить эфир
      </button>{" "}
      <button type="button" disabled={broadcast?.status !== "playing"} onClick={() => void stop()}>
        Остановить эфир
      </button>
      {error && <p role="alert">{error}</p>}
    </>
  );
}

// Tab «Видео» of the camera setup (tech.md 8.14); calibration, zones and rules come with slice 9,
// so the player gets no zones and no grid yet.
export function CameraSetup() {
  const cameraId = Number(useParams().cameraId);
  const view = useApi(
    () => api.GET("/api/admin/cameras/{camera_id}", { params: { path: { camera_id: cameraId } } }),
    [cameraId],
  );
  const [live, setLive] = useState<Record<number, Job>>({});
  const [upload, setUpload] = useState<number>();
  const [error, setError] = useState<string>();
  const [watch, setWatch] = useState<number>();
  const [seekMs, setSeekMs] = useState<number>();

  useWs((message) => {
    if (message.type !== "job.progress") return;
    const job = message.data as Job;
    if (job.camera_id !== cameraId) return;
    setLive((jobs) => ({ ...jobs, [job.id]: job }));
    if (job.status === "done" || job.status === "failed") view.reload();
  });

  const send = async (file: File) => {
    setError(undefined);
    setUpload(0);
    const result = await uploadVideo(cameraId, file, setUpload);
    setUpload(undefined);
    if (result.error) setError(result.error.message);
    view.reload();
  };

  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!view.data) return <p>Загрузка…</p>;
  const jobs = view.data.jobs.map((j) => live[j.id] ?? j);
  const lastJob = (video: Video) => jobs.find((j) => j.video_id === video.id);
  const analyzed = view.data.videos.filter((v) => v.active_analysis_id !== null);
  const shown = analyzed.find((v) => v.id === watch) ?? analyzed[0];
  const metrics: Metrics[] = jobs
    .filter((j) => j.status === "done")
    .flatMap((j) => j.metrics.map((m, n) => ({ ...m, id: j.id * 10 + n })));

  return (
    <section>
      <h1>{view.data.camera.name}</h1>
      <h2>Видео</h2>
      <label>
        Загрузить видео{" "}
        <input
          type="file"
          accept="video/*"
          disabled={upload !== undefined}
          onChange={(e) => e.target.files?.[0] && void send(e.target.files[0])}
        />
      </label>
      {upload !== undefined && <progress value={upload} max={1} aria-label="Загрузка файла" />}
      {error && <p role="alert">{error}</p>}
      <DataTable
        columns={[
          { title: "Файл", cell: (v) => v.filename },
          { title: "Статус", cell: (v) => VIDEO_STATUS[v.status] },
          { title: "Длительность, с", cell: (v) => num(v.duration_ms / 1000) },
          {
            title: "Обработка",
            cell: (v) => {
              const job = lastJob(v);
              if (!job) return "—";
              return (
                <>
                  <progress value={job.progress} max={1} /> {percent(job.progress)}
                  {job.fake && <span className="badge"> фейк</span>}
                  {job.error_text && <div>{job.error_text}</div>}
                </>
              );
            },
          },
          {
            title: "Плеер",
            cell: (v) =>
              v.active_analysis_id === null ? (
                "—"
              ) : (
                <button type="button" onClick={() => setWatch(v.id)}>
                  Смотреть с HUD
                </button>
              ),
          },
          {
            title: "Кодек",
            cell: (v) =>
              v.browser_playable ? (
                v.codec
              ) : (
                <span>Браузер может не воспроизвести кодек {v.codec}: нужен H.264</span>
              ),
          },
        ]}
        rows={view.data.videos}
        empty="Видео ещё нет"
      />
      <BroadcastPanel cameraId={cameraId} broadcast={view.data.broadcast} onChange={view.reload} />
      <h2>Плеер</h2>
      {shown ? (
        <>
          <p>{shown.filename}</p>
          <VideoWithHud
            key={shown.id}
            videoId={shown.id}
            src={videoUrl(shown.id)}
            positionMs={seekMs}
            zones={[]}
            grid={[]}
          />
          <Episodes video={shown} onSeek={setSeekMs} onRecompute={view.reload} />
        </>
      ) : (
        <p>Нет видео с готовым анализом</p>
      )}
      <h2>Замеры</h2>
      <DataTable
        columns={[
          { title: "Модель", cell: (m) => `${m.model_id}@${m.model_version}` },
          { title: "Бэкенд", cell: (m) => `${m.backend}${m.fake ? " (фейк)" : ""}` },
          { title: "Кадров", cell: (m) => m.frames_processed },
          { title: "Кадр/с", cell: (m) => num(m.throughput_fps) },
          { title: "RTT p50/p90, мс", cell: (m) => `${num(m.tpu_rtt_p50_ms, 0)} / ${num(m.tpu_rtt_p90_ms, 0)}` },
          { title: "Всего, с", cell: (m) => num(m.total_s) },
          { title: "Кэш", cell: (m) => (m.cached ? "да" : "нет") },
        ]}
        rows={metrics}
        empty="Замеров ещё нет"
      />
    </section>
  );
}
