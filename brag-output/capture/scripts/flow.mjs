// One clean pass of the argus-real scenario: calm -> red takeover -> confirm -> master accepts -> resolved.
import { chromium, BASE, ctxFor, buttons } from "./lib.mjs";
const OUT = "flow";
const post = (p, body) => fetch(BASE + p, { method: "POST", headers: { "X-Role": "admin", "Content-Type": "application/json" }, body: JSON.stringify(body) }).then(r => r.status);
const ev = (id) => fetch(BASE + `/api/events/${id}`, { headers: { "X-Role": "operator" } }).then(r => r.json());
const browser = await chromium.launch();
const named = async (ctx, name) => { await ctx.addInitScript((n) => localStorage.setItem("safewatch.actor", n), name); return ctx; };
const dc = await named(await ctxFor(browser, "operator"), "Иванов А."); const dp = await dc.newPage();
const oc = await named(await ctxFor(browser, "operator", true), "Иванов А."); const op = await oc.newPage();
const mc = await named(await ctxFor(browser, "master", true), "Соколов Д."); const mp = await mc.newPage();
await dp.goto(BASE + "/operator"); await op.goto(BASE + "/m/operator"); await mp.goto(BASE + "/master");
await dp.waitForTimeout(4000);
console.log("bc10", await post("/api/cameras/10/broadcast", { loop: true }), "bc9", await post("/api/cameras/9/broadcast", { loop: false }));
const t0 = Date.now(); const T = () => (Date.now() - t0) / 1000;
const shot = async (page, name) => { await page.screenshot({ path: `${OUT}/${name}.png` }); console.log(T().toFixed(1), name, page.url()); };
const until = async (t) => { const w = t * 1000 - (Date.now() - t0); if (w > 0) await dp.waitForTimeout(w); };
for (const t of [2.5, 6, 10, 13.5]) { await until(t); await shot(dp, `d-calm-${t}`); }
await until(14.5); await shot(op, "m-op-calm");
let i = 0;
while (T() < 21) { await shot(dp, `d-alarm-${String(i++).padStart(2, "0")}`); }
await shot(op, "m-op-red");
await op.goto(BASE + "/m/operator"); await op.waitForTimeout(2500); await shot(op, "m-op-red-reload");
console.log(await buttons(dp));
const confirm = dp.getByRole("button", { name: /^Подтвердить/ }).first();
await confirm.hover(); await dp.waitForTimeout(300); await shot(dp, "d-confirm-hover");
await confirm.click(); await dp.waitForTimeout(250); await shot(dp, "d-confirm-0.25");
await dp.waitForTimeout(1200); await shot(dp, "d-confirm-1.5");
const e1 = await ev(241); console.log("after confirm", e1.status, e1.operator_verdict, e1.allowed_actions);
console.log(await buttons(dp));
if (e1.status !== "sent_to_master") {
  const send = dp.getByRole("button", { name: /Передать мастеру/ }).first();
  if (await send.count()) { await send.click(); await dp.waitForTimeout(1500); await shot(dp, "d-sent"); }
  const e2 = await ev(241); console.log("after send", e2.status);
}
await mp.goto(BASE + "/master"); await mp.waitForTimeout(3000); await shot(mp, "m-master-inbox");
console.log(await buttons(mp));
await mp.goto(BASE + "/master/events/241"); await mp.waitForTimeout(3000); await shot(mp, "m-master-event");
await mp.locator('[data-action="accept"]').click(); await mp.waitForTimeout(1800); await shot(mp, "m-master-accepted");
const ta = mp.locator("textarea").first();
await ta.click(); await ta.fill("Остановил работу, вывел человека из проезда погрузчиков. Провёл инструктаж.");
await mp.waitForTimeout(400); await shot(mp, "m-master-measures");
await mp.locator('[data-action="resolve"]').scrollIntoViewIfNeeded(); await mp.waitForTimeout(300); await shot(mp, "m-master-measures-btn");
await mp.locator('[data-action="resolve"]').click(); await mp.waitForTimeout(1500); await shot(mp, "m-master-resolved");
const e3 = await ev(241); console.log("final", e3.status, e3.operator_verdict);
await dp.goto(BASE + "/events/241"); await dp.waitForTimeout(4000); await shot(dp, "d-event-card");
await op.goto(BASE + "/m/operator"); await op.waitForTimeout(3000); await shot(op, "m-op-after");
const jc = await ctxFor(browser, "ohs"); const jp = await jc.newPage();
await jp.goto(BASE + "/ohs/journal"); await jp.waitForTimeout(4000); await shot(jp, "d-journal");
const ac = await ctxFor(browser, "admin"); const ap = await ac.newPage();
await ap.goto(BASE + "/admin/system"); await ap.waitForTimeout(4000); await shot(ap, "d-system");
await ap.screenshot({ path: `${OUT}/d-system-full.png`, fullPage: true });
await browser.close();
