import { api } from "./client";
import type { ResultV2, RolloutIn, RolloutRequestV2, RolloutResult, ScaleIn, ScaleRequestV2, ScaleResult } from "./types";

// The calculator POST answers a union (contract 1.2.0): `?format=` picks the variant, OpenAPI
// cannot tie the two. These wrappers pick the format and narrow the answer by its `format`
// discriminator; every number is the server's (docs/contracts/calculator_v2.md К1, К10).

export interface CalcAnswer<T> { data?: T; error?: unknown; response: Response }

export function isResultV2(value: unknown): value is ResultV2 {
  return typeof value === "object" && value !== null && (value as { format?: unknown }).format === "v2";
}

export async function rolloutLegacy(body: RolloutIn): Promise<CalcAnswer<RolloutResult>> {
  const r = await api.POST("/api/calculator/rollout", { body, params: { query: { format: "legacy" } } });
  return { error: r.error, response: r.response, data: r.data === undefined || isResultV2(r.data) ? undefined : r.data };
}

export async function scaleLegacy(body: ScaleIn): Promise<CalcAnswer<ScaleResult>> {
  const r = await api.POST("/api/calculator/scale", { body, params: { query: { format: "legacy" } } });
  return { error: r.error, response: r.response, data: r.data === undefined || isResultV2(r.data) ? undefined : r.data };
}

export async function rolloutV2(body: RolloutRequestV2): Promise<CalcAnswer<ResultV2>> {
  const r = await api.POST("/api/calculator/rollout", { body, params: { query: { format: "v2" } } });
  return { error: r.error, response: r.response, data: isResultV2(r.data) ? r.data : undefined };
}

export async function scaleV2(body: ScaleRequestV2): Promise<CalcAnswer<ResultV2>> {
  const r = await api.POST("/api/calculator/scale", { body, params: { query: { format: "v2" } } });
  return { error: r.error, response: r.response, data: isResultV2(r.data) ? r.data : undefined };
}
