// Checks on the private stack (mock 4110/4111, Vite 5174), one per watch iteration:
// smoke --target mock N times in a row, the e2e on e2e/fixture-front (the harness itself) and the
// e2e on the owner's frontend (failures go to e2e/FRONT_BUGS.md).
//   node bin/local-checks.mjs [--runs N]
// The last stdout line is a JSON summary; `text` is the piece for the WATCH_LOG line.
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
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

// The frontend under test: worktree of origin/front/control-room, updated before each e2e.
const FRONT_WT = "C:/Users/User/Documents/mosprom2026-front";
const git = (...a) => spawnSync("git", a, { cwd: FRONT_WT, encoding: "utf8" });
const lockHash = () => {
  const f = join(FRONT_WT, "frontend", "package-lock.json");
  return existsSync(f) ? createHash("sha256").update(readFileSync(f)).digest("hex") : "";
};
let frontNote = "";
if (existsSync(join(FRONT_WT, ".git"))) {
  const before = lockHash();
  git("fetch", "-q", "origin");
  const co = git("checkout", "-q", "--detach", "origin/front/control-room");
  if (co.status !== 0) frontNote = ` (checkout: ${co.stderr.trim().slice(0, 80)})`;
  if (lockHash() !== before || !existsSync(join(FRONT_WT, "frontend", "node_modules", "vite"))) {
    const ci = spawnSync("npm", ["ci", "--no-fund", "--no-audit"], { cwd: join(FRONT_WT, "frontend"), shell: true, encoding: "utf8", timeout: 600000 });
    frontNote += ci.status === 0 ? " (npm ci)" : ` (npm ci: код ${ci.status})`;
  }
  frontNote = ` ${git("rev-parse", "--short=8", "HEAD").stdout.trim()}${frontNote}`;
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
  `e2e фронт control-room${frontNote} ${e2e(owner)}${owner?.result === "FAIL" ? " → FRONT_BUGS" : ""}`,
].join(" · ");
console.log(JSON.stringify({ smoke: { pass, runs: RUNS, fails }, fixture, owner, text }));
