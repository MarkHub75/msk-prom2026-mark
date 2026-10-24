import { useState } from "react";
import { api, apiError } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { useWs } from "../../api/ws";
import { DataTable } from "../../components/DataTable";
import { STATE_ICON } from "../../components/SectorTile";

type BackendStatus = components["schemas"]["BackendStatus"];
type Job = components["schemas"]["Job"];
type MetricRow = components["schemas"]["InferenceMetrics"] & { id: number; job: Job };

function num(x: number | null | undefined, digits = 1): string {
  return x === null || x === undefined ? "—" : x.toFixed(digits).replace(".", ",");
}

// /admin/system (tech.md 8.14): backend state, queue, measurements of recent jobs, models,
// freshness of the analysis per camera.
export function SystemScreen() {
  const view = useApi(() => api.GET("/api/system"), []);
  const [status, setStatus] = useState<BackendStatus>();
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState<string>();

  useWs((message) => {
    if (message.type === "backend.status") setStatus(message.data as BackendStatus);
    if (message.type === "job.progress") {
      const job = message.data as Job;
      if (job.status !== "running") view.reload();
    }
  });

  const check = async () => {
    setChecking(true);
    const result = await api.POST("/api/system/backend-check");
    setChecking(false);
    if (result.data) setStatus(result.data);
    else setError(apiError(result.error).message);
  };

  const retry = async (job: Job) => {
    setError(undefined);
    const result = await api.POST("/api/jobs/{job_id}/retry", { params: { path: { job_id: job.id } } });
    if (result.error) setError(apiError(result.error).message);
    view.reload();
  };

  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!view.data) return <p>Загрузка…</p>;
  const data = view.data;
  const backend = status ?? data.backend_status;
  const rows: MetricRow[] = data.recent_jobs.flatMap((job) =>
    job.metrics.length
      ? job.metrics.map((m, n) => ({ ...m, id: job.id * 10 + n, job }))
      : [{ ...EMPTY_METRICS, backend: job.backend, fake: job.fake, id: job.id * 10, job }],
  );
  const delay = data.latency.notify_delay_s;

  return (
    <section>
      <h1>Система</h1>
      <h2>Бэкенд инференса</h2>
      <p>
        {data.backend === "linq" ? "LinQ TPU" : "CPU (local), не LinQ"}
        {data.fake && <span className="badge"> фейк</span>}
      </p>
      <p data-testid="backend-state">
        {backend.state === "ok" ? "● " : "▲ "}
        {backend.message}
      </p>
      {backend.latency_ms !== null && <p>Отклик Jupyter: {num(backend.latency_ms, 0)} мс</p>}
      <button type="button" disabled={checking} onClick={() => void check()}>
        Проверить LinQ
      </button>
      {error && <p role="alert">{error}</p>}

      <h2>Очередь</h2>
      <DataTable
        columns={[
          { title: "Задача", cell: (j) => j.id },
          { title: "Видео", cell: (j) => j.video_id },
          { title: "Статус", cell: (j) => j.status },
          { title: "Стадия", cell: (j) => j.stage },
          { title: "Прогресс", cell: (j) => `${Math.round(j.progress * 100)} %` },
        ]}
        rows={data.queue}
        empty="Очередь пуста"
      />

      <h2>Последние задачи и замеры</h2>
      <DataTable
        columns={[
          { title: "Задача", cell: (m) => m.job.id },
          { title: "Статус", cell: (m) => m.job.status },
          { title: "Модель", cell: (m) => (m.model_id ? `${m.model_id}@${m.model_version}` : "—") },
          { title: "Бэкенд", cell: (m) => `${m.backend === "local" ? "CPU, не LinQ" : "LinQ"}${m.fake ? " (фейк)" : ""}` },
          { title: "Кадров", cell: (m) => m.frames_processed },
          { title: "Кадр/с", cell: (m) => num(m.throughput_fps) },
          { title: "Пре, мс/кадр", cell: (m) => num(m.preprocess_ms) },
          { title: "Пост, мс/кадр", cell: (m) => num(m.postprocess_ms) },
          { title: "RTT p50/p90, мс", cell: (m) => `${num(m.tpu_rtt_p50_ms, 0)} / ${num(m.tpu_rtt_p90_ms, 0)}` },
          { title: "Загрузка, с", cell: (m) => num(m.upload_s) },
          { title: "Всего, с", cell: (m) => num(m.total_s) },
          {
            title: "Ошибка",
            cell: (m) =>
              m.job.status === "failed" ? (
                <>
                  {m.job.error_text}{" "}
                  <button type="button" onClick={() => void retry(m.job)}>
                    Повторить
                  </button>
                </>
              ) : (
                (m.job.error_text ?? "")
              ),
          },
        ]}
        rows={rows}
        empty="Завершённых задач нет"
      />

      <h2>Модели</h2>
      <DataTable
        columns={[
          { title: "Модель", cell: ({ spec }) => `${spec.id}@${spec.version}` },
          { title: "Программа", cell: ({ spec }) => spec.linq_program ?? "—" },
          { title: "Хвост", cell: ({ spec }) => spec.linq_tail ?? "—" },
        ]}
        rows={data.models.map((spec, n) => ({ id: n, spec }))}
        empty="Активных моделей нет"
      />

      <h2>Свежесть анализа по камерам</h2>
      <DataTable
        columns={[
          { title: "Камера", cell: (c) => c.camera_id },
          { title: "Состояние", cell: (c) => `${STATE_ICON[c.state]} ${c.reason_text}` },
          { title: "Свежесть, с", cell: (c) => num(c.freshness_ms === null ? null : c.freshness_ms / 1000) },
        ]}
        rows={data.cameras.map((c) => ({ ...c, id: c.camera_id }))}
        empty="Камер нет"
      />

      <h2>Задержка уведомлений</h2>
      <p>
        p50 {num(delay.p50)} с, p95 {num(delay.p95)} с, n = {delay.n}
      </p>
    </section>
  );
}

// A failed job may have no measurements: its row still shows the error and «Повторить».
const EMPTY_METRICS: components["schemas"]["InferenceMetrics"] = {
  backend: "linq",
  fake: false,
  model_id: "",
  model_version: "",
  task: "detect",
  input_size: 0,
  step: 1,
  frames_processed: 0,
  wall_s: 0,
  throughput_fps: 0,
  preprocess_ms: null,
  postprocess_ms: null,
  tpu_rtt_p50_ms: null,
  tpu_rtt_p90_ms: null,
  upload_s: null,
  total_s: 0,
  cached: false,
};
