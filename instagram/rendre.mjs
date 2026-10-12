// Rend chaque post en PNG 1080 × 1350.
import { createRequire } from 'module';
import fs from 'node:fs';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = createRequire('/opt/node22/lib/node_modules/')('playwright')); }
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const b = await chromium.launch();
for (const j of jobs) {
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  await p.goto('file://' + j.html);
  await p.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 20000 });
  await p.waitForTimeout(200);
  await p.screenshot({ path: j.png });
  console.log('✓', j.png.split('/').pop());
  await p.close();
}
await b.close();
