import { getActor } from "./client";
import { getRole } from "../roles";
import type { ApiFailure } from "./client";
import type { Schemas } from "./types";

export type UploadResult = Schemas["UploadResult"];
export interface UploadProgress { loaded: number; total: number }

// POST /api/cameras/{id}/videos as multipart with upload progress (fetch has no upload progress).
// Same headers as the openapi-fetch client: X-Role and X-Actor.
export function uploadVideo(cameraId: number, file: File, onProgress: (p: UploadProgress) => void): { done: Promise<{ data?: UploadResult; error?: ApiFailure }>; abort: () => void } {
  const xhr = new XMLHttpRequest();
  const done = new Promise<{ data?: UploadResult; error?: ApiFailure }>((resolve) => {
    const base = import.meta.env.VITE_API_BASE || location.origin;
    xhr.open("POST", new URL(`/api/cameras/${cameraId}/videos`, base).toString());
    xhr.setRequestHeader("X-Role", getRole());
    const actor = getActor();
    if (actor) xhr.setRequestHeader("X-Actor", encodeURIComponent(actor));
    xhr.upload.onprogress = (e) => { if (e.lengthComputable) onProgress({ loaded: e.loaded, total: e.total }); };
    xhr.onload = () => {
      let body: unknown = null;
      try { body = JSON.parse(xhr.responseText || "null"); } catch { /* not JSON */ }
      if (xhr.status >= 200 && xhr.status < 300) { resolve({ data: body as UploadResult }); return; }
      const e = body as Partial<ApiFailure> | null;
      resolve({ error: { code: typeof e?.code === "string" ? e.code : `http_${xhr.status}`, message: typeof e?.message === "string" ? e.message : `Сервер ответил ${xhr.status}`, status: xhr.status, ...(e?.details ? { details: e.details } : {}) } });
    };
    xhr.onerror = () => resolve({ error: { code: "network", message: "Сервер не отвечает" } });
    xhr.onabort = () => resolve({ error: { code: "aborted", message: "Загрузка отменена" } });
    const form = new FormData();
    form.append("file", file);
    xhr.send(form);
  });
  return { done, abort: () => xhr.abort() };
}
