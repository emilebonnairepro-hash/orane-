"""ORANE — style « signature » (v4) du calque d'étiquette.

Plus riche que l'épuré, plus rangé que le plein : la richesse vient de la composition.
  Face avant : « orane » + numéro, le nom en très grand, puis une fenêtre crème dont la bouille déborde,
               dans un médaillon entouré d'un texte circulaire (comme le bouton tournant du site),
               deux pastilles et le volume posés dans la fenêtre.
  Côté       : le geste avec de grands chiffres en contour, « dedans » en pastilles, pour qui,
               séparés par de fines lignes et une étincelle ; pastille et logo en bas.
Même géométrie et mêmes fichiers produits que les autres styles (voir calque.py).
"""
from calque import C, FONCES, BOUILLE, anneau, spark, svg_asset, e, geometrie


def page(spec, guides=False, leger=False):
    g, p, t = spec["gabarit"], spec["produit"], spec["theme"]
    G = geometrie(g)
    fond, texte = C[t["fond"]], C[t.get("texte", "aubergine")]
    accent = C[t["accent"]]
    A, CR = C["aubergine"], C["creme"]
    fonce = t["fond"] in FONCES
    # médaillon : une couleur vive différente du fond (violet sinon rose) ; texte du cercle lisible selon la charte
    halo_nom = t.get("halo") or ("violet" if t["fond"] != "violet" else "rose")
    halo = C[halo_nom]
    halo_txt = CR if halo_nom in ("violet", "aubergine") else A
    pills = [C[c] for c in t.get("pastilles", ["creme", "citron", "rose"])]
    fx0, fy0, fx1, fy1 = G["front"]
    FW, FH = fx1 - fx0, fy1 - fy0
    u = max(.62, min(FW / 36, FH / 82, 2.2))
    bx0, by0, bx1, by1 = G["bg"]

    def pt(v):
        return f"{max(5.0, v * u):.2f}pt"

    lignes = p["lignes"]
    nom_html = "".join(
        f'<span class="ln{" em" if i % 2 else ""}" data-fit data-max="{p.get("taille_max", 40) * u:.1f}">{e(l)}</span>'
        for i, l in enumerate(lignes))
    two = p.get("pastilles", [])[:1 if leger else 2]
    pills_html = "".join(
        f'<span class="pill" style="--bg:{pills[i % len(pills)]};--fg:{CR if pills[i % len(pills)] in (C["violet"], A) else A};--r:{[-5, 4][i % 2]}deg">{e(x)}</span>'
        for i, x in enumerate(two))
    cercle = p.get("cercle") or " ✦ ".join([p.get("bulle", "").rstrip(" !"), *p.get("pastilles", [])[2:3], "peau neuve, mine de rien"])

    # ---------- côté
    side_html = ""
    if G["side"]:
        sx0, sy0, sx1, sy1 = G["side"]
        blocs = []
        if p.get("geste"):
            steps = "".join(f'<li><b>{i + 1}</b><span>{e(x)}</span></li>' for i, x in enumerate(p["geste"]))
            blocs.append(f'<section><p class="ct">{e(p.get("titre_geste", "Le geste"))}</p><ol class="steps">{steps}</ol></section>')
        if p.get("dedans") and leger:
            blocs.append(f'<section><p class="ct">{e(p.get("titre_dedans", "Dedans"))}</p><p class="txt">{e(" · ".join(p["dedans"]))}.'
                         f'{(" " + e(p["parfum"])) if p.get("parfum") else ""}</p></section>')
        elif p.get("dedans"):
            chips = "".join(f'<span class="chip">{e(x)}</span>' for x in p["dedans"])
            blocs.append(f'<section><p class="ct">{e(p.get("titre_dedans", "Dedans"))}</p><div class="chips">{chips}</div>'
                         f'{"<p class=note>" + e(p["parfum"]) + "</p>" if p.get("parfum") else ""}</section>')
        if p.get("pour_qui") and not leger:
            blocs.append(f'<section><p class="ct">Pour qui ?</p><p class="txt">{e(p["pour_qui"])}</p></section>')
        badges = "".join(f'<p class="badge"><span>{e(x["grand"])}<small>{e(x.get("petit", ""))}</small></span></p>' for x in p.get("badges", []))
        logos = "".join(svg_asset(l, "logo") for l in p.get("logos", []))
        sep = '<div class="sep sep--fin"></div>' if leger else f'<div class="sep">{spark("", accent if not fonce else C["citron"]).replace('class="sp "', 'class="sepsp"')}</div>'
        corps = sep.join(blocs)
        side_html = (f'<div class="side" style="left:{sx0}mm;top:{sy0}mm;width:{sx1 - sx0}mm;height:{sy1 - sy0}mm">'
                     f'<div class="side-in">{corps}</div>{"<div class=badges>" + badges + logos + "</div>" if (badges or logos) else ""}</div>')

    strip_html = ""
    if G["strip"]:
        lx0, ly0, lx1, ly1 = G["strip"]
        strip_html = (f'<p class="slogan" style="left:{(lx0 + lx1) / 2}mm;top:{(ly0 + ly1) / 2}mm;font-size:{min(7, (lx1 - lx0) * 1.2):.2f}pt">'
                      f'{e(p.get("slogan", "peau neuve, mine de rien"))} ✦</p>'
                      f'{spark("", CR if t["fond"] != "creme" else C["citron"]).replace("class=\"sp \"", "class=\"sp\" style=\"width:5.5mm;left:" + str((lx0 + lx1) / 2 - 2.75) + "mm;top:" + str(ly0 + 2) + "mm\"")}')

    trous_html = "".join(f'<div class="trou" style="left:{x0}mm;top:{y0}mm;width:{x1 - x0}mm;height:{y1 - y0}mm"></div>' for x0, y0, x1, y1 in G["trous"])

    guides_html = ""
    if guides:
        b = G["b"]
        zs = "".join(f'<div class="gz" style="left:{z["x"]}mm;top:{z["y"]}mm;width:{z["l"]}mm;height:{z["h"]}mm"><span>mentions obligatoires<br>(Selfnamed)</span></div>'
                     for z in g.get("zones_vides", []))
        guides_html = (f'<div class="gl" style="inset:{b}mm;border:.3mm solid #2a6cff"></div>'
                       f'<div class="gl" style="inset:{b + G["m"]}mm;border:.25mm dashed #2a6cff;opacity:.6"></div>'
                       f'<div class="gl" style="left:{fx0}mm;width:{FW}mm;top:0;bottom:0;border-inline:.3mm dashed #777"></div>'
                       f'{zs}<p class="gt">bleu : coupe · pointillés : marge · gris : face avant · orange : laissé vide</p>')

    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Unbounded:wght@700;800;900&display=block" rel="stylesheet">
