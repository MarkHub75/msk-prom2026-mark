// Shared parts of the camera setup tabs: meta, the camera frame with a measured overlay,
// the recompute notice of tech.md 8.12 and a two-step confirm button.
import { useEffect, useLayoutEffect, useRef, useState, type ReactNode } from "react";
import { AlertTriangle, Check, ImageOff, Loader2, RefreshCw, TriangleAlert, X } from "lucide-react";
import { api, apiError, mediaUrl, type ApiFailure } from "../../api/client";
import type { Job, Meta, Video } from "../../api/types";
import { useApi } from "../../api/useApi";
import { useMeta } from "../../components/AppShell";
import { fmt } from "./geometry";

export const ICON = { size: 15, strokeWidth: 1.75 } as const;

/** Meta from the shell; the tabs fetch it themselves when rendered outside AppShell (tests, dev route). */
export function useSetupMeta(): { meta?: Meta; error?: ApiFailure } {
  const shell = useMeta();
  const own = useApi(() => (shell ? Promise.resolve({ data: shell }) : api.GET("/api/meta")), [shell]);
  return { meta: shell ?? own.data, error: shell ? undefined : own.error };
}

/** The last loaded value: a reload after a save does not blank the editor. */
export function useLastLoaded<T>(value: T | undefined, key: unknown): T | undefined {
  const [kept, setKept] = useState<{ key: unknown; value: T } | undefined>();
  useEffect(() => { if (value !== undefined) setKept({ key, value }); }, [value, key]);
  if (value !== undefined) return value;
  return kept && kept.key === key ? kept.value : undefined;
}

export interface FrameSize { w: number; h: number }

