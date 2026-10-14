"""ORANE — moteur des boîtes (étuis Selfnamed) : même design que les étiquettes V1 (verrouillé).

Fond swirl de la catégorie sur toute la boîte (jusqu'au fond perdu), la bouille, Unbounded + Bricolage Grotesque.
Les zones de mentions obligatoires (dos, côté gauche, rabat du dessous) restent vides et transparentes :
Selfnamed les remplit. Le texte n'est posé que sur la face avant et le côté droit, à 3 mm des plis
(vérifié au rendu : le script s'arrête si un texte dépasse).

Chaque boîte a son dossier etiquettes/boites/<produit>/ avec :
  boite.json            { "produit": "<fichier de etiquettes/v1/produits sans .json>", "gabarit": "gabarit/<x>.json",
                          "flacon": "<image détourée pour la maquette>", "face_extra": "ligne sous le sticker",
                          "cote": [["Titre", "texte"], ...] (facultatif, sinon celui de l'étiquette) }
  gabarit/<x>.json      tracés relus dans le .ai (lire_boite_ai.py) + position des faces, en pt
  gabarit/mentions-selfnamed.png   ce que Selfnamed imprime (contrôle sur l'aperçu, si le zip fournit le SVG)

Usage : python3 etiquettes/boites/boite.py            → toutes les boîtes
        python3 etiquettes/boites/boite.py 10         → une seule
Sorties (sortie/) : boite.png (à téléverser, 600 dpi, transparent), boite.pdf (600 dpi, taille exacte),
                    boite-600dpi.tif (sans perte), apercu.png (découpe, plis, mentions), maquette.png (boîte montée)
"""
import json, pathlib, subprocess, sys, re, html as h
from urllib.parse import quote

ICI = pathlib.Path(__file__).resolve().parent
ET = ICI.parent
sys.path.insert(0, str(ET))
from couleurs import C, palette, texte_sur, couleur_motif  # noqa: E402

A, CR = C["aubergine"], C["creme"]
MARGE = 3 / 25.4 * 72          # 3 mm en pt
H_REF = 319.7                  # hauteur de face de la boîte n°08 : les tailles grandissent au-delà

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


def logo(nom):
    s = (ET / "v1" / "assets" / nom).read_text(encoding="utf-8")
    s = re.sub(r"<\?xml.*?\?>|<!--.*?-->|<!DOCTYPE.*?\]>", "", s, flags=re.S)
    return s.replace("<svg ", '<svg class="logo" ', 1)


