// Aperçu local : rend les sections ORANE (vrai Liquid) avec des données factices
// proches de la boutique, et écrit la page d'accueil dans ../../index.html.
// Usage : npm i liquidjs@10 && node shopify/preview/render.mjs
import { Liquid, Tag } from 'liquidjs';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const engine = new Liquid({ root: [path.join(root, 'sections'), path.join(root, 'snippets')], extname: '.liquid', globals: { cart: { total_price: 1340 } } });

engine.registerTag('schema', class extends Tag {
  constructor(token, remain, liquid, parser) {
    super(token, remain, liquid);
    const stream = parser.parseStream(remain);
    stream.on('tag:endschema', () => stream.stop()).on('template', () => {}).on('end', () => { throw new Error('schema non fermé'); });
    stream.start();
  }
  * render() {}
});
engine.registerFilter('image_url', (img) => img?.src ?? img);
engine.registerFilter('image_tag', (src, ...args) => {
  const o = Object.fromEntries(args.filter(Array.isArray));
  return `<img src="${src}"${o.class ? ` class="${o.class}"` : ''} alt="${o.alt ?? ''}" loading="${o.loading ?? 'lazy'}">`;
});
engine.registerFilter('money', (c) => `${(c / 100).toFixed(2).replace('.', ',')} €`);
engine.registerFilter('asset_url', (f) => `shopify/assets/${f}`);
engine.registerFilter('stylesheet_tag', (u) => `<link rel="stylesheet" href="${u}">`);

