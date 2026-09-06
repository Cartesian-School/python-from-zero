// Regression coverage for the Polish homepage (/pl/index.html) navigation.
//
// M02-I04 post-merge bug report: after the complete Polish translation
// shipped, /pl/index.html was reported to still behave like the earlier
// M02-I03 partial-translation shell -- chapter/project/reference cards
// blocked or showing "Tłumaczenie niedostępne" even though the
// corresponding PL pages already existed. scripts/validate_pl_complete.py's
// homepage_navigation_errors() now catches this at the HTML level; this
// suite proves it holds up in a real browser too: every chapter/project/
// reference card is a real, clickable link, and clicking through a
// representative sample actually lands on the correct Polish page.
//
// Usage: node web/tests/test-pl-homepage-navigation.mjs (or `npm run test:pl-home`)

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
function log(...args) { console.log('[pl-home]', ...args); }

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
    try { const r = await fetch(url); if (r.ok) return; } catch (e) { /* not up yet */ }
    await new Promise((r) => setTimeout(r, 200));
  }
  throw new Error(`Server at ${url} did not become ready`);
}

const ROUTES = JSON.parse(fs.readFileSync(path.join(ROOT, 'manifest', 'i18n', 'routes.json'), 'utf-8'));
const PAGES = ROUTES.pages;
const CHAPTER_OPENERS = Object.entries(PAGES).filter(([id]) => /^chapter-\d{2}$/.test(id));
const PROJECT_PAGES = Object.entries(PAGES).filter(([, p]) => p.project_id);

// The exact obsolete M02-I03 "partial shell" phrasing (manifest/i18n/content/
// pl/home.json, deleted alongside this test) -- must never be visible again.
const STALE_PATTERN = /Tłumaczenie niedostępne|nie została jeszcze przetłumaczona|kolejnych etapach tłumaczenia|są już ujęte w planie/;
const DISABLED_SELECTOR = '.jn-card[aria-disabled], .project-card[aria-disabled], '
  + '.practice-chapter-group[aria-disabled], #spravochnik .reference-card[aria-disabled]';

const VIEWPORTS = [[1920, 1080], [1440, 900], [1280, 800], [1024, 900], [768, 1024], [430, 932], [390, 844], [360, 800]];

