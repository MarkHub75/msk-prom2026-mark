import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { Link } from "react-router-dom";
import {
  AlertTriangle, Ban, Bell, Check, CircleCheck, CircleDashed, CircleHelp, CircleX, Cpu, Eye, EyeOff, Hourglass,
  LoaderCircle, Radio, RefreshCw, RotateCcw, Server, Square, Webhook, Wifi, WifiOff, X, type LucideIcon,
} from "lucide-react";
import { api, apiError, type ApiFailure } from "../api/client";
import type { BackendStatus, Job, Schemas } from "../api/types";
import { useApi } from "../api/useApi";
import { useWs } from "../api/ws";
import { ErrorNotice, Loading, PageHeading, time } from "../components/ui";

type Metrics = Schemas["InferenceMetrics"];
type ModelSpec = Schemas["ModelSpec"];
type CameraState = Schemas["CameraState"];
type Percentiles = Schemas["Percentiles"];
type BackendState = BackendStatus["state"];
type Tone = "ok" | "warn" | "bad" | "idle" | "info";

// /admin/system (tech.md 8.14, 6.10, 8.10): inference backend and its check, queue and measured jobs,
// models, notification delay, analysis freshness per camera, delivery channels; live over WS.
const SW = 1.75;
const nf = (digits: number) => new Intl.NumberFormat("ru-RU", { maximumFractionDigits: digits, minimumFractionDigits: 0 });
export function num(x: number | null | undefined, digits = 1): string { return x === null || x === undefined || !Number.isFinite(x) ? "—" : nf(digits).format(x); }
const ago = (iso: string | null | undefined, now: number) => {
  if (!iso) return "";
  const s = Math.max(0, Math.round((now - Date.parse(iso)) / 1000));
  return s < 60 ? `${s} с назад` : s < 3600 ? `${Math.floor(s / 60)} мин назад` : `${Math.floor(s / 3600)} ч назад`;
};

export const BACKEND_STATE: Record<BackendState, { label: string; tone: Tone; icon: LucideIcon }> = {
  ok: { label: "Отвечает", tone: "ok", icon: CircleCheck },
  models_missing: { label: "Нет программ моделей", tone: "bad", icon: AlertTriangle },
  unreachable: { label: "Не отвечает", tone: "bad", icon: CircleX },
  bad_answer: { label: "Неверный ответ", tone: "bad", icon: AlertTriangle },
  unchecked: { label: "Не проверено", tone: "idle", icon: CircleHelp },
};
const JOB_STATUS: Record<Job["status"], { label: string; tone: Tone; icon: LucideIcon }> = {
  queued: { label: "В очереди", tone: "idle", icon: Hourglass },
  running: { label: "Выполняется", tone: "info", icon: LoaderCircle },
  retry_wait: { label: "Ждёт повтора", tone: "warn", icon: RotateCcw },
  done: { label: "Готово", tone: "ok", icon: Check },
  failed: { label: "Ошибка", tone: "bad", icon: CircleX },
};
const JOB_STAGE: Record<Job["stage"], string> = {
  queued: "ожидание", inference_detect: "детекция", inference_pose: "позы", analysis: "анализ", evidence: "кадры-доказательства", done: "завершено",
};
const KIND: Record<Job["kind"], string> = { process: "обработка", recompute: "пересчёт" };
const TASK: Record<Metrics["task"], string> = { detect: "детекция", pose: "позы" };
const backendTitle = (b: "linq" | "local") => (b === "linq" ? "LinQ TPU" : "CPU (local)");

function Chip({ tone, icon: I, children, spin }: { tone: Tone; icon: LucideIcon; children: ReactNode; spin?: boolean }) {
  return <span className={`ops-chip ops-tone-${tone}`}><I size={13} strokeWidth={SW} aria-hidden="true" className={spin ? "ops-spin" : undefined} />{children}</span>;
}

interface Check { at: string; state: BackendState; latency_ms: number | null; source: "кнопка" | "WS" | "сервер" }
interface Names { camera: Map<number, string>; sector: Map<number, string> }

