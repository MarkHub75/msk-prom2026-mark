import { useState } from "react";
import { useParams } from "react-router-dom";
import { api, apiUrl, uploadVideo, videoUrl } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { useWs } from "../../api/ws";
import { useMeta } from "../../components/AppShell";
import { DataTable } from "../../components/DataTable";
import { EvidenceImage } from "../../components/EvidenceImage";
import { PolygonEditor } from "../../components/PolygonEditor";
import { Timeline } from "../../components/Timeline";
import { VideoWithHud } from "../../components/VideoWithHud";

type Analysis = components["schemas"]["Analysis"];
type Broadcast = components["schemas"]["Broadcast"];
type CameraSetupView = components["schemas"]["CameraSetupView"];
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

type Point = [number, number];
type Calibration = components["schemas"]["Calibration"];
type CameraRule = components["schemas"]["CameraRule"];
type Zone = components["schemas"]["Zone"];

function previewUrl(cameraId: number): string {
  return apiUrl(`/api/cameras/${cameraId}/preview`);
}

// Tab «Калибровка» (slice 9): 4–8 floor points by mouse, their meters, the 1 m grid.
function CalibrationPanel({ cameraId, calibration, onChange }: { cameraId: number; calibration: Calibration | null; onChange: () => void }) {
  const [points, setPoints] = useState<Point[]>((calibration?.image_points ?? []) as Point[]);
  const [world, setWorld] = useState<[string, string][]>(
    (calibration?.world_points ?? []).map(([x, y]) => [String(x), String(y)]),
  );
  const [error, setError] = useState<string>();
  const path = { params: { path: { camera_id: cameraId } } };
  const meters = (n: number, axis: 0 | 1, text: string) =>
    setWorld((rows) =>
      points.map((_, i) => {
        const [x, y] = rows[i] ?? ["", ""];
        if (i !== n) return [x, y];
        return axis === 0 ? [text, y] : [x, text];
      }),
    );
  const save = async () => {
    setError(undefined);
    const world_points = points.map((_, i): Point => {
      const [x, y] = world[i] ?? ["", ""];
      return [Number(x.replace(",", ".")), Number(y.replace(",", "."))];
    });
    const result = await api.PUT("/api/cameras/{camera_id}/calibration", { ...path, body: { image_points: points, world_points, control_points: [] } });
    if (result.error) setError(result.error.message);
    onChange();
  };
  const remove = async () => {
    setError(undefined);
    const result = await api.DELETE("/api/cameras/{camera_id}/calibration", path);
    if (result.error) setError(result.error.message);
    setPoints([]);
    onChange();
  };
  return (
    <>
      <h2>Калибровка</h2>
      <PolygonEditor image={previewUrl(cameraId)} mode="points" value={points} onChange={setPoints} maxPoints={8} grid={calibration?.grid ?? []} />
      {points.map((_, n) => (
        <p key={n}>
          Точка {n + 1}: X, м{" "}
          <input aria-label={`X точки ${n + 1}`} value={world[n]?.[0] ?? ""} onChange={(e) => meters(n, 0, e.target.value)} /> Y, м{" "}
          <input aria-label={`Y точки ${n + 1}`} value={world[n]?.[1] ?? ""} onChange={(e) => meters(n, 1, e.target.value)} />
        </p>
      ))}
      <button type="button" onClick={() => void save()}>
        Сохранить калибровку
      </button>{" "}
      <button type="button" disabled={!calibration} onClick={() => void remove()}>
        Удалить калибровку
      </button>
      {error && <p role="alert">{error}</p>}
      {calibration ? (
        <p>
          Ошибка подгонки {num(calibration.fit_rmse_m, 2)} м;{" "}
          {calibration.control_rmse_m === null
            ? "нет контрольных точек: точность не проверена"
            : `контрольные точки: ${num(calibration.control_rmse_m, 2)} м`}
        </p>
      ) : (
        <p>Калибровки нет: система работает в ростах человека</p>
      )}
    </>
  );
}