class Boite:
    def __init__(self, dossier):
        self.dir = dossier
        self.cfg = json.loads((dossier / "boite.json").read_text(encoding="utf-8"))
        self.g = json.loads((dossier / self.cfg["gabarit"]).read_text(encoding="utf-8"))
        self.p = json.loads((ET / "v1" / "produits" / f"{self.cfg['produit']}.json").read_text(encoding="utf-8"))["produit"]
        self.pal = palette(self.p["univers"])
        self.W, self.H = self.g["plan"]
        self.YH, self.YB = self.g["hauteur"]
        self.FACE, self.COTE = self.g["face"], self.g["cote"]

    # ---------------------------------------------------------------- fond
    def fond_svg(self):
        g, W, H = self.g, self.W, self.H
        trous = "".join(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="#000"/>' for x0, y0, x1, y1 in g["mentions"])
        if g.get("fond_perdu_masque"):   # gabarit sans tracé continu : masque reconstruit depuis les pointillés du fond perdu
            import base64
            png = base64.b64encode((self.dir / g["fond_perdu_masque"]).read_bytes()).decode()
            zone = f'<image href="data:image/png;base64,{png}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="none"/>'
        elif g.get("fond_perdu"):
            zone = f'<path d="{g["fond_perdu"]}" fill="#fff"/>'
        else:   # pas de tracé de fond perdu dans le gabarit : la découpe élargie de chaque côté
            zone = f'<path d="{g["decoupe"]}" fill="#fff" stroke="#fff" stroke-width="{2 * g["fond_perdu_pt"]}" stroke-linejoin="round"/>'
        return f"""<svg class="fond" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs><mask id="mz" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">{zone}{trous}</mask></defs>
<g mask="url(#mz)"><rect width="{W}" height="{H}" fill="{couleur_motif(self.p['univers'])}"/>
<image href="{swirl(C[self.pal['fond']])}" x="-12" y="-8" width="{W + 24}" height="{H + 16}" preserveAspectRatio="xMidYMid slice"/></g></svg>"""

    def guides_svg(self):
        g, W, H, YH, YB = self.g, self.W, self.H, self.YH, self.YB
        fp = (f'<path d="{g["pointilles"]}" fill="#2a6cff"/>' if g.get("pointilles") else
              f'<path d="{g["fond_perdu"]}" fill="none" stroke="#2a6cff" stroke-width=".5"/>' if g.get("fond_perdu") else
              f'<path d="{g["decoupe"]}" fill="none" stroke="#2a6cff" stroke-opacity=".18" stroke-width="{2 * g["fond_perdu_pt"]}" stroke-linejoin="round"/>')
        plis = "".join(f'<path d="{d}" fill="none" stroke="#e11d48" stroke-width=".6" stroke-dasharray="3 2"/>' for d in g["plis"])
        fentes = "".join(f'<path d="{d}" fill="none" stroke="#111" stroke-width=".6"/>' for d in g["fentes"])
        zones = "".join(f'<rect x="{x0 + 1}" y="{y0 + 1}" width="{x1 - x0 - 2}" height="{y1 - y0 - 2}" fill="none" stroke="#FF6A2B" stroke-width="1.2" stroke-dasharray="4 3"/>'
                        for x0, y0, x1, y1 in g["mentions"])
        zt = "".join(f'<rect x="{x0 + MARGE}" y="{YH + MARGE}" width="{x1 - x0 - 2 * MARGE}" height="{YB - YH - 2 * MARGE}" fill="none" stroke="#2a6cff" stroke-width=".5" stroke-dasharray="2 2"/>'
                     for x0, x1 in (self.FACE, self.COTE) + ((tuple(g["cote_gauche"]),) if g.get("cote_gauche") else ()))
        noms = "".join(f'<text x="{(m[0] + m[2]) / 2}" y="{m[1] + 11 if m[3] - m[1] > 150 else (m[1] + m[3]) / 2 + 22}" font-family="sans-serif" font-size="{9 if m[3] - m[1] > 150 else 7}" font-weight="700" fill="#c2410c" text-anchor="middle">'
                       f'{"mentions obligatoires (ajoutées par Selfnamed)" if m[3] - m[1] > 150 else "PAO / lot (Selfnamed)"}</text>' for m in g["mentions"])
        return f"""<svg class="fond" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="z-index:5">
{fp}{f'<path d="{g["decoupe"]}" fill="none" stroke="#6B2CF5" stroke-width="1"/>' if g.get("decoupe") else ""}{plis}{fentes}{zones}{zt}
{noms}
<text x="6" y="{H - 3}" font-family="sans-serif" font-size="6" font-weight="700" fill="#c2410c">{'violet : découpe · bleu : fond perdu' if g.get('decoupe') else 'bleu : fond perdu (la coupe est juste à l’intérieur)'} · rouge : plis · bleu pointillé : marge 3 mm</text></svg>"""

    # ---------------------------------------------------------------- page
    def html(self, guides=False):
        if self.g.get("disposition") == "etui_plat":
            return self.html_etui(guides)
        p, P, W, H, YH, YB = self.p, self.pal, self.W, self.H, self.YH, self.YB
        fx0, fx1 = self.FACE[0] + MARGE, self.FACE[1] - MARGE
        cx0, cx1 = self.COTE[0] + MARGE, self.COTE[1] - MARGE
        y0, y1 = YH + MARGE, YB - MARGE
        k0, ky0, k1, ky1 = self.g["couvercle"]
        x = max(0, (YB - YH) - H_REF)                     # hauteur en plus par rapport à la boîte n°08
        # la bouille grandit avec la hauteur, sans jamais passer le pli de droite (bord droit = 50 % + 64 % de sa hauteur)
        larg = (self.FACE[1] - self.FACE[0]) - 2 * MARGE
        fw = min(1, larg / 101.4)                         # face plus étroite que la boîte n°08 : le texte rétrécit
        qw = min(1, ((self.COTE[1] - self.COTE[0]) - 2 * MARGE) / 83)   # idem pour le côté
        z = lambda v, mini=4.6: f'{max(mini, v):.2f}pt'
        bou_h = min(64 + .5 * x, (larg / 2 - 4) / .64)
        art_h, ann_w = bou_h + 16 + .25 * x, min(56 + .44 * x, bou_h * .9)
        cote = self.cfg.get("cote") or p["cote"]
        sec = "".join(f'<div><h3>{e(t)}</h3><p>{e(s)}</p></div>' for t, s in cote)
        sec_d, side_g, zg = sec, "", ""
        if self.g.get("cote_gauche"):          # côté gauche libre : la première moitié des textes y passe
            gx0, gx1 = self.g["cote_gauche"][0] + MARGE, self.g["cote_gauche"][1] - MARGE
            n = (len(cote) + 1) // 2
            mk = lambda l: "".join(f'<div><h3>{e(t)}</h3><p>{e(s)}</p></div>' for t, s in l)
            sec_d = mk(cote[n:])
            side_g = (f'<!-- côté gauche -->\n<div class="side gauche" style="left:{gx0}pt;width:{gx1 - gx0}pt">'
                      f'<p class="slog" style="margin-top:0">n°{e(p["numero"])} · {e(p["univers"])}</p>{mk(cote[:n])}</div>')
            zg = f", ['.gauche', {gx0}, {y0}, {gx1}, {y1}]"
        nom = "<br>".join(e(l) for l in p["nom"])
        extra = f'<p class="sous2">{e(self.cfg["face_extra"])}</p>' if self.cfg.get("face_extra") else ""
        logos = "".join(logo(l) for l in p.get("logos", []))
        ref = (f'<img src="../gabarit/mentions-selfnamed.png" style="position:absolute;left:0;top:0;width:{W}pt;height:{H}pt;opacity:.55;z-index:4">'
               if guides and (self.dir / "gabarit" / "mentions-selfnamed.png").exists() else "")
        pastille = (f'<p class="pastille"><span>{e(p["pastille"]["grand"])}<small>{e(p["pastille"]["petit"])}</small></span></p>'
                    if p.get("pastille") else "")
        if self.cfg.get("pastille"):        # pastille propre à la boîte (l'étiquette n'a pas la place)
            pastille = f'<p class="pastille"><span>{e(self.cfg["pastille"]["grand"])}<small>{e(self.cfg["pastille"]["petit"])}</small></span></p>'
        st = P["sticker"]
        return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Unbounded:wght@700;800&display=block" rel="stylesheet">
<style>
@page {{ size: {W}pt {H}pt; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {W}pt; height: {H}pt; overflow: hidden; background: {'#fff' if guides else 'transparent'}; }}
body {{ position: relative; color: {C[P['texte']]}; font-family: "Bricolage Grotesque", sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.fond {{ position: absolute; left: 0; top: 0; width: {W}pt; height: {H}pt; }}
.z {{ position: absolute; overflow: visible; }}

.front {{ position: absolute; left: {fx0}pt; top: {y0 + 4}pt; width: {fx1 - fx0}pt; height: {y1 - y0 - 6}pt; display: flex; flex-direction: column; align-items: center; text-align: center; }}
.kicker {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: {z(7 * fw)}; letter-spacing: .22em; text-transform: uppercase; white-space: nowrap; }}
.marque {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: {z(25 * fw)}; letter-spacing: -.05em; line-height: .9; margin-top: 6pt; }}
.art {{ position: relative; flex: none; width: 100%; height: {art_h}pt; margin: {12 + .12 * x}pt 0 10pt; }}
.art .bouille {{ position: absolute; height: {bou_h}pt; left: 50%; top: {8 + .05 * x}pt; transform: translateX(-36%) rotate(8deg); }}
.nom {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 14pt; line-height: 1; letter-spacing: -.03em; margin-top: auto; }}
.sous {{ font-weight: 700; font-size: {z(7 * fw)}; margin-top: 5pt; line-height: 1.2; }}
.sticker {{ margin-top: 12pt; background: {C[st]}; color: {texte_sur(st)}; border: 1.3pt solid {A}; border-radius: 99pt;
  padding: 3.5pt 11pt; font-family: Unbounded, sans-serif; font-weight: 700; font-size: 14pt; box-shadow: 2pt 2pt 0 {A}; transform: rotate(-4deg); white-space: nowrap; }}
