// Renders the PWA icons in public/icons from the header mark (aperture-eye) on graphite.
// No project dependency: pass any Playwright install, e.g.
//   node scripts/icons.mjs ../../sw-demo/tools/checkpoint-demo/node_modules/playwright
// Colours are read from src/styles/ds.css (--ds-bg-2 background, --ds-accent mark).
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const playwright = process.argv[2];
if (!playwright) { console.error("usage: node scripts/icons.mjs <path to playwright package>"); process.exit(1); }
const { chromium } = createRequire(import.meta.url)(path.resolve(playwright));
const css = readFileSync(path.join(root, "src/styles/ds.css"), "utf8");
const token = name => css.match(new RegExp(`--${name}:\\s*(#[0-9a-fA-F]{3,8})`))[1];
const bg = token("ds-bg-2"), mark = token("ds-accent");

const EYE = `<path d="M2 12c2.6-4.6 6-7 10-7s7.4 2.4 10 7c-2.6 4.6-6 7-10 7s-7.4-2.4-10-7Z" stroke-width="1.6"/>
  <circle cx="12" cy="12" r="4.2" stroke-width="1.6"/>
  <path d="M12 7.8v2.4M15.6 9.9l-2.1 1.2M15.6 14.1l-2.1-1.2M12 16.2v-2.4M8.4 14.1l2.1-1.2M8.4 9.9l2.1 1.2" stroke-width="1.2"/>`;
// scale: share of the canvas the eye spans; maskable keeps it inside the 80 % safe circle.
const svg = ({ scale, background = bg, color = mark }) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%">
  ${background ? `<rect width="24" height="24" fill="${background}"/>` : ""}
  <g transform="translate(12 12) scale(${scale}) translate(-12 -12)" fill="none" stroke="${color}">${EYE}</g></svg>`;

const ICONS = [
  ["icon-192.png", 192, { scale: .72 }],
  ["icon-512.png", 512, { scale: .72 }],
  ["maskable-512.png", 512, { scale: .5 }],
  ["maskable-192.png", 192, { scale: .5 }],
  ["apple-touch-icon.png", 180, { scale: .66 }],
  // Android status bar badge: white on transparent, the system tints it.
  ["badge-96.png", 96, { scale: .9, background: "", color: "#fff" }],
];
const browser = await chromium.launch();
for (const [file, size, opts] of ICONS) {
  const page = await browser.newPage({ viewport: { width: size, height: size } });
  await page.setContent(`<style>html,body{margin:0;background:transparent}</style>${svg(opts)}`);
  await page.screenshot({ path: path.join(root, "public/icons", file), omitBackground: true });
  await page.close();
  console.log("icons/" + file);
}
await browser.close();