export function SystemPage() {
  const system = useApi(() => api.GET("/api/system"), []);
  const models = useApi(() => api.GET("/api/models"), []);
  const health = useApi(() => api.GET("/api/health"), []);
  const admin = useApi(() => api.GET("/api/admin/cameras"), []);
  const [status, setStatus] = useState<BackendStatus>();
  const [checks, setChecks] = useState<Check[]>([]);
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState<ApiFailure>();
  const [live, setLive] = useState<Map<number, Job>>(new Map());
  const [now, setNow] = useState(() => Date.now());
  const reloadTimer = useRef<ReturnType<typeof setTimeout>>();

  useEffect(() => { const t = setInterval(() => setNow(Date.now()), 1000); return () => clearInterval(t); }, []);
  useEffect(() => () => clearTimeout(reloadTimer.current), []);
  const pushCheck = (s: BackendStatus, source: Check["source"]) => {
    if (!s.checked_at) return;
    setChecks(prev => prev.some(c => c.at === s.checked_at) ? prev : [...prev, { at: s.checked_at!, state: s.state, latency_ms: s.latency_ms, source }].slice(-30));
  };
  const initial = system.data?.backend_status;
  useEffect(() => { if (initial) pushCheck(initial, "сервер"); }, [initial]);

  const ws = useWs(message => {
    if (message.type === "backend.status") { setStatus(message.data); pushCheck(message.data, "WS"); }
    if (message.type === "job.progress") {
      const job = message.data;
      setLive(prev => new Map(prev).set(job.id, job));
      if (job.status === "done" || job.status === "failed") {
        clearTimeout(reloadTimer.current);
        reloadTimer.current = setTimeout(() => { setLive(new Map()); system.reload(); }, 800);
      }
    }
  });

  async function check() {
    setChecking(true); setError(undefined);
    try {
      const result = await api.POST("/api/system/backend-check");
      if (result.data) { setStatus(result.data); pushCheck(result.data, "кнопка"); } else setError(apiError(result.error));
    } catch (e) { setError(apiError(e)); }
    setChecking(false);
  }
  async function retry(job: Job) {
    setError(undefined);
    const result = await api.POST("/api/jobs/{job_id}/retry", { params: { path: { job_id: job.id } } });
    if (result.error) setError(apiError(result.error));
    reload();
  }
  function reload() { setLive(new Map()); system.reload(); models.reload(); health.reload(); admin.reload(); }

  const names: Names = useMemo(() => ({
    camera: new Map((admin.data?.cameras ?? []).map(c => [c.id, c.name])),
    sector: new Map((admin.data?.sectors ?? []).map(s => [s.id, s.name])),
  }), [admin.data]);

  const actions = <>
    <button className="button button-small" onClick={reload} disabled={system.loading}><RefreshCw size={14} strokeWidth={SW} aria-hidden="true" /> Обновить</button>
    <button className="button button-small button-primary" onClick={() => void check()} disabled={checking} data-testid="backend-check">
      {checking ? <LoaderCircle size={14} strokeWidth={SW} className="ops-spin" aria-hidden="true" /> : <Radio size={14} strokeWidth={SW} aria-hidden="true" />} {checking ? "Проверяем…" : "Проверить LinQ"}
    </button>
  </>;
  const wsChip = ws.status === "connected" || ws.status === "fixture"
    ? <Chip tone="ok" icon={Wifi}>Живое обновление</Chip>
    : ws.status === "connecting" ? <Chip tone="idle" icon={LoaderCircle} spin>Подключаемся к WS</Chip>
      : <Chip tone="bad" icon={WifiOff}>Нет связи по WS, переподключаемся</Chip>;

  if (system.error) return <div className="ops-page">{<PageHeading title="Состояние системы" meta={wsChip}>{actions}</PageHeading>}<ErrorNotice error={system.error} retry={reload} /></div>;
  if (!system.data) return <div className="ops-page"><PageHeading title="Состояние системы" meta={wsChip}>{actions}</PageHeading><Loading text="Собираем состояние системы" /></div>;

  const data = system.data;
  const backend = status ?? data.backend_status;
  const st = BACKEND_STATE[backend.state];
  // The queue is the server snapshot plus WS job.progress until the next reload.
  const queueMap = new Map(data.queue.map(j => [j.id, j]));
  for (const job of live.values()) {
    if (job.status === "done" || job.status === "failed") queueMap.delete(job.id);
    else queueMap.set(job.id, job);
  }
  const queue = [...queueMap.values()].sort((a, b) => a.id - b.id);
  const recent = data.recent_jobs.map(j => live.get(j.id) ?? j);
  const by = (s: Job["status"]) => queue.filter(j => j.status === s).length;
  const observed = data.cameras.filter(c => c.state !== "no_observation");
  const reasons = new Map<string, number>();
  for (const c of data.cameras) if (c.state === "no_observation") reasons.set(c.reason_text, (reasons.get(c.reason_text) ?? 0) + 1);
  const delay = data.latency.notify_delay_s;
  const failed = recent.filter(j => j.status === "failed").length;
  const latencies = checks.map(c => c.latency_ms).filter((v): v is number => v !== null);

  return <div className="ops-page ops-system" data-testid="system-view">
    <PageHeading title="Состояние системы" meta={<>{wsChip}<span className="ops-asof">данные сервера на <time className="mono">{time(data.server_now)}</time> МСК</span></>}>{actions}</PageHeading>
    {data.fake && <div className="ops-fake" role="note"><AlertTriangle size={15} strokeWidth={SW} aria-hidden="true" /><span><b>Фейк-режим.</b> Настоящий LinQ не вызывается: детекции синтетические, замеры ниже — от фейк-оболочки, а не TPU.</span></div>}
    {error && <div className="ops-inline-error" role="alert"><AlertTriangle size={15} strokeWidth={SW} aria-hidden="true" /><span>{error.message}</span><button className="ops-icon-button" aria-label="Скрыть ошибку" onClick={() => setError(undefined)}><X size={14} strokeWidth={SW} /></button></div>}

    <section className="ops-tiles" aria-label="Сводка">
      <Tile label="Бэкенд инференса" tone={data.fake ? "warn" : "info"} icon={data.backend === "linq" ? Server : Cpu} value={backendTitle(data.backend)}
        sub={data.fake ? "Фейк: детекции синтетические" : data.backend === "linq" ? "Инференс на ускорителе" : "Не LinQ: инференс на процессоре"} />
      <Tile label={data.backend === "linq" ? "Связь с LinQ" : "Проверка моделей"} tone={st.tone} icon={st.icon} value={st.label} testId="backend-state"
        sub={backend.message} foot={backend.checked_at ? `проверено ${time(backend.checked_at)} · ${ago(backend.checked_at, now)}` : "Ещё не проверялся с запуска сервера"} />
      <Tile label="Отклик проверки" tone={backend.latency_ms === null ? "idle" : "info"} icon={Radio} value={backend.latency_ms === null ? "—" : <>{num(backend.latency_ms, 0)}<small> мс</small></>}
        sub={data.backend === "linq" ? "Jupyter, последняя проверка" : "последняя проверка"} spark={latencies.length >= 2 ? <Spark series={[{ values: latencies, tone: "info" }]} label="Отклик проверок за сеанс" /> : undefined}
        foot={latencies.length >= 2 ? `${latencies.length} проверок за сеанс` : undefined} />
      <Tile label="Очередь задач" tone={by("retry_wait") ? "warn" : queue.length ? "info" : "idle"} icon={Hourglass} value={queue.length}
        sub={queue.length ? `выполняется ${by("running")} · ждёт ${by("queued")} · повтор ${by("retry_wait")}` : "Очередь пуста"} foot={failed ? `ошибок среди последних: ${failed}` : undefined} footTone={failed ? "bad" : undefined} />
      <Tile label="Задержка уведомлений, p50" tone={delay.n ? "info" : "idle"} icon={Bell} value={delay.p50 === null ? "—" : <>{num(delay.p50, 2)}<small> с</small></>}
        sub={delay.n ? `p95 ${num(delay.p95, 2)} с · n = ${delay.n}` : "Событий ещё не было (n = 0)"} />
      <Tile label="Камеры под наблюдением" tone={!data.cameras.length ? "idle" : observed.length === data.cameras.length ? "ok" : observed.length ? "warn" : "bad"} icon={observed.length ? Eye : EyeOff}
        value={<>{observed.length}<small> из {data.cameras.length}</small></>} sub={reasons.size ? [...reasons].map(([t, n]) => `${t}: ${n}`).join(" · ") : data.cameras.length ? "Все камеры анализируются" : "Камер нет"} />
    </section>

    <div className="ops-grid ops-grid-main">
      <JobsPanel queue={queue} recent={recent} names={names} retry={job => void retry(job)} />
      <CheckPanel backend={backend} fake={data.fake} kind={data.backend} checks={checks} now={now} checking={checking} check={() => void check()} />
    </div>
    <div className="ops-grid ops-grid-mid">
      <ModelsPanel state={models} fallback={data.models} backend={backend} />
      <LatencyPanel delay={delay} lag={data.latency.publish_lag_ms} />
    </div>
    <div className="ops-grid ops-grid-mid">
      <FreshnessPanel cameras={data.cameras} names={names} />
      <ChannelsPanel channels={data.channels} />
    </div>
    <footer className="ops-statusbar" aria-label="Статус">
      <span>{health.data ? <Chip tone="ok" icon={CircleCheck}>API отвечает</Chip> : health.error ? <Chip tone="bad" icon={CircleX}>API: {health.error.message}</Chip> : <Chip tone="idle" icon={LoaderCircle} spin>API…</Chip>}</span>
      {health.data && <span>контракт <b className="mono">{health.data.contract}</b></span>}
      <span>бэкенд <b>{backendTitle(data.backend)}{data.fake ? " · фейк" : ""}</b></span>
      <span>WS <b>{ws.status === "connected" ? "подключён" : ws.status === "fixture" ? "демо-поток" : ws.status === "connecting" ? "подключается" : "нет связи"}</b></span>
      <span className="ops-statusbar-right">часы сервера <time className="mono">{time(data.server_now)}</time></span>
    </footer>
  </div>;
}

