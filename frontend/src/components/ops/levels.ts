import { useMeta } from "../AppShell";

type Level = "red" | "yellow";
// Fallback only until /api/meta arrives; the same titles the backend sends in meta.levels.
const FALLBACK: Record<Level, string> = { red: "Красная опасность", yellow: "Жёлтая опасность" };

/** Level title from /api/meta levels (one wording on every screen). */
export function useLevelTitle(): (level: Level) => string {
  const levels = useMeta()?.levels;
  return (level) => levels?.find((item) => item.id === level)?.title ?? FALLBACK[level];
}
