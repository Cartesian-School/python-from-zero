// Regression coverage for the Chapters 18-24 rollout: the final curriculum
// batch. Chapters 18 (Tkinter paint app), 19 (Turtle Snake), 20 and 21
// (Pygame — confirmed via direct testing to trigger a fatal Pyodide Worker
// crash on pygame.display.set_mode(), not just an unavailable import) are
// entirely local-required. Chapter 22 is mixed: 22-02 exercises the shared
// IPython.display.HTML bridge (genuinely renders HTML in-browser, not a
// repr() fallback), 22-05 is local-required (flask confirmed unavailable).
// Chapter 23 is mixed: 23-02/23-03 exercise the shared companion-file
// loader (real local project modules mirrored into the Pyodide VFS so
// their own unmodified sys.path.insert() imports resolve), the rest are
// local-required (their referenced project modules call tk.Tk() or
// pygame.display.set_mode() at import time). Chapter 24 has zero notebooks
// by design (a wrap-up chapter with no code exercises) — verified here by
// asserting no phantom /practice/24-* routes exist.
//
// Runs against a local static build (dist/) served with cross-origin
// isolation headers (scripts/dev_server.py). Requires the Playwright
// Chromium browser: `npx playwright install chromium`.
//
// Usage: node web/tests/test-chapters-18-24.mjs (or `npm run test:ch18-24` from web/)

import { chromium } from 'playwright';
import { execSync, spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';
import net from 'node:net';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');

let failures = 0;
function ok(label, cond) {
  if (cond) console.log(`  [ok] ${label}`);
  else { console.error(`  [FAIL] ${label}`); failures += 1; }
}
function log(...args) { console.log('[ch18-24]', ...args); }

async function getFreePort() {
  return new Promise((resolve, reject) => {
    const srv = net.createServer();
    srv.listen(0, () => { const { port } = srv.address(); srv.close(() => resolve(port)); });
    srv.on('error', reject);
  });
}
async function waitForServer(url, timeoutMs = 15000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try { const r = await fetch(url); if (r.ok) return; } catch (e) {}
    await new Promise((r) => setTimeout(r, 200));
  }
  throw new Error(`Server at ${url} did not become ready`);
}

async function runAllAndCheck(page) {
  await page.waitForSelector('#status.practice-status-ready', { timeout: 30000 });
  await page.click('#run-all-btn');
  await page.waitForFunction(() => ['Готово', 'Остановлено на ошибке'].includes(document.getElementById('status').textContent), { timeout: 60000 });
  await page.click('#check-btn');
  await page.waitForSelector('.practice-result', { timeout: 15000 });
  return (await page.locator('.practice-result').textContent()).trim();
}

async function checkLocalRequired(browser, base, id, { reason } = {}) {
  const page = await browser.newPage();
  const requests = [];
  page.on('request', (r) => requests.push(r.url()));
  await page.goto(`${base}/practice/${id}/index.html`, { waitUntil: 'networkidle' });
  ok(`${id}: local-required badge visible`, await page.locator('.local-required-badge').isVisible());
  ok(`${id}: zero Pyodide worker starts${reason ? ` (${reason})` : ''}`, !requests.some((u) => /pyodide|python-worker/i.test(u)));
  const downloadHref = await page.locator('.actions a.btn-primary').getAttribute('href');
  const dres = await page.request.get(base + downloadHref);
  ok(`${id}: .ipynb download works`, dres.status() === 200);
  await page.close();
}

