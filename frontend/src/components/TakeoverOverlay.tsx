import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import type { components } from "../api/schema";
import { useWs } from "../api/ws";
import { playSound } from "./sound";

type Notification = components["schemas"]["Notification"];

// A red notification takes the whole screen with a siren until the operator opens the event.
export function TakeoverOverlay() {
  const [note, setNote] = useState<Notification>();
  const stop = useRef<() => void>(() => undefined);
  const navigate = useNavigate();
  useWs((message) => {
    if (message.type !== "notification") return;
    const data = message.data as Notification;
    if (!data.takeover) return;
    stop.current();
    stop.current = playSound(data.sound);
    setNote(data);
  });
  useEffect(() => () => stop.current(), []);
  if (!note) return null;
  const open = () => {
    stop.current();
    setNote(undefined);
    navigate(`/events/${note.event_id}?takeover=1`);
  };
  return (
    <div className="takeover" role="alertdialog" aria-label="Красная опасность">
      <p className="takeover-text">■ {note.text}</p>
      <button type="button" onClick={open}>
        Открыть событие
      </button>
    </div>
  );
}
