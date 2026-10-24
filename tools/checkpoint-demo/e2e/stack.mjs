// The private stack of the e2e and the smoke loop: mock on 4110/4111, Vite on 5174.
// The ports 4010/4011/5173 belong to the owner and Codex, 8000 to the watch over main.
import { spawn, spawnSync } from "node:child_process";
import { existsSync, mkdirSync, openSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

export const HERE = fileURLToPath(new URL("..", import.meta.url));
export const REST = "http://127.0.0.1:4110";
export const WS = "ws://127.0.0.1:4111/ws";
export const FRONT_URL = "http://127.0.0.1:5174";
export const OWNER_FRONT = "C:/Users/User/Documents/mosprom2026-hack/frontend";
// Vite for the fixture front (e2e/fixture-front) comes from the main frontend of the watch worktree.
export const FIXTURE_FRONT = join(HERE, "e2e", "fixture-front");
const MAIN_FRONT = "C:/Users/User/Documents/mosprom2026-real/frontend";
const RUN = join(tmpdir(), "sw-checkpoint-demo");
mkdirSync(RUN, { recursive: true });
const VITE_STATE = join(RUN, "vite-5174.json");

async function ok(url) {
  try {
    return (await fetch(url, { signal: AbortSignal.timeout(2000) })).status < 500;
  } catch {
    return false;
  }
}

async function waitFor(pred, ms) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    if (await pred()) return true;
    await new Promise((r) => setTimeout(r, 500));
  }
  return false;
}

function start(cmd, args, { cwd, env, log }) {
  const out = openSync(join(RUN, log), "a");
  const child = spawn(cmd, args, { cwd, env: { ...process.env, ...env }, detached: true, stdio: ["ignore", out, out], windowsHide: true });
  child.unref();
  return child.pid;
}

export async function ensureMock() {
  if (await ok(`${REST}/api/health`)) return "уже работал";
  start(process.execPath, [join(HERE, "src", "server.mjs"), "--quiet", "--rest-port", "4110", "--ws-port", "4111"], { cwd: HERE, log: "mock-4110.log" });
  if (!(await waitFor(() => ok(`${REST}/api/health`), 20000))) throw new Error("мок 4110 не поднялся (лог: %TEMP%/sw-checkpoint-demo/mock-4110.log)");
  return "запущен";
}

// The owner's frontend when it is there and installed; otherwise null with the reason.
export function pickFront(override) {
  const dir = override ?? OWNER_FRONT;
  if (dir === FIXTURE_FRONT) return { dir, viteFrom: MAIN_FRONT, reason: "" };
  if (!existsSync(join(dir, "package.json"))) return { dir: null, reason: `нет фронта: ${dir}` };
  if (!existsSync(join(dir, "node_modules", "vite"))) return { dir: null, reason: `во фронте нет node_modules (не ставлю сам): ${dir}` };
  return { dir, viteFrom: dir, reason: "" };
}

function killTree(pid) {
  spawnSync("taskkill", ["/PID", String(pid), "/T", "/F"], { stdio: "ignore" });
}

export async function ensureVite(dir, viteFrom = dir) {
  const state = existsSync(VITE_STATE) ? JSON.parse(readFileSync(VITE_STATE, "utf8")) : null;
  const alive = await ok(FRONT_URL);
  if (alive && state?.dir === dir) return "уже работал";
  if (alive && state?.pid) killTree(state.pid); // another frontend folder: restart on the new one
  if (alive && !state) throw new Error("порт 5174 занят чужим процессом");
  await waitFor(async () => !(await ok(FRONT_URL)), 10000);
  const pid = start(process.execPath, [join(viteFrom, "node_modules", "vite", "bin", "vite.js"), "--config", join(HERE, "e2e", "vite.e2e.config.mjs")], {
    cwd: dir,
    log: "vite-5174.log",
    env: { SW_FRONT_DIR: dir, SW_VITE_FROM: viteFrom, SW_VITE_CACHE: join(RUN, "vite-cache"), VITE_API_BASE: REST, VITE_WS_URL: WS },
  });
  writeFileSync(VITE_STATE, JSON.stringify({ dir, pid }));
  if (!(await waitFor(() => ok(FRONT_URL), 60000))) throw new Error("Vite 5174 не поднялся (лог: %TEMP%/sw-checkpoint-demo/vite-5174.log)");
  return "запущен";
}

export async function director(path, method = "POST") {
  const r = await fetch(`${REST}/__demo/${path}`, { method });
  return r.json();
}