function Tile({ label, value, sub, foot, footTone, tone, icon: I, spark, testId }: { label: string; value: ReactNode; sub?: ReactNode; foot?: ReactNode; footTone?: Tone; tone: Tone; icon: LucideIcon; spark?: ReactNode; testId?: string }) {
  return <div className={`ops-tile ops-tone-${tone}`} data-testid={testId}>
    <div className="ops-tile-label"><I size={14} strokeWidth={SW} aria-hidden="true" />{label}</div>
    <div className={`ops-tile-value ${typeof value === "string" ? "is-text" : "mono"}`}>{value}</div>
    {sub && <div className="ops-tile-sub">{sub}</div>}
    {spark}
    {foot && <div className={`ops-tile-foot ${footTone ? `ops-text-${footTone}` : ""}`}>{foot}</div>}
  </div>;
}

// Minimal SVG sparkline: one polyline per series, last point marked. Only real series, no smoothing.
export function Spark({ series, label, height = 28 }: { series: { values: number[]; tone: Tone; name?: string }[]; label: string; height?: number }) {
  const all = series.flatMap(s => s.values);
  const max = Math.max(...all, 0) || 1, min = Math.min(...all, max);
  const span = max - min || max || 1;
  const w = 120;
  return <svg className="ops-spark" viewBox={`0 0 ${w} ${height}`} preserveAspectRatio="none" role="img" aria-label={label}>
    {series.map((s, i) => {
      const n = s.values.length;
      const pts = s.values.map((v, k) => [n === 1 ? w / 2 : (k / (n - 1)) * (w - 4) + 2, height - 3 - ((v - min) / span) * (height - 6)]);
      const last = pts[pts.length - 1];
      return <g key={i} className={`ops-spark-${s.tone}`}><polyline points={pts.map(p => p.join(",")).join(" ")} fill="none" vectorEffect="non-scaling-stroke" />{last && <circle cx={last[0]} cy={last[1]} r="1.8" />}</g>;
    })}
  </svg>;
}

