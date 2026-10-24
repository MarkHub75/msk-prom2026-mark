// Dumps the ARIA snapshot of the main screens of a frontend on the private stack (for selectors).
//   node e2e/probe.mjs [--front DIR]
import { chromium } from "playwright";
import { FRONT_URL, director, ensureMock, ensureVite, pickFront } from "./stack.mjs";

const i = process.argv.indexOf("--front");
const front = pickFront(i > 0 ? process.argv[i + 1] : undefined);
if (!front.dir) throw new Error(front.reason);
await ensureMock();
await ensureVite(front.dir, front.viteFrom);
await director("reset");
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
const dump = async (title) => {
  await page.waitForTimeout(1500);
  console.log(`\n===== ${title} · ${page.url()}\n${await page.locator("body").ariaSnapshot()}`);
};
await page.goto(`${FRONT_URL}/operator`);
await dump("operator before");
await director("next");
await dump("operator after yellow");
await director("next?force=1");
await dump("operator after red");
const red = (await director("status", "GET")).live.find((e) => e.story === "red");
await page.goto(`${FRONT_URL}/events/${red.id}`);
await dump("event red");
await page.goto(`${FRONT_URL}/master`);
await dump("master");
await page.goto(`${FRONT_URL}/ohs/journal`);
await dump("journal");
await browser.close();
await director("reset");
