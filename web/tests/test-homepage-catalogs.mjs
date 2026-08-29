// Regression coverage for the homepage hero and three generated catalogs: the
// Practice catalog (manifest/practice_manifest.json, 493 entries), the
// Projects catalog (manifest/projects_manifest.json, 13 real projects), and
// the Course Journey roadmap (manifest/coverage_manifest.json, 24 chapters).
//
// scripts/validate_site_catalogs.py already proves every rendered entry
// maps 1:1 onto its source-of-truth manifest, with no missing/duplicate/
// wrong-route entries, across ALL 493/13/24 items — this suite instead
// exercises the actual rendered UI in a real browser: interactive sampling
// of representative lessons/projects, the progress-aggregation script
// (site/assets/js/progress.js) against seeded localStorage state, the
// Все/В браузере/Локально filter, and responsive layout of the roadmap at
// all three breakpoints.
//
// Runs against a local static build (dist/) served with cross-origin
// isolation headers (scripts/dev_server.py). Requires the Playwright
// Chromium browser: `npx playwright install chromium`.
//
// Usage: node web/tests/test-homepage-catalogs.mjs (or `npm run test:homepage` from web/)

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
function log(...args) { console.log('[homepage]', ...args); }

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

const PRACTICE_MANIFEST = JSON.parse(fs.readFileSync(path.join(ROOT, 'manifest', 'practice_manifest.json'), 'utf-8'));
const PROJECTS_MANIFEST = JSON.parse(fs.readFileSync(path.join(ROOT, 'manifest', 'projects_manifest.json'), 'utf-8')).projects;
const COVERAGE_MANIFEST = JSON.parse(fs.readFileSync(path.join(ROOT, 'manifest', 'coverage_manifest.json'), 'utf-8'));
const TOTAL_LESSONS = Object.keys(PRACTICE_MANIFEST).length;

const SAMPLE_LESSONS = ['01-01', '03-01', '05-05', '10-05', '15-01', '17-05', '22-02', '23-03'];
const HERO_VIEWPORTS = [[1920, 1080], [1440, 900], [1280, 800], [1024, 900], [768, 1024], [430, 932], [390, 844], [360, 800]];

