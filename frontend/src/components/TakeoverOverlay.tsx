import { useNavigate } from "react-router-dom";
import { useWs, type WsNotification } from "../api/ws";

// A red notification opens its event on the whole screen; the event screen in takeover mode
// sounds the siren until an action or «Свернуть» (tech.md 8.14).
export function TakeoverOverlay() {
  const navigate = useNavigate();
  useWs((message) => {
    if (message.type !== "notification") return;
    const data = message.data as WsNotification;
    if (data.takeover) navigate(`/events/${data.event_id}?takeover=1`);
  });
  return null;
}
