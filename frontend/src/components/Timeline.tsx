import type { components } from "../api/schema";
import { LevelBadge } from "./Badges";

type Episode = components["schemas"]["Episode"];

interface Props {
  episodes: Episode[];
  durationMs: number;
  onSeek: (ms: number) => void;
}

// Episodes on the length of the video: color, icon and text of the level; a click seeks the player.
export function Timeline({ episodes, durationMs, onSeek }: Props) {
  if (episodes.length === 0) return <p>Эпизодов нет</p>;
  return (
    <div className="timeline">
      {episodes.map((e) => (
        <button
          key={e.id}
          type="button"
          className={`timeline-item badge-${e.level_max}`}
          style={{ marginLeft: `${(100 * e.start_ms) / Math.max(durationMs, 1)}%` }}
          onClick={() => onSeek(e.start_ms)}
        >
          <LevelBadge level={e.level_max} /> {e.scenario_title}: {e.reason_text} ({(e.start_ms / 1000).toFixed(1)}–
          {(e.end_ms / 1000).toFixed(1)} с)
        </button>
      ))}
    </div>
  );
}
