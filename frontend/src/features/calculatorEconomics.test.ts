import { describe, expect, it } from "vitest";
import { breakEven, industryHint, marketRows, tierReduction } from "./calculatorEconomics";
import { EXAMPLE_ASSUMPTIONS, exampleRollout } from "./calculatorExample";

describe("break-even over 3 years (docs/ECONOMICS_SOURCES.md, item 3)", () => {
  const r = exampleRollout();
  const base = r.tiers[0];
  it("needs capex / 3 + opex of savings a year", () => {
    const b = breakEven(base, tierReduction(base, EXAMPLE_ASSUMPTIONS, 4, r.incident_cost_rub), 4, r.incident_cost_rub);
    expect(b.needRub).toBeCloseTo(9_700_000 / 3 + 1_455_000, 0);
    expect(b.incidents).toBeCloseTo(b.needRub / (1_500_000 * 0.2), 6);
    expect(b.cost).toBeCloseTo(b.needRub / (4 * 0.2), 6);
    expect(b.met).toBe(false);
  });
  it("reduction falls back to savings / (incidents × cost) when the answer has no such assumption", () => {
    expect(tierReduction(base, [], 4, 1_500_000)).toBeCloseTo(0.2, 9);
    expect(tierReduction(base, [], 0, 1_500_000)).toBeNull();
    expect(breakEven(base, null, 4, 1_500_000).incidents).toBeNull();
  });
  it("industry hint uses Rosstat 1,17 per 1000", () => {
    expect(industryHint(200)).toBe("Среднее по обрабатывающей промышленности — 1,17 на 1000 работников (Росстат, 2025): для 200 человек ≈ 0,23");
  });
  it("cloud benchmark is 3900 ₽ per camera a month", () => {
    expect(marketRows(8)[0].value).toMatch(/374\s400 ₽ в год/);
    expect(marketRows(8).every(row => row.source.length > 0)).toBe(true);
  });
});
