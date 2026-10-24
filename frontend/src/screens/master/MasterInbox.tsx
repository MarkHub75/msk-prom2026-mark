import { Link, useNavigate } from "react-router-dom";
import { api } from "../../api/client";
import type { components } from "../../api/schema";
import { useApi } from "../../api/useApi";
import { useWs, type WsNotification } from "../../api/ws";
import { LevelBadge, StatusBadge } from "../../components/Badges";

type EventSummary = components["schemas"]["EventSummary"];

const TIME = new Intl.DateTimeFormat("ru-RU", { timeZone: "Europe/Moscow", timeStyle: "short" });

export function place(e: EventSummary): string {
  return [e.sector_name, e.camera_name, e.zone_name].filter(Boolean).join(" · ");
}

function Card({ event }: { event: EventSummary }) {
  return (
    <Link className={`master-card master-${event.level}`} to={`/master/events/${event.id}`}>
      <span>
        <LevelBadge level={event.level} /> <StatusBadge status={event.status} />
      </span>
      <strong>{event.title}</strong>
      <span>{place(event)}</span>
      <span>{event.reason_text}</span>
      <span>{TIME.format(new Date(event.published_at))}</span>
    </Link>
  );
}

// The chime comes from Toasts in the shell; the phone also vibrates and may show a system notice.
function alertPhone(note: WsNotification): void {
  navigator.vibrate?.(300);
  if (typeof Notification !== "undefined" && Notification.permission === "granted") new Notification(note.text);
}

// /master: one column for the phone, active events in big cards, resolved ones below.
export function MasterInbox() {
  const view = useApi(() => api.GET("/api/master/inbox"), []);
  const navigate = useNavigate();
  useWs((message) => {
    if (message.type === "notification") {
      const note = message.data as WsNotification;
      alertPhone(note);
      // An event handed to the master opens its card at once (tech.md 8.24).
      if (note.id.endsWith(":to_master")) navigate(`/master/events/${note.event_id}`);
    }
    if (message.type === "notification" || message.type.startsWith("event.")) view.reload();
  });
  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!view.data) return <p>Загрузка…</p>;
  const { active, recent_resolved } = view.data;
  return (
    <section className="master">
      <h1>Мои события</h1>
      {active.length === 0 && <p>Активных событий нет</p>}
      {active.map((e) => (
        <Card key={e.id} event={e} />
      ))}
      <h2>Решённые</h2>
      {recent_resolved.length === 0 && <p>Решённых событий нет</p>}
      {recent_resolved.map((e) => (
        <Card key={e.id} event={e} />
      ))}
    </section>
  );
}
