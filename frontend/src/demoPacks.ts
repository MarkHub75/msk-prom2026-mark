import type { DemoPack } from "./api/types";

// tech.md 8.19: the header and the IT screens name the pack and where its detections come from.
export function packSource(pack: Pick<DemoPack, "backend" | "fake">): string {
  if (pack.fake) return "фейк";
  return pack.backend === "linq" ? "детекции LinQ" : "детекции CPU (local)";
}

export function packLabel(pack: Pick<DemoPack, "name" | "backend" | "fake">): string {
  return `Демо-пакет ${pack.name}: ${packSource(pack)}`;
}

// The newest import first (the API lists them by imported_at).
export function latestPack(packs: DemoPack[] | undefined): DemoPack | undefined {
  return [...(packs ?? [])].sort((a, b) => b.imported_at.localeCompare(a.imported_at))[0];
}
