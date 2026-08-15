// Regression test for the Pyodide bridge session contract (site/assets/js/
// practice-app.js + python-worker.mjs). Exists specifically to catch the
// stale-bridge-after-reset bug found during preview validation: cells used
// to close over the PyodideBridge instance at render time, so after Reset
// created a new bridge, every cell kept calling the terminated one
// (worker: null) and crashed. Fixed by routing all execution through
// state.bridge, a single mutable reference. This test exercises exactly the
// sequence that exposed the bug, plus the busy-guard added alongside it.
//
// Runs against a local static build (dist/), not the live Vercel preview,
// so it works offline / in CI without Vercel auth. Requires the Playwright
// Chromium browser: `npx playwright install chromium` (run once).
//
// Usage: node web/tests/test-bridge-contract.mjs   (or `npm test` from web/)

import { chromium } from 'playwright';
import { execSync, spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import net from 'node:net';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');

function log(...args) {
  console.log('[bridge-contract]', ...args);
}

function fail(msg) {
  console.error('[bridge-contract] FAIL:', msg);
  process.exitCode = 1;
}

async function getFreePort() {
  return new Promise((resolve, reject) => {
    const srv = net.createServer();
    srv.listen(0, () => {
      const { port } = srv.address();
      srv.close(() => resolve(port));
    });
    srv.on('error', reject);
  });
}

async function waitForServer(url, timeoutMs = 15000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const res = await fetch(url);
      if (res.ok) return;
    } catch (e) {
      // not up yet
    }
    await new Promise((r) => setTimeout(r, 200));
  }
  throw new Error(`Server at ${url} did not become ready in time`);
}

(async () => {
  log('Building dist/ (bash scripts/build_vercel.sh)...');
  execSync('bash scripts/build_vercel.sh', { cwd: ROOT, stdio: 'inherit' });

  const port = await getFreePort();
  const distDir = path.join(ROOT, 'dist');
  log(`Starting static server on :${port} for ${distDir}`);
  const server = spawn('python3', [path.join(ROOT, 'scripts', 'dev_server.py'), String(port), distDir], { stdio: 'ignore' });

  const base = `http://localhost:${port}`;
  try {
    await waitForServer(`${base}/practice/03-01/index.html`);

    const browser = await chromium.launch();
    const page = await browser.newPage();

    const consoleErrors = [];
    const pageErrors = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });
    page.on('pageerror', (err) => pageErrors.push(err.message));

    log('1. Navigate + wait for Pyodide ready...');
    await page.goto(`${base}/practice/03-01/index.html`, { waitUntil: 'networkidle' });
    await page.waitForSelector('#status.practice-status-ready', { timeout: 30000 });

    const firstCellRun = page.locator('.nb-run-cell').first();
    const firstCell = page.locator('.nb-cell-code').first();

    log('2. Execute cell...');
    await firstCellRun.click();
    await page.waitForFunction(
      (el) => el.classList.contains('nb-cell-ok') || el.classList.contains('nb-cell-error'),
      await firstCell.elementHandle(),
      { timeout: 15000 }
    );
    if (!(await firstCell.evaluate((el) => el.classList.contains('nb-cell-ok')))) {
      fail('step 2: first cell did not execute successfully');
    }

    log('3. Reset...');
    await page.click('#reset-btn');
    await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 30000 });

    log('4. Execute same cell again (the exact scenario that used to crash)...');
    await firstCellRun.click();
    await page.waitForFunction(
      (el) => el.classList.contains('nb-cell-ok') || el.classList.contains('nb-cell-error'),
      await firstCell.elementHandle(),
      { timeout: 15000 }
    );
    if (!(await firstCell.evaluate((el) => el.classList.contains('nb-cell-ok')))) {
      fail('step 4: cell re-run after reset did not execute successfully (stale bridge?)');
    }

    log('5. Run All...');
    await page.click('#run-all-btn');
    await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 60000 });

    log('6. Reset...');
    await page.click('#reset-btn');
    await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 30000 });

    log('7. Check Result (with no cells run since reset — must not crash)...');
    await page.click('#check-btn');
    await page.waitForFunction(() => !document.getElementById('check-btn').disabled, { timeout: 30000 });

    log('8. Check Result while Run All is busy...');
    await page.click('#run-all-btn');
    await page.click('#check-btn'); // fired immediately after, while Run All is mid-flight
    await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 60000 });
    await page.waitForFunction(
      () => !document.getElementById('run-all-btn').disabled && !document.getElementById('check-btn').disabled && !document.getElementById('reset-btn').disabled,
      { timeout: 10000 }
    );

    log('9. Run All while Check Result is busy...');
    await page.click('#check-btn');
    await page.click('#run-all-btn'); // fired immediately after, while Check Result is mid-flight
    await page.waitForFunction(() => document.getElementById('status').textContent === 'Готово', { timeout: 60000 });
    await page.waitForFunction(
      () => !document.getElementById('run-all-btn').disabled && !document.getElementById('check-btn').disabled && !document.getElementById('reset-btn').disabled,
      { timeout: 10000 }
    );

    const finalState = await page.evaluate(() => ({
      status: document.getElementById('status').textContent,
      runAllDisabled: document.getElementById('run-all-btn').disabled,
      checkDisabled: document.getElementById('check-btn').disabled,
      resetDisabled: document.getElementById('reset-btn').disabled,
    }));
    log('Final state:', JSON.stringify(finalState));

    if (finalState.status !== 'Готово') fail(`final status is "${finalState.status}", expected "Готово"`);
    if (finalState.runAllDisabled || finalState.checkDisabled || finalState.resetDisabled) {
      fail('a control is permanently disabled after the sequence: ' + JSON.stringify(finalState));
    }
    if (pageErrors.length > 0) {
      fail('uncaught page errors during the sequence:\n  ' + pageErrors.join('\n  '));
    }
    if (consoleErrors.length > 0) {
      fail('console errors during the sequence:\n  ' + consoleErrors.join('\n  '));
    }

    await browser.close();
  } finally {
    server.kill();
  }

  if (process.exitCode === 1) {
    console.error('[bridge-contract] RESULT: FAIL');
  } else {
    console.log('[bridge-contract] RESULT: PASS — no null worker, no stale bridge, no permanently disabled controls, no concurrent execution corruption.');
  }
})().catch((err) => {
  console.error('[bridge-contract] FATAL:', err);
  process.exit(1);
});
