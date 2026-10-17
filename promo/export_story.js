// Exporte story_bienvenue.html en PNG haute définition.
// Usage : node export_story.js [échelle]   (2 → 2160x3840, 3 → 3240x5760)
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const scale = Number(process.argv[2] || 2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: scale });
  await page.goto("file://" + path.join(__dirname, "story_bienvenue.html"));
  await page.evaluate(() => document.fonts.ready);
  const out = path.join(__dirname, `story_bienvenue10_${1080 * scale}x${1920 * scale}.png`);
  await page.screenshot({ path: out });
  await browser.close();
  console.log("ok", out);
})();
