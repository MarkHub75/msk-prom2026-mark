import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, apiUrl } from "../../api/client";
import { useApi } from "../../api/useApi";
import { useWs } from "../../api/ws";
import { EventFeed } from "../../components/EventFeed";
import { STATE_ICON } from "../../components/SectorTile";

const PREVIEW_MS = 2000; // preview.cache_s of config/default.yaml
const RELOAD_ON = new Set(["event.created", "event.updated", "event.escalated", "camera.state"]);

// /operator/sectors/:sectorId: camera tiles with previews and state, the sector feed.
export function SectorScreen() {
  const sectorId = Number(useParams().sectorId);
  const view = useApi(
    () => api.GET("/api/sectors/{sector_id}/view", { params: { path: { sector_id: sectorId } } }),
    [sectorId],
  );
  const [frame, setFrame] = useState(0);
  useEffect(() => {
    const timer = setInterval(() => setFrame((n) => n + 1), PREVIEW_MS);
    return () => clearInterval(timer);
  }, []);
  useWs((message) => RELOAD_ON.has(message.type) && view.reload());
  if (view.error) return <p role="alert">{view.error.message}</p>;
  if (!view.data) return <p>Загрузка…</p>;
  const { sector, cameras, feed } = view.data;
  return (
    <section className="operator">
      <div>
        <h1>
          {sector.name}: {STATE_ICON[sector.state]} {sector.reason_text}
        </h1>
        <div className="tiles">
          {cameras.length === 0 && <p>В секторе нет камер</p>}
          {cameras.map(({ camera, state, preview_url }) => (
            <Link key={camera.id} className={`tile state-${state.state}`} to={`/operator/cameras/${camera.id}`}>
              {preview_url ? (
                <img src={`${apiUrl(preview_url)}?n=${frame}`} alt={`Кадр камеры ${camera.name}`} width={320} />
              ) : (
                <span>Нет кадра</span>
              )}
              <strong>{camera.name}</strong>
              <span>
                {STATE_ICON[state.state]} {state.reason_text}
              </span>
            </Link>
          ))}
        </div>
      </div>
      <aside>
        <h2>События сектора</h2>
        <EventFeed items={feed} />
      </aside>
    </section>
  );
}
