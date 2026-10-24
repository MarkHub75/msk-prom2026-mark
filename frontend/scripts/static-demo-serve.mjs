// CI fixture: serve only the built files, with Pages' 404 behavior. No API or SPA fallback.
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { resolve, extname } from "node:path";
const root = resolve("dist");
const base = process.env.PAGES_BASE;
const mime = {".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".jpg": "image/jpeg", ".png": "image/png", ".woff2": "font/woff2", ".mp4": "video/mp4"};
createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost");
  if (!url.pathname.startsWith(base)) { res.writeHead(404); res.end("Outside Pages base"); return; }
  const pathname = decodeURIComponent(url.pathname.slice(base.length)) || "index.html";
  const path = resolve(root, pathname);
  if (!path.startsWith(root + "/")) { res.writeHead(403); res.end(); return; }
  try { const file = await readFile(path); res.writeHead(200, {"Content-Type": mime[extname(path)] ?? "application/octet-stream"}); res.end(file); }
  catch { res.writeHead(404, {"Content-Type": "text/html"}); res.end(await readFile(resolve(root, "404.html"))); }
}).listen(4173, "127.0.0.1", () => console.log(`Static Pages fixture: http://127.0.0.1:4173${base}`));
