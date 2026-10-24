import { Link } from "react-router-dom";
import type { components } from "../api/schema";
import { LevelBadge, StatusBadge } from "./Badges";

type EventSummary = components["schemas"]["EventSummary"];

const TIME = new Intl.DateTimeFormat("ru-RU", { timeZone: "Europe/Moscow", timeStyle: "medium" });

// The operator feed as chat messages: level, sector, reason, time, duration, status.
export function EventFeed({ items }: { items: EventSummary[] }) {
  if (items.length === 0) {
    return <p>Событий нет — это не значит, что всё безопасно, если камера без наблюдения</p>;
  }
  return (
    <ol className="feed">
      {items.map((e) => (
        <li key={e.id} className={`feed-item badge-${e.level}`}>
          <Link to={`/events/${e.id}`}>
            <LevelBadge level={e.level} /> {e.sector_name} · {e.reason_text}
          </Link>
          <div>
            {TIME.format(new Date(e.started_at))} · {Math.round(e.duration_s)} с · <StatusBadge status={e.status} />
          </div>
        </li>
      ))}
    </ol>
  );
}
