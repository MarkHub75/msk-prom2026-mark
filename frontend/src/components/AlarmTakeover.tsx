import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";
import "../styles/takeover-media.css";
import { Link, useSearchParams } from "react-router-dom";
import type { EventSummary } from "../api/types";
import { Icon, number, time } from "./ui";

export interface TakeoverAction { id: string; title: string; key?: string; danger?: boolean }
interface ActProps { actions?: TakeoverAction[]; busy?: string | null | false; onAct?: (id: string) => void; media?: ReactNode }

function Takeover({ event, close, actions = [], busy, onAct, media }: { event: EventSummary; close: () => void } & ActProps) {
  const dialog = useRef<HTMLElement>(null);
  useEffect(() => { const previous = document.activeElement as HTMLElement | null; dialog.current?.querySelector<HTMLButtonElement>("button")?.focus(); const keys = (e: KeyboardEvent) => { if(e.key === "Escape") close(); if(e.key !== "Tab") return; const items=dialog.current?.querySelectorAll<HTMLElement>("button,a[href]"); if(!items?.length)return; const first=items[0],last=items[items.length-1]; if(e.shiftKey && document.activeElement === first){e.preventDefault();last.focus();}else if(!e.shiftKey && document.activeElement === last){e.preventDefault();first.focus();} }; document.addEventListener("keydown",keys); return () => { document.removeEventListener("keydown",keys); previous?.focus(); }; }, [close]);
  const [sound, setSound] = useState(false);
  const audio = useRef<AudioContext>();
  const timer = useRef<ReturnType<typeof setInterval>>();
  useEffect(() => () => { clearInterval(timer.current); void audio.current?.close(); }, []);
  const toggle = () => {
    if (sound) { clearInterval(timer.current); void audio.current?.suspend(); setSound(false); return; }
    const ctx = audio.current ?? new AudioContext(); audio.current = ctx; void ctx.resume();
    const tone = () => { const osc = ctx.createOscillator(); const gain = ctx.createGain(); osc.connect(gain); gain.connect(ctx.destination); osc.frequency.value = 640; gain.gain.value = .07; osc.start(); gain.gain.exponentialRampToValueAtTime(.001,ctx.currentTime+.45); osc.stop(ctx.currentTime+.5); };
    tone(); timer.current = setInterval(tone,1600); setSound(true);
  };
  // The operator decides looking at the evidence: the frame with its box sits inside the siren screen.
  const frame = media ?? (event.evidence_url ? <img className="takeover-img" src={event.evidence_url} alt={`Кадр события: ${event.title}`} /> : null);
  return <section ref={dialog} className={`takeover ${frame ? "has-media" : ""}`} role="alertdialog" aria-modal="true" aria-label="Критическое событие"><div className="takeover-top"><span>Критическое событие / #{event.id}</span><button onClick={close} className="button">Свернуть <Icon name="cross" size={16} /></button></div>{frame && <div className="takeover-media">{frame}</div>}<div className="takeover-side"><div className="takeover-body"><span className="takeover-sector">{number(event.sector_id)}</span><div><div className="takeover-location">{event.sector_name} / {event.camera_name} · {time(event.started_at)}</div><h2>{event.title}</h2><p>{event.reason_text}</p></div></div><div className="takeover-actions">{onAct && actions.map(a => <button key={a.id} data-action={a.id} disabled={Boolean(busy)} onClick={() => onAct(a.id)} className={`button ${a.danger ? "button-danger" : ""}`}>{busy === a.id ? "Сохраняем…" : a.title}{a.key && <kbd>{a.key}</kbd>}</button>)}<button onClick={toggle} className="button"><Icon name={sound ? "mute" : "sound"} />{sound ? "Выключить звук" : "Включить звуковой сигнал"}</button><Link className="button button-light" to={`/events/${event.id}`} onClick={close}>Открыть карточку события <Icon name="arrow" /></Link></div></div></section>;
}
// The siren screen stays until the operator acts on the event (status leaves new/viewed) or presses «Свернуть».
export function EventAlarm({event, ...act}:{event?:EventSummary} & ActProps) {
  const [query] = useSearchParams(); const [collapsed,setCollapsed]=useState(false);
  const close=useCallback(()=>setCollapsed(true),[]);
  useEffect(()=>setCollapsed(false),[event?.id]);
  if(query.get("takeover")!=="1" || event?.level!=="red" || (event.status!=="new" && event.status!=="viewed"))return null;
  return collapsed ? <button className="collapsed-alarm" onClick={()=>setCollapsed(false)}>Критическое событие #{event.id}<Icon name="arrow" /></button> : <Takeover event={event} close={close} {...act} />;
}