.sous2 {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: {z(6 * fw, 4.8)}; letter-spacing: .14em; text-transform: uppercase; margin-top: 9pt; }}
.volume {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: {z(8 * fw, 4.8)}; margin-top: {16 + .1 * x}pt; white-space: nowrap; }}

.side {{ position: absolute; left: {cx0}pt; top: {y0 + 4}pt; width: {cx1 - cx0}pt; height: {y1 - y0 - 6}pt; display: flex; flex-direction: column; gap: {8 + .1 * x}pt; }}
.side .tete {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: {z(15 * qw)}; letter-spacing: -.05em; line-height: .9; }}
.side .slog {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: {z(5.6 * qw)}; letter-spacing: .16em; text-transform: uppercase; margin-top: -5pt; line-height: 1.4; }}
.side h3 {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: {z(7.8 * qw, 5.5)}; margin-bottom: 2pt; }}
.side p {{ font-size: {z(6.6 * qw)}; line-height: 1.28; font-weight: 600; }}
.bas {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8pt; margin-top: auto; padding: 0 0 4pt 4pt; }}
.pastille {{ flex: none; display: grid; place-items: center; text-align: center; width: {40 * qw:.1f}pt; height: {40 * qw:.1f}pt; border-radius: 50%;
  background: {CR}; color: {A}; border: 1.3pt solid {A}; box-shadow: 2pt 2pt 0 {A};
  font-family: Unbounded, sans-serif; font-weight: 800; font-size: {z(10 * qw)}; line-height: 1; transform: rotate(8deg); }}