function JobStatusChip({ job }: { job: Job }) {
  const s = JOB_STATUS[job.status];
  return <Chip tone={s.tone} icon={s.icon} spin={job.status === "running"}>{s.label}</Chip>;
}
function Progress({ value }: { value: number }) {
  const pct = Math.round(Math.max(0, Math.min(1, value)) * 100);
  return <span className="ops-progress" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}><span className="ops-track"><i style={{ width: `${pct}%` }} /></span><b className="mono">{pct}%</b></span>;
}

function JobsPanel({ queue, recent, names, retry }: { queue: Job[]; recent: Job[]; names: Names; retry: (job: Job) => void }) {
  const camera = (id: number) => names.camera.get(id) ?? `Камера ${id}`;
  // Chronological series of measured jobs, one per model task.
  const ordered = [...recent].filter(j => j.metrics.length).sort((a, b) => a.id - b.id);
  const series = (task: Metrics["task"], pick: (m: Metrics) => number | null) => ordered.map(j => j.metrics.find(m => m.task === task)).filter((m): m is Metrics => !!m).map(pick).filter((v): v is number => v !== null);
  const fpsDet = series("detect", m => m.throughput_fps), fpsPose = series("pose", m => m.throughput_fps);
  const rtt50 = series("detect", m => m.tpu_rtt_p50_ms), rtt90 = series("detect", m => m.tpu_rtt_p90_ms);
  const total = ordered.map(j => j.metrics.reduce((s, m) => s + m.total_s, 0));
  return <section className="ops-panel ops-jobs" data-panel="Задачи и замеры">
    <div className="ops-subhead"><h3>Очередь</h3><span className="mono">{queue.length}</span></div>
    {queue.length ? <table className="ops-table">
      <thead><tr><th>Задача</th><th>Камера</th><th>Статус</th><th>Стадия</th><th className="ops-w-progress">Прогресс</th><th className="num">Попытки</th><th>Следующая попытка</th><th>Ошибка</th></tr></thead>
      <tbody>{queue.map(j => <tr key={j.id}>
        <td className="mono ops-job-id">#{j.id}<small>{KIND[j.kind]}</small></td><td>{camera(j.camera_id)}<small className="ops-block ops-muted">видео {j.video_id}</small></td>
        <td><JobStatusChip job={j} /></td><td>{JOB_STAGE[j.stage]}</td><td><Progress value={j.progress} /></td><td className="num mono">{j.attempts}</td>
        <td className="mono">{j.next_attempt_at ? time(j.next_attempt_at) : "—"}</td><td className="ops-err-text">{j.error_text ?? ""}</td>
      </tr>)}</tbody>
    </table> : <p className="ops-empty-line">Очередь пуста: новых видео на обработку нет.</p>}

    <div className="ops-subhead"><h3>Последние задачи</h3><span className="mono">{recent.length}</span>
      {ordered.length >= 2 ? <span className="ops-sparks">
        <span className="ops-spark-box"><em>кадр/с</em><Spark series={[{ values: fpsDet, tone: "info" }, { values: fpsPose, tone: "ok" }]} label="Кадров в секунду по задачам: детекция и позы" /><small><i className="ops-dot-info" />дет. <i className="ops-dot-ok" />позы</small></span>
        {rtt50.length >= 2 && <span className="ops-spark-box"><em>RTT, мс</em><Spark series={[{ values: rtt50, tone: "info" }, { values: rtt90, tone: "warn" }]} label="RTT TPU детекции p50 и p90 по задачам" /><small><i className="ops-dot-info" />p50 <i className="ops-dot-warn" />p90</small></span>}
        <span className="ops-spark-box"><em>всего, с</em><Spark series={[{ values: total, tone: "idle" }]} label="Полное время задач, с" /></span>
      </span> : <span className="ops-muted ops-small">График появится от двух задач с замерами (сейчас {ordered.length})</span>}
    </div>
    {recent.length ? <div className="ops-table-scroll"><table className="ops-table ops-metrics" aria-label="Последние задачи и замеры">
      <thead>
        <tr><th rowSpan={2}>Задача</th><th rowSpan={2}>Статус</th><th rowSpan={2}>Камера</th><th rowSpan={2}>Модель</th><th rowSpan={2} className="num">Кадров</th><th rowSpan={2} className="num">Кадр/с</th>
          <th colSpan={4} className="ops-th-group">мс на кадр</th><th rowSpan={2} className="num">Загрузка, с</th><th rowSpan={2} className="num">Всего, с</th></tr>
        <tr><th className="num">пре</th><th className="num">пост</th><th className="num">RTT p50</th><th className="num">RTT p90</th></tr>
      </thead>
      {recent.map(j => {
        const ms = j.metrics.length ? j.metrics : [null];
        return <tbody key={j.id} className={j.status === "failed" ? "is-failed" : undefined}>
          {ms.map((m, k) => <tr key={k}>
            {k === 0 && <><td rowSpan={ms.length} className="mono ops-job-id">#{j.id}<small>{KIND[j.kind]} · {time(j.finished_at ?? j.created_at)}</small></td>
              <td rowSpan={ms.length}><JobStatusChip job={j} /></td><td rowSpan={ms.length}>{camera(j.camera_id)}<small className="ops-block ops-muted">видео {j.video_id}</small></td></>}
            {m ? <>
              <td><span className="mono ops-nowrap">{m.model_id}@{m.model_version}</span><small className="ops-block ops-muted">{TASK[m.task]} · {m.input_size} px · шаг {m.step}{m.cached ? " · из кэша" : ""}{m.fake ? " · фейк" : ""}{m.backend === "local" ? " · CPU, не LinQ" : ""}</small></td>
              <td className="num mono">{num(m.frames_processed, 0)}</td><td className="num mono">{num(m.throughput_fps, 1)}</td>
              <td className="num mono">{num(m.preprocess_ms, 1)}</td><td className="num mono">{num(m.postprocess_ms, 1)}</td>
              <td className="num mono">{num(m.tpu_rtt_p50_ms, 1)}</td><td className="num mono">{num(m.tpu_rtt_p90_ms, 1)}</td>
              <td className="num mono">{num(m.upload_s, 3)}</td><td className="num mono">{num(m.total_s, 3)}</td>
            </> : <td colSpan={9} className="ops-err-text">{j.status === "failed" ? <span className="ops-fail-line"><span>{j.error_text ?? "Задача завершилась ошибкой"}{j.error_code && <code>{j.error_code}</code>}</span><button className="button button-small" onClick={() => retry(j)}><RotateCcw size={13} strokeWidth={SW} aria-hidden="true" /> Повторить</button></span> : "Замеров нет"}</td>}
          </tr>)}
          {j.status === "failed" && j.metrics.length > 0 && <tr><td colSpan={12} className="ops-err-text"><span className="ops-fail-line"><span>{j.error_text}{j.error_code && <code>{j.error_code}</code>}</span><button className="button button-small" onClick={() => retry(j)}><RotateCcw size={13} strokeWidth={SW} aria-hidden="true" /> Повторить</button></span></td></tr>}
        </tbody>;
      })}
    </table></div> : <p className="ops-empty-line">Завершённых задач пока нет. Загрузите видео в параметрах камеры.</p>}
  </section>;
}

