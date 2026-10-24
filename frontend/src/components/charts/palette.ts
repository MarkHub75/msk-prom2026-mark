// Chart colours for the dark theme. Levels keep their product meaning (amber = yellow, red = red);
// verdicts are blue / light grey / dark grey so they never impersonate a level.
// Validated with the dataviz validator on surface #232323 (lightness band, CVD separation, contrast).
export const C = {
  yellow: "#e8a33d",
  red: "#e5484d",
  confirmed: "#3987e5",
  falseAlarm: "#9a9a9a",
  noVerdict: "#4a4a4a",
  trend: "#d9d9d9",
  master: "#9085e9",
  neutral: "#6f8193",
} as const;

export interface Counts { count: number; confirmed: number; false_alarm: number }

export const verdictSegments = (r: Counts) => [
  { name: "Подтверждено", value: r.confirmed, color: C.confirmed },
  { name: "Ложное срабатывание", value: r.false_alarm, color: C.falseAlarm },
  { name: "Без вердикта", value: Math.max(0, r.count - r.confirmed - r.false_alarm), color: C.noVerdict },
];
