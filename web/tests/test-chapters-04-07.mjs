// Regression coverage for the Chapters 4-7 rollout: representative
// browser-pyodide lessons (Ch4/Ch5, positive + negative grading, including
// a property-based check on a random-number lesson and an
// error-is-expected lesson), and the Ch6/Ch7 local-required flow (no
// Pyodide worker, notebook download, local-instructions present, the
// learner-declared "completed locally" flow storing verified:false and
// score:null — never a fabricated PASS).
//
// Runs against a local static build (dist/). Requires the Playwright
// Chromium browser: `npx playwright install chromium` (run once).
//
// Usage: node web/tests/test-chapters-04-07.mjs (or `npm run test:ch4-7` from web/)

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
function log(...args) { console.log('[ch4-7]', ...args); }

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

(async () => {
  log('Building dist/...');
  execSync('bash scripts/build_vercel.sh', { cwd: ROOT, stdio: 'inherit' });

  const port = await getFreePort();
  const distDir = path.join(ROOT, 'dist');
  const server = spawn('python3', [path.join(ROOT, 'scripts', 'dev_server.py'), String(port), distDir], { stdio: 'ignore' });
  const base = `http://localhost:${port}`;

  try {
    await waitForServer(`${base}/practice/04-01/index.html`);
    const browser = await chromium.launch();

    // --- 04-01: positive grading (personalized data + namespace-checked relationship) ---
    log('04-01: positive grading');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/04-01/index.html`, { waitUntil: 'networkidle' });
      await page.evaluate(() => localStorage.removeItem('cartesian.python.progress.v1'));
      await page.waitForSelector('#status.practice-status-ready', { timeout: 30000 });
      await page.click('#run-all-btn');
      await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 60000 });
      await page.click('#check-btn');
      await page.waitForSelector('.practice-result', { timeout: 30000 });
      const resultText = await page.locator('.practice-result').textContent();
      ok('04-01 default answer PASSes', resultText.includes('PASS'));
      await page.close();
    }

    // --- 04-05: error-is-expected lesson (broken cell must show ok:false and still grade as PASS) ---
    log('04-05: error-is-expected grading');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/04-05/index.html`, { waitUntil: 'networkidle' });
      await page.evaluate(() => localStorage.removeItem('cartesian.python.progress.v1'));
      await page.waitForSelector('#status.practice-status-ready', { timeout: 30000 });
      await page.click('#run-all-btn');
      await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 60000 });
      const brokenCellOk = await page.evaluate(() => {
        const cell = document.querySelector('.nb-cell-code[data-cell-id="a8533ee4"]');
        return cell ? cell.classList.contains('nb-cell-error') : null;
      });
      ok('04-05: the intentionally-broken cell shows as errored (expected)', brokenCellOk === true);
      await page.click('#check-btn');
      await page.waitForSelector('.practice-result', { timeout: 30000 });
      const resultText = await page.locator('.practice-result').textContent();
      ok('04-05 default (broken+fixed both present) PASSes overall', resultText.includes('PASS'));
      await page.close();
    }

    // --- 05-05: random-number lesson, property-based automatic grading ---
    log('05-05: property-based grading on non-deterministic output');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/05-05/index.html`, { waitUntil: 'networkidle' });
      await page.evaluate(() => localStorage.removeItem('cartesian.python.progress.v1'));
      await page.waitForSelector('#status.practice-status-ready', { timeout: 30000 });
      await page.click('#run-all-btn');
      await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 60000 });
      await page.click('#check-btn');
      await page.waitForSelector('.practice-result', { timeout: 30000 });
      const resultText = await page.locator('.practice-result').textContent();
      ok('05-05 random-number lesson PASSes via property checks (not exact-value)', resultText.includes('PASS'));
      await page.close();
    }

    // --- negative grading: break 05-01's deterministic answer ---
    log('05-01: negative grading');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/05-01/index.html`, { waitUntil: 'networkidle' });
      await page.waitForSelector('#status.practice-status-ready', { timeout: 30000 });
      const cell = page.locator('.nb-cell-code[data-cell-id="d15260d5"] .cm-content');
      await cell.click();
      await page.keyboard.press('Control+A');
      await page.keyboard.type('print(999)'); // wrong answer, was change = paid - price = 150
      await page.click('#run-all-btn');
      await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 60000 });
      await page.click('#check-btn');
      await page.waitForSelector('.practice-result', { timeout: 30000 });
      const resultText = await page.locator('.practice-result').textContent();
      ok('05-01 wrong answer correctly FAILs', resultText.includes('FAIL'));
      await page.close();
    }

    // --- Ch6/Ch7 local-required pages ---
    for (const lessonId of ['06-02', '07-01']) {
      log(`${lessonId}: local-required page`);
      const page = await browser.newPage();
      const requests = [];
      page.on('request', (r) => requests.push(r.url()));
      await page.goto(`${base}/practice/${lessonId}/index.html`, { waitUntil: 'networkidle' });
      await page.evaluate(() => localStorage.removeItem('cartesian.python.progress.v1'));

      ok(`${lessonId}: badge shows "Требуется локальный Python"`, await page.locator('.local-required-badge').isVisible());
      ok(`${lessonId}: no Pyodide worker/wasm requested`, !requests.some((u) => /pyodide|python-worker/i.test(u)));
      ok(`${lessonId}: no #run-all-btn (no live runner) present`, (await page.locator('#run-all-btn').count()) === 0);

      const downloadHref = await page.locator('.actions a.btn-primary').getAttribute('href');
      const dres = await page.request.get(base + downloadHref);
      ok(`${lessonId}: .ipynb download link works (${downloadHref})`, dres.status() === 200);

      const instructionTitles = await page.locator('.instruction-card h3').allTextContents();
      ok(`${lessonId}: VS Code / PyCharm / Jupyter instructions all present`,
        instructionTitles.includes('VS Code') && instructionTitles.includes('PyCharm') && instructionTitles.includes('Jupyter'));

      // learner-declared local completion
      page.once('dialog', (d) => d.accept());
      await page.click('#mark-local-complete-btn');
      await page.waitForTimeout(200);
      const progress = await page.evaluate((id) => JSON.parse(localStorage.getItem('cartesian.python.progress.v1') || '{}')[id], lessonId);
      ok(`${lessonId}: manual completion stores status=completed-local`, progress?.status === 'completed-local');
      ok(`${lessonId}: verified=false (not auto-verified)`, progress?.verified === false);
      ok(`${lessonId}: score=null (no fake score)`, progress?.score === null);

      const statusText = await page.locator('#local-complete-status').textContent();
      ok(`${lessonId}: UI shows "Выполнено локально" after confirming`, statusText.includes('Выполнено локально'));

      // return link works
      const returnHref = await page.locator('.practice-return').getAttribute('href');
      await page.goto(new URL(returnHref, `${base}/practice/${lessonId}/index.html`).toString(), { waitUntil: 'networkidle' });
      ok(`${lessonId}: return link lands on a real page`, page.url().includes('.html'));

      await page.close();
    }

    // --- responsive check on one local-required page ---
    log('06-02: responsive (390x844, 768x1024, 1440x900)');
    for (const vp of [{ w: 390, h: 844 }, { w: 768, h: 1024 }, { w: 1440, h: 900 }]) {
      const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h } });
      const page = await ctx.newPage();
      await page.goto(`${base}/practice/06-02/index.html`, { waitUntil: 'networkidle' });
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
      ok(`06-02 no horizontal overflow at ${vp.w}x${vp.h}`, !overflow);
      await ctx.close();
    }

    await browser.close();
  } finally {
    server.kill();
  }

  if (failures > 0) {
    console.error(`\n[ch4-7] RESULT: FAIL (${failures} check(s) failed)`);
    process.exitCode = 1;
  } else {
    console.log('\n[ch4-7] RESULT: PASS');
  }
})().catch((err) => {
  console.error('[ch4-7] FATAL:', err);
  process.exit(1);
});
