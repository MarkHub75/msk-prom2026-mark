import { Link } from "react-router-dom";
import { api } from "../../api/client";
import { useApi } from "../../api/useApi";
import { useWs } from "../../api/ws";
import { LevelBadge, StatusBadge } from "../../components/Badges";
import { place } from "../master/MasterInbox";

const TIME = new Intl.DateTimeFormat("ru-RU", { timeZone: "Europe/Moscow", timeStyle: "short" });

// /m/operator: the operator feed in one column for the phone; a tap opens the card (tech.md 8.14).
// The chime comes from Toasts in the shell; the phone also vibrates.
export function OperatorMobile() {
  const view = useApi(() => api.GET("/api/operator/feed"), []);
  useWs((message) => {
    if (message.type === "notification") navigator.vibrate?.(300);
    if (message.type === "notification" || message.type.startsWith("event.")) view.reload();
  });
  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!view.data) return <p>Загрузка…</p>;
  return (
    <section className="master">
      <h1>События</h1>
      {view.data.length === 0 && <p>Событий нет — это не значит, что всё безопасно, если камера без наблюдения</p>}
      {view.data.map((e) => (
        <Link key={e.id} className={`master-card master-${e.level}`} to={`/m/operator/events/${e.id}`}>
          <span>
            <LevelBadge level={e.level} /> <StatusBadge status={e.status} />
          </span>
          <strong>{e.title}</strong>
          <span>{place(e)}</span>
          <span>{e.reason_text}</span>
          <span>{TIME.format(new Date(e.published_at))}</span>
        </Link>
      ))}
    </section>
  );
}
