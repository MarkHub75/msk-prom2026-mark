import react from "@vitejs/plugin-react";
import { readFileSync, realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { searchForWorkspaceRoot, type Plugin } from "vite";
import { defineConfig } from "vitest/config";
import { PRODUCT } from "./src/brand";

const backend = process.env.SW_BACKEND ?? "http://127.0.0.1:8000";

/** Web app manifest: the name from src/brand.ts, colours from the ds.css tokens (served in dev, emitted on build). */
function manifest() {
  const css = readFileSync(fileURLToPath(new URL("./src/styles/ds.css", import.meta.url)), "utf8");
  const token = (name: string) => {
    const value = css.match(new RegExp(`--${name}:\\s*(#[0-9a-fA-F]{3,8})`))?.[1];
    if (!value) throw new Error(`ds.css: no --${name}`);
    return value;
  };
  const icon = (src: string, size: number, purpose = "any") => ({ src, sizes: `${size}x${size}`, type: "image/png", purpose });
  return JSON.stringify({
    id: "/m/",
    name: PRODUCT,
    short_name: PRODUCT,
    description: `${PRODUCT} — тревоги оператора и поручения мастера на телефоне`,
    lang: "ru",
    dir: "ltr",
    // /m/ opens the start screen of the saved role: /m/operator for the operator, /master for the master.
    start_url: "/m/",
    scope: "/",
    display: "standalone",
    background_color: token("ds-bg-0"),
    theme_color: token("ds-bg-2"),
    icons: [icon("/icons/icon-192.png", 192), icon("/icons/icon-512.png", 512), icon("/icons/maskable-192.png", 192, "maskable"), icon("/icons/maskable-512.png", 512, "maskable")],
    shortcuts: [
      { name: "Оператор · тревоги", short_name: "Оператор", url: "/m/operator", icons: [icon("/icons/icon-192.png", 192)] },
      { name: "Мастер · поручения", short_name: "Мастер", url: "/master", icons: [icon("/icons/icon-192.png", 192)] },
    ],
  }, null, 2);
}

function pwa(): Plugin {
  return {
    name: "argus-pwa",
    configureServer(server) {
      server.middlewares.use("/manifest.webmanifest", (_req, res) => { res.setHeader("Content-Type", "application/manifest+json"); res.end(manifest()); });
    },
    generateBundle() { this.emitFile({ type: "asset", fileName: "manifest.webmanifest", source: manifest() }); },
  };
}

export default defineConfig({
  plugins: [react(), pwa()],
  server: {
    watch: { usePolling: true, interval: 300 },
    // node_modules may be a symlink to a shared install (worktrees): let dev serve fonts from there
    fs: { allow: [searchForWorkspaceRoot(process.cwd()), realpathSync("node_modules")] },
    proxy: {
      "/api": backend,
      "/ws": { target: backend, ws: true },
    },
  },
  // Bound jsdom memory/CPU alongside Docker: many workers can starve real debounce timers.
  // Keep every test and its existing assertions/timeouts; only limit concurrent files.
  test: { environment: "jsdom", testTimeout: 60000, maxWorkers: 2 },
});