function CheckPanel({ backend, fake, kind, checks, now, checking, check }: { backend: BackendStatus; fake: boolean; kind: "linq" | "local"; checks: Check[]; now: number; checking: boolean; check: () => void }) {
  const st = BACKEND_STATE[backend.state];
  return <section className={`ops-panel ops-check ops-tone-${st.tone}`} data-panel={kind === "linq" ? "Проверка LinQ" : "Проверка бэкенда"} aria-live="polite">
    <div className="ops-check-state" data-testid="check-result">
      <st.icon size={28} strokeWidth={1.5} aria-hidden="true" />
      <div><strong>{st.label}</strong><p>{backend.message}</p></div>
    </div>
    <dl className="ops-kv">
      <div><dt>Бэкенд</dt><dd>{backendTitle(backend.backend)}{backend.fake ? " · фейк" : ""}</dd></div>
      <div><dt>Проверено</dt><dd className="mono">{backend.checked_at ? <>{time(backend.checked_at)} <span className="ops-muted">· {ago(backend.checked_at, now)}</span></> : "ещё нет"}</dd></div>
      <div><dt>Отклик</dt><dd className="mono">{backend.latency_ms === null ? "—" : `${num(backend.latency_ms, 0)} мс`}</dd></div>
    </dl>
    {(backend.present.length > 0 || backend.missing.length > 0) && <ul className="ops-files" aria-label="Программы и файлы моделей">
      {backend.present.map(p => <li key={p} className="ops-text-ok"><Check size={13} strokeWidth={2} aria-hidden="true" /><span className="mono">{p}</span><em>найдена</em></li>)}
      {backend.missing.map(p => <li key={p} className="ops-text-bad"><X size={13} strokeWidth={2} aria-hidden="true" /><span className="mono">{p}</span><em>нет</em></li>)}
    </ul>}
    {fake && <p className="ops-small ops-muted">В фейк-режиме проверка идёт через фейковую оболочку Jupyter: «отвечает» здесь не значит, что настоящий LinQ доступен.</p>}
    <button className="button button-primary ops-check-btn" onClick={check} disabled={checking}>{checking ? <LoaderCircle size={14} strokeWidth={SW} className="ops-spin" aria-hidden="true" /> : <Radio size={14} strokeWidth={SW} aria-hidden="true" />} {checking ? "Проверяем…" : "Проверить ещё раз"}</button>
    <div className="ops-subhead"><h3>Проверки за этот сеанс</h3><span className="mono">{checks.length}</span></div>
    {checks.length ? <ol className="ops-checks">{[...checks].reverse().slice(0, 8).map(c => { const s = BACKEND_STATE[c.state]; return <li key={c.at}>
      <time className="mono">{time(c.at)}</time><Chip tone={s.tone} icon={s.icon}>{s.label}</Chip><span className="mono num">{c.latency_ms === null ? "—" : `${num(c.latency_ms, 0)} мс`}</span><em>{c.source}</em>
    </li>; })}</ol> : <p className="ops-empty-line">Проверок ещё не было. Нажмите «Проверить LinQ».</p>}
  </section>;
}

