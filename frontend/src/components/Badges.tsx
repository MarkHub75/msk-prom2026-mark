import type { components } from "../api/schema";
import { useMeta } from "./AppShell";

type Level = components["schemas"]["LevelMeta"]["id"];
type Status = components["schemas"]["StatusMeta"]["id"];

// Level is never shown by color alone: an icon and the title from /api/meta go with it.
const LEVEL_ICON: Record<Level, string> = { yellow: "▲", red: "■" };

export function LevelBadge({ level }: { level: Level }) {
  const title = useMeta()?.levels.find((l) => l.id === level)?.title ?? level;
  return (
    <span className={`badge badge-${level}`}>
      <span aria-hidden="true">{LEVEL_ICON[level]}</span>
      {title}
    </span>
  );
}

export function StatusBadge({ status }: { status: Status }) {
  const meta = useMeta()?.statuses.find((s) => s.id === status);
  return (
    <span className="badge">
      <span aria-hidden="true">{meta?.terminal ? "✓" : "●"}</span>
      {meta?.title ?? status}
    </span>
  );
}
