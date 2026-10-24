// Presentation-only QA: the browser harness is an image measurement surface.
// Do not run until the director has frozen the thirteen PNGs and notes.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = path.join(root, process.env.SAFEWATCH_BROWSER_EVIDENCE || 'evidence/browser-13');
const harnessBase = process.env.SAFEWATCH_CAPTURE_BASE || 'http://127.0.0.1:8744/';
const reviewURL = process.env.SAFEWATCH_REVIEW_URL || 'http://127.0.0.1:8745/msk-promhack/argus-final-presentation/presentations/final-argus-release/review-13/';
const playwrightFile = process.env.CRAFT_PLAYWRIGHT_MODULE || '/mnt/d/templates/msk-promhack/safewatch-checkpoint-mock/tools/checkpoint-demo/node_modules/playwright/index.mjs';
const chromiumFile = process.env.CRAFT_CHROMIUM || '/home/egor/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome';
const {chromium} = await import(pathToFileURL(playwrightFile).href);
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const readJSON = async file => JSON.parse((await fs.readFile(file, 'utf8')).replace(/^\uFEFF/, ''));
const notes = await readJSON(path.join(root, 'speaker-notes.json'));
const scenes = Array.isArray(notes) ? notes : notes.slides;
assert.equal(scenes.length, 13, 'Expected thirteen speaker-note objects');
const duration = scenes.reduce((sum, scene) => sum + Number(scene.duration), 0);
assert.equal(duration, 300, 'This release QA allocates exactly 300 seconds');
for (const scene of scenes) assert.ok(Number(scene.duration) > 0, 'Positive slide duration required');
try { await fs.access(path.join(out, 'report.json')); throw new Error('Refusing to overwrite browser report; use a new evidence revision.'); }
catch (error) { if (error.code !== 'ENOENT') throw error; }
await fs.mkdir(out, {recursive: true});
const sources = ['speaker-notes.json', 'craft/capture.html', ...scenes.map((_, index) => `slides/slide-${String(index + 1).padStart(2, '0')}.png`)];
const inventory = async () => Object.fromEntries(await Promise.all(sources.map(async file => [file, hash(await fs.readFile(path.join(root, file)))])));
const before = await inventory();
const report = {status: 'RUNNING', startedAt: new Date().toISOString(), checks: [], errors: [], screenshots: [],
  sourceInventory: before, projection: [], humanReview: {}, sequence: {},
  limits: ['Silent browser QA sequence, not a spoken rehearsal.', 'Human verdicts are never selected, imported, exported, or submitted by this script.', 'The harness measures existing images; it is not a presentation website.']};