function ModelsPanel({ state, fallback, backend }: { state: { data?: Schemas["ModelsView"]; error?: ApiFailure; reload: () => void }; fallback: ModelSpec[]; backend: BackendStatus }) {
  const active = state.data?.active ?? fallback;
  const list = state.data ? [...state.data.available] : fallback;
  for (const m of active) if (!list.some(x => x.id === m.id && x.version === m.version)) list.unshift(m);
  const isActive = (m: ModelSpec) => active.some(a => a.id === m.id && a.version === m.version);
  const programState = (p: string | null) => !p ? null : backend.present.includes(p) ? "ok" : backend.missing.includes(p) ? "bad" : null;
  const base = (p: string) => p.split(/[\\/]/).pop() ?? p;
  return <section className="ops-panel" data-panel="Модели">
    {state.error && <ErrorNotice error={state.error} compact retry={state.reload} />}
    {list.length ? <div className="ops-table-scroll"><table className="ops-table">
      <thead><tr><th>Модель</th><th>Задача</th><th className="num">Вход</th><th className="num">conf / iou</th><th>Классы</th><th>Программа LinQ</th><th>Хвост ONNX</th></tr></thead>
      <tbody>{list.sort((a, b) => Number(isActive(b)) - Number(isActive(a))).map(m => { const ps = programState(m.linq_program); return <tr key={`${m.id}@${m.version}`} className={isActive(m) ? "is-active" : "is-idle"}>
        <td><span className="mono">{m.id}@{m.version}</span>{isActive(m) ? <span className="ops-tag ops-tone-ok">активна</span> : <span className="ops-tag">доступна</span>}</td>
        <td>{TASK[m.task]}</td><td className="num mono">{m.input_size}</td><td className="num mono">{num(m.conf, 2)} / {num(m.iou, 2)}</td>
        <td className="ops-classes" title={Object.values(m.classes).join(", ")}>{Object.values(m.classes).join(", ")}</td>
        <td className="mono ops-path" title={m.linq_program ?? undefined}>{m.linq_program ?? "—"}{ps === "ok" && <Check size={12} strokeWidth={2} className="ops-text-ok" aria-label="найдена при проверке" />}{ps === "bad" && <X size={12} strokeWidth={2} className="ops-text-bad" aria-label="не найдена при проверке" />}</td>
        <td className="mono ops-path" title={m.linq_tail ?? undefined}>{m.linq_tail ? base(m.linq_tail) : "—"}</td>
      </tr>; })}</tbody>
    </table></div> : <p className="ops-empty-line">Активных моделей нет: обработка видео не запустится.</p>}
  </section>;
}

