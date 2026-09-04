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

    const STORY_GENERATOR_VIEWPORTS = [[1440, 900], [1024, 900], [768, 1024], [390, 844]];
    for (const [width, height] of STORY_GENERATOR_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/projects/story-generator/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const svg = document.querySelector('.project-art--story-generator[aria-hidden="true"]');
        const visual = document.querySelector('.project-detail-hero__visual');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const visualRect = visual.getBoundingClientRect();
        const motionNodes = [
          ...document.querySelectorAll(
            '.project-art--story-generator .story-token, .project-art--story-generator .story-route, ' +
            '.project-art--story-generator .story-hub-dot, .project-art--story-generator .story-output-line, ' +
            '.project-art--story-generator .story-spark'
          ),
        ];
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          artFound: Boolean(svg),
          svgContained: svg ? svgRect.width <= visualRect.width + 1 && svgRect.height <= visualRect.height + 1 : false,
          tokenCount: document.querySelectorAll('.project-art--story-generator .story-token').length,
          routeCount: document.querySelectorAll('.project-art--story-generator .story-route').length,
          outputFound: Boolean(document.querySelector('.project-art--story-generator .story-output-card')),
          hasNormalMotion: motionNodes.some((node) => getComputedStyle(node).animationName !== 'none'),
        };
      });
      const viewport = `${width}x${height}`;
      ok(`story-generator ${viewport}: art renders and is contained (no SVG overflow)`, result.artFound && result.svgContained);
      ok(`story-generator ${viewport}: 3 source-pool tokens render`, result.tokenCount === 3);
      ok(`story-generator ${viewport}: routing path(s) to the result render`, result.routeCount >= 1);
      ok(`story-generator ${viewport}: assembled result card renders`, result.outputFound);
      ok(`story-generator ${viewport}: normal-motion animation is present`, result.hasNormalMotion);
      ok(`story-generator ${viewport}: no page overflow or browser faults`, !result.overflow && faults.length === 0);
      await page.close();
    }

    const PAINT_APP_VIEWPORTS = [[1440, 900], [1024, 900], [768, 1024], [390, 844]];
    for (const [width, height] of PAINT_APP_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/projects/paint-app/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const svg = document.querySelector('.project-art--paint-app[aria-hidden="true"]');
        const visual = document.querySelector('.project-detail-hero__visual');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const visualRect = visual.getBoundingClientRect();
        const motionNodes = [
          ...document.querySelectorAll(
            '.project-art--paint-app .paint-stroke, .project-art--paint-app .paint-cursor, ' +
            '.project-art--paint-app .paint-shape, .project-art--paint-app .paint-tool-btn, ' +
            '.project-art--paint-app .paint-swatch'
          ),
        ];
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          artFound: Boolean(svg),
          svgContained: svg ? svgRect.width <= visualRect.width + 1 && svgRect.height <= visualRect.height + 1 : false,
          canvasFound: Boolean(document.querySelector('.project-art--paint-app .paint-canvas')),
          strokeFound: Boolean(document.querySelector('.project-art--paint-app .paint-stroke')),
          cursorFound: Boolean(document.querySelector('.project-art--paint-app .paint-cursor')),
          shapeCount: document.querySelectorAll('.project-art--paint-app .paint-shape').length,
          toolCount: document.querySelectorAll('.project-art--paint-app .paint-tool').length,
          hasNormalMotion: motionNodes.some((node) => getComputedStyle(node).animationName !== 'none'),
        };
      });
      const viewport = `${width}x${height}`;
      ok(`paint-app ${viewport}: art renders and is contained (no SVG overflow)`, result.artFound && result.svgContained);
      ok(`paint-app ${viewport}: canvas, brush stroke, and cursor render`, result.canvasFound && result.strokeFound && result.cursorFound);
      ok(`paint-app ${viewport}: at least one shape-tool outline renders`, result.shapeCount >= 1);
      ok(`paint-app ${viewport}: toolbar renders`, result.toolCount >= 3);
      ok(`paint-app ${viewport}: normal-motion animation is present`, result.hasNormalMotion);
      ok(`paint-app ${viewport}: no page overflow or browser faults`, !result.overflow && faults.length === 0);
      await page.close();
    }

    const SNAKE_VIEWPORTS = [[1440, 900], [1024, 900], [768, 1024], [390, 844]];
    for (const [width, height] of SNAKE_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/projects/snake/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const svg = document.querySelector('.project-art--snake[aria-hidden="true"]');
        const visual = document.querySelector('.project-detail-hero__visual');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const visualRect = visual.getBoundingClientRect();
        const motionNodes = [
          ...document.querySelectorAll(
            '.project-art--snake .snake-segment, .project-art--snake .snake-head, ' +
            '.project-art--snake .snake-apple, .project-art--snake .snake-route, ' +
            '.project-art--snake .snake-tail'
          ),
        ];
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          artFound: Boolean(svg),
          svgContained: svg ? svgRect.width <= visualRect.width + 1 && svgRect.height <= visualRect.height + 1 : false,
          segmentCount: document.querySelectorAll('.project-art--snake .snake-segment').length,
          headFound: Boolean(document.querySelector('.project-art--snake .snake-head')),
          appleFound: Boolean(document.querySelector('.project-art--snake .snake-apple')),
          routeFound: Boolean(document.querySelector('.project-art--snake .snake-route')),
          hasNormalMotion: motionNodes.some((node) => getComputedStyle(node).animationName !== 'none'),
        };
      });
      const viewport = `${width}x${height}`;
      ok(`snake ${viewport}: art renders and is contained (no SVG overflow)`, result.artFound && result.svgContained);
      ok(`snake ${viewport}: 6-9 body segments render`, result.segmentCount >= 6 && result.segmentCount <= 9);
      ok(`snake ${viewport}: a distinct head renders`, result.headFound);
      ok(`snake ${viewport}: one apple renders`, result.appleFound);
      ok(`snake ${viewport}: a route/trajectory hint renders`, result.routeFound);
      ok(`snake ${viewport}: normal-motion animation is present`, result.hasNormalMotion);
      ok(`snake ${viewport}: no page overflow or browser faults`, !result.overflow && faults.length === 0);
      await page.close();
    }

    const SPACE_SHOOTER_VIEWPORTS = [[1440, 900], [1024, 900], [768, 1024], [390, 844]];
    for (const [width, height] of SPACE_SHOOTER_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/projects/space-shooter/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const svg = document.querySelector('.project-art--space-shooter[aria-hidden="true"]');
        const visual = document.querySelector('.project-detail-hero__visual');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const visualRect = visual.getBoundingClientRect();
        const motionNodes = [
          ...document.querySelectorAll(
            '.project-art--space-shooter .shooter-player, .project-art--space-shooter .shooter-enemy, ' +
            '.project-art--space-shooter .shooter-shot, .project-art--space-shooter .shooter-enemy-shot, ' +
            '.project-art--space-shooter .shooter-engine, .project-art--space-shooter .shooter-explosion, ' +
            '.project-art--space-shooter .shooter-stars-far, .project-art--space-shooter .shooter-route'
          ),
        ];
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          artFound: Boolean(svg),
          svgContained: svg ? svgRect.width <= visualRect.width + 1 && svgRect.height <= visualRect.height + 1 : false,
          playerFound: Boolean(document.querySelector('.project-art--space-shooter .shooter-player')),
          enemyCount: document.querySelectorAll('.project-art--space-shooter .shooter-enemy').length,
          shotFound: Boolean(document.querySelector('.project-art--space-shooter .shooter-shot')),
          engineFound: Boolean(document.querySelector('.project-art--space-shooter .shooter-engine')),
          explosionFound: Boolean(document.querySelector('.project-art--space-shooter .shooter-explosion')),
          starsFound: Boolean(document.querySelector('.project-art--space-shooter .shooter-stars-far')),
          hasNormalMotion: motionNodes.some((node) => getComputedStyle(node).animationName !== 'none'),
        };
      });
      const viewport = `${width}x${height}`;
      ok(`space-shooter ${viewport}: art renders and is contained (no SVG overflow)`, result.artFound && result.svgContained);
      ok(`space-shooter ${viewport}: player ship renders`, result.playerFound);
      ok(`space-shooter ${viewport}: 2-4 enemies render`, result.enemyCount >= 2 && result.enemyCount <= 4);
      ok(`space-shooter ${viewport}: player shot, engine, and explosion cue render`, result.shotFound && result.engineFound && result.explosionFound);
      ok(`space-shooter ${viewport}: starfield renders`, result.starsFound);
      ok(`space-shooter ${viewport}: normal-motion animation is present`, result.hasNormalMotion);
      ok(`space-shooter ${viewport}: no page overflow or browser faults`, !result.overflow && faults.length === 0);
      await page.close();
    }

    const CALCULATOR_VIEWPORTS = [[1440, 900], [1024, 900], [768, 1024], [390, 844]];
    for (const [width, height] of CALCULATOR_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/projects/calculator/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const svg = document.querySelector('.project-art--calculator[aria-hidden="true"]');
        const visual = document.querySelector('.project-detail-hero__visual');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const visualRect = visual.getBoundingClientRect();
        const motionNodes = [
          ...document.querySelectorAll(
            '.project-art--calculator .calc-key--seq-1, .project-art--calculator .calc-key--seq-2, ' +
            '.project-art--calculator .calc-key--seq-3, .project-art--calculator .calc-key--seq-4, ' +
            '.project-art--calculator .calc-key--seq-5, .project-art--calculator .calc-display-state, ' +
            '.project-art--calculator .calc-result-value'
          ),
        ];
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          artFound: Boolean(svg),
          svgContained: svg ? svgRect.width <= visualRect.width + 1 && svgRect.height <= visualRect.height + 1 : false,
          displayFound: Boolean(document.querySelector('.project-art--calculator .calc-display')),
          keyCount: document.querySelectorAll('.project-art--calculator .calc-key').length,
          operatorKeyCount: document.querySelectorAll('.project-art--calculator .calc-key--operator').length,
          equalsKeyFound: Boolean(document.querySelector('.project-art--calculator .calc-key--equals')),
          displayStateCount: document.querySelectorAll('.project-art--calculator .calc-display-state').length,
          resultStateFound: Boolean(document.querySelector('.project-art--calculator .calc-display-state--result')),
          hasNormalMotion: motionNodes.some((node) => getComputedStyle(node).animationName !== 'none'),
        };
      });
      const viewport = `${width}x${height}`;
      ok(`calculator ${viewport}: art renders and is contained (no SVG overflow)`, result.artFound && result.svgContained);
      ok(`calculator ${viewport}: display renders`, result.displayFound);
      ok(`calculator ${viewport}: 16 keys render`, result.keyCount === 16);
      ok(`calculator ${viewport}: 4 operator keys and one equals key render`, result.operatorKeyCount === 4 && result.equalsKeyFound);
      ok(`calculator ${viewport}: 6 display states including the result state render`, result.displayStateCount === 6 && result.resultStateFound);
      ok(`calculator ${viewport}: normal-motion animation is present`, result.hasNormalMotion);
      ok(`calculator ${viewport}: no page overflow or browser faults`, !result.overflow && faults.length === 0);
      await page.close();
    }

    const TODO_APP_VIEWPORTS = [[1440, 900], [1024, 900], [768, 1024], [390, 844]];
    for (const [width, height] of TODO_APP_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/projects/todo-app/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const svg = document.querySelector('.project-art--todo-app[aria-hidden="true"]');
        const visual = document.querySelector('.project-detail-hero__visual');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const visualRect = visual.getBoundingClientRect();
        const motionNodes = [
          ...document.querySelectorAll(
            '.project-art--todo-app .todo-input-state, .project-art--todo-app .todo-add, ' +
            '.project-art--todo-app .todo-row--new, .project-art--todo-app .todo-checkbox-fill, ' +
            '.project-art--todo-app .todo-check, .project-art--todo-app .todo-strike, ' +
            '.project-art--todo-app .todo-delete, .project-art--todo-app .todo-db-pulse'
          ),
        ];
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          artFound: Boolean(svg),
          svgContained: svg ? svgRect.width <= visualRect.width + 1 && svgRect.height <= visualRect.height + 1 : false,
          inputFound: Boolean(document.querySelector('.project-art--todo-app .todo-input')),
          addFound: Boolean(document.querySelector('.project-art--todo-app .todo-add')),
          rowCount: document.querySelectorAll('.project-art--todo-app .todo-row').length,
          checkboxCount: document.querySelectorAll('.project-art--todo-app .todo-checkbox').length,
          checkFound: Boolean(document.querySelector('.project-art--todo-app .todo-check')),
          strikeFound: Boolean(document.querySelector('.project-art--todo-app .todo-strike')),
          deleteCount: document.querySelectorAll('.project-art--todo-app .todo-delete').length,
          dbFound: Boolean(document.querySelector('.project-art--todo-app .todo-db')),
          hasNormalMotion: motionNodes.some((node) => getComputedStyle(node).animationName !== 'none'),
        };
      });
      const viewport = `${width}x${height}`;
      ok(`todo-app ${viewport}: art renders and is contained (no SVG overflow)`, result.artFound && result.svgContained);
      ok(`todo-app ${viewport}: input and add button render`, result.inputFound && result.addFound);
      ok(`todo-app ${viewport}: at least 3 task rows with checkboxes render`, result.rowCount >= 3 && result.checkboxCount >= 3);
      ok(`todo-app ${viewport}: completed task shows a drawn checkmark and strike-through`, result.checkFound && result.strikeFound);
      ok(`todo-app ${viewport}: delete controls render`, result.deleteCount >= 3);
      ok(`todo-app ${viewport}: persistence (database) cue renders`, result.dbFound);
      ok(`todo-app ${viewport}: normal-motion animation is present`, result.hasNormalMotion);
      ok(`todo-app ${viewport}: no page overflow or browser faults`, !result.overflow && faults.length === 0);
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
      '.project-art--story-generator .story-token', '.project-art--story-generator .story-route',
      '.project-art--story-generator .story-hub-dot', '.project-art--story-generator .story-output-line',
      '.project-art--story-generator .story-spark',
      '.project-art--paint-app .paint-stroke', '.project-art--paint-app .paint-cursor',
      '.project-art--paint-app .paint-shape', '.project-art--paint-app .paint-tool-btn',
      '.project-art--paint-app .paint-swatch',
      '.project-art--snake .snake-segment', '.project-art--snake .snake-head',
      '.project-art--snake .snake-apple', '.project-art--snake .snake-apple-leaf',
      '.project-art--snake .snake-route', '.project-art--snake .snake-tail',
      '.project-art--space-shooter .shooter-player', '.project-art--space-shooter .shooter-enemy',
      '.project-art--space-shooter .shooter-shot', '.project-art--space-shooter .shooter-enemy-shot',
      '.project-art--space-shooter .shooter-engine', '.project-art--space-shooter .shooter-explosion',
      '.project-art--space-shooter .shooter-stars-far', '.project-art--space-shooter .shooter-stars-near',
      '.project-art--space-shooter .shooter-stars-bright circle', '.project-art--space-shooter .shooter-route',
      '.project-art--calculator .calc-key--seq-1', '.project-art--calculator .calc-key--seq-2',
      '.project-art--calculator .calc-key--seq-3', '.project-art--calculator .calc-key--seq-4',
      '.project-art--calculator .calc-key--seq-5', '.project-art--calculator .calc-display-state',
      '.project-art--calculator .calc-result-value',
      '.project-art--todo-app .todo-input-state', '.project-art--todo-app .todo-add',
      '.project-art--todo-app .todo-row--new', '.project-art--todo-app .todo-checkbox-fill',
      '.project-art--todo-app .todo-check', '.project-art--todo-app .todo-strike',
      '.project-art--todo-app .todo-delete', '.project-art--todo-app .todo-db-pulse',
    ].flatMap((selector) => [...document.querySelectorAll(selector)].map((node) => getComputedStyle(node).animationName)));
    ok('reduced motion: all redesigned decorative animation is disabled', animations.every((name) => name === 'none'));
    const storyReducedState = await reduced.evaluate(() => {
      const visible = (node) => getComputedStyle(node).opacity !== '0';
      return {
        tokensVisible: [...document.querySelectorAll('.project-art--story-generator .story-token')].every(visible),
        outputLinesVisible: [...document.querySelectorAll('.project-art--story-generator .story-output-line')].every(visible),
      };
    });
    ok('reduced motion: story generator result card stays fully visible (not mid-fade)', storyReducedState.tokensVisible && storyReducedState.outputLinesVisible);
    const paintReducedState = await reduced.evaluate(() => {
      const visible = (node) => getComputedStyle(node).opacity !== '0';
      const strokePath = document.querySelector('.project-art--paint-app .paint-stroke');
      return {
        shapesVisible: [...document.querySelectorAll('.project-art--paint-app .paint-shape')].every(visible),
        strokeComplete: strokePath ? parseFloat(getComputedStyle(strokePath).strokeDashoffset) === 0 : false,
      };
    });
    ok('reduced motion: paint app canvas stays fully visible (stroke complete, shapes shown)', paintReducedState.shapesVisible && paintReducedState.strokeComplete);
    const snakeReducedState = await reduced.evaluate(() => {
      const visible = (node) => getComputedStyle(node).opacity !== '0';
      return {
        segmentsVisible: [...document.querySelectorAll('.project-art--snake .snake-segment')].every(visible),
        headVisible: visible(document.querySelector('.project-art--snake .snake-head')),
        appleVisible: visible(document.querySelector('.project-art--snake .snake-apple')),
      };
    });
    ok('reduced motion: snake body, head, and apple stay fully visible', snakeReducedState.segmentsVisible && snakeReducedState.headVisible && snakeReducedState.appleVisible);
    const shooterReducedState = await reduced.evaluate(() => {
      const visible = (node) => getComputedStyle(node).opacity !== '0';
      const explosion = document.querySelector('.project-art--space-shooter .shooter-explosion');
      return {
        playerVisible: visible(document.querySelector('.project-art--space-shooter .shooter-player')),
        enemiesVisible: [...document.querySelectorAll('.project-art--space-shooter .shooter-enemy')].every(visible),
        explosionHidden: explosion ? getComputedStyle(explosion).opacity === '0' : false,
      };
    });
    ok('reduced motion: space-shooter ship and enemies stay fully visible', shooterReducedState.playerVisible && shooterReducedState.enemiesVisible);
    ok('reduced motion: space-shooter explosion does not freeze mid-blast', shooterReducedState.explosionHidden);
    const calculatorReducedState = await reduced.evaluate(() => {
      const opacityOf = (node) => parseFloat(getComputedStyle(node).opacity);
      const nonResultStates = [...document.querySelectorAll('.project-art--calculator .calc-display-state:not(.calc-display-state--result)')];
      const resultState = document.querySelector('.project-art--calculator .calc-display-state--result');
      return {
        onlyResultVisible: nonResultStates.every((node) => opacityOf(node) === 0) && resultState && opacityOf(resultState) === 1,
        equalsKeyStyled: getComputedStyle(document.querySelector('.project-art--calculator .calc-key--seq-5')).transform !== 'none',
      };
    });
    ok('reduced motion: calculator shows only the settled 12 + 7 / 19 result state', calculatorReducedState.onlyResultVisible);
    ok('reduced motion: calculator equals key stays visually selected', calculatorReducedState.equalsKeyStyled);
    const todoReducedState = await reduced.evaluate(() => {
      const opacityOf = (node) => parseFloat(getComputedStyle(node).opacity);
      const newRow = document.querySelector('.project-art--todo-app .todo-row--new');
      const checkboxFill = document.querySelector('.project-art--todo-app .todo-checkbox-fill');
      const check = document.querySelector('.project-art--todo-app .todo-check');
      const strike = document.querySelector('.project-art--todo-app .todo-strike');
      const dbPulses = [...document.querySelectorAll('.project-art--todo-app .todo-db-pulse')];
      return {
        rowCount: document.querySelectorAll('.project-art--todo-app .todo-row').length,
        newRowVisible: newRow ? opacityOf(newRow) === 1 && getComputedStyle(newRow).transform === 'none' : false,
        completedChecked: checkboxFill ? opacityOf(checkboxFill) === 1 : false,
        checkmarkDrawn: check ? parseFloat(getComputedStyle(check).strokeDashoffset) === 0 : false,
        strikeDrawn: strike ? parseFloat(getComputedStyle(strike).strokeDashoffset) === 0 : false,
        pulsesHidden: dbPulses.every((node) => opacityOf(node) === 0),
      };
    });
    ok('reduced motion: todo-app shows 3 task rows with the new row settled in place', todoReducedState.rowCount >= 3 && todoReducedState.newRowVisible);
    ok('reduced motion: todo-app completed task shows a checked box with drawn checkmark and strike-through', todoReducedState.completedChecked && todoReducedState.checkmarkDrawn && todoReducedState.strikeDrawn);
    ok('reduced motion: todo-app persistence pulses stay hidden (no mid-flight ping)', todoReducedState.pulsesHidden);
    await reduced.close();

    await browser.close();
  } finally {
    server.kill('SIGTERM');
  }

  console.log(`\n[projects-reference] RESULT: ${failures === 0 ? 'PASS' : `FAIL (${failures} checks)`}`);
  if (failures) process.exitCode = 1;
})().catch((error) => { console.error(error); process.exitCode = 1; });