(async () => {
  log('Building dist/...');
  execSync('bash scripts/build_vercel.sh', { cwd: ROOT, stdio: 'inherit' });

  const port = await getFreePort();
  const distDir = path.join(ROOT, 'dist');
  const server = spawn('python3', [path.join(ROOT, 'scripts', 'dev_server.py'), String(port), distDir], { stdio: 'ignore' });
  const base = `http://localhost:${port}`;

  try {
    await waitForServer(`${base}/index.html`);
    const browser = await chromium.launch();

    // =========================================================================
    // HOMEPAGE HERO
    // =========================================================================
    log('Homepage hero: Python identity, computational domains, routes, and responsive containment');
    for (const [width, height] of HERO_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const consoleErrors = [];
      page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
      page.on('pageerror', (error) => consoleErrors.push(error.message));
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      await page.waitForTimeout(1100);

      const result = await page.evaluate(() => {
        const box = (selector) => {
          const rect = document.querySelector(selector).getBoundingClientRect();
          return { left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom };
        };
        const overlaps = (a, b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
        const system = box('.hero-system');
        const content = box('.home-hero__content');
        const cta = box('.home-cta');
        const moduleBoxes = [...document.querySelectorAll('.hero-module')].map((module) => {
          const rect = module.getBoundingClientRect();
          return { left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom };
        });
        const logo = document.querySelector('.home-hero .kicker img');
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          logoLoaded: logo.complete && logo.naturalWidth > 0,
          logoSrc: logo.getAttribute('src'),
          kicker: document.querySelector('.home-hero .kicker').innerText.trim(),
          moduleCount: moduleBoxes.length,
          modulesContained: moduleBoxes.every((rect) => rect.left >= system.left - 6 && rect.right <= system.right + 6 && rect.top >= system.top - 6 && rect.bottom <= system.bottom + 6),
          contentSystemOverlap: overlaps(content, system),
          systemBelowCta: system.top >= cta.bottom - 1,
          oldDecorationPresent: getComputedStyle(document.querySelector('.home-hero'), '::after').content.includes('</>'),
          startHref: document.querySelector('.home-cta .btn-primary').getAttribute('href'),
          bookHref: document.querySelector('.home-cta .btn-ghost').getAttribute('href'),
        };
      });

      const viewport = `${width}x${height}`;
      ok(`${viewport}: no horizontal overflow`, !result.overflow);
      ok(`${viewport}: local Python logo is loaded`, result.logoLoaded && result.logoSrc === '/assets/img/brand/python-logo-mark.svg');
      ok(`${viewport}: eyebrow preserves Python 3.14 course identity`, result.kicker === 'PYTHON 3.14 · БЕСПЛАТНЫЙ ИНТЕРАКТИВНЫЙ КУРС');
      ok(`${viewport}: CODE / GRAPH / APP / GAME modules are present and contained`, result.moduleCount === 4 && result.modulesContained);
      ok(`${viewport}: old </> decoration is absent`, !result.oldDecorationPresent);
      ok(`${viewport}: hero produced no console errors`, consoleErrors.length === 0);
      if (width >= 1200) ok(`${viewport}: text and computational plane do not collide`, !result.contentSystemOverlap);
      if (width <= 1100) ok(`${viewport}: text-first layout places the plane below the CTAs`, result.systemBelowCta);
      ok(`${viewport}: CTA routes are unchanged`, result.startHref === '/chapters/glava-01/index.html' && result.bookHref === '/front-matter/vvedenie.html');
      await page.close();
    }

    log('Homepage hero: reduced-motion keeps the complete illustration static');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.emulateMedia({ reducedMotion: 'reduce' });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      const reduced = await page.evaluate(() => {
        const selectors = ['.hero-system__grid', '.hero-system__prompt', '.hero-signal', '.hero-core__orbit', '.hero-code-cursor', '.hero-game__sprite'];
        return {
          animations: selectors.map((selector) => getComputedStyle(document.querySelector(selector)).animationName),
          modulesVisible: [...document.querySelectorAll('.hero-module')].every((module) => module.getBoundingClientRect().width > 0),
          graphComplete: getComputedStyle(document.querySelector('.hero-plot__curve')).strokeDashoffset === '0px',
        };
      });
      ok('reduced motion: all continuous decorative animations are disabled', reduced.animations.every((name) => name === 'none'));
      ok('reduced motion: the full four-domain illustration remains visible', reduced.modulesVisible);
      ok('reduced motion: graph remains in its completed static state', reduced.graphComplete);
      await page.close();
    }

    if (process.env.HERO_ONLY === '1') {
      await browser.close();
      console.log(`\n[homepage] HERO RESULT: ${failures === 0 ? 'PASS' : `FAIL (${failures} check(s) failed)`}`);
      if (failures > 0) process.exitCode = 1;
      return;
    }

    // =========================================================================
    // PRACTICE CATALOG
    // =========================================================================
    log('Practice catalog: renders, count derives from manifest, grouping, sample links');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html#praktika`, { waitUntil: 'networkidle' });

      const rowCount = await page.locator('.practice-lesson-row').count();
      ok(`Practice catalog renders exactly ${TOTAL_LESSONS} lesson rows (manifest count, not hardcoded)`, rowCount === TOTAL_LESSONS);

      const groupCount = await page.locator('.practice-chapter-group').count();
      const expectedGroups = new Set(Object.keys(PRACTICE_MANIFEST).map((id) => id.split('-')[0])).size;
      ok(`Practice catalog groups into ${expectedGroups} chapters with practice`, groupCount === expectedGroups);

      for (const lessonId of SAMPLE_LESSONS) {
        const row = page.locator(`.practice-lesson-row[data-lesson-id="${lessonId}"]`);
        const count = await row.count();
        ok(`${lessonId}: exactly one row rendered`, count === 1);
        if (count === 1) {
          const href = await row.getAttribute('href');
          ok(`${lessonId}: links to /practice/${lessonId}/index.html`, href === `/practice/${lessonId}/index.html`);
          const idText = await row.locator('.plr-id').textContent();
          ok(`${lessonId}: lesson id visible`, idText.trim() === lessonId);
          const badgeText = await row.locator('.plr-badge').textContent();
          const expectedMode = PRACTICE_MANIFEST[lessonId].backend === 'browser-pyodide' ? 'В браузере' : 'Локально';
          ok(`${lessonId}: badge reads "${expectedMode}" (no raw backend string exposed)`, badgeText.trim() === expectedMode);
        }
      }

      // No raw .ipynb as a primary catalog action.
      const ipynbPrimaryLinks = await page.locator('.practice-lesson-row[href$=".ipynb"]').count();
      ok('zero practice rows use a raw .ipynb as the primary action', ipynbPrimaryLinks === 0);

      await page.close();
    }

    log('Practice catalog: Все/В браузере/Локально filter');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html#praktika`, { waitUntil: 'networkidle' });
      // Open one details group so its rows are actually laid out for visibility checks.
      await page.locator('.practice-chapter-group').first().locator('.pcg-summary').click();

      await page.click('.pf-btn[data-filter="local"]');
      await page.waitForTimeout(150);
      const visibleAfterLocalFilter = await page.locator('.practice-lesson-row[data-mode="browser"]:visible').count();
      ok('filter "Локально": zero browser-mode rows visible', visibleAfterLocalFilter === 0);

      await page.click('.pf-btn[data-filter="browser"]');
      await page.waitForTimeout(150);
      const visibleAfterBrowserFilter = await page.locator('.practice-lesson-row[data-mode="local"]:visible').count();
      ok('filter "В браузере": zero local-mode rows visible', visibleAfterBrowserFilter === 0);

      await page.click('.pf-btn[data-filter="all"]');
      await page.waitForTimeout(150);
      // Only the one <details> group opened above is actually laid out (every
      // other group is legitimately collapsed by design — 122 rows must not
      // render as a flat wall), so "Все" is checked within that open group,
      // not against the full 122 across the whole (mostly-collapsed) page.
      const openGroup = page.locator('.practice-chapter-group').first();
      const rowsInOpenGroup = await openGroup.locator('.practice-lesson-row').count();
      const visibleInOpenGroup = await openGroup.locator('.practice-lesson-row:visible').count();
      ok(`filter "Все": all ${rowsInOpenGroup} rows in the open group visible again`, visibleInOpenGroup === rowsInOpenGroup);
      const anyRowHiddenByDisplayNone = await page.locator('.practice-lesson-row[style*="display: none"]').count();
      ok('filter "Все": no row is left with an explicit display:none from the filter', anyRowHiddenByDisplayNone === 0);
      await page.close();
    }

    log('Practice catalog: progress aggregation reflects seeded localStorage state');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      await page.evaluate(() => {
        localStorage.setItem('cartesian.python.progress.v1', JSON.stringify({
          '01-01': { status: 'completed', score: 100 },
          '03-01': { status: 'completed', score: 100 },
        }));
      });
      await page.reload({ waitUntil: 'networkidle' });
      const summaryDetail = await page.locator('#journey-progress .jp-detail').textContent();
      ok(`course-wide summary reflects 2 completed lessons`, summaryDetail.includes(`2 из ${TOTAL_LESSONS}`));
      const check0101 = page.locator('.practice-lesson-row[data-lesson-id="01-01"] .plr-check');
      ok('01-01 row shows a completed checkmark', await check0101.evaluate((el) => el.classList.contains('done')));
      await page.evaluate(() => localStorage.removeItem('cartesian.python.progress.v1'));
      await page.close();
    }

    // =========================================================================
    // PROJECTS CATALOG
    // =========================================================================
    log(`Projects catalog: ${PROJECTS_MANIFEST.length} real project cards, each visible/correct/leads to its own page`);
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html#proekty`, { waitUntil: 'networkidle' });
      const cardCount = await page.locator('.project-card').count();
      ok(`Projects catalog renders exactly ${PROJECTS_MANIFEST.length} cards (manifest count)`, cardCount === PROJECTS_MANIFEST.length);

      for (const proj of PROJECTS_MANIFEST) {
        const card = page.locator(`.project-card[href="/projects/${proj.slug}/"]`);
        ok(`${proj.slug}: exactly one card`, (await card.count()) === 1);
        const svgVisible = await card.locator('.project-card-visual svg').isVisible();
        ok(`${proj.slug}: visual illustration visible`, svgVisible);
        const titleText = await card.locator('.project-card-title').textContent();
        ok(`${proj.slug}: title matches manifest ("${proj.title}")`, titleText.trim() === proj.title);
        const descVisible = await card.locator('.project-card-desc').isVisible();
        ok(`${proj.slug}: description visible`, descVisible);
        const ctaVisible = await card.locator('.project-card-cta').isVisible();
        ok(`${proj.slug}: CTA visible`, ctaVisible);
      }
      await page.close();
    }

    log('Projects catalog: click-through identity check (sample)');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html#proekty`, { waitUntil: 'networkidle' });
      const sample = PROJECTS_MANIFEST[0];
      await page.click(`.project-card[href="/projects/${sample.slug}/"]`);
      await page.waitForLoadState('networkidle');
      const h1 = await page.locator('h1').textContent();
      ok(`clicking "${sample.title}" card lands on a page identifying as "${sample.title}"`, h1.trim() === sample.title);
      const backLink = await page.locator('.breadcrumb a').getAttribute('href');
      ok('detail page has a working "Все проекты" back link', backLink === '/index.html#proekty');
      await page.close();
    }

    // =========================================================================
    // COURSE JOURNEY ROADMAP
    // =========================================================================
    const chapters = COVERAGE_MANIFEST.chapters.filter((c) => c.kind === 'chapter');
    log(`Course roadmap: ${chapters.length} chapter milestones, no fake locking, responsive`);
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html#glavy`, { waitUntil: 'networkidle' });

      const nodeCount = await page.locator('.journey-node').count();
      ok(`roadmap renders exactly ${chapters.length} milestones`, nodeCount === chapters.length);

      const chapterNumbers = await page.locator('.journey-node').evaluateAll((els) => els.map((el) => el.dataset.chapter));
      const uniqueNumbers = new Set(chapterNumbers);
      ok('every chapter number 1..24 appears exactly once', uniqueNumbers.size === chapterNumbers.length && chapters.every((c) => uniqueNumbers.has(String(c.number))));

      // No fake "locked" state anywhere in the roadmap.
      const lockedMentions = await page.locator('.journey-node:has-text("Заблокировано"), .journey-node:has-text("заблокирован")').count();
      ok('zero milestones claim to be locked (all chapters are actually reachable)', lockedMentions === 0);
      const allLinksEnabled = await page.locator('.journey-node .jn-card').evaluateAll((els) => els.every((el) => !el.classList.contains('disabled')));
      ok('every milestone link is enabled (no disabled class)', allLinksEnabled);

      // Progress summary renders with a real (not hardcoded) total.
      const totalAttr = await page.locator('#journey-progress').getAttribute('data-total-lessons');
      ok(`progress summary total-lessons = ${TOTAL_LESSONS} (from manifest, not hardcoded)`, totalAttr === String(TOTAL_LESSONS));

      await page.close();
    }

    log('Course roadmap: seeded progress drives completed/in-progress/current state honestly');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      const ch1Ids = Object.keys(PRACTICE_MANIFEST).filter((id) => id.startsWith('01-'));
      const seeded = {};
      ch1Ids.forEach((id) => { seeded[id] = { status: 'completed', score: 100 }; });
      await page.evaluate((data) => {
        localStorage.setItem('cartesian.python.progress.v1', JSON.stringify(data));
      }, seeded);
      await page.reload({ waitUntil: 'networkidle' });

      const ch1State = await page.locator('.journey-node[data-chapter="1"]').getAttribute('data-state');
      ok('chapter 1 (fully seeded as done) shows state=completed', ch1State === 'completed');
      const ch1Badge = await page.locator('.journey-node[data-chapter="1"] .jn-state-badge').textContent();
      ok('chapter 1 badge reads "Завершено" (not a raw implementation string)', ch1Badge.trim() === 'Завершено');

      const ch2State = await page.locator('.journey-node[data-chapter="2"]').getAttribute('data-state');
      ok('chapter 2 (zero real lessons) shows state=no-lessons, not falsely completed', ch2State === 'no-lessons');

      const currentCount = await page.locator('.journey-node.state-current').count();
      ok('exactly one milestone is marked as the current chapter', currentCount === 1);

      await page.evaluate(() => localStorage.removeItem('cartesian.python.progress.v1'));
      await page.close();
    }

    log('Course roadmap: mobile rail (390x844) does not overflow, desktop zig-zag (1440x900) does not overlap');
    {
      const mobile = await browser.newPage({ viewport: { width: 390, height: 844 } });
      await mobile.goto(`${base}/index.html#glavy`, { waitUntil: 'networkidle' });
      const mobileOverflow = await mobile.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
      ok('mobile roadmap: no horizontal overflow', !mobileOverflow);
      const railLeft = await mobile.evaluate(() => {
        const rail = document.querySelector('.journey-rail');
        return getComputedStyle(rail, '::before').left;
      });
      ok('mobile roadmap: rail is left-aligned (not the desktop centered zig-zag)', railLeft !== '50%');
      await mobile.close();

      const desktop = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await desktop.goto(`${base}/index.html#glavy`, { waitUntil: 'networkidle' });
      const overlap = await desktop.evaluate(() => {
        const cards = Array.from(document.querySelectorAll('.jn-card'));
        for (let i = 1; i < cards.length; i++) {
          const a = cards[i - 1].getBoundingClientRect();
          const b = cards[i].getBoundingClientRect();
          const horizontallyOverlaps = a.left < b.right && b.left < a.right;
          const verticallyOverlaps = a.top < b.bottom && b.top < a.bottom;
          if (horizontallyOverlaps && verticallyOverlaps) return true;
        }
        return false;
      });
      ok('desktop roadmap: no two adjacent milestone cards visually overlap', !overlap);
      await desktop.close();
    }

    log('Course roadmap: prefers-reduced-motion still renders a usable roadmap');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
      await page.goto(`${base}/index.html#glavy`, { waitUntil: 'networkidle' });
      const nodeCount = await page.locator('.journey-node').count();
      ok('roadmap still renders all milestones with prefers-reduced-motion', nodeCount === chapters.length);
      const firstCardVisible = await page.locator('.journey-node').first().locator('.jn-card').isVisible();
      ok('roadmap cards remain visible/usable with prefers-reduced-motion', firstCardVisible);
      await page.close();
    }

    // Tablet pass for both catalogs (breadth, not full duplication of the desktop assertions).
    log('Tablet (768x1024): practice catalog and projects catalog both usable, no overflow');
    {
      const page = await browser.newPage({ viewport: { width: 768, height: 1024 } });
      await page.goto(`${base}/index.html#praktika`, { waitUntil: 'networkidle' });
      let overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
      ok('tablet: practice catalog no horizontal overflow', !overflow);
      await page.goto(`${base}/index.html#proekty`, { waitUntil: 'networkidle' });
      overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
      ok('tablet: projects catalog no horizontal overflow', !overflow);
      const cardCount = await page.locator('.project-card').count();
      ok(`tablet: all ${PROJECTS_MANIFEST.length} project cards present`, cardCount === PROJECTS_MANIFEST.length);
      await page.close();
    }

    await browser.close();
  } finally {
    server.kill();
  }

  if (failures > 0) {
    console.error(`\n[homepage] RESULT: FAIL (${failures} check(s) failed)`);
    process.exitCode = 1;
  } else {
    console.log('\n[homepage] RESULT: PASS');
  }
})().catch((err) => {
  console.error('[homepage] FATAL:', err);
  process.exit(1);
});
