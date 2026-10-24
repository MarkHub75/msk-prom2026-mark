import { useEffect, useRef, useState, type DragEvent } from "react";
import { useLevelTitle } from "../../components/ops/levels";
import { CircleCheck, CircleX, Clock, Film, LoaderCircle, Octagon, RefreshCw, RotateCw, TriangleAlert, Upload, X } from "lucide-react";
import { api, apiError, type ApiFailure } from "../../api/client";
import type { Analysis, Camera, Episode, Job, Video } from "../../api/types";
import { uploadVideo, type UploadProgress } from "../../api/upload";
import { useApi, type ApiState } from "../../api/useApi";
import { VideoWithHud } from "../../components/Media";
import { duration, Empty, ErrorNotice, time } from "../../components/ui";
import { Bar, bytes, fmt } from "../../components/admin/AdminUi";
import { plural } from "./ZonesTab";

const I = { size: 15, strokeWidth: 1.75 } as const;

const VIDEO_STATUS: Record<Video["status"], string> = { uploaded: "В очереди", processing: "Обрабатывается", ready: "Готово", failed: "Ошибка" };
const JOB_STATUS: Record<Job["status"], string> = { queued: "В очереди", running: "Идёт", retry_wait: "Ждёт повтора", done: "Готово", failed: "Ошибка" };
const STAGE: Record<Job["stage"], string> = { queued: "ожидает воркер", inference_detect: "детекция объектов", inference_pose: "поза людей", analysis: "анализ сценариев", evidence: "кадры доказательств", done: "завершена" };
const TASK: Record<string, string> = { detect: "Детекция", pose: "Поза" };

function JobIcon({ status }: { status: Job["status"] }) {
  if (status === "done") return <CircleCheck {...I} />;
  if (status === "failed") return <CircleX {...I} />;
  if (status === "retry_wait") return <Clock {...I} />;
  if (status === "running") return <LoaderCircle {...I} className="adm-spin" />;
  return <Clock {...I} />;
}

function Uploader({ camera, onJob, onChange }: { camera: Camera; onJob: (job: Job) => void; onChange: () => void }) {
  const [progress, setProgress] = useState<UploadProgress & { name: string }>();
  const [error, setError] = useState<ApiFailure>();
  const [note, setNote] = useState<string>();
  const [over, setOver] = useState(false);
  const abort = useRef<() => void>();
  const input = useRef<HTMLInputElement>(null);
  const send = async (file: File) => {
    setError(undefined); setNote(undefined);
    setProgress({ loaded: 0, total: file.size, name: file.name });
    const call = uploadVideo(camera.id, file, (p) => setProgress({ ...p, name: file.name }));
    abort.current = call.abort;
    const result = await call.done;
    abort.current = undefined;
    setProgress(undefined);
    if (input.current) input.current.value = "";
    if (result.error) { setError(result.error); return; }
    const data = result.data!;
    if (data.job) onJob(data.job);
    setNote(data.reused ? `«${data.video.filename}» уже загружен: использована прежняя запись и её анализ.` : `«${data.video.filename}» загружен, ${duration(data.video.duration_ms)}, ${data.video.width}×${data.video.height}. Задача анализа поставлена в очередь.`);
    onChange();
  };
  const drop = (e: DragEvent) => { e.preventDefault(); setOver(false); const file = e.dataTransfer.files[0]; if (file && !progress) void send(file); };
  return <section className="adm-panel" data-panel="Загрузка записи">
    <div className={`adm-drop ${over ? "over" : ""} ${progress ? "busy" : ""}`} onDragOver={(e) => { e.preventDefault(); setOver(true); }} onDragLeave={() => setOver(false)} onDrop={drop}>
      {progress ? <div className="adm-upload">
        <div className="adm-upload-line"><Film {...I} /><b>{progress.name}</b><span>{bytes(progress.loaded)} из {bytes(progress.total)}</span><span className="adm-tc">{Math.round(progress.loaded / Math.max(1, progress.total) * 100)} %</span></div>
        <Bar value={progress.loaded / Math.max(1, progress.total)} label="Загрузка файла" />
        <button type="button" className="button button-small" onClick={() => abort.current?.()}><X {...I} />Отменить</button>
      </div> : <>
        <Upload size={22} strokeWidth={1.5} />
        <p><b>Перетащите видеофайл сюда</b> или выберите на диске</p>
        <label className="button button-primary adm-file"><input ref={input} type="file" accept="video/*,.mp4,.mov,.mkv,.avi" aria-label="Видеофайл для загрузки" onChange={(e) => { const f = e.target.files?.[0]; if (f) void send(f); }} />Выбрать файл</label>
        <small>После загрузки сервер сам ставит задачу анализа. Для плеера в браузере нужен H.264.</small>
      </>}
    </div>
    {error && <div className="adm-pad"><ErrorNotice error={error} compact /></div>}
    {note && <p className="adm-note" role="status"><CircleCheck {...I} />{note}</p>}
  </section>;
}

