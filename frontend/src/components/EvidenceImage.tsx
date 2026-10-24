import { apiUrl } from "../api/client";
import type { components } from "../api/schema";

type Evidence = components["schemas"]["Evidence"];

const pct = (v: number) => `${(v * 100).toFixed(2)}%`;

// The evidence JPEG has no boxes drawn in (tech.md 16, slice 5): the boxes of its frame come along
// and are laid over the image with a callout of each object.
export function EvidenceImage({ evidence, hudVisible }: { evidence: Evidence; hudVisible: boolean }) {
  const people = evidence.objects.filter((o) => o.kind === "person").length;
  return (
    <figure className="evidence">
      <div className="evidence-frame">
        <img src={apiUrl(evidence.url)} alt={`Кадр ${evidence.kind === "confirm" ? "подтверждения" : "эскалации"}`} width={240} />
        {hudVisible &&
          evidence.objects.map((o, i) => {
            const [x1, y1, x2, y2] = o.bbox;
            const style = { left: pct(x1), top: pct(y1), width: pct(x2 - x1), height: pct(y2 - y1) };
            return (
              <div key={i} className="evidence-box" style={style}>
                <span className="evidence-callout">{[o.label, ...o.tags.map((t) => t.text)].join(" · ")}</span>
              </div>
            );
          })}
      </div>
      {hudVisible && <figcaption>{`${(evidence.ts_ms / 1000).toFixed(1)} с, объектов: ${evidence.objects.length}, людей: ${people}`}</figcaption>}
    </figure>
  );
}
