import { describe, expect, it } from "vitest";
import { exampleRollout, exampleScale } from "./calculatorExample";

// tech.md 8.25 on the demo plant (8 cameras, 12 fps, 2 requests per frame, 12.4 fps per accelerator).
describe("calculator example (shown while the server answers 501)", () => {
  it("rollout tiers follow the formulas, the base tier does not pay off", () => {
    const r = exampleRollout();
    expect(r.incident_cost_rub).toBe(1_500_000);
    expect(r.incidents_per_1000_workers).toBe(20);
    expect(r.events_per_operator_shift).toBeNull();
    const [base, extended, max] = r.tiers;
    expect([base.accelerators, base.servers]).toEqual([16, 4]);
    expect(base.capex_rub).toBe(9_700_000);
    expect(base.payback_months).toBeNull();
    expect(extended.capex_rub).toBe(9_900_000);
    expect(extended.payback_months).toBeCloseTo(377.14, 1);
    expect(max.capex_rub).toBe(10_040_000);
    expect(max.payback_months).toBeCloseTo(134.77, 1);
  });
  it("scale adds accelerators, servers and cameras", () => {
    const s = exampleScale();
    expect([s.accelerators_now, s.accelerators_total, s.servers_total]).toEqual([16, 31, 8]);
    expect(s.capex_rub).toBe(15 * 500_000 + 4 * 350_000 + 8 * 30_000);
  });
});
