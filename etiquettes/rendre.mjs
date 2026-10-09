// Rend chaque étiquette en PNG 600 dpi (et en PDF pour les fichiers à téléverser) avec Chromium.
import { createRequire } from 'module';
import fs from 'node:fs';
import path from 'node:path';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }

const dir = process.argv[2];
const jobs = JSON.parse(fs.readFileSync(path.join(dir, 'source', 'jobs.json'), 'utf8'));
const MM = 96 / 25.4;           // px CSS par mm
const SCALE = 600 / 96;         // 600 dpi
for (const d of ['export', 'apercu']) fs.mkdirSync(path.join(dir, d), { recursive: true });

const browser = await chromium.launch();
for (const j of jobs) {
  const page = await browser.newPage({ viewport: { width: Math.round(j.w * MM), height: Math.round(j.h * MM) }, deviceScaleFactor: j.apercu ? 3 : SCALE });
  await page.goto('file://' + j.html);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const out = path.join(dir, j.apercu ? 'apercu' : 'export', `${j.nom}.png`);
  await page.screenshot({ path: out });
  if (!j.apercu) await page.pdf({ path: path.join(dir, 'export', `${j.nom}.pdf`), width: `${j.w}mm`, height: `${j.h}mm`, printBackground: true });
  console.log('✓', path.relative(dir, out));
  await page.close();
}
await browser.close();
