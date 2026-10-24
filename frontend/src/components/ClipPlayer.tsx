import { apiUrl } from "../api/client";
import type { components } from "../api/schema";

type Clip = components["schemas"]["Clip"];

// The clip is a window of the source video (tech.md 8.20): the URL ends with `#t=<from>,<to>`,
// and playback stops at the end of the window.
export function ClipPlayer({ clip }: { clip: Clip }) {
  if (!clip.playable) return <p>Видео не воспроизводится браузером</p>;
  return (
    <video
      src={apiUrl(clip.url)}
      controls
      muted
      preload="metadata"
      width={320}
      aria-label="Клип события"
      onTimeUpdate={(e) => {
        if (e.currentTarget.currentTime * 1000 >= clip.end_ms) e.currentTarget.pause();
      }}
    />
  );
}
