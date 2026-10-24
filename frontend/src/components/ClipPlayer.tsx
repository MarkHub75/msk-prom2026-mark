import { useRef, useState } from "react";
import { mediaUrl } from "../api/client";
import type { EventSummary } from "../api/types";
import { duration, Empty, Icon } from "./ui";
import "../styles/mobile-clip.css";

type Clip = NonNullable<EventSummary["clip"]>;

/** Event clip (tech.md 8.20): a window of the source video, `url` carries `#t=start,end`; plays inside the window and stops at its end. */
export function ClipPlayer({ clip, title = "Клип события" }: { clip: Clip; title?: string }) {
  const video = useRef<HTMLVideoElement>(null);
  const [failed, setFailed] = useState(false);
  const range = `${duration(clip.start_ms)}–${duration(clip.end_ms)}`;
  const replay = () => { const el = video.current; if (!el) return; el.currentTime = clip.start_ms / 1000; void el.play().catch(() => undefined); };
  // The fragment end is a hint only some browsers honour: stop at end_ms ourselves.
  const guard = () => { const el = video.current; if (el && el.currentTime * 1000 >= clip.end_ms) { el.pause(); el.currentTime = clip.end_ms / 1000; } };
  return <section className="clip" aria-label={title} data-testid="clip-player">
    <header className="clip-head"><span><Icon name="play" size={14} />{title}</span><span className="mono">{range}</span></header>
    {!clip.playable || failed
      ? <Empty title="Клип не воспроизводится в браузере" text={failed ? "Не удалось загрузить запись из источника. Кадр события доступен выше." : "Формат записи не поддерживается браузером, H.264-копии нет."} />
      : <div className="clip-frame">
        <video ref={video} src={mediaUrl(clip.url)} controls playsInline muted preload="metadata" onTimeUpdate={guard} onError={() => setFailed(true)} />
        <button type="button" className="clip-replay" onClick={replay}><Icon name="refresh" size={14} />С начала клипа</button>
      </div>}
  </section>;
}
