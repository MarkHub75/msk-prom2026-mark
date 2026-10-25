import { apiError, type ApiFailure } from "./client";

type BlobCall = () => Promise<{ data?: Blob; error?: unknown; response: Response }>;

/** File name from `Content-Disposition: attachment; filename="…"`, else the fallback. */
export function fileName(header: string | null, fallback: string): string {
  const star = /filename\*=UTF-8''([^;]+)/i.exec(header ?? "")?.[1];
  if (star) return decodeURIComponent(star);
  return /filename="?([^";]+)"?/i.exec(header ?? "")?.[1] ?? fallback;
}

// Downloads go through api.GET (role headers, the same 501/422 as every other call) instead of a bare
// <a href>: an unimplemented route must show its error, not save the JSON of the error as a file.
export async function saveDownload(call: BlobCall, fallback: string): Promise<ApiFailure | undefined> {
  try {
    const result = await call();
    if (result.error !== undefined || !result.data) return { ...apiError(result.error), status: result.response.status };
    const url = URL.createObjectURL(result.data);
    const link = document.createElement("a");
    link.href = url;
    link.download = fileName(result.response.headers.get("Content-Disposition"), fallback);
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
    return undefined;
  } catch (e) {
    return apiError(e);
  }
}
