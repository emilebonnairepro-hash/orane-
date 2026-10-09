// Rend chaque étiquette du calque : PNG 600 dpi fond transparent (taille exacte du gabarit), PDF, et aperçu avec repères.
import { createRequire } from 'module';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }

const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const MM = 96 / 25.4;
const browser = await chromium.launch();
for (const j of jobs) {
  for (const [name, transparent, scale] of [['etiquette', true, 600 / 96], ['apercu', false, 2.5]]) {
    const page = await browser.newPage({ viewport: { width: Math.ceil(j.w * MM), height: Math.ceil(j.h * MM) }, deviceScaleFactor: scale });
    await page.goto('file://' + path.join(j.dir, `${name}.html`));
    await page.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 20000 });
    await page.waitForTimeout(150);
    await page.screenshot({ path: path.join(j.dir, `${name}.png`), omitBackground: transparent, clip: { x: 0, y: 0, width: j.w * MM, height: j.h * MM } });
    if (name === 'etiquette') await page.pdf({ path: path.join(j.dir, 'etiquette.pdf'), width: `${j.w}mm`, height: `${j.h}mm`, printBackground: true });
    await page.close();
  }
  execFileSync('python3', ['-c', `
from PIL import Image
p='${path.join(j.dir, 'etiquette.png')}'
im=Image.open(p).convert('RGBA')
if im.size != (${j.px[0]}, ${j.px[1]}): im=im.resize((${j.px[0]}, ${j.px[1]}), Image.LANCZOS)
im.save(p, dpi=(600, 600), optimize=True)
`]);
  console.log('✓', path.basename(j.dir), j.px.join('×'));
}
await browser.close();
