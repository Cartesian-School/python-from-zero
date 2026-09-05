// Regression test for site-wide navigation (site_lib.py's site_header() /
// mobile_nav_links(), site/assets/js/nav.js). Exists specifically to catch
// the bug found during the SEO/navigation audit: the top-nav was hidden
// entirely on mobile (`.top-nav { display: none }`) while the visible
// hamburger button only toggled the page-local chapter TOC, not the
// site-wide menu — so on mobile the primary navigation was completely
// unreachable from any page, including the homepage (which had no
// hamburger button at all). Fixed by giving every page a mobile drawer
// that includes the real top-nav links, driven by nav.js.
//
// Runs against a local static build (dist/), not the live Vercel preview,
// so it works offline / in CI without Vercel auth. Requires the Playwright
// Chromium browser: `npx playwright install chromium` (run once).
//
// Usage: node web/tests/test-navigation.mjs   (or `npm run test:nav` from web/)

import { chromium } from 'playwright';
import { execSync, spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import net from 'node:net';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');

let failures = 0;
function ok(label, cond) {
  if (cond) {
    console.log(`  [ok] ${label}`);
  } else {
    console.error(`  [FAIL] ${label}`);
    failures += 1;
  }
}

function log(...args) {
  console.log('[nav-test]', ...args);
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

const TOP_NAV = [
  ['О курсе', '#o-kurse', 'О курсе'],
  ['Главы', '#glavy', 'Главы'],
  ['Практика', '#praktika', 'Практика'],
  ['Проекты', '#proekty', 'Проекты'],
  ['Справочник', '#spravochnik', 'Справочник'],
];

(async () => {
  log('Building dist/ (bash scripts/build_vercel.sh)...');
  execSync('bash scripts/build_vercel.sh', { cwd: ROOT, stdio: 'inherit' });

  const port = await getFreePort();
  const distDir = path.join(ROOT, 'dist');
  log(`Starting static server on :${port} for ${distDir}`);
  const server = spawn('python3', [path.join(ROOT, 'scripts', 'dev_server.py'), String(port), distDir], { stdio: 'ignore' });
  const base = `http://localhost:${port}`;

  try {
    await waitForServer(`${base}/index.html`);
    const browser = await chromium.launch();

    // --- Desktop: chapter page top-nav, every item ---
    log('Desktop (1440x900): chapter page top-nav');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      const chapterUrl = `${base}/chapters/glava-03/03-01-sozdanie-i-zapusk-programm.html`;
      await page.goto(chapterUrl, { waitUntil: 'networkidle' });

      const activeText = await page.locator('.top-nav a.active').textContent();
      ok('active top-nav item on a chapter page is "Главы"', activeText.trim() === 'Главы');

      for (const [label, fragment, expectedHeading] of TOP_NAV) {
        await page.goto(chapterUrl, { waitUntil: 'networkidle' });
        await page.click(`.top-nav a:has-text("${label}")`);
        await page.waitForLoadState('networkidle');
        const url = new URL(page.url());
        ok(`desktop "${label}" -> ${fragment}`, url.pathname === '/index.html' && url.hash === fragment);
        const check = await page.evaluate((frag) => {
          const el = document.getElementById(frag.slice(1));
          if (!el) return { visible: false, heading: null };
          const r = el.getBoundingClientRect();
          const visible = r.top >= 0 && r.top < window.innerHeight;
          const h2 = el.querySelector('h2');
          return { visible, heading: h2 ? h2.textContent.trim() : null };
        }, fragment);
        ok(`desktop "${label}" target is visible (not hidden under sticky header)`, check.visible);
        ok(`desktop "${label}" target has heading "${expectedHeading}"`, check.heading === expectedHeading);
      }
      await page.close();
    }

    // --- Tablet: chapter page top-nav, every item ---
    log('Tablet (768x1024): chapter page top-nav');
    {
      const page = await browser.newPage({ viewport: { width: 768, height: 1024 } });
      const chapterUrl = `${base}/chapters/glava-03/03-01-sozdanie-i-zapusk-programm.html`;

      for (const [label, fragment, expectedHeading] of TOP_NAV) {
        await page.goto(chapterUrl, { waitUntil: 'networkidle' });
        // At 768px the layout is already in the mobile/hamburger breakpoint
        // (theory.css's @media (max-width: 860px)) — use the drawer, exactly
        // as a real tablet visitor would, not the (hidden) desktop top-nav.
        await page.click('.nav-toggle');
        await page.click(`#mobile-nav-panel a:has-text("${label}")`);
        await page.waitForTimeout(200);
        const url = new URL(page.url());
        ok(`tablet "${label}" -> ${fragment}`, url.pathname === '/index.html' && url.hash === fragment);
        const check = await page.evaluate((frag) => {
          const el = document.getElementById(frag.slice(1));
          if (!el) return { visible: false, heading: null };
          const r = el.getBoundingClientRect();
          const visible = r.top >= 0 && r.top < window.innerHeight;
          const h2 = el.querySelector('h2');
          return { visible, heading: h2 ? h2.textContent.trim() : null };
        }, fragment);
        ok(`tablet "${label}" target is visible (not hidden under sticky header)`, check.visible);
        ok(`tablet "${label}" target has heading "${expectedHeading}"`, check.heading === expectedHeading);
      }
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
      ok('tablet: no horizontal overflow on homepage', !overflow);
      await page.close();
    }

    // --- Desktop: practice page logo/home link ---
    log('Desktop (1440x900): practice page home link');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/practice/03-01/index.html`, { waitUntil: 'networkidle' });
      const href = await page.locator('.brand').getAttribute('href');
      ok('practice page .brand is a link to /index.html', href === '/index.html');
      await page.close();
    }

    // --- Desktop: active main-menu state follows scroll position (IntersectionObserver) ---
    log('Desktop (1440x900): active menu state on scroll (site/assets/js/progress.js)');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      await page.click('a[href="/index.html#proekty"]');
      await page.waitForTimeout(400); // IntersectionObserver fires async after scroll settles
      const activeAfterProekty = await page.locator('.top-nav a.active').textContent();
      ok('scrolling to #proekty makes "Проекты" the active menu item', activeAfterProekty.trim() === 'Проекты');

      await page.click('a[href="/index.html#spravochnik"]');
      await page.waitForTimeout(400);
      const activeAfterSpravochnik = await page.locator('.top-nav a.active').textContent();
      ok('scrolling to #spravochnik makes "Справочник" the active menu item', activeAfterSpravochnik.trim() === 'Справочник');
      await page.close();
    }

    // --- Mobile: homepage hamburger reveals real nav and closes correctly ---
    log('Mobile (390x844): homepage hamburger menu');
    {
      const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });

      ok('hamburger button visible on mobile', await page.locator('.nav-toggle').isVisible());
      ok('top-nav hidden on mobile (menu lives in the drawer instead)', !(await page.locator('.top-nav').isVisible()));

      await page.click('.nav-toggle');
      const expandedAfterOpen = await page.locator('.nav-toggle').getAttribute('aria-expanded');
      ok('aria-expanded="true" after opening', expandedAfterOpen === 'true');
      const linkCount = await page.locator('#mobile-nav-panel a').count();
      ok('drawer contains all 5 top-nav links', linkCount === 5);

      for (const [label, fragment, expectedHeading] of TOP_NAV) {
        await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
        await page.click('.nav-toggle');
        await page.click(`#mobile-nav-panel a:has-text("${label}")`);
        await page.waitForTimeout(200);
        const url = new URL(page.url());
        ok(`mobile "${label}" -> ${fragment}`, url.pathname === '/index.html' && url.hash === fragment);
        const closed = await page.evaluate(() => !document.getElementById('mobile-nav-panel').classList.contains('open'));
        ok(`mobile drawer closes after selecting "${label}"`, closed);
        const heading = await page.evaluate((frag) => {
          const el = document.getElementById(frag.slice(1));
          const h2 = el && el.querySelector('h2');
          return h2 ? h2.textContent.trim() : null;
        }, fragment);
        ok(`mobile "${label}" target has heading "${expectedHeading}"`, heading === expectedHeading);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
        ok(`mobile "${label}": no horizontal overflow`, !overflow);
      }

      await page.click('.nav-toggle');
      await page.keyboard.press('Escape');
      const closedByEscape = await page.evaluate(() => !document.getElementById('mobile-nav-panel').classList.contains('open'));
      ok('Escape closes the open drawer', closedByEscape);
      await page.close();
    }

    // --- Mobile: chapter page drawer includes both site nav and chapter TOC ---
    log('Mobile (390x844): chapter page drawer (site nav + local TOC together)');
    {
      const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
      await page.goto(`${base}/chapters/glava-03/03-01-sozdanie-i-zapusk-programm.html`, { waitUntil: 'networkidle' });
      await page.click('.nav-toggle');
      const hasSiteNav = await page.locator('#mobile-nav-panel .mobile-nav-links a:has-text("Практика")').count();
      const hasChapterToc = await page.locator('#mobile-nav-panel .toc-list a:has-text("Создание и запуск программ")').count();
      ok('mobile drawer on a chapter page includes site-wide nav', hasSiteNav > 0);
      ok('mobile drawer on a chapter page also includes the chapter TOC', hasChapterToc > 0);
      await page.close();
    }

    // =========================================================================
    // Regression: deep-scroll mobile menu visibility (Product Owner report).
    //
    // Root cause: the mobile drawer (#mobile-nav-panel) used to be a normal
    // document-flow element sitting right after the sticky header. Opening it
    // inserted/revealed a block near the TOP of the document; if the reader
    // had scrolled far down (e.g. to #praktika), that insertion point was
    // above the current viewport, so the drawer's state changed (.open class,
    // aria-expanded) but nothing visible appeared, and the drawer's links were
    // not just hidden but literally not under the pointer at any point in the
    // viewport (see the elementFromPoint hit-test below).
    //
    // Fix: the drawer is now position:fixed, anchored to
    // var(--mobile-nav-top) (site/assets/js/nav.js measures the real header's
    // rendered bottom edge — see updateMobileNavTop()), so it always renders
    // directly under the header regardless of scroll position, and opening/
    // closing it never touches document flow (so scrollY never moves).
    // =========================================================================

    async function deepScrollMenuCheck(page, url, scrollTarget, headerSelector, tag) {
      await page.goto(url, { waitUntil: 'networkidle' });
      if (scrollTarget) {
        await page.locator(scrollTarget).scrollIntoViewIfNeeded();
      } else {
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      }
      await page.waitForTimeout(50);

      const before = await page.evaluate(() => window.scrollY);
      ok(`${tag}: scrolled away from the top before opening`, before > 100);

      await page.click('.nav-toggle');
      const panel = page.locator('#mobile-nav-panel');
      ok(`${tag}: panel reports visible after opening`, await panel.isVisible());

      const panelBox = await panel.boundingBox();
      const headerBox = await page.locator(headerSelector).boundingBox();
      ok(`${tag}: panel has a bounding box`, panelBox !== null);
      if (panelBox && headerBox) {
        const gap = panelBox.y - (headerBox.y + headerBox.height);
        ok(`${tag}: panel top sits flush under the header (gap=${gap.toFixed(1)}px)`, Math.abs(gap) <= 1);
        ok(`${tag}: panel is within the viewport, not above it`, panelBox.y >= 0 && panelBox.y < page.viewportSize().height);
      }

      const after = await page.evaluate(() => window.scrollY);
      ok(`${tag}: opening the menu does not move scroll position (before=${before}, after=${after})`, Math.abs(after - before) <= 2);

      return { before, after, panelBox, headerBox };
    }

    log('Regression: #praktika deep scroll on homepage (390x844)');
    {
      const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
      await deepScrollMenuCheck(page, `${base}/index.html`, '#praktika', '.site-header', 'homepage/#praktika');

      // Pointer hit-test: the visible link must actually receive the click,
      // not just exist in the DOM under an invisible/mispositioned ancestor.
      const link = page.locator('#mobile-nav-panel .mobile-nav-links a:has-text("Проекты")');
      const box = await link.boundingBox();
      ok('homepage/#praktika: "Проекты" link has a bounding box', box !== null);
      const hitOk = box
        ? await page.evaluate(([x, y]) => {
            const el = document.elementFromPoint(x, y);
            return !!(el && el.closest('a'));
          }, [box.x + box.width / 2, box.y + box.height / 2])
        : false;
      ok('homepage/#praktika: elementFromPoint on "Проекты" resolves to the link (not an overlay)', hitOk);

      await link.click();
      await page.waitForLoadState('networkidle');
      const url = new URL(page.url());
      ok('homepage/#praktika: clicking "Проекты" navigates to #proekty', url.hash === '#proekty');

      const closed = await page.evaluate(() => !document.getElementById('mobile-nav-panel').classList.contains('open'));
      ok('homepage/#praktika: drawer closes after the link click', closed);
      await page.close();
    }

    log('Regression: deep scroll on chapter/front-matter/project routes (390x844)');
    {
      const routes = [
        [`${base}/chapters/glava-09/09-16-not.html`, '.site-header', 'chapter lesson (glava-09)'],
        [`${base}/front-matter/ob-avtore.html`, '.site-header', 'front matter (ob-avtore)'],
        [`${base}/projects/safesort/index.html`, '.site-header', 'project page (safesort)'],
      ];
      for (const [url, headerSelector, tag] of routes) {
        const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
        await deepScrollMenuCheck(page, url, null, headerSelector, tag);

        const link = page.locator('#mobile-nav-panel .mobile-nav-links a:has-text("Практика")');
        const box = await link.boundingBox();
        const hitOk = box
          ? await page.evaluate(([x, y]) => {
              const el = document.elementFromPoint(x, y);
              return !!(el && el.closest('a'));
            }, [box.x + box.width / 2, box.y + box.height / 2])
          : false;
        ok(`${tag}: "Практика" nav link is pointer-hittable after deep scroll`, hitOk);
        await page.close();
      }
    }

    log('Regression: interactive practice tool page (non-sticky .practice-header)');
    {
      // The practice tool has its own header (.practice-header) that is NOT
      // sticky (it has its own sticky toolbar below it instead) — nav.js
      // must still measure whichever header is actually on the page.
      const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
      await page.goto(`${base}/practice/03-01/index.html`, { waitUntil: 'networkidle' });
      await page.click('.nav-toggle');
      const panelBox = await page.locator('#mobile-nav-panel').boundingBox();
      const headerBox = await page.locator('.practice-header').boundingBox();
      const gap = panelBox.y - (headerBox.y + headerBox.height);
      ok(`practice tool: panel sits flush under .practice-header (gap=${gap.toFixed(1)}px)`, Math.abs(gap) <= 1);
      await page.close();
    }

    log('Regression: click outside the open drawer closes it');
    {
      const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      await page.click('.nav-toggle');
      ok('click-outside: drawer opens', await page.evaluate(() => document.getElementById('mobile-nav-panel').classList.contains('open')));
      await page.mouse.click(300, 700); // homepage content below the drawer
      await page.waitForTimeout(100);
      const closed = await page.evaluate(() => !document.getElementById('mobile-nav-panel').classList.contains('open'));
      const expanded = await page.locator('.nav-toggle').getAttribute('aria-expanded');
      ok('click-outside: drawer closes on outside click', closed);
      ok('click-outside: aria-expanded is back to "false"', expanded === 'false');
      await page.close();
    }

    log('Regression: resize across the mobile/desktop breakpoint resets stale state');
    {
      const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      await page.click('.nav-toggle');
      ok('resize: drawer open before resize', await page.evaluate(() => document.getElementById('mobile-nav-panel').classList.contains('open')));

      await page.setViewportSize({ width: 1280, height: 900 });
      await page.waitForTimeout(150);
      const openAtDesktop = await page.evaluate(() => document.getElementById('mobile-nav-panel').classList.contains('open'));
      const expandedAtDesktop = await page.locator('.nav-toggle').getAttribute('aria-expanded');
      ok('resize: no stale .open after growing past the breakpoint', !openAtDesktop);
      ok('resize: aria-expanded reset to "false" after growing past the breakpoint', expandedAtDesktop === 'false');

      await page.setViewportSize({ width: 390, height: 844 });
      await page.waitForTimeout(150);
      const openBackAtMobile = await page.evaluate(() => document.getElementById('mobile-nav-panel').classList.contains('open'));
      ok('resize: drawer starts closed after shrinking back to mobile', !openBackAtMobile);
      await page.close();
    }

    log('Viewport matrix: 360/390/430/768 x top/#praktika/#proekty/#spravochnik');
    {
      const viewports = [[360, 800], [390, 844], [430, 932], [768, 1024]];
      const scrollTargets = ['TOP', '#praktika', '#proekty', '#spravochnik'];
      for (const [w, h] of viewports) {
        const page = await browser.newPage({ viewport: { width: w, height: h } });
        await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
        for (const target of scrollTargets) {
          if (target === 'TOP') {
            await page.evaluate(() => window.scrollTo(0, 0));
          } else {
            await page.locator(target).scrollIntoViewIfNeeded();
          }
          await page.waitForTimeout(50);
          const before = await page.evaluate(() => window.scrollY);
          await page.click('.nav-toggle');
          await page.waitForTimeout(80);

          const panelBox = await page.locator('#mobile-nav-panel').boundingBox();
          const headerBox = await page.locator('.site-header').boundingBox();
          const after = await page.evaluate(() => window.scrollY);
          const gap = panelBox.y - (headerBox.y + headerBox.height);
          const tag = `${w}x${h} @ ${target}`;

          ok(`${tag}: no gap/overlap between header and panel (${gap.toFixed(1)}px)`, Math.abs(gap) <= 1);
          ok(`${tag}: scroll position unchanged`, Math.abs(after - before) <= 2);

          let allHit = true;
          for (const label of TOP_NAV.map((t) => t[0])) {
            const box = await page.locator(`#mobile-nav-panel .mobile-nav-links a:has-text("${label}")`).boundingBox();
            if (!box) { allHit = false; continue; }
            const hit = await page.evaluate(([x, y]) => {
              const el = document.elementFromPoint(x, y);
              return !!(el && el.closest('a'));
            }, [box.x + box.width / 2, box.y + box.height / 2]);
            if (!hit) allHit = false;
          }
          ok(`${tag}: all 5 nav links are pointer-hittable`, allHit);

          const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
          ok(`${tag}: no horizontal overflow`, !overflow);

          await page.click('.nav-toggle'); // close before next iteration
          await page.waitForTimeout(50);
        }
        await page.close();
      }
    }

    log('Desktop regression: 1024/1280/1440/1920 unaffected by the drawer fix');
    {
      for (const w of [1024, 1280, 1440, 1920]) {
        const page = await browser.newPage({ viewport: { width: w, height: 900 } });
        await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
        ok(`desktop ${w}: top-nav visible`, await page.locator('.top-nav').isVisible());
        ok(`desktop ${w}: hamburger hidden`, !(await page.locator('.nav-toggle').isVisible()));
        const panelDisplay = await page.evaluate(() => getComputedStyle(document.getElementById('mobile-nav-panel')).display);
        ok(`desktop ${w}: mobile panel stays display:none even if .open were stale`, panelDisplay === 'none');
        await page.close();
      }
    }

    // =========================================================================
    // Regression: precise anchor positioning under the sticky header
    // (Product Owner report #2).
    //
    // Root cause: theory.css had a blanket [id]{scroll-margin-top:96px} that
    // was never measured against the real header — the actual .site-header
    // renders at 65px (desktop) / 49px (mobile), so 96px overshot by ~30-47px
    // and left a strip of the *previous* section's background visible in the
    // gap between the header and the target section's top edge.
    //
    // Fix: html{scroll-padding-top: calc(--site-header-height + 10px)},
    // with --site-header-height measured live off .site-header's real
    // getBoundingClientRect().height (nav.js, ResizeObserver) rather than a
    // guessed constant. Expected result: every anchor's section boundary
    // lands ~10px below the header's bottom edge, and the element directly
    // under that point belongs to the target section, never the previous one.
    // =========================================================================

    const ANCHOR_MIN_GAP = 4; // px — tolerance floor (target must clear the header)
    const ANCHOR_MAX_GAP = 24; // px — hard ceiling per spec; no documented reason to exceed it

    async function measureAnchorGeometry(page, anchorId, headerSelector) {
      const headerBox = await page.locator(headerSelector).boundingBox();
      const targetBox = await page.locator(`#${anchorId}`).boundingBox();
      const headerBottom = headerBox.y + headerBox.height;
      const gap = targetBox.y - headerBottom;
      const vw = page.viewportSize().width;
      const belongsToTarget = await page.evaluate(
        ([x, y, id]) => {
          const el = document.elementFromPoint(x, y);
          return !!(el && el.closest(`#${id}`));
        },
        [vw / 2, headerBottom + gap + 1, anchorId]
      );
      return { headerBottom, targetTop: targetBox.y, gap, belongsToTarget };
    }

    log('Regression: precise anchor offset via desktop top-nav (1024/1280/1440/1920)');
    {
      for (const w of [1024, 1280, 1440, 1920]) {
        const page = await browser.newPage({ viewport: { width: w, height: 900 } });
        await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
        for (const [label, fragment] of TOP_NAV) {
          await page.click(`.top-nav a:has-text("${label}")`);
          await page.waitForTimeout(150);
          const anchorId = fragment.slice(1);
          const { gap, belongsToTarget } = await measureAnchorGeometry(page, anchorId, '.site-header');
          const tag = `desktop ${w} #${anchorId}`;
          ok(`${tag}: gap is within [${ANCHOR_MIN_GAP}, ${ANCHOR_MAX_GAP}]px (${gap.toFixed(1)}px)`, gap >= ANCHOR_MIN_GAP && gap <= ANCHOR_MAX_GAP);
          ok(`${tag}: point just past the gap belongs to the target section, not the previous one`, belongsToTarget);
        }
        await page.close();
      }
    }

    log('Regression: precise anchor offset via mobile hamburger menu (360/390/430/768)');
    {
      for (const [w, h] of [[360, 800], [390, 844], [430, 932], [768, 1024]]) {
        const page = await browser.newPage({ viewport: { width: w, height: h } });
        for (const [label, fragment] of TOP_NAV) {
          await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
          // Deep-scroll first (task's exact click-order requirement): open
          // from a scrolled position, click, menu closes, THEN it navigates.
          await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight / 2));
          await page.click('.nav-toggle');
          await page.click(`#mobile-nav-panel .mobile-nav-links a:has-text("${label}")`);
          await page.waitForTimeout(150);
          const anchorId = fragment.slice(1);
          const { gap, belongsToTarget } = await measureAnchorGeometry(page, anchorId, '.site-header');
          const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
          const tag = `mobile ${w}x${h} #${anchorId}`;
          ok(`${tag}: gap is within [${ANCHOR_MIN_GAP}, ${ANCHOR_MAX_GAP}]px (${gap.toFixed(1)}px)`, gap >= ANCHOR_MIN_GAP && gap <= ANCHOR_MAX_GAP);
          ok(`${tag}: point just past the gap belongs to the target section, not the previous one`, belongsToTarget);
          ok(`${tag}: no horizontal overflow`, !overflow);
        }
        await page.close();
      }
    }

    log('Regression: direct hash URL load and reload land precisely');
    {
      const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
      for (const [, fragment] of TOP_NAV) {
        const anchorId = fragment.slice(1);
        await page.goto(`${base}/index.html${fragment}`, { waitUntil: 'networkidle' });
        await page.waitForTimeout(150);
        let { gap, belongsToTarget } = await measureAnchorGeometry(page, anchorId, '.site-header');
        ok(`direct load #${anchorId}: gap within range (${gap.toFixed(1)}px)`, gap >= ANCHOR_MIN_GAP && gap <= ANCHOR_MAX_GAP);
        ok(`direct load #${anchorId}: lands on target section`, belongsToTarget);

        await page.reload({ waitUntil: 'networkidle' });
        await page.waitForTimeout(150);
        ({ gap, belongsToTarget } = await measureAnchorGeometry(page, anchorId, '.site-header'));
        ok(`reload #${anchorId}: gap within range after reload (${gap.toFixed(1)}px)`, gap >= ANCHOR_MIN_GAP && gap <= ANCHOR_MAX_GAP);
        ok(`reload #${anchorId}: lands on target section after reload`, belongsToTarget);
      }
      await page.close();
    }

    log('Regression: browser back/forward preserve precise anchor alignment');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      await page.click('.top-nav a:has-text("Практика")');
      await page.waitForTimeout(150);
      await page.click('.top-nav a:has-text("Проекты")');
      await page.waitForTimeout(150);

      await page.goBack();
      await page.waitForTimeout(150);
      let hash = new URL(page.url()).hash;
      ok('back: hash returns to #praktika', hash === '#praktika');
      let { gap, belongsToTarget } = await measureAnchorGeometry(page, 'praktika', '.site-header');
      ok(`back: #praktika gap still precise (${gap.toFixed(1)}px, no accumulated offset)`, gap >= ANCHOR_MIN_GAP && gap <= ANCHOR_MAX_GAP);
      ok('back: #praktika still lands on target section', belongsToTarget);

      await page.goForward();
      await page.waitForTimeout(150);
      hash = new URL(page.url()).hash;
      ok('forward: hash returns to #proekty', hash === '#proekty');
      ({ gap, belongsToTarget } = await measureAnchorGeometry(page, 'proekty', '.site-header'));
      ok(`forward: #proekty gap still precise (${gap.toFixed(1)}px, no accumulated offset)`, gap >= ANCHOR_MIN_GAP && gap <= ANCHOR_MAX_GAP);
      ok('forward: #proekty still lands on target section', belongsToTarget);
      await page.close();
    }

    log('Regression: keyboard activation (Tab + Enter) lands as precisely as a click');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      const link = page.locator('.top-nav a:has-text("Практика")');
      await link.focus();
      ok('keyboard: "Практика" link is focused', await link.evaluate((el) => el === document.activeElement));
      await page.keyboard.press('Enter');
      await page.waitForTimeout(150);
      const hash = new URL(page.url()).hash;
      ok('keyboard: Enter on focused link navigates to #praktika', hash === '#praktika');
      const { gap, belongsToTarget } = await measureAnchorGeometry(page, 'praktika', '.site-header');
      ok(`keyboard: #praktika gap precise via keyboard activation (${gap.toFixed(1)}px)`, gap >= ANCHOR_MIN_GAP && gap <= ANCHOR_MAX_GAP);
      ok('keyboard: #praktika lands on target section via keyboard activation', belongsToTarget);
      await page.close();
    }

    // =========================================================================
    // Regression: focusing a sticky-header control must never scroll the page.
    //
    // scroll-padding-top isn't only consulted for #fragment navigation —
    // browsers also apply it to their own "scroll the focused element into
    // view" behavior, triggered by ANY focus (a mouse click or Tab, from any
    // page, since .site-header is site-wide). An element inside a
    // position:sticky container is already fully visible at a fixed spot no
    // matter the scroll position, but the browser doesn't special-case that:
    // it computed a large, wrong scroll jump trying to satisfy
    // scroll-padding-top's clearance against a sticky element whose position
    // doesn't move. Caught by focusing (not clicking — isolates the browser's
    // native focus-scroll from any click-driven side effect) each interactive
    // header element while scrolled deep on the page, before the fix landed
    // (the .site-header, .site-header * scroll-margin-top cancellation).
    // =========================================================================
    log('Regression: focusing header controls never scrolls the page (sticky + scroll-padding interaction)');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      for (const sel of ['.brand', '.top-nav li:first-child a']) {
        await page.locator('#praktika').scrollIntoViewIfNeeded();
        await page.waitForTimeout(50);
        const before = await page.evaluate(() => window.scrollY);
        await page.locator(sel).focus();
        await page.waitForTimeout(150);
        const after = await page.evaluate(() => window.scrollY);
        ok(`focusing "${sel}" while deep-scrolled does not move scrollY (before=${before}, after=${after})`, Math.abs(after - before) <= 2);
      }
      await page.close();

      const mobilePage = await browser.newPage({ viewport: { width: 390, height: 844 } });
      await mobilePage.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      await mobilePage.locator('#praktika').scrollIntoViewIfNeeded();
      await mobilePage.waitForTimeout(50);
      const before = await mobilePage.evaluate(() => window.scrollY);
      await mobilePage.locator('.nav-toggle').focus();
      await mobilePage.waitForTimeout(150);
      const after = await mobilePage.evaluate(() => window.scrollY);
      ok(`focusing ".nav-toggle" (mobile) while deep-scrolled does not move scrollY (before=${before}, after=${after})`, Math.abs(after - before) <= 2);
      await mobilePage.close();
    }

    log('Regression: active nav-item highlight still follows scroll after the anchor fix');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      await page.click('.top-nav a:has-text("Справочник")');
      await page.waitForTimeout(400); // IntersectionObserver settles async
      const active = await page.locator('.top-nav a.active').textContent();
      ok('active nav-item highlight follows #spravochnik after precise-anchor navigation', active.trim() === 'Справочник');
      await page.close();
    }

    await browser.close();
  } finally {
    server.kill();
  }

  if (failures > 0) {
    console.error(`\n[nav-test] RESULT: FAIL (${failures} check(s) failed)`);
    process.exitCode = 1;
  } else {
    console.log('\n[nav-test] RESULT: PASS — desktop and mobile navigation both resolve to the correct destinations.');
  }
})().catch((err) => {
  console.error('[nav-test] FATAL:', err);
  process.exit(1);
});
