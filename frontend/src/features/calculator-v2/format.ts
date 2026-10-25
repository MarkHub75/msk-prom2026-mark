import type { NumberStatus, ResultStatus } from "../../api/calcV2";

// К10 п.5: null is «нужно значение / нет данных / неприменимо» by its reason; a zero is a known zero.
const rubFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });
const numFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 2 });
const oneFmt = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 1 });

export function nullText(status?: NumberStatus | null): string {
  if (status === "missing") return "нужно значение";
  if (status === "not_applicable") return "неприменимо";
  return "нет данных";
}

export const rub = (v: number | null | undefined, status?: NumberStatus | null) => v === null || v === undefined ? nullText(status) : `${rubFmt.format(v)} ₽`;
export const num = (v: number | null | undefined, status?: NumberStatus | null) => v === null || v === undefined ? nullText(status) : numFmt.format(v);
export const one = (v: number) => oneFmt.format(v);
export const isNull = (v: unknown): v is null | undefined => v === null || v === undefined;

export function months(v: number): string {
  const text = `${oneFmt.format(v)} мес.`;
  return v >= 24 ? `${text} · ${oneFmt.format(v / 12)} г.` : text;
}

export const STATUS: Record<ResultStatus, { title: string; text: string; tone: "neutral" | "amber" | "grey" }> = {
  ready: { title: "Расчёт полный", text: "Все входы известны; это расчёт, а не обещание предотвратить травмы.", tone: "neutral" },
  estimated: { title: "Оценка на допущениях", text: "Расчёт полный, но опирается на допущения команды и заявления производителя.", tone: "neutral" },
  partial: { title: "Неполный расчёт", text: "Части входов не хватает: известное посчитано, недоступные итоги показаны как «нужно значение».", tone: "amber" },
  empty: { title: "Нет проекта", text: "Камер в расчёте нет: покупки нет, итоги нулевые.", tone: "grey" },
};

/** `n` boards in Russian: 1 плата, 3 платы, 16 плат. */
export function boards(n: number): string {
  const m10 = n % 10, m100 = n % 100;
  const word = m10 === 1 && m100 !== 11 ? "плата" : m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14) ? "платы" : "плат";
  return `${n} ${word}`;
}
