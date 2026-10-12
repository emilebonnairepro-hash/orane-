// Maquette 3D d'une boîte montée à partir de boite.png : face avant, côté droit et dessus.
// Usage : node maquette-boite.mjs <dossier sortie> <json faces> [image flacon]
import { createRequire } from 'module';
import fs from 'node:fs';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }
const [dir, facesJson, flacon] = process.argv.slice(2);
const F = JSON.parse(facesJson);           // {plan:[W,H], face:[x0,y0,x1,y1], cote:[..], dessus:[..]} en pt
const S = 2.2;                              // pt → px de la maquette
const img = 'data:image/png;base64,' + fs.readFileSync(dir + '/boite.png').toString('base64');
const fw = (F.face[2] - F.face[0]) * S, fh = (F.face[3] - F.face[1]) * S, d = (F.cote[2] - F.cote[0]) * S;
const crop = (r, w, h, extra = '') => `width:${w}px;height:${h}px;background:url(${img}) no-repeat;background-size:${F.plan[0] * S}px ${F.plan[1] * S}px;background-position:${-r[0] * S}px ${-r[1] * S}px;${extra}`;
const fl = flacon ? `<img src="data:image/png;base64,${fs.readFileSync(flacon).toString('base64')}" style="position:absolute;left:700px;bottom:150px;height:400px;filter:drop-shadow(0 18px 18px rgba(42,18,64,.25))">` : '';
const html = `<!doctype html><html><body style="margin:0;width:1200px;height:1200px;background:radial-gradient(circle at 50% 38%,#FFF3E3,#F4DCC8);overflow:hidden;position:relative">
<div style="position:absolute;left:330px;bottom:150px;width:${fw}px;height:${fh}px;perspective:2200px">
 <div style="position:absolute;inset:0;transform-style:preserve-3d;transform:rotateX(-24deg) rotateY(-34deg)">
  <div style="position:absolute;left:0;top:0;${crop(F.face, fw, fh)};transform:translateZ(${d / 2}px)"></div>
  <div style="position:absolute;left:${fw / 2 - d / 2}px;top:0;${crop(F.cote, d, fh, 'filter:brightness(.86);')};transform:rotateY(90deg) translateZ(${fw / 2}px)"></div>
  <div style="position:absolute;left:0;top:${fh / 2 - d / 2}px;${crop(F.dessus, fw, d, 'filter:brightness(1.05);')};transform:rotateX(90deg) translateZ(${fh / 2}px)"></div>
 </div></div>
<div style="position:absolute;left:250px;right:330px;bottom:118px;height:60px;border-radius:50%;background:rgba(42,18,64,.18);filter:blur(16px)"></div>
${fl}</body></html>`;
fs.writeFileSync(dir + '/maquette.html', html);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1200, height: 1200 } });
await p.goto('file://' + dir + '/maquette.html'); await p.waitForTimeout(400);
await p.screenshot({ path: dir + '/maquette.png' }); await b.close();
console.log('✓ maquette');
