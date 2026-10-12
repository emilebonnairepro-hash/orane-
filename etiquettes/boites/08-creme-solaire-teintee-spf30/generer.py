"""ORANE n°08 — boîte de la crème solaire teintée SPF 30 (gabarit Selfnamed BOX30-001).

Même design que l'étiquette n°08 (verrouillé) : fond swirl de la catégorie visage (rose), la bouille,
Unbounded + Bricolage Grotesque, sticker SPF 30, pastille et logo COSMOS NATURAL.

Gabarit (gabarit/box30-001.json, relu dans BOX_30-001_Template.ai) :
  - plan de travail 495,95 × 601,09 pt = 174,96 × 212,05 mm → 4133 × 5009 px à 600 dpi
  - faces (plis) : languette de collage | dos 48,8–168,5 | côté 168,5–270,3 | FACE 270,3–388,7 | côté 388,7–488,7 (pt)
    hauteur des faces 140,7 → 460,4 pt
  - mentions obligatoires (ajoutées par Selfnamed, laissées vides et transparentes) : dos + côté gauche, et le rabat du dessous
  - texte seulement sur la face avant et le côté droit, à 3 mm des plis ; fond perdu jusqu'au tracé bleu

Usage : python3 etiquettes/boites/08-creme-solaire-teintee-spf30/generer.py
Sorties (sortie/) : boite.png (à téléverser, 600 dpi), boite.pdf (600 dpi, taille exacte), apercu.png (avec découpe, plis et mentions), maquette.png (boîte montée)
"""
import json, pathlib, subprocess, sys, re, html as h
from urllib.parse import quote

ICI = pathlib.Path(__file__).resolve().parent
ET = ICI.parent.parent
sys.path.insert(0, str(ET))
from couleurs import C, palette, texte_sur, couleur_motif  # noqa: E402

G = json.loads((ICI / "gabarit" / "box30-001.json").read_text(encoding="utf-8"))
W, H = G["plan"]
PX = G["px"]
P = palette("visage")
A, CR = C["aubergine"], C["creme"]
FOND = C[P["fond"]]
MARGE = 3 / 25.4 * 72          # 3 mm en pt

# faces (pt)
YH, YB = 140.7, 460.4
FACE = (270.3, 388.7)
COTE = (388.7, 488.7)
MENTIONS = [(48.8, YH, 270.3, YB), (270.3, 462.9, 388.7, 562.3)]   # dos + côté gauche, rabat du dessous
COUVERCLE = (270.3, 42.2, 388.7, 138.2)

BOUILLE = """<svg viewBox="0 0 120 120" class="{cls}"><circle cx="64" cy="64" r="52" fill="#2A1240"/>
<circle cx="58" cy="58" r="52" fill="#FF6A2B" stroke="#2A1240" stroke-width="5"/>
<ellipse cx="30" cy="70" rx="10" ry="7" fill="#FF5FA8"/><ellipse cx="86" cy="70" rx="10" ry="7" fill="#FF5FA8"/>
<circle cx="42" cy="48" r="7" fill="#2A1240"/>
<path d="M68 48 Q76 40 84 48" fill="none" stroke="#2A1240" stroke-width="5" stroke-linecap="round"/>
<path d="M36 66 Q58 98 82 66 Z" fill="#2A1240" stroke="#2A1240" stroke-width="4" stroke-linejoin="round"/>
<path d="M48 80 Q58 72 70 80 Q60 90 48 80 Z" fill="#FF5FA8"/></svg>"""


def swirl(couleur):
    svg = (ET / "assets" / "swirl-modele.svg").read_text(encoding="utf-8").replace("#B8ADFF", couleur)
    return "data:image/svg+xml," + quote(svg)


def e(t):
    t = str(t)
    for c in "%?!:":
        t = t.replace(" " + c, " " + c)
    return h.escape(t)


def anneau(a, b, style):
    return (f'<svg viewBox="0 0 100 100" style="position:absolute;{style}"><path d="M10 50 A40 40 0 0 1 90 50" fill="none" stroke="{a}" stroke-width="18"/>'
            f'<path d="M90 50 A40 40 0 0 1 10 50" fill="none" stroke="{b}" stroke-width="18"/>'
            f'<circle cx="78.3" cy="21.7" r="10" fill="{CR}" stroke="{A}" stroke-width="2"/></svg>')


