// Checks on the private stack (mock 4110/4111, Vite 5174), one per watch iteration:
// smoke --target mock N times in a row, the e2e on e2e/fixture-front (the harness itself) and the
// e2e on the owner's frontend (failures go to e2e/FRONT_BUGS.md).
//   node bin/local-checks.mjs [--runs N]
// The last stdout line is a JSON summary; `text` is the piece for the WATCH_LOG line.
import { spawnSync } from "node:child_process";
import { join } from "node:path";
import { HERE, REST, WS, ensureMock } from "../e2e/stack.mjs";

const args = process.argv.slice(2);
const RUNS = Number(args[args.indexOf("--runs") + 1] || 20);
const node = (script, argv) => spawnSync(process.execPath, [join(HERE, script), ...argv], { cwd: HERE, encoding: "utf8", timeout: 300000 });
const lastJson = (out) => {
  try {
    return JSON.parse(out.trim().split("\n").at(-1));
  } catch {
    return null;
  }
};

await ensureMock();
let pass = 0;
const fails = [];
for (let i = 1; i <= RUNS; i++) {
  const r = node("bin/smoke.mjs", ["--target", "mock", "--rest", REST, "--ws", WS]);
  if (r.status === 0) pass += 1;
  else fails.push(`#${i}: ${(r.stdout.match(/^FAIL .*$/m) ?? [`код ${r.status}`])[0].replace(/\s+/g, " ").slice(0, 140)}`);
}

const fixture = lastJson(node("e2e/run.mjs", ["--fixture", "--no-bugs"]).stdout);
const owner = lastJson(node("e2e/run.mjs", []).stdout);
const e2e = (s) => !s ? "ошибка запуска"
  : s.result === "SKIP" ? `SKIP (${s.reason})`
    : s.result === "PASS" ? `${s.passed}/${s.total}`
      : `${s.passed}/${s.total}, упал шаг ${s.failed.step} «${s.failed.name}»`;
const text = [
  `smoke mock ${pass}/${RUNS}${fails.length ? ` (${fails.join("; ")})` : ""}`,
  `e2e фикстура ${e2e(fixture)}`,
  `e2e фронт ${e2e(owner)}${owner?.result === "FAIL" ? " → FRONT_BUGS" : ""}`,
].join(" · ");
console.log(JSON.stringify({ smoke: { pass, runs: RUNS, fails }, fixture, owner, text }));
