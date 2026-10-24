import { useCallback, useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { CircleStop, Play, Radio, RotateCcw, SkipForward } from "lucide-react";
import { api, apiError, type ApiFailure } from "../api/client";
import type { Broadcast, Camera, Video } from "../api/types";
import { useApi } from "../api/useApi";
import { useWs } from "../api/ws";
import { duration, Empty, ErrorNotice, Loading, PageHeading } from "../components/ui";
import { packImported, packLabel, packList } from "../demoPacks";
import "../styles/admin.css";
import "../styles/demo-console.css";

const I = { size: 15, strokeWidth: 1.75 } as const;
const LIVE_THROTTLE_MS = 1500;
// After a launch the button stays locked until the list shows the broadcast (WS broadcast.state + refetch).
const LAUNCH_GUARD_MS = 6000;
const CAPTION = "Пульт ведущего: управляет повтором записей, события создаёт конвейер";

// The checkpoint-demo mock (tools/checkpoint-demo) answers on REST port 4010 and has a director under /__demo/.
export function isMockApi(base: string | undefined = import.meta.env.VITE_API_BASE): boolean {
  if (!base) return false;
  try { return new URL(base).port === "4010"; } catch { return false; }
}

interface Row { camera: Camera; videos: Video[]; broadcast: Broadcast | null; error?: ApiFailure; fetchedAt: number }
interface Director { step: number; story: string[]; open: number }

function failure(result: { error?: unknown; response?: Response }): ApiFailure | undefined {
  if (result.error === undefined) return undefined;
  return { ...apiError(result.error), ...(result.response ? { status: result.response.status } : {}) };
}

async function loadRows() {
  const list = await api.GET("/api/admin/cameras");
  if (list.error !== undefined) return { error: list.error, response: list.response };
  const cameras = list.data.cameras.filter((c) => c.videos_count > 0).sort((a, b) => a.sector_id - b.sector_id || a.id - b.id);
  const rows = await Promise.all(cameras.map(async (camera): Promise<Row> => {
    const path = { params: { path: { camera_id: camera.id } } };
    const [videos, broadcast] = await Promise.all([api.GET("/api/cameras/{camera_id}/videos", path), api.GET("/api/cameras/{camera_id}/broadcast", path)]);
    return { camera, videos: videos.data ?? [], broadcast: broadcast.data ?? null, error: failure(videos) ?? failure(broadcast), fetchedAt: Date.now() };
  }));
  return { data: { rows, sectors: list.data.sectors } };
}

// The record the backend plays for `video_id: null`: the newest ready video of the camera.
function readyVideo(videos: Video[]): Video | undefined {
  return videos.filter((v) => v.status === "ready" && v.active_analysis_id !== null).sort((a, b) => b.id - a.id)[0];
}

function position(b: Broadcast, fetchedAt: number, now: number): number {
  return b.status === "playing" ? Math.min(b.duration_ms, b.position_ms + Math.max(0, now - fetchedAt)) : b.position_ms;
}

function AirState({ broadcast, fetchedAt, now }: { broadcast: Broadcast | null; fetchedAt: number; now: number }) {
  if (!broadcast) return <span className="dc-air"><CircleStop {...I} />Эфир не запущен</span>;
  const pos = <span className="adm-tc">{duration(position(broadcast, fetchedAt, now))} / {duration(broadcast.duration_ms)}</span>;
  if (broadcast.status === "playing") return <span className="dc-air dc-air-on"><Radio {...I} /><b>Идёт</b><em>{broadcast.loop ? "по кругу" : "один раз"}</em>{pos}</span>;
  return <span className="dc-air"><CircleStop {...I} />{broadcast.status === "ended" ? "Запись закончилась" : "Остановлен"}{pos}</span>;
}

function PacksPanel() {
  const packs = useApi(() => api.GET("/api/demo/packs"), []);
  const list = packList(packs.data);
  return <section className="adm-panel" data-panel={`Демо-пакеты${packs.data ? ` · ${list.length}` : ""}`}>
    {packs.error ? <p className="dc-packs-note adm-muted">Список пакетов недоступен ({packs.error.status ?? packs.error.code}): бэкенд без <code>GET /api/demo/packs</code> или мок.</p>
      : !packs.data ? <p className="dc-packs-note adm-muted">Получаем пакеты…</p>
      : !list.length ? <p className="dc-packs-note adm-muted">Пакетов нет. Демо-события сида видны только в журнале и аналитике: в ленту оператора попадают события эфира, поэтому для показа запустите повтор записи ниже.</p>
      : <ol className="dc-packs">{list.map((p) => <li key={p.id} className={`dc-pack ${p.fake ? "dc-pack-fake" : ""}`}>
        <b>{packLabel(p)}</b>
        <span className="adm-muted">камер {p.cameras} · видео {p.videos} · импорт {packImported(p)}</span>
        <code className="adm-muted" title={p.sha256}>{p.sha256.slice(0, 12)}</code>
      </li>)}</ol>}
  </section>;
}

function ScenarioPanel({ base }: { base: string }) {
  // undefined: not asked yet; null: no director (plain Prism `npm run mock` has no /__demo/).
  const [status, setStatus] = useState<Director | null>();
  const [message, setMessage] = useState<string>();
  const [error, setError] = useState<ApiFailure>();
  const [busy, setBusy] = useState<"next" | "reset">();
  const call = useCallback(async (method: "GET" | "POST", path: string) => {
    const response = await fetch(new URL(path, base), { method });
    const body = await response.json().catch(() => ({})) as Record<string, unknown>;
    return { response, body };
  }, [base]);
  const refresh = useCallback(async () => {
    try {
      const { response, body } = await call("GET", "/__demo/status");
      setStatus(response.ok && Array.isArray(body.story) ? body as unknown as Director : null);
    } catch { setStatus(null); }
  }, [call]);
  useEffect(() => { void refresh(); }, [refresh]);
  const run = async (kind: "next" | "reset") => {
    setBusy(kind); setError(undefined); setMessage(undefined);
    try {
      const { response, body } = await call("POST", `/__demo/${kind}`);
      const published = body.published as { id: number; notification_text: string } | undefined;
      if (kind === "reset") setMessage("Сценарий сброшен: мир мока восстановлен, экраны перечитают данные.");
      else if (published) setMessage(`Опубликовано событие #${published.id}: ${published.notification_text}`);
      else setMessage(String(body.message ?? `Ответ ${response.status}`));
      if (!response.ok && response.status !== 409) setError({ code: String(body.code ?? "director"), message: String(body.message ?? `HTTP ${response.status}`), status: response.status });
    } catch {
      setError({ code: "network", message: "Мок не отвечает на /__demo/" });
    }
    setBusy(undefined);
    void refresh();
  };
  const total = status?.story.length ?? 0;
  return <section className="adm-panel dc-scenario" data-panel="Сценарий мока">
    <div className="dc-scenario-body">
      <p className="adm-muted">Фронт работает с моком ({base}). Здесь события публикует режиссёр мока по заготовленной истории — это синтетика, не результат конвейера.</p>
      <div className="dc-scenario-state">
        {status ? <span>Шаг <b className="adm-tc">{Math.min(status.step, total)} / {total}</b> · открыто событий: <b>{status.open}</b></span>
          : status === null ? <span className="adm-warn">Режиссёр не отвечает на /__demo/status: это Prism без сценария. Сценарий есть у мока tools/checkpoint-demo (ветка demo/checkpoint).</span>
          : <span className="adm-muted">спрашиваем режиссёра…</span>}
      </div>
      <div className="dc-buttons">
        <button type="button" className="button button-primary" disabled={busy !== undefined || !status || status.step >= total} onClick={() => void run("next")}><SkipForward {...I} />{busy === "next" ? "Публикуем…" : "Следующий шаг"}</button>
        <button type="button" className="button" disabled={busy !== undefined || !status} onClick={() => void run("reset")}><RotateCcw {...I} />{busy === "reset" ? "Сбрасываем…" : "Сбросить сценарий"}</button>
      </div>
      {message && <p className="dc-message" role="status">{message}</p>}
      {error && <ErrorNotice error={error} compact />}
    </div>
  </section>;
}

// `mockBase`: the REST origin of the mock when the front runs against it (scenario buttons), undefined for a backend.
export function DemoConsolePage({ mockBase = isMockApi() ? import.meta.env.VITE_API_BASE as string : undefined }: { mockBase?: string }) {
  const mock = mockBase !== undefined;
  const fresh = useApi(loadRows, []);
  const last = useRef(fresh.data);
  if (fresh.data) last.current = fresh.data;
  const data = fresh.data ?? last.current;
  const reload = fresh.reload;
  const [busy, setBusy] = useState<Record<number, "play" | "stop">>({});
  const [errors, setErrors] = useState<Record<number, ApiFailure | undefined>>({});
  const [stopAll, setStopAll] = useState<{ busy: boolean; text?: string }>({ busy: false });
  const [now, setNow] = useState(() => Date.now());
  // Just launched, the list has not shown «Идёт» yet: a second press would restart the record and publish its episodes again.
  const [launched, setLaunched] = useState<Record<number, true>>({});
  const launchTimers = useRef<ReturnType<typeof setTimeout>[]>([]);
  useEffect(() => () => launchTimers.current.forEach(clearTimeout), []);

  const pending = useRef<ReturnType<typeof setTimeout>>();
  const latestReload = useRef(reload);
  latestReload.current = reload;
  useEffect(() => () => clearTimeout(pending.current), []);
  useWs(useCallback((m) => {
    if (m.type !== "broadcast.state" || pending.current) return;
    pending.current = setTimeout(() => { pending.current = undefined; latestReload.current(); }, LIVE_THROTTLE_MS);
  }, []));

  const rows = data?.rows ?? [];
  const playing = rows.filter((r) => r.broadcast?.status === "playing");
  useEffect(() => {
    if (!playing.length) return;
    const timer = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(timer);
  }, [playing.length]);

  const act = async (camera: Camera, kind: "play" | "stop", video?: Video) => {
    setBusy((b) => ({ ...b, [camera.id]: kind }));
    setErrors((e) => ({ ...e, [camera.id]: undefined }));
    const path = { params: { path: { camera_id: camera.id } } };
    const result = kind === "play"
      ? await api.POST("/api/cameras/{camera_id}/broadcast", { ...path, body: { loop: false, video_id: video?.id ?? null } })
      : await api.DELETE("/api/cameras/{camera_id}/broadcast", path);
    setErrors((e) => ({ ...e, [camera.id]: failure(result) }));
    if (kind === "play" && !failure(result)) {
      setLaunched((l) => ({ ...l, [camera.id]: true }));
      launchTimers.current.push(setTimeout(() => setLaunched((l) => { const next = { ...l }; delete next[camera.id]; return next; }), LAUNCH_GUARD_MS));
    }
    setBusy((b) => { const next = { ...b }; delete next[camera.id]; return next; });
    reload();
  };

  const stopEverything = async () => {
    setStopAll({ busy: true });
    const targets = rows.filter((r) => r.broadcast?.status === "playing");
    const results = await Promise.all(targets.map((r) => api.DELETE("/api/cameras/{camera_id}/broadcast", { params: { path: { camera_id: r.camera.id } } })));
    const failed = results.map((r, i) => [targets[i].camera.id, failure(r)] as const).filter(([, e]) => e);
    setErrors((e) => ({ ...e, ...Object.fromEntries(failed) }));
    setStopAll({ busy: false, text: failed.length ? `Не удалось остановить: ${failed.length} из ${targets.length}` : `Остановлено эфиров: ${targets.length}` });
    reload();
  };

  const sectorName = (id: number) => data?.sectors.find((s) => s.id === id)?.name ?? `сектор ${id}`;
  const heading = <PageHeading title="Демо-пульт" meta={<span className="adm-muted">{CAPTION}</span>}>
    <button type="button" className="button" disabled={stopAll.busy || !playing.length} onClick={() => void stopEverything()} title={playing.length ? undefined : "Сейчас ни одна камера не в эфире"}><CircleStop {...I} />{stopAll.busy ? "Останавливаем…" : "Остановить все эфиры"}</button>
  </PageHeading>;

  return <div className="adm-page dc-page">
    {heading}
    {mockBase !== undefined && <ScenarioPanel base={mockBase} />}
    <PacksPanel />
    <section className="adm-panel" data-panel={`Камеры с записями${data ? ` · ${rows.length}` : ""}`}>
      {stopAll.text && <p className="dc-message adm-pad" role="status">{stopAll.text}</p>}
      {fresh.error && !data ? <div className="adm-pad"><ErrorNotice error={fresh.error} retry={reload} /></div>
        : !data ? <Loading text="Загружаем камеры и эфиры" />
        : !rows.length ? <Empty title="Нет камер с записями" text={mock ? "У камер мока нет записей, а эфир мок не ведёт (ответ 501): сценарием управляют кнопки выше." : "Загрузите видео камере на экране «Камеры» и дождитесь анализа: здесь появится кнопка повтора."} />
        : <ol className="dc-list">{rows.map((r) => {
          const video = readyVideo(r.videos);
          const onAir = r.broadcast?.status === "playing";
          const error = errors[r.camera.id] ?? r.error;
          return <li key={r.camera.id} className={`dc-row ${onAir ? "dc-row-on" : ""}`}>
            <div className="dc-cam">
              <Link to={`/admin/cameras/${r.camera.id}`}><b>{r.camera.name}</b></Link>
              <small className="adm-muted">{sectorName(r.camera.sector_id)}</small>
            </div>
            <div className="dc-video">
              {video ? <><span className="adm-ellipsis" title={video.filename}>{video.filename}</span><small className="adm-muted">{duration(video.duration_ms)} · анализ #{video.active_analysis_id}</small></>
                : <span className="adm-muted">нет записи с готовым анализом</span>}
            </div>
            <AirState broadcast={r.broadcast} fetchedAt={r.fetchedAt} now={now} />
            <div className="dc-buttons">
              <button type="button" className="button" disabled={!video || busy[r.camera.id] !== undefined || onAir || launched[r.camera.id]} title={onAir || launched[r.camera.id] ? "Камера уже в эфире: повторный запуск опубликует события записи ещё раз. Дождитесь конца или остановите эфир." : undefined} onClick={() => void act(r.camera, "play", video)} aria-label={`Проиграть один раз: ${r.camera.name}`}><Play {...I} />{busy[r.camera.id] === "play" ? "Запускаем…" : "Проиграть один раз"}</button>
              <button type="button" className="button" disabled={!onAir || busy[r.camera.id] !== undefined} onClick={() => void act(r.camera, "stop")} aria-label={`Остановить: ${r.camera.name}`}><CircleStop {...I} />{busy[r.camera.id] === "stop" ? "Останавливаем…" : "Остановить"}</button>
            </div>
            {error && <div className="dc-error"><ErrorNotice error={error} compact /></div>}
          </li>;
        })}</ol>}
    </section>
    {!mock && <p className="adm-muted dc-note">Сброса мира через API нет: события прошлых прогонов остаются в журнале. Для чистого показа перезапустите бэкенд на пустом data_dir с <code>--seed</code>.</p>}
  </div>;
}
