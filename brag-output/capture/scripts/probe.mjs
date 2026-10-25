import { createRequire } from "module";
const require = createRequire("C:/Users/User/Documents/mosprom2026-demo/tools/checkpoint-demo/package.json");
const { chromium } = require("playwright");
const BASE = "http://127.0.0.1:8030";
const OUT = process.argv[2];
const shots = [
  ["operator", "/operator", 1920, 1080, "probe-operator"],
  ["operator", "/m/operator", 390, 844, "probe-m-operator"],
  ["master", "/master", 390, 844, "probe-master"],
  ["ohs", "/ohs/journal", 1920, 1080, "probe-journal"],
  ["admin", "/admin/system", 1920, 1080, "probe-system"],
];
const browser = await chromium.launch();
for (const [role, path, w, h, name] of shots) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: w < 500 ? 3 : 1 });
  await ctx.addInitScript((r) => localStorage.setItem("safewatch.role", r), role);
  const page = await ctx.newPage();
  await page.goto(BASE + path, { waitUntil: "networkidle" }).catch(() => {});
  await page.waitForTimeout(6000);
  await page.screenshot({ path: `${OUT}/${name}.png` });
  console.log("ok", name, page.url());
  await ctx.close();
}
await browser.close();
