import react from "@vitejs/plugin-react";
import { realpathSync } from "node:fs";
import { searchForWorkspaceRoot } from "vite";
import { defineConfig } from "vitest/config";

const backend = process.env.SW_BACKEND ?? "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    watch: { usePolling: true, interval: 300 },
    // node_modules may be a symlink to a shared install (worktrees): let dev serve fonts from there
    fs: { allow: [searchForWorkspaceRoot(process.cwd()), realpathSync("node_modules")] },
    proxy: {
      "/api": backend,
      "/ws": { target: backend, ws: true },
    },
  },
  test: { environment: "jsdom", testTimeout: 60000 },
});
