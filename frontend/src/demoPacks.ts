import type { DemoPack } from "./api/types";

// tech.md 8.19: the header and the IT screens name the pack and where its detections come from.
export function packSource(pack: Pick<DemoPack, "backend" | "fake">): string {
  if (pack.fake) return "фейк";
  return pack.backend === "linq" ? "детекции LinQ" : "детекции CPU (local)";
}

export function packLabel(pack: Pick<DemoPack, "name" | "backend" | "fake">): string {
  return `Демо-пакет ${pack.name}: ${packSource(pack)}`;
}

// A route that answers something else than a list (mock, older backend) counts as no packs.
export function packList(packs: unknown): DemoPack[] {
  return Array.isArray(packs) ? [...packs as DemoPack[]].sort((a, b) => b.imported_at.localeCompare(a.imported_at)) : [];
}

// The newest import first (the API lists them by imported_at).
export function latestPack(packs: unknown): DemoPack | undefined {
  return packList(packs)[0];
}
