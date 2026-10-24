// Chart colours (design reference of 24.10): series cyan / violet, semantic warning / critical / resolved.
// Levels keep their product meaning (warning = yellow, critical = red); verdicts are cyan / violet / grey.
// Checked with the dataviz validator on surface #232323: adjacent CVD separation passes (ΔE ≥ 13.8);
// the hues are lighter than its band by design, every mark also has a legend or a written value.
export const C = {
  yellow: "#FFB65C",
  red: "#FF5D65",
  confirmed: "#55D6F5",
  falseAlarm: "#A38BFF",
  noVerdict: "#5b616b",
  trend: "#c9ced6",
  master: "#43D6A6",
  neutral: "#78818E",
} as const;

export interface Counts { count: number; confirmed: number; false_alarm: number }

export const verdictSegments = (r: Counts) => [
  { name: "Подтверждено", value: r.confirmed, color: C.confirmed },
  { name: "Ложное срабатывание", value: r.false_alarm, color: C.falseAlarm },
  { name: "Без вердикта", value: Math.max(0, r.count - r.confirmed - r.false_alarm), color: C.noVerdict },
];
