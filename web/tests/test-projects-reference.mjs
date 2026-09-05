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

    const BOUNCING_BALL_VIEWPORTS = [[1440, 900], [1024, 900], [768, 1024], [390, 844]];
    for (const [width, height] of BOUNCING_BALL_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/projects/bouncing-ball/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const svg = document.querySelector('.project-art--bouncing-ball[aria-hidden="true"]');
        const visual = document.querySelector('.project-detail-hero__visual');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const visualRect = visual.getBoundingClientRect();
        const motionNodes = [
          ...document.querySelectorAll(
            '.project-art--bouncing-ball .ball-travel, .project-art--bouncing-ball .ball-squash, ' +
            '.project-art--bouncing-ball .ball-shadow, .project-art--bouncing-ball .ball-trail, ' +
            '.project-art--bouncing-ball .ball-impact, .project-art--bouncing-ball .ball-counter-pip-fill'
          ),
        ];
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          artFound: Boolean(svg),
          svgContained: svg ? svgRect.width <= visualRect.width + 1 && svgRect.height <= visualRect.height + 1 : false,
          playfieldFound: Boolean(document.querySelector('.project-art--bouncing-ball .ball-playfield')),
          ballFound: Boolean(document.querySelector('.project-art--bouncing-ball .ball-main')),
          trailFound: Boolean(document.querySelector('.project-art--bouncing-ball .ball-trail')),
          impactCount: document.querySelectorAll('.project-art--bouncing-ball .ball-impact').length,
          counterPipCount: document.querySelectorAll('.project-art--bouncing-ball .ball-counter-pip-fill').length,
          hasNormalMotion: motionNodes.some((node) => getComputedStyle(node).animationName !== 'none'),
        };
      });
      const viewport = `${width}x${height}`;
      ok(`bouncing-ball ${viewport}: art renders and is contained (no SVG overflow)`, result.artFound && result.svgContained);
      ok(`bouncing-ball ${viewport}: playfield and ball render`, result.playfieldFound && result.ballFound);
      ok(`bouncing-ball ${viewport}: a motion-trail hint renders`, result.trailFound);
      ok(`bouncing-ball ${viewport}: two wall-impact marks render`, result.impactCount === 2);
      ok(`bouncing-ball ${viewport}: a 2-pip bounce counter renders`, result.counterPipCount === 2);
      ok(`bouncing-ball ${viewport}: normal-motion animation is present`, result.hasNormalMotion);
      ok(`bouncing-ball ${viewport}: no page overflow or browser faults`, !result.overflow && faults.length === 0);
      await page.close();
    }

    const ROCK_PAPER_SCISSORS_VIEWPORTS = [[1440, 900], [1024, 900], [768, 1024], [390, 844]];
    for (const [width, height] of ROCK_PAPER_SCISSORS_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/projects/rock-paper-scissors/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const svg = document.querySelector('.project-art--rock-paper-scissors[aria-hidden="true"]');
        const visual = document.querySelector('.project-detail-hero__visual');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const visualRect = visual.getBoundingClientRect();
        const motionNodes = [
          ...document.querySelectorAll(
            '.project-art--rock-paper-scissors .rps-pool-token--selected, .project-art--rock-paper-scissors .rps-player-move, ' +
            '.project-art--rock-paper-scissors .rps-player-scale, .project-art--rock-paper-scissors .rps-winner-glow, ' +
            '.project-art--rock-paper-scissors .rps-computer-move, .project-art--rock-paper-scissors .rps-computer--rock, ' +
            '.project-art--rock-paper-scissors .rps-computer--paper, .project-art--rock-paper-scissors .rps-computer--scissors, ' +
            '.project-art--rock-paper-scissors .rps-reveal-ring, .project-art--rock-paper-scissors .rps-impact-pulse, ' +
            '.project-art--rock-paper-scissors .rps-impact-spark, .project-art--rock-paper-scissors .rps-rule-path'
          ),
        ];
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          artFound: Boolean(svg),
          svgContained: svg ? svgRect.width <= visualRect.width + 1 && svgRect.height <= visualRect.height + 1 : false,
          rockFound: Boolean(document.querySelector('.project-art--rock-paper-scissors .rps-player')),
          computerRockFound: Boolean(document.querySelector('.project-art--rock-paper-scissors .rps-computer--rock')),
          computerPaperFound: Boolean(document.querySelector('.project-art--rock-paper-scissors .rps-computer--paper')),
          computerScissorsFound: Boolean(document.querySelector('.project-art--rock-paper-scissors .rps-computer--scissors')),
          poolTokenCount: document.querySelectorAll('.project-art--rock-paper-scissors .rps-pool-token').length,
          winnerGlowFound: Boolean(document.querySelector('.project-art--rock-paper-scissors .rps-winner-glow')),
          impactFound: Boolean(document.querySelector('.project-art--rock-paper-scissors .rps-impact-pulse')),
          hasNormalMotion: motionNodes.some((node) => getComputedStyle(node).animationName !== 'none'),
        };
      });
      const viewport = `${width}x${height}`;
      ok(`rock-paper-scissors ${viewport}: art renders and is contained (no SVG overflow)`, result.artFound && result.svgContained);
      ok(`rock-paper-scissors ${viewport}: player rock symbol renders`, result.rockFound);
      ok(`rock-paper-scissors ${viewport}: all three computer choice groups render`, result.computerRockFound && result.computerPaperFound && result.computerScissorsFound);
      ok(`rock-paper-scissors ${viewport}: a 3-token player choice pool renders`, result.poolTokenCount === 3);
      ok(`rock-paper-scissors ${viewport}: winner glow and confrontation cue render`, result.winnerGlowFound && result.impactFound);
      ok(`rock-paper-scissors ${viewport}: normal-motion animation is present`, result.hasNormalMotion);
      ok(`rock-paper-scissors ${viewport}: no page overflow or browser faults`, !result.overflow && faults.length === 0);
      await page.close();
    }

    const BOUNCING_BALLS_OOP_VIEWPORTS = [[1440, 900], [1024, 900], [768, 1024], [390, 844]];
    for (const [width, height] of BOUNCING_BALLS_OOP_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/projects/bouncing-balls-oop/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const svg = document.querySelector('.project-art--bouncing-balls-oop[aria-hidden="true"]');
        const visual = document.querySelector('.project-detail-hero__visual');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const visualRect = visual.getBoundingClientRect();
        const motionNodes = [
          ...document.querySelectorAll(
            '.project-art--bouncing-balls-oop .oop-ball-travel, .project-art--bouncing-balls-oop .oop-ball-squash, ' +
            '.project-art--bouncing-balls-oop .oop-trail, .project-art--bouncing-balls-oop .oop-impact, ' +
            '.project-art--bouncing-balls-oop .oop-loop-ring, .project-art--bouncing-balls-oop .oop-instance-link'
          ),
        ];
        const balls = [...document.querySelectorAll('.project-art--bouncing-balls-oop .oop-ball')];
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          artFound: Boolean(svg),
          svgContained: svg ? svgRect.width <= visualRect.width + 1 && svgRect.height <= visualRect.height + 1 : false,
          playfieldFound: Boolean(document.querySelector('.project-art--bouncing-balls-oop .oop-playfield')),
          ballCount: balls.length,
          distinctRadiusCount: new Set(balls.map((b) => b.getAttribute('r'))).size,
          trailFound: Boolean(document.querySelector('.project-art--bouncing-balls-oop .oop-trail')),
          impactCount: document.querySelectorAll('.project-art--bouncing-balls-oop .oop-impact').length,
          instanceLinkFound: Boolean(document.querySelector('.project-art--bouncing-balls-oop .oop-instance-link')),
          loopFound: Boolean(document.querySelector('.project-art--bouncing-balls-oop .oop-loop-ring')),
          hasNormalMotion: motionNodes.some((node) => getComputedStyle(node).animationName !== 'none'),
        };
      });
      const viewport = `${width}x${height}`;
      ok(`bouncing-balls-oop ${viewport}: art renders and is contained (no SVG overflow)`, result.artFound && result.svgContained);
      ok(`bouncing-balls-oop ${viewport}: playfield renders`, result.playfieldFound);
      ok(`bouncing-balls-oop ${viewport}: at least 4 ball instances render with distinct radii`, result.ballCount >= 4 && result.distinctRadiusCount >= 4);
      ok(`bouncing-balls-oop ${viewport}: motion-trail hints render`, result.trailFound);
      ok(`bouncing-balls-oop ${viewport}: independent wall-impact cues render`, result.impactCount >= 4);
      ok(`bouncing-balls-oop ${viewport}: one-class/many-instances cue renders`, result.instanceLinkFound);
      ok(`bouncing-balls-oop ${viewport}: shared-loop cue renders`, result.loopFound);
      ok(`bouncing-balls-oop ${viewport}: normal-motion animation is present`, result.hasNormalMotion);
      ok(`bouncing-balls-oop ${viewport}: no page overflow or browser faults`, !result.overflow && faults.length === 0);
      await page.close();
    }

    const TEMPERATURE_CONVERTER_VIEWPORTS = [[1440, 900], [1024, 900], [768, 1024], [390, 844]];
    for (const [width, height] of TEMPERATURE_CONVERTER_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/projects/temperature-converter/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const svg = document.querySelector('.project-art--temperature-converter[aria-hidden="true"]');
        const visual = document.querySelector('.project-detail-hero__visual');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const visualRect = visual.getBoundingClientRect();
        const motionNodes = [
          ...document.querySelectorAll(
            '.project-art--temperature-converter .temp-column, .project-art--temperature-converter .temp-glow, ' +
            '.project-art--temperature-converter .temp-input, .project-art--temperature-converter .temp-hub-ring, ' +
            '.project-art--temperature-converter .temp-flow--fahrenheit, .project-art--temperature-converter .temp-flow--kelvin, ' +
            '.project-art--temperature-converter .temp-flow-dot, .project-art--temperature-converter .temp-value-state, ' +
            '.project-art--temperature-converter .temp-celsius, .project-art--temperature-converter .temp-fahrenheit, ' +
            '.project-art--temperature-converter .temp-kelvin'
          ),
        ];
        const cardText = (selector) => {
          const node = document.querySelector(selector);
          return node ? node.textContent.trim() : '';
        };
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          artFound: Boolean(svg),
          svgContained: svg ? svgRect.width <= visualRect.width + 1 && svgRect.height <= visualRect.height + 1 : false,
          thermometerFound: Boolean(document.querySelector('.project-art--temperature-converter .temp-thermometer')),
          columnFound: Boolean(document.querySelector('.project-art--temperature-converter .temp-column')),
          bulbFound: Boolean(document.querySelector('.project-art--temperature-converter .temp-bulb')),
          celsiusFound: Boolean(document.querySelector('.project-art--temperature-converter .temp-celsius')),
          fahrenheitFound: Boolean(document.querySelector('.project-art--temperature-converter .temp-fahrenheit')),
          kelvinFound: Boolean(document.querySelector('.project-art--temperature-converter .temp-kelvin')),
          flowCount: document.querySelectorAll('.project-art--temperature-converter .temp-flow').length,
          celsiusText: cardText('.project-art--temperature-converter .temp-value-state--celsius'),
          fahrenheitText: cardText('.project-art--temperature-converter .temp-value-state--fahrenheit'),
          kelvinText: cardText('.project-art--temperature-converter .temp-value-state--kelvin'),
          hasNormalMotion: motionNodes.some((node) => getComputedStyle(node).animationName !== 'none'),
        };
      });
      const viewport = `${width}x${height}`;
      ok(`temperature-converter ${viewport}: art renders and is contained (no SVG overflow)`, result.artFound && result.svgContained);
      ok(`temperature-converter ${viewport}: thermometer, liquid column, and bulb render`, result.thermometerFound && result.columnFound && result.bulbFound);
      ok(`temperature-converter ${viewport}: Celsius, Fahrenheit, and Kelvin cards all render`, result.celsiusFound && result.fahrenheitFound && result.kelvinFound);
      ok(`temperature-converter ${viewport}: conversion flow paths render`, result.flowCount >= 3);
      ok(`temperature-converter ${viewport}: displayed values are the mathematically correct 20 °C = 68 °F = 293.15 K`,
        result.celsiusText.includes('20') && result.celsiusText.includes('°C') &&
        result.fahrenheitText.includes('68') && result.fahrenheitText.includes('°F') &&
        result.kelvinText.includes('293.15') && result.kelvinText.includes('K'));
      ok(`temperature-converter ${viewport}: normal-motion animation is present`, result.hasNormalMotion);
      ok(`temperature-converter ${viewport}: no page overflow or browser faults`, !result.overflow && faults.length === 0);
      await page.close();
    }

    const NOTES_APP_VIEWPORTS = [[1440, 900], [1024, 900], [768, 1024], [390, 844]];
    for (const [width, height] of NOTES_APP_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/projects/notes-app/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const svg = document.querySelector('.project-art--notes-app[aria-hidden="true"]');
        const visual = document.querySelector('.project-detail-hero__visual');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const visualRect = visual.getBoundingClientRect();
        const motionNodes = [
          ...document.querySelectorAll(
            '.project-art--notes-app .notes-line--active, .project-art--notes-app .notes-caret, ' +
            '.project-art--notes-app .notes-unsaved, .project-art--notes-app .notes-save, ' +
            '.project-art--notes-app .notes-flow, .project-art--notes-app .notes-flow-dot, ' +
            '.project-art--notes-app .notes-file-glow, .project-art--notes-app .notes-file-line, ' +
            '.project-art--notes-app .notes-saved'
          ),
        ];
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          artFound: Boolean(svg),
          svgContained: svg ? svgRect.width <= visualRect.width + 1 && svgRect.height <= visualRect.height + 1 : false,
          windowFound: Boolean(document.querySelector('.project-art--notes-app .notes-window')),
          headerFound: Boolean(document.querySelector('.project-art--notes-app .notes-header')),
          editorFound: Boolean(document.querySelector('.project-art--notes-app .notes-editor')),
          lineCount: document.querySelectorAll('.project-art--notes-app .notes-line').length,
          caretFound: Boolean(document.querySelector('.project-art--notes-app .notes-caret')),
          unsavedFound: Boolean(document.querySelector('.project-art--notes-app .notes-unsaved')),
          saveFound: Boolean(document.querySelector('.project-art--notes-app .notes-save')),
          fileFound: Boolean(document.querySelector('.project-art--notes-app .notes-file')),
          savedFound: Boolean(document.querySelector('.project-art--notes-app .notes-saved')),
          hasNormalMotion: motionNodes.some((node) => getComputedStyle(node).animationName !== 'none'),
        };
      });
      const viewport = `${width}x${height}`;
      ok(`notes-app ${viewport}: art renders and is contained (no SVG overflow)`, result.artFound && result.svgContained);
      ok(`notes-app ${viewport}: editor window, header, and editor body render`, result.windowFound && result.headerFound && result.editorFound);
      ok(`notes-app ${viewport}: at least 4 text lines render`, result.lineCount >= 4);
      ok(`notes-app ${viewport}: caret, unsaved indicator, and save icon render`, result.caretFound && result.unsavedFound && result.saveFound);
      ok(`notes-app ${viewport}: file cue and saved-confirmation cue render`, result.fileFound && result.savedFound);
      ok(`notes-app ${viewport}: normal-motion animation is present`, result.hasNormalMotion);
      ok(`notes-app ${viewport}: no page overflow or browser faults`, !result.overflow && faults.length === 0);
      await page.close();
    }

    const SAFESORT_VIEWPORTS = [[1440, 900], [1024, 900], [768, 1024], [390, 844]];
    for (const [width, height] of SAFESORT_VIEWPORTS) {
      const page = await browser.newPage({ viewport: { width, height } });
      const faults = observePage(page, base);
      await page.goto(`${base}/projects/safesort/`, { waitUntil: 'networkidle' });
      const result = await page.evaluate(() => {
        const svg = document.querySelector('.project-art--safesort[aria-hidden="true"]');
        const visual = document.querySelector('.project-detail-hero__visual');
        const svgRect = svg ? svg.getBoundingClientRect() : null;
        const visualRect = visual.getBoundingClientRect();
        const motionNodes = [
          ...document.querySelectorAll(
            '.project-art--safesort .safesort-scan, .project-art--safesort .safesort-plan, ' +
            '.project-art--safesort .safesort-plan-row, .project-art--safesort .safesort-shield-badge, ' +
            '.project-art--safesort .safesort-folder-active, .project-art--safesort .safesort-files__mover--1, ' +
            '.project-art--safesort .safesort-files__mover--2, .project-art--safesort .safesort-duplicate-tile, ' +
            '.project-art--safesort .safesort-history-row, .project-art--safesort .safesort-undo'
          ),
        ];
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          artFound: Boolean(svg),
          svgContained: svg ? svgRect.width <= visualRect.width + 1 && svgRect.height <= visualRect.height + 1 : false,
          filesFound: Boolean(document.querySelector('.project-art--safesort .safesort-files')),
          scanFound: Boolean(document.querySelector('.project-art--safesort .safesort-scan')),
          planFound: Boolean(document.querySelector('.project-art--safesort .safesort-plan')),
          planRowCount: document.querySelectorAll('.project-art--safesort .safesort-plan-row').length,
          shieldFound: Boolean(document.querySelector('.project-art--safesort .safesort-shield')),
          folderCount: document.querySelectorAll('.project-art--safesort .safesort-folder').length,
          duplicateFound: Boolean(document.querySelector('.project-art--safesort .safesort-duplicate')),
          hashFound: Boolean(document.querySelector('.project-art--safesort .safesort-hash')),
          historyFound: Boolean(document.querySelector('.project-art--safesort .safesort-history')),
          undoFound: Boolean(document.querySelector('.project-art--safesort .safesort-undo')),
          hasNormalMotion: motionNodes.some((node) => getComputedStyle(node).animationName !== 'none'),
        };
      });
      const viewport = `${width}x${height}`;
      ok(`safesort ${viewport}: art renders and is contained (no SVG overflow)`, result.artFound && result.svgContained);
      ok(`safesort ${viewport}: source files and scan cue render`, result.filesFound && result.scanFound);
      ok(`safesort ${viewport}: plan card renders with at least 2 planned-move rows`, result.planFound && result.planRowCount >= 2);
      ok(`safesort ${viewport}: shield/safety-gate cue renders`, result.shieldFound);
      ok(`safesort ${viewport}: at least 2 destination folders render`, result.folderCount >= 2);
      ok(`safesort ${viewport}: duplicate comparison and hash cue render`, result.duplicateFound && result.hashFound);
      ok(`safesort ${viewport}: history/manifest log and undo cue render`, result.historyFound && result.undoFound);
      ok(`safesort ${viewport}: normal-motion animation is present`, result.hasNormalMotion);
      ok(`safesort ${viewport}: no page overflow or browser faults`, !result.overflow && faults.length === 0);
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
      '.project-art--bouncing-ball .ball-trail', '.project-art--bouncing-ball .ball-shadow',
      '.project-art--bouncing-ball .ball-impact', '.project-art--bouncing-ball .ball-travel',
      '.project-art--bouncing-ball .ball-squash', '.project-art--bouncing-ball .ball-counter-pip-fill',
      '.project-art--rock-paper-scissors .rps-pool-token--selected', '.project-art--rock-paper-scissors .rps-rule-path',
      '.project-art--rock-paper-scissors .rps-player-move', '.project-art--rock-paper-scissors .rps-player-scale',
      '.project-art--rock-paper-scissors .rps-winner-glow', '.project-art--rock-paper-scissors .rps-computer-move',
      '.project-art--rock-paper-scissors .rps-computer--rock', '.project-art--rock-paper-scissors .rps-computer--paper',
      '.project-art--rock-paper-scissors .rps-computer--scissors', '.project-art--rock-paper-scissors .rps-reveal-ring',
      '.project-art--rock-paper-scissors .rps-impact-pulse', '.project-art--rock-paper-scissors .rps-impact-spark',
      '.project-art--bouncing-balls-oop .oop-ball-travel', '.project-art--bouncing-balls-oop .oop-ball-squash',
      '.project-art--bouncing-balls-oop .oop-trail', '.project-art--bouncing-balls-oop .oop-impact',
      '.project-art--bouncing-balls-oop .oop-loop-ring', '.project-art--bouncing-balls-oop .oop-instance-link',
      '.project-art--temperature-converter .temp-column', '.project-art--temperature-converter .temp-glow',
      '.project-art--temperature-converter .temp-input', '.project-art--temperature-converter .temp-hub-ring',
      '.project-art--temperature-converter .temp-flow--fahrenheit', '.project-art--temperature-converter .temp-flow--kelvin',
      '.project-art--temperature-converter .temp-flow-dot', '.project-art--temperature-converter .temp-value-state',
      '.project-art--temperature-converter .temp-celsius', '.project-art--temperature-converter .temp-fahrenheit',
      '.project-art--temperature-converter .temp-kelvin',
      '.project-art--notes-app .notes-line--active', '.project-art--notes-app .notes-caret',
      '.project-art--notes-app .notes-unsaved', '.project-art--notes-app .notes-save',
      '.project-art--notes-app .notes-flow', '.project-art--notes-app .notes-flow-dot',
      '.project-art--notes-app .notes-file-glow', '.project-art--notes-app .notes-file-line',
      '.project-art--notes-app .notes-saved',
      '.project-art--safesort .safesort-scan', '.project-art--safesort .safesort-route',
      '.project-art--safesort .safesort-plan', '.project-art--safesort .safesort-plan-row',
      '.project-art--safesort .safesort-shield-badge', '.project-art--safesort .safesort-shield-check',
      '.project-art--safesort .safesort-folder-active', '.project-art--safesort .safesort-files__mover--1',
      '.project-art--safesort .safesort-files__mover--2', '.project-art--safesort .safesort-folder-pulse--1',
      '.project-art--safesort .safesort-folder-pulse--2', '.project-art--safesort .safesort-history-row',
      '.project-art--safesort .safesort-duplicate-tile', '.project-art--safesort .safesort-duplicate-check-badge',
      '.project-art--safesort .safesort-duplicate-check', '.project-art--safesort .safesort-hash-tick',
      '.project-art--safesort .safesort-history-check-badge', '.project-art--safesort .safesort-history-check',
      '.project-art--safesort .safesort-undo',
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
    const bouncingBallReducedState = await reduced.evaluate(() => {
      const opacityOf = (node) => parseFloat(getComputedStyle(node).opacity);
      const ball = document.querySelector('.project-art--bouncing-ball .ball-main');
      const travel = document.querySelector('.project-art--bouncing-ball .ball-travel');
      const squash = document.querySelector('.project-art--bouncing-ball .ball-squash');
      const impactRight = document.querySelector('.project-art--bouncing-ball .ball-impact--right');
      const impactTop = document.querySelector('.project-art--bouncing-ball .ball-impact--top');
      const pipFills = [...document.querySelectorAll('.project-art--bouncing-ball .ball-counter-pip-fill')];
      return {
        ballVisible: ball ? opacityOf(ball) !== 0 : false,
        atRest: travel && squash
          ? getComputedStyle(travel).transform === 'none' && getComputedStyle(squash).transform === 'none'
          : false,
        exactlyOneImpactVisible: impactRight && impactTop
          ? opacityOf(impactRight) > 0 && opacityOf(impactTop) === 0
          : false,
        pipsReset: pipFills.length > 0 && pipFills.every((node) => opacityOf(node) === 0),
      };
    });
    ok('reduced motion: bouncing-ball rests in place, not mid-flight or mid-squash', bouncingBallReducedState.ballVisible && bouncingBallReducedState.atRest);
    ok('reduced motion: bouncing-ball shows exactly one static wall-impact mark', bouncingBallReducedState.exactlyOneImpactVisible);
    ok('reduced motion: bouncing-ball counter pips stay reset (not stuck mid-count)', bouncingBallReducedState.pipsReset);
    const rpsReducedState = await reduced.evaluate(() => {
      const opacityOf = (node) => parseFloat(getComputedStyle(node).opacity);
      const player = document.querySelector('.project-art--rock-paper-scissors .rps-player');
      const glow = document.querySelector('.project-art--rock-paper-scissors .rps-winner-glow');
      const computerRock = document.querySelector('.project-art--rock-paper-scissors .rps-computer--rock');
      const computerPaper = document.querySelector('.project-art--rock-paper-scissors .rps-computer--paper');
      const computerScissors = document.querySelector('.project-art--rock-paper-scissors .rps-computer--scissors');
      const revealRing = document.querySelector('.project-art--rock-paper-scissors .rps-reveal-ring');
      const impactPulse = document.querySelector('.project-art--rock-paper-scissors .rps-impact-pulse');
      return {
        playerVisible: player ? opacityOf(player.closest('.rps-player-move') || player) !== 0 : false,
        glowVisible: glow ? opacityOf(glow) > 0 : false,
        rockHidden: computerRock ? opacityOf(computerRock) === 0 : false,
        paperHidden: computerPaper ? opacityOf(computerPaper) === 0 : false,
        scissorsDimmedVisible: computerScissors ? opacityOf(computerScissors) > 0 && opacityOf(computerScissors) < 1 : false,
        reveaRingHidden: revealRing ? opacityOf(revealRing) === 0 : false,
        impactHidden: impactPulse ? opacityOf(impactPulse) === 0 : false,
      };
    });
    ok('reduced motion: rock-paper-scissors shows the player rock settled and visible', rpsReducedState.playerVisible);
    ok('reduced motion: rock-paper-scissors shows a static winner glow on rock', rpsReducedState.glowVisible);
    ok('reduced motion: rock-paper-scissors hides the unselected computer previews (rock/paper)', rpsReducedState.rockHidden && rpsReducedState.paperHidden);
    ok('reduced motion: rock-paper-scissors shows scissors settled and dimmed as the loser', rpsReducedState.scissorsDimmedVisible);
    ok('reduced motion: rock-paper-scissors hides the reveal ring and confrontation pulse (no mid-cycle freeze)', rpsReducedState.reveaRingHidden && rpsReducedState.impactHidden);
    const oopReducedState = await reduced.evaluate(() => {
      const opacityOf = (node) => parseFloat(getComputedStyle(node).opacity);
      const balls = [...document.querySelectorAll('.project-art--bouncing-balls-oop .oop-ball')];
      const travels = [...document.querySelectorAll('.project-art--bouncing-balls-oop .oop-ball-travel, .project-art--bouncing-balls-oop .oop-ball-squash')];
      const trails = [...document.querySelectorAll('.project-art--bouncing-balls-oop .oop-trail')];
      const impacts = [...document.querySelectorAll('.project-art--bouncing-balls-oop .oop-impact')];
      const loopRing = document.querySelector('.project-art--bouncing-balls-oop .oop-loop-ring');
      const instanceLink = document.querySelector('.project-art--bouncing-balls-oop .oop-instance-link');
      return {
        ballsVisible: balls.length >= 4 && balls.every((b) => opacityOf(b) > 0),
        atRest: travels.every((node) => getComputedStyle(node).transform === 'none'),
        trailsHidden: trails.every((node) => opacityOf(node) === 0),
        impactsHidden: impacts.every((node) => opacityOf(node) === 0),
        loopHidden: loopRing ? opacityOf(loopRing) === 0 : false,
        instanceLinkHidden: instanceLink ? opacityOf(instanceLink) === 0 : false,
      };
    });
    ok('reduced motion: bouncing-balls-oop balls stay visible and at rest (no mid-flight or mid-squash freeze)', oopReducedState.ballsVisible && oopReducedState.atRest);
    ok('reduced motion: bouncing-balls-oop trails and impact cues are hidden', oopReducedState.trailsHidden && oopReducedState.impactsHidden);
    ok('reduced motion: bouncing-balls-oop shared-loop and instance-link cues are hidden', oopReducedState.loopHidden && oopReducedState.instanceLinkHidden);
    const tempReducedState = await reduced.evaluate(() => {
      const opacityOf = (node) => parseFloat(getComputedStyle(node).opacity);
      const textOf = (selector) => {
        const node = document.querySelector(selector);
        return node ? node.textContent.trim() : '';
      };
      const dots = [...document.querySelectorAll('.project-art--temperature-converter .temp-flow-dot')];
      const hubRing = document.querySelector('.project-art--temperature-converter .temp-hub-ring');
      const empty = document.querySelector('.project-art--temperature-converter .temp-value-state--empty');
      return {
        allValuesVisible:
          opacityOf(document.querySelector('.project-art--temperature-converter .temp-value-state--celsius')) === 1 &&
          opacityOf(document.querySelector('.project-art--temperature-converter .temp-value-state--fahrenheit')) === 1 &&
          opacityOf(document.querySelector('.project-art--temperature-converter .temp-value-state--kelvin')) === 1,
        emptyPlaceholderHidden: empty ? opacityOf(empty) === 0 : false,
        celsiusText: textOf('.project-art--temperature-converter .temp-value-state--celsius'),
        fahrenheitText: textOf('.project-art--temperature-converter .temp-value-state--fahrenheit'),
        kelvinText: textOf('.project-art--temperature-converter .temp-value-state--kelvin'),
        dotsHidden: dots.every((node) => opacityOf(node) === 0),
        hubRingHidden: hubRing ? opacityOf(hubRing) === 0 : false,
      };
    });
    ok('reduced motion: temperature-converter shows Celsius, Fahrenheit, and Kelvin simultaneously (not the empty placeholder)',
      tempReducedState.allValuesVisible && tempReducedState.emptyPlaceholderHidden);
    ok('reduced motion: temperature-converter static values are the mathematically correct 20 °C = 68 °F = 293.15 K',
      tempReducedState.celsiusText.includes('20') && tempReducedState.celsiusText.includes('°C') &&
      tempReducedState.fahrenheitText.includes('68') && tempReducedState.fahrenheitText.includes('°F') &&
      tempReducedState.kelvinText.includes('293.15') && tempReducedState.kelvinText.includes('K'));
    ok('reduced motion: temperature-converter travelling dots and hub pulse ring stay hidden (no mid-flight freeze)',
      tempReducedState.dotsHidden && tempReducedState.hubRingHidden);
    const notesReducedState = await reduced.evaluate(() => {
      const opacityOf = (node) => parseFloat(getComputedStyle(node).opacity);
      const lines = [...document.querySelectorAll('.project-art--notes-app .notes-line')];
      const activeLine = document.querySelector('.project-art--notes-app .notes-line--active');
      const referenceLine = lines.find((node) => node !== activeLine);
      const caret = document.querySelector('.project-art--notes-app .notes-caret');
      const unsaved = document.querySelector('.project-art--notes-app .notes-unsaved');
      const fileLines = [...document.querySelectorAll('.project-art--notes-app .notes-file-line')];
      const flowDot = document.querySelector('.project-art--notes-app .notes-flow-dot');
      const flow = document.querySelector('.project-art--notes-app .notes-flow');
      const fileGlow = document.querySelector('.project-art--notes-app .notes-file-glow');
      const saved = document.querySelector('.project-art--notes-app .notes-saved');
      return {
        allLinesVisible: lines.every((node) => opacityOf(node) > 0),
        activeLineComplete: activeLine && referenceLine
          ? activeLine.getBoundingClientRect().width / referenceLine.getBoundingClientRect().width > 0.5
          : false,
        caretVisible: caret ? opacityOf(caret) === 1 : false,
        unsavedClean: unsaved ? opacityOf(unsaved) < 0.5 : false,
        fileLinesVisible: fileLines.length > 0 && fileLines.every((node) => opacityOf(node) > 0),
        flowHidden: flow ? opacityOf(flow) === 0 : false,
        flowDotHidden: flowDot ? opacityOf(flowDot) === 0 : false,
        fileGlowHidden: fileGlow ? opacityOf(fileGlow) === 0 : false,
        savedBadgeHidden: saved ? opacityOf(saved) === 0 : false,
      };
    });
    ok('reduced motion: notes-app shows all text lines complete (not mid-typing)',
      notesReducedState.allLinesVisible && notesReducedState.activeLineComplete);
    ok('reduced motion: notes-app caret stays visible at rest (not blinking)', notesReducedState.caretVisible);
    ok('reduced motion: notes-app settles on a clean (saved) unsaved-indicator state', notesReducedState.unsavedClean);
    ok('reduced motion: notes-app file icon shows saved content', notesReducedState.fileLinesVisible);
    ok('reduced motion: notes-app data-flow path and travelling dot stay hidden (no mid-flight freeze)',
      notesReducedState.flowHidden && notesReducedState.flowDotHidden);
    ok('reduced motion: notes-app file confirmation glow and saved-checkmark badge stay hidden (no frozen pulse)',
      notesReducedState.fileGlowHidden && notesReducedState.savedBadgeHidden);
    const safesortReducedState = await reduced.evaluate(() => {
      const opacityOf = (node) => parseFloat(getComputedStyle(node).opacity);
      const scan = document.querySelector('.project-art--safesort .safesort-scan');
      const plan = document.querySelector('.project-art--safesort .safesort-plan');
      const planRows = [...document.querySelectorAll('.project-art--safesort .safesort-plan-row')];
      const shieldBadge = document.querySelector('.project-art--safesort .safesort-shield-badge');
      const shieldCheck = document.querySelector('.project-art--safesort .safesort-shield-check');
      const foldersActive = [...document.querySelectorAll('.project-art--safesort .safesort-folder-active')];
      const movers = [...document.querySelectorAll('.project-art--safesort .safesort-files__mover--1, .project-art--safesort .safesort-files__mover--2')];
      const folderPulses = [...document.querySelectorAll('.project-art--safesort .safesort-folder-pulse--1, .project-art--safesort .safesort-folder-pulse--2')];
      const historyRows = [...document.querySelectorAll('.project-art--safesort .safesort-history-row')];
      const duplicateTiles = [...document.querySelectorAll('.project-art--safesort .safesort-duplicate-tile')];
      const duplicateCheck = document.querySelector('.project-art--safesort .safesort-duplicate-check');
      const historyCheck = document.querySelector('.project-art--safesort .safesort-history-check');
      const undo = document.querySelector('.project-art--safesort .safesort-undo');
      return {
        scanHidden: scan ? opacityOf(scan) === 0 : false,
        planVisible: plan ? opacityOf(plan) === 1 : false,
        planRowsVisible: planRows.length >= 2 && planRows.every((node) => opacityOf(node) > 0),
        shieldValidated: shieldBadge && shieldCheck
          ? opacityOf(shieldBadge) === 1 && parseFloat(getComputedStyle(shieldCheck).strokeDashoffset) === 0
          : false,
        foldersActive: foldersActive.length >= 2 && foldersActive.every((node) => opacityOf(node) > 0),
        moversHidden: movers.every((node) => opacityOf(node) === 0),
        folderPulsesHidden: folderPulses.every((node) => opacityOf(node) === 0),
        historyRowsVisible: historyRows.length >= 2 && historyRows.every((node) => opacityOf(node) > 0),
        duplicateTilesVisible: duplicateTiles.every((node) => opacityOf(node) > 0),
        duplicateConfirmed: duplicateCheck ? parseFloat(getComputedStyle(duplicateCheck).strokeDashoffset) === 0 : false,
        historyConfirmed: historyCheck ? parseFloat(getComputedStyle(historyCheck).strokeDashoffset) === 0 : false,
        undoVisible: undo ? opacityOf(undo) === 1 && getComputedStyle(undo).transform !== 'none' : false,
      };
    });
    ok('reduced motion: safesort scan sweep stays hidden (not frozen mid-sweep)', safesortReducedState.scanHidden);
    ok('reduced motion: safesort plan card shows all planned-move rows settled in place', safesortReducedState.planVisible && safesortReducedState.planRowsVisible);
    ok('reduced motion: safesort shield/safety-gate shows a settled, validated checkmark', safesortReducedState.shieldValidated);
    ok('reduced motion: safesort destination folders stay in the active (approved) state', safesortReducedState.foldersActive);
    ok('reduced motion: safesort moving files and arrival pulses stay hidden (no mid-transfer freeze)', safesortReducedState.moversHidden && safesortReducedState.folderPulsesHidden);
    ok('reduced motion: safesort history/manifest log shows both logged rows with a confirmed checkmark', safesortReducedState.historyRowsVisible && safesortReducedState.historyConfirmed);
    ok('reduced motion: safesort duplicate pair stays visible with a confirmed match (not deleted)', safesortReducedState.duplicateTilesVisible && safesortReducedState.duplicateConfirmed);
    ok('reduced motion: safesort undo cue stays visible in its resting position', safesortReducedState.undoVisible);
    await reduced.close();

    await browser.close();
  } finally {
    server.kill('SIGTERM');
  }

  console.log(`\n[projects-reference] RESULT: ${failures === 0 ? 'PASS' : `FAIL (${failures} checks)`}`);
  if (failures) process.exitCode = 1;
})().catch((error) => { console.error(error); process.exitCode = 1; });
