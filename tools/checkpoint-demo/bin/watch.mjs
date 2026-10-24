// One iteration of the watch loop over main (until 10:00 MSK, every 30 min):
// 1) the scratch worktree of main: fetch + checkout origin/main, uv sync, backend with SAFEWATCH_FAKE=1 on 8000;
// 2) smoke --target real by the contract of main; compare contract/*.json with contract-base.json;
// 3) stop the backend (uv run --no-sync safewatch stop) and wait for the port;
// 4) one line in WATCH_LOG.md; a PASS that became FAIL is a line «РЕГРЕССИЯ».
//   node bin/watch.mjs [--real DIR]
// Exit: 0 done, 10 the contract changed (the mock must be updated), 2 the scratch worktree is missing.
import { spawn, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { appendFileSync, existsSync, mkdirSync, openSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const args = process.argv.slice(2);
const opt = (name, def) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : def;
};
const HERE = fileURLToPath(new URL("..", import.meta.url));
const REAL = opt("--real", "C:/Users/User/Documents/mosprom2026-real");
const HEALTH = "http://127.0.0.1:8000/api/health";
const LOG = join(HERE, "WATCH_LOG.md");
const LAST = join(HERE, "watch", "last-real.json");
const BASE = JSON.parse(readFileSync(join(HERE, "contract-base.json"), "utf8"));
const CONTRACT_FILES = ["openapi.json", "ws.schema.json", "ws-examples.json"];

if (!existsSync(join(REAL, ".git"))) {
  console.error(`нет scratch-worktree ${REAL}: git worktree add --detach ${REAL} origin/main`);
  process.exit(2);
}

function run(cmd, argv, opts = {}) {
  const r = spawnSync(cmd, argv, { cwd: REAL, encoding: "utf8", ...opts });
  return { code: r.status, out: `${r.stdout ?? ""}${r.stderr ?? ""}`.trim(), error: r.error };
}
const UV = run("uv", ["--version"]).error ? "C:/Users/User/AppData/Roaming/Python/Python312/Scripts/uv.exe" : "uv";
const now = () => new Date().toLocaleTimeString("ru-RU", { timeZone: "Europe/Moscow", hour: "2-digit", minute: "2-digit" });

async function up() {
  try {
    return (await fetch(HEALTH, { signal: AbortSignal.timeout(2000) })).ok;
  } catch {
    return false;
  }
}
async function waitFor(pred, ms) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    if (await pred()) return true;
    await new Promise((r) => setTimeout(r, 1000));
  }
  return false;
}

const notes = [];
const started = now();

// 1. main and the backend
run("git", ["fetch", "-q", "origin"]);
const co = run("git", ["checkout", "-q", "--detach", "origin/main"]);
if (co.code !== 0) notes.push(`checkout: ${co.out.slice(0, 120)}`);
const commit = run("git", ["rev-parse", "--short=8", "HEAD"]).out;
const state = (readFileSync(join(REAL, "progress.md"), "utf8").match(/^- state: (.*)$/m) ?? [, "?"])[1];
const sync = run(UV, ["sync", "-q"]);
if (sync.code !== 0) notes.push(`uv sync: код ${sync.code}`);

// The tails of config/models.yaml are git-ignored (models/*), and LinqBackend wants the file even
// with SAFEWATCH_FAKE=1 (model_missing otherwise). FakeRemoteShell never reads them: empty stubs in
// the scratch worktree let the smoke go past the upload (GAPS G8).
const tails = [...readFileSync(join(REAL, "config", "models.yaml"), "utf8").matchAll(/^\s*linq_tail:\s*(\S+)\s*$/gm)].map((m) => m[1]);
const stubbed = tails.filter((t) => t !== "null" && !existsSync(join(REAL, t)));
for (const t of stubbed) {
  mkdirSync(dirname(join(REAL, t)), { recursive: true });
  writeFileSync(join(REAL, t), "");
}
if (stubbed.length) notes.push(`созданы заглушки хвостов ONNX: ${stubbed.length}`);
const stubs = tails.filter((t) => t !== "null" && existsSync(join(REAL, t)) && readFileSync(join(REAL, t)).length === 0).length;

