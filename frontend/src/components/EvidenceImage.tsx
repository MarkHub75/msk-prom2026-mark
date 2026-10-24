import { apiUrl } from "../api/client";
import type { components } from "../api/schema";

type Evidence = components["schemas"]["Evidence"];

// The evidence JPEG has no boxes drawn in (tech.md 16, slice 5): the boxes of its frame come along.
export function EvidenceImage({ evidence, hudVisible }: { evidence: Evidence; hudVisible: boolean }) {
  const people = evidence.objects.filter((o) => o.kind === "person").length;
  return (
    <figure className="evidence">
      <img src={apiUrl(evidence.url)} alt={`Кадр ${evidence.kind === "confirm" ? "подтверждения" : "эскалации"}`} width={240} />
      {hudVisible && <figcaption>{`${(evidence.ts_ms / 1000).toFixed(1)} с, объектов: ${evidence.objects.length}, людей: ${people}`}</figcaption>}
    </figure>
  );
}
