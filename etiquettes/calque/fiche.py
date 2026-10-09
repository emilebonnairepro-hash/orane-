"""ORANE — style « fiche » (v6) du calque d'étiquette.

Simple, lisible, sans vide : l'identité en tête (orane, petite bouille, numéro, grand nom),
puis toutes les informations essentielles en lignes, dont la taille s'ajuste pour remplir la hauteur.
  produit["fiche"] = [["Pour qui", "..."], ["Ce qu'il fait", "..."], ["Dedans", "..."], ["Parfum", "..."]]
                     (la ligne « Ce qu'il fait » est mise en avant dans un bandeau de couleur)
  produit["geste"] = étapes ; produit["plus"] = atouts (« sans parfum », « certifié COSMOS Natural »…)
S'il y a un panneau côté : le geste et les atouts y vont ; sinon ils restent sur la face avant.
"""
from calque import C, FONCES, BOUILLE, svg_asset, e, geometrie


def page(spec, guides=False, simple=False):
    g, p, t = spec["gabarit"], spec["produit"], spec["theme"]
    G = geometrie(g)
    fond, texte = C[t["fond"]], C[t.get("texte", "aubergine")]
    accent = C[t["accent"]]
    A, CR = C["aubergine"], C["creme"]
    fonce = t["fond"] in FONCES
    bande_nom = t.get("bande") or ("aubergine" if not fonce else ("citron" if t["fond"] != "citron" else "creme"))
    bande = C[bande_nom]
    bande_txt = CR if bande_nom in ("aubergine", "violet") else A
    fx0, fy0, fx1, fy1 = G["front"]
    FW, FH = fx1 - fx0, fy1 - fy0
    u = max(.62, min(FW / 36, FH / 82, 2.2))
    bx0, by0, bx1, by1 = G["bg"]
    side = G["side"]

    def pt(v):
        return f"{max(5.0, v * u):.2f}pt"

    nom_html = "".join(
        f'<span class="ln{" em" if i % 2 else ""}" data-fit data-max="{p.get("taille_max", 40) * u:.1f}">{e(l)}</span>'
        for i, l in enumerate(p["lignes"]))

    # ---------- lignes de la fiche (face avant)
    lignes = list(p.get("fiche", []))
    if not side:
        if p.get("geste"): lignes.append(["Le geste", " · ".join(p["geste"])])
        if p.get("plus"): lignes.append(["En plus", " · ".join(p["plus"])])
    rows = ""
    if simple:
        d = {l[0].lower(): l[1] for l in p.get("fiche", [])}
        claim = next((v for k, v in d.items() if k.startswith("ce qu")), p.get("sous_titre", ""))
        pour = next((v for k, v in d.items() if k.startswith("pour qui")), "")
        claim = claim[:1].upper() + claim[1:] + ("" if claim.endswith(".") else ".")
        rows = f'<p class="claim">{e(claim)}</p>' + (f'<p class="pour">pour {e(pour)}</p>' if pour else "")
        lignes = []
    for lab, val in lignes:
        hl = lab.lower().startswith("ce qu")
        rows += f'<div class="row{" hl" if hl else ""}"><p class="lab">{e(lab)}</p><p class="val">{e(val)}</p></div>'
    badges = "".join(f'<span class="mini">{e(x["grand"])} {e(x.get("petit", ""))}</span>' for x in p.get("badges", []))
    foot = f'<div class="foot"><div class="minis">{badges}</div><b>{e(p.get("volume", ""))}</b></div>'

    # ---------- côté
    side_html = ""
    if side:
        sx0, sy0, sx1, sy1 = side
        blocs = []
        if p.get("geste"):
            steps = "".join(f'<li><b>{i + 1}</b><span>{e(x)}</span></li>' for i, x in enumerate(p["geste"]))
            blocs.append(f'<section><p class="ct">{e(p.get("titre_geste", "Le geste"))}</p><ol class="steps">{steps}</ol></section>')
        if p.get("plus") and not simple:
            plus = "".join(f"<li>{e(x)}</li>" for x in p["plus"])
            blocs.append(f'<section><p class="ct">En plus</p><ul class="plus">{plus}</ul></section>')
        if p.get("pour_qui") and not any(l[0].lower().startswith("pour qui") for l in p.get("fiche", [])):
            blocs.append(f'<section><p class="ct">Pour qui ?</p><p class="txt">{e(p["pour_qui"])}</p></section>')
        bdg = "".join(f'<p class="badge"><span>{e(x["grand"])}<small>{e(x.get("petit", ""))}</small></span></p>' for x in p.get("badges", []))
        logos = "".join(svg_asset(l, "logo") for l in p.get("logos", []))
        side_html = (f'<div class="side" style="left:{sx0}mm;top:{sy0}mm;width:{sx1 - sx0}mm;height:{sy1 - sy0}mm">'
                     f'{"".join(blocs)}{"<div class=badges>" + bdg + logos + "</div>" if (bdg or logos) else ""}</div>')
        foot = f'<div class="foot"><span class="slog">{e(p.get("univers", ""))} · n°{e(p["numero"])}</span><b>{e(p.get("volume", ""))}</b></div>'

    strip_html = ""
    if G["strip"]:
        lx0, ly0, lx1, ly1 = G["strip"]
        strip_html = (f'<p class="slogan" style="left:{(lx0 + lx1) / 2}mm;top:{(ly0 + ly1) / 2}mm;font-size:{min(7, (lx1 - lx0) * 1.2):.2f}pt">'
                      f'{e(p.get("slogan", "peau neuve, mine de rien"))} ✦</p>')

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
body {{ position: relative; color: {texte}; font-family: "Bricolage Grotesque", sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; --f: 1; }}
.fond {{ position: absolute; left: {bx0}mm; top: {by0}mm; width: {bx1 - bx0}mm; height: {by1 - by0}mm; background: {fond}; }}
.trou {{ position: absolute; background: #fff; border-radius: 2mm; }}
.slogan {{ position: absolute; transform: translate(-50%, -50%) rotate(-90deg); white-space: nowrap; font-family: Unbounded, sans-serif; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; }}

/* ----- face avant ----- */
.front {{ position: absolute; left: {fx0}mm; top: {fy0}mm; width: {FW}mm; height: {FH}mm; display: flex; flex-direction: column; }}
.head {{ display: flex; align-items: center; gap: {1.6 * u:.2f}mm; padding-bottom: {1.2 * u:.2f}mm; border-bottom: {.45 * u:.2f}mm solid currentColor; }}
.mark {{ flex: 0 0 40%; width: 40%; min-width: 0; overflow: hidden; font-family: Unbounded, sans-serif; font-weight: 900; letter-spacing: -.055em; line-height: .82; white-space: nowrap; }}
.head .bouille {{ width: {8.5 * u:.2f}mm; flex: none; transform: rotate(8deg); }}
.kick {{ flex: 1; min-width: 0; text-align: right; font-family: Unbounded, sans-serif; font-weight: 700; font-size: {pt(4.8)}; letter-spacing: .12em; text-transform: uppercase; line-height: 1.3; }}
.kick b {{ display: block; font-weight: 900; font-size: {pt(8.5)}; letter-spacing: -.02em; }}
.name {{ display: flex; flex-direction: column; margin-top: {2 * u:.2f}mm; }}
.ln {{ display: block; width: 100%; white-space: nowrap; font-family: Unbounded, sans-serif; font-weight: 900; line-height: .92; letter-spacing: -.045em; }}
.ln.em {{ color: {accent}; -webkit-text-stroke: {.45 * u:.2f}mm {A}; paint-order: stroke fill; }}
.sous {{ font-weight: 800; font-size: calc({max(5.0, 6.8 * u):.2f}pt * min(var(--f), 1.25)); line-height: 1.2; margin-top: {1.2 * u:.2f}mm; }}

.fiche {{ flex: 1; display: flex; flex-direction: column; justify-content: space-between; margin-top: {2.4 * u:.2f}mm; min-height: 0; }}
.row {{ border-top: {.3 * u:.2f}mm solid currentColor; padding-top: calc({.9 * u:.2f}mm * var(--f)); }}
.row:first-child {{ border-top: 0; padding-top: 0; }}
.lab {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: calc({max(4.6, 4.6 * u):.2f}pt * var(--f)); letter-spacing: .14em; text-transform: uppercase; opacity: .8; }}
.val {{ font-weight: 800; font-size: calc({max(5.2, 6.4 * u):.2f}pt * var(--f)); line-height: 1.18; margin-top: calc(.4mm * var(--f)); }}
.row.hl {{ border: 0; background: {bande}; color: {bande_txt}; border-radius: {2.2 * u:.2f}mm; padding: calc({1.2 * u:.2f}mm * var(--f)) calc({2 * u:.2f}mm * var(--f)); }}
.row.hl + .row {{ border-top: 0; }}
.row.hl .lab {{ opacity: .85; }}
.row.hl .val {{ font-family: Unbounded, sans-serif; font-weight: 800; letter-spacing: -.01em; }}
.foot {{ display: flex; justify-content: space-between; align-items: center; gap: 2mm; border-top: {.45 * u:.2f}mm solid currentColor; padding-top: {1.2 * u:.2f}mm; margin-top: {1.4 * u:.2f}mm; }}
.foot b {{ font-family: Unbounded, sans-serif; font-weight: 900; font-size: {max(5.5, 9 * u):.2f}pt; white-space: nowrap; }}
.minis {{ display: flex; flex-wrap: wrap; gap: 1mm; }}
.mini {{ border: {.35 * u:.2f}mm solid currentColor; border-radius: 99mm; padding: .3mm 1.6mm; font-weight: 800; font-size: {max(5.0, 5.4 * u):.2f}pt; white-space: nowrap; }}
.claim {{ overflow-wrap: normal; width: 100%; font-family: Unbounded, sans-serif; font-weight: 800; font-size: calc({max(6, 9 * u):.2f}pt * var(--f)); line-height: 1.08; letter-spacing: -.02em; }}
.pour {{ width: 100%; font-weight: 800; font-size: calc({max(5.5, 6.5 * u):.2f}pt * var(--f)); line-height: 1.2; border-top: {.3 * u:.2f}mm solid currentColor; padding-top: calc({1 * u:.2f}mm * var(--f)); }}
.slog {{ white-space: nowrap; font-family: Unbounded, sans-serif; font-weight: 700; font-size: {max(4.6, 4.8 * u):.2f}pt; letter-spacing: .1em; text-transform: uppercase; }}

/* ----- côté ----- */
.side {{ position: absolute; display: flex; flex-direction: column; justify-content: space-between; }}
.side section {{ border-top: .3mm solid currentColor; padding-top: 1.6mm; }}
.side section:first-child {{ border-top: 0; padding-top: 0; }}
.ct {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 8pt; margin-bottom: 1.4mm; }}
.steps {{ list-style: none; display: grid; gap: 1.2mm; }}
.steps li {{ display: grid; grid-template-columns: 7mm 1fr; align-items: center; gap: 1.6mm; font-weight: 700; font-size: 6.8pt; line-height: 1.2; }}
.steps b {{ font-family: Unbounded, sans-serif; font-weight: 900; font-size: 16pt; line-height: .8; color: {accent}; -webkit-text-stroke: .3mm {A}; paint-order: stroke fill; text-align: center; }}
.plus {{ list-style: none; display: grid; gap: .8mm; }}
.plus li {{ font-weight: 800; font-size: 6.8pt; }}
.plus li::before {{ content: "✦ "; color: {accent}; -webkit-text-stroke: .15mm {A}; }}
.txt {{ font-weight: 700; font-size: 6.8pt; line-height: 1.3; }}
.badges {{ display: flex; align-items: center; gap: 2.6mm; }}
.badge {{ width: 15mm; height: 15mm; flex: none; border-radius: 50%; background: {CR}; color: {A}; border: .5mm solid {A};
  display: grid; place-items: center; text-align: center; font-family: Unbounded, sans-serif; font-weight: 800; font-size: 8pt; line-height: 1; }}
