// Verify the actual approved HRE and evidence package, without casting votes.
const { chromium } = require(process.env.HACKATHON_BROWSER_NODE_PATH + '/playwright');
const fs = require('node:fs');
const path = require('node:path');
let browser;

(async () => {
  const [url, evidence] = process.argv.slice(2);
  if (!url || !evidence) throw new Error('Pass HRE URL and a new evidence directory.');
  fs.mkdirSync(evidence, { recursive: true });
  browser = await chromium.launch({ executablePath: process.env.HACKATHON_CHROMIUM_EXECUTABLE, headless: true });
  const errors = [];
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
  await page.goto(url);
  await page.waitForFunction(() => document.querySelector('#title')?.textContent.includes('HUMAN_CONCEPT_REVIEW'));
  await page.waitForFunction(() => document.querySelector('#asset-status')?.textContent === '0 broken assets · Evidence byte checks complete', null, { timeout: 60000 });
  if (await page.locator('.review-item').count() !== 6) throw new Error('Expected six concept directions.');
  if (await page.locator('input[type=radio]:checked').count()) throw new Error('A human verdict was preselected.');
  await page.waitForFunction(() => [...document.querySelectorAll('.column.after img')].every(image => image.complete && image.naturalWidth > 0));
  await page.screenshot({ path: path.join(evidence, 'hre-ui-1440x900.png') });
  const ids = await page.locator('.review-item').evaluateAll(items => items.map(item => item.id.slice(5)));
  const inspected = [];
  for (const id of ids) {
    const select = page.locator('#state-' + id);
    const options = await select.locator('option').evaluateAll(nodes => nodes.map(node => node.value));
    if (options.length < 2) throw new Error('Missing second concept frame: ' + id);
    for (const option of options) {
      await select.selectOption(option);
      const image = page.locator('#item-' + id + ' .column.after img');
      await image.waitFor();
      await image.evaluate(node => node.decode());
      inspected.push({ id, state: option, size: await image.evaluate(node => [node.naturalWidth, node.naturalHeight]) });
    }
    await select.selectOption(options[0]);
  }
  await page.locator('#item-evidence-desk .column.after button').click();
  if (!(await page.locator('#inspector').isVisible())) throw new Error('Original-pixel inspection did not open.');
  await page.locator('#image-size').click();
  await page.keyboard.press('Escape');
  if (await page.locator('#inspector').isVisible()) throw new Error('Escape did not close inspection.');
  await page.locator('#motion').selectOption('reduced');
  if (await page.locator('.column.after img').count()) throw new Error('HRE substituted ordinary concepts for missing reduced-motion evidence.');
  await page.locator('#motion').selectOption('normal');
  await page.locator('#media').selectOption('video');
  if (await page.locator('.column.after video').count()) throw new Error('A recording was invented.');
  await page.locator('#media').selectOption('image');
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.screenshot({ path: path.join(evidence, 'hre-ui-1280x800.png') });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({ path: path.join(evidence, 'hre-ui-390x844.png') });
  const comparison = page.locator('#item-signal-post .review-scroll');
  const scroll = await comparison.evaluate(node => ({ width: node.clientWidth, scrollWidth: node.scrollWidth }));
  if (scroll.scrollWidth <= scroll.width) throw new Error('Mobile comparison does not preserve horizontally scrollable columns.');
  if (await page.locator('input[type=radio]:checked').count()) throw new Error('QA changed a human verdict.');
  if (errors.length) throw new Error(errors.join('\n'));
  const report = {
    status: 'PASS', scope: 'Approved HRE renderer and actual image concept package only; not SafeWatch runtime QA',
    url, viewports: [[1440, 900], [1280, 800], [390, 844]],
    renderer: await page.locator('#version').textContent(), decodedConceptFrames: inspected,
    checks: ['six directions', 'all package artifact byte checks', 'twelve original image decodes', 'no preselected or cast human verdicts', 'original pixel inspection', 'Escape returns', 'missing reduced motion remains missing', 'missing recordings remain missing', 'mobile comparison scroll'],
    consoleErrors: errors, human_decisions: 'NONE', product_integration: 'NOT RUN', product_screenshots: 'NONE'
  };
  fs.writeFileSync(path.join(evidence, 'review-qa.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({ status: report.status, frames: inspected.length, renderer: report.renderer, human_decisions: 'NONE' }));
  await browser.close();
})().catch(async error => { console.error(error); await browser?.close(); process.exitCode = 1; });
