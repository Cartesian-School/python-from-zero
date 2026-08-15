// Regression coverage for the Chapters 8-12 rollout: representative
// browser-pyodide lessons from each chapter (including exact/property/
// relationship-invariant grading), the shared input() bridge (both a
// single-shot prompt and a while-loop with live stdout feedback between
// prompts), and the local-required Turtle lessons.
//
// Runs against a local static build (dist/) served with cross-origin
// isolation headers (scripts/dev_server.py) — SharedArrayBuffer, and
// therefore input(), is unavailable without them. Requires the
// Playwright Chromium browser: `npx playwright install chromium`.
//
// Usage: node web/tests/test-chapters-08-12.mjs (or `npm run test:ch8-12` from web/)

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
function log(...args) { console.log('[ch8-12]', ...args); }

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
  await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 60000 });
  await page.click('#check-btn');
  await page.waitForSelector('.practice-result', { timeout: 15000 });
  return (await page.locator('.practice-result').textContent()).trim();
}

async function answerPrompts(page, answers) {
  for (const ans of answers) {
    await page.waitForSelector('.nb-input-prompt', { timeout: 15000 });
    await page.fill('.nb-input-field', ans);
    await page.click('.nb-input-submit');
  }
}

async function checkLocalRequired(browser, base, id) {
  const page = await browser.newPage();
  const requests = [];
  page.on('request', (r) => requests.push(r.url()));
  await page.goto(`${base}/practice/${id}/index.html`, { waitUntil: 'networkidle' });
  ok(`${id}: local-required badge visible`, await page.locator('.local-required-badge').isVisible());
  ok(`${id}: no Pyodide worker/wasm requested`, !requests.some((u) => /pyodide|python-worker/i.test(u)));
  ok(`${id}: no #run-all-btn (no live runner) present`, (await page.locator('#run-all-btn').count()) === 0);
  const downloadHref = await page.locator('.actions a.btn-primary').getAttribute('href');
  const dres = await page.request.get(base + downloadHref);
  ok(`${id}: .ipynb download link works (${downloadHref})`, dres.status() === 200);
  page.once('dialog', (d) => d.accept());
  await page.click('#mark-local-complete-btn');
  await page.waitForTimeout(200);
  const progress = await page.evaluate((lid) => JSON.parse(localStorage.getItem('cartesian.python.progress.v1') || '{}')[lid], id);
  ok(`${id}: manual completion verified=false, score=null`, progress?.verified === false && progress?.score === null);
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
    await waitForServer(`${base}/practice/08-01/index.html`);
    const browser = await chromium.launch();

    // --- Chapter 8: exact/relationship grading + real input() ---
    log('08-01: exact-invariant grading (two quoting techniques)');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/08-01/index.html`, { waitUntil: 'networkidle' });
      const result = await runAllAndCheck(page);
      ok('08-01 default run PASSes', result.includes('PASS'));
      await page.close();
    }
    log('08-07: real input() bridge, 4 sequential prompts across cells');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/08-07/index.html`, { waitUntil: 'networkidle' });
      await page.waitForSelector('#status.practice-status-ready', { timeout: 30000 });
      await page.click('#run-all-btn');
      await answerPrompts(page, ['Ада', '30', '30', 'Ада']);
      await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 30000 });
      await page.click('#check-btn');
      await page.waitForSelector('.practice-result', { timeout: 15000 });
      const result = await page.locator('.practice-result').textContent();
      ok('08-07 grading PASSes with real typed input (not a canned answer)', result.includes('PASS'));
      await page.close();
    }

    // --- Chapter 9: bool/comparison grading + seeded-random input() ---
    log('09-06: elif ladder + nested conditions, deterministic invariant grading');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/09-06/index.html`, { waitUntil: 'networkidle' });
      const result = await runAllAndCheck(page);
      ok('09-06 default run PASSes', result.includes('PASS'));
      await page.close();
    }

    // --- Chapter 10: live stdout streaming during a real while-loop input() game ---
    log('10-05: input() inside a while loop — live "higher/lower" feedback between guesses');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/10-05/index.html`, { waitUntil: 'networkidle' });
      await page.waitForSelector('#status.practice-status-ready', { timeout: 30000 });
      await page.click('#run-all-btn');
      await page.waitForSelector('.nb-input-prompt', { timeout: 15000 });
      await page.fill('.nb-input-field', '10');
      await page.click('.nb-input-submit');
      await page.waitForTimeout(600);
      const feedback = await page.locator('.nb-output-stdout:not(.nb-input-echo)').last().textContent();
      ok('10-05: feedback text ("больше"/"меньше") renders BEFORE the cell finishes, not just at the end',
        feedback.includes('больше') || feedback.includes('меньше'));
      // finish the game via binary search so Check has a valid namespace to grade
      let lo = 1, hi = 20, rounds = 0;
      while (rounds++ < 10) {
        const status = await page.locator('#status').textContent();
        if (status === 'Готово') break;
        await page.waitForSelector('.nb-input-prompt', { timeout: 15000 });
        const guess = Math.floor((lo + hi) / 2);
        await page.fill('.nb-input-field', String(guess));
        await page.click('.nb-input-submit');
        await page.waitForTimeout(300);
        const fb = await page.locator('.nb-output-stdout:not(.nb-input-echo)').last().textContent().catch(() => '');
        if (fb.includes('больше')) lo = guess + 1; else if (fb.includes('меньше')) hi = guess - 1;
      }
      await page.click('#check-btn');
      await page.waitForSelector('.practice-result', { timeout: 15000 });
      const result = await page.locator('.practice-result').textContent();
      ok('10-05: grading PASSes once the real (live-guided) guess converges', result.includes('PASS'));
      await page.close();
    }
    for (const id of ['10-06', '10-08']) {
      await checkLocalRequired(browser, base, id);
    }

    // --- Chapter 11: collection graders + local-required Turtle+data lessons ---
    log('11-04: list comprehension vs. loop-built list equivalence');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/11-04/index.html`, { waitUntil: 'networkidle' });
      const result = await runAllAndCheck(page);
      ok('11-04 default run PASSes', result.includes('PASS'));
      await page.close();
    }
    await checkLocalRequired(browser, base, '11-05');

    // --- Chapter 12: input() mini-projects + local-required Turtle mini-projects ---
    log('12-02: real input() tip calculator, property-based percentage check');
    {
      const page = await browser.newPage();
      await page.goto(`${base}/practice/12-02/index.html`, { waitUntil: 'networkidle' });
      await page.waitForSelector('#status.practice-status-ready', { timeout: 30000 });
      await page.click('#run-all-btn');
      await answerPrompts(page, ['1000', '150', '1000', '350']);
      await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 30000 });
      await page.click('#check-btn');
      await page.waitForSelector('.practice-result', { timeout: 15000 });
      const result = await page.locator('.practice-result').textContent();
      ok('12-02 grading PASSes with real typed bill/tip amounts', result.includes('PASS'));
      await page.close();
    }
    await checkLocalRequired(browser, base, '12-06');

    await browser.close();
  } finally {
    server.kill();
  }

  if (failures > 0) {
    console.error(`\n[ch8-12] RESULT: FAIL (${failures} check(s) failed)`);
    process.exitCode = 1;
  } else {
    console.log('\n[ch8-12] RESULT: PASS');
  }
})().catch((err) => {
  console.error('[ch8-12] FATAL:', err);
  process.exit(1);
});