function Metrics({ job }: { job: Job }) {
  if (!job.metrics.length) return <p className="adm-muted adm-metrics-none">{job.status === "done" ? "Сервер не прислал замеров для этой задачи." : "Замеры появятся, когда закончится инференс."}</p>;
  return <div className="adm-metrics">{job.metrics.map((m, i) => <div key={i} className="adm-metric">
    <div className="adm-metric-head"><b>{TASK[m.task] ?? m.task}</b><code className="adm-ellipsis" title={`${m.model_id}@${m.model_version}`}>{m.model_id}@{m.model_version}</code><span className="adm-muted">{m.input_size}px · шаг {m.step}</span>{m.cached && <i className="adm-tag" title="Результат взят из кэша">кэш</i>}</div>
    <dl>
      <div><dt>кадров</dt><dd>{m.frames_processed}</dd></div>
      <div><dt>кадр/с</dt><dd>{fmt(m.throughput_fps)}</dd></div>
      <div><dt title="мс на кадр: предобработка / постобработка">пре / пост, мс</dt><dd>{fmt(m.preprocess_ms)} / {fmt(m.postprocess_ms)}</dd></div>
      <div><dt title="Время ответа TPU: медиана / 90-й перцентиль">RTT p50 / p90, мс</dt><dd>{fmt(m.tpu_rtt_p50_ms, 0)} / {fmt(m.tpu_rtt_p90_ms, 0)}</dd></div>
      <div><dt>загрузка, с</dt><dd>{fmt(m.upload_s, 2)}</dd></div>
      <div><dt>всего, с</dt><dd>{fmt(m.total_s, 2)}</dd></div>
    </dl>
  </div>)}</div>;
}

function JobCard({ job, video, onJob, onChange }: { job: Job; video?: Video; onJob: (job: Job) => void; onChange: () => void }) {
  const [error, setError] = useState<ApiFailure>();
  const [busy, setBusy] = useState(false);
  const retry = async () => {
    setBusy(true); setError(undefined);
    const result = await api.POST("/api/jobs/{job_id}/retry", { params: { path: { job_id: job.id } } });
    setBusy(false);
    if (result.error !== undefined) { setError(apiError(result.error)); return; }
    onJob(result.data); onChange();
  };
  const tone = job.status === "failed" ? "red" : job.status === "done" ? "ok" : "accent";
  return <article className={`adm-job adm-job-${job.status}`} aria-label={`Задача ${job.id}`}>
    <header>
      <span className={`adm-job-status adm-job-status-${job.status}`}><JobIcon status={job.status} />{JOB_STATUS[job.status]}</span>
      <b>#{job.id} · {job.kind === "recompute" ? "Пересчёт событий" : "Анализ записи"}</b>
      <span className="adm-muted adm-ellipsis">{video?.filename ?? `видео ${job.video_id}`}</span>
      <span className="adm-tag">{job.backend === "linq" ? "LinQ" : "локально"}{job.fake ? " · фейк" : ""}</span>
    </header>
    <div className="adm-job-progress"><Bar value={job.progress} tone={tone} label={`Прогресс задачи ${job.id}`} /><span className="adm-tc">{Math.round(job.progress * 100)} %</span><span className="adm-muted">{STAGE[job.stage]}</span></div>
    <div className="adm-job-times adm-muted">
      <span>создана {time(job.created_at)}</span>{job.started_at && <span>старт {time(job.started_at)}</span>}{job.finished_at && <span>конец {time(job.finished_at)}</span>}
      {job.analysis_ms !== null && <span>анализ {fmt(job.analysis_ms / 1000)} с</span>}<span>попыток {job.attempts}</span>
      {job.next_attempt_at && <span>повтор в {time(job.next_attempt_at)}</span>}
    </div>
    {job.error_text && <p className="adm-job-error" role="alert"><TriangleAlert {...I} /><span><b>{job.error_code ?? "ошибка"}</b> {job.error_text}</span></p>}
    {job.status === "failed" && <button type="button" className="button button-small" onClick={() => void retry()} disabled={busy}><RotateCw {...I} />{busy ? "Ставим в очередь…" : "Повторить задачу"}</button>}
    {error && <ErrorNotice error={error} compact />}
    <Metrics job={job} />
  </article>;
}

