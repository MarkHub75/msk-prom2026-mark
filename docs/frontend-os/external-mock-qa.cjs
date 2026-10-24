#!/usr/bin/env node
'use strict';
// Reusable external checkpoint-mock QA. Own this isolated mock exclusively while running.
// node docs/frontend-os/external-mock-qa.cjs --base http://127.0.0.1:5185 --rest http://127.0.0.1:4010 --out /absolute/new-evidence-dir
// Business actions use visible application controls. Only /__demo controls mutate the mock directly.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { execFileSync } = require('node:child_process');
let pw;
try {
    pw = require(process.env.SAFEWATCH_PLAYWRIGHT || 'playwright');
}
catch {
    pw = require('/home/egor/md-hardening/frontend/node_modules/playwright');
}
const args = process.argv.slice(2);
const arg = (name, fallback) => args.includes(name) ? args[args.indexOf(name) + 1] : fallback;
const base = arg('--base', 'http://127.0.0.1:5185').replace(/\/$/, '');
const rest = arg('--rest', 'http://127.0.0.1:4010').replace(/\/$/, '');
const out = path.resolve(arg('--out', '/mnt/d/templates/frontend-hackathon-os/production/runs/safewatch-20261024-working-r3/evidence/external-mock-v1'));
const workspace = path.resolve(__dirname, '../..');
const actor = 'Внешний QA';
fs.mkdirSync(out, { recursive: true });
if (fs.existsSync(path.join(out, 'raw-observations.json')))
    throw Error('Evidence already exists; use a new --out directory.');
const raw = { scope: 'External checkpoint stateful REST/WS mock through Vite dev:mock; review=real, never in-browser review fixtures', started_at: new Date().toISOString(), base, rest, actor, browser_path: 'Browser plugin unavailable; installed Playwright and Chromium', cases: [], observations: [], findings: [], limitations: [], director: [], server_reads: [], network: [], websockets: [], served_frontend: [], console: [], page_errors: [], request_failures: [], captures: [] };
const now = () => new Date().toISOString();
const save = () => fs.writeFileSync(path.join(out, 'raw-observations.json'), JSON.stringify(raw, null, 2) + '\n');
const pending = new Set();
function track(promise) { pending.add(promise); promise.finally(() => pending.delete(promise)); }
function note(name, observed) { raw.observations.push({ name, at: now(), observed }); save(); console.log(name, JSON.stringify(observed)); }
function requireThat(condition, message, observed) { if (!condition) {
    const e = Error(message);
    e.observed = observed;
    throw e;
} }
function finding(severity, message, observed, evidence) { raw.findings.push({ severity, message, observed, evidence }); save(); console.log('FINDING', severity, message); }
async function runCase(name, fn) { const c = { name, started_at: now(), result: 'RUNNING' }; raw.cases.push(c); save(); try {
    await fn();
    c.result = 'PASS';
}
catch (e) {
    c.result = 'FAIL';
    c.error = e.message;
    c.observed = e.observed;
    c.stack = e.stack;
    finding('BLOCKER', name + ': ' + e.message, e.observed);
}
finally {
    c.completed_at = now();
    save();
} }
async function control(command) { const r = await fetch(rest + '/__demo/' + command, { method: command === 'status' ? 'GET' : 'POST' }); const body = await r.json(); raw.director.push({ at: now(), command, status: r.status, body }); save(); requireThat(r.ok, 'Director failed ' + command, { status: r.status, body }); return body; }
async function readApi(route, role = 'operator') { const r = await fetch(rest + route, { headers: { 'X-Role': role, 'X-Actor': encodeURIComponent(actor) } }); const type = r.headers.get('content-type') || ''; const body = type.includes('json') ? await r.json() : { bytes: (await r.arrayBuffer()).byteLength }; const result = { at: now(), route, role, status: r.status, content_type: type, body }; raw.server_reads.push(result); save(); return result; }
function sourceIdentity() { const manifest = {}; const hash = b => crypto.createHash('sha256').update(b).digest('hex'); function walk(dir) { for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory())
        walk(p);
    else if (entry.isFile())
        manifest[path.relative(workspace, p)] = hash(fs.readFileSync(p));
} } for (const dir of ['frontend/src', 'frontend/public'])
    walk(path.join(workspace, dir)); for (const f of ['frontend/index.html', 'frontend/package.json', 'frontend/package-lock.json', 'frontend/vite.config.ts'])
    if (fs.existsSync(path.join(workspace, f)))
        manifest[f] = hash(fs.readFileSync(path.join(workspace, f))); const ordered = Object.fromEntries(Object.entries(manifest).sort(([a], [b]) => a.localeCompare(b))); return { method: 'SHA256 of JSON of sorted frontend source/public/config per-file SHA256 map; independent of OS frozen-source identity', files: ordered, sha256: hash(JSON.stringify(ordered)), git_head: execFileSync('git', ['rev-parse', 'HEAD'], { cwd: workspace, encoding: 'utf8' }).trim() }; }