def spark(style, fill):
    return (f'<svg viewBox="0 0 40 40" style="position:absolute;{style}"><path d="M20 2 C22 14 26 18 38 20 C26 22 22 26 20 38 C18 26 14 22 2 20 '
            f'C14 18 18 14 20 2 Z" fill="{fill}" stroke="{A}" stroke-width="2.5" stroke-linejoin="round"/></svg>')


def logo():
    s = (ET / "v1" / "assets" / "ecocert-cosmos-natural.svg").read_text(encoding="utf-8")
    s = re.sub(r"<\?xml.*?\?>|<!--.*?-->|<!DOCTYPE.*?\]>", "", s, flags=re.S)
    return s.replace("<svg ", '<svg class="logo" ', 1)


def fond_svg():
    """Fond swirl sur toute la boîte (jusqu'au fond perdu), zones de mentions laissées transparentes."""
    trous = "".join(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="#000"/>' for x0, y0, x1, y1 in MENTIONS)
    return f"""<svg class="fond" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs><clipPath id="fp"><path d="{G['fond_perdu']}"/></clipPath>
<mask id="mz" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#fff"/>{trous}</mask></defs>
<g clip-path="url(#fp)" mask="url(#mz)"><rect width="{W}" height="{H}" fill="{couleur_motif('visage')}"/>
<image href="{swirl(FOND)}" x="-12" y="-8" width="{W + 24}" height="{H + 16}" preserveAspectRatio="xMidYMid slice"/></g></svg>"""


def guides_svg():
    plis = "".join(f'<path d="{d}" fill="none" stroke="#e11d48" stroke-width=".6" stroke-dasharray="3 2"/>' for d in G["plis"])
    fentes = "".join(f'<path d="{d}" fill="none" stroke="#111" stroke-width=".6"/>' for d in G["fentes"])
    zones = "".join(f'<rect x="{x0 + 1}" y="{y0 + 1}" width="{x1 - x0 - 2}" height="{y1 - y0 - 2}" fill="none" stroke="#FF6A2B" stroke-width="1.2" stroke-dasharray="4 3"/>'
                    for x0, y0, x1, y1 in MENTIONS)
    zt = "".join(f'<rect x="{x0 + MARGE}" y="{YH + MARGE}" width="{x1 - x0 - 2 * MARGE}" height="{YB - YH - 2 * MARGE}" fill="none" stroke="#2a6cff" stroke-width=".5" stroke-dasharray="2 2"/>'
                 for x0, x1 in (FACE, COTE))
    return f"""<svg class="fond" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="z-index:5">
<path d="{G['fond_perdu']}" fill="none" stroke="#2a6cff" stroke-width=".5"/>
<path d="{G['decoupe']}" fill="none" stroke="#6B2CF5" stroke-width="1"/>{plis}{fentes}{zones}{zt}
<text x="160" y="152" font-family="sans-serif" font-size="9" font-weight="700" fill="#c2410c" text-anchor="middle">mentions obligatoires (ajoutées par Selfnamed)</text>
<text x="329.5" y="515" font-family="sans-serif" font-size="7" font-weight="700" fill="#c2410c" text-anchor="middle">PAO / lot (Selfnamed)</text>
<text x="6" y="598" font-family="sans-serif" font-size="6" font-weight="700" fill="#c2410c">violet : découpe · bleu : fond perdu · rouge : plis · bleu pointillé : marge 3 mm</text></svg>"""


def boite(guides=False):
    fx0, fx1 = FACE[0] + MARGE, FACE[1] - MARGE
    cx0, cx1 = COTE[0] + MARGE, COTE[1] - MARGE
    y0, y1 = YH + MARGE, YB - MARGE
    k0, k1 = COUVERCLE[0], COUVERCLE[2]
    cote = [
        ("Le geste", "Applique généreusement avant l'exposition et renouvelle souvent, surtout après la baignade."),
        ("Ce qu'on aime", "Facile à étaler, sans traces blanches. Une teinte légère qui aide à uniformiser le teint."),
        ("Dedans", "Filtre minéral (oxyde de zinc) · argousier · acide hyaluronique."),
    ]
    sec = "".join(f'<div><h3>{e(t)}</h3><p>{e(p)}</p></div>' for t, p in cote)
    ref = ""
    if guides:
        ref = f'<img src="../gabarit/mentions-selfnamed.png" style="position:absolute;left:0;top:0;width:{W}pt;height:{H}pt;opacity:.55;z-index:4">'
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Unbounded:wght@700;800&display=block" rel="stylesheet">
<style>
@page {{ size: {W}pt {H}pt; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {W}pt; height: {H}pt; overflow: hidden; background: {'#fff' if guides else 'transparent'}; }}
body {{ position: relative; color: {A}; font-family: "Bricolage Grotesque", sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.fond {{ position: absolute; left: 0; top: 0; width: {W}pt; height: {H}pt; }}
.z {{ position: absolute; overflow: visible; }}

.front {{ position: absolute; left: {fx0}pt; top: {y0 + 4}pt; width: {fx1 - fx0}pt; height: {y1 - y0 - 6}pt; display: flex; flex-direction: column; align-items: center; text-align: center; }}
.kicker {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: 7pt; letter-spacing: .22em; text-transform: uppercase; white-space: nowrap; }}
.marque {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 25pt; letter-spacing: -.05em; line-height: .9; margin-top: 6pt; }}
.art {{ position: relative; flex: none; width: 100%; height: 80pt; margin: 12pt 0 10pt; }}
.art .bouille {{ position: absolute; height: 64pt; left: 50%; top: 8pt; transform: translateX(-36%) rotate(8deg); }}
.nom {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 14pt; line-height: 1; letter-spacing: -.03em; margin-top: auto; }}
.sous {{ font-weight: 700; font-size: 7pt; margin-top: 5pt; line-height: 1.2; }}
.sticker {{ margin-top: 12pt; background: {C[P['sticker']]}; color: {texte_sur(P['sticker'])}; border: 1.3pt solid {A}; border-radius: 99pt;
  padding: 3.5pt 11pt; font-family: Unbounded, sans-serif; font-weight: 700; font-size: 14pt; box-shadow: 2pt 2pt 0 {A}; transform: rotate(-4deg); white-space: nowrap; }}
