import { useState } from "react";
import { CircleStop, Play, Radio, Repeat, RotateCcw } from "lucide-react";
import { api, apiError, type ApiFailure } from "../../api/client";
import type { Broadcast, Camera, Video } from "../../api/types";
import { RecordedVideo } from "../../components/Media";
import { duration, Empty, ErrorNotice, time } from "../../components/ui";

const I = { size: 15, strokeWidth: 1.75 } as const;
const STATUS: Record<Broadcast["status"], string> = { playing: "Идёт", stopped: "Остановлен", ended: "Запись закончилась" };

export function BroadcastTab({ camera, videos, broadcast, onChange }: { camera: Camera; videos: Video[]; broadcast: Broadcast | null; onChange: () => void }) {
  const ready = videos.filter((v) => v.active_analysis_id !== null).sort((a, b) => b.id - a.id);
  const [videoId, setVideoId] = useState<number>();
  const [loop, setLoop] = useState(broadcast?.loop ?? false);
  const [error, setError] = useState<ApiFailure>();
  const [busy, setBusy] = useState<"start" | "stop">();
  const chosen = ready.find((v) => v.id === videoId) ?? ready.find((v) => v.id === broadcast?.video_id) ?? ready[0];
  const path = { params: { path: { camera_id: camera.id } } };
  const start = async (id?: number) => {
    setBusy("start"); setError(undefined);
    const result = await api.POST("/api/cameras/{camera_id}/broadcast", { ...path, body: { loop, video_id: id ?? chosen?.id ?? null } });
    setBusy(undefined);
    if (result.error !== undefined) setError(apiError(result.error));
    onChange();
  };
  const stop = async () => {
    setBusy("stop"); setError(undefined);
    const result = await api.DELETE("/api/cameras/{camera_id}/broadcast", path);
    setBusy(undefined);
    if (result.error !== undefined) setError(apiError(result.error));
    onChange();
  };
  const onAir = broadcast?.status === "playing";
  const airVideo = videos.find((v) => v.id === broadcast?.video_id);

  return <div className="adm-air">
    <section className="adm-panel adm-player" data-panel={onAir ? "Эфир · сейчас" : "Эфир"}>
      {broadcast && airVideo ? <RecordedVideo key={broadcast.id} videoId={broadcast.video_id} camera={camera.name} broadcast={broadcast} />
        : <Empty title="Эфира нет" text={ready.length ? "Запустите повтор записи: оператор увидит камеру как живую, с HUD и событиями." : "Нет записи с готовым анализом. Загрузите видео на вкладке «Видео» и дождитесь конца задачи."} />}
    </section>
    <aside className="adm-air-side">
      <section className="adm-panel" data-panel="Что в эфире">
        <div className="adm-air-state">
          <span className={`adm-air-badge ${onAir ? "on" : ""}`}><Radio {...I} />{broadcast ? STATUS[broadcast.status] : "Не запущен"}</span>
          {broadcast && <dl className="adm-kv">
            <div><dt>Запись</dt><dd className="adm-ellipsis">{airVideo?.filename ?? `видео ${broadcast.video_id}`}</dd></div>
            <div><dt>Анализ</dt><dd>#{broadcast.analysis_id}</dd></div>
            <div><dt>Старт</dt><dd>{time(broadcast.started_at)}</dd></div>
            <div><dt title="На момент последнего ответа сервера">Позиция</dt><dd className="adm-tc">{duration(broadcast.position_ms)} / {duration(broadcast.duration_ms)}</dd></div>
            <div><dt>Круг</dt><dd>{broadcast.cycle + 1}</dd></div>
            <div><dt>Повтор</dt><dd>{broadcast.loop ? "по кругу" : "один раз"}</dd></div>
          </dl>}
          <p className="adm-muted">Эфир — повтор загруженной записи по часам сервера. Это не живой поток с камеры.</p>
        </div>
      </section>
      <section className="adm-panel" data-panel="Управление">
        <div className="adm-air-controls">
          <label className="adm-field"><span>Запись для эфира</span>
            <select value={chosen?.id ?? ""} onChange={(e) => setVideoId(Number(e.target.value))} disabled={!ready.length}>
              {!ready.length && <option value="">нет готовых записей</option>}
              {ready.map((v) => <option key={v.id} value={v.id}>{v.filename} · {duration(v.duration_ms)}</option>)}
            </select>
          </label>
          <label className="adm-check"><input type="checkbox" checked={loop} onChange={(e) => setLoop(e.target.checked)} /><Repeat {...I} />Повторять по кругу</label>
          <div className="adm-air-buttons">
            <button type="button" className="button button-primary" disabled={!chosen || busy !== undefined} onClick={() => void start()}><Play {...I} />{busy === "start" ? "Запускаем…" : onAir ? "Запустить выбранную" : "Запустить эфир"}</button>
            <button type="button" className="button" disabled={!onAir || busy !== undefined} onClick={() => void stop()}><CircleStop {...I} />{busy === "stop" ? "Останавливаем…" : "Остановить"}</button>
            <button type="button" className="button" disabled={!broadcast || busy !== undefined} onClick={() => void start(broadcast?.video_id)} title="Начать эту же запись с начала"><RotateCcw {...I} />Сначала</button>
          </div>
          {error && <ErrorNotice error={error} compact />}
        </div>
      </section>
    </aside>
  </div>;
}
