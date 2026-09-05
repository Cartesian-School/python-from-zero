// Browser contract for the Author Profile redesign: homepage typography
// correction (scripts/build_site_index.py + homepage.css) and the expanded
// front-matter author page (scripts/build_front_matter.py + theory.css),
// sharing one canonical identity source (scripts/author_profile.py).

import { chromium } from 'playwright';
import { execSync, spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import net from 'node:net';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const VIEWPORTS = [[1920, 1080], [1440, 900], [1280, 800], [1024, 900], [768, 1024], [430, 932], [390, 844], [360, 800]];

let failures = 0;
function ok(label, condition) {
  if (condition) console.log(`  [ok] ${label}`);
  else { console.error(`  [FAIL] ${label}`); failures += 1; }
}

async function getFreePort() {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.listen(0, () => { const { port } = server.address(); server.close(() => resolve(port)); });
    server.on('error', reject);
  });
}

async function waitForServer(url, timeoutMs = 15000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try { const response = await fetch(url); if (response.ok) return; } catch (_) {}
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
  throw new Error(`Server at ${url} did not become ready`);
}

function observePage(page, base) {
  const faults = [];
  page.on('console', (message) => { if (message.type() === 'error') faults.push(`console: ${message.text()}`); });
  page.on('pageerror', (error) => faults.push(`pageerror: ${error.message}`));
  page.on('response', (response) => {
    if (response.url().startsWith(base) && response.status() >= 400) faults.push(`${response.status()}: ${response.url()}`);
  });
  return faults;
}