.sous2 {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: 6pt; letter-spacing: .14em; text-transform: uppercase; margin-top: 9pt; }}
.volume {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: 8pt; margin-top: 16pt; white-space: nowrap; }}

.side {{ position: absolute; left: {cx0}pt; top: {y0 + 4}pt; width: {cx1 - cx0}pt; height: {y1 - y0 - 6}pt; display: flex; flex-direction: column; gap: 8pt; }}
.side .tete {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 15pt; letter-spacing: -.05em; line-height: .9; }}
.side .slog {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: 5.6pt; letter-spacing: .16em; text-transform: uppercase; margin-top: -5pt; line-height: 1.4; }}
.side h3 {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 7.8pt; margin-bottom: 2pt; }}
.side p {{ font-size: 6.6pt; line-height: 1.28; font-weight: 600; }}
.bas {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8pt; margin-top: auto; padding: 0 0 4pt 4pt; }}
.pastille {{ flex: none; display: grid; place-items: center; text-align: center; width: 40pt; height: 40pt; border-radius: 50%;
  background: {CR}; color: {A}; border: 1.3pt solid {A}; box-shadow: 2pt 2pt 0 {A};
  font-family: Unbounded, sans-serif; font-weight: 800; font-size: 10pt; line-height: 1; transform: rotate(8deg); }}
