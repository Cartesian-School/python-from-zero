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
const BOOK_PAGINATION = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'book-pagination.json'), 'utf-8'));
const TOTAL_LESSONS = Object.keys(PRACTICE_MANIFEST).length;
const TOTAL_CHAPTERS = COVERAGE_MANIFEST.chapters.filter((chapter) => chapter.kind === 'chapter').length;
const TOTAL_PROJECTS = PROJECTS_MANIFEST.length;
const TOTAL_PAGES = BOOK_PAGINATION.total_pages;

const SAMPLE_LESSONS = ['01-01', '03-01', '05-05', '10-05', '15-01', '17-05', '22-02', '23-03'];
const HERO_VIEWPORTS = [[1920, 1080], [1440, 900], [1280, 800], [1024, 900], [768, 1024], [430, 932], [390, 844], [360, 800]];
const COURSE_EXPERIENCE_VIEWPORTS = HERO_VIEWPORTS;
const AUTHOR_PROFILE_VIEWPORTS = HERO_VIEWPORTS;
const COURSE_STAGE_TITLES = ['Теория на сайте', 'Практика в браузере', 'Классика и современность', 'Настоящие проекты'];

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
    // COURSE EXPERIENCE — overview metrics + connected four-stage pathway
    // =========================================================================
    log('Course experience: asymmetric metrics, connected learning path, responsive containment');
    for (const [width, height] of COURSE_EXPERIENCE_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const consoleErrors = [];
      page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
      page.on('pageerror', (error) => consoleErrors.push(error.message));
      await page.goto(`${base}/index.html#o-kurse`, { waitUntil: 'networkidle' });
      await page.locator('.about-stats').scrollIntoViewIfNeeded();
      await page.waitForTimeout(1000);

      const result = await page.evaluate(() => {
        const rectOf = (element) => {
          const rect = element.getBoundingClientRect();
          return { left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom, width: rect.width, height: rect.height };
        };
        const rectsOf = (selector) => [...document.querySelectorAll(selector)].map(rectOf);
        const noPairOverlaps = (rects) => rects.every((a, index) => rects.slice(index + 1).every((b) =>
          !(a.left < b.right - 1 && a.right > b.left + 1 && a.top < b.bottom - 1 && a.bottom > b.top + 1)
        ));
        const containedHorizontally = (rects) => rects.every((rect) => rect.left >= -1 && rect.right <= window.innerWidth + 1);
        const containedBy = (outer, inner) =>
          inner.left >= outer.left - 1 && inner.right <= outer.right + 1 &&
          inner.top >= outer.top - 1 && inner.bottom <= outer.bottom + 1;
        const metricNodes = [...document.querySelectorAll('.about-stat')];
        const stageNodes = [...document.querySelectorAll('.course-stage')];
        const metricValues = Object.fromEntries(metricNodes.map((node) => [
          node.querySelector('.lbl').textContent.trim(),
          node.querySelector('.num').textContent.trim(),
        ]));
        const metricLayout = metricNodes.map((node) => {
          const card = rectOf(node);
          const codeNode = node.querySelector('.about-stat__code');
          const numberZoneNode = node.querySelector('.about-stat__number-zone');
          const numberNode = node.querySelector('.num');
          const copyNode = node.querySelector('.about-stat__copy');
          const labelNode = node.querySelector('.lbl');
          const detailNode = node.querySelector('.about-stat__detail');
          const code = rectOf(codeNode);
          const numberZone = rectOf(numberZoneNode);
          const number = rectOf(numberNode);
          const copy = rectOf(copyNode);
          const contentRects = [code, number, copy];
          if (detailNode) contentRects.push(rectOf(detailNode));
          return {
            modifier: [...node.classList].find((name) => name.startsWith('about-stat--')),
            cardWidth: card.width,
            codeNumberGap: number.top - code.bottom,
            numberCopyGap: copy.top - number.bottom,
            centerDeltaX: Math.abs((number.left + number.right - numberZone.left - numberZone.right) / 2),
            centerDeltaY: Math.abs((number.top + number.bottom - numberZone.top - numberZone.bottom) / 2),
            contentContained: contentRects.every((rect) => containedBy(card, rect)),
            fontSizes: {
              code: parseFloat(getComputedStyle(codeNode).fontSize),
              number: parseFloat(getComputedStyle(numberNode).fontSize),
              label: parseFloat(getComputedStyle(labelNode).fontSize),
              detail: detailNode ? parseFloat(getComputedStyle(detailNode).fontSize) : null,
            },
            stable: node.classList.contains('is-metric-revealed') && getComputedStyle(node).transform === 'none',
          };
        });
        const metricWidths = Object.fromEntries(metricLayout.map((metric) => [metric.modifier, metric.cardWidth]));
        const metricFontSizes = Object.fromEntries(metricLayout.map((metric) => [metric.modifier, metric.fontSizes.number]));
        const desktopRail = getComputedStyle(document.querySelector('.course-path__rail--desktop')).display;
        const mobileRail = getComputedStyle(document.querySelector('.course-path__rail--mobile')).display;
        const routes = document.querySelector('.about-stats__routes');
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          metricCount: metricNodes.length,
          metricValues,
          metricLayout,
          metricWidths,
          metricFontSizes,
          metricsContained: containedHorizontally(rectsOf('.about-stat')),
          metricsDoNotOverlap: noPairOverlaps(rectsOf('.about-stat')),
          metricRoutesValid: !!routes && routes.viewBox.baseVal.width === 600 && routes.viewBox.baseVal.height === 430,
          stageCount: stageNodes.length,
          stageTitles: stageNodes.map((node) => node.querySelector('h3').textContent.trim()),
          stagesContained: containedHorizontally(rectsOf('.course-stage__content')),
          stagesDoNotOverlap: noPairOverlaps(rectsOf('.course-stage__content')),
          coherentIconCount: document.querySelectorAll('.course-stage__icon svg[viewBox="0 0 64 64"]').length,
          oldFeatureGridCount: document.querySelectorAll('.feature-grid, .feature').length,
          desktopRailVisible: desktopRail !== 'none',
          mobileRailVisible: mobileRail !== 'none',
          routeBasePresent: !!document.querySelector('.course-path__base'),
        };
      });

      await page.locator('.course-path').scrollIntoViewIfNeeded();
      await page.waitForTimeout(750);
      const pathwayRevealed = await page.locator('.course-path').evaluate((node) =>
        getComputedStyle(node).opacity === '1' && node.getBoundingClientRect().height > 0
      );

      const viewport = `${width}x${height}`;
      ok(`${viewport}: course experience has no horizontal overflow`, !result.overflow);
      ok(`${viewport}: four source-derived metric nodes are present`, result.metricCount === 4);
      ok(`${viewport}: metric values match chapter, practice, project, and pagination sources`,
        result.metricValues['Главы'] === String(TOTAL_CHAPTERS) &&
        result.metricValues['Практических заданий'] === String(TOTAL_LESSONS) &&
        result.metricValues['Готовых проектов'] === String(TOTAL_PROJECTS) &&
        result.metricValues['Страниц в книге'] === String(TOTAL_PAGES));
      ok(`${viewport}: metrics are contained and do not collide`, result.metricsContained && result.metricsDoNotOverlap);
      ok(`${viewport}: metric micro-label, centered number, and lower-copy zones are separated`,
        result.metricLayout.every((metric) => metric.codeNumberGap >= 8 && metric.numberCopyGap >= 8 &&
          metric.centerDeltaX <= 1 && metric.centerDeltaY <= 1));
      ok(`${viewport}: all metric content remains inside its card`, result.metricLayout.every((metric) => metric.contentContained));
      ok(`${viewport}: metric typography resolves to the refined 10/14/11px hierarchy`,
        result.metricLayout.every((metric) => metric.fontSizes.code === 10 && metric.fontSizes.label === 14 &&
          (metric.fontSizes.detail === null || metric.fontSizes.detail === 11)));
      ok(`${viewport}: metric entrance completes in a stable final position`, result.metricLayout.every((metric) => metric.stable));
      ok(`${viewport}: metric route SVG preserves its valid viewBox`, result.metricRoutesValid);
      if (width <= 700) {
        ok(`${viewport}: mobile constellation keeps chapter/practice cards wide while page/project cards remain compact`,
          Math.abs(result.metricWidths['about-stat--chapters'] - result.metricWidths['about-stat--practice']) <= 1 &&
          result.metricWidths['about-stat--practice'] > result.metricWidths['about-stat--pages'] * 1.8 &&
          Math.abs(result.metricWidths['about-stat--pages'] - result.metricWidths['about-stat--projects']) <= 1);
        ok(`${viewport}: mobile number hierarchy remains differentiated`,
          result.metricFontSizes['about-stat--chapters'] === 48 &&
          result.metricFontSizes['about-stat--practice'] === 44 &&
          result.metricFontSizes['about-stat--pages'] === 36 &&
          result.metricFontSizes['about-stat--projects'] === 36);
      }
      ok(`${viewport}: four learning stages preserve their ordered concepts`,
        result.stageCount === 4 && JSON.stringify(result.stageTitles) === JSON.stringify(COURSE_STAGE_TITLES));
      ok(`${viewport}: stages are contained and do not collide`, result.stagesContained && result.stagesDoNotOverlap);
      ok(`${viewport}: all four stages use the coherent local SVG family`, result.coherentIconCount === 4);
      ok(`${viewport}: generic feature-card grid is absent`, result.oldFeatureGridCount === 0);
      ok(`${viewport}: the pathway has the correct responsive orientation`,
        width > 900 ? result.desktopRailVisible && !result.mobileRailVisible : !result.desktopRailVisible && result.mobileRailVisible);
      ok(`${viewport}: route and staged entrance render completely`, result.routeBasePresent && pathwayRevealed);
      ok(`${viewport}: course experience produced no console errors`, consoleErrors.length === 0);
      await page.close();
    }

    log('Course experience: metric cards enter in order and release transform ownership');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      await page.evaluate(() => {
        window.__metricMotionEvents = [];
        document.querySelectorAll('.about-stat').forEach((card) => {
          card.addEventListener('animationstart', (event) => {
            if (event.animationName !== 'course-metric-enter' && event.animationName !== 'course-metric-number-settle') return;
            window.__metricMotionEvents.push({
              animation: event.animationName,
              metric: card.querySelector('.num').textContent.trim(),
              target: event.target.classList.contains('num') ? 'number' : 'card',
              time: performance.now(),
            });
          });
        });
      });
      await page.locator('.about-stats').scrollIntoViewIfNeeded();
      await page.waitForSelector('.about-stat--chapters.is-metric-entering');
      const motionConfig = await page.locator('.about-stat').evaluateAll((cards) => cards.map((card) => ({
        delay: getComputedStyle(card).animationDelay,
        duration: getComputedStyle(card).animationDuration,
      })));
      await page.waitForTimeout(1150);
      const motion = await page.evaluate(() => {
        const cards = [...document.querySelectorAll('.about-stat')];
        const cardStarts = window.__metricMotionEvents.filter((event) => event.animation === 'course-metric-enter' && event.target === 'card');
        const numberStarts = window.__metricMotionEvents.filter((event) => event.animation === 'course-metric-number-settle' && event.target === 'number');
        return {
          cardStarts,
          numberStarts,
          cardsStable: cards.every((card) => card.classList.contains('is-metric-revealed') && getComputedStyle(card).animationName === 'none' && getComputedStyle(card).transform === 'none'),
          glowAnimations: cards.map((card) => getComputedStyle(card, '::before').animationName),
        };
      });
      const expectedMetricOrder = [TOTAL_CHAPTERS, TOTAL_PAGES, TOTAL_PROJECTS, TOTAL_LESSONS].map(String);
      ok('metric entrance order follows chapter, pagination, project, and practice sources',
        JSON.stringify(motion.cardStarts.map((event) => event.metric)) === JSON.stringify(expectedMetricOrder));
      ok('metric entrance uses the configured 620ms duration and exact 80ms stagger',
        JSON.stringify(motionConfig.map((config) => config.delay)) === JSON.stringify(['0s', '0.08s', '0.16s', '0.24s']) &&
        motionConfig.every((config) => config.duration === '0.62s'));
      ok('each metric number runs exactly one settle animation',
        motion.numberStarts.length === 4 && new Set(motion.numberStarts.map((event) => event.metric)).size === 4);
      ok('cards release entrance transforms while ambient motion remains on the glow only',
        motion.cardsStable && motion.glowAnimations.every((name) => name === 'course-metric-glow-drift'));
      await page.close();
    }

    log('Course experience: metric hover is restrained and returns to a stable position');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html#o-kurse`, { waitUntil: 'networkidle' });
      await page.waitForTimeout(1000);
      const card = page.locator('.about-stat--chapters');
      const before = await card.evaluate((node) => ({
        top: node.getBoundingClientRect().top,
        border: getComputedStyle(node).borderColor,
        label: getComputedStyle(node.querySelector('.lbl')).color,
        numberFilter: getComputedStyle(node.querySelector('.num')).filter,
      }));
      await card.hover();
      await page.waitForTimeout(300);
      const hovered = await card.evaluate((node) => ({
        top: node.getBoundingClientRect().top,
        border: getComputedStyle(node).borderColor,
        label: getComputedStyle(node.querySelector('.lbl')).color,
        numberFilter: getComputedStyle(node.querySelector('.num')).filter,
      }));
      await page.mouse.move(0, 0);
      await page.waitForTimeout(300);
      const restoredTop = await card.evaluate((node) => node.getBoundingClientRect().top);
      const lift = before.top - hovered.top;
      ok('metric hover lift is visible and no greater than 2px', lift >= 1 && lift <= 2.1);
      ok('metric hover refines border, label, and number emphasis',
        before.border !== hovered.border && before.label !== hovered.label && before.numberFilter !== hovered.numberFilter);
      ok('metric card returns to its stable zero-offset position after hover', Math.abs(before.top - restoredTop) <= 0.2);
      await page.close();
    }

    log('Course experience: stage hover activates its route segment');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html#o-kurse`, { waitUntil: 'networkidle' });
      const segment = page.locator('.course-path__segment--2');
      const before = await segment.evaluate((node) => getComputedStyle(node).stroke);
      await page.locator('.course-stage--practice').hover();
      await page.waitForTimeout(220);
      const after = await segment.evaluate((node) => getComputedStyle(node).stroke);
      ok('practice hover brightens the corresponding route segment', before !== after);
      await page.close();
    }

    log('Course experience: prefers-reduced-motion disables continuous and entrance motion');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
      await page.goto(`${base}/index.html#o-kurse`, { waitUntil: 'networkidle' });
      const reduced = await page.evaluate(() => {
        const selectors = ['.about-stat', '.about-stats__signal', '.course-path__signal', '.course-stage__node i', '.stage-icon__cursor'];
        const cards = [...document.querySelectorAll('.about-stat')];
        return {
          animations: selectors.map((selector) => getComputedStyle(document.querySelector(selector)).animationName),
          glowAnimations: cards.map((card) => getComputedStyle(card, '::before').animationName),
          metricStatic: cards.every((card) => {
            const cardStyle = getComputedStyle(card);
            const numberStyle = getComputedStyle(card.querySelector('.num'));
            return cardStyle.opacity === '1' && cardStyle.transform === 'none' && cardStyle.transitionDuration === '0s' &&
              numberStyle.animationName === 'none' && numberStyle.transform === 'none' && numberStyle.transitionDuration === '0s';
          }),
          revealsVisible: [...document.querySelectorAll('.experience-reveal')].every((node) => getComputedStyle(node).opacity === '1'),
          stageCount: document.querySelectorAll('.course-stage').length,
        };
      });
      ok('reduced motion: continuous metric, route, node, and icon animations are disabled', reduced.animations.every((name) => name === 'none'));
      ok('reduced motion: metric cards, numbers, and glows are immediately static',
        reduced.metricStatic && reduced.glowAnimations.every((name) => name === 'none'));
      ok('reduced motion: all content remains visible and complete', reduced.revealsVisible && reduced.stageCount === 4);
      await page.close();
    }

    // =========================================================================
    // SIGNATURE AUTHOR PROFILE — real portrait + Cartesian systems drawing
    // =========================================================================
    log('Author profile: real local portrait, editorial hierarchy, domains, and responsive containment');
    for (const [width, height] of AUTHOR_PROFILE_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const consoleErrors = [];
      page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
      page.on('pageerror', (error) => consoleErrors.push(error.message));
      await page.goto(`${base}/index.html#avtor`, { waitUntil: 'networkidle' });
      await page.locator('.author-profile__name').scrollIntoViewIfNeeded();
      await page.waitForTimeout(1500);

      const result = await page.evaluate(() => {
        const rectOf = (element) => {
          const rect = element.getBoundingClientRect();
          return { left: rect.left, top: rect.top, right: rect.right, bottom: rect.bottom, width: rect.width, height: rect.height };
        };
        const overlaps = (a, b) => a.left < b.right - 1 && a.right > b.left + 1 && a.top < b.bottom - 1 && a.bottom > b.top + 1;
        const section = document.querySelector('.author-profile');
        const intro = rectOf(document.querySelector('.author-profile__intro'));
        const portrait = rectOf(document.querySelector('.author-portrait'));
        const portraitImage = document.querySelector('.author-portrait img');
        const portraitImageRect = rectOf(portraitImage);
        const body = rectOf(document.querySelector('.author-profile__body'));
        const name = document.querySelector('.author-profile__name');
        const nameRange = document.createRange();
        nameRange.selectNodeContents(name);
        const domainRects = [...document.querySelectorAll('.author-domain')].map(rectOf);
        const affiliationRects = [...document.querySelectorAll('.author-affiliation')].map(rectOf);
        const bio = document.querySelector('.author-bio');
        const glaeron = document.querySelector('.author-affiliation a');
        const sectionText = section.textContent;
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          sectionOverflow: section.scrollWidth > section.clientWidth + 1,
          name: name.textContent.trim(),
          nameLineCount: nameRange.getClientRects().length,
          role: document.querySelector('.author-profile__role').textContent.trim(),
          specializations: [...document.querySelectorAll('.author-profile__specialization span')].map((node) => node.textContent.trim()),
          introPortraitOverlap: overlaps(intro, portrait),
          bodyPortraitOverlap: overlaps(body, portrait),
          mobileOrder: intro.bottom <= portrait.top + 1 && portrait.bottom <= body.top + 1,
          portraitLoaded: portraitImage.complete && portraitImage.naturalWidth === 456 && portraitImage.naturalHeight === 570,
          portraitSrc: portraitImage.getAttribute('src'),
          portraitCurrentSrc: portraitImage.currentSrc,
          webpSrc: document.querySelector('.author-portrait source[type="image/webp"]').getAttribute('srcset'),
          portraitRatio: portraitImageRect.width / portraitImageRect.height,
          portraitHeight: portraitImageRect.height,
          bioWidth: bio.getBoundingClientRect().width,
          bioFontSize: parseFloat(getComputedStyle(bio.querySelector('p')).fontSize),
          do178cPresent: sectionText.includes('DO-178C'),
          bioProductsPresent: ['GuardBSD', 'AstraDesk', 'AeroNerve', 'PySH', 'ECLI'].every((product) => sectionText.includes(product)),
          domainCount: domainRects.length,
          domainsUseTwoColumns: Math.abs(domainRects[0].top - domainRects[1].top) <= 1 && Math.abs(domainRects[0].left - domainRects[1].left) > 20,
          domainsUseOneColumn: domainRects.every((rect) => Math.abs(rect.left - domainRects[0].left) <= 1),
          affiliationsUseTwoColumns: Math.abs(affiliationRects[0].top - affiliationRects[1].top) <= 1 && Math.abs(affiliationRects[0].left - affiliationRects[1].left) > 20,
          affiliationsUseOneColumn: affiliationRects[1].top > affiliationRects[0].bottom,
          glaeronHref: glaeron.href,
          glaeronTarget: glaeron.target,
          glaeronRel: glaeron.rel,
          metadataCount: document.querySelectorAll('.author-metadata > div').length,
          framePathCount: document.querySelectorAll('.author-portrait__frame path').length,
          fakeFaceOverlayCount: document.querySelectorAll('.author-portrait picture svg, .author-portrait picture canvas').length,
          revealed: section.classList.contains('is-profile-revealed') && [...section.querySelectorAll('.author-reveal')].every((node) => getComputedStyle(node).opacity === '1'),
        };
      });

      const viewport = `${width}x${height}`;
      ok(`${viewport}: author section has no document or local horizontal overflow`, !result.overflow && !result.sectionOverflow);
      ok(`${viewport}: author identity, role, and four specializations are explicit`,
        result.name === 'Siergej Sobolewski' &&
        result.role === 'Founder & CEO · Senior Systems & AI Engineer' &&
        JSON.stringify(result.specializations) === JSON.stringify(['AI/ML', 'Embedded Systems', 'Radar & Avionics', 'High-Assurance Engineering']));
      ok(`${viewport}: author name remains a readable one- or two-line anchor`, result.nameLineCount >= 1 && result.nameLineCount <= 2);
      ok(`${viewport}: optimized local WebP/JPEG portrait sources load at the canonical 4:5 dimensions`,
        result.portraitLoaded && result.portraitSrc === '/assets/img/author/siergej-sobolewski.jpg' &&
        result.webpSrc === '/assets/img/author/siergej-sobolewski.webp' && result.portraitCurrentSrc.endsWith('/assets/img/author/siergej-sobolewski.webp') &&
        Math.abs(result.portraitRatio - 0.8) <= 0.005);
      ok(`${viewport}: portrait remains substantial without consuming the viewport`, result.portraitHeight >= 270 && result.portraitHeight <= height * 0.7);
      ok(`${viewport}: biography measure and reading size remain controlled`, result.bioWidth <= 760.5 && result.bioFontSize >= 13.5);
      ok(`${viewport}: visible safety-critical biography explicitly represents DO-178C`, result.do178cPresent);
      ok(`${viewport}: GuardBSD, AstraDesk, AeroNerve, PySH, and ECLI are represented`, result.bioProductsPresent);
      ok(`${viewport}: five engineering domains use the correct responsive architecture`,
        result.domainCount === 5 && (width <= 600 ? result.domainsUseOneColumn : result.domainsUseTwoColumns));
      ok(`${viewport}: affiliations use the correct responsive architecture`, width <= 600 ? result.affiliationsUseOneColumn : result.affiliationsUseTwoColumns);
      ok(`${viewport}: Glaeron CTA is external and opener-safe`,
        result.glaeronHref === 'https://www.glaeron.com/' && result.glaeronTarget === '_blank' &&
        result.glaeronRel.includes('noopener') && result.glaeronRel.includes('noreferrer'));
      ok(`${viewport}: technical frame and four-field metadata rail are complete without a face overlay`,
        result.framePathCount === 5 && result.metadataCount === 4 && result.fakeFaceOverlayCount === 0);
      ok(`${viewport}: staged entrance completes with all content visible`, result.revealed);
      ok(`${viewport}: author section produced no console errors`, consoleErrors.length === 0);
      if (width > 900) ok(`${viewport}: editorial columns do not collide`, !result.introPortraitOverlap && !result.bodyPortraitOverlap);
      if (width <= 900) ok(`${viewport}: mobile/tablet reading order is intro, portrait, biography`, result.mobileOrder);
      await page.close();
    }

    log('Author profile: entrance timing is staged once and releases portrait/text transforms');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
      await page.locator('.author-profile').evaluate((section) => {
        window.__authorMotionEvents = [];
        section.addEventListener('animationstart', (event) => {
          if (!event.animationName.startsWith('author-')) return;
          window.__authorMotionEvents.push({
            animation: event.animationName,
            target: event.target.className.baseVal || event.target.className || event.target.tagName,
            time: performance.now(),
          });
        });
      });
      await page.locator('.author-profile__name').scrollIntoViewIfNeeded();
      await page.waitForSelector('.author-profile.is-profile-entering');
      const entering = await page.evaluate(() => {
        const config = (selector) => {
          const style = getComputedStyle(document.querySelector(selector));
          return { delay: style.animationDelay, duration: style.animationDuration, name: style.animationName, iterations: style.animationIterationCount };
        };
        return {
          eyebrow: config('.author-profile__eyebrow'),
          name: config('.author-profile__name'),
          role: config('.author-profile__role'),
          portrait: config('.author-portrait'),
          firstDomain: config('.author-domain:nth-child(1)'),
          lastDomain: config('.author-domain:nth-child(5)'),
          metadata: config('.author-metadata'),
          frame: config('.author-portrait__outline'),
          signal: config('.author-portrait__signal'),
        };
      });
      ok('author entrance uses the specified 100/180/260/320ms opening sequence',
        entering.eyebrow.delay === '0.1s' && entering.name.delay === '0.18s' &&
        entering.role.delay === '0.26s' && entering.portrait.delay === '0.32s');
      ok('engineering domains stagger from 650ms to 970ms and metadata starts at 900ms',
        entering.firstDomain.delay === '0.65s' && entering.lastDomain.delay === '0.97s' && entering.metadata.delay === '0.9s');
      ok('portrait frame draws once and the technical signal traverses once',
        entering.frame.name === 'author-frame-draw' && entering.frame.delay === '0.42s' && entering.frame.duration === '0.8s' &&
        entering.signal.name === 'author-frame-signal' && entering.signal.iterations === '1');
      await page.waitForTimeout(1500);
      const settled = await page.evaluate(() => {
        const section = document.querySelector('.author-profile');
        const portrait = document.querySelector('.author-portrait');
        const image = portrait.querySelector('img');
        return {
          revealed: section.classList.contains('is-profile-revealed') && !section.classList.contains('is-profile-entering'),
          allEntranceAnimationsReleased: [...section.querySelectorAll('.author-reveal')].every((node) => getComputedStyle(node).animationName === 'none' && getComputedStyle(node).transform === 'none'),
          portraitStable: getComputedStyle(portrait).animationName === 'none' && getComputedStyle(portrait).transform === 'none' && getComputedStyle(image).animationName === 'none',
          ambientGlow: getComputedStyle(section, '::after').animationName,
          ambientNodes: [...section.querySelectorAll('.author-profile__ambient-node')].map((node) => getComputedStyle(node).animationName),
          eventNames: window.__authorMotionEvents.map((event) => event.animation),
        };
      });
      ok('one-shot entrance reaches its stable released state', settled.revealed && settled.allEntranceAnimationsReleased);
      ok('portrait and text remain stationary after entrance', settled.portraitStable);
      ok('post-entrance ambient motion is restricted to the glow and sparse nodes',
        settled.ambientGlow === 'author-ambient-glow' && settled.ambientNodes.every((name) => name === 'author-node-breathe'));
      ok('frame draw and signal animations each start exactly once',
        settled.eventNames.filter((name) => name === 'author-frame-draw').length === 3 &&
        settled.eventNames.filter((name) => name === 'author-frame-signal').length === 1);
      await page.close();
    }

    log('Author profile: fine-pointer hover is restrained and does not translate the portrait');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      await page.goto(`${base}/index.html#avtor`, { waitUntil: 'networkidle' });
      await page.waitForTimeout(1500);
      const portrait = page.locator('.author-portrait');
      const before = await portrait.evaluate((node) => ({
        top: node.getBoundingClientRect().top,
        left: node.getBoundingClientRect().left,
        stroke: getComputedStyle(node.querySelector('.author-portrait__corners')).stroke,
      }));
      await portrait.hover();
      await page.waitForTimeout(450);
      const hovered = await portrait.evaluate((node) => {
        const matrix = new DOMMatrixReadOnly(getComputedStyle(node.querySelector('img')).transform);
        return {
          top: node.getBoundingClientRect().top,
          left: node.getBoundingClientRect().left,
          scale: matrix.a,
          stroke: getComputedStyle(node.querySelector('.author-portrait__corners')).stroke,
        };
      });
      const domain = page.locator('.author-domain').first();
      const lineBefore = await domain.evaluate((node) => parseFloat(getComputedStyle(node, '::after').width));
      await domain.hover();
      await page.waitForTimeout(320);
      const lineAfter = await domain.evaluate((node) => parseFloat(getComputedStyle(node, '::after').width));
      const glaeron = page.locator('.author-affiliation a');
      const ctaBefore = await glaeron.evaluate((node) => getComputedStyle(node).color);
      await glaeron.hover();
      await page.waitForTimeout(240);
      const ctaAfter = await glaeron.evaluate((node) => getComputedStyle(node).color);
      ok('portrait hover scale is visible and capped at 1.01', hovered.scale > 1 && hovered.scale <= 1.01);
      ok('portrait frame strengthens without translating the portrait',
        before.stroke !== hovered.stroke && Math.abs(before.top - hovered.top) <= 0.2 && Math.abs(before.left - hovered.left) <= 0.2);
      ok('domain line extends and Glaeron CTA gains a clear hover state', lineAfter > lineBefore && ctaBefore !== ctaAfter);
      await page.close();
    }

    log('Author profile: prefers-reduced-motion renders the complete static system immediately');
    {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
      await page.goto(`${base}/index.html#avtor`, { waitUntil: 'networkidle' });
      const reduced = await page.evaluate(() => {
        const section = document.querySelector('.author-profile');
        const animationSelectors = ['.author-profile__name', '.author-portrait', '.author-portrait__outline', '.author-portrait__signal', '.author-profile__ambient-node'];
        return {
          revealed: section.classList.contains('is-profile-revealed'),
          animations: animationSelectors.map((selector) => getComputedStyle(document.querySelector(selector)).animationName),
          contentVisible: [...section.querySelectorAll('.author-reveal')].every((node) => getComputedStyle(node).opacity === '1' && getComputedStyle(node).transform === 'none'),
          frameComplete: ['.author-portrait__outline', '.author-portrait__corners', '.author-portrait__route'].every((selector) => parseFloat(getComputedStyle(document.querySelector(selector)).strokeDashoffset) === 0),
          portraitStatic: getComputedStyle(document.querySelector('.author-portrait img')).transform === 'none',
          domainCount: section.querySelectorAll('.author-domain').length,
          metadataCount: section.querySelectorAll('.author-metadata > div').length,
        };
      });
      ok('reduced motion: entrance, frame, signal, glow, and node animations are disabled', reduced.animations.every((name) => name === 'none'));
      ok('reduced motion: profile is immediately visible with a complete static frame', reduced.revealed && reduced.contentVisible && reduced.frameComplete && reduced.portraitStatic);
      ok('reduced motion: all domains and metadata remain complete', reduced.domainCount === 5 && reduced.metadataCount === 4);
      await page.close();
    }

    if (process.env.EXPERIENCE_ONLY === '1') {
      await browser.close();
      console.log(`\n[homepage] EXPERIENCE RESULT: ${failures === 0 ? 'PASS' : `FAIL (${failures} check(s) failed)`}`);
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
      const groupChapters = await page.locator('.practice-chapter-group').evaluateAll((groups) => groups.map((group) => Number(group.dataset.chapter)));
      const expectedChapters = COVERAGE_MANIFEST.chapters.filter((chapter) => chapter.kind === 'chapter').map((chapter) => chapter.number);
      ok(`Practice catalog keeps one group for all ${TOTAL_CHAPTERS} chapters, including theory-only chapters`,
        groupCount === TOTAL_CHAPTERS && JSON.stringify(groupChapters) === JSON.stringify(expectedChapters));

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
