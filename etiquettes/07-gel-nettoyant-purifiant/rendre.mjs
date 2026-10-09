// Rend l'étiquette au format exact du gabarit Selfnamed : 3367 × 2575 px (600 dpi), fond transparent.
import { createRequire } from 'module';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }

const dir = process.argv[2];
const W_MM = 142.5, H_MM = 109;
const MM = 96 / 25.4, SCALE = 600 / 96;
const browser = await chromium.launch();
for (const [name, transparent, scale] of [['etiquette', true, SCALE], ['apercu', false, 2.5]]) {
  const page = await browser.newPage({ viewport: { width: Math.ceil(W_MM * MM), height: Math.ceil(H_MM * MM) }, deviceScaleFactor: scale });
  await page.goto('file://' + path.join(dir, `${name}.html`));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(dir, `${name}.png`), omitBackground: transparent, clip: { x: 0, y: 0, width: W_MM * MM, height: H_MM * MM } });
  if (name === 'etiquette') await page.pdf({ path: path.join(dir, 'etiquette.pdf'), width: `${W_MM}mm`, height: `${H_MM}mm`, printBackground: true });
  await page.close();
}
await browser.close();
// Taille exacte demandée par le gabarit
execFileSync('python3', ['-c', `
from PIL import Image
p='${path.join(dir, 'etiquette.png')}'
im=Image.open(p).convert('RGBA')
if im.size != (3367, 2575): im=im.resize((3367, 2575), Image.LANCZOS)
im.save(p, dpi=(600, 600), optimize=True)
print('etiquette.png', im.size)
`], { stdio: 'inherit' });
