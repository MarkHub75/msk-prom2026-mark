import type { CalcAssumption, TierResult } from "../api/types";
import { Badge, Panel } from "../components/ui";

// docs/ECONOMICS_SOURCES.md: industry injury rate, market prices and fines next to the calculator.
// Break-even is arithmetic on the server's answer only (capex, opex, reduction); nothing new is assumed.

/** Пострадавшие на 1000 работающих в год, обрабатывающая промышленность (Росстат, 7-травматизм, данные 2025). */
export const INDUSTRY_RATE = 1.17;
export const HORIZON_YEARS = 3;

const n2 = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 2 });
const n0 = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });
const rub = (v: number) => `${n0.format(v)} ₽`;

export function industryHint(workers: number | undefined): string {
  const people = workers && workers > 0 ? workers : 200;
  return `Среднее по обрабатывающей промышленности — 1,17 на 1000 работников (Росстат, 2025): для ${n0.format(people)} человек ≈ ${n2.format(Math.round(people * INDUSTRY_RATE / 10) / 100)}`;
}

export interface BreakEven {
  /** Savings per year that pay the capex back in HORIZON_YEARS: capex / 3 + opex. */
  needRub: number;
  /** Incidents per year needed at the entered incident cost. */
  incidents: number | null;
  /** Incident cost needed at the entered incidents per year. */
  cost: number | null;
  met: boolean;
}

/** Reduction share of the tier from the answer's assumptions; else savings / (incidents × cost). */
export function tierReduction(tier: TierResult, assumptions: CalcAssumption[], incidents: number | undefined, cost: number): number | null {
  const listed = assumptions.find(a => a.key === `reduction.${tier.tier}`)?.value;
  if (listed !== undefined) return listed;
  return incidents && cost ? tier.savings_rub_year / (incidents * cost) : null;
}

export function breakEven(tier: TierResult, reduction: number | null, incidents: number | undefined, cost: number): BreakEven {
  const needRub = tier.capex_rub / HORIZON_YEARS + tier.opex_rub_year;
  return {
    needRub,
    incidents: reduction && cost ? needRub / (cost * reduction) : null,
    cost: reduction && incidents ? needRub / (incidents * reduction) : null,
    met: tier.savings_rub_year >= needRub,
  };
}

export function BreakEvenPanel({ tiers, assumptions, incidents, workers, cost }: { tiers: TierResult[]; assumptions: CalcAssumption[]; incidents?: number; workers?: number; cost: number }) {
  const average = workers ? workers * INDUSTRY_RATE / 1000 : undefined;
  return <Panel title="Точка безубыточности" tools={<span className="v5-muted">окупаемость за {HORIZON_YEARS} года · расчёт от ваших допущений</span>} flush data-testid="break-even">
    <table className="ds-table v5-breakeven">
      <thead><tr><th>Уровень</th><th className="num">Нужна экономия в год</th><th className="num">Инцидентов в год при цене {rub(cost)}</th><th className="num">Или цена инцидента при {incidents === undefined ? "—" : n2.format(incidents)} в год</th><th /></tr></thead>
      <tbody>{tiers.map(t => {
        const b = breakEven(t, tierReduction(t, assumptions, incidents, cost), incidents, cost);
        const times = b.incidents !== null && average ? b.incidents / average : null;
        return <tr key={t.tier} data-testid={`break-even-${t.tier}`}>
          <td><b>{t.title}</b><small>вложения / {HORIZON_YEARS} + поддержка</small></td>
          <td className="num">{rub(b.needRub)}</td>
          <td className="num">{b.incidents === null ? "—" : n2.format(b.incidents)}{times !== null && <small>в {n0.format(times)} раз выше среднего по отрасли</small>}</td>
          <td className="num">{b.cost === null ? "—" : rub(b.cost)}</td>
          <td>{b.met ? <Badge tone="green" icon="ok">окупается за {HORIZON_YEARS} года</Badge> : <Badge tone="grey">не окупается за {HORIZON_YEARS} года</Badge>}</td>
        </tr>;
      })}</tbody>
    </table>
    <p className="v5-hint">Доля снижения инцидентов — гипотеза команды, проверяется пилотом. Окупаемость только на травмах при среднеотраслевой частоте не получается; остальная ценность — штрафы, время контроля и стоимость владения.</p>
  </Panel>;
}

interface MarketRow { title: string; value: string; source: string }
const CLOUD_RUB_MONTH = 3900;
export function marketRows(cameras: number | undefined): MarketRow[] {
  const cams = cameras && cameras > 0 ? cameras : 8;
  return [
    { title: "Облачная видеоаналитика NormaCheck", value: `3 900 ₽ за камеру в месяц · ${cams} камер — ${rub(CLOUD_RUB_MONTH * 12 * cams)} в год`, source: "прайс NormaCheck, проверено 10.2026" },
    { title: "Модуль контроля спецодежды и СИЗ на канал", value: "6–7 тыс. ₽ (TRASSIR), 9–11,5 тыс. ₽ (Macroscop)", source: "каталоги производителей, 10.2026" },
    { title: "Пилот ИИ-видеоаналитики у интегратора на 2–4 камерах", value: "от 480 000 ₽", source: "прайс НЬЮ-ССТ, 09.2026" },
    { title: "Штраф юрлицу: общие нарушения охраны труда, КоАП 5.27.1 ч. 1", value: "50–80 тыс. ₽", source: "КоАП РФ, ред. 2026" },
    { title: "Допуск без обучения или медосмотра, ч. 3", value: "110–130 тыс. ₽", source: "КоАП РФ, ред. 2026" },
    { title: "Необеспечение СИЗ 2-го класса риска, ч. 4", value: "130–150 тыс. ₽", source: "КоАП РФ, ред. 2026" },
    { title: "Повторное аналогичное нарушение, ч. 5", value: "100–200 тыс. ₽ или приостановка до 90 суток", source: "КоАП РФ, ред. 2026" },
  ];
}

export function MarketPanel({ cameras }: { cameras?: number }) {
  return <Panel title="Рыночные ориентиры" tools={<Badge tone="grey">чужие цены, не цена Argus</Badge>} flush data-testid="market">
    <table className="ds-table v5-market">
      <thead><tr><th>Что</th><th>Цена</th><th>Источник, дата</th></tr></thead>
      <tbody>{marketRows(cameras).map(m => <tr key={m.title}><td><b>{m.title}</b><small className="v5-source-inline">{m.source}</small></td><td className="v5-market-value">{m.value}</td><td className="v5-source">{m.source}</td></tr>)}</tbody>
    </table>
    <p className="v5-hint">Для сравнения со стоимостью владения: облако платится каждый месяц и видео уходит с завода, контур на LinQ остаётся на площадке. Штраф — не экономия по умолчанию: вероятность проверки зависит от завода.</p>
  </Panel>;
}