const tones = ['#ffffff'];
const photo = (label, color) => 'data:image/svg+xml,' + encodeURIComponent(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"><rect width="400" height="400" fill="#fff"/><rect x="150" y="70" width="100" height="50" rx="10" fill="#2A1240"/><rect x="120" y="110" width="160" height="230" rx="40" fill="${color}" stroke="#2A1240" stroke-width="6"/><text x="200" y="235" font-family="sans-serif" font-weight="800" font-size="30" text-anchor="middle" fill="#2A1240">${label}</text></svg>`);
const P = (handle, title, price, tags, desc, color) => ({
  handle, title, price, tags, description: desc, url: `/products/${handle}`, available: true,
  featured_image: { src: photo('orane', color), alt: title }, selected_or_first_available_variant: { id: 1 },
});
const products = {
  'gel-lavant-mains-corps-pamplemousse': P('gel-lavant-mains-corps-pamplemousse', 'Gel lavant mains & corps, pamplemousse', 830, ['Gel douche (Type)'], 'Frais, doux, et un parfum de pamplemousse. Un gel lavant pour les mains et le corps qui nettoie sans dessécher et laisse la peau fraîche.', '#D4F23A'),
  'shampooing-pour-cuir-chevelu-sensible': P('shampooing-pour-cuir-chevelu-sensible', 'Shampooing pour cuir chevelu sensible', 1120, ['Shampooings (Type)'], "La douceur qu'il faut aux cuirs chevelus sensibles. Doux mais efficace, ce shampooing prend soin des peaux sèches et sensibles.", '#FFF3E3'),
  'huile-a-barbe-adoucissante': P('huile-a-barbe-adoucissante', 'Huile à barbe adoucissante', 1110, ['Huiles pour le visage (Type)'], "Une barbe plus douce, sans effet gras. Un mélange d'huiles naturelles de première qualité, dans une formule non grasse.", '#FF6A2B'),
  'demaquillant-biphasic-sans-parfum-1': P('demaquillant-biphasic-sans-parfum-1', 'Démaquillant BiPhasic, sans parfum', 630, ['Nettoyant (Type)'], 'Une double action, un seul geste. Une phase huileuse, une phase aqueuse : ce démaquillant biphasé fait disparaître le maquillage.', '#2CC8F5'),
  'gel-visage-au-zinc-sans-huile-pour-hommes': P('gel-visage-au-zinc-sans-huile-pour-hommes', 'Gel visage au zinc sans huile pour hommes', 900, ['Hydratant (Type)'], 'Hydratation instantanée, zéro effet gras. Ce gel hydratant sans huile se glisse dans la routine en un geste.', '#FF5FA8'),
  'patchs-hydrogel-energisants-pour-les-yeux-a-la-cafeine-et-a-la-vitamine-c': P('patchs-hydrogel-energisants-pour-les-yeux-a-la-cafeine-et-a-la-vitamine-c', 'Patchs hydrogel énergisants pour les yeux', 1340, ['Patches (Type)'], 'Un petit moment rien que pour ton regard. Frais et légers, ces patchs hydrogel inspirés de la K-beauty apaisent et revitalisent.', '#FFF3E3'),
};
const all = { url: '/collections/all', products: Object.values(products) };
const real = JSON.parse(fs.readFileSync(path.join(here, 'products.json'), 'utf8'));
for (const r of real) Object.assign(products[r.handle], { description: r.descriptionHtml, tags: r.tags, id: r.id });

const readJson = (f) => { const t = fs.readFileSync(path.join(root, f), 'utf8'); return JSON.parse(t.slice(t.indexOf('{\n'))); };
const tpl = process.argv[2] || 'index';
const out = process.argv[3] || path.resolve(root, '..', 'index.html');
const index = readJson(`templates/${tpl}.json`);
const extra = { collection: tpl === 'collection' ? { title: 'Soin du visage', handle: 'soin-du-visage', products_count: 4, description: '<p>Nettoyer, réveiller, hydrater : la routine visage, sans prise de tête.</p>' } : null,
  page: tpl.startsWith('page') ? { title: 'Contact', handle: 'contact' } : null, page_title: tpl === 'cart' ? 'Panier' : '404',
  product: tpl === 'product' ? products[process.argv[4] || 'patchs-hydrogel-energisants-pour-les-yeux-a-la-cafeine-et-a-la-vitamine-c'] : null,
  all_products: products, cart: { total_price: 1340 } };
if (extra.product) extra.product.selected_or_first_available_variant.price = extra.product.price;

const resolve = (v) => (typeof v === 'string' && products[v]) ? products[v] : (v === 'all' ? all : v);
let html = '';
for (const id of index.order) {
  const s = index.sections[id];
  const ctxBase = { ...extra, shop: { name: 'ORANE', email: 'emilebonnairepro@gmail.com' }, routes: { root_url: '/', all_products_collection_url: '/collections/all', cart_add_url: '#panier' }, collections: { all } };
  if (s.type === 'custom-liquid') { html += await engine.parseAndRender(s.settings.custom_liquid, ctxBase); continue; }
  if (s.type === 'main-product') { html += await engine.parseAndRender(fs.readFileSync(path.join(here, 'mock-main-product.liquid'), 'utf8'), ctxBase); continue; }
  if (!s.type.startsWith('orane-')) { html += `<div class="dawn-placeholder">Section existante du thème : ${s.type}${s.settings?.title ? ` — « ${s.settings.title} »` : ''}</div>`; continue; }
  const settings = Object.fromEntries(Object.entries(s.settings ?? {}).map(([k, v]) => [k, resolve(v)]));
  const blocks = (s.block_order ?? []).map((bid) => ({ id: bid, shopify_attributes: '', settings: Object.fromEntries(Object.entries(s.blocks[bid].settings).map(([k, v]) => [k, resolve(v)])) }));
  html += await engine.renderFile(s.type, {
    ...extra, section: { id, settings, blocks }, shop: { name: 'ORANE', email: 'emilebonnairepro@gmail.com' },
    routes: { root_url: '/', all_products_collection_url: '/collections/all', cart_add_url: '#panier' }, collections: { all },
  });
}

const page = `<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ORANE — peau neuve, mine de rien.</title>
<meta name="description" content="Aperçu de la page d'accueil ORANE, rendu à partir des sections Liquid du thème Shopify.">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600&family=Unbounded:wght@700;800&display=swap" rel="stylesheet">
<style>
  /* Base façon Dawn, uniquement pour l'aperçu */
  :root { --font-heading-family: "Unbounded", sans-serif; --font-body-family: "Bricolage Grotesque", sans-serif; }
  *, *::before, *::after { box-sizing: border-box; }
  html { font-size: 62.5%; }
  body { margin: 0; font-family: var(--font-body-family); font-size: 1.8rem; line-height: 1.5; background: #FFF3E3; color: #2A1240; overflow-x: hidden; }
  .visually-hidden { position: absolute !important; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
  .demo-bar { background: #6B2CF5; color: #FFF3E3; text-align: center; font: 700 1.3rem/1 var(--font-heading-family); padding: 1.2rem; letter-spacing: .04em; }
  .demo-header { display: flex; align-items: center; justify-content: space-between; padding: 1.6rem clamp(1.6rem, 4vw, 5rem); border-bottom: 3px solid #2A1240; font: 800 2.6rem var(--font-heading-family); }
  .demo-header nav { font: 600 1.6rem var(--font-body-family); display: flex; gap: 2.4rem; }
  @media (max-width: 749px) { .demo-header nav span:not(:last-child) { display: none; } }
  .dawn-placeholder { padding: 3rem; text-align: center; font: 600 1.4rem var(--font-body-family); background: repeating-linear-gradient(45deg, #fff3e3, #fff3e3 12px, #f6e6cf 12px, #f6e6cf 24px); border-block: 2px dashed #2A1240; }
</style>
<link rel="stylesheet" href="shopify/assets/orane-brand.css">
</head>
<body>
<div class="demo-bar">Livraison offerte dès 50€ d'achat</div>
<header class="demo-header"><span>orane</span><nav><span>Visage</span><span>Corps</span><span>Cheveux</span><span>Homme</span><span>Panier (0)</span></nav></header>
<main>
${html}
</main>
<script>
  // Aperçu seulement : pas de vrai panier
  document.addEventListener('submit', (e) => { const f = e.target.closest('.o-prod__form'); if (!f) return; e.preventDefault(); const b = f.querySelector('.o-add'); b.textContent = 'dans le panier ✦'; b.classList.add('is-added'); });
</script>
<script src="shopify/assets/orane.js" defer></script>
</body>
</html>
`;
fs.writeFileSync(out, tpl === 'index' ? page : page.replaceAll('shopify/assets/', path.relative(path.dirname(out), path.join(root, 'assets')) + '/'));
console.log(`${tpl} → ${out}`);
