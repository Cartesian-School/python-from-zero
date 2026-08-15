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
