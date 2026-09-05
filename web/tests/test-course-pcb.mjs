// Real manifest/state, connector geometry, animation and responsive contracts.
// PCB_BASE_URL can target the exact preview or production deployment.
import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'manifest/practice_manifest.json')));
const chapters = JSON.parse(fs.readFileSync(path.join(root, 'data/chapters.json'))).chapters;
const server = process.env.PCB_BASE_URL ? null : spawn('python3', ['-m', 'http.server', '0', '--bind', '127.0.0.1', '--directory', path.join(root, 'dist')], {env: {...process.env, PYTHONUNBUFFERED: '1'}});
let base = process.env.PCB_BASE_URL;
let checks = 0;
function check(message, condition) { assert.ok(condition, message); checks++; console.log(`[ok] ${message}`); }
const output = process.env.PCB_EVIDENCE_DIR;
if (output) fs.mkdirSync(output, {recursive: true});
let browser;
try {
  if (server) base = await new Promise((resolve, reject) => {
    server.stdout.on('data', data => { const match = String(data).match(/port (\d+)/); if (match) resolve(`http://127.0.0.1:${match[1]}`); });
    server.on('error', reject); server.on('exit', code => reject(new Error(`server exited ${code}`)));
  });
  browser = await chromium.launch();
  for (const [width, height] of [[1920,1080],[1440,900],[1280,800],[1024,900],[768,1024],[430,932],[390,844],[360,800]]) {
    const page = await browser.newPage({viewport:{width,height}});
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    await page.goto(`${base}/index.html`, {waitUntil:'networkidle'});
    await page.locator('.pcb-board').waitFor();
    const geometry = await page.evaluate(() => {
      const board = document.querySelector('.pcb-board').getBoundingClientRect();
      const nodes = [...document.querySelectorAll('.journey-node')];
      return {
        overflow: document.documentElement.scrollWidth > innerWidth,
        contained: nodes.every(n => { const c=n.querySelector('.jn-card').getBoundingClientRect(); return c.left>=board.left && c.right<=board.right; }),
        collision: nodes.some((n,i) => { if (!i) return false; const a=n.getBoundingClientRect(), b=nodes[i-1].getBoundingClientRect(); return a.top < b.bottom-1; }),
        connected: nodes.every(n => { const card=n.querySelector('.jn-card').getBoundingClientRect(), route=n.querySelector('.jn-route').getBoundingClientRect(); return Math.min(Math.abs(route.right-card.left),Math.abs(route.left-card.right))<2 && Math.abs(route.top+90-(card.top+card.height/2))<2; }),
        pins: nodes.every(n => n.querySelectorAll('.jn-pins i').length===4),
        bus: document.querySelectorAll('.pcb-bus i').length,
        links: nodes.map(n=>({number:Number(n.dataset.chapter),href:n.querySelector('a').getAttribute('href'),title:n.querySelector('.jn-title').textContent})),
        packet: getComputedStyle(document.querySelector('.state-current .pcb-packet')).animationName,
        decorative: [...document.querySelectorAll('.pcb-board svg')].every(s=>s.getAttribute('aria-hidden')==='true'),
      };
    });
    check(`${width}: no overflow, clipping or collisions`, !geometry.overflow && geometry.contained && !geometry.collision);
    check(`${width}: every module physically connects to three-line bus`, geometry.connected && geometry.pins && geometry.bus===3);
    check(`${width}: exact 24 manifest routes and titles`, geometry.links.length===24 && chapters.every(c=>geometry.links.some(l=>l.number===c.number && l.href===c.url && l.title===c.title)));
    check(`${width}: decorative SVG and live packet`, geometry.decorative && geometry.packet==='pcb-packet-travel');
    check(`${width}: no JavaScript errors`, errors.length===0);
    await page.locator('.journey-rail').evaluate(el=>window.scrollTo(0,el.getBoundingClientRect().top+scrollY-180));
    if (output) await page.screenshot({path:path.join(output,`roadmap-${width}.png`)});
    await page.close();
  }
  const page = await browser.newPage({viewport:{width:1440,height:900}});
  await page.goto(`${base}/index.html`, {waitUntil:'networkidle'});
  const seed = Object.fromEntries(Object.keys(manifest).filter(id=>id.startsWith('01-')).map(id=>[id,{status:'completed'}]));
  seed[Object.keys(manifest).find(id=>id.startsWith('03-'))]={status:'completed-local'};
  await page.evaluate(data=>localStorage.setItem('cartesian.python.progress.v1',JSON.stringify(data)),seed);
  await page.reload({waitUntil:'networkidle'});
  // Scoped to .journey-node: the Practice catalog cards (.practice-chapter-group)
  // share the same data-chapter/.state-* convention (see progress.js) and now
  // legitimately carry their own independent .state-completed/.state-no-lessons
  // for the same chapters, so an unscoped [data-chapter] selector would match both.
  check('completed/current/theory states derive from real lesson store', await page.locator('.journey-node[data-chapter="1"].state-completed').count()===1 && await page.locator('.journey-node[data-chapter="3"].state-current.state-in-progress').count()===1 && await page.locator('.journey-node[data-chapter="2"].state-no-lessons .jn-progress-track').count()===0);
  check('current module exposes aria-current and completed conductor is full', await page.locator('.state-current .jn-card').getAttribute('aria-current')==='step' && await page.locator('.journey-node[data-chapter="1"] .jn-progress-fill').evaluate(e=>e.style.width)==='100%');
  const before = await page.locator('.state-current .pcb-packet').evaluate(e=>getComputedStyle(e).strokeDashoffset);
  await page.waitForTimeout(1100);
  const after = await page.locator('.state-current .pcb-packet').evaluate(e=>getComputedStyle(e).strokeDashoffset);
  check('packet moves within 1.1 seconds', before!==after);
  await page.locator('.state-current .jn-card').focus();
  check('keyboard focus is visible', await page.locator('.state-current .jn-card').evaluate(e=>getComputedStyle(e).outlineStyle)==='solid');
  if (output) {
    await page.locator('.state-current').evaluate(e=>window.scrollTo(0,e.getBoundingClientRect().top+scrollY-400));
    await page.screenshot({path:path.join(output,'seeded-desktop.png')});
  }
  await page.emulateMedia({reducedMotion:'reduce'});
  check('reduced motion freezes all board animations and preserves packet', await page.evaluate(()=>document.querySelector('.pcb-board').getAnimations({subtree:true}).length===0 && getComputedStyle(document.querySelector('.state-current .pcb-packet')).opacity==='1'));
  await page.evaluate(ids=>localStorage.setItem('cartesian.python.progress.v1',JSON.stringify(Object.fromEntries(ids.map(id=>[id,{status:'completed'}])))),Object.keys(manifest));
  await page.reload({waitUntil:'networkidle'});
  check('fully completed course has no fake current chapter or moving packet', await page.locator('.state-current').count()===0 && await page.locator('.jp-pct').textContent()==='100%');
  await page.close();
  const offline = await browser.newPage({javaScriptEnabled:false,viewport:{width:390,height:844}});
  await offline.goto(`${base}/index.html`);
  check('without JavaScript all 24 semantic links and board remain visible', await offline.locator('.jn-card').count()===24 && await offline.locator('.pcb-board').isVisible());
  await offline.close();
  console.log(`PCB contract: ${checks} passed`);
} finally { await browser?.close(); server?.kill(); }
