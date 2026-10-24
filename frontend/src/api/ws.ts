import { useEffect, useRef } from "react";
import { useRole } from "../roles";
// contract/ws.schema.json describes `data` per type; screens narrow it by `type`.
export interface WsMessage {
  type: string;
  at: string;
  data: unknown;
}

const BACKOFF_S = [1, 2, 4, 8];

function wsUrl(role: string): string {
  const base =
    import.meta.env.VITE_WS_URL ||
    `${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws`;
  return `${base}?role=${role}`;
}

// One connection per role; reconnects after 1, 2, 4, 8 s (then every 8 s).
export function useWs(handler: (message: WsMessage) => void): void {
  const [role] = useRole();
  const latest = useRef(handler);
  latest.current = handler;

  useEffect(() => {
    let socket: WebSocket | undefined;
    let attempt = 0;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let closed = false;

    const open = () => {
      socket = new WebSocket(wsUrl(role));
      socket.onopen = () => {
        attempt = 0;
      };
      socket.onmessage = (event) => latest.current(JSON.parse(String(event.data)) as WsMessage);
      socket.onclose = () => {
        if (closed) return;
        const delay = BACKOFF_S[Math.min(attempt, BACKOFF_S.length - 1)];
        attempt += 1;
        timer = setTimeout(open, delay * 1000);
      };
    };
    open();
    return () => {
      closed = true;
      clearTimeout(timer);
      socket?.close();
    };
  }, [role]);
}