.pastille small {{ display: block; font-family: "Bricolage Grotesque", sans-serif; font-weight: 700; font-size: 5.4pt; margin-top: 1.5pt; }}
.logo {{ width: 28pt; height: 28pt; background: #fff; border-radius: 50%; flex: none; }}
</style></head><body>
{fond_svg()}
{ref}
<!-- couvercle (dessus de la boîte) : la bouille, sans texte (zone sans texte du gabarit) -->
{anneau(C['violet'], C['citron'], f'width:70pt;left:{(k0 + k1) / 2 - 35}pt;top:{COUVERCLE[1] + 13}pt;transform:rotate(-20deg)')}
{BOUILLE.format(cls='z" style="width:48pt;left:' + str((k0 + k1) / 2 - 22) + 'pt;top:' + str(COUVERCLE[1] + 24) + 'pt;transform:rotate(8deg)')}
{spark(f'width:12pt;left:{k0 + 14}pt;top:{COUVERCLE[1] + 16}pt', CR)}{spark(f'width:9pt;left:{k1 - 22}pt;top:{COUVERCLE[3] - 26}pt', C['citron'])}

<!-- face avant -->
{spark(f'width:13pt;left:{fx0}pt;top:{y0 + 62}pt', CR)}{spark(f'width:9pt;left:{fx1 - 10}pt;top:{y0 + 150}pt', C['citron'])}
<div class="front">
  <p class="kicker">n°08 · visage</p>
  <p class="marque">orane</p>
  <div class="art">{anneau(C[P['anneau'][0]], C[P['anneau'][1]], 'width:56pt;left:6pt;top:20pt;transform:rotate(-24deg)')}{BOUILLE.format(cls='bouille')}</div>
  <p class="nom">crème solaire<br>teintée</p>
  <p class="sous">hydratante · sans traces blanches</p>
  <p class="sticker">SPF 30</p>
  <p class="sous2">haute protection · filtre minéral</p>
  <p class="volume">30 ml ℮</p>
</div>

<!-- côté droit -->
<div class="side">
  <div><p class="tete">orane</p></div>
  <p class="slog">peau neuve,<br>mine de rien ✦</p>
  {sec}
  <div class="bas"><p class="pastille"><span>99 %<small>d'origine naturelle</small></span></p>{logo()}</div>
</div>
{guides_svg() if guides else ''}
<script>document.fonts.ready.then(() => {{
  const pt = 96 / 72, err = [];
  for (const [sel, x0, y0, x1, y1] of [['.front', {fx0}, {y0}, {fx1}, {y1}], ['.side', {cx0}, {y0}, {cx1}, {y1}]]) {{
    for (const el of document.querySelectorAll(sel + ' p, ' + sel + ' h3, ' + sel + ' .logo')) {{
      const r = el.getBoundingClientRect();
      if (r.width === 0) continue;
      const d = Math.max(x0 * pt - r.left, r.right - x1 * pt, y0 * pt - r.top, r.bottom - y1 * pt) / pt * 25.4 / 72;
      if (d > 0.05) err.push(sel + ' ' + el.tagName + ' ' + (el.className.baseVal ?? el.className) + ' dépasse de ' + d.toFixed(2) + ' mm');
    }}
  }}
  document.body.dataset.erreurs = JSON.stringify(err);
  document.body.dataset.ready = '1';
}});</script>
</body></html>"""


def main():
    out = ICI / "sortie"; out.mkdir(exist_ok=True)
    (out / "boite.html").write_text(boite(False), encoding="utf-8")
    (out / "apercu.html").write_text(boite(True), encoding="utf-8")
    subprocess.run(["node", str(ICI.parent / "rendre-boite.mjs"), str(out), str(W), str(H), str(PX[0]), str(PX[1])], check=True)
    # taille exacte demandée par Selfnamed (le navigateur arrondit à ±2 px)
    from PIL import Image
    im = Image.open(out / "boite.png")
    if im.size != tuple(PX):
        im.resize(tuple(PX), Image.LANCZOS).save(out / "boite.png", dpi=(600, 600))
    else:
        im.save(out / "boite.png", dpi=(600, 600))
    # PDF d'impression : l'image 600 dpi posée à la taille exacte du plan de travail (174,96 × 212,05 mm)
    im = Image.open(out / "boite.png").convert("RGBA")
    blanc = Image.new("RGB", im.size, "white"); blanc.paste(im, mask=im.split()[3])
    blanc.save(out / "boite.pdf", "PDF", resolution=600.0, quality=100)
    blanc.save(out / "boite-600dpi.tif", dpi=(600, 600), compression="tiff_lzw")   # sans perte, pour l'imprimeur
    faces = {"plan": [W, H], "face": [FACE[0], YH, FACE[1], YB], "cote": [COTE[0], YH, COTE[1], YB],
             "dessus": [COUVERCLE[0], 40.7, COUVERCLE[2], YH]}
    flacon = ET.parent / "instagram" / "assets" / "08-creme-solaire-teintee-spf30.png"   # flacon détouré
    subprocess.run(["node", str(ICI.parent / "maquette-boite.mjs"), str(out), json.dumps(faces), str(flacon)], check=True)


if __name__ == "__main__":
    main()
