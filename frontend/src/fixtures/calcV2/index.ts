import type { ApiErrorExisting, DefaultsV2, ResultV2, RolloutRequestV2, ScaleRequestV2 } from "../../api/calcV2";
import defaults from "./defaults-v2.json";
import rolloutRequest from "./rollout-request.json";
import rolloutResult from "./rollout-result.json";
import scaleRequest from "./scale-request.json";
import scaleProjection from "./scale-result.projection.json";
import partialProjection from "./partial-hp-unknown.projection.json";
import error422 from "./error-422-activity-share.json";
import error422Format from "./error-422-format.json";
import error501Pdf from "./error-501-pdf.json";
import paybackGallery from "./payback-gallery.json";

// JSON examples of docs/CALCULATOR_CONTRACT_V2.md К14, copied as they are: for tests and screenshots only.
// К10 п.6: they never stand in for a live calculation on the screen.

/** К14.5 and К14.6 are projections: «the full answer has the same К5 schema as К14.3». Full = К14.3 with the projection on top. */
export function withProjection<T>(base: T, projection: unknown): T {
  if (Array.isArray(base) && Array.isArray(projection)) {
    return (projection.length === base.length ? projection.map((p, i) => withProjection(base[i], p)) : projection) as T;
  }
  if (base && projection && typeof base === "object" && typeof projection === "object" && !Array.isArray(projection)) {
    const out: Record<string, unknown> = { ...(base as Record<string, unknown>) };
    for (const [k, v] of Object.entries(projection)) out[k] = withProjection(out[k], v);
    return out as T;
  }
  return projection as T;
}

export const K14 = {
  defaults: defaults as DefaultsV2,
  rolloutRequest: rolloutRequest as RolloutRequestV2,
  rolloutResult: rolloutResult as ResultV2,
  scaleRequest: scaleRequest as ScaleRequestV2,
  scaleResult: withProjection(rolloutResult as ResultV2, scaleProjection),
  partialResult: withProjection(rolloutResult as ResultV2, partialProjection),
  error422: error422 as ApiErrorExisting,
  error422Format: error422Format as ApiErrorExisting,
  error501Pdf: error501Pdf as ApiErrorExisting,
  paybackGallery,
};
