// Inspect the approved HRE renderer. This never casts or exports human votes.
const { chromium } = require(process.env.HACKATHON_BROWSER_NODE_PATH + '/playwright');
const fs = require('node:fs');
const path = require('node:path');
let browser;
(async () => {
  const [url, evidence, expectedItemsText] = process.argv.slice(2);
  const expectedItems = Number(expectedItemsText ?? 11);
  if (!url || !evidence) throw new Error('Pass the actual review-serve URL and a fresh evidence directory.');
  if (fs.existsSync(evidence)) throw new Error('Preserve previous evidence; use a new directory.');
  fs.mkdirSync(evidence, { recursive: true });
  browser = await chromium.launch({ executablePath: process.env.HACKATHON_CHROMIUM_EXECUTABLE, headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(url);
  await page.waitForFunction(() => document.querySelector('#asset-status')?.textContent === '0 broken assets · Evidence byte checks complete', null, { timeout: 60000 });
  if (await page.locator('.review-item').count() !== expectedItems) throw new Error('Unexpected working-product review item count.');
  if (await page.locator('input[type=radio]:checked').count()) throw new Error('Unexpected human verdict.');
  const manifestUrl = new URL(new URL(url).searchParams.get('manifest'), url).href;
  const manifest = await (await context.request.get(manifestUrl)).json();
  const images = manifest.artifacts.filter(a => a.kind === 'image');
  const videos = manifest.artifacts.filter(a => a.kind === 'video');
  if (images.length !== expectedItems * 4 || videos.length !== 4) throw new Error('Expected complete viewport/motion image variants and four recordings.');
  const decoded = await page.evaluate(async ({ images, manifestUrl }) => {
    const result = [];
    for (const a of images) {
      // The approved renderer deliberately allows only blob/data images in CSP.
      const response = await fetch(new URL(a.path, manifestUrl));
      if (!response.ok) throw new Error('Artifact HTTP status: ' + a.id);
      const blobUrl = URL.createObjectURL(await response.blob());
      const img = new Image(); img.src = blobUrl;
      await img.decode(); URL.revokeObjectURL(blobUrl);
      if (img.naturalWidth !== a.width || img.naturalHeight !== a.height) throw new Error('Image dimensions: ' + a.id);
      result.push({ id: a.id, width: img.naturalWidth, height: img.naturalHeight });
    }
    return result;
  }, { images, manifestUrl });
  for (const viewport of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
    await page.setViewportSize(viewport);
    await page.screenshot({ path: path.join(evidence, `hre-ui-${viewport.width}x${viewport.height}.png`) });
  }
  await page.locator('#motion').selectOption('reduced');
  await page.waitForFunction(() => [...document.querySelectorAll('.column.after img')].every(i => i.complete && i.naturalWidth > 0));
  if (await page.locator('.column.after img').count() !== expectedItems) throw new Error('Missing reduced-motion captures.');
  await page.locator('#motion').selectOption('normal');
  await page.locator('#media').selectOption('video');
  const video = page.locator('.column.after video').first();
  await video.waitFor();
  await video.evaluate(v => new Promise((resolve, reject) => {
    if (v.readyState >= 1) return resolve();
    v.onloadedmetadata = resolve; v.onerror = () => reject(new Error('Recording failed to decode'));
    v.load();
  }));
  if (await page.locator('input[type=radio]:checked').count()) throw new Error('QA changed a human verdict.');
  if (errors.length) throw new Error(errors.join('\n'));
  const receipt = { result: 'PASS', scope: 'Approved HRE renderer and source-bound working-product package; no human approval', url, manifest: manifest.review, source_sha256: manifest.revisions.current.snapshot_sha256, images: decoded.length, recordings: videos.length, states: manifest.states.length, renderer: await page.locator('#version').textContent(), human_verdicts: 'NONE', console_errors: errors, checks: ['sealed artifact byte checks', 'all image dimensions and decodes', expectedItems + ' unreviewed items', 'reduced-motion evidence', 'recording metadata decode', 'desktop/mobile review UI'] };
  fs.writeFileSync(path.join(evidence, 'review-qa.json'), JSON.stringify(receipt, null, 2) + '\n');
  console.log(JSON.stringify(receipt));
  await browser.close();
})().catch(async error => { console.error(error); await browser?.close(); process.exitCode = 1; });