async function newPage(browser, scenario, viewport = { width: 1440, height: 900 }) { const context = await browser.newContext({ viewport }); const page = await context.newPage(); page.setDefaultTimeout(10000); page.on('console', m => { if (['error', 'warning'].includes(m.type())) {
    raw.console.push({ at: now(), scenario, type: m.type(), text: m.text(), location: m.location() });
    save();
} }); page.on('pageerror', e => { raw.page_errors.push({ at: now(), scenario, message: e.message, stack: e.stack }); save(); }); page.on('requestfailed', r => { raw.request_failures.push({ at: now(), scenario, url: r.url(), failure: r.failure() }); save(); }); const requests = new WeakMap(); page.on('request', r => { if (!r.url().startsWith(rest + '/api/'))
    return; const h = r.headers(); const n = { at: now(), scenario, url: r.url(), method: r.method(), resource_type: r.resourceType(), headers: { 'x-role': h['x-role'] || null, 'x-actor': h['x-actor'] || null }, body: r.postData() }; requests.set(r, n); raw.network.push(n); save(); }); page.on('response', r => {
        const u = new URL(r.url());
        if (u.origin !== new URL(base).origin || !u.pathname.startsWith('/src/') || r.request().resourceType() !== 'script') return;
        track((async () => {
            try {
                const bytes = await r.body();
                const sourcePath = 'frontend' + u.pathname;
                const expected = raw.source_before.files[sourcePath];
                const match = bytes.toString('utf8').match(/sourceMappingURL=data:application\/json;base64,([A-Za-z0-9+/=]+)/);
                const sourceMap = match ? JSON.parse(Buffer.from(match[1], 'base64').toString('utf8')) : null;
                const sourceContentHashes = (sourceMap?.sourcesContent || []).filter(x => typeof x === 'string').map(x => crypto.createHash('sha256').update(x).digest('hex'));
                raw.served_frontend.push({scenario,url:r.url(),status:r.status(),source_path:sourcePath,source_file_sha256:expected || null,served_js_sha256:crypto.createHash('sha256').update(bytes).digest('hex'),source_map_content_sha256:sourceContentHashes,source_map_matches_current_file:expected ? sourceContentHashes.includes(expected) : null});
                save();
            } catch(e) {raw.served_frontend.push({scenario,url:r.url(),read_error:e.message});save();}
        })());
    });
    page.on('response', r => { const n = requests.get(r.request()); if (!n)
    return; track((async () => { n.response_at = now(); n.status = r.status(); n.content_type = r.headers()['content-type']; try {
    if (n.content_type?.includes('json'))
        n.response_body = await r.json();
}
catch (e) {
    n.body_read_error = e.message;
} save(); })()); }); page.on('websocket', ws => { if (!ws.url().includes(':4011/'))
    return; const entry = { scenario, url: ws.url(), opened_at: now(), frames: [] }; raw.websockets.push(entry); ws.on('framereceived', f => { let payload = String(f.payload); try {
    payload = JSON.parse(payload);
}
catch { } entry.frames.push({ at: now(), payload }); save(); }); ws.on('close', () => { entry.closed_at = now(); save(); }); ws.on('socketerror', e => { entry.error = String(e); save(); }); save(); }); return { context, page, scenario }; }
async function settle(page) { await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(120); }
async function capture(page, name) { await settle(page); await page.screenshot({ path: path.join(out, name + '.png'), fullPage: false }); fs.writeFileSync(path.join(out, name + '.txt'), await page.locator('body').innerText()); raw.captures.push({ name, file: name + '.png', url: page.url(), viewport: page.viewportSize(), at: now() }); save(); }
async function layout(page, label) { const v = await page.evaluate(() => ({ width: innerWidth, height: innerHeight, document_width: document.documentElement.scrollWidth, overlay: !!document.querySelector('vite-error-overlay,nextjs-portal') })); note('layout:' + label, v); requireThat(v.document_width <= v.width && !v.overlay, 'Layout/overlay failure', v); }
async function realMode(page) { const observed = await page.evaluate(() => ({ review_mode: sessionStorage.getItem('safewatch.review.mode.v1'), backend: document.querySelector('[data-testid=backend]')?.textContent, review_strip: !!document.querySelector('.review-strip') })); note('external_real_mode', observed); requireThat(observed.review_mode === null && !observed.review_strip && observed.backend !== 'REVIEW', 'Internal fixtures enabled', observed); }
async function role(page, id) { const select = page.locator('select[aria-label="Роль"]'); if (await select.isVisible())
    await select.selectOption(id);
else {
    const meta = await readApi('/api/meta');
    const title = meta.body.roles.find(x => x.id === id).title;
    await page.getByRole('button', { name: title, exact: true }).click();
} }
async function serverStatus(id, expected, roleName) { let r; for (let i = 0; i < 40; i++) {
    r = await readApi('/api/events/' + id, roleName);
    if (r.status === 200 && r.body.event.status === expected)
        return r.body;
    await new Promise(resolve => setTimeout(resolve, 100));
} throw Error('Server status not reached ' + id + ' ' + expected + ' actual ' + JSON.stringify(r)); }
async function uiStatus(page, detail) { await page.waitForFunction(text => [...document.querySelectorAll('[data-testid="event-status"]')].some(x => x.textContent.trim() === text), detail.event.status_title); note('ui_server_status', { event_id: detail.event.id, enum: detail.event.status, title: detail.event.status_title, actual: await page.getByTestId('event-status').allTextContents() }); }
async function namedAction(page, scenario, action, captureName, testCancel = false) {
    const before = raw.network.filter(r => r.scenario === scenario && r.method === 'POST' && /\/api\/events\/\d+\/actions$/.test(new URL(r.url).pathname)).length;
    const unnamed = await page.evaluate(() => ({ actor: localStorage.getItem('safewatch.actor') }));
    requireThat(!unnamed.actor?.trim(), 'Fresh context unexpectedly has an actor', unnamed);
    const priorRequests = raw.network.filter(r => r.scenario === scenario);
    requireThat(priorRequests.every(r => !r.headers['x-actor']), 'Unnamed requests fabricate X-Actor', priorRequests.map(r => ({ url: r.url, actor: r.headers['x-actor'] })));
    requireThat(before === 0, 'Unnamed context auto-posted view/action', raw.network.filter(r => r.scenario === scenario && r.method === 'POST'));
    const button = page.locator('button[data-action="' + action + '"]');
    await button.click();
    const dialog = page.getByRole('dialog', { name: 'Представьтесь для действия', exact: true });
    await dialog.waitFor();
    await page.waitForTimeout(150);
    const posts = () => raw.network.filter(r => r.scenario === scenario && r.method === 'POST' && /\/api\/events\/\d+\/actions$/.test(new URL(r.url).pathname));
    requireThat(posts().length === before, 'Action was posted before explicit identity', posts());
    await layout(page, captureName);
    await capture(page, captureName);
    if (testCancel) {
        await dialog.getByRole('button', { name: 'Отмена', exact: true }).click();
        await dialog.waitFor({ state: 'hidden' });
        requireThat(posts().length === before, 'Cancel posted an action', posts());
        await button.click();
        await dialog.waitFor();
    }
    const input = dialog.getByLabel('Ваше имя', { exact: true });
    await input.fill('   ');
    const submit = dialog.getByRole('button', { name: 'Сохранить имя и продолжить', exact: true });
    if (await submit.isEnabled())
        await submit.click();
    requireThat(await dialog.isVisible() && posts().length === before, 'Whitespace identity was accepted', posts());
    await input.fill(actor);
    await submit.click();
    await dialog.waitFor({ state: 'hidden' });
    note('explicit_identity_guard', { scenario, action, before, unnamed, actor_entered: actor, cancel_checked: testCancel, first_action_requests: posts().map(r => ({ url: r.url, body: r.body, headers: r.headers })) });
}
function hellos(scenario) { return raw.websockets.filter(w => w.scenario === scenario).flatMap(w => w.frames).filter(f => f.payload?.type === 'hello'); }
async function waitForObserved(predicate, description, ms = 10000) { const start = Date.now(); while (Date.now() - start < ms) {
    if (predicate())
        return;
    await new Promise(r => setTimeout(r, 100));
} throw Error('Observation timeout: ' + description); }
async function waitConnected(page) { await page.locator('.connection[data-status="connected"]').waitFor({ state: 'attached' }); }
let browser;
(async () => {
    raw.source_before = sourceIdentity();
    raw.tool_versions = { node: process.version, playwright: require('/home/egor/md-hardening/frontend/node_modules/playwright/package.json').version };
    save();
    browser = await pw.chromium.launch({ headless: true, executablePath: process.env.SAFEWATCH_CHROMIUM || '/home/egor/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome', args: ['--no-sandbox'] });
    raw.tool_versions.chromium = browser.version();
    let core, master, red, yellow, resolved;
    await runCase('external operator -> yellow -> red takeover -> mobile master resolve', async () => {
        await control('reset');
        core = await newPage(browser, 'core');
        const p = core.page;
        await p.goto(base + '/operator?review=real');
        await p.getByTestId('operator-view').waitFor();
        await waitConnected(p);
        await realMode(p);
        note('fresh_unnamed_operator', { actor: await p.evaluate(() => localStorage.getItem('safewatch.actor')), action_requests: raw.network.filter(r => ['core', 'core-master'].includes(r.scenario) && r.method === 'POST') });
        const empty = await readApi('/api/operator/dashboard');
        requireThat(empty.body.feed.length === 0, 'Initial external feed not empty', empty);
        await layout(p, 'empty1440');
        await capture(p, '01-operator-empty-1440');
        yellow = (await control('next')).published;
        requireThat(yellow?.level === 'yellow', 'Director did not publish yellow', yellow);
        await p.locator('a[href="/events/' + yellow.id + '"]').first().waitFor();
        await p.locator('a[href="/events/' + yellow.id + '"]').first().click();
        await p.getByTestId('incident-focus').waitFor();
        await p.locator('button[data-action="confirm"]').waitFor();
        const y = await readApi('/api/events/' + yellow.id);
        requireThat(y.body.episode?.evidence?.length > 0, 'External live evidence missing', y);
        const img = p.locator('.evidence-image-wrap img');
        await img.waitFor();
        await p.waitForFunction(() => { const i = document.querySelector('.evidence-image-wrap img'); return i && i.complete && i.naturalWidth > 0; });
        note('relative_evidence', { relative_url: y.body.episode.evidence[0].url, actual_src: await img.getAttribute('src'), image: await img.evaluate(i => ({ naturalWidth: i.naturalWidth, naturalHeight: i.naturalHeight, complete: i.complete })) });
        requireThat((await img.getAttribute('src')).startsWith(rest + '/api/evidence/'), 'Evidence bypasses configured REST origin');
        await capture(p, '02-yellow-incident-1440');
        await namedAction(p, 'core', 'confirm', '02a-identity-dialog-1440', true);
        await uiStatus(p, await serverStatus(yellow.id, 'confirmed', 'operator'));
        await capture(p, '02b-yellow-confirmed-1440');
        red = (await control('next')).published;
        requireThat(red?.level === 'red', 'Director did not publish red', red);
        await p.getByRole('alertdialog', { name: 'Критическое событие' }).waitFor();
        requireThat(new URL(p.url()).pathname === '/events/' + red.id && new URL(p.url()).searchParams.get('takeover') === '1', 'WS takeover did not navigate', p.url());
        await capture(p, '03-red-takeover-1440');
        await p.getByRole('button', { name: 'Свернуть' }).click();
        await p.locator('button[data-action="confirm"]').click();
        const handed = await serverStatus(red.id, 'sent_to_master', 'operator');
        await uiStatus(p, handed);
        const actions = handed.actions.map(a => a.action);
        requireThat(actions.includes('confirmed') && actions.includes('sent_to_master'), 'Red confirmation lacks dual history', handed.actions);
        note('red_dual_history', handed.actions);
        await capture(p, '04-red-handoff-1440');
        master = await newPage(browser, 'core-master', { width: 390, height: 844 });
        const m = master.page;
        await m.goto(base + '/master?review=real');
        await m.getByTestId('master-inbox').waitFor();
        await waitConnected(m);
        await realMode(m);
        await m.locator('a[href="/master/events/' + red.id + '"]').first().waitFor();
        await layout(m, 'master-inbox390');
        await capture(m, '05-master-inbox-390');
        await m.locator('a[href="/master/events/' + red.id + '"]').first().click();
        await m.getByTestId('master-detail').waitFor();
        await capture(m, '06-master-pending-390');
        await namedAction(m, 'core-master', 'accept', '06a-identity-dialog-master-390');
        await uiStatus(m, await serverStatus(red.id, 'master_accepted', 'master'));
        const finish = m.locator('button[data-action="resolve"]');
        requireThat(await finish.isDisabled(), 'Empty measures allow resolve');
        await m.getByTestId('measures').fill('   ');
        requireThat(await finish.isDisabled(), 'Whitespace measures allow resolve');
        await capture(m, '07-master-accepted-390');
        const comment = 'Внешний мок: участок ограждён, оборудование остановлено, выполнен осмотр.';
        await m.getByTestId('measures').fill(comment);
        await finish.click();
        resolved = await serverStatus(red.id, 'resolved', 'master');
        await uiStatus(m, resolved);
        requireThat(resolved.actions.some(a => a.action === 'resolved' && a.comment === comment && a.actor_name === actor), 'Resolve comment/actor not persisted', resolved.actions);
        await layout(m, 'master-resolved390');
        await capture(m, '08-master-resolved-390');
        await m.reload();
        await m.getByTestId('master-detail').waitFor();
        await uiStatus(m, resolved);
        await realMode(m);
        note('resolved_server_detail', resolved);
    });
    await runCase('journal UI and external journal server state', async () => {
        requireThat(master && resolved, 'Core prerequisite not completed');
        const p = master.page;
        await role(p, 'ohs');
        await p.waitForURL('**/ohs/journal');
        const journal = await readApi('/api/events', 'ohs');
        const row = journal.body.items?.find(e => e.id === red.id);
        requireThat(row?.status === 'resolved', 'Resolved event missing from external journal', journal);
        note('external_journal_resolved_row', row);
        await capture(p, '09-journal-390');
        await p.setViewportSize({ width: 1440, height: 900 });
        await capture(p, '10-journal-1440');
        const text = await p.locator('body').innerText();
        const stub = text.includes('Раздел запланирован');
        const fetched = raw.network.filter(n => n.scenario === 'core-master' && new URL(n.url).pathname === '/api/events');
        note('journal_ui_observed', { url: p.url(), stub, visible_text: text, journal_api_requests: fetched });
        requireThat(!stub && text.includes('#' + red.id), 'Journal UI remains a stub although external /api/events contains resolved event', { event_id: red.id, stub, actual_text: text });
        const selects = p.locator('select');
        let statusFilter, levelFilter;
        for (let i = 0; i < await selects.count(); i++) {
            const select = selects.nth(i);
            const values = await select.locator('option').evaluateAll(es => es.map(e => e.value));
            if (values.includes('resolved') && values.includes('new'))
                statusFilter = select;
            if (values.includes('red') && values.includes('yellow'))
                levelFilter = select;
        }
        requireThat(statusFilter && levelFilter, 'Journal status/level filter controls missing', await selects.evaluateAll(es => es.map(e => ({ label: e.getAttribute('aria-label'), options: [...e.options].map(o => o.value) }))));
        const filteredResponse = p.waitForResponse(r => { const u = new URL(r.url()); return u.origin === rest && u.pathname === '/api/events' && u.searchParams.get('status') === 'resolved' && u.searchParams.get('level') === 'red' && r.status() === 200; });
        await levelFilter.selectOption('red');
        await statusFilter.selectOption('resolved');
        await p.getByRole('button', { name: 'Найти', exact: true }).click();
        const filtered = await (await filteredResponse).json();
        requireThat(filtered.items?.length > 0 && filtered.items.every(e => e.level === 'red' && e.status === 'resolved') && filtered.items.some(e => e.id === red.id), 'Journal filters do not match external server data', filtered);
        await capture(p, '10a-journal-filtered-red-resolved-1440');
        const refreshedResponse = p.waitForResponse(r => { const u = new URL(r.url()); return u.origin === rest && u.pathname === '/api/events' && u.searchParams.get('status') === 'resolved' && u.searchParams.get('level') === 'red' && r.status() === 200; });
        await p.getByRole('button', { name: /^Обновить/ }).click();
        const refreshed = await (await refreshedResponse).json();
        requireThat(refreshed.items?.some(e => e.id === red.id), 'Journal reload lost resolved external event', refreshed);
        note('journal_filters_and_reload', { filters: { level: await levelFilter.inputValue(), status: await statusFilter.inputValue() }, filtered, refreshed, url: p.url() });
        await p.setViewportSize({ width: 390, height: 844 });
        await layout(p, 'journal-filtered390');
        await capture(p, '10b-journal-filtered-390');
        await p.reload();
        await p.locator('a[href="/events/' + red.id + '"]').first().waitFor();
        note('journal_browser_reload', { url: p.url(), resolved_link_visible: await p.locator('a[href="/events/' + red.id + '"]').first().isVisible(), body: await p.locator('body').innerText() });
    });
    await runCase('historical episode:null detail and mock camera501', async () => { const x = await newPage(browser, 'historical'); const d = await readApi('/api/events/1', 'operator'); requireThat(d.status === 200 && d.body.episode === null, 'Historical fixture is not episode:null', d); await x.page.goto(base + '/events/1?review=real'); await x.page.getByTestId('incident-focus').waitFor(); await x.page.getByRole('heading', { name: 'Доказательство отсутствует', exact: true }).waitFor(); await x.page.getByRole('heading', { name: 'Запись не привязана', exact: true }).waitFor(); await layout(x.page, 'historical1440'); await capture(x.page, '11-historical-null-1440'); await x.page.setViewportSize({ width: 390, height: 844 }); await layout(x.page, 'historical390'); await capture(x.page, '12-historical-null-390'); await x.page.setViewportSize({ width: 1280, height: 800 }); await x.page.goto(base + '/operator/cameras/1?review=real'); await x.page.getByTestId('camera-view').waitFor(); await x.page.getByRole('alert').waitFor(); const camera = await readApi('/api/cameras/1/view'); requireThat(camera.status === 501, 'Unexpected camera endpoint status', camera); raw.limitations.push({ kind: 'external_mock_capability', message: 'Camera view/video/HUD/broadcast/preview unavailable in checkpoint mock; actual camera view501 is an expected mock limitation.', observed: camera }); await layout(x.page, 'camera501-1280'); await capture(x.page, '13-camera501-1280'); await x.context.close(); });
    await runCase('WS reset/drop reconnect and dashboard REST reconciliation', async () => { await control('reset'); const x = await newPage(browser, 'dashboard-reconnect'); const p = x.page; await p.goto(base + '/operator?review=real'); await p.getByTestId('operator-view').waitFor(); await waitConnected(p); const a = (await control('next')).published; await p.locator('a[href="/events/' + a.id + '"]').first().waitFor(); const start = now(), n = hellos(x.scenario).length; await control('reset'); await waitForObserved(() => hellos(x.scenario).length > n, 'new hello after reset'); await waitForObserved(() => raw.network.some(r => r.scenario === x.scenario && r.at > start && new URL(r.url).pathname === '/api/operator/dashboard' && r.status === 200 && r.response_body?.feed?.length === 0), 'empty dashboard REST after reset'); await p.locator('a[href="/events/' + a.id + '"]').first().waitFor({ state: 'hidden' }); note('dashboard_reset_reconciliation', { removed_event_id: a.id, new_hello: hellos(x.scenario).at(-1), requests: raw.network.filter(r => r.scenario === x.scenario && r.at > start && new URL(r.url).pathname === '/api/operator/dashboard') }); await capture(p, '14-dashboard-reset-cleared'); const n2 = hellos(x.scenario).length, dropAt = now(); await control('ws-drop'); await p.locator('.offline-strip').waitFor({ state: 'visible' }); await capture(p, '15-ws-disconnected'); await waitForObserved(() => hellos(x.scenario).length > n2, 'hello after explicit ws-drop'); await waitForObserved(() => raw.network.some(r => r.scenario === x.scenario && r.at > dropAt && new URL(r.url).pathname === '/api/operator/dashboard' && r.status === 200), 'REST after ws-drop hello'); await waitConnected(p); note('ws_drop_reconciliation', { new_hello: hellos(x.scenario).at(-1), dashboard_after_drop: raw.network.filter(r => r.scenario === x.scenario && r.at > dropAt && new URL(r.url).pathname === '/api/operator/dashboard') }); await x.context.close(); });
    await runCase('incident reset404 stale detail/actions probe', async () => { await control('reset'); const event = (await control('next')).published; const x = await newPage(browser, 'incident-reset404'); const p = x.page; await p.goto(base + '/events/' + event.id + '?review=real'); await p.locator('button[data-action="confirm"]').waitFor(); await waitConnected(p); const before = { status: await p.getByTestId('event-status').allTextContents(), actions: await p.locator('[data-action]').evaluateAll(es => es.map(e => ({ action: e.dataset.action, disabled: e.disabled, text: e.innerText }))) }; const resetAt = now(), n = hellos(x.scenario).length; await control('reset'); await waitForObserved(() => hellos(x.scenario).length > n, 'new hello after incident reset'); await waitForObserved(() => raw.network.some(r => r.scenario === x.scenario && r.at > resetAt && new URL(r.url).pathname === '/api/events/' + event.id && r.status === 404), 'incident REST404 after reset'); await p.getByRole('alert').first().waitFor(); const server = await readApi('/api/events/' + event.id); const after = { status: await p.getByTestId('event-status').allTextContents(), actions: await p.locator('[data-action]').evaluateAll(es => es.map(e => ({ action: e.dataset.action, disabled: e.disabled, text: e.innerText }))), alerts: await p.getByRole('alert').allTextContents(), body: await p.locator('body').innerText() }; note('incident_reset404', { event_id: event.id, before, after, server }); await capture(p, '16-incident-reset404'); const stale = after.actions.some(a => !a.disabled) || after.status.length > 0; requireThat(!stale, 'Deleted external event retains stale detail/actions after fresh REST404', { event_id: event.id, before, after, server }); await x.context.close(); });
    await runCase('evidence404 -> fault-off sameURL card refresh', async () => { await control('reset'); const event = (await control('next')).published; await control('fault/evidence-404'); const x = await newPage(browser, 'evidence-recovery'); const p = x.page; await p.goto(base + '/events/' + event.id + '?review=real'); await p.getByRole('heading', { name: 'Кадр не загрузился', exact: true }).waitFor(); await capture(p, '17-evidence404'); const failedRequests = raw.network.filter(n => n.scenario === x.scenario && new URL(n.url).pathname.startsWith('/api/evidence/')); await control('fault/off'); const external = await readApi('/api/evidence/1/image'); requireThat(external.status === 200 && external.content_type.includes('image/'), 'Evidence did not recover on external server', external); const offAt = now(); const retry = p.locator('.evidence-panel').getByRole('button', { name: /Повторить|Загрузить.*(?:снова|повторно)|Обновить.*кадр/i }).first(); const retryMechanism = await retry.isVisible() ? await retry.innerText() : 'card Обновить'; if (await retry.isVisible())
        await retry.click();
    else
        await p.getByTestId('incident-focus').getByRole('button', { name: 'Обновить', exact: true }).click(); await p.waitForFunction(() => { const i = document.querySelector('.evidence-image-wrap img'); return i && i.complete && i.naturalWidth > 0; }, undefined, { timeout: 5000 }).catch(() => { }); const sameUrl = { retryMechanism, failedRequests, server: external, failedHeading: await p.getByRole('heading', { name: 'Кадр не загрузился', exact: true }).isVisible(), images: await p.locator('.evidence-image-wrap img').evaluateAll(es => es.map(i => ({ src: i.src, complete: i.complete, naturalWidth: i.naturalWidth }))), newEvidenceRequests: raw.network.filter(n => n.scenario === x.scenario && n.at > offAt && new URL(n.url).pathname.startsWith('/api/evidence/')) }; note('evidence_same_url_recovery', sameUrl); await capture(p, '18-evidence-off-refresh'); const recovered = sameUrl.images.some(i => i.complete && i.naturalWidth > 0); if (!recovered) {
        await p.reload();
        await p.waitForFunction(() => { const i = document.querySelector('.evidence-image-wrap img'); return i && i.complete && i.naturalWidth > 0; });
        note('evidence_reload_workaround', { restored: await p.locator('.evidence-image-wrap img').evaluate(i => ({ src: i.src, naturalWidth: i.naturalWidth })) });
        await capture(p, '19-evidence-full-reload-restored');
    } requireThat(recovered, 'Same-URL evidence stays failed after server recovery and card refresh', sameUrl); await x.context.close(); });
    await runCase('external fault500 error message and visible retry recovery', async () => { await control('reset'); const x = await newPage(browser, 'fault500'); const p = x.page; await p.goto(base + '/operator?review=real'); await p.getByTestId('operator-view').waitFor(); await control('fault/500'); await p.getByRole('button', { name: 'Обновить', exact: true }).click(); await p.getByRole('alert').waitFor(); const actual = await readApi('/api/operator/dashboard'); const alert = await p.getByRole('alert').innerText(); requireThat(actual.status === 500 && alert.includes(actual.body.message), 'External ApiError message not visible', { actual, alert }); await capture(p, '20-external500'); await control('fault/off'); await p.getByRole('button', { name: 'Повторить', exact: true }).click(); await p.getByRole('alert').waitFor({ state: 'hidden' }); await p.locator('a[href^="/operator/sectors/"]').first().waitFor({ state: 'visible' }); note('fault500_retry', { server: await readApi('/api/operator/dashboard'), alert_count: await p.getByRole('alert').count() }); await capture(p, '21-external500-recovered'); await x.context.close(); });
    await runCase('actual role/actor request headers', async () => { const requests = raw.network.filter(r => ['core', 'core-master'].includes(r.scenario) && r.method === 'POST' && /\/api\/events\/\d+\/actions$/.test(new URL(r.url).pathname)); const observed = requests.map(r => ({ url: r.url, role: r.headers['x-role'], actor: r.headers['x-actor'], body: JSON.parse(r.body), status: r.status })); note('core_action_request_headers', observed); requireThat(observed.some(r => r.body.action === 'resolve') && observed.every(r => r.status === 200 && r.actor === encodeURIComponent(actor) && r.role === (['accept', 'resolve'].includes(r.body.action) ? 'master' : 'operator')), 'Role/actor request headers mismatch', observed); });
    await control('fault/off');
    raw.final_director_state = await control('status');
    await browser.close();
    browser = null;
    await Promise.allSettled([...pending]);
    raw.source_after = sourceIdentity();
    raw.source_unchanged = raw.source_before.sha256 === raw.source_after.sha256;
    if (!raw.source_unchanged)
        finding('CONCURRENT_SOURCE_CHANGE', 'Frontend source changed during external proof', { before: raw.source_before.sha256, after: raw.source_after.sha256 });
    const actionRequests = raw.network.filter(r => r.method === 'POST' && /\/api\/events\/\d+\/actions$/.test(new URL(r.url).pathname));
    raw.role_actor_requests = actionRequests.map(r => ({ url: r.url, role: r.headers['x-role'], actor: r.headers['x-actor'], body: r.body, status: r.status }));
    raw.result = raw.cases.every(c => c.result === 'PASS') && raw.page_errors.length === 0 && raw.source_unchanged ? 'PASS' : 'FAIL';
    raw.completed_at = now();
    save();
    fs.writeFileSync(path.join(out, 'network.json'), JSON.stringify(raw.network, null, 2) + '\n');
    fs.writeFileSync(path.join(out, 'ws.json'), JSON.stringify(raw.websockets, null, 2) + '\n');
    console.log('FINAL', raw.result, JSON.stringify(raw.cases.map(c => ({ name: c.name, result: c.result, error: c.error }))));
    if (raw.result !== 'PASS')
        process.exitCode = 1;
})().catch(async (e) => { raw.result = 'HARNESS_ERROR'; raw.harness_error = { message: e.message, stack: e.stack }; raw.completed_at = now(); save(); console.error(e); if (browser)
    await browser.close(); process.exitCode = 2; });
