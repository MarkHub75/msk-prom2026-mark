import { Link } from "react-router-dom";
import type { EventSummary } from "../api/types";
import { Empty, Icon, number, Status, time } from "./ui";
export function EventFeed({ events, master = false, compact = false }: { events: EventSummary[]; master?: boolean; compact?: boolean }) {
  if (!events.length) return <Empty title="Событий нет" text="Новых событий для этой выборки не получено." />;
  return <ol className={`event-feed ${compact ? "compact" : ""}`}>{events.map((event, index) => <li key={event.id} className={`feed-event feed-${event.level}`}>
    <Link to={`${master ? "/master/events" : "/events"}/${event.id}`} className="feed-event-link">
      <div className="feed-topline"><time>{time(event.published_at)}</time><span>#{event.id}</span><Icon name="arrow" size={17} /></div>
      <div className="feed-place">Сектор {number(event.sector_id)} / {event.camera_name}</div>
      <h3>{event.title}</h3><p className="feed-reason">{event.reason_text}</p><Status event={event} />
      {index === 0 && !master && <span className={`button ${event.level === "red" ? "button-danger" : "button-light"}`}>Открыть доказательство<Icon name="arrow" /></span>}
    </Link>
  </li>)}</ol>;
}