(async () => {
  log('Building dist/...');
  execSync('bash scripts/build_vercel.sh', { cwd: ROOT, stdio: 'inherit' });

  const port = await getFreePort();
  const distDir = path.join(ROOT, 'dist');
  const server = spawn('python3', [path.join(ROOT, 'scripts', 'dev_server.py'), String(port), distDir], { stdio: 'ignore' });
  const base = `http://localhost:${port}`;

  try {
    await waitForServer(`${base}/pl/index.html`);
    const browser = await chromium.launch();

    log(`Structural + visual check across ${VIEWPORTS.length} viewports`);
    for (const [width, height] of VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      await page.goto(`${base}/pl/index.html`, { waitUntil: 'networkidle' });
      const viewport = `${width}x${height}`;
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
      ok(`${viewport}: no horizontal overflow`, !overflow);
      const bodyText = await page.evaluate(() => document.body.innerText);
      ok(`${viewport}: no stale partial-translation copy visible`, !STALE_PATTERN.test(bodyText));
      const disabledCount = await page.locator(DISABLED_SELECTOR).count();
      ok(`${viewport}: no disabled localization cards`, disabledCount === 0);
      if (width > 860) {
        const switcher = page.locator('.language-switcher-desktop .language-switcher a');
        ok(`${viewport}: RU|PL switcher present and points at RU homepage`, await switcher.getAttribute('href') === '/index.html');
      }
      await page.close();
    }

    log('Structural check: every chapter and project card links to its exact PL route');
    {
      const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
      await page.goto(`${base}/pl/index.html`, { waitUntil: 'networkidle' });

      const chapterHrefs = (await page.locator('a.jn-card').evaluateAll((els) => els.map((el) => el.getAttribute('href')))).sort();
      const expectedChapterHrefs = CHAPTER_OPENERS.map(([, p]) => p.variants.pl.path).sort();
      ok(`all ${expectedChapterHrefs.length} chapter cards match routes.json exactly`,
        JSON.stringify(chapterHrefs) === JSON.stringify(expectedChapterHrefs));

      const projectHrefs = (await page.locator('a.project-card').evaluateAll((els) => els.map((el) => el.getAttribute('href')))).sort();
      const expectedProjectHrefs = PROJECT_PAGES.map(([, p]) => p.variants.pl.path).sort();
      ok(`all ${expectedProjectHrefs.length} project cards match routes.json exactly`,
        JSON.stringify(projectHrefs) === JSON.stringify(expectedProjectHrefs));

      await page.close();
    }

    log('Click-through navigation for representative pages');
    {
      const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
      await page.goto(`${base}/pl/index.html`, { waitUntil: 'networkidle' });

      const clickAndVerify = async (label, locator, expectedPath) => {
        await locator.scrollIntoViewIfNeeded();
        await locator.click();
        await page.waitForURL(`${base}${expectedPath}`);
        ok(`${label}: navigates to ${expectedPath}`, page.url() === `${base}${expectedPath}`);
        ok(`${label}: rendered page declares lang="pl"`, await page.locator('html').getAttribute('lang') === 'pl');
        await page.goBack({ waitUntil: 'networkidle' });
      };

      await clickAndVerify('Chapter 1', page.locator(`a.jn-card[href="${PAGES['chapter-01'].variants.pl.path}"]`), PAGES['chapter-01'].variants.pl.path);
      await clickAndVerify('Chapter 12 (middle)', page.locator(`a.jn-card[href="${PAGES['chapter-12'].variants.pl.path}"]`), PAGES['chapter-12'].variants.pl.path);
      await clickAndVerify('Chapter 24', page.locator(`a.jn-card[href="${PAGES['chapter-24'].variants.pl.path}"]`), PAGES['chapter-24'].variants.pl.path);

      const firstProjectPath = PROJECT_PAGES[0][1].variants.pl.path;
      await clickAndVerify('First project', page.locator(`a.project-card[href="${firstProjectPath}"]`), firstProjectPath);

      const referenceTargets = [
        ['Indeks rzeczowy', PAGES['reference-index'].variants.pl.path],
        ['Wprowadzenie', PAGES['front-matter-introduction'].variants.pl.path],
        ['O autorze', PAGES['front-matter-author'].variants.pl.path],
        ['O recenzencie technicznym', PAGES['front-matter-technical-reviewer'].variants.pl.path],
        ['Licencja', PAGES['front-matter-license'].variants.pl.path],
      ];
      for (const [label, expectedPath] of referenceTargets) {
        await clickAndVerify(label, page.locator(`#spravochnik a.reference-card[href="${expectedPath}"]`), expectedPath);
      }

      // The CLI/runtime and official-Python-resources reference cards point
      // at specific lesson pages (not a dedicated front-matter route) --
      // verify a real, non-disabled PL page rather than hardcoding a
      // brittle lesson path that would break the moment content moves.
      const cliCard = page.locator('#spravochnik a.reference-card').filter({ hasText: 'Środowisko wykonawcze' });
      const cliHref = await cliCard.getAttribute('href');
      ok('CLI/runtime reference card has a real PL href',
        typeof cliHref === 'string' && cliHref.startsWith('/pl/') && fs.existsSync(path.join(distDir, cliHref.slice(1))));

      await page.close();
    }

    log('Practice: expand a chapter group and open a real lesson');
    {
      const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
      await page.goto(`${base}/pl/index.html#praktika`, { waitUntil: 'networkidle' });
      const group = page.locator('.practice-chapter-group[data-chapter="1"]');
      await group.locator('summary').click();
      const lessonLink = group.locator('.practice-lesson-row[href]').first();
      const expectedHref = await lessonLink.getAttribute('href');
      ok('practice lesson row for Chapter 1 has a real href', typeof expectedHref === 'string' && expectedHref.startsWith('/pl/practice/'));
      await lessonLink.click();
      await page.waitForURL(`${base}${expectedHref}`);
      ok('practice lesson row navigates to its PL practice page', page.url() === `${base}${expectedHref}`);
      ok('practice page declares lang="pl"', await page.locator('html').getAttribute('lang') === 'pl');
      await page.close();
    }

    await browser.close();
  } finally {
    server.kill();
  }

  if (failures > 0) {
    console.error(`\n[pl-home] RESULT: FAIL (${failures} check(s) failed)`);
    process.exitCode = 1;
  } else {
    console.log('\n[pl-home] RESULT: PASS');
  }
})().catch((err) => {
  console.error('[pl-home] FATAL:', err);
  process.exit(1);
});