// Tab «Зоны» (slice 9): a polygon or a line by the geometry of the zone kind, the list, delete.
function ZonesPanel({ cameraId, zones, onChange }: { cameraId: number; zones: Zone[]; onChange: () => void }) {
  const kinds = useMeta()?.zone_kinds ?? [];
  const [kind, setKind] = useState<string>();
  const [name, setName] = useState("");
  const [points, setPoints] = useState<Point[]>([]);
  const [error, setError] = useState<string>();
  const current = kinds.find((k) => k.id === kind) ?? kinds[0];
  const line = current?.geometry === "line";
  const title = (id: string) => kinds.find((k) => k.id === id)?.title ?? id;
  const add = async () => {
    setError(undefined);
    const body = { kind: current?.id ?? "", name, points };
    const result = await api.POST("/api/cameras/{camera_id}/zones", { params: { path: { camera_id: cameraId } }, body });
    if (result.error) setError(result.error.message);
    else setPoints([]);
    onChange();
  };
  const remove = async (zoneId: number) => {
    setError(undefined);
    const result = await api.DELETE("/api/zones/{zone_id}", { params: { path: { zone_id: zoneId } } });
    if (result.error) setError(result.error.message);
    onChange();
  };
  return (
    <>
      <h2>Зоны</h2>
      <label>
        Тип зоны{" "}
        <select value={current?.id ?? ""} onChange={(e) => setKind(e.target.value)}>
          {kinds.map((k) => (
            <option key={k.id} value={k.id}>
              {k.title}
            </option>
          ))}
        </select>
      </label>{" "}
      <label>
        Название <input value={name} onChange={(e) => setName(e.target.value)} />
      </label>
      <PolygonEditor image={previewUrl(cameraId)} mode={line ? "line" : "polygon"} value={points} onChange={setPoints} maxPoints={line ? 2 : 32} />
      <button type="button" onClick={() => void add()}>
        Добавить зону
      </button>
      {error && <p role="alert">{error}</p>}
      <DataTable
        columns={[
          { title: "Название", cell: (z) => z.name },
          { title: "Тип", cell: (z) => title(z.kind) },
          { title: "Точек", cell: (z) => z.points.length },
          {
            title: "",
            cell: (z) => (
              <button type="button" onClick={() => void remove(z.id)}>
                Удалить
              </button>
            ),
          },
        ]}
        rows={zones}
        empty="Зон нет"
      />
    </>
  );
}

// Tab «Правила» (slice 9): scenario switches, parameters with units, «Пересчитать события».
function RulesPanel({ cameraId, rules, video, onChange }: { cameraId: number; rules: CameraRule[]; video?: Video; onChange: () => void }) {
  const scenarios = useMeta()?.scenarios ?? [];
  const [error, setError] = useState<string>();
  const put = async (rule: CameraRule, enabled: boolean, params: Record<string, number>) => {
    setError(undefined);
    const result = await api.PUT("/api/cameras/{camera_id}/rules/{scenario}", {
      params: { path: { camera_id: cameraId, scenario: rule.scenario } },
      body: { enabled, params },
    });
    if (result.error) setError(result.error.message);
    onChange();
  };
  const recompute = async () => {
    if (!video) return;
    setError(undefined);
    const result = await api.POST("/api/videos/{video_id}/recompute", { params: { path: { video_id: video.id } } });
    if (result.error) setError(result.error.message);
    onChange();
  };
  return (
    <>
      <h2>Правила</h2>
      {rules.map((rule) => {
        const meta = scenarios.find((s) => s.id === rule.scenario);
        return (
          <fieldset key={rule.scenario}>
            <legend>
              <label>
                <input type="checkbox" checked={rule.enabled} onChange={(e) => void put(rule, e.target.checked, rule.params)} />{" "}
                {meta?.title ?? rule.scenario}
              </label>
              {rule.status !== "active" && <span> {meta?.status_text}</span>}
            </legend>
            {(meta?.params ?? []).map((p) => (
              <label key={p.key}>
                {p.title}, {p.unit}{" "}
                <input
                  aria-label={p.title}
                  defaultValue={String(rule.effective[p.key] ?? p.default)}
                  onBlur={(e) => {
                    const value = Number(e.target.value.replace(",", "."));
                    if (value !== rule.effective[p.key]) void put(rule, rule.enabled, { ...rule.params, [p.key]: value });
                  }}
                />{" "}
              </label>
            ))}
          </fieldset>
        );
      })}
      <button type="button" disabled={!video} onClick={() => void recompute()}>
        Пересчитать события
      </button>
      {error && <p role="alert">{error}</p>}
    </>
  );
}

// The camera setup of tech.md 8.14: «Видео», «Эфир», «Калибровка», «Зоны», «Правила».
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
  // openapi-fetch widens the tuples of the schema (points, grid) to arrays; the server sends tuples.
  const setup = view.data as CameraSetupView;
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
      <CalibrationPanel cameraId={cameraId} calibration={setup.calibration} onChange={view.reload} />
      <ZonesPanel cameraId={cameraId} zones={setup.zones} onChange={view.reload} />
      <RulesPanel cameraId={cameraId} rules={view.data.rules} video={shown} onChange={view.reload} />
      <h2>Плеер</h2>
      {shown ? (
        <>
          <p>{shown.filename}</p>
          <VideoWithHud
            key={shown.id}
            videoId={shown.id}
            src={videoUrl(shown.id)}
            positionMs={seekMs}
            zones={setup.zones}
            grid={setup.calibration?.grid ?? []}
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
