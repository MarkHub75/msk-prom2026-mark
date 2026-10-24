import { useEffect, useRef, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import { api, apiError } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { useWs } from "../../api/ws";
import { LevelBadge, StatusBadge } from "../../components/Badges";
import { ClipPlayer } from "../../components/ClipPlayer";
import { EvidenceImage } from "../../components/EvidenceImage";
import { playSound } from "../../components/sound";
import { CameraScreen } from "../operator/CameraScreen";

type EventDetail = components["schemas"]["EventDetail"];
type EventSummary = components["schemas"]["EventSummary"];
type HumanAction = EventDetail["allowed_actions"][number];

// Button titles of tech.md 8.14; the keys 1, 2, 3 press the buttons in the order shown.
const ACTION_TITLES: Record<HumanAction, string> = {
  view: "Просмотрено",
  confirm: "Подтверждаю",
  false_alarm: "Ложное срабатывание",
  send_to_master: "Передать мастеру",
  accept: "Принял, иду",
  resolve: "Решено",
};

const TIME = new Intl.DateTimeFormat("ru-RU", { timeZone: "Europe/Moscow", dateStyle: "short", timeStyle: "medium" });
const sec = (ms: number) => `${(ms / 1000).toFixed(1)} с`;

// /events/:eventId: evidence frame and description on top, the camera broadcast below.
export function EventScreen() {
  const eventId = Number(useParams().eventId);
  const [search] = useSearchParams();
  const [takeover, setTakeover] = useState(search.get("takeover") === "1");
  const [comment, setComment] = useState("");
  const [error, setError] = useState<string>();
  const viewed = useRef(false);
  const view = useApi(() => api.GET("/api/events/{event_id}", { params: { path: { event_id: eventId } } }), [eventId]);
  const detail = view.data as EventDetail | undefined;
  useWs((message) => {
    if (message.type.startsWith("event.") && (message.data as EventSummary).id === eventId) view.reload();
  });

  const act = async (action: HumanAction) => {
    const body = { action, comment };
    const result = await api.POST("/api/events/{event_id}/actions", { params: { path: { event_id: eventId } }, body });
    if (result.error) return setError(apiError(result.error).message);
    setError(undefined);
    if (action !== "view") setTakeover(false);
    view.reload();
  };

  // Opening by the operator is the `view` action (tech.md 8.14).
  useEffect(() => {
    if (viewed.current || !detail?.allowed_actions.includes("view")) return;
    viewed.current = true;
    void act("view");
  });

  useEffect(() => (takeover ? playSound("siren") : undefined), [takeover]);

  const buttons = detail?.allowed_actions.filter((a) => a !== "view") ?? [];
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const action = buttons[Number(e.key) - 1];
      if (action && !(e.target instanceof HTMLTextAreaElement)) void act(action);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!detail) return <p>Загрузка…</p>;
  const { event, episode, provenance: p } = detail;
  const shot = episode?.evidence.find((e) => e.kind === "confirm");
  const facts: [string, string | number | null | undefined][] = [
    ["Режим", event.mode === "demo" ? "демо-данные" : "запись"],
    ["Бэкенд", p.backend && `${p.backend}${p.fake ? ", детекции синтетические" : ""}`],
    ["Детектор", p.det_model],
    ["Поза", p.pose_model],
    ["Задача", p.job_id],
    ["Версия анализа", p.analysis_version],
    ["sha256 видео", p.video_sha256],
    ["sha256 кадра", p.evidence_sha256],
    ["Параметры правила", Object.entries(p.rule_params).map(([k, v]) => `${k}=${v}`).join(", ")],
  ];
  return (
    <section className={takeover ? "event event-takeover" : "event"}>
      {takeover && (
        <button type="button" onClick={() => setTakeover(false)}>
          Свернуть
        </button>
      )}
      <div className="event-top">
        <div>
          {shot ? <EvidenceImage evidence={shot} hudVisible /> : <p>Нет доказательного кадра</p>}
          {event.clip && <ClipPlayer clip={event.clip} />}
        </div>
        <div>
          <h1>
            <LevelBadge level={event.level} /> {event.title}
          </h1>
          <p>
            {event.sector_name} · {event.camera_name}
            {event.zone_name ? ` · ${event.zone_name}` : ""} · <StatusBadge status={event.status} />
          </p>
          <p>
            Начало {TIME.format(new Date(event.started_at))}, длительность {Math.round(event.duration_s)} с
          </p>
          <h2>Почему</h2>
          <dl className="facts">
            {detail.why.map((w) => (
              <div key={w.label}>
                <dt>{w.label}</dt>
                <dd>{w.value}</dd>
              </div>
            ))}
          </dl>
          {episode && (
            <p>
              Эпизод: начало {sec(episode.start_ms)}, подтверждение {sec(episode.confirm_ms)}
              {episode.escalate_ms !== null ? `, жёлтое → красное ${sec(episode.escalate_ms)}` : ""}, конец {sec(episode.end_ms)}
            </p>
          )}
          <h2>История</h2>
          <ol>
            {detail.actions.map((a) => (
              <li key={a.id}>
                {TIME.format(new Date(a.at))} · {a.actor_name} · {a.to_status && <StatusBadge status={a.to_status} />}
                {a.comment && ` · ${a.comment}`}
              </li>
            ))}
          </ol>
          <h2>Происхождение</h2>
          <dl className="facts">
            {facts.map(([label, value]) => (
              <div key={label}>
                <dt>{label}</dt>
                <dd>{value ?? "—"}</dd>
              </div>
            ))}
          </dl>
          {buttons.includes("resolve") && (
            <textarea aria-label="Принятые меры" value={comment} onChange={(e) => setComment(e.target.value)} />
          )}
          <div className="form-buttons">
            {buttons.map((a, i) => (
              <button key={a} type="button" onClick={() => void act(a)}>
                {i + 1}. {ACTION_TITLES[a]}
              </button>
            ))}
          </div>
          {error && <p className="form-error">{error}</p>}
        </div>
      </div>
      <CameraScreen cameraId={event.camera_id} />
    </section>
  );
}
