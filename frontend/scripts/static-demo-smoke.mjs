// Runs against dist using Chromium installed only on the GitHub runner.
import assert from "node:assert/strict";
import { mkdir, readFile } from "node:fs/promises";
import { pathToFileURL } from "node:url";
const { chromium } = await import(pathToFileURL(process.env.PLAYWRIGHT_MODULE));
const browser = await chromium.launch();
const context = await browser.newContext({viewport: {width: 1440, height: 1000}});
const page = await context.newPage();
const errors = [];
const forbidden = [];
const requests = [];
page.on("pageerror", error => errors.push(error.message));
page.on("console", message => { if (message.type() === "error" && !message.text().includes("404")) errors.push(message.text()); });
page.on("request", request => {
  const url = new URL(request.url()); requests.push(url.pathname);
  if (url.pathname.startsWith("/api/") || url.pathname.endsWith("/ws") || !["127.0.0.1", "localhost"].includes(url.hostname)) forbidden.push(request.url());
});
page.on("websocket", socket => forbidden.push(socket.url()));
const base = `http://127.0.0.1:4173${process.env.PAGES_BASE}`;
const product = (await readFile("src/brand.ts", "utf8")).match(/PRODUCT\s*=\s*"([^"]+)"/)[1];
const screenshotDir = process.env.SMOKE_OUTPUT;
await mkdir(screenshotDir, {recursive: true});
const waitStatus = (id, status) => page.waitForFunction(async ({id, status}) => {
  const response = await fetch(`/api/events/${id}`);
  return (await response.json()).event.status === status;
}, {id, status});
try {
  // Includes the deep-link 404 -> canonical #/operator redirect, not a Vite SPA server.
  await page.goto(`${base}operator`);
  await page.getByTestId("operator-view").waitFor();
  assert.equal(await page.title(), product);
  assert.match(page.url(), /#\/operator$/);
  assert(await page.getByText("Статическое демо: данные и кадры синтетические, сервера нет", {exact: true}).isVisible());
  await page.getByLabel("Имя сотрудника").fill("Демо оператор");
  await page.locator('[data-panel="Камеры завода"] img').first().waitFor();
  await page.waitForFunction(() => [...document.querySelectorAll('[data-panel="Камеры завода"] img')].every(image => image.complete && image.naturalWidth > 0));
  await page.getByRole("button", {name: "Следующий шаг демо", exact: true}).click();
  await page.locator(".cr-q-yellow").first().waitFor();
  await page.getByTestId("evidence-image").first().waitFor();
  await page.waitForFunction(() => document.querySelector('[data-testid="evidence-image"]')?.naturalWidth > 0);
  await page.screenshot({path: `${screenshotDir}/01-yellow.png`});
  await page.getByRole("button", {name: "Следующий шаг демо", exact: true}).click();
  await page.getByTestId("incident-focus").waitFor();
  const red = await page.evaluate(async () => (await (await fetch("/api/operator/feed")).json()).find(event => event.level === "red" && ["new", "viewed"].includes(event.status)));
  assert(red, "Second director step must publish a red event");
  await page.screenshot({path: `${screenshotDir}/02-red.png`});
  await page.getByRole("alertdialog", {name: "Критическое событие"}).locator('[data-action="confirm"]').click();
  await waitStatus(red.id, "sent_to_master");
  await page.getByRole("navigation", {name: "Выбор роли"}).getByRole("button", {name: "Мастер", exact: true}).click();
  await page.locator("a.brand").click();
  await page.getByTestId("master-inbox").waitFor();
  const assignment = page.locator(`.ms-cards a[href$="/master/events/${red.id}"]`);
  await assignment.waitFor();
  assert.match(await assignment.innerText(), /Падение/);
  await page.screenshot({path: `${screenshotDir}/03-master.png`});
  await assignment.click();
  await page.getByTestId("master-detail").waitFor();
  await page.locator('[data-action="accept"]').click();
  await waitStatus(red.id, "master_accepted");
  await page.getByTestId("measures").fill("Демонстрация: участок осмотрен, приняты меры.");
  await page.locator('[data-action="resolve"]').click();
  await waitStatus(red.id, "resolved");
  const unsupported = await page.evaluate(async () => {
    const result = await fetch("/api/stats/management");
    return {status: result.status, body: await result.json()};
  });
  assert.equal(unsupported.status, 501);
  assert.equal(unsupported.body.message, "Недоступно в статическом демо");
  // Probe unknown reads and writes too: never fall through to the network.
  for (const method of ["GET", "POST", "PUT", "PATCH", "DELETE"]) {
    const code = await page.evaluate(async method => (await fetch("/api/unsupported-static", {method})).status, method);
    assert.equal(code, 501);
  }
  await page.getByRole("button", {name: "Сбросить", exact: true}).click();
  await page.getByRole("navigation", {name: "Выбор роли"}).getByRole("button", {name: "Оператор", exact: true}).click();
  await page.locator("a.brand").click();
  await page.getByTestId("operator-view").waitFor();
  await page.waitForFunction(async () => (await (await fetch("/api/operator/feed")).json()).length === 0);
  assert(await page.getByRole("button", {name: "Следующий шаг демо", exact: true}).isEnabled());
  await page.setViewportSize({width: 390, height: 844});
  await page.screenshot({path: `${screenshotDir}/04-mobile.png`});
  const director = await page.getByRole("complementary", {name: "Режиссёр демо"}).boundingBox();
  assert(director && director.x >= 0 && director.x + director.width <= 391);
  assert.equal(await page.locator("vite-error-overlay").count(), 0);
  assert.deepEqual(errors, [], "No browser runtime/console errors");
  assert.deepEqual(forbidden, [], "No backend, external requests or network WebSockets");
  assert(requests.some(path => path.includes("/demo/previews/")));
  assert(requests.some(path => path.includes("/demo/evidence/")));
  console.log("PASS: Pages deep link; operator; yellow/red WS events; static frames; master assignment, accept and resolve; honest 501; reset; mobile; no backend requests.");
} catch (error) {
  await page.screenshot({path: `${screenshotDir}/failure.png`, fullPage: true});
  console.error("URL:", page.url(), "Errors:", errors, "Network:", forbidden);
  throw error;
} finally { await browser.close(); }
