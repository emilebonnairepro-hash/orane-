"""ORANE — le style V1 (retenu), en moteur réutilisable pour tous les produits et tous les gabarits Selfnamed.

Même dessin que la V1 du gel nettoyant : face avant centrée (n° · catégorie, « orane », la bouille, le nom,
le sous-titre, un sticker, le volume), côté en texte (titres + paragraphes), pastille et logo,
slogan vertical à gauche, anneau et étincelles. La couleur de fond suit la catégorie (etiquettes/couleurs.py).
Les tailles sont recalculées pour remplir chaque gabarit (texte jamais sous 4,6 pt, la bouille rétrécit d'abord).

Usage :  python3 etiquettes/v1/v1.py            → tous les produits de etiquettes/v1/produits/
         python3 etiquettes/v1/v1.py 08          → un seul
Sorties : etiquettes/v1/sortie/<produit>/etiquette.png (à téléverser), etiquette.pdf, apercu.png

Produit (JSON) :
  "gabarit": { "largeur", "hauteur", "fond_perdu", "marge", "zones_vides": [{x,y,l,h}], "face": {cx, largeur}, "px": [l, h] }
  "produit": { "numero", "univers", "nom": ["ligne 1", "ligne 2"], "sous_titre", "sticker", "volume",
               "grand_badge" (facultatif, ex. « SPF 30 »),
               "cote": [["Titre", "texte"], ...]   ← sections du côté, dans l'ordre (les dernières sautent si ça ne tient pas)
               "pastille": {"grand": "98 %", "petit": "d'origine naturelle"}, "logos": ["fichier.svg"] }
"""
import json, pathlib, re, subprocess, sys, html as h

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent))
sys.path.insert(0, str(ICI.parent / "calque"))
from couleurs import C, palette, texte_sur, couleur_motif  # noqa: E402
from urllib.parse import quote


def swirl(couleur):
    """Les formes exactes du modèle (etiquettes/assets/swirl-modele.svg), recolorées."""
    svg = (ICI.parent / "assets" / "swirl-modele.svg").read_text(encoding="utf-8").replace("#B8ADFF", couleur)
    return "data:image/svg+xml," + quote(svg)
from calque import geometrie, BOUILLE               # noqa: E402

A, CR = C["aubergine"], C["creme"]


def e(t):
    # typographie française : espace insécable avant % ? ! :
    t = str(t)
    for c in "%?!:":
        t = t.replace(" " + c, "\u00a0" + c)
    return h.escape(t)


def anneau(a, b):
    return (f'<svg viewBox="0 0 100 100" class="anneau"><path d="M10 50 A40 40 0 0 1 90 50" fill="none" stroke="{a}" stroke-width="18"/>'
            f'<path d="M90 50 A40 40 0 0 1 10 50" fill="none" stroke="{b}" stroke-width="18"/>'
            f'<circle cx="78.3" cy="21.7" r="10" fill="{CR}" stroke="{A}" stroke-width="2"/></svg>')


def spark(style, fill):
    return (f'<svg viewBox="0 0 40 40" class="sp" style="{style}"><path d="M20 2 C22 14 26 18 38 20 C26 22 22 26 20 38 C18 26 14 22 2 20 '
            f'C14 18 18 14 20 2 Z" fill="{fill}" stroke="{A}" stroke-width="2.5" stroke-linejoin="round"/></svg>')


def logo(nom):
    f = ICI / "assets" / nom
    if not f.exists():
        f = ICI.parent / "calque" / "assets" / nom
    s = f.read_text(encoding="utf-8")
    s = re.sub(r"<\?xml.*?\?>|<!--.*?-->|<!DOCTYPE.*?\]>", "", s, flags=re.S)
    return s.replace("<svg ", '<svg class="logo" ', 1)


