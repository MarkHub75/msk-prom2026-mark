import { useEffect, useRef, useState } from "react";
import { apiError, getActor, type ApiFailure } from "../../api/client";
import { getRole } from "../../roles";
import type { DefaultsV2, Mode, ResultV2, RolloutRequestV2, ScaleRequestV2 } from "../../api/calcV2";

// docs/CALCULATOR_CONTRACT_V2.md К2: the v2 JSON is chosen by the query (?format=v2), never by guessing from fields.
// Not through openapi-fetch: schema.d.ts is still 1.1.0 and has no v2 bodies (OpenAPI 1.2.0 comes with the backend).

/** GET /api/calculator/defaults carries `v2: DefaultsV2` from contract 2.0.0 on; without it the legacy screen stays. */
export function defaultsV2(data: unknown): DefaultsV2 | undefined {
  const v2 = (data as { v2?: unknown } | undefined)?.v2 as Partial<DefaultsV2> | undefined;
  return v2 && v2.format === "v2" ? v2 as DefaultsV2 : undefined;
}

export type RequestV2 = RolloutRequestV2 | ScaleRequestV2;

async function post(mode: Mode, body: RequestV2): Promise<{ data?: ResultV2; error?: ApiFailure }> {
  const base = import.meta.env.VITE_API_BASE || location.origin;
  const headers: Record<string, string> = { "Content-Type": "application/json", "X-Role": getRole() };
  const actor = getActor();
  if (actor) headers["X-Actor"] = encodeURIComponent(actor);
  const response = await globalThis.fetch(new Request(new URL(`/api/calculator/${mode}?format=v2`, base), { method: "POST", headers, body: JSON.stringify(body) }));
  const json: unknown = await response.json().catch(() => undefined);
  if (!response.ok) return { error: { ...apiError(json), status: response.status } };
  return { data: json as ResultV2 };
}

export interface CalcV2State {
  /** Last answer of this mode; while `busy` it is the previous result, shown with a mark. */
  result?: ResultV2;
  error?: ApiFailure;
  /** details.field of a 422, e.g. `load.activity_share` (К10: no `body.` prefix). */
  field?: string;
  busy: boolean;
}

/**
 * Debounced POST of the current body (К10 п.4): the previous result stays on screen while the next one runs,
 * and only the answer to the latest request is applied — a late answer of an older request is dropped.
 */
export function useCalcV2(mode: Mode, body: RequestV2, ready: boolean, delayMs = 350): CalcV2State {
  const [state, setState] = useState<CalcV2State>({ busy: false });
  const seq = useRef(0);
  const key = JSON.stringify(body);
  useEffect(() => {
    // An input became invalid before the timer fired: nothing is sent, so nothing is recounting.
    if (!ready) { setState(st => (st.busy ? { ...st, busy: false } : st)); return; }
    // No AbortController: the sequence number alone decides which answer is applied (and jsdom signals break Request).
    const id = ++seq.current;
    setState(s => ({ ...s, busy: true }));
    const timer = setTimeout(() => {
      post(mode, JSON.parse(key) as RequestV2)
        .then(r => {
          if (id !== seq.current) return;
          if (r.error) {
            const field = r.error.code === "validation" && typeof r.error.details?.field === "string" ? r.error.details.field : undefined;
            setState(s => ({ result: s.result, error: r.error, field, busy: false }));
          } else setState({ result: r.data, busy: false });
        })
        .catch((e: unknown) => {
          if (id !== seq.current) return;
          setState(s => ({ result: s.result, error: apiError(e), busy: false }));
        });
    }, delayMs);
    return () => clearTimeout(timer);
  }, [mode, key, ready, delayMs]);
  return state;
}
