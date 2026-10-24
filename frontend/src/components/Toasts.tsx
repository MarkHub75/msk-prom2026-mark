import { useState } from "react";
import { Link } from "react-router-dom";
import type { components } from "../api/schema";
import { useWs } from "../api/ws";
import { LevelBadge } from "./Badges";
import { playSound } from "./sound";

type Notification = components["schemas"]["Notification"];

const SHOW_MS = 10_000;

// Notifications without a screen takeover (yellow for the operator): a toast with a chime.
export function Toasts() {
  const [items, setItems] = useState<Notification[]>([]);
  useWs((message) => {
    if (message.type !== "notification") return;
    const note = message.data as Notification;
    if (note.takeover) return;
    playSound(note.sound);
    setItems((list) => [...list.filter((n) => n.id !== note.id), note]);
    setTimeout(() => setItems((list) => list.filter((n) => n.id !== note.id)), SHOW_MS);
  });
  if (items.length === 0) return null;
  return (
    <div className="toasts" role="status">
      {items.map((n) => (
        <Link key={n.id} className="toast" to={`/events/${n.event_id}`}>
          <LevelBadge level={n.level} /> {n.text}
        </Link>
      ))}
    </div>
  );
}