function EpisodeTimeline({ episodes, durationMs, onSeek }: { episodes: Episode[]; durationMs: number; onSeek: (ms: number) => void }) {
  const lanes = [...new Map(episodes.map((e) => [e.scenario, e.scenario_title])).entries()];
  const ticks = [0, .25, .5, .75, 1];
  return <div className="adm-tl" aria-label="Таймлайн эпизодов">
    <div className="adm-tl-ruler"><span />{<div>{ticks.map((t) => <i key={t} style={{ left: `${t * 100}%` }}>{duration(durationMs * t)}</i>)}</div>}</div>
    {lanes.map(([id, title]) => <div key={id} className="adm-tl-lane">
      <span className="adm-tl-name" title={title}>{title}</span>
      <div className="adm-tl-track">{episodes.filter((e) => e.scenario === id).map((e) => <button key={e.id} type="button" className={`adm-tl-clip adm-tl-${e.level_max}`} style={{ left: `${e.start_ms / Math.max(1, durationMs) * 100}%`, width: `${Math.max(.8, (e.end_ms - e.start_ms) / Math.max(1, durationMs) * 100)}%` }} onClick={() => onSeek(e.confirm_ms)} aria-label={`${title}, ${e.level_max === "red" ? "красный" : "жёлтый"}, ${duration(e.start_ms)}`} title={e.reason_text} />)}</div>
    </div>)}
  </div>;
}

function Episodes({ video, analysis, onSeek, onJob, onChange }: { video: Video; analysis: ApiState<Analysis>; onSeek: (ms: number) => void; onJob: (job: Job) => void; onChange: () => void }) {
  const levelTitle = useLevelTitle();
  const [error, setError] = useState<ApiFailure>();
  const [busy, setBusy] = useState(false);
  const recompute = async () => {
    setBusy(true); setError(undefined);
    const result = await api.POST("/api/videos/{video_id}/recompute", { params: { path: { video_id: video.id } } });
    setBusy(false);
    if (result.error !== undefined) { setError(apiError(result.error)); return; }
    onJob(result.data); onChange();
  };
  const data = analysis.data;
  return <section className="adm-panel adm-episodes" data-panel={data ? `Эпизоды · анализ v${data.version}` : "Эпизоды"}>
    <div className="adm-panel-bar">
      <span className="adm-muted">{data ? `${data.episodes.length} ${plural(data.episodes.length, "эпизод", "эпизода", "эпизодов")} · ${data.pose_used ? "с позой" : "без позы"} · ${time(data.created_at)}` : "Таймлайн по активному анализу"}</span>
      <button type="button" className="button button-small" onClick={() => void recompute()} disabled={busy} title="Заново пройти правила по сохранённым трекам, без инференса"><RefreshCw {...I} />{busy ? "Ставим задачу…" : "Пересчитать события"}</button>
    </div>
    {error && <div className="adm-pad"><ErrorNotice error={error} compact /></div>}
    {analysis.error ? <div className="adm-pad"><ErrorNotice error={analysis.error} compact retry={analysis.reload} /></div>
      : !data ? <p className="adm-muted adm-pad">Загружаем анализ…</p>
      : !data.episodes.length ? <p className="adm-muted adm-pad">В этой записи правила не нашли эпизодов. Это не значит, что всё безопасно: проверьте зоны и калибровку.</p>
      : <>
        <EpisodeTimeline episodes={data.episodes} durationMs={data.duration_ms} onSeek={onSeek} />
        <ol className="adm-ep-list">{data.episodes.map((e) => <li key={e.id}><button type="button" onClick={() => onSeek(e.confirm_ms)}>
          <span className={`adm-lvl adm-lvl-${e.level_max}`}>{e.level_max === "red" ? <Octagon size={13} strokeWidth={1.75} /> : <TriangleAlert size={13} strokeWidth={1.75} />}{levelTitle(e.level_max)}</span>
          <b>{e.scenario_title}</b>
          <span className="adm-tc">{duration(e.start_ms)}–{duration(e.end_ms)}</span>
          <span className="adm-muted adm-ellipsis">{e.reason_text}</span>
          <span className="adm-muted">{Math.round(e.confidence * 100)} %</span>
        </button></li>)}</ol>
        {data.gaps.length > 0 && <p className="adm-muted adm-pad">Без наблюдения: {data.gaps.length} интервал(ов) в записи.</p>}
      </>}
  </section>;
}