function LatencyPanel({ delay, lag }: { delay: Percentiles; lag: Percentiles }) {
  return <section className="ops-panel ops-latency" data-panel="Задержка уведомлений">
    <div className="ops-lat-big">
      <div><em>p50</em><b className="mono">{num(delay.p50, 2)}</b><small>с</small></div>
      <div><em>p95</em><b className="mono">{num(delay.p95, 2)}</b><small>с</small></div>
      <div><em>n</em><b className="mono">{delay.n}</b><small>событий</small></div>
    </div>
    {delay.p50 !== null && delay.p95 !== null && <LatencyScale p50={delay.p50} p95={delay.p95} />}
    <p className="ops-small ops-muted">От начала эпизода на видео до публикации события на пульт.{delay.pending ? ` Ожидают: ${delay.pending}.` : ""}</p>
    <dl className="ops-kv">
      <div><dt>Отставание публикации от плана</dt><dd className="mono">p50 {num(lag.p50, 0)} мс · p95 {num(lag.p95, 0)} мс · n = {lag.n}</dd></div>
    </dl>
    {!delay.n && <p className="ops-empty-line">Событий ещё не публиковалось — считать нечего.</p>}
  </section>;
}
function LatencyScale({ p50, p95 }: { p50: number; p95: number }) {
  const max = Math.max(p95 * 1.25, 0.001);
  return <div className="ops-lat-scale" aria-hidden="true"><i className="ops-lat-range" style={{ left: `${(p50 / max) * 100}%`, width: `${((p95 - p50) / max) * 100}%` }} /><i className="ops-lat-mark" style={{ left: `${(p50 / max) * 100}%` }} /><i className="ops-lat-mark is-p95" style={{ left: `${(p95 / max) * 100}%` }} /><span>0</span><span>{num(max, 2)} с</span></div>;
}

