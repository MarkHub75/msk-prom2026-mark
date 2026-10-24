// Service worker of the installable app, written by hand (no build plugin).
// Caches only the app shell (index.html, hashed /assets, icons, manifest).
// /api and /ws never go through a cache: alarms are shown live or not at all.
const SHELL = "argus-shell-v1";
const SHELL_KEY = "/index.html";
const NEVER = /^\/(?:api|ws)(?:\/|$)/;
const STATIC = /^\/(?:assets|icons|fonts)\/|^\/manifest\.webmanifest$/;
const FILES = ["/manifest.webmanifest", "/icons/icon.svg", "/icons/icon-192.png", "/icons/icon-512.png", "/icons/maskable-512.png", "/icons/badge-96.png"];

// Shown when there is neither network nor a cached shell: never a white screen.
const OFFLINE_HTML = `<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#1e1f23"><title>Нет связи</title><style>
html,body{height:100%;margin:0}body{display:grid;place-items:center;padding:24px;box-sizing:border-box;background:#111214;color:#eceef1;font:16px/1.45 system-ui,sans-serif;text-align:center}
main{max-width:340px}h1{margin:16px 0 8px;font-size:22px;line-height:1.2}p{margin:0 0 20px;color:#a1a7b0}
button{min-height:48px;padding:0 20px;border:1px solid #363940;border-radius:12px;background:#26282d;color:#eceef1;font:600 16px system-ui,sans-serif}
</style></head><body><main><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#a1a7b0" stroke-width="1.6"><path d="M2 12c2.6-4.6 6-7 10-7s7.4 2.4 10 7c-2.6 4.6-6 7-10 7s-7.4-2.4-10-7Z"/><path d="M3 3l18 18"/></svg>
<h1>Нет связи с сервером — данные не показываются</h1><p>Устаревшие тревоги опаснее пустого экрана. Как только сеть вернётся, откройте приложение снова.</p>
<button onclick="location.reload()">Проверить связь</button></main></body></html>`;

/** Stores index.html and its /assets; drops scripts and styles of older builds. */
async function keepShell(cache, response) {
  const html = await response.clone().text();
  await cache.put(SHELL_KEY, response);
  const assets = [...html.matchAll(/(?:src|href)="(\/assets\/[^"]+)"/g)].map(m => m[1]);
  await Promise.all(assets.map(async url => { if (!await cache.match(url)) await cache.add(url); }));
  for (const request of await cache.keys()) {
    const path = new URL(request.url).pathname;
    if (/^\/assets\/.*\.(?:js|css)$/.test(path) && !assets.includes(path)) await cache.delete(request);
  }
}

self.addEventListener("install", event => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL);
    try {
      const response = await fetch("/", { cache: "no-store" });
      if (response.ok) await keepShell(cache, response);
      await cache.addAll(FILES);
    } catch { /* offline at install: the next online visit fills the cache */ }
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) if (key !== SHELL) await caches.delete(key);
    await self.clients.claim();
  })());
});

async function navigation(request) {
  const cache = await caches.open(SHELL);
  try {
    const response = await fetch(request);
    if (response.ok && (response.headers.get("content-type") ?? "").includes("text/html")) await keepShell(cache, response.clone());
    return response;
  } catch {
    // The shell starts and shows its own «Нет связи с сервером» screen: no API answer, no data.
    return await cache.match(SHELL_KEY) ?? new Response(OFFLINE_HTML, { status: 503, headers: { "Content-Type": "text/html; charset=utf-8" } });
  }
}

async function cacheFirst(request) {
  const cache = await caches.open(SHELL);
  const hit = await cache.match(request);
  if (hit) return hit;
  const response = await fetch(request);
  if (response.ok) await cache.put(request, response.clone());
  return response;
}

self.addEventListener("fetch", event => {
  const request = event.request;
  const url = new URL(request.url);
  // Live data and everything that is not a plain same-origin GET: straight to the network, no cache.
  if (request.method !== "GET" || url.origin !== self.location.origin || NEVER.test(url.pathname)) return;
  if (request.mode === "navigate") event.respondWith(navigation(request));
  else if (STATIC.test(url.pathname)) event.respondWith(cacheFirst(request));
});

// A tap on an alarm notification opens its card in the app window (or a new one).
self.addEventListener("notificationclick", event => {
  event.notification.close();
  const target = new URL(event.notification.data?.url ?? "/m/", self.location.origin).href;
  event.waitUntil((async () => {
    const windows = await self.clients.matchAll({ type: "window", includeUncontrolled: true });
    const client = windows.find(w => new URL(w.url).origin === self.location.origin);
    if (!client) return self.clients.openWindow(target);
    await client.focus();
    try { await client.navigate(target); } catch { /* uncontrolled window: it stays focused where it was */ }
  })());
});