.pastille small {{ display: block; font-family: "Bricolage Grotesque", sans-serif; font-weight: 700; font-size: 5.4pt; margin-top: 1.5pt; }}
.logo {{ width: {28 * qw:.1f}pt; height: {28 * qw:.1f}pt; background: #fff; border-radius: 50%; flex: none; }}
</style></head><body>
{self.fond_svg()}
{ref}
<!-- couvercle (dessus de la boîte) : la bouille, sans texte (zone sans texte du gabarit) -->
{anneau(C[P['anneau'][0]], C[P['anneau'][1]], f'width:70pt;left:{(k0 + k1) / 2 - 35}pt;top:{ky0 + 13}pt;transform:rotate(-20deg)')}
{BOUILLE.format(cls='z" style="width:48pt;left:' + str((k0 + k1) / 2 - 22) + 'pt;top:' + str(ky0 + 24) + 'pt;transform:rotate(8deg)')}
{spark(f'width:12pt;left:{k0 + 14}pt;top:{ky0 + 16}pt', CR)}{spark(f'width:9pt;left:{k1 - 22}pt;top:{ky1 - 26}pt', C['citron'])}

<!-- face avant -->
{spark(f'width:13pt;left:{fx0}pt;top:{y0 + 62 + .1 * x}pt', CR)}{spark(f'width:9pt;left:{fx1 - 10}pt;top:{y0 + (150 if x < 20 else 95)}pt', C['citron'])}
<div class="front">
  <p class="kicker">n°{e(p['numero'])} · {e(p['univers'])}</p>
  <p class="marque">orane</p>
  <div style="flex:1 1 0"></div>
  <div class="art">{anneau(C[P['anneau'][0]], C[P['anneau'][1]], f'width:{ann_w}pt;left:6pt;top:{20 + .05 * x}pt;transform:rotate(-24deg)')}{BOUILLE.format(cls='bouille')}</div>
  <p class="nom">{nom}</p>
  <p class="sous">{e(p['sous_titre'])}</p>
  <p class="sticker">{e(p['sticker'])}</p>
  {extra}
  <p class="volume">{e(p['volume'])}</p>
</div>

{side_g}
<!-- côté droit -->
<div class="side">
  <div><p class="tete">orane</p></div>
  <p class="slog">peau neuve,<br>mine de rien ✦</p>
  {sec_d}
  <div class="bas">{pastille}{logos}</div>
</div>
{self.guides_svg() if guides else ''}
<script>document.fonts.ready.then(() => {{
  const pt = 96 / 72, err = [];
  // le sticker rétrécit s'il est plus large que la face (jamais sous 7 pt)
  const st = document.querySelector('.front .sticker');
  for (let fs = 14; st.getBoundingClientRect().width > ({fx1 - fx0} - 6) * pt && fs > 7; ) {{ fs -= .5; st.style.fontSize = fs + 'pt'; }}
  // le nom aussi, s'il a un mot trop long pour la face (jamais sous 9 pt)
  const nm = document.querySelector('.front .nom');
  for (let fs = 14; nm.getBoundingClientRect().width > ({fx1 - fx0} - 2) * pt && fs > 9; ) {{ fs -= .5; nm.style.fontSize = fs + 'pt'; }}
  for (const [sel, x0, y0, x1, y1] of [['.front', {fx0}, {y0}, {fx1}, {y1}], ['.side:not(.gauche)', {cx0}, {y0}, {cx1}, {y1}]{zg}]) {{
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

    def html_etui(self, guides=False):
        """Étui plat (sachets) : grande face avant, dos réservé aux mentions, tranches étroites.
        Les textes du côté passent en bandeau sous la face ; « orane » et le slogan à la verticale sur la tranche."""
        p, P, W, H, YH, YB = self.p, self.pal, self.W, self.H, self.YH, self.YB
        fx0, fx1 = self.FACE[0] + MARGE, self.FACE[1] - MARGE
        cx0, cx1 = self.COTE[0] + MARGE, self.COTE[1] - MARGE
        y0, y1 = YH + MARGE, YB - MARGE
        k0, ky0, k1, ky1 = self.g["couvercle"]
        r0, ry0, r1, ry1 = self.g.get("rabat", [0, 0, 0, 0])
        cote = self.cfg.get("cote") or p.get("cote", [])
        sec = "".join(f'<div><h3>{e(t)}</h3><p>{e(x)}</p></div>' for t, x in cote)
        nom = "<br>".join(e(l) for l in p["nom"])
        extra = f'<p class="sous2">{e(self.cfg["face_extra"])}</p>' if self.cfg.get("face_extra") else ""
        logos = "".join(logo(l) for l in p.get("logos", []))
        ref = (f'<img src="../gabarit/mentions-selfnamed.png" style="position:absolute;left:0;top:0;width:{W}pt;height:{H}pt;opacity:.55;z-index:4">'
               if guides and (self.dir / "gabarit" / "mentions-selfnamed.png").exists() else "")
        st = P["sticker"]
        haut = (y1 - y0) * .6                       # partie haute de la face : marque + bouille ; dessous : le bandeau de textes
        return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Unbounded:wght@700;800&display=block" rel="stylesheet">
<style>
@page {{ size: {W}pt {H}pt; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {W}pt; height: {H}pt; overflow: hidden; background: {'#fff' if guides else 'transparent'}; }}
body {{ position: relative; color: {C[P['texte']]}; font-family: "Bricolage Grotesque", sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.fond {{ position: absolute; left: 0; top: 0; width: {W}pt; height: {H}pt; }}
.z {{ position: absolute; overflow: visible; }}
.front {{ position: absolute; left: {fx0}pt; top: {y0}pt; width: {fx1 - fx0}pt; height: {y1 - y0}pt; }}
.haut {{ position: absolute; left: 4pt; top: 6pt; width: calc(100% - 8pt); height: {haut - 6}pt; display: flex; flex-direction: column; align-items: flex-start; }}
.kicker {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: 8pt; letter-spacing: .22em; text-transform: uppercase; white-space: nowrap; }}
.marque {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 36pt; letter-spacing: -.05em; line-height: .9; margin-top: 7pt; white-space: nowrap; }}
.nom {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 19pt; line-height: 1; letter-spacing: -.03em; margin-top: auto; }}
.sous {{ font-weight: 700; font-size: 8.4pt; margin-top: 6pt; line-height: 1.25; }}
.sticker {{ margin-top: 11pt; background: {C[st]}; color: {texte_sur(st)}; border: 1.3pt solid {A}; border-radius: 99pt;
  padding: 3.5pt 11pt; font-family: Unbounded, sans-serif; font-weight: 700; font-size: 13pt; box-shadow: 2pt 2pt 0 {A}; transform: rotate(-4deg); white-space: nowrap; }}
.sous2 {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: 6.4pt; letter-spacing: .14em; text-transform: uppercase; margin-top: 10pt; }}
.volume {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: 9pt; margin-top: 8pt; white-space: nowrap; }}
.bouille {{ position: absolute; width: 66pt; right: 6pt; top: 8pt; transform: rotate(8deg); }}
.bande {{ position: absolute; left: 4pt; right: 4pt; top: {haut + 14}pt; bottom: 4pt; display: grid; grid-template-columns: repeat({max(1, len(cote))}, 1fr); gap: 12pt; align-content: start; }}
.bande h3 {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 9.4pt; margin-bottom: 3.5pt; }}
.bande p {{ font-size: 8pt; line-height: 1.32; font-weight: 600; }}
.logos {{ position: absolute; right: 4pt; bottom: 4pt; display: flex; gap: 6pt; }}
.logo {{ width: 30pt; height: 30pt; background: #fff; border-radius: 50%; flex: none; }}
.tranche {{ position: absolute; left: {cx0}pt; top: {y0}pt; width: {cx1 - cx0}pt; height: {y1 - y0}pt; display: grid; place-items: center; }}
.tranche p {{ writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-family: Unbounded, sans-serif; font-weight: 800; font-size: 13pt; letter-spacing: -.04em; line-height: 1; }}
.tranche small {{ font-weight: 700; font-size: 5.8pt; letter-spacing: .16em; text-transform: uppercase; margin-top: 10pt; }}
</style></head><body>
{self.fond_svg()}
{ref}
<!-- dessus (couvercle) et rabat du dessous : décor sans texte -->
{anneau(C['violet'], C['citron'], f'width:44pt;left:{(k0 + k1) / 2 - 22}pt;top:{ky0 + (ky1 - ky0) / 2 - 22}pt;transform:rotate(-20deg)')}
{BOUILLE.format(cls='z" style="width:28pt;left:' + str((k0 + k1) / 2 - 12) + 'pt;top:' + str(ky0 + (ky1 - ky0) / 2 - 13) + 'pt;transform:rotate(8deg)')}
{spark(f'width:11pt;left:{k0 + 40}pt;top:{ky0 + 10}pt', CR)}{spark(f'width:8pt;left:{k1 - 50}pt;top:{ky0 + 14}pt', C['citron'])}
{spark(f'width:10pt;left:{r0 + 60}pt;top:{ry0 + 8}pt', CR) if r1 else ''}{spark(f'width:8pt;left:{r1 - 70}pt;top:{ry0 + 12}pt', C['citron']) if r1 else ''}

<!-- face avant -->
{anneau(C[P['anneau'][0]], C[P['anneau'][1]], f'width:60pt;left:{fx1 - 84}pt;top:{y0 + 22}pt;transform:rotate(-24deg)')}
{spark(f'width:13pt;left:{fx1 - 26}pt;top:{y0 + haut * .5}pt', CR)}{spark(f'width:10pt;left:{fx1 - 60}pt;top:{y0 + haut * .78}pt', C['citron'])}
<div class="front">
  <div class="haut">
    <p class="kicker">n°{e(p['numero'])} · {e(p['univers'])}</p>
    <p class="marque">orane</p>
    <p class="nom">{nom}</p>
    <p class="sous">{e(p['sous_titre'])}</p>
    <p class="sticker">{e(p['sticker'])}</p>
    {extra}
    <p class="volume">{e(p['volume'])}</p>
  </div>
  {BOUILLE.format(cls='bouille')}
  <div class="bande">{sec}</div>
  {f'<div class="logos">{logos}</div>' if logos else ''}
</div>

<!-- tranche droite -->
<div class="tranche"><p>orane <small>peau neuve, mine de rien ✦</small></p></div>
{self.guides_svg() if guides else ''}
<script>document.fonts.ready.then(() => {{
  const pt = 96 / 72, err = [];
  for (const [sel, x0, y0, x1, y1] of [['.front', {fx0}, {y0}, {fx1}, {y1}], ['.tranche', {cx0}, {y0}, {cx1}, {y1}]]) {{
    for (const el of document.querySelectorAll(sel + ' p, ' + sel + ' h3, ' + sel + ' .logo')) {{
      const r = el.getBoundingClientRect();
      if (r.width === 0) continue;
      const d = Math.max(x0 * pt - r.left, r.right - x1 * pt, y0 * pt - r.top, r.bottom - y1 * pt) / pt * 25.4 / 72;
      if (d > 0.05) err.push(sel + ' ' + el.tagName + ' ' + (el.className.baseVal ?? el.className) + ' dépasse de ' + d.toFixed(2) + ' mm');
    }}
  }}
  // la bouille ne doit pas toucher le texte de la colonne de gauche
  const b = document.querySelector('.front .bouille').getBoundingClientRect();
  for (const el of document.querySelectorAll('.haut p')) {{ const r = el.getBoundingClientRect();
    if (r.right > b.left + 2 && r.bottom > b.top && r.top < b.bottom) err.push('bouille sur ' + el.className); }}
  document.body.dataset.erreurs = JSON.stringify(err);
  document.body.dataset.ready = '1';
}});</script>
</body></html>"""

    # ---------------------------------------------------------------- rendu
    def rendre(self):
        from PIL import Image
        out = self.dir / "sortie"; out.mkdir(exist_ok=True)
        (out / "boite.html").write_text(self.html(False), encoding="utf-8")
        (out / "apercu.html").write_text(self.html(True), encoding="utf-8")
        PX = tuple(self.g["px"])
        subprocess.run(["node", str(ICI / "rendre-boite.mjs"), str(out), str(self.W), str(self.H), str(PX[0]), str(PX[1])], check=True)
        im = Image.open(out / "boite.png")
        if im.size != PX:              # taille exacte demandée par Selfnamed (le navigateur arrondit à ±2 px)
            im = im.resize(PX, Image.LANCZOS)
        im.save(out / "boite.png", dpi=(600, 600))
        # PDF d'impression : l'image 600 dpi posée à la taille exacte du plan de travail
        im = im.convert("RGBA")
        blanc = Image.new("RGB", im.size, "white"); blanc.paste(im, mask=im.split()[3])
        blanc.save(out / "boite.pdf", "PDF", resolution=600.0, quality=100)
        blanc.save(out / "boite-600dpi.tif", dpi=(600, 600), compression="tiff_lzw")   # sans perte, pour l'imprimeur
        k = self.g["couvercle"]
        faces = {"plan": [self.W, self.H], "face": [self.FACE[0], self.YH, self.FACE[1], self.YB],
                 "cote": [self.COTE[0], self.YH, self.COTE[1], self.YB], "dessus": [k[0], k[1], k[2], self.YH]}
        cmd = ["node", str(ICI / "maquette-boite.mjs"), str(out), json.dumps(faces)]
        if self.cfg.get("flacon"):
            cmd.append(str(ET.parent / self.cfg["flacon"]))
        subprocess.run(cmd, check=True)


def main(args):
    dossiers = sorted(d for d in ICI.iterdir() if (d / "boite.json").exists())
    if args:
        dossiers = [d for d in dossiers if any(d.name.startswith(a) for a in args)]
    for d in dossiers:
        print("→", d.name)
        Boite(d).rendre()


if __name__ == "__main__":
    main(sys.argv[1:])
