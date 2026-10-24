import { useState } from "react";
import { useParams } from "react-router-dom";
import { api, uploadVideo, videoUrl } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { useWs } from "../../api/ws";
import { DataTable } from "../../components/DataTable";
import { VideoWithHud } from "../../components/VideoWithHud";

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
      <h2>Плеер</h2>
      {shown ? (
        <>
          <p>{shown.filename}</p>
          <VideoWithHud key={shown.id} videoId={shown.id} src={videoUrl(shown.id)} zones={[]} grid={[]} />
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