(async () => {
  execSync('bash scripts/build_vercel.sh', { cwd: ROOT, stdio: 'inherit', env: { ...process.env, CHAPTER23_VALIDATION_MODE: 'portable' } });
  const port = await getFreePort();
  const base = `http://localhost:${port}`;
  const server = spawn('python3', [path.join(ROOT, 'scripts', 'dev_server.py'), String(port), path.join(ROOT, 'dist')], { stdio: 'ignore' });

  try {
    await waitForServer(`${base}/index.html`);
    const browser = await chromium.launch();

    // ---- Homepage author profile: typography, portrait, no overflow ----
    for (const [width, height] of VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/index.html#avtor`, { waitUntil: 'networkidle' });
      await page.waitForTimeout(900); // let the one-shot entrance animation settle
      const result = await page.evaluate(() => {
        const name = document.querySelector('.author-profile__name');
        const portraitImg = document.querySelector('.author-portrait img');
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          nameFound: Boolean(name),
          nameText: name ? name.textContent.trim() : '',
          nameFontSize: name ? parseFloat(getComputedStyle(name).fontSize) : -1,
          portraitFound: Boolean(portraitImg) && portraitImg.naturalWidth !== 0,
          roleText: document.querySelector('.author-profile__role')?.textContent.trim() ?? '',
          bodyVisible: (() => {
            const lead = document.querySelector('.author-bio__lead');
            return lead ? getComputedStyle(lead).opacity === '1' && lead.textContent.trim().length > 0 : false;
          })(),
        };
      });
      const viewport = `${width}x${height}`;
      // Hard regression guard: the rejected design rendered the name at 72px
      // on desktop and ~43px on mobile. Never again above these bounds.
      const maxAllowed = width >= 900 ? 56 : 44;
      ok(`homepage ${viewport}: no horizontal overflow`, !result.overflow);
      ok(`homepage ${viewport}: author name renders as "Siergej Sobolewski"`, result.nameFound && result.nameText === 'Siergej Sobolewski');
      ok(`homepage ${viewport}: author name stays within the refined scale (<=${maxAllowed}px, not the rejected poster size)`, result.nameFontSize > 0 && result.nameFontSize <= maxAllowed);
      ok(`homepage ${viewport}: author portrait renders`, result.portraitFound);
      ok(`homepage ${viewport}: role reads "Founder & CEO · Senior Systems & AI Engineer"`, result.roleText === 'Founder & CEO · Senior Systems & AI Engineer');
      ok(`homepage ${viewport}: biography body is visible (not stuck hidden)`, result.bodyVisible);
      ok(`homepage ${viewport}: no console, runtime, or same-origin request errors`, faults.length === 0);
      await page.close();
    }

    // ---- Front-matter author page: substance, structure, consistency ----
    for (const [width, height] of VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/front-matter/ob-avtore.html`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const lede = document.querySelector('.lede');
        const heroName = document.querySelector('.author-page__name');
        const heroRole = document.querySelector('.author-page__role');
        const portraitImg = document.querySelector('.author-page__portrait img');
        const sections = [...document.querySelectorAll('.author-page__section')];
        const sidebarLinks = [...document.querySelectorAll('.sidebar .toc-list a')].map((a) => a.textContent.trim());
        const nextNav = document.querySelector('.section-nav a.next');
        const ids = [...document.querySelectorAll('[id]')].map((n) => n.id);
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          ledeNonEmpty: Boolean(lede) && lede.textContent.trim().length > 40,
          heroNameText: heroName ? heroName.textContent.trim() : '',
          heroRoleText: heroRole ? heroRole.textContent.trim() : '',
          portraitFound: Boolean(portraitImg) && portraitImg.naturalWidth !== 0,
          sectionCount: sections.length,
          sectionHeadings: sections.map((s) => s.querySelector('h2')?.textContent.trim()),
          domainCount: document.querySelectorAll('.author-page__domain').length,
          projectCount: document.querySelectorAll('.author-page__projects li').length,
          sidebarHasCoreLinks: ['Об авторе', 'О техническом рецензенте', 'Введение'].every((label) => sidebarLinks.includes(label)),
          nextNavPresent: Boolean(nextNav) && nextNav.textContent.includes('О техническом рецензенте'),
          noDuplicateIds: ids.length === new Set(ids).size,
        };
      });
      const viewport = `${width}x${height}`;
      ok(`author page ${viewport}: no horizontal overflow`, !result.overflow);
      ok(`author page ${viewport}: lede is non-empty and substantive (was empty before)`, result.ledeNonEmpty);
      ok(`author page ${viewport}: hero states the same canonical name as the homepage`, result.heroNameText === 'Siergej Sobolewski');
      ok(`author page ${viewport}: hero states the same canonical role as the homepage (no contradictory title)`, result.heroRoleText === 'Founder & CEO · Senior Systems & AI Engineer');
      ok(`author page ${viewport}: portrait renders`, result.portraitFound);
      ok(`author page ${viewport}: at least 5 structured sections beyond the two intro paragraphs`, result.sectionCount >= 5);
      ok(`author page ${viewport}: engineering domains grid renders (5 domains)`, result.domainCount === 5);
      ok(`author page ${viewport}: selected projects list renders (6 projects)`, result.projectCount === 6);
      ok(`author page ${viewport}: sidebar keeps all front-matter links`, result.sidebarHasCoreLinks);
      ok(`author page ${viewport}: next-page navigation to "О техническом рецензенте" is preserved`, result.nextNavPresent);
      ok(`author page ${viewport}: no duplicate element ids`, result.noDuplicateIds);
      ok(`author page ${viewport}: no console, runtime, or same-origin request errors`, faults.length === 0);
      await page.close();
    }

    // ---- Reduced motion: both surfaces stay fully readable, nothing frozen mid-transition ----
    const reduced = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await reduced.emulateMedia({ reducedMotion: 'reduce' });
    await reduced.goto(`${base}/index.html#avtor`, { waitUntil: 'networkidle' });
    const homepageReduced = await reduced.evaluate(() => {
      const opacityOf = (sel) => { const n = document.querySelector(sel); return n ? parseFloat(getComputedStyle(n).opacity) : -1; };
      return {
        nameVisible: opacityOf('.author-profile__name') === 1,
        bioVisible: opacityOf('.author-bio__lead') === 1,
        domainsVisible: opacityOf('.author-domain') === 1,
      };
    });
    ok('reduced motion: homepage author name/bio/domains render fully visible (no stuck entrance state)',
      homepageReduced.nameVisible && homepageReduced.bioVisible && homepageReduced.domainsVisible);

    await reduced.goto(`${base}/front-matter/ob-avtore.html`, { waitUntil: 'networkidle' });
    const authorPageReduced = await reduced.evaluate(() => {
      const hero = document.querySelector('.author-page__hero');
      return { heroVisible: hero ? getComputedStyle(hero).opacity === '1' : false };
    });
    ok('reduced motion: author page hero renders fully visible (no stuck entrance state)', authorPageReduced.heroVisible);
    await reduced.close();

    await browser.close();
  } finally {
    server.kill('SIGTERM');
  }

  console.log(`\n[author-profile] RESULT: ${failures === 0 ? 'PASS' : `FAIL (${failures} checks)`}`);
  if (failures) process.exitCode = 1;
})();
