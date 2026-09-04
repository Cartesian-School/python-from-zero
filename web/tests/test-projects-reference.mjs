// Browser contract for the manifest-driven project and reference redesign.

import { chromium } from 'playwright';
import { execSync, spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';
import net from 'node:net';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const VIEWPORTS = [[1920, 1080], [1440, 900], [1280, 800], [1024, 900], [768, 1024], [430, 932], [390, 844], [360, 800]];
const TIC_TAC_TOE_VIEWPORTS = [[1440, 900], [768, 1024], [390, 844]];
const REPRESENTATIVE_PROJECTS = ['paint-app', 'space-shooter', 'todo-app', 'safesort'];
const PROJECTS = JSON.parse(fs.readFileSync(path.join(ROOT, 'manifest', 'projects_manifest.json'), 'utf8')).projects;

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
  execSync('bash scripts/build_vercel.sh', { cwd: ROOT, stdio: 'inherit' });
  const port = await getFreePort();
  const base = `http://localhost:${port}`;
  const server = spawn('python3', [path.join(ROOT, 'scripts', 'dev_server.py'), String(port), path.join(ROOT, 'dist')], { stdio: 'ignore' });

  try {
    await waitForServer(`${base}/index.html`);
    const browser = await chromium.launch();

    for (const [width, height] of VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/index.html#proekty`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const cards = [...document.querySelectorAll('.project-card')];
        const uniqueColumns = new Set(cards.slice(0, 6).map((card) => Math.round(card.getBoundingClientRect().left)));
        const referenceCopy = document.querySelector('.reference-hero__copy').getBoundingClientRect();
        const referenceArt = document.querySelector('.reference-hero__art').getBoundingClientRect();
        const focusWidth = (selector) => {
          const node = document.querySelector(selector);
          node.focus();
          return parseFloat(getComputedStyle(node).outlineWidth);
        };
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          projectCount: cards.length,
          columns: uniqueColumns.size,
          referenceCount: document.querySelectorAll('.reference-card').length,
          referenceArt: Boolean(document.querySelector('.reference-hero__art svg[aria-hidden="true"]')),
          referenceMicrocopy: document.querySelector('.reference-art').textContent,
          referenceTextFirst: referenceCopy.top <= referenceArt.top,
          contentContained: [...document.querySelectorAll('.project-card-title, .project-card-topics, .reference-card')].every((node) => {
            const rect = node.getBoundingClientRect();
            return rect.left >= -1 && rect.right <= window.innerWidth + 1;
          }),
          focusWidths: ['.project-card', '.reference-card', window.innerWidth <= 700 ? '.nav-toggle' : '.top-nav a'].map(focusWidth),
        };
      });
      const expectedColumns = width <= 600 ? 1 : width <= 860 ? 2 : 3;
      const viewport = `${width}x${height}`;
      ok(`${viewport}: homepage has no horizontal overflow`, !result.overflow);
      ok(`${viewport}: 13 project cards render`, result.projectCount === 13);
      ok(`${viewport}: project grid uses ${expectedColumns} column(s)`, result.columns === expectedColumns);
      ok(`${viewport}: reference hero and eight real destinations render`, result.referenceArt && result.referenceCount === 8);
      ok(`${viewport}: reference illustration microcopy is Russian`, result.referenceMicrocopy.includes('УКАЗАТЕЛЬ / КАРТА ЗНАНИЙ') && !/INDEX|KNOWLEDGE|reference/i.test(result.referenceMicrocopy));
      if (width <= 900) ok(`${viewport}: reference text precedes art`, result.referenceTextFirst);
      ok(`${viewport}: titles, tags, and reference cards are contained`, result.contentContained);
      ok(`${viewport}: card, reference, and navigation focus is visible`, result.focusWidths.every((value) => value >= 2));
      ok(`${viewport}: no console, runtime, or same-origin request errors`, faults.length === 0);
      await page.close();
    }

    for (const project of PROJECTS) {
      const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
      const faults = observePage(page, base);
      const response = await page.goto(`${base}/projects/${project.slug}/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(({ id, sourcePath }) => ({
        overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        h1Count: document.querySelectorAll('h1').length,
        artFound: Boolean(document.querySelector(`.project-art--${id}[aria-hidden="true"]`)),
        sourceFound: Boolean(document.querySelector(`a[href="/${sourcePath}"]`)),
        visualHeight: document.querySelector('.project-detail-hero__visual').getBoundingClientRect().height,
        linksPresent: Boolean(document.querySelector('.project-detail-back a')) && Boolean(document.querySelector('.project-related-card')),
        focusWidths: ['.project-detail-actions a', '.project-source-link', '.project-related-card', '.project-detail-back a', '.top-nav a'].map((selector) => {
          const node = document.querySelector(selector);
          node.focus();
          return parseFloat(getComputedStyle(node).outlineWidth);
        }),
      }), { id: project.id, sourcePath: project.source_path });
      const relatedUrls = [
        `/${project.source_path}`,
        `/chapters/glava-${String(project.chapter).padStart(2, '0')}/index.html`,
        `/practice/${project.lesson_id}/index.html`,
        '/index.html#proekty',
      ];
      const relatedStatuses = await Promise.all(relatedUrls.map(async (url) => (await page.request.get(`${base}${url}`)).status()));
      ok(`${project.slug}: route and shared template are valid`, response.ok() && result.h1Count === 1 && result.artFound);
      ok(`${project.slug}: canonical source link is present`, result.sourceFound);
      ok(`${project.slug}: source, chapter, practice, and back routes resolve`, result.linksPresent && relatedStatuses.every((status) => status >= 200 && status < 400));
      ok(`${project.slug}: desktop hero visual is compact`, result.visualHeight <= 440);
      ok(`${project.slug}: detail actions and resources have visible focus`, result.focusWidths.every((value) => value >= 2));
      ok(`${project.slug}: no overflow or browser faults`, !result.overflow && faults.length === 0);
      await page.close();
    }

    for (const [width, height] of VIEWPORTS) {
      for (const slug of REPRESENTATIVE_PROJECTS) {
        const page = await browser.newPage({ viewport: { width, height } });
        const faults = observePage(page, base);
        await page.goto(`${base}/projects/${slug}/`, { waitUntil: 'networkidle' });
        const result = await page.evaluate(() => {
          const title = document.querySelector('h1').getBoundingClientRect();
          const art = document.querySelector('.project-detail-hero__visual').getBoundingClientRect();
          const contained = (node) => {
            const rect = node.getBoundingClientRect();
            return rect.left >= -1 && rect.right <= window.innerWidth + 1;
          };
          return {
            textFirst: title.top < art.top,
            overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
            visualHeight: art.height,
            titleContained: contained(document.querySelector('h1')),
            tagsContained: [...document.querySelectorAll('.project-meta-row .project-topic')].every(contained),
            ctaContained: [...document.querySelectorAll('.project-detail-actions .btn')].every(contained),
            resourcesContained: [...document.querySelectorAll('.project-source-link, .project-related-card')].every(contained),
          };
        });
        const viewport = `${width}x${height}`;
        if (width <= 780) ok(`${slug} ${viewport}: title precedes compact art`, result.textFirst);
        else ok(`${slug} ${viewport}: desktop hero visual stays below 440px`, result.visualHeight <= 440);
        ok(`${slug} ${viewport}: title, tags, CTAs, and resources are contained`, result.titleContained && result.tagsContained && result.ctaContained && result.resourcesContained);
        ok(`${slug} ${viewport}: no overflow or browser faults`, !result.overflow && faults.length === 0);
        await page.close();
      }
    }

    for (const [width, height] of TIC_TAC_TOE_VIEWPORTS) {
      for (const [surface, url, containerSelector] of [
        ['homepage card', '/index.html#proekty', '.project-card[data-project="tic-tac-toe"]'],
        ['detail hero', '/projects/tic-tac-toe/', '.project-detail-hero__visual'],
      ]) {
        const page = await browser.newPage({ viewport: { width, height } });
        const faults = observePage(page, base);
        await page.goto(`${base}${url}`, { waitUntil: 'networkidle' });
        const result = await page.evaluate((containerSelector) => {
          const container = document.querySelector(containerSelector);
          const svg = container.querySelector('.project-art--tic-tac-toe');
          const board = svg.querySelector('.tic-tac-toe__board');
          const xMark = svg.querySelector('.tic-tac-toe__x');
          const oMark = svg.querySelector('.tic-tac-toe__o');
          const route = svg.querySelector('.project-art__route');
          const box = (node) => {
            const value = node.getBBox();
            return { x: value.x, y: value.y, width: value.width, height: value.height };
          };
          const contained = (node) => {
            const outer = container.getBoundingClientRect();
            const inner = node.getBoundingClientRect();
            return inner.left >= outer.left - 1 && inner.right <= outer.right + 1
              && inner.top >= outer.top - 1 && inner.bottom <= outer.bottom + 1;
          };
          const strokeAwareBox = (node, clearance) => {
            const value = box(node);
            const inset = parseFloat(getComputedStyle(node).strokeWidth) / 2 + clearance;
            return {
              left: value.x - inset,
              right: value.x + value.width + inset,
              top: value.y - inset,
              bottom: value.y + value.height + inset,
            };
          };
          const protectedMarks = [strokeAwareBox(xMark, 4), strokeAwareBox(oMark, 4)];
          const routeLength = route.getTotalLength();
          const routeClear = Array.from({ length: 201 }, (_, index) => route.getPointAtLength(routeLength * index / 200))
            .every((point) => protectedMarks.every((mark) => point.x < mark.left || point.x > mark.right
              || point.y < mark.top || point.y > mark.bottom));
          return {
            board: box(board),
            xMark: box(xMark),
            oMark: box(oMark),
            boardStroke: parseFloat(getComputedStyle(board).strokeWidth),
            xStroke: parseFloat(getComputedStyle(xMark).strokeWidth),
            oStroke: parseFloat(getComputedStyle(oMark).strokeWidth),
            routeClear,
            contained: [board, xMark, oMark].every(contained),
            overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          };
        }, containerSelector);
        const near = (actual, expected) => Math.abs(actual - expected) < 0.01;
        const centeredAt = (box, x, y) => near(box.x + box.width / 2, x) && near(box.y + box.height / 2, y);
        const viewport = `${width}x${height}`;
        ok(`${surface} ${viewport}: board is a centered 168x168 grid with 56-unit cells`,
          near(result.board.x, 116) && near(result.board.y, 28.5)
          && near(result.board.width, 168) && near(result.board.height, 168));
        ok(`${surface} ${viewport}: X and O are anchored to exact cell centers`,
          centeredAt(result.xMark, 144, 56.5) && centeredAt(result.oMark, 256, 112.5));
        ok(`${surface} ${viewport}: marks retain 9 units of stroke-aware cell padding`,
          near(result.xStroke, 8) && near(result.oStroke, 8) && near(result.boardStroke, 6)
          && near(result.xMark.x - result.xStroke / 2 - 116, 9)
          && near(172 - (result.xMark.x + result.xMark.width + result.xStroke / 2), 9)
          && near(result.oMark.x - result.oStroke / 2 - 228, 9)
          && near(284 - (result.oMark.x + result.oMark.width + result.oStroke / 2), 9));
        ok(`${surface} ${viewport}: decorative route clears both marks`, result.routeClear);
        ok(`${surface} ${viewport}: board and marks are contained without page overflow`, result.contained && !result.overflow);
        ok(`${surface} ${viewport}: no console, runtime, or same-origin request errors`, faults.length === 0);
        await page.close();
      }
    }

    const reduced = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await reduced.emulateMedia({ reducedMotion: 'reduce' });
    await reduced.goto(`${base}/index.html#proekty`, { waitUntil: 'networkidle' });
    const animations = await reduced.evaluate(() => [
      '.project-art__route', '.project-art__nodes circle', '.project-art__subject > *',
      '.reference-art__search', '.reference-art__nodes circle',
    ].flatMap((selector) => [...document.querySelectorAll(selector)].map((node) => getComputedStyle(node).animationName)));
    ok('reduced motion: all redesigned decorative animation is disabled', animations.every((name) => name === 'none'));
    await reduced.close();

    await browser.close();
  } finally {
    server.kill('SIGTERM');
  }

  console.log(`\n[projects-reference] RESULT: ${failures === 0 ? 'PASS' : `FAIL (${failures} checks)`}`);
  if (failures) process.exitCode = 1;
})().catch((error) => { console.error(error); process.exitCode = 1; });
