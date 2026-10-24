import { api } from "../../api/client";
import { useApi } from "../../api/useApi";
import { useWs } from "../../api/ws";
import { EventFeed } from "../../components/EventFeed";
import { SectorTile } from "../../components/SectorTile";

const RELOAD_ON = new Set(["event.created", "event.updated", "event.escalated", "sector.state"]);

// /operator: sector tiles on the left, the event feed on the right (tech.md 8.14).
export function OperatorDashboard() {
  const view = useApi(() => api.GET("/api/operator/dashboard"), []);
  useWs((message) => RELOAD_ON.has(message.type) && view.reload());
  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!view.data) return <p>Загрузка…</p>;
  return (
    <section className="operator">
      <div className="tiles">
        {view.data.sectors.length === 0 && <p>Секторов нет</p>}
        {view.data.sectors.map((s) => (
          <SectorTile key={s.sector_id} state={s} />
        ))}
      </div>
      <aside>
        <h2>События</h2>
        <EventFeed items={view.data.feed} />
      </aside>
    </section>
  );
}
