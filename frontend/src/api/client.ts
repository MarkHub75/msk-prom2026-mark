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

// Multipart upload with progress: fetch has no upload progress, XMLHttpRequest does.
export function uploadVideo(
  cameraId: number,
  file: File,
  onProgress: (share: number) => void,
): Promise<{ data?: components["schemas"]["UploadResult"]; error?: ApiError }> {
  return new Promise((resolve) => {
    const xhr = new XMLHttpRequest();
    const base = import.meta.env.VITE_API_BASE || location.origin;
    xhr.open("POST", `${base}/api/cameras/${cameraId}/videos`);
    xhr.setRequestHeader("X-Role", getRole());
    xhr.upload.onprogress = (e) => e.lengthComputable && onProgress(e.loaded / e.total);
    xhr.onload = () => {
      const body: unknown = JSON.parse(xhr.responseText || "null");
      resolve(xhr.status < 300 ? { data: body as never } : { error: body as ApiError });
    };
    xhr.onerror = () => resolve({ error: { code: "network", message: "Сервер не отвечает" } as ApiError });
    const form = new FormData();
    form.append("file", file);
    xhr.send(form);
  });
}
