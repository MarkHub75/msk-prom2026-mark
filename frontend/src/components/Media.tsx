import { useEffect, useRef, useState, type CSSProperties } from "react";
import { api, videoUrl, mediaUrl } from "../api/client";
import { useApi } from "../api/useApi";
import type { Broadcast, Episode, Evidence, HudObject, Video } from "../api/types";
import { isReviewMode } from "../fixtures/review";
import { duration, Empty, ErrorNotice, Icon, time } from "./ui";

function Hud({ objects }: { objects: HudObject[] }) {
  return <svg className="hud-layer" viewBox="0 0 1000 1000" preserveAspectRatio="none" aria-label="Объекты на исходном кадре">{objects.map((object, i) => { const [x1,y1,x2,y2] = object.bbox; const level = object.tags.find(t => t.level)?.level ?? "neutral"; return <g key={`${object.track_id}-${i}`} className={`hud-object hud-${level}`}><rect x={x1*1000} y={y1*1000} width={(x2-x1)*1000} height={(y2-y1)*1000} vectorEffect="non-scaling-stroke" /><title>{object.label} · {Math.round(object.score * 100)}%</title></g>; })}</svg>;
}
export function EvidenceFrame({ evidence, camera, level }: { evidence: Evidence; camera: string; level: "red" | "yellow" }) {
  const [failed, setFailed] = useState(false);
  useEffect(() => setFailed(false), [evidence.url]);
  return <div className={`evidence-frame level-frame-${level}`}>
    {failed ? <Empty title="Кадр не загрузился" text="Доказательство недоступно по адресу, полученному от API." /> : <div className="evidence-image-wrap"><img src={mediaUrl(evidence.url)} alt={`Доказательный кадр: ${camera}, кадр ${evidence.frame_idx}`} onError={() => setFailed(true)} /><Hud objects={evidence.objects} /><span className="media-stamp">{camera}<b>{duration(evidence.ts_ms)} · кадр {evidence.frame_idx}</b></span><span className="media-source">{isReviewMode() ? "Синтетический кадр" : "Доказательство · исходный кадр"}</span></div>}
  </div>;
}
export function VideoWithHud({ video, camera, initialMs = 0, episodes = [], broadcast }: { video: Video; camera: string; initialMs?: number; episodes?: Episode[]; broadcast?: Broadcast | null }) {
  const player = useRef<HTMLVideoElement>(null);
  const [position, setPosition] = useState(initialMs);
  const [playing, setPlaying] = useState(false);
  const [hud, setHud] = useState(true);
  const [failed, setFailed] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [rate, setRate] = useState(1);
  const [follow, setFollow] = useState(Boolean(broadcast));
  const broadcastKey = broadcast ? `${broadcast.id}:${broadcast.server_now}:${broadcast.position_ms}:${broadcast.status}` : "";
  const anchor = useRef({key:broadcastKey,received:performance.now()});
  if(anchor.current.key !== broadcastKey) anchor.current = {key:broadcastKey,received:performance.now()};
  const targetPosition = () => {
    if(!broadcast)return initialMs;
    const elapsed = broadcast.status === "playing" ? performance.now()-anchor.current.received : 0;
    const serverElapsed = Date.parse(broadcast.server_now)-Date.parse(broadcast.started_at);
    const snapshot = Number.isFinite(broadcast.position_ms) ? broadcast.position_ms : serverElapsed;
    const target = Math.max(0,snapshot+elapsed);
    return broadcast.loop && broadcast.duration_ms > 0 ? target % broadcast.duration_ms : Math.min(target,broadcast.duration_ms);
  };
  useEffect(() => {
    if(!loaded || !follow || !broadcast || !player.current)return;
    const sync = () => { const element=player.current; if(!element)return; const target=targetPosition(); if(Math.abs(element.currentTime*1000-target)>500) element.currentTime=target/1000; if(broadcast.status === "playing"){element.playbackRate=1;setRate(1);void element.play().catch(()=>setFollow(false));}else element.pause(); };
    sync();const timer=setInterval(sync,500);return()=>clearInterval(timer);
    // Broadcast snapshots are identified by server time and playback position.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[broadcastKey,loaded,follow]);
  useEffect(() => {
    const element=player.current;
    if(!element || !loaded || !element.requestVideoFrameCallback)return;
    let callback=0; let active=true;
    const next: VideoFrameRequestCallback = (_now,metadata)=>{if(!active)return;setPosition(metadata.mediaTime*1000);callback=element.requestVideoFrameCallback(next);};
    callback=element.requestVideoFrameCallback(next);return()=>{active=false;element.cancelVideoFrameCallback(callback);};
  },[video.id,loaded]);
  const windowStart = Math.floor(position/10000)*10000;
  const tracks = useApi(() => api.GET("/api/videos/{video_id}/tracks", { params: { path: { video_id: video.id }, query: { from_ms: windowStart, to_ms: Math.min(windowStart+10000,video.duration_ms) } } }), [video.id, video.duration_ms,windowStart]);
  const tolerance = 1000 / Math.max(1, video.fps) * .51;
  const frame = tracks.data?.frames.find(frame => Math.abs(frame.ts_ms - position) <= tolerance);
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => { if ((event.target as HTMLElement)?.closest("input,textarea,select,[contenteditable=true]")) return; if (event.key.toLowerCase() === "h") setHud(value => !value); };
    window.addEventListener("keydown", onKey); return () => window.removeEventListener("keydown", onKey);
  }, []);
  useEffect(() => { setFailed(false); setLoaded(false); setPlaying(false); }, [video.id]);
  useEffect(() => { if(!follow && player.current?.readyState) { player.current.currentTime=initialMs/1000; setPosition(initialMs); } }, [video.id,initialMs,follow]);
  const seek = (ms: number) => { setFollow(false); if (player.current) player.current.currentTime = ms / 1000; setPosition(ms); };
  const togglePlay = async () => { setFollow(false); if (!player.current) return; if (playing) player.current.pause(); else { try { await player.current.play(); } catch { setFailed(true); } } };
  if (!video.browser_playable) return <Empty title="Формат записи не поддерживается" text={`Браузер не может воспроизвести ${video.codec}. Нужна совместимая запись.`} />;
  return <div className="recorded-player">
    <div className="video-frame" style={{ aspectRatio: `${video.width || 16}/${video.height || 9}`, "--media-ratio": (video.width || 16)/(video.height || 9) } as CSSProperties}>
      {!failed && <video data-testid="camera-video" ref={player} src={videoUrl(video.id)} preload="metadata" playsInline muted loop={Boolean(broadcast?.loop)} onLoadedMetadata={() => { setLoaded(true); if (player.current) player.current.currentTime = (broadcast ? targetPosition() : initialMs)/1000; }} onTimeUpdate={e => setPosition(e.currentTarget.currentTime * 1000)} onPlay={() => setPlaying(true)} onPause={() => setPlaying(false)} onEnded={() => setPlaying(false)} onError={() => setFailed(true)} />}
      {failed ? <Empty title="Запись не воспроизводится" text="Не удалось загрузить видео из источника. Кадр события доступен отдельно." /> : <>{hud && loaded && frame && <Hud objects={frame.objects} />}<span className="media-stamp">{camera}<b>{broadcast ? time(new Date(Date.parse(broadcast.started_at)+position).toISOString()) : duration(position)} · {duration(position)} / {duration(video.duration_ms)}</b></span><span className="media-source">{isReviewMode() ? "Синтетический повтор · статичный кадр" : "Воспроизведение архивной записи"}</span>{!playing && loaded && <button className="center-play" onClick={togglePlay} aria-label="Воспроизвести запись"><Icon name="play" size={30} /></button>}</>}
    </div>
    <div className="player-controls"><button className="icon-button" onClick={togglePlay} disabled={failed || !loaded} aria-label={playing ? "Пауза" : "Воспроизвести"}><Icon name={playing ? "pause" : "play"} /></button><button className="rate-button" onClick={() => { const next = rate === 1 ? 2 : rate === 2 ? .5 : 1; setFollow(false); setRate(next); if (player.current) player.current.playbackRate = next; }}>×{rate}</button><time>{duration(position)}<span> / {duration(video.duration_ms)}</span></time><button data-testid="hud-toggle" className={`hud-button ${hud ? "selected" : ""}`} aria-pressed={hud} onClick={() => setHud(v => !v)}><Icon name="eye" size={15} />HUD <kbd>H</kbd></button>{broadcast && <button className="sync-button" onClick={()=>setFollow(true)} disabled={follow}>{follow?"Позиция повтора":"К позиции повтора"}</button>}<span className="frame-status">{hud ? frame ? `Кадр ${frame.frame_idx}` : "HUD скрыт: нет совпадающего кадра" : "HUD выключен"}</span></div>
    <div className="timeline-wrap"><input className="video-seek" type="range" aria-label="Позиция записи" min={0} max={video.duration_ms} step={1000 / Math.max(1,video.fps)} value={Math.min(position,video.duration_ms)} onChange={e => seek(Number(e.target.value))} /><div className="episode-markers">{episodes.map(episode => <button key={episode.id} style={{left:`${episode.start_ms/video.duration_ms*100}%`,width:`${Math.max(1,(episode.end_ms-episode.start_ms)/video.duration_ms*100)}%`}} className={`episode-marker marker-${episode.level_max}`} aria-label={`${episode.scenario_title}, ${duration(episode.start_ms)}`} onClick={() => seek(episode.confirm_ms)} title={episode.reason_text} />)}</div><div className="timeline-labels"><span>00:00</span><span>{duration(video.duration_ms / 4)}</span><span>{duration(video.duration_ms / 2)}</span><span>{duration(video.duration_ms * .75)}</span><span>{duration(video.duration_ms)}</span></div></div>
    {tracks.error && <ErrorNotice error={tracks.error} compact retry={tracks.reload} />}
  </div>;
}
export function RecordedVideo({ videoId, camera, initialMs = 0, episodes, broadcast }: { videoId: number; camera: string; initialMs?: number; episodes?: Episode[]; broadcast?: Broadcast | null }) {
  const video = useApi(() => api.GET("/api/videos/{video_id}", {params:{path:{video_id:videoId}}}), [videoId]);
  return video.error ? <ErrorNotice error={video.error} retry={video.reload} /> : video.data ? <VideoWithHud video={video.data} camera={camera} initialMs={initialMs} episodes={episodes} broadcast={broadcast} /> : <div className="loading-state">Загружаем метаданные записи…</div>;
}