let ownBackend = false;
if (await up()) {
  notes.push("порт 8000 уже занят чужим бэкендом: свой не поднимал, smoke против него");
} else {
  rmSync(join(REAL, "data", "app"), { recursive: true, force: true }); // fresh scratch DB each run
  mkdirSync(join(REAL, "data"), { recursive: true });
  const out = openSync(join(REAL, "data", "watch-serve.log"), "w");
  const child = spawn(UV, ["run", "--no-sync", "safewatch", "serve", "--seed"], {
    cwd: REAL, env: { ...process.env, SAFEWATCH_FAKE: "1", PYTHONIOENCODING: "utf-8" },
    detached: true, stdio: ["ignore", out, out], windowsHide: true,
  });
  child.unref();
  ownBackend = true;
  if (!(await waitFor(up, 90000))) {
    const tail = readFileSync(join(REAL, "data", "watch-serve.log"), "utf8").trim().split("\n").slice(-2).join(" / ");
    notes.push(`бэкенд не поднялся за 90 с: ${tail.slice(0, 160)}`);
  }
}

// 2. smoke and the contract
const json = join(HERE, "watch", "current-real.json");
mkdirSync(join(HERE, "watch"), { recursive: true });
const smoke = spawnSync(process.execPath, [join(HERE, "bin", "smoke.mjs"), "--target", "real", "--contract", join(REAL, "contract"), "--json", json], { encoding: "utf8", timeout: 600000 });
process.stdout.write(smoke.stdout ?? "");
const result = existsSync(json) ? JSON.parse(readFileSync(json, "utf8")) : { rows: [], verdict: -1 };

const changed = CONTRACT_FILES.filter((f) => {
  const p = join(REAL, "contract", f);
  const h = existsSync(p) ? createHash("sha256").update(readFileSync(p)).digest("hex") : "missing";
  return h !== BASE[f];
});

// 3. stop
if (ownBackend) {
  const stop = run(UV, ["run", "--no-sync", "safewatch", "stop"]);
  if (!(await waitFor(async () => !(await up()), 20000))) notes.push(`порт 8000 не освободился (${stop.out.slice(0, 60)})`);
}

// 4. log
const prev = existsSync(LAST) ? JSON.parse(readFileSync(LAST, "utf8")) : null;
const before = new Map((prev?.rows ?? []).map((r) => [r.step, r.result]));
const fixed = [];
const broken = [];
const regressions = [];
for (const r of result.rows) {
  const was = before.get(r.step);
  if (!prev || was === r.result) continue;
  if (r.result === "PASS") fixed.push(r.step);
  else if (was === "PASS" && r.result === "FAIL") regressions.push(`${r.step}: ${r.detail}`);
  else if (r.result === "FAIL" || was === "PASS") broken.push(`${r.step} (${was}→${r.result})`);
}
const count = (k) => result.rows.filter((r) => r.result === k).length;
if (!existsSync(LOG)) {
  writeFileSync(LOG, "# WATCH_LOG: smoke --target real по main\n\nСтрока на прогон: время МСК · коммит main · слайс из progress.md · PASS/FAIL/SKIP · контракт · что заработало или сломалось. `РЕГРЕССИЯ` — шаг был PASS, стал FAIL.\n\n");
}
const line = [
  `- ${started} · main ${commit} · ${state}`,
  `PASS ${count("PASS")} / FAIL ${count("FAIL")} / SKIP ${count("SKIP")}`,
  changed.length ? `контракт ИЗМЕНИЛСЯ: ${changed.join(", ")}` : "контракт без изменений",
  !prev ? "первый прогон" : `заработало: ${fixed.join("; ") || "—"}; сломалось: ${broken.join("; ") || "—"}`,
  ...(stubs ? [`хвосты ONNX: заглушки (${stubs}), фейк их не читает`] : []),
  ...notes,
].join(" · ");
appendFileSync(LOG, `${line}\n`);
for (const r of regressions) appendFileSync(LOG, `- РЕГРЕССИЯ ${started} · main ${commit} · ${r}\n`);
if (result.rows.length) writeFileSync(LAST, JSON.stringify(result, null, 2));
console.log(`\n${line}`);
for (const r of regressions) console.log(`РЕГРЕССИЯ: ${r}`);
process.exit(changed.length ? 10 : 0);
