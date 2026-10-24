import createClient, { type Middleware } from "openapi-fetch";
import { getRole } from "../roles";
import type { components, paths } from "./schema";
import { isReviewMode, reviewFetch, reviewMediaUrl } from "../fixtures/review";

export { getReviewScenario, isReviewMode, resetReview } from "../fixtures/review";

export type ApiError = components["schemas"]["ApiError"];

const KEY_ACTOR = "safewatch.actor";

export function getActor(): string {
  try {
    return localStorage.getItem(KEY_ACTOR) || (getRole() === "master" ? "Мастер смены" : "Оператор");
  } catch {
    return getRole() === "master" ? "Мастер смены" : "Оператор";
  }
}
export function setActor(value: string): void {
  try { if (value.trim()) localStorage.setItem(KEY_ACTOR, value.trim()); else localStorage.removeItem(KEY_ACTOR); } catch { /* Storage may be disabled. */ }
}

// Every request carries the role of the switcher; the server trusts it (no login in baseline).
const headers: Middleware = {
  onRequest({ request }) {
    request.headers.set("X-Role", getRole());
    const name = getActor();
    if (name) request.headers.set("X-Actor", encodeURIComponent(name));
    return request;
  },
};

export const api = createClient<paths>({
  // Empty VITE_API_BASE: the same origin as the page (the backend serves frontend/dist).
  baseUrl: import.meta.env.VITE_API_BASE || location.origin,
  // Looked up on every call, so tests can stub the global fetch.
  fetch: (request) => isReviewMode() ? reviewFetch(request) : globalThis.fetch(request),
});
api.use(headers);

export interface ApiFailure { code: string; message: string; status?: number; details?: ApiError["details"] }
export function apiError(e: unknown): ApiFailure {
  if (e && typeof e === "object" && "code" in e && "message" in e) {
    const { code, message, details, status } = e as ApiError & {status?: number};
    if (typeof code === "string" && typeof message === "string") return {code, message, ...(details ? {details} : {}), ...(status ? {status} : {})};
  }
  return { code: "network", message: "Сервер не отвечает" };
}

export function mediaUrl(url: string): string {
  if (isReviewMode()) return reviewMediaUrl(url);
  return new URL(url, import.meta.env.VITE_API_BASE || location.origin).toString();
}
export const resolveMediaUrl = mediaUrl;
export function videoUrl(videoId: number): string { return mediaUrl(`/api/videos/${videoId}/file`); }
