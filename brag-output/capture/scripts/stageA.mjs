import { chromium, BASE, ctxFor, buttons } from "./lib.mjs";
const OUT = "raw";
const browser = await chromium.launch();
// phone operator feed before any verdict
const pc = await ctxFor(browser, "operator", true); const pp = await pc.newPage();
await pp.goto(BASE + "/m/operator"); await pp.waitForTimeout(4000);
await pp.screenshot({ path: `${OUT}/A1-m-operator.png` });
// desktop takeover
const dc = await ctxFor(browser, "operator"); const dp = await dc.newPage();
await dp.goto(BASE + "/events/241?takeover=1"); await dp.waitForTimeout(5000);
await dp.screenshot({ path: `${OUT}/A2-takeover.png` });
console.log(await buttons(dp));
await dp.getByRole("button", { name: /^Подтвердить/ }).first().hover();
await dp.waitForTimeout(400);
await dp.screenshot({ path: `${OUT}/A3-takeover-hover.png` });
await dp.getByRole("button", { name: /^Подтвердить/ }).first().click();
await dp.waitForTimeout(400);
await dp.screenshot({ path: `${OUT}/A4-after-confirm-0.4.png` });
await dp.waitForTimeout(1600);
await dp.screenshot({ path: `${OUT}/A5-after-confirm-2.png` });
console.log(dp.url(), await buttons(dp));
await dp.goto(BASE + "/events/241"); await dp.waitForTimeout(4000);
await dp.screenshot({ path: `${OUT}/A6-event-card.png` });
console.log(await buttons(dp));
await browser.close();