/** Camera frame (`/preview`) fitted into the well; the overlay gets the rendered size in px. */
export function FrameStage({ cameraId, children, toolbar, statusbar, className = "" }: {
  cameraId: number;
  children: (size: FrameSize) => ReactNode;
  toolbar?: ReactNode;
  statusbar?: ReactNode;
  className?: string;
}) {
  const well = useRef<HTMLDivElement>(null);
  const [box, setBox] = useState<FrameSize>({ w: 960, h: 540 });
  const [ratio, setRatio] = useState(16 / 9);
  const [stamp, setStamp] = useState(0);
  const [frameError, setFrameError] = useState<string>();
  const src = mediaUrl(`/api/cameras/${cameraId}/preview${stamp ? `?t=${stamp}` : ""}`);

  useLayoutEffect(() => {
    const el = well.current;
    if (!el) return;
    const measure = () => {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) setBox({ w: r.width, h: r.height });
    };
    measure();
    if (typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  useEffect(() => setFrameError(undefined), [cameraId, stamp]);

  const onError = () => {
    // The <img> does not expose the body: ask once more for the ApiError text.
    fetch(src).then(async (r) => {
      const body = r.ok ? null : await r.json().catch(() => null);
      setFrameError(body ? apiError(body).message : "Кадр не загрузился");
    }).catch(() => setFrameError("Сервер не отвечает"));
  };

  const w = Math.max(1, Math.floor(Math.min(box.w, box.h * ratio)));
  const h = Math.max(1, Math.floor(w / ratio));
  return (
    <div className={`geo-stage-panel ${className}`} data-panel="Кадр камеры">
      {toolbar && <div className="geo-toolbar">{toolbar}</div>}
      <div className="geo-well" ref={well}>
        <div className="geo-stage" style={{ width: w, height: h }}>
          {frameError ? (
            <div className="geo-noframe">
              <ImageOff size={22} strokeWidth={1.5} />
              <strong>Нет кадра камеры</strong>
              <span>{frameError}</span>
              <small>Разметка сохраняется в долях кадра и подойдёт к будущему видео той же камеры.</small>
            </div>
          ) : (
            <img
              src={src}
              alt="Кадр камеры"
              draggable={false}
              onLoad={(e) => { const i = e.currentTarget; if (i.naturalWidth && i.naturalHeight) setRatio(i.naturalWidth / i.naturalHeight); }}
              onError={onError}
            />
          )}
          {children({ w, h })}
        </div>
      </div>
      <div className="geo-statusbar">
        {statusbar}
        <button type="button" className="geo-ghost" onClick={() => setStamp(Date.now())} title="Запросить свежий кадр">
          <RefreshCw {...ICON} size={13} /> Кадр
        </button>
      </div>
    </div>
  );
}

export function FieldError({ error, field, also }: { error?: ApiFailure; field: string; also?: string | null }) {
  const own = error && error.details?.field === field ? error.message : undefined;
  const text = own ?? also ?? undefined;
  if (!text) return null;
  return <p className="geo-field-error" role="alert"><TriangleAlert {...ICON} size={13} /> {text}</p>;
}

/** Error not tied to a field (403, 404, network). */
export function FormError({ error, fields }: { error?: ApiFailure; fields: string[] }) {
  if (!error || (typeof error.details?.field === "string" && fields.includes(error.details.field))) return null;
  return <div className="geo-form-error" role="alert"><AlertTriangle {...ICON} /> <span>{error.message}</span></div>;
}

/** Destructive action in two clicks: the second click within the inline confirm runs it. */
export function ConfirmButton({ label, confirm, onConfirm, disabled, icon }: { label: string; confirm: string; onConfirm: () => void; disabled?: boolean; icon?: ReactNode }) {
  const [asking, setAsking] = useState(false);
  if (!asking) return <button type="button" className="button button-small geo-danger-ghost" disabled={disabled} onClick={() => setAsking(true)}>{icon}{label}</button>;
  return (
    <div className="geo-confirm" role="alertdialog" aria-label={confirm}>
      <span>{confirm}</span>
      <button type="button" className="button button-small button-danger" onClick={() => { setAsking(false); onConfirm(); }}><Check {...ICON} size={13} /> Удалить</button>
      <button type="button" className="button button-small" onClick={() => setAsking(false)}><X {...ICON} size={13} /> Отмена</button>
    </div>
  );
}

const STAGE_TITLES: Record<Job["stage"], string> = {
  queued: "в очереди", inference_detect: "детекция", inference_pose: "поза", analysis: "анализ", evidence: "кадры-доказательства", done: "готово",
};

/** After a geometry or rules change: events of the published analysis are not rewritten until a recompute (tech.md 8.12). */
export function RecomputeNotice({ cameraId, what }: { cameraId: number; what: string }) {
  const videos = useApi(() => api.GET("/api/cameras/{camera_id}/videos", { params: { path: { camera_id: cameraId } } }), [cameraId]);
  const [job, setJob] = useState<Job>();
  const [error, setError] = useState<ApiFailure>();
  const video: Video | undefined = (videos.data ?? []).filter((v) => v.status === "ready" && v.active_analysis_id !== null).sort((a, b) => b.id - a.id)[0];
  const running = job && (job.status === "queued" || job.status === "running" || job.status === "retry_wait");

  useEffect(() => {
    if (!job || !running) return;
    const t = setTimeout(async () => {
      const r = await api.GET("/api/jobs/{job_id}", { params: { path: { job_id: job.id } } });
      if (r.data) setJob(r.data); else setError(apiError(r.error));
    }, 1000);
    return () => clearTimeout(t);
  }, [job, running]);

  const start = async () => {
    if (!video) return;
    setError(undefined);
    const r = await api.POST("/api/videos/{video_id}/recompute", { params: { path: { video_id: video.id } } });
    if (r.data) setJob(r.data); else setError(apiError(r.error));
  };

  return (
    <div className="geo-recompute" data-testid="recompute-notice">
      <div className="geo-recompute-text">
        <strong>{what}</strong>
        {!job && <span>Новый анализ видео учтёт изменения. Уже опубликованные события пересчитываются по кнопке: необработанные получат статус «Пересчитано», события, с которыми работали люди, не меняются.</span>}
        {job && running && <span><Loader2 {...ICON} size={13} className="geo-spin" /> Пересчёт видео №{video?.id ?? job.video_id}: {STAGE_TITLES[job.stage]}, {fmt(job.progress * 100, 0)} %</span>}
        {job?.status === "done" && <span className="geo-ok"><Check {...ICON} size={13} /> Пересчёт готов: анализ №{job.analysis_id ?? "—"}. Прежние необработанные события помечены «Пересчитано»; если эфир играл это видео, он перезапущен с новым анализом.</span>}
        {job?.status === "failed" && <span className="geo-bad"><TriangleAlert {...ICON} size={13} /> Пересчёт не удался: {job.error_text ?? job.error_code}</span>}
        {error && <span className="geo-bad"><TriangleAlert {...ICON} size={13} /> {error.message}</span>}
      </div>
      {!running && job?.status !== "done" && (
        <button type="button" className="button button-small" disabled={!video} onClick={() => void start()} title={video ? `Видео №${video.id}` : "У камеры нет готового видео"}>
          <RefreshCw {...ICON} size={13} /> {video ? "Пересчитать события" : "Нет готового видео"}
        </button>
      )}
    </div>
  );
}
