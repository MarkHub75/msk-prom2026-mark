import { useState } from "react";
import { useParams } from "react-router-dom";
import { api, apiError } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { useWs } from "../../api/ws";
import { LevelBadge, StatusBadge } from "../../components/Badges";
import { EvidenceImage } from "../../components/EvidenceImage";
import { place } from "./MasterInbox";

type EventDetail = components["schemas"]["EventDetail"];
type EventSummary = components["schemas"]["EventSummary"];

// /master/events/:eventId: the frame, where and why, «Принял, иду» and «Решено» with the measures.
export function MasterEvent() {
  const eventId = Number(useParams().eventId);
  const [comment, setComment] = useState("");
  const [error, setError] = useState<string>();
  const view = useApi(() => api.GET("/api/events/{event_id}", { params: { path: { event_id: eventId } } }), [eventId]);
  const detail = view.data as EventDetail | undefined;
  useWs((message) => {
    if (message.type.startsWith("event.") && (message.data as EventSummary).id === eventId) view.reload();
  });

  const act = async (action: "accept" | "resolve") => {
    const body = { action, comment: action === "resolve" ? comment : "" };
    const result = await api.POST("/api/events/{event_id}/actions", { params: { path: { event_id: eventId } }, body });
    if (result.error) return setError(apiError(result.error).message);
    setError(undefined);
    view.reload();
  };

  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!detail) return <p>Загрузка…</p>;
  const { event, episode } = detail;
  const shot = episode?.evidence.find((e) => e.kind === "confirm");
  return (
    <section className="master">
      {shot ? <EvidenceImage evidence={shot} hudVisible /> : <p>Нет доказательного кадра</p>}
      <h1>
        <LevelBadge level={event.level} /> {event.title}
      </h1>
      <p>
        <StatusBadge status={event.status} />
      </p>
      <p>{place(event)}</p>
      <p>{event.reason_text}</p>
      {event.escalated_by_timeout && <p className="form-error">Не подтверждено оператором</p>}
      {detail.allowed_actions.includes("accept") && (
        <button type="button" className="master-button" onClick={() => void act("accept")}>
          Принял, иду
        </button>
      )}
      {detail.allowed_actions.includes("resolve") && (
        <>
          <textarea aria-label="Принятые меры" value={comment} onChange={(e) => setComment(e.target.value)} />
          <button type="button" className="master-button" disabled={!comment.trim()} onClick={() => void act("resolve")}>
            Решено
          </button>
        </>
      )}
      {error && <p className="form-error">{error}</p>}
    </section>
  );
}
