// `npm run demo`: the backend of main in fake mode with the demo seed, plus this frontend on Vite.
// Until PR #21 is merged the backend and this frontend live on different branches, so the backend
// comes from a separate checkout of main: ARGUS_BACKEND_DIR, by default ../argus-backend next to the repo.
//
//   ARGUS_BACKEND_DIR  checkout of main (default <repo>/../argus-backend)
//   ARGUS_PORT         backend port (default 8000; `port` of its config/user.yaml must match)
//   ARGUS_VIDEOS       folder of mp4 clips: imported once by `safewatch seed --videos` before serve
//   UV                 path to uv when it is not on PATH
import { spawn, spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const front = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repo = resolve(front, "..");
const backend = resolve(process.env.ARGUS_BACKEND_DIR ?? resolve(repo, "..", "argus-backend"));
const port = process.env.ARGUS_PORT ?? "8000";
const uv = process.env.UV ?? "uv";

function fail(lines) {
  console.error(lines.join("\n"));
  process.exit(1);
}

const services = resolve(backend, "src/safewatch/services.py");
if (!existsSync(services)) {
  fail([
    `Нет бэкенда в ${backend}.`,
    "Возьмите ветку main рядом с репозиторием (один раз):",
    "  git worktree add ../argus-backend origin/main",
    "или укажите свою копию main в ARGUS_BACKEND_DIR.",
  ]);
}
if (/NotImplementedError\("slice 6"\)/.test(readFileSync(services, "utf8"))) {
  fail([`В ${backend} заглушки бэкенда (ветка фронта, а не main). Нужна копия ветки main.`]);
}

// The fake LinQ never reads the ONNX tail, but the job checks that the file exists (models/ is not in git).
// Missing tails get a marked placeholder, as the backend tests do; a real file is never touched.
const models = readFileSync(resolve(backend, "config/models.yaml"), "utf8");
const placed = [];
for (const [, tail] of models.matchAll(/linq_tail:\s*(\S+)/g)) {
  const file = resolve(backend, tail);
  if (existsSync(file)) continue;
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, "ARGUS FAKE TAIL: placeholder for SAFEWATCH_FAKE=1, replace with the real export (tools/linq/README.md)\n");
  placed.push(tail);
}
if (placed.length) console.warn(`[backend] заглушки хвостов для фейк-режима (для LinQ замените настоящими): ${placed.join(", ")}`);

const env = { ...process.env, SAFEWATCH_FAKE: "1", PYTHONUTF8: "1" };
const children = [];
function run(name, command, args, options) {
  const child = spawn(command, args, { stdio: "inherit", ...options });
  child.on("error", (e) => {
    console.error(`[${name}] не запустился: ${e.message}${command === uv ? " (uv не найден: укажите путь в UV)" : ""}`);
    stop(1);
  });
  child.on("exit", (code) => {
    console.log(`[${name}] завершён с кодом ${code}`);
    stop(code ?? 0);
  });
  children.push(child);
}
let stopping = false;
function stop(code) {
  if (stopping) return;
  stopping = true;
  for (const child of children) {
    if (child.exitCode !== null || child.pid === undefined) continue;
    // uv starts python as a grandchild: on Windows only a tree kill stops the server.
    if (process.platform === "win32") spawnSync("taskkill", ["/pid", String(child.pid), "/T", "/F"], { stdio: "ignore" });
    else child.kill();
  }
  process.exit(code);
}
process.on("SIGINT", () => stop(0));
process.on("SIGTERM", () => stop(0));

if (process.env.ARGUS_VIDEOS) {
  // `safewatch seed --videos` imports every file of the folder and stops at the first non-video one, leaving
  // the seed half made; and it imports videos only on the first seed (an existing database: "skipped").
  const dir = resolve(process.env.ARGUS_VIDEOS);
  if (!existsSync(dir)) fail([`Нет папки ARGUS_VIDEOS: ${dir}`]);
  const files = readdirSync(dir, { withFileTypes: true }).filter((d) => d.isFile()).map((d) => d.name);
  const other = files.filter((name) => !/\.(mp4|avi|mov|mkv)$/i.test(name));
  if (other.length) fail([
    `В ARGUS_VIDEOS не только видео: ${other.slice(0, 5).join(", ")}${other.length > 5 ? ` и ещё ${other.length - 5}` : ""}.`,
    "Бэкенд импортирует каждый файл папки и падает на первом не-видео. Положите ролики (mp4 H.264, .avi, .mov, .mkv) в отдельную папку.",
  ]);
  if (!files.length) fail([`В ${dir} нет видео.`]);
  const db = resolve(backend, "data/app/safewatch.db");
  if (existsSync(db)) {
    console.warn(`[backend] сид уже есть (${db}): seed --videos ролики из ARGUS_VIDEOS не импортирует.`);
    console.warn(`          Для чистого старта удалите ${resolve(backend, "data/app")} или загрузите видео в «Администратор → Камеры → Настроить → Видео».`);
  }
  console.log(`[backend] seed --videos ${process.env.ARGUS_VIDEOS}`);
  const seeded = spawnSync(uv, ["run", "safewatch", "seed", "--videos", resolve(process.env.ARGUS_VIDEOS)], { cwd: backend, env, stdio: "inherit" });
  if (seeded.status !== 0) fail([`[backend] seed не прошёл: ${seeded.error?.message ?? `код ${seeded.status}`}`]);
}

run("backend", uv, ["run", "safewatch", "serve", "--seed", "--port", port], { cwd: backend, env });
run("front", process.execPath, [resolve(front, "node_modules/vite/bin/vite.js"), "--host", "127.0.0.1"], { cwd: front, env: { ...process.env, SW_BACKEND: `http://127.0.0.1:${port}` } });
console.log(`АРГУС: бэкенд ${backend} в фейк-режиме на :${port}, фронт — адрес Vite ниже. Ctrl+C останавливает оба.`);
