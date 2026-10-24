// Vite for the e2e: serves a frontend folder we must not touch (SW_FRONT_DIR) on 127.0.0.1:5174.
// Its own vite.config is not used; the cache goes to SW_VITE_CACHE, so the folder gets no writes.
// VITE_API_BASE and VITE_WS_URL come from the process env, which wins over the .env files.
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

export default async () => {
  const root = process.env.SW_FRONT_DIR;
  const require = createRequire(`${process.env.SW_VITE_FROM ?? root}/package.json`);
  let plugins = [];
  try {
    plugins = [(await import(pathToFileURL(require.resolve("@vitejs/plugin-react")).href)).default()];
  } catch {
    // a frontend without React (the e2e fixture)
  }
  return {
    root,
    envDir: root,
    cacheDir: process.env.SW_VITE_CACHE,
    plugins,
    clearScreen: false,
    server: { host: "127.0.0.1", port: Number(process.env.SW_VITE_PORT ?? 5174), strictPort: true },
  };
};
