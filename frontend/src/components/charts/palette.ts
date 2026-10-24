// Chart colours (v2): the UI palette, muted. Levels keep their product meaning (warning = amber,
// critical = red, the same tokens as the interface); verdicts are steel blue / muted violet / grey.
// Every mark also has a legend or a written value, so colour is never the only key.
export const C = {
  yellow: "#C99A3A",
  red: "#D64545",
  confirmed: "#6B96C8",
  falseAlarm: "#8F88B6",
  noVerdict: "#4A4E57",
  trend: "#B9BEC6",
  master: "#8A909A",
  neutral: "#747B86",
} as const;

export interface Counts { count: number; confirmed: number; false_alarm: number }

export const verdictSegments = (r: Counts) => [
  { name: "Подтверждено", value: r.confirmed, color: C.confirmed },
  { name: "Ложное срабатывание", value: r.false_alarm, color: C.falseAlarm },
  { name: "Без вердикта", value: Math.max(0, r.count - r.confirmed - r.false_alarm), color: C.noVerdict },
];
