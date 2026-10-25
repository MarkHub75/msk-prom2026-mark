import { createRequire } from "module";
const require = createRequire("C:/Users/User/Documents/mosprom2026-demo/tools/checkpoint-demo/package.json");
export const { chromium } = require("playwright");
export const BASE = "http://127.0.0.1:8030";
export async function ctxFor(browser, role, phone = false) {
  const ctx = await browser.newContext(phone
    ? { viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true }
    : { viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  await ctx.addInitScript((r) => localStorage.setItem("safewatch.role", r), role);
  return ctx;
}
export async function buttons(page) {
  return (await page.locator("button, a").allInnerTexts()).map(s => s.trim().replace(/\s+/g, " ")).filter(Boolean);
}
