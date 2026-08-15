// Regression coverage for the Chapters 13-17 rollout: representative
// browser-pyodide lessons (functions/lambda, OOP), the new golden file-I/O
// lesson (Pyodide virtual filesystem — write/read/append/pathlib, the
// honest "files live in this browser tab" notice, and Reset genuinely
// wiping file state between attempts), local-required Tkinter lessons
// (confirmed unavailable in Pyodide the same way turtle is), and the one
// deliberate non-tkinter exception in the tic-tac-toe chapter (17-05: pure
// win-checking logic, classified by actual code, not chapter theme).
//
// Runs against a local static build (dist/) served with cross-origin
// isolation headers (scripts/dev_server.py). Requires the Playwright
// Chromium browser: `npx playwright install chromium`.
//
// Usage: node web/tests/test-chapters-13-17.mjs (or `npm run test:ch13-17` from web/)

import { chromium } from 'playwright';
import { execSync, spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import net from 'node:net';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');

let failures = 0;
function ok(label, cond) {
  if (cond) console.log(`  [ok] ${label}`);
  else { console.error(`  [FAIL] ${label}`); failures += 1; }
}
function log(...args) { console.log('[ch13-17]', ...args); }

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

async function checkLocalRequired(browser, base, id) {
  const page = await browser.newPage();
  const requests = [];
  page.on('request', (r) => requests.push(r.url()));
  await page.goto(`${base}/practice/${id}/index.html`, { waitUntil: 'networkidle' });
  ok(`${id}: local-required badge visible`, await page.locator('.local-required-badge').isVisible());
  ok(`${id}: zero Pyodide worker starts (tkinter genuinely absent, not faked)`, !requests.some((u) => /pyodide|python-worker/i.test(u)));
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
    await waitForServer(`${base}/practice/13-01/index.html`);
    const browser = await chromium.launch();

    // --- Chapter 13: functions/lambda ---
    log('13-03: return-based grading on fresh function calls');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/13-03/index.html`, { waitUntil: 'networkidle' });
      const result = await runAllAndCheck(page);
      ok('13-03 default run PASSes', result.includes('PASS'));
      await page.close();
    }
    await checkLocalRequired(browser, base, '13-08');

    // --- Chapter 14: OOP ---
    log('14-03: real object/method behavior grading');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/14-03/index.html`, { waitUntil: 'networkidle' });
      const result = await runAllAndCheck(page);
      ok('14-03 default run PASSes', result.includes('PASS'));
      await page.close();
    }
    await checkLocalRequired(browser, base, '14-04');

    // --- Chapter 15: GOLDEN FILE LESSON (new regression-matrix entry) ---
    log('15-01: Pyodide virtual filesystem — write/read, honest notice, Reset wipes state');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/15-01/index.html`, { waitUntil: 'networkidle' });
      ok('15-01: virtual-filesystem notice visible (files live in the browser tab, not on disk)',
        await page.locator('.practice-fs-notice').isVisible());
      const result = await runAllAndCheck(page);
      ok('15-01: default run PASSes (real write-then-read against the VFS)', result.includes('PASS'));
      // Reset must wipe file state, not just Python variables
      await page.click('#reset-btn');
      await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 30000 });
      const result2 = await runAllAndCheck(page);
      ok('15-01: re-run after Reset still PASSes (fresh VFS, no stale file from the prior run)', result2.includes('PASS'));
      await page.close();
    }
    log('15-04: input()-driven file writes, notebook\'s own assert-based self-check');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/15-04/index.html`, { waitUntil: 'networkidle' });
      await page.waitForSelector('#status.practice-status-ready', { timeout: 30000 });
      await page.click('#run-all-btn');
      for (const ans of ['Первая заметка', 'Вторая заметка']) {
        await page.waitForSelector('.nb-input-prompt', { timeout: 15000 });
        await page.fill('.nb-input-field', ans);
        await page.click('.nb-input-submit');
      }
      await page.waitForFunction(() => ['Готово', 'Остановлено на ошибке'].includes(document.getElementById('status').textContent), { timeout: 30000 });
      await page.click('#check-btn');
      await page.waitForSelector('.practice-result', { timeout: 15000 });
      const result = await page.locator('.practice-result').textContent();
      ok('15-04: real input()-driven note-taking to a file PASSes with the canonical notes', result.includes('PASS'));
      await page.close();
    }

    // --- Chapter 16: Tkinter, fully local-required ---
    await checkLocalRequired(browser, base, '16-01');
    await checkLocalRequired(browser, base, '16-08');

    // --- Chapter 17: tic-tac-toe project ---
    await checkLocalRequired(browser, base, '17-01');
    await checkLocalRequired(browser, base, '17-06');
    log('17-05: pure logic living in a Tkinter chapter — correctly browser-pyodide, not local-required');
    {
      const page = await browser.newPage();
      const requests = [];
      page.on('request', (r) => requests.push(r.url()));
      await page.goto(`${base}/practice/17-05/index.html`, { waitUntil: 'networkidle' });
      await page.waitForSelector('#status.practice-status-ready', { timeout: 30000 });
      const versionText = await page.locator('#version-label').textContent();
      ok('17-05: Python 3.14.2 via Pyodide (not local-required, despite the chapter theme)', versionText.includes('3.14.2'));
      const result = await runAllAndCheck(page);
      ok('17-05: win-checking logic PASSes (zero tkinter code in this notebook)', result.includes('PASS'));
      ok('17-05: zero Pyodide worker was NOT required to skip this lesson', requests.some((u) => /pyodide/i.test(u)));
      await page.close();
    }

    await browser.close();
  } finally {
    server.kill();
  }

  if (failures > 0) {
    console.error(`\n[ch13-17] RESULT: FAIL (${failures} check(s) failed)`);
    process.exitCode = 1;
  } else {
    console.log('\n[ch13-17] RESULT: PASS');
  }
})().catch((err) => {
  console.error('[ch13-17] FATAL:', err);
  process.exit(1);
});