const CAM_STATE: Record<CameraState["state"], { label: string; tone: Tone; icon: LucideIcon }> = {
  normal: { label: "Норма", tone: "ok", icon: CircleCheck },
  yellow: { label: "Жёлтая опасность", tone: "warn", icon: AlertTriangle },
  red: { label: "Красная опасность", tone: "bad", icon: Square },
  no_observation: { label: "Нет наблюдения", tone: "idle", icon: EyeOff },
};
function FreshnessPanel({ cameras, names }: { cameras: CameraState[]; names: Names }) {
  return <section className="ops-panel" data-panel="Свежесть анализа по камерам">
    {cameras.length ? <table className="ops-table">
      <thead><tr><th>Камера</th><th>Сектор</th><th>Состояние</th><th className="num">Свежесть</th><th className="num">Открыто ▲ / ■</th></tr></thead>
      <tbody>{cameras.map(c => { const s = CAM_STATE[c.state]; return <tr key={c.camera_id}>
        <td><Link to={`/operator/cameras/${c.camera_id}`}>{names.camera.get(c.camera_id) ?? `Камера ${c.camera_id}`}</Link></td>
        <td className="ops-muted">{names.sector.get(c.sector_id) ?? `Сектор ${c.sector_id}`}</td>
        <td><Chip tone={s.tone} icon={s.icon}>{c.state === "no_observation" ? c.reason_text : s.label}</Chip></td>
        <td className="num mono">{c.freshness_ms === null ? "—" : c.freshness_ms < 1000 ? `${num(c.freshness_ms, 0)} мс` : `${num(c.freshness_ms / 1000, 1)} с`}</td>
        <td className="num mono"><span className="ops-text-warn">{c.open_yellow}</span> / <span className="ops-text-bad">{c.open_red}</span></td>
      </tr>; })}</tbody>
    </table> : <p className="ops-empty-line">Камер нет.</p>}
    <p className="ops-small ops-muted ops-pad">Свежесть — отставание последнего проанализированного кадра от позиции эфира. «—»: эфира нет, мерить нечего.</p>
  </section>;
}

function ChannelsPanel({ channels }: { channels: Schemas["Channel"][] }) {
  return <section className="ops-panel" data-panel="Каналы доставки">
    {channels.length ? <ul className="ops-channels">{channels.map(c => <li key={`${c.kind}:${c.name}`}>
      {c.kind === "ws" ? <Wifi size={16} strokeWidth={SW} aria-hidden="true" /> : <Webhook size={16} strokeWidth={SW} aria-hidden="true" />}
      <div><strong>{c.name}</strong><span className="mono">{c.kind === "ws" ? "WebSocket" : "Webhook"} · {c.target}</span></div>
      <span className="ops-ch-levels">{c.levels.map(l => <span key={l} className={`ops-level ops-level-${l}`}>{l === "red" ? <Square size={9} strokeWidth={0} fill="currentColor" aria-hidden="true" /> : <AlertTriangle size={10} strokeWidth={2.2} aria-hidden="true" />}{l === "red" ? "Красный" : "Жёлтый"}</span>)}</span>
    </li>)}</ul> : <div className="ops-empty-block"><CircleDashed size={22} strokeWidth={1.5} aria-hidden="true" /><p><b>Внешние каналы не настроены.</b> Уведомления получают только открытые экраны по WebSocket.</p></div>}
    <p className="ops-small ops-muted ops-pad"><Ban size={12} strokeWidth={SW} aria-hidden="true" /> Адреса показаны без секретов: только хост.</p>
  </section>;
}
