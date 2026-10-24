import type { components } from "../api/schema";
import { useMeta } from "./AppShell";
import { Badge, type IconName, type Tone } from "./ui";

type Level = components["schemas"]["LevelMeta"]["id"];
type Status = components["schemas"]["StatusMeta"]["id"];
type State = components["schemas"]["SectorState"]["state"];

// Level is never shown by color alone: an icon and the title from /api/meta go with it.
const LEVEL: Record<Level, { icon: IconName; tone: Tone }> = { yellow: { icon: "alert", tone: "amber" }, red: { icon: "critical", tone: "red" } };

export function LevelBadge({ level, solid }: { level: Level; solid?: boolean }) {
  const title = useMeta()?.levels.find((l) => l.id === level)?.title ?? level;
  return <Badge tone={LEVEL[level].tone} icon={LEVEL[level].icon} solid={solid}>{title}</Badge>;
}

export function StatusBadge({ status }: { status: Status }) {
  const meta = useMeta()?.statuses.find((s) => s.id === status);
  const tone: Tone = status === "false_alarm" || status === "superseded" ? "grey" : meta?.terminal ? "green" : status === "new" ? "accent" : "neutral";
  return <Badge tone={tone} icon={meta?.terminal ? "ok" : status === "new" ? "bell" : "activity"}>{meta?.title ?? status}</Badge>;
}

const STATE: Record<State, { title: string; icon: IconName; tone: Tone }> = {
  red: { title: "Тревога", icon: "critical", tone: "red" },
  yellow: { title: "Внимание", icon: "alert", tone: "amber" },
  normal: { title: "Норма", icon: "ok", tone: "green" },
  no_observation: { title: "Нет наблюдения", icon: "no-observation", tone: "grey" },
};
/** Sector/camera observation state. «Нет наблюдения» is grey, never green: no alarms there does not mean safe. */
export function StateBadge({ state, text, solid }: { state: State; text?: string; solid?: boolean }) {
  const s = STATE[state];
  return <Badge tone={s.tone} icon={s.icon} solid={solid}>{text ?? s.title}</Badge>;
}
