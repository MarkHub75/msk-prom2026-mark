import { useEffect, useRef, useState } from "react";
import { useRole } from "../roles";
import { getReviewScenario, subscribeFixtureMessages } from "../fixtures/review";
import schemaText from "./ws.schema.generated.json?raw";
import type { WsMessage } from "./types";

export type { WsMessage } from "./types";
export type WsStatus = "connecting" | "connected" | "disconnected" | "fixture";
const BACKOFF_S = [1, 2, 4, 8];
type JsonSchema = Record<string, unknown>;
const schema = JSON.parse(schemaText) as JsonSchema;
const definitions = schema.$defs as Record<string, JsonSchema>;
const payloadDefinitions: Record<WsMessage["type"], string> = {
  hello: "WsHello", "event.created": "EventSummary", "event.updated": "EventSummary", "event.escalated": "EventSummary",
  notification: "Notification", "camera.state": "CameraState", "sector.state": "SectorState", "job.progress": "Job",
  "broadcast.state": "Broadcast", "backend.status": "BackendStatus",
};

// Bundle the real schema unchanged; ignore malformed/unknown messages safely.
function matches(value: unknown, rule: JsonSchema): boolean {
  if (typeof rule.$ref === "string") return matches(value, definitions[rule.$ref.split("/").pop()!] ?? {});
  if (Array.isArray(rule.anyOf) && !rule.anyOf.some((item) => matches(value, item as JsonSchema))) return false;
  if (Array.isArray(rule.enum) && !rule.enum.includes(value)) return false;
  if ("const" in rule && rule.const !== value) return false;
  if (rule.type === "null") return value === null;
  if (rule.type === "string") {
    if (typeof value !== "string") return false;
    if (rule.format === "date-time" && !Number.isFinite(Date.parse(value))) return false;
  }
  if (rule.type === "number" && (typeof value !== "number" || !Number.isFinite(value))) return false;
  if (rule.type === "integer" && (typeof value !== "number" || !Number.isInteger(value))) return false;
  if (rule.type === "boolean" && typeof value !== "boolean") return false;
  if (rule.type === "array") {
    if (!Array.isArray(value)) return false;
    if (typeof rule.minItems === "number" && value.length < rule.minItems) return false;
    if (typeof rule.maxItems === "number" && value.length > rule.maxItems) return false;
    if (Array.isArray(rule.prefixItems) && !rule.prefixItems.every((item, index) => matches(value[index], item as JsonSchema))) return false;
    if (rule.items && typeof rule.items === "object" && !value.every((item) => matches(item, rule.items as JsonSchema))) return false;
  }
  if (rule.type === "object") {
    if (!value || typeof value !== "object" || Array.isArray(value)) return false;
    const object = value as Record<string, unknown>;
    if (Array.isArray(rule.required) && !rule.required.every((key) => typeof key === "string" && key in object)) return false;
    const properties = (rule.properties ?? {}) as Record<string, JsonSchema>;
    for (const [key, item] of Object.entries(object)) {
      if (properties[key] && !matches(item, properties[key])) return false;
      if (!properties[key] && rule.additionalProperties === false) return false;
      if (!properties[key] && rule.additionalProperties && typeof rule.additionalProperties === "object" && !matches(item, rule.additionalProperties as JsonSchema)) return false;
    }
  }
  return true;
}

export function parseWsMessage(payload: unknown): WsMessage | null {
  try {
    const parsed: unknown = typeof payload === "string" ? JSON.parse(payload) : payload;
    if (!matches(parsed, schema)) return null;
    const envelope = parsed as {type: WsMessage["type"]; data: unknown};
    const definition = payloadDefinitions[envelope.type];
    if (!definition || !matches(envelope.data, definitions[definition])) return null;
    return parsed as WsMessage;
  } catch { return null; }
}

export function wsUrl(role: string): string {
  const base =
    import.meta.env.VITE_WS_URL ||
    `${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws`;
  const url = new URL(base, location.href);
  url.searchParams.set("role", role);
  return url.toString();
}

// One connection per hook/role. Explicit review fixtures never create WebSockets.
export function useWs(handler: (message: WsMessage) => void): {status: WsStatus} {
  const [role] = useRole();
  const scenario = getReviewScenario();
  const latest = useRef(handler);
  latest.current = handler;
  const [status, setStatus] = useState<WsStatus>(() => scenario === "offline" || scenario === "disconnected" ? "disconnected" : scenario ? "fixture" : "connecting");
  useEffect(() => {
    if (scenario) {
      setStatus(scenario === "offline" || scenario === "disconnected" ? "disconnected" : "fixture");
      if (scenario === "offline" || scenario === "disconnected") return;
      return subscribeFixtureMessages((message) => latest.current(message), role);
    }
    let socket: WebSocket | undefined;
    let attempt = 0;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let closed = false;

    const retry = () => {
      if (closed) return;
      setStatus("disconnected");
      const delay = BACKOFF_S[Math.min(attempt, BACKOFF_S.length - 1)];
      attempt += 1;
      timer = setTimeout(open, delay * 1000);
    };
    const open = () => {
      if (closed) return;
      setStatus("connecting");
      try { socket = new WebSocket(wsUrl(role)); } catch { retry(); return; }
      socket.onopen = () => {
        if (!closed) { attempt = 0; setStatus("connected"); }
      };
      socket.onmessage = (event) => {
        const message = parseWsMessage(event.data);
        if (!closed && message) latest.current(message);
      };
      socket.onerror = () => { if (!closed) setStatus("disconnected"); };
      socket.onclose = (event) => {
        if (closed) return;
        if (event.code === 4400) { setStatus("disconnected"); return; }
        retry();
      };
    };
    open();
    return () => {
      closed = true;
      clearTimeout(timer);
      socket?.close();
    };
  }, [role, scenario]);
  return {status};
}
