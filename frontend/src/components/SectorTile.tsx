import { Link } from "react-router-dom";
import type { components } from "../api/schema";

type SectorState = components["schemas"]["SectorState"];
type StateKind = SectorState["state"];

// State is never shown by color alone: an icon and the text from the server go with it.
export const STATE_ICON: Record<StateKind, string> = { normal: "●", yellow: "▲", red: "■", no_observation: "○" };

export function SectorTile({ state }: { state: SectorState }) {
  return (
    <Link className={`tile state-${state.state}`} to={`/operator/sectors/${state.sector_id}`}>
      <strong>{state.name}</strong>
      <span>
        {STATE_ICON[state.state]} {state.reason_text}
      </span>
      <span>
        жёлтых: {state.open_yellow} · красных: {state.open_red}
      </span>
      <span>
        нет наблюдения: {state.cameras_no_observation} из {state.cameras_total}
      </span>
    </Link>
  );
}
