// Rend une boîte : boite.html → boite.png (px exacts, fond transparent) + boite.pdf ; apercu.html → apercu.png
// Usage : node rendre-boite.mjs <dossier sortie> <largeur pt> <hauteur pt> <px l> <px h>
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }
const [dir, wpt, hpt, pxw, pxh] = process.argv.slice(2);
const cssW = (+wpt) * 96 / 72, cssH = (+hpt) * 96 / 72;
const b = await chromium.launch();
for (const [nom, scale] of [['boite', +pxw / cssW], ['apercu', 1800 / cssW]]) {
  const p = await b.newPage({ viewport: { width: Math.ceil(cssW), height: Math.ceil(cssH) }, deviceScaleFactor: scale });
  await p.goto('file://' + dir + '/' + nom + '.html');
  await p.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 30000 });
  await p.waitForTimeout(300);
  const err = JSON.parse(await p.evaluate(() => document.body.dataset.erreurs || '[]'));
  if (err.length) { console.error('✗ marges :\n  ' + err.join('\n  ')); process.exitCode = 1; }
  await p.screenshot({ path: dir + '/' + nom + '.png', omitBackground: nom === 'boite', clip: { x: 0, y: 0, width: cssW, height: cssH } });
  if (nom === 'boite') await p.pdf({ path: dir + '/boite.pdf', width: (cssW / 96) + 'in', height: (cssH / 96) + 'in', printBackground: true, pageRanges: '1' });
  console.log('✓', nom);
  await p.close();
}
await b.close();
