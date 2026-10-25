import { createRequire } from "module";
const require = createRequire("C:/Users/User/Documents/mosprom2026-demo/tools/checkpoint-demo/package.json");
const { chromium } = require("playwright");
const BASE = "http://127.0.0.1:8030";
const OUT = "raw";
const post = (p, body, method="POST") => fetch(BASE + p, { method, headers: { "X-Role": "admin", "Content-Type": "application/json" }, body: body ? JSON.stringify(body) : undefined }).then(r => r.status);
console.log("bc10", await post("/api/cameras/10/broadcast", { loop: true }));
console.log("bc9", await post("/api/cameras/9/broadcast", { loop: false }));
const t0 = Date.now();
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await ctx.addInitScript(() => localStorage.setItem("safewatch.role", "operator"));
const shots = [["/operator", "ex-operator"], ["/operator/sectors/1", "ex-sector1"], ["/operator/cameras/9", "ex-cam9"], ["/operator/cameras", "ex-cameras"]];
for (const [p, n] of shots) {
  const page = await ctx.newPage();
  await page.goto(BASE + p, { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(2500);
  await page.screenshot({ path: `${OUT}/${n}.png` });
  console.log(n, ((Date.now() - t0) / 1000).toFixed(1), page.url());
  await page.close();
}
await browser.close();