const browser = await chromium.launch({headless: true, executablePath: chromiumFile});
report.browser = await browser.version();
const observe = (page, scope) => {
  page.on('pageerror', error => report.errors.push({scope, type: 'pageerror', message: error.message}));
  page.on('console', message => { if (message.type() === 'error') report.errors.push({scope, type: 'console', message: message.text()}); });
  page.on('requestfailed', request => { const error = request.failure()?.errorText; if (error !== 'net::ERR_ABORTED') report.errors.push({scope, type: 'request', message: request.url() + ': ' + error}); });
  page.on('response', response => { if (response.status() >= 400) report.errors.push({scope, type: 'http', message: `${response.status()} ${response.url()}`}); });
};
const holdURL = index => new URL(`craft/capture.html?slide=${index}`, harnessBase).href;
const settled = async (page, index) => {
  await page.locator('[data-craft-settled="true"]').waitFor();
  await page.locator('#slide').evaluate(image => image.decode());
  const result = await page.locator('#slide').evaluate(image => {
    const rect = image.getBoundingClientRect();
    return {src: image.currentSrc, complete: image.complete, naturalWidth: image.naturalWidth, naturalHeight: image.naturalHeight,
      rect: {x: rect.x, y: rect.y, width: rect.width, height: rect.height}, viewport: {width: innerWidth, height: innerHeight},
      overflow: document.documentElement.scrollWidth > innerWidth || document.documentElement.scrollHeight > innerHeight};
  });
  assert.ok(result.src.endsWith(`slide-${String(index).padStart(2, '0')}.png`), 'Wrong image state');
  assert.equal(result.naturalWidth, 1920); assert.equal(result.naturalHeight, 1080);
  assert.equal(result.rect.x, 0); assert.equal(result.rect.y, 0);
  assert.equal(result.rect.width, result.viewport.width); assert.equal(result.rect.height, result.viewport.height);
  assert.equal(result.overflow, false);
  return result;
};
try {
  // Craft supplies the complete 2×2 projection matrix; verify its actual receipt.
  const craftDirectory = process.env.SAFEWATCH_CRAFT_EVIDENCE || 'evidence/craft-13';
  const craft = await readJSON(path.join(root, craftDirectory, 'report.json'));
  assert.equal(craft.status, 'CAPTURED'); assert.equal(craft.sourceStable, true);
  assert.deepEqual(craft.runtimeErrors, []);
  const keys = new Set(craft.screenshots.map(shot => `${String(shot.state).padStart(2, '0')}|${shot.height}|${shot.motion}`));
  for (let n = 1; n <= 13; n++) for (const height of [1080, 720]) for (const motion of ['normal', 'reduced']) {
    assert.ok(keys.has(`${String(n).padStart(2, '0')}|${height}|${motion}`), 'Missing Craft projection state');
  }
  for (const shot of craft.screenshots) {
    assert.equal(hash(await fs.readFile(path.join(root, craftDirectory, shot.path))), shot.sha256, 'Craft screenshot hash changed');
  }
  report.checks.push('Craft receipt: all 52 semantic-state/size/motion captures present, stable, hash-checked, zero runtime errors.');
  // Independent current harness loads at both projection sizes.
  for (const viewport of [{width: 1920, height: 1080}, {width: 1280, height: 720}]) {
    const context = await browser.newContext({viewport, deviceScaleFactor: 1, reducedMotion: 'no-preference'});
    const page = await context.newPage(); observe(page, `projection-${viewport.height}`);
    try {
      for (let index = 1; index <= 13; index++) {
        await page.goto(holdURL(index));
        const observation = await settled(page, index);
        const file = `projection-${String(index).padStart(2, '0')}-${viewport.height}.png`;
        await page.screenshot({path: path.join(out, file)});
        report.projection.push({slide: index, viewport, url: page.url(), observation});
        report.screenshots.push({path: file, sha256: hash(await fs.readFile(path.join(out, file)))});
      }
    } finally { await context.close(); }
  }
  report.checks.push('All thirteen final images independently decoded and fit without clipping at 1920×1080 and 1280×720.');
  console.log('Projection QA passed. Checking unchanged Human Review Engine.');
  // A fresh context cannot restore any human draft from another session.
  const reviewContext = await browser.newContext({viewport: {width: 1440, height: 1000}});
  const reviewPage = await reviewContext.newPage(); observe(reviewPage, 'human-review');
  try {
    await reviewPage.goto(reviewURL);
    await reviewPage.waitForFunction(() => document.querySelector('#asset-status')?.textContent.includes('Evidence byte checks complete'), null, {timeout: 90000});
    assert.equal(await reviewPage.locator('#fatal:visible').count(), 0);
    assert.equal(await reviewPage.locator('#reviews article.review-item').count(), 13);
    assert.match(await reviewPage.locator('#asset-status').textContent(), /^0 broken assets/);
    assert.equal(await reviewPage.locator('input[type=radio]:checked').count(), 0);
    const manifestParam = new URL(reviewPage.url()).searchParams.get('manifest');
    assert.ok(manifestParam, 'Renderer manifest parameter missing');
    assert.equal(new URL(manifestParam, reviewPage.url()).origin, new URL(reviewPage.url()).origin, 'HRE manifest must be same-origin');
    for (const viewport of ['1080', '720']) for (const motion of ['normal', 'reduced']) {
      await reviewPage.selectOption('#viewport', viewport);
      await reviewPage.selectOption('#motion', motion);
      await reviewPage.waitForFunction(() => document.querySelectorAll('#reviews .after .frame img').length === 13 &&
        [...document.querySelectorAll('#reviews .after .frame img')].every(image => image.complete && image.naturalWidth > 0));
      assert.equal(await reviewPage.locator('#reviews .before .frame img').count(), 0, 'No historical BEFORE expected');
      assert.equal(await reviewPage.locator('input[type=radio]:checked').count(), 0);
      report.checks.push(`HRE ${viewport}/${motion}: thirteen AFTER images decoded; no fabricated BEFORE or selected verdict.`);
    }
    await reviewPage.selectOption('#viewport', '1080');
    await reviewPage.selectOption('#motion', 'normal');
    await reviewPage.waitForFunction(() => document.querySelectorAll('#reviews .after .frame img').length === 13 &&
      [...document.querySelectorAll('#reviews .after .frame img')].every(image => image.complete && image.naturalWidth > 0));
    await reviewPage.screenshot({path: path.join(out, 'review-desktop.png')});
    await reviewPage.locator('#reviews .after .frame button').first().click();
    await reviewPage.locator('#inspector[open]').waitFor();
    await reviewPage.locator('#inspection-image').evaluate(image => image.decode());
    assert.equal(await reviewPage.locator('#inspection-image').evaluate(image => image.naturalWidth), 1920);
    await reviewPage.screenshot({path: path.join(out, 'review-inspector.png')});
    await reviewPage.click('#close-inspector');
    assert.equal(await reviewPage.locator('#inspector[open]').count(), 0);
    assert.equal(await reviewPage.locator('input[type=radio]:checked').count(), 0);
    assert.match(await reviewPage.locator('#asset-status').textContent(), /^0 broken assets/);
    report.humanReview = {status: 'PASS', url: reviewPage.url(), items: 13, assetStatus: await reviewPage.locator('#asset-status').textContent(),
      checkedVerdicts: 0, inspectorOpenedAndClosed: true, sameOriginManifest: true};
  } finally { await reviewContext.close(); }
  assert.deepEqual(report.errors, []);
  // Full silent QA sequence. Each planned hold is measured after its real image decodes.
  // The browser records original speed. Navigation overhead is reported separately.
  if(process.env.ARGUS_FAST_QA !== '1') {
  const sequenceContext = await browser.newContext({viewport: {width: 1280, height: 720}, deviceScaleFactor: 1,
    reducedMotion: 'no-preference', recordVideo: {dir: out, size: {width: 1280, height: 720}}});
  const sequencePage = await sequenceContext.newPage(); observe(sequencePage, 'sequence');
  const video = sequencePage.video();
  const sequenceStart = Date.now();
  const timeline = [];
  console.log('Starting full silent sequence: thirteen static images, 300 seconds of planned holds.');
  try {
    for (let index = 1; index <= 13; index++) {
      await sequencePage.goto(holdURL(index));
      await settled(sequencePage, index);
      const holdStart = Date.now();
      const deadline = holdStart + Number(scenes[index - 1].duration) * 1000;
      console.log(`Sequence slide ${index}/13 settled; planned hold ${scenes[index - 1].duration}s.`);
      while (Date.now() < deadline) {
        await new Promise(resolve => setTimeout(resolve, Math.min(15000, deadline - Date.now())));
        console.log(`Sequence heartbeat: slide ${index}/13, elapsed ${((Date.now() - sequenceStart) / 1000).toFixed(1)}s.`);
      }
      timeline.push({slide: index, url: sequencePage.url(), plannedDurationSeconds: Number(scenes[index - 1].duration),
        settledAtSeconds: (holdStart - sequenceStart) / 1000, actualHoldSeconds: (Date.now() - holdStart) / 1000});
    }
  } finally { await sequenceContext.close(); }
  const sequenceFile = path.join(out, 'complete-300s-sequence.webm');
  await video.saveAs(sequenceFile);
  report.sequence = {status: 'PASS', kind: 'silent QA image navigation, not narrated rehearsal', path: path.basename(sequenceFile),
    plannedHoldSeconds: duration, elapsedSeconds: (Date.now() - sequenceStart) / 1000, viewport: {width: 1280, height: 720},
    motion: 'normal', timeline, sha256: hash(await fs.readFile(sequenceFile))};
  assert.ok(report.sequence.elapsedSeconds >= 300);
  } else report.sequence={status:'NOT_RUN',reason:'User explicitly prioritized delivery before18:00; static projection and HRE checks completed,full silent hold sequence omitted.'};
  assert.deepEqual(report.errors, []);
  report.sourceInventoryAfter = await inventory();
  report.sourceStable = JSON.stringify(before) === JSON.stringify(report.sourceInventoryAfter);
  assert.equal(report.sourceStable, true, 'Source slides/notes/harness changed during QA');
  if(report.sequence.status==='PASS')report.checks.push('Complete original-speed300-second silent sequence recorded.');
  report.status = 'PASS';
} catch (error) {
  report.status = 'FAIL'; report.failure = error.stack; process.exitCode = 1;
} finally {
  await browser.close();
  report.finishedAt = new Date().toISOString();
  await fs.writeFile(path.join(out, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({status: report.status, checks: report.checks.length, errors: report.errors.length, report: path.join(out, 'report.json')}));
}
