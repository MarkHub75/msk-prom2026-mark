import createClient, { type Middleware } from "openapi-fetch";
import { getRole } from "../roles";
import type { components, paths } from "./schema";

export type ApiError = components["schemas"]["ApiError"];

const KEY_ACTOR = "safewatch.actor";

function actor(): string | null {
  try {
    return localStorage.getItem(KEY_ACTOR);
  } catch {
    return null;
  }
}

// Every request carries the role of the switcher; the server trusts it (no login in baseline).
const headers: Middleware = {
  onRequest({ request }) {
    request.headers.set("X-Role", getRole());
    const name = actor();
    if (name) request.headers.set("X-Actor", encodeURIComponent(name));
    return request;
  },
};

export const api = createClient<paths>({
  // Empty VITE_API_BASE: the same origin as the page (the backend serves frontend/dist).
  baseUrl: import.meta.env.VITE_API_BASE || location.origin,
  // Looked up on every call, so tests can stub the global fetch.
  fetch: (request) => globalThis.fetch(request),
});
api.use(headers);

export function apiError(e: unknown): { code: string; message: string } {
  if (e && typeof e === "object" && "code" in e && "message" in e) {
    const { code, message } = e as ApiError;
    return { code, message };
  }
  return { code: "network", message: "Сервер не отвечает" };
}