def page(spec, guides=False):
    g, p = spec["gabarit"], spec["produit"]
    G = geometrie(g)
    P = palette(p["univers"])
    FOND, TEXTE = C[P["fond"]], C[P["texte"]]
    if p.get("couleurs_modele"):          # couleurs exactes du modèle (menthe + lavande) : texte aubergine partout
        TEXTE = C["aubergine"]
    fx0, fy0, fx1, fy1 = G["front"]
    FW, FH = fx1 - fx0, fy1 - fy0
    bx0, by0, bx1, by1 = G["bg"]
    H = G["H"]
    s = min(FW / 32, 1.15)                     # échelle de base (32 mm de large = V1 d'origine)

    nom = "<br>".join(e(x) for x in p["nom"])
    badge = f'<p class="gbadge">{e(p["grand_badge"]).replace(" ", chr(10))}</p>' if p.get("grand_badge") else ""
    front = f"""<div class="front" style="left:{fx0}mm;top:{fy0}mm;width:{FW}mm;height:{FH}mm">
    <p class="kicker">n°{e(p['numero'])} · {e(p['univers'])}</p>
    <p class="marque">orane</p>
    <div class="art">{BOUILLE}{badge}</div>
    <p class="nom">{nom}</p>
    {'<p class="sous">' + e(p['sous_titre']) + '</p>' if p.get('sous_titre') else ''}
    {'<p class="sticker' + (' fort' if p.get('sticker_fort') else '') + '">' + e(p['sticker']) + '</p>' if p.get('sticker') else ''}
    {'<p class="volume">' + e(p['volume']) + '</p>' if p.get('volume') else ''}
  </div>"""

    side2 = None
    if (G["strip"] and G["strip"][2] - G["strip"][0] >= 20 and G["side"]
            and G["strip"][2] - G["strip"][0] >= .6 * (G["side"][2] - G["side"][0])):   # 2e côté seulement si les deux sont comparables
        side2, G["strip"] = G["strip"], None
    side = ""
    if G["side"]:
        sx0, sy0, sx1, sy1 = G["side"]
        secs = "".join(f'<div class="sec"><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in p.get("cote", []))
        bas = ""
        if p.get("pastille") or p.get("logos"):
            past = (f'<p class="pastille"><span>{e(p["pastille"]["grand"])}<small>{e(p["pastille"].get("petit", ""))}</small></span></p>'
                    if p.get("pastille") else "")
            bas = f'<div class="bas">{past}{"".join(logo(l) for l in p.get("logos", []))}</div>'
        if side2:
            # côté gauche : les premières sections ; côté droit : la suite + pastille et logo
            cote = p.get("cote", [])
            n = max(1, (len(cote) + 1) // 2)
            mk = lambda lst: "".join(f'<div class="sec"><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in lst)
            lx0, ly0, lx1, ly1 = side2
            side = (f'<div class="side" style="left:{lx0}mm;top:{ly0}mm;width:{lx1 - lx0}mm;height:{ly1 - ly0}mm">{mk(cote[:n])}</div>'
                    f'<div class="side" style="left:{sx0}mm;top:{sy0}mm;width:{sx1 - sx0}mm;height:{sy1 - sy0}mm">{mk(cote[n:])}{bas}</div>')
        else:
            side = f'<div class="side" style="left:{sx0}mm;top:{sy0}mm;width:{sx1 - sx0}mm;height:{sy1 - sy0}mm">{secs}{bas}</div>'

    deco = ""
    if G["strip"]:
        lx0, ly0, lx1, ly1 = G["strip"]
        sw = lx1 - lx0
        rw = min(max(18, sw * 3), (ly1 - ly0) * .55)          # anneau plus petit sur les formats bas
        haut, bas_ = ly0 + 9, H - rw * .55 - 2                 # le slogan tient entre l'étincelle et l'anneau
        slogan = "peau neuve, mine de rien ✦"
        fs = max(4.6, min(6.5, sw * .9, (bas_ - haut) / (len(slogan) * .95 * .3528)))
        cx, cy = (lx0 + lx1) / 2 - bx0, (haut + bas_) / 2 - by0
        deco += (f'<p class="slogan" style="left:{cx}mm;top:{cy}mm;font-size:{fs:.2f}pt">{slogan}</p>'
                 f'<div style="position:absolute;width:{rw}mm;left:{lx0 - bx0 - rw * .5}mm;top:{H - by0 - rw * .55}mm;transform:rotate(-24deg)">{anneau(C[P["anneau"][0]], C[P["anneau"][1]])}</div>'
                 + spark(f"width:{min(7, sw * .8):.2f}mm;left:{cx - min(7, sw * .8) / 2:.2f}mm;top:{fy0 - by0 + 1:.2f}mm", C[P["etincelles"][0]]))
    if G["side"]:
        sx0, sy0, sx1, sy1 = G["side"]
        if sy1 - sy0 > 70:   # pas d'étincelle sur le texte des petits formats
            deco += spark(f"width:4.5mm;left:{sx1 - bx0 - 5:.2f}mm;top:{sy0 - by0 + .5:.2f}mm", C[P["etincelles"][0]])
        if sy1 - sy0 > 70:
            deco += spark(f"width:3.8mm;left:{sx1 - bx0 - 12:.2f}mm;top:{sy1 - by0 - 5:.2f}mm", C[P["etincelles"][1]])

    guides_html = ""
    if guides:
        b = G["b"]
        zs = "".join(f'<div class="gz" style="left:{z["x"]}mm;top:{z["y"]}mm;width:{z["l"]}mm;height:{z["h"]}mm"><span>mentions obligatoires<br>(Selfnamed)</span></div>'
                     for z in g.get("zones_vides", []))
        guides_html = (f'<div class="gl" style="inset:{b}mm;border:.3mm solid #2a6cff"></div>'
                       f'<div class="gl" style="inset:{b + G["m"]}mm;border:.25mm dashed #2a6cff;opacity:.6"></div>'
                       f'<div class="gl" style="left:{fx0}mm;width:{FW}mm;top:0;bottom:0;border-inline:.3mm solid #888"></div>'
                       f'{zs}<p class="gt">bleu : coupe · pointillés : marge · gris : face avant · orange : laissé vide</p>')

    sti = P["sticker"]
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Unbounded:wght@700;800&display=block" rel="stylesheet">
<style>
@page {{ size: {G['W']}mm {G['H']}mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {G['W']}mm; height: {G['H']}mm; overflow: hidden; background: transparent; }}
body {{ position: relative; color: {TEXTE}; font-family: "Bricolage Grotesque", sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; --k: 1; --q: 1; }}
.fond {{ position: absolute; left: {bx0}mm; top: {by0}mm; width: {bx1 - bx0}mm; height: {by1 - by0}mm; background-color: {'#C9FFF7' if p.get('couleurs_modele') else couleur_motif(p['univers'])}; background-image: url("{swirl('#B8ADFF' if p.get('couleurs_modele') else FOND)}"); background-size: cover; background-position: left center; background-repeat: no-repeat; overflow: hidden; }}
.fond::after {{ content: ""; position: absolute; right: 0; top: {G['b'] + G['m']}mm; bottom: {G['b'] + G['m']}mm; border-right: .5mm dashed {TEXTE}; opacity: .35; }}
.trou {{ position: absolute; background: #fff; }}
.sp {{ position: absolute; }}
.anneau {{ width: 100%; display: block; }}
.slogan {{ position: absolute; transform: translate(-50%, -50%) rotate(-90deg); white-space: nowrap; font-family: Unbounded, sans-serif; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; }}

/* face avant : tailles × --k (calculé pour remplir la hauteur), jamais sous 4,6 pt */
.front {{ position: absolute; display: flex; flex-direction: column; align-items: center; text-align: center; }}
.kicker {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: max(4.6pt, calc({6 * s:.2f}pt * var(--k))); letter-spacing: .22em; text-transform: uppercase; white-space: nowrap; }}
.marque {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: calc({25 * s:.2f}pt * var(--k)); letter-spacing: -.05em; line-height: .9; margin-top: calc({2.2 * s:.2f}mm * var(--k)); white-space: nowrap; }}
.art {{ container-type: size; position: relative; flex: 1 1 0; min-height: 5mm; max-height: calc({26 * s:.2f}mm * var(--k)); width: 100%; display: flex; justify-content: center; margin: calc({3 * s:.2f}mm * var(--k)) 0 calc({1.5 * s:.2f}mm * var(--k)); }}
.art .bouille {{ height: 100%; width: auto; max-width: 70%; transform: translateX(8%) rotate(8deg); }}
.art:has(.gbadge) .bouille {{ height: 78%; align-self: center; transform: translateX(-46%) rotate(8deg); }}
.gbadge {{ position: absolute; right: 4%; top: 50%; translate: 0 -50%; height: 100%; aspect-ratio: 1; border-radius: 50%; display: grid; place-items: center; text-align: center;
  background: {C['citron'] if P['fond'] != 'citron' else CR}; color: {A}; border: .45mm solid {A}; box-shadow: .6mm .6mm 0 {A};
  font-family: Unbounded, sans-serif; font-weight: 800; font-size: 27cqh; line-height: .9; transform: rotate(10deg); padding: .5mm; white-space: pre-line; }}
.nom {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: max(5.5pt, calc({12.5 * s:.2f}pt * var(--k))); line-height: 1; letter-spacing: -.03em; }}
.sous {{ font-weight: 700; font-size: max(4.6pt, calc({7 * s:.2f}pt * var(--k))); margin-top: calc({1.4 * s:.2f}mm * var(--k)); line-height: 1.2; }}
.sticker.fort {{ font-size: max(6pt, calc({9.5 * s:.2f}pt * var(--k))); padding: calc(1mm * var(--k)) calc({3.6 * s:.2f}mm * var(--k)); }}
.sticker {{ margin-top: calc({2.4 * s:.2f}mm * var(--k)); background: {C[sti]}; color: {texte_sur(sti)}; border: .45mm solid {A}; border-radius: 99mm;
  padding: calc(.8mm * var(--k)) calc({3 * s:.2f}mm * var(--k)); font-family: Unbounded, sans-serif; font-weight: 700; font-size: max(4.8pt, calc({7 * s:.2f}pt * var(--k)));
  box-shadow: .7mm .7mm 0 {A}; transform: rotate(-4deg); white-space: nowrap; }}
.volume {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: max(4.8pt, calc({6.5 * s:.2f}pt * var(--k))); margin-top: auto; padding-top: calc(1.5mm * var(--k)); white-space: nowrap; }}

/* côté : tailles × --q */
.side {{ position: absolute; display: flex; flex-direction: column; gap: calc(3mm * var(--q)); padding-bottom: 2.4mm; }}
.side h3 {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: max(5pt, calc(8pt * var(--q))); margin-bottom: calc(.8mm * var(--q)); }}
.side p {{ font-size: max(4.6pt, calc(6.6pt * var(--q))); line-height: 1.3; font-weight: 600; }}
.bas {{ display: flex; flex-wrap: wrap; align-items: center; gap: calc(3mm * var(--q)); margin-top: auto; }}
.pastille {{ flex: none; display: grid; place-items: center; text-align: center; width: max(13mm, calc(17mm * var(--q))); height: max(13mm, calc(17mm * var(--q))); border-radius: 50%;
  background: {CR}; color: {A}; border: .5mm solid {A}; box-shadow: .8mm .8mm 0 {A};
  font-family: Unbounded, sans-serif; font-weight: 800; font-size: max(5pt, calc(9pt * var(--q))); line-height: 1; transform: rotate(8deg); }}