(async () => {
  log('Building dist/...');
  execSync('bash scripts/build_vercel.sh', { cwd: ROOT, stdio: 'inherit' });

  const port = await getFreePort();
  const distDir = path.join(ROOT, 'dist');
  const server = spawn('python3', [path.join(ROOT, 'scripts', 'dev_server.py'), String(port), distDir], { stdio: 'ignore' });
  const base = `http://localhost:${port}`;

  try {
    await waitForServer(`${base}/practice/18-02/index.html`);
    const browser = await chromium.launch();

    // --- Chapter 18: Tkinter paint app, fully local-required ---
    await checkLocalRequired(browser, base, '18-02', { reason: 'tkinter confirmed unavailable in Pyodide' });
    await checkLocalRequired(browser, base, '18-07');

    // --- Chapter 19: Turtle Snake, fully local-required ---
    await checkLocalRequired(browser, base, '19-02', { reason: 'turtle confirmed unavailable in Pyodide' });
    await checkLocalRequired(browser, base, '19-08');

    // --- Chapter 20: Pygame, fully local-required (fatal Worker crash, not just unavailable) ---
    await checkLocalRequired(browser, base, '20-02', { reason: 'pygame.display.set_mode() triggers a fatal Pyodide Worker crash' });
    await checkLocalRequired(browser, base, '20-05');

    // --- Chapter 21: Pygame Space Shooter, fully local-required ---
    await checkLocalRequired(browser, base, '21-01', { reason: 'pygame.display.set_mode() triggers a fatal Pyodide Worker crash' });
    await checkLocalRequired(browser, base, '21-08');

    // --- Chapter 22: mixed — display-html bridge + local-required flask ---
    log('22-02: shared IPython.display.HTML bridge renders real HTML, not repr()');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/22-02/index.html`, { waitUntil: 'networkidle' });
      const result = await runAllAndCheck(page);
      const displayBoxes = await page.locator('.nb-output-display-html').count();
      ok('22-02: display-html bridge rendered at least one box', displayBoxes >= 1);
      const displayHtml = await page.locator('.nb-output-display-html').first().innerHTML().catch(() => '');
      ok('22-02: rendered box contains real markup, not an object repr()', displayHtml.includes('<h1>') || displayHtml.toLowerCase().includes('привет'));
      ok('22-02: grading PASSes', result.includes('PASS'));
      await page.close();
    }
    await checkLocalRequired(browser, base, '22-05', { reason: 'flask confirmed unavailable in Pyodide' });

    // --- Chapter 23: mixed — companion-file loader + local-required project modules ---
    for (const id of ['23-02', '23-03']) {
      log(`${id}: shared companion-file loader mirrors a real project module into the Pyodide VFS`);
      const page = await browser.newPage();
      await page.goto(`${base}/practice/${id}/index.html`, { waitUntil: 'networkidle' });
      const result = await runAllAndCheck(page);
      ok(`${id}: companion-file import resolves and grading PASSes`, result.includes('PASS'));
      await page.close();
    }
    await checkLocalRequired(browser, base, '23-01', { reason: 'calculator.py calls tk.Tk() at import time' });
    await checkLocalRequired(browser, base, '23-06', { reason: 'notes_app.py calls tk.Tk() at import time' });

    // --- Chapter 24: zero notebooks by design (wrap-up chapter, no code exercises) ---
    log('24: confirming no phantom /practice/24-* routes exist');
    {
      const manifestPath = path.join(ROOT, 'manifest', 'practice_manifest.json');
      const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
      const ch24Keys = Object.keys(manifest).filter((k) => k.startsWith('24-'));
      ok('manifest: zero Chapter 24 entries (no notebooks exist for this chapter)', ch24Keys.length === 0);
      const practiceDir24 = path.join(ROOT, 'site', 'practice');
      const phantom24 = fs.existsSync(practiceDir24)
        ? fs.readdirSync(practiceDir24).filter((d) => d.startsWith('24-'))
        : [];
      ok('site/practice: zero Chapter 24 directories generated', phantom24.length === 0);
      const page = await browser.newPage();
      await page.goto(`${base}/chapters/glava-24/index.html`, { waitUntil: 'networkidle' });
      ok('glava-24/index.html loads (theory pages still present)', (await page.title()).length > 0);
      await page.close();
    }

    await browser.close();
  } finally {
    server.kill();
  }

  if (failures > 0) {
    console.error(`\n[ch18-24] RESULT: FAIL (${failures} check(s) failed)`);
    process.exitCode = 1;
  } else {
    console.log('\n[ch18-24] RESULT: PASS');
  }
})().catch((err) => {
  console.error('[ch18-24] FATAL:', err);
  process.exit(1);
});
