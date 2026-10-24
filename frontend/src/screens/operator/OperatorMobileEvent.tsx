import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import { api, apiError } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { useWs } from "../../api/ws";
import { LevelBadge, StatusBadge } from "../../components/Badges";
import { ClipPlayer } from "../../components/ClipPlayer";
import { EvidenceImage } from "../../components/EvidenceImage";
import { ACTION_TITLES } from "../events/EventScreen";
import { place } from "../master/MasterInbox";

type EventDetail = components["schemas"]["EventDetail"];
type EventSummary = components["schemas"]["EventSummary"];
type HumanAction = EventDetail["allowed_actions"][number];

// /m/operator/events/:eventId: the evidence, the clip, where and why, the operator's buttons.
export function OperatorMobileEvent() {
  const eventId = Number(useParams().eventId);
  const [error, setError] = useState<string>();
  const viewed = useRef(false);
  const view = useApi(() => api.GET("/api/events/{event_id}", { params: { path: { event_id: eventId } } }), [eventId]);
  const detail = view.data as EventDetail | undefined;
  useWs((message) => {
    if (message.type.startsWith("event.") && (message.data as EventSummary).id === eventId) view.reload();
  });

  const act = async (action: HumanAction) => {
    const body = { action, comment: "" };
    const result = await api.POST("/api/events/{event_id}/actions", { params: { path: { event_id: eventId } }, body });
    if (result.error) return setError(apiError(result.error).message);
    setError(undefined);
    view.reload();
  };

  // Opening by the operator is the `view` action (tech.md 8.14).
  useEffect(() => {
    if (viewed.current || !detail?.allowed_actions.includes("view")) return;
    viewed.current = true;
    void act("view");
  });

  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!detail) return <p>Загрузка…</p>;
  const { event, episode } = detail;
  const shot = episode?.evidence.find((e) => e.kind === "confirm");
  return (
    <section className="master">
      {shot ? <EvidenceImage evidence={shot} hudVisible /> : <p>Нет доказательного кадра</p>}
      {event.clip && <ClipPlayer clip={event.clip} />}
      <h1>
        <LevelBadge level={event.level} /> {event.title}
      </h1>
      <p>
        <StatusBadge status={event.status} />
      </p>
      <p>{place(event)}</p>
      <p>{event.reason_text}</p>
      {detail.allowed_actions
        .filter((a) => a !== "view")
        .map((a) => (
          <button key={a} type="button" className="master-button" onClick={() => void act(a)}>
            {ACTION_TITLES[a]}
          </button>
        ))}
      {error && <p className="form-error">{error}</p>}
    </section>
  );
}