export function VideoTab({ camera, videos, jobs, onJob, onChange }: { camera: Camera; videos: Video[]; jobs: Job[]; onJob: (job: Job) => void; onChange: () => void }) {
  const [picked, setPicked] = useState<number>();
  const [seek, setSeek] = useState(0);
  const sorted = [...videos].sort((a, b) => b.id - a.id);
  const video = sorted.find((v) => v.id === picked) ?? sorted.find((v) => v.active_analysis_id !== null) ?? sorted[0];
  useEffect(() => setSeek(0), [video?.id]);
  const analysis = useApi<Analysis>(() => video?.active_analysis_id ? api.GET("/api/videos/{video_id}/analysis", { params: { path: { video_id: video.id } } }) : Promise.resolve({ data: undefined }), [video?.id, video?.active_analysis_id]);
  const ordered = [...jobs].sort((a, b) => Date.parse(b.created_at) - Date.parse(a.created_at));
  const lastJob = (v: Video) => ordered.find((j) => j.video_id === v.id);

  return <div className="adm-video">
    <div className="adm-video-main">
      <section className="adm-panel adm-player" data-panel={video ? `Просмотр с HUD · ${video.filename}` : "Просмотр с HUD"}>
        {!video ? <Empty title="Записей ещё нет" text="Загрузите видео справа: сервер проанализирует его, и здесь появится плеер с рамками объектов." />
          : video.active_analysis_id === null ? <Empty title={video.status === "failed" ? "Анализ записи не удался" : "Анализ ещё не готов"} text={video.status === "failed" ? "Ошибка задачи показана справа. Повторите задачу, когда причина устранена." : "Плеер с HUD откроется, когда задача анализа закончится."}>
            {(() => { const job = lastJob(video); return job && job.status !== "done" && job.status !== "failed" ? <div className="adm-wait"><Bar value={job.progress} label="Прогресс анализа" /><span><span className="adm-tc">{Math.round(job.progress * 100)} %</span> · {STAGE[job.stage]}</span></div> : null; })()}
          </Empty>
          : <VideoWithHud key={video.id} video={video} camera={camera.name} initialMs={seek} episodes={analysis.data?.episodes ?? []} />}
      </section>
      {video?.active_analysis_id != null && <Episodes video={video} analysis={analysis} onSeek={setSeek} onJob={onJob} onChange={onChange} />}
    </div>
    <div className="adm-video-side">
      <Uploader camera={camera} onJob={onJob} onChange={onChange} />
      <section className="adm-panel" data-panel={`Записи камеры · ${videos.length}`}>
        {!sorted.length ? <p className="adm-muted adm-pad">Записей нет.</p> : <ul className="adm-videos">{sorted.map((v) => {
          const job = lastJob(v);
          return <li key={v.id}><button type="button" className={v.id === video?.id ? "selected" : ""} onClick={() => setPicked(v.id)} aria-pressed={v.id === video?.id}>
            <Film {...I} />
            <span className="adm-v-name"><b className="adm-ellipsis">{v.filename}</b><small>{duration(v.duration_ms)} · {v.width}×{v.height} · {fmt(v.fps, 0)} к/с · {v.codec} · {bytes(v.size_bytes)}</small>{!v.browser_playable && <small className="adm-warn">Браузер не воспроизведёт {v.codec}: нужен H.264</small>}</span>
            <span className={`adm-v-status adm-v-${v.status}`}>{VIDEO_STATUS[v.status]}{job && job.status !== "done" && job.status !== "failed" ? ` · ${Math.round(job.progress * 100)} %` : ""}</span>
          </button></li>;
        })}</ul>}
      </section>
      <section className="adm-panel adm-jobs" data-panel={`Задачи и замеры · ${jobs.length}`}>
        {!ordered.length ? <p className="adm-muted adm-pad">Задач ещё не было. Задача появится после загрузки записи.</p> : ordered.map((j) => <JobCard key={j.id} job={j} video={videos.find((v) => v.id === j.video_id)} onJob={onJob} onChange={onChange} />)}
      </section>
    </div>
  </div>;
}
