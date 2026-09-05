// Non-public bilingual fixture: shared desktop/mobile navigation and progress storage.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtemp, cp, readFile, rm } from 'node:fs/promises';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const dir = await mkdtemp(path.join(os.tmpdir(), 'cartesian-localization-'));
let browser;
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const file = path.resolve(dir, '.' + decodeURIComponent(url.pathname));
  if (!file.startsWith(dir + path.sep)) { res.writeHead(403).end(); return; }
  try {
    const bytes = await readFile(file);
    const type = {'.html':'text/html', '.css':'text/css', '.js':'text/javascript'}[path.extname(file)];
    res.writeHead(200, {'Content-Type': type || 'application/octet-stream'}).end(bytes);
  } catch { res.writeHead(404).end(); }
});
try {
  execFileSync(process.env.PYTHON_BIN || 'python3', ['scripts/build_localization_fixture.py', dir], {cwd:root});
  await cp(path.join(root, 'site/assets'), path.join(dir, 'assets'), {recursive:true});
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  browser = await chromium.launch({headless:true});
  for (const width of [1280, 390]) {
    const page = await browser.newPage({viewport:{width, height:900}});
    await page.goto(origin + '/practice/03-01/index.html');
    await page.evaluate(() => localStorage.setItem('cartesian.python.progress.v1', JSON.stringify({'03-01':{passed:true,score:100}})));
    const selector = width > 860 ? '.language-switcher-desktop' : '#mobile-nav-panel';
    if (width <= 860) {
      assert.equal(await page.locator('.language-switcher-desktop').isVisible(), false);
      await page.locator('.nav-toggle').click();
    }
    const link = page.locator(`${selector} .language-switcher a`);
    assert.equal(await link.isVisible(), true);
    assert.equal(await link.evaluate(el => getComputedStyle(el).color), 'rgb(255, 255, 255)');
    assert.equal(await page.locator(`${selector} .language-switcher [aria-current]`).evaluate(el => getComputedStyle(el).color), 'rgb(34, 211, 238)');
    assert.equal(await link.getAttribute('href'), '/pl/practice/03-01/index.html');
    await link.focus();
    await page.keyboard.press('Enter');
    await page.waitForURL(origin + '/pl/practice/03-01/index.html');
    assert.equal(await page.locator('html').getAttribute('lang'), 'pl');
    assert.equal(await page.evaluate(() => JSON.parse(localStorage.getItem('cartesian.python.progress.v1'))['03-01'].passed), true);
    if (width <= 860) await page.locator('.nav-toggle').click();
    const back = page.locator(`${selector} .language-switcher a`);
    assert.equal(await back.getAttribute('href'), '/practice/03-01/index.html');
    await back.click();
    await page.waitForURL(origin + '/practice/03-01/index.html');
    await page.close();
  }
  console.log('PASS: RU/PL exact-page keyboard switching, desktop/mobile, shared progress storage');
} finally {
  await browser?.close();
  await new Promise(resolve => server.close(resolve));
  await rm(dir, {recursive:true, force:true});
}