.pastille small {{ display: block; font-family: "Bricolage Grotesque", sans-serif; font-weight: 700; font-size: max(4.6pt, calc(5.4pt * var(--q))); margin-top: .5mm; }}
.logo {{ width: max(10mm, calc(13mm * var(--q))); height: max(10mm, calc(13mm * var(--q))); background: #fff; border-radius: 50%; flex: none; }}

.gl {{ position: absolute; pointer-events: none; }}
.gz {{ position: absolute; border: .5mm dashed #FF6A2B; background: repeating-linear-gradient(45deg, rgba(255,106,43,.14) 0 2mm, transparent 2mm 4mm); display: grid; place-items: center; }}
.gz span, .gt {{ font: 700 4.6pt sans-serif; color: #c2410c; background: rgba(255,255,255,.9); padding: .3mm .8mm; text-align: center; }}
.gt {{ position: absolute; left: {G['b'] + 1}mm; bottom: .1mm; }}
</style></head><body>
<div class="fond">{deco}</div>
{"".join(f'<div class="trou" style="left:{x0}mm;top:{y0}mm;width:{x1 - x0}mm;height:{y1 - y0}mm"></div>' for x0, y0, x1, y1 in G["trous"])}
{front}
{side}
{guides_html}
<script>
async function run() {{
  await document.fonts.ready;
  const body = document.body, front = document.querySelector('.front');
  const wide = (el) => [...el.querySelectorAll('p')].some((c) => c.scrollWidth > el.clientWidth + .5);
  const overF = () => front.lastElementChild.getBoundingClientRect().bottom > front.getBoundingClientRect().bottom + .01 || front.scrollHeight > front.clientHeight || wide(front) || document.querySelector('.art').clientHeight < 5 * 3.78;
  let lo = .3, hi = 1.25;
  for (let i = 0; i < 18; i++) {{ const m = (lo + hi) / 2; body.style.setProperty('--k', m); if (overF()) hi = m; else lo = m; }}
  body.style.setProperty('--k', lo);
  const sides = [...document.querySelectorAll('.side')];
  if (sides.length) {{
    const overS = () => sides.some((side) => side.scrollHeight > side.clientHeight + 1 || side.scrollWidth > side.clientWidth + 1 || wide(side));
    let a = .4, b = 1.25;
    for (let i = 0; i < 18; i++) {{ const m = (a + b) / 2; body.style.setProperty('--q', m); if (overS()) b = m; else a = m; }}
    body.style.setProperty('--q', a);
    // si ça ne tient toujours pas, on retire les dernières sections
    const secs = [...document.querySelectorAll('.side .sec')];
    while (overS() && secs.length > 1) secs.pop().remove();
  }}
  body.dataset.ready = '1';
}}
run();
</script>
</body></html>"""


def verifier_verrou(args):
    """Le design est verrouillé : on refuse de générer si un fichier du design a changé (--deverrouiller pour forcer)."""
    import hashlib
    v = json.loads((ICI / "VERROU.json").read_text(encoding="utf-8"))
    changes = [f for f, h in v["empreintes"].items()
               if hashlib.sha256((ICI.parent / f).read_bytes()).hexdigest() != h]
    if changes and "--deverrouiller" not in args:
        sys.exit("🔒 Design verrouillé : ces fichiers ont changé → " + ", ".join(changes)
                 + "\nAnnule la modification, ou relance avec --deverrouiller si le changement est voulu.")


def main(args):
    verifier_verrou(args)
    args = [a for a in args if not a.startswith("--")]
    fichiers = sorted((ICI / "produits").glob("*.json"))
    if args:
        fichiers = [f for f in fichiers if any(a in f.stem for a in args)]
    jobs = []
    for f in fichiers:
        spec = json.loads(f.read_text(encoding="utf-8"))
        out = ICI / "sortie" / f.stem
        out.mkdir(parents=True, exist_ok=True)
        g = spec["gabarit"]
        px = g.get("px") or [round(g["largeur"] / 25.4 * 600), round(g["hauteur"] / 25.4 * 600)]
        (out / "etiquette.html").write_text(page(spec, False), encoding="utf-8")
        (out / "apercu.html").write_text(page(spec, True), encoding="utf-8")
        jobs.append({"dir": str(out), "w": g["largeur"], "h": g["hauteur"], "px": px})
    jf = ICI / "sortie" / "jobs.json"
    jf.write_text(json.dumps(jobs), encoding="utf-8")
    subprocess.run(["node", str(ICI.parent / "calque" / "rendre.mjs"), str(jf)], check=True)


if __name__ == "__main__":
    main(sys.argv[1:])