.badge small {{ display: block; font-family: "Bricolage Grotesque", sans-serif; font-weight: 700; font-size: 5pt; margin-top: .5mm; }}
.logo {{ width: 12mm; height: 12mm; background: #fff; border-radius: 50%; flex: none; }}

.gl {{ position: absolute; pointer-events: none; }}
.gz {{ position: absolute; border: .6mm dashed #FF6A2B; background: repeating-linear-gradient(45deg, rgba(255,106,43,.14) 0 2mm, transparent 2mm 4mm); display: grid; place-items: center; }}
.gz span, .gt {{ font: 700 5pt sans-serif; color: #c2410c; background: rgba(255,255,255,.9); padding: .4mm 1mm; text-align: center; }}
.gt {{ position: absolute; left: {G['b'] + 1}mm; bottom: .2mm; }}
</style></head><body>
<div class="fond"></div>
{trous_html}
{strip_html}
<div class="front">
  <div class="head"><p class="mark" data-fit data-max="{26 * u:.1f}">orane</p>{BOUILLE}<p class="kick"><b>n°{e(p['numero'])}</b>{e(p['univers'])}</p></div>
  <div class="name">{nom_html}</div>
  {'<p class="sous">' + e(p['sous_titre']) + '</p>' if p.get('sous_titre') and not p.get('fiche') else ''}
  <div class="fiche">{rows}</div>
  {foot}
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
  const front = document.querySelector('.front'), fiche = document.querySelector('.fiche');
  const foot = document.querySelector('.foot');
  const over = () => front.scrollHeight > front.clientHeight + .5 || fiche.scrollHeight > fiche.clientHeight + .5
    || [...fiche.children].some((c) => c.scrollWidth > fiche.clientWidth + .5);
  // 1. le nom remplit la largeur, sans prendre plus de 36 % de la hauteur
  let k = 1;
  for (let i = 0; i < 16; i++) {{
    document.querySelectorAll('[data-fit]').forEach((el) => fit(el, parseFloat(el.dataset.max) * (el.classList.contains('ln') ? k : 1)));
    if (document.querySelector('.name').getBoundingClientRect().height <= front.clientHeight * .36) break;
    k *= .93;
  }}
  // 2. la fiche grandit jusqu'à remplir toute la hauteur restante (pas de vide)
  let lo = .6, hi = 2.4;
  for (let i = 0; i < 18; i++) {{ const mid = (lo + hi) / 2; document.body.style.setProperty('--f', mid); if (over()) hi = mid; else lo = mid; }}
  document.body.style.setProperty('--f', lo);
  // 3. le côté remplit sa hauteur
  const side = document.querySelector('.side');
  if (side) {{
    const H0 = side.clientHeight, W0 = side.clientWidth;
    const apply = (z) => {{ side.style.transformOrigin = '0 0'; side.style.transform = `scale(${{z}})`; side.style.width = (W0 / z) + 'px'; side.style.height = (H0 / z) + 'px'; }};
    const need = () => [...side.children].reduce((a, c) => a + c.scrollHeight, 0) + 6 * 4;
    let a = .6, b = 1.5;
    for (let i = 0; i < 16; i++) {{ const mid = (a + b) / 2; apply(mid); if (need() > side.clientHeight) b = mid; else a = mid; }}
    apply(a);
  }}
  document.body.dataset.ready = '1';
}}
run();
</script>
</body></html>"""