<style>
@page {{ size: {G['W']}mm {G['H']}mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {G['W']}mm; height: {G['H']}mm; overflow: hidden; background: transparent; }}
body {{ position: relative; color: {texte}; font-family: "Bricolage Grotesque", sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.fond {{ position: absolute; left: {bx0}mm; top: {by0}mm; width: {bx1 - bx0}mm; height: {by1 - by0}mm; background: {fond}; overflow: hidden; }}
.trou {{ position: absolute; background: #fff; border-radius: 2mm; }}
.sp {{ position: absolute; }}
.slogan {{ position: absolute; transform: translate(-50%, -50%) rotate(-90deg); white-space: nowrap; font-family: Unbounded, sans-serif; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; }}

/* ----- face avant ----- */
.front {{ position: absolute; left: {fx0}mm; top: {fy0}mm; width: {FW}mm; height: {FH}mm; display: flex; flex-direction: column; }}
.head {{ display: flex; align-items: flex-end; justify-content: space-between; gap: {2 * u:.2f}mm; padding-bottom: {1.2 * u:.2f}mm; border-bottom: {.45 * u:.2f}mm solid currentColor; }}
.mark {{ flex: 0 0 60%; width: 60%; min-width: 0; overflow: hidden; font-family: Unbounded, sans-serif; font-weight: 900; letter-spacing: -.055em; line-height: .82; white-space: nowrap; }}
.kick {{ flex: 1; min-width: 0; text-align: right; font-family: Unbounded, sans-serif; font-weight: 700; font-size: {pt(5)}; letter-spacing: .14em; text-transform: uppercase; line-height: 1.35; }}
.kick b {{ display: block; font-weight: 900; font-size: {pt(9)}; letter-spacing: -.02em; }}
.name {{ display: flex; flex-direction: column; margin-top: {2.2 * u:.2f}mm; }}
.ln {{ display: block; width: 100%; white-space: nowrap; font-family: Unbounded, sans-serif; font-weight: 900; line-height: .92; letter-spacing: -.045em; }}
.ln.em {{ color: {accent}; -webkit-text-stroke: {.5 * u:.2f}mm {A}; paint-order: stroke fill; }}
.sous {{ font-weight: 800; font-size: {pt(6.8)}; line-height: 1.2; margin-top: {1.2 * u:.2f}mm; }}

.win {{ position: relative; flex: 1; min-height: {22 * u:.2f}mm; margin-top: {2.6 * u:.2f}mm; container-type: size; display: flex; flex-direction: column; align-items: center; }}
.win-bg {{ position: absolute; left: 0; right: 0; bottom: 0; top: calc(min(86cqw, 66cqh) * .42); background: {CR}; color: {A};
  border: {.55 * u:.2f}mm solid {A}; border-radius: {5 * u:.2f}mm; box-shadow: {1.1 * u:.2f}mm {1.1 * u:.2f}mm 0 {A}; }}
.halo {{ position: relative; flex: none; width: min(86cqw, 66cqh); aspect-ratio: 1; }}
.halo svg.cercle {{ position: absolute; inset: 0; width: 100%; height: 100%; animation: none; }}
.halo .bouille {{ position: absolute; width: {68 if leger else 56}%; left: {16 if leger else 22}%; top: {15 if leger else 21}%; transform: rotate(8deg); }}
.halo .sp {{ width: 16%; right: -6%; top: 2%; }}
.win-foot {{ position: relative; flex: 1; align-self: stretch; padding: {1.6 * u:.2f}mm {2.4 * u:.2f}mm {2 * u:.2f}mm; color: {A}; display: flex; flex-direction: column; justify-content: space-between; gap: {1.6 * u:.2f}mm; align-items: center; }}
.pills {{ display: flex; flex-wrap: wrap; justify-content: center; gap: {1.2 * u:.2f}mm; }}
.pill {{ background: var(--bg); color: var(--fg); border: {.45 * u:.2f}mm solid {A}; border-radius: 99mm; padding: {.7 * u:.2f}mm {2.2 * u:.2f}mm;
  font-family: Unbounded, sans-serif; font-weight: 700; font-size: {pt(5.8)}; white-space: nowrap; transform: rotate(var(--r)); box-shadow: {.55 * u:.2f}mm {.55 * u:.2f}mm 0 {A}; }}
.acc {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: {pt(6.4)}; line-height: 1.15; text-align: center; letter-spacing: -.01em; max-width: 92%; }}
{'.win-foot {{ justify-content: flex-start; gap: ' + format(2.6 * u, '.2f') + 'mm; }} .win-foot .acc {{ margin: auto 0; font-size: ' + format(max(5.0, 7.2 * u), '.2f') + 'pt; font-weight: 700; }}' if leger else ''}
.vol {{ align-self: stretch; display: flex; justify-content: space-between; align-items: baseline; border-top: {.3 * u:.2f}mm dashed {A}; padding-top: {1 * u:.2f}mm; }}
.vol span {{ font-weight: 700; font-size: {pt(5.2)}; }}
.vol b {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: {pt(6.4)}; white-space: nowrap; }}

/* ----- côté ----- */
.side {{ position: absolute; display: flex; flex-direction: column; }}
.side-in {{ display: flex; flex-direction: column; gap: {4 if leger else 2.2}mm; }}
.ct {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 8pt; letter-spacing: -.01em; margin-bottom: 1.6mm; }}
.steps {{ list-style: none; display: grid; gap: 1.4mm; }}
.steps li {{ display: grid; grid-template-columns: 7mm 1fr; align-items: center; gap: 1.6mm; font-weight: 700; font-size: 6.6pt; line-height: 1.2; }}
.steps b {{ font-family: Unbounded, sans-serif; font-weight: 900; font-size: 17pt; line-height: .8; color: transparent; -webkit-text-stroke: .35mm {texte}; text-align: center; }}
.steps li:nth-child(2) b {{ color: {accent}; -webkit-text-stroke: .35mm {A}; paint-order: stroke fill; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 1.2mm; }}
.chip {{ border: .4mm solid currentColor; border-radius: 99mm; padding: .5mm 2mm; font-weight: 700; font-size: 6.4pt; }}
.note {{ font-weight: 600; font-size: 6.2pt; margin-top: 1.4mm; }}
.txt {{ font-weight: 600; font-size: 6.6pt; line-height: 1.32; }}
.sep {{ display: flex; align-items: center; gap: 2mm; }}
.sep::before, .sep::after {{ content: ""; flex: 1; border-top: .3mm solid currentColor; opacity: .5; }}
.sep--fin {{ border-top: .3mm solid currentColor; opacity: .35; }}
.sep--fin::before, .sep--fin::after {{ display: none; }}
.sepsp {{ width: 3.6mm; height: 3.6mm; flex: none; }}
.badges {{ display: flex; align-items: center; gap: 2.6mm; margin-top: auto; padding-top: 2mm; }}
.badge {{ width: 15mm; height: 15mm; flex: none; border-radius: 50%; background: {CR}; color: {A}; border: .5mm solid {A}; box-shadow: .8mm .8mm 0 {A};
  display: grid; place-items: center; text-align: center; font-family: Unbounded, sans-serif; font-weight: 800; font-size: 8pt; line-height: 1; transform: rotate(8deg); }}
.badge small {{ display: block; font-family: "Bricolage Grotesque", sans-serif; font-weight: 700; font-size: 5pt; margin-top: .5mm; }}
.logo {{ width: 12mm; height: 12mm; background: #fff; border-radius: 50%; flex: none; }}

/* ----- repères (aperçu seulement) ----- */
.gl {{ position: absolute; pointer-events: none; }}
.gz {{ position: absolute; border: .6mm dashed #FF6A2B; background: repeating-linear-gradient(45deg, rgba(255,106,43,.14) 0 2mm, transparent 2mm 4mm); display: grid; place-items: center; }}
.gz span, .gt {{ font: 700 5pt sans-serif; color: #c2410c; background: rgba(255,255,255,.9); padding: .4mm 1mm; text-align: center; }}
.gt {{ position: absolute; left: {G['b'] + 1}mm; bottom: .2mm; }}
</style></head><body>
<div class="fond"></div>
{trous_html}
{strip_html}
<div class="front">
  <div class="head"><p class="mark" data-fit data-max="{30 * u:.1f}">orane</p><p class="kick"><b>n°{e(p['numero'])}</b>{e(p['univers'])}</p></div>
  <div class="name">{nom_html}</div>
  {'<p class="sous">' + e(p['sous_titre']) + '</p>' if p.get('sous_titre') else ''}
  <div class="win">
    <div class="win-bg"></div>
    <div class="halo">
      <svg class="cercle" viewBox="0 0 200 200">
        <defs><path id="c" d="M100 100 m-76 0 a76 76 0 1 1 152 0 a76 76 0 1 1 -152 0"/></defs>
        <circle cx="100" cy="100" r="97" fill="{halo}" stroke="{A}" stroke-width="4"/>
        <circle cx="100" cy="100" r="{80 if leger else 60}" fill="{CR}" stroke="{A}" stroke-width="3"/>
        {'' if leger else ''}<text {'display="none"' if leger else ''} font-family="Unbounded, sans-serif" font-weight="800" font-size="15.5" letter-spacing="1.2" fill="{halo_txt}"><textPath href="#c" textLength="470" lengthAdjust="spacingAndGlyphs">{e(cercle)} ✦ </textPath></text>
      </svg>
      {BOUILLE}
      {spark('', C['citron'] if t['fond'] != 'citron' else CR)}
    </div>
    <div class="win-foot">
      <div class="pills">{pills_html}</div>
      {'<p class="acc">' + e(p['accroche']) + '</p>' if p.get('accroche') else ''}
      <div class="vol"><span>{'' if leger else e(p.get('pied', ''))}</span><b>{e(p.get('volume', ''))}</b></div>
    </div>
  </div>
</div>
{side_html}
{guides_html}
<script>
function fit(el, max) {{
  let lo = 4, hi = max;
  for (let i = 0; i < 18; i++) {{ const mid = (lo + hi) / 2; el.style.fontSize = mid + 'pt'; if (el.scrollWidth > el.clientWidth + .5) hi = mid; else lo = mid; }}
  el.style.fontSize = lo + 'pt';
}}
async function run() {{
  await document.fonts.ready;
  const front = document.querySelector('.front'), win = document.querySelector('.win');
  let k = 1;
  for (let pass = 0; pass < 14; pass++) {{
    document.querySelectorAll('[data-fit]').forEach((el) => fit(el, parseFloat(el.dataset.max) * (el.classList.contains('ln') ? k : 1)));
    const over = () => front.scrollHeight > front.clientHeight + .5 || win.scrollHeight > win.clientHeight + .5;
    if (!over() && win.getBoundingClientRect().height >= front.clientHeight * .34) break;
    // petits formats : on retire d'abord l'accroche, puis la 2e pastille, et seulement ensuite on réduit le nom
    const acc = document.querySelector('.acc'), pill2 = document.querySelectorAll('.pill')[1];
    if (acc && acc.style.display !== 'none') {{ acc.style.display = 'none'; continue; }}
    if (pill2 && pill2.style.display !== 'none') {{ pill2.style.display = 'none'; continue; }}
    k *= .92;
  }}
  const side = document.querySelector('.side');
  if (side) {{
    const H0 = side.clientHeight, W0 = side.clientWidth;
    const apply = (z) => {{ side.style.transformOrigin = '0 0'; side.style.transform = `scale(${{z}})`; side.style.width = (W0 / z) + 'px'; side.style.height = (H0 / z) + 'px'; }};
    const inner = () => side.querySelector('.side-in').scrollHeight + (side.querySelector('.badges')?.scrollHeight || 0) + 8;
    let lo = .6, hi = {1.12 if leger else 1.3};
    for (let i = 0; i < 16; i++) {{ const mid = (lo + hi) / 2; apply(mid); if (inner() > side.clientHeight) hi = mid; else lo = mid; }}
    apply(lo * .97);
  }}
  document.body.dataset.ready = '1';
}}
run();
</script>
</body></html>"""
