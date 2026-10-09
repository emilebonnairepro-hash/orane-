"""ORANE — le calque d'étiquette.

Un seul design, appliqué à n'importe quel produit et n'importe quel gabarit :
  produits/<fichier>.json = { "gabarit": {...dimensions Selfnamed...}, "produit": {...textes...}, "theme": {...couleurs...} }

Le calque calcule tout seul :
  - la zone utile (plan de travail − fond perdu − marge − zones des mentions obligatoires, laissées transparentes)
  - la face avant (centrée sur face.cx si le gabarit l'indique, sinon au centre de la zone utile)
  - un panneau « côté » si la place le permet (le geste, dedans, pour qui, pastilles, logo)
  - une bande décorative si une petite place reste à gauche
  - la taille de chaque texte (le nom du produit remplit toute la largeur, quelle que soit sa longueur)

Usage :
  python3 etiquettes/calque/calque.py                 → tous les produits
  python3 etiquettes/calque/calque.py 07-gel-nettoyant → un seul
Sorties dans etiquettes/calque/sortie/<nom>/ : etiquette.png (600 dpi, à téléverser), etiquette.pdf, apercu.png (repères)

Gabarit (mm, origine en haut à gauche du plan de travail, fond perdu compris) :
  "largeur", "hauteur", "fond_perdu", "marge",
  "zones_vides": [{"x":..,"y":..,"l":..,"h":..}]   ← cadre orange Selfnamed (mentions obligatoires)
  "face": {"cx": .., "largeur": ..}                 ← facultatif : partie visible de face sur le flacon
  "px": [largeur_px, hauteur_px]                    ← facultatif : taille exacte demandée (sinon calculée à 600 dpi)
"""
import json, pathlib, re, subprocess, sys, html as h

ICI = pathlib.Path(__file__).resolve().parent
C = {"mandarine": "#FF6A2B", "rose": "#FF5FA8", "violet": "#6B2CF5", "citron": "#D4F23A",
     "piscine": "#2CC8F5", "aubergine": "#2A1240", "creme": "#FFF3E3"}
FONCES = {"aubergine", "violet"}

BOUILLE = """<svg viewBox="0 0 120 120" class="bouille"><circle cx="64" cy="64" r="52" fill="#2A1240"/>
<circle cx="58" cy="58" r="52" fill="#FF6A2B" stroke="#2A1240" stroke-width="5"/>
<ellipse cx="30" cy="70" rx="10" ry="7" fill="#FF5FA8"/><ellipse cx="86" cy="70" rx="10" ry="7" fill="#FF5FA8"/>
<circle cx="42" cy="48" r="7" fill="#2A1240"/>
<path d="M68 48 Q76 40 84 48" fill="none" stroke="#2A1240" stroke-width="5" stroke-linecap="round"/>
<path d="M36 66 Q58 98 82 66 Z" fill="#2A1240" stroke="#2A1240" stroke-width="4" stroke-linejoin="round"/>
<path d="M48 80 Q58 72 70 80 Q60 90 48 80 Z" fill="#FF5FA8"/></svg>"""

def anneau(cls, a, b):
    return (f'<svg viewBox="0 0 100 100" class="{cls}"><path d="M10 50 A40 40 0 0 1 90 50" fill="none" stroke="{a}" stroke-width="18"/>'
            f'<path d="M90 50 A40 40 0 0 1 10 50" fill="none" stroke="{b}" stroke-width="18"/>'
            f'<circle cx="78.3" cy="21.7" r="10" fill="#D4F23A" stroke="#2A1240" stroke-width="2"/></svg>')

def spark(cls, fill):
    return (f'<svg viewBox="0 0 40 40" class="sp {cls}"><path d="M20 2 C22 14 26 18 38 20 C26 22 22 26 20 38 C18 26 14 22 2 20 '
            f'C14 18 18 14 20 2 Z" fill="{fill}" stroke="#2A1240" stroke-width="2.5" stroke-linejoin="round"/></svg>')

def svg_asset(nom, cls):
    s = (ICI / "assets" / nom).read_text(encoding="utf-8")
    s = re.sub(r"<\?xml.*?\?>|<!--.*?-->|<!DOCTYPE.*?\]>", "", s, flags=re.S)
    return s.replace("<svg ", f'<svg class="{cls}" ', 1)

def e(t):
    return h.escape(str(t))

# ---------------------------------------------------------------- géométrie
def geometrie(g):
    W, H, b, m = g["largeur"], g["hauteur"], g.get("fond_perdu", 3), g.get("marge", 3)
    bg = [0.0, 0.0, W, H]                     # x0, y0, x1, y1 du fond coloré
    trous = []                                 # zones vides intérieures (fond crème)
    for z in g.get("zones_vides", []):
        x0, y0, x1, y1 = z["x"], z["y"], z["x"] + z["l"], z["y"] + z["h"]
        pleine_h = y0 <= b + .5 and y1 >= H - b - .5
        pleine_l = x0 <= b + .5 and x1 >= W - b - .5
        if pleine_h and x1 >= W - b - .5: bg[2] = min(bg[2], x0 - 1)
        elif pleine_h and x0 <= b + .5: bg[0] = max(bg[0], x1 + 1)
        elif pleine_l and y1 >= H - b - .5: bg[3] = min(bg[3], y0 - 1)
        elif pleine_l and y0 <= b + .5: bg[1] = max(bg[1], y1 + 1)
        else: trous.append((x0, y0, x1, y1))
    s = b + m
    U = [max(s, bg[0] + (m if bg[0] > 0 else 0)), max(s, bg[1] + (m if bg[1] > 0 else 0)),
         min(W - s, bg[2] - (m if bg[2] < W else 0)), min(H - s, bg[3] - (m if bg[3] < H else 0))]
    uw = U[2] - U[0]
    face = g.get("face") or {}
    fw = min(face.get("largeur", uw), uw)
    cx = face.get("cx", (U[0] + U[2]) / 2)
    fx0 = max(U[0], min(cx - fw / 2, U[2] - fw))
    front = [fx0, U[1], fx0 + fw, U[3]]
    GAP = 4
    droite = [front[2] + GAP, U[1], U[2], U[3]]
    gauche = [U[0], U[1], front[0] - GAP, U[3]]
    side = None
    for r in (droite, gauche):
        if r[2] - r[0] >= 22 and (side is None or r[2] - r[0] > side[2] - side[0]):
            side = r
    strip = gauche if (gauche[2] - gauche[0] >= 5 and gauche is not side) else None
    return dict(W=W, H=H, b=b, m=m, bg=bg, trous=trous, U=U, front=front, side=side, strip=strip)

# ---------------------------------------------------------------- page
def page(spec, guides=False, style="plein"):
    epure = style == "epure"
    g, p, t = spec["gabarit"], spec["produit"], spec["theme"]
    G = geometrie(g)
    fond, texte = C[t["fond"]], C[t.get("texte", "aubergine")]
    accent = C[t["accent"]]
    pills = [C[c] for c in t.get("pastilles", ["creme", "citron", "rose"])]
    arche = C[t.get("arche", "creme")]
    ring_a, ring_b = C[t.get("anneau", [t["accent"], "rose"])[0]], C[t.get("anneau", [t["accent"], "rose"])[1]]
    fonce = t["fond"] in FONCES
    dots = "rgba(255,243,227,.16)" if fonce else "rgba(42,18,64,.10)"
    fx0, fy0, fx1, fy1 = G["front"]
    FW, FH = fx1 - fx0, fy1 - fy0
    u = max(.62, min(FW / 36, FH / 82, 2.2))
    bx0, by0, bx1, by1 = G["bg"]

    if G["strip"]:
        sw = G["strip"][2] - G["strip"][0]
        RB = max(22, sw * 2.6)
        RBX = G["strip"][0] - bx0 - RB * .62
        RBY = G["H"] - by0 - RB * .62
    else:
        RB = RBX = RBY = 0

    EPURE_CSS = f"""
/* ----- style épuré : moins d'éléments, plus d'air ----- */
.fond {{ background-image: none; }}
.top {{ flex-direction: column; align-items: flex-start; gap: {.8 * u:.2f}mm; }}
.mark {{ flex: none; width: 74%; }}
.kick-r {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: {max(5.0, 5.2 * u):.2f}pt; letter-spacing: .18em; text-transform: uppercase; white-space: nowrap; }}
.front {{ gap: {2.4 * u:.2f}mm; }}
.ln.em {{ -webkit-text-stroke: {.35 * u:.2f}mm {C['aubergine']}; }}
.arch {{ display: none; }}
.art .bouille {{ height: min(52%, 46cqw); bottom: auto; top: 50%; transform: translate(-50%, -50%) rotate(8deg); }}
.art .ring-solo {{ position: absolute; height: min(92%, 82cqw); aspect-ratio: 1; left: 50%; top: 50%; transform: translate(-50%, -50%) rotate(-25deg); }}
.art .s2 {{ display: none; }}
.pill {{ font-size: {max(5.0, 6.2 * u):.2f}pt; padding: {.8 * u:.2f}mm {2.6 * u:.2f}mm; }}
.foot {{ border-top-style: solid; border-top-width: {.3 * u:.2f}mm; opacity: .9; justify-content: flex-end; }}
.side {{ justify-content: flex-start !important; gap: 5mm; padding-top: 1mm; }}
.ep .ct {{ font-size: 8pt; margin-bottom: 1mm; }}
.ep p {{ font-weight: 600; font-size: 7pt; line-height: 1.35; }}
.badges {{ margin-top: auto; }}
.badge {{ box-shadow: none; transform: none; }}
.slogan {{ opacity: .85; }}
"""

    def pt(v):
        return f"{max(5.0, v * u):.2f}pt"

    lignes = p["lignes"]
    nom_html = "".join(
        f'<span class="ln{" em" if i % 2 else ""}" data-fit data-max="{p.get("taille_max", 40) * u:.1f}">{e(l)}</span>'
        for i, l in enumerate(lignes))
    pills_html = "".join(
        f'<span class="pill" style="--bg:{pills[i % len(pills)]};--fg:{C["creme"] if pills[i % len(pills)] in (C["violet"], C["aubergine"]) else C["aubergine"]};--r:{[-4, 3, -2, 4][i % 4]}deg">{e(x)}</span>'
        for i, x in enumerate(p.get("pastilles", [])[:1] if epure else p.get("pastilles", [])))

    side_html = ""
    if G["side"]:
        sx0, sy0, sx1, sy1 = G["side"]
        geste = "".join(f"<li><b>{i + 1}</b><span>{e(x)}</span></li>" for i, x in enumerate(p.get("geste", [])))
        dedans = "".join(f'<span class="chip">{e(x)}</span>' for x in p.get("dedans", []))
        badges = "".join(f'<p class="badge"><span>{e(x["grand"])}<small>{e(x.get("petit", ""))}</small></span></p>' for x in p.get("badges", []))
        logos = "".join(svg_asset(l, "logo") for l in p.get("logos", []))
        blocs = []
        if geste and not epure: blocs.append(f'<div class="card"><p class="ct">{e(p.get("titre_geste", "Le geste"))}</p><ol class="steps">{geste}</ol></div>')
        if epure:
            blocs = []
            if p.get("geste"): blocs.append(f'<div class="ep"><p class="ct">{e(p.get("titre_geste", "Le geste"))}</p><p>{e(" · ".join(p["geste"]))}.</p></div>')
            if p.get("dedans"): blocs.append(f'<div class="ep"><p class="ct">{e(p.get("titre_dedans", "Dedans"))}</p><p>{e(", ".join(p["dedans"]))}.{(" " + e(p["parfum"])) if p.get("parfum") else ""}</p></div>')
            dedans = ""
        if dedans: blocs.append(f'<div class="card alt"><p class="ct">{e(p.get("titre_dedans", "Dedans"))}</p><div class="chips">{dedans}</div>'
                                f'{"<p class=note>" + e(p["parfum"]) + "</p>" if p.get("parfum") else ""}</div>')
        if p.get("pour_qui") and not epure: blocs.append(f'<div class="pq"><p class="ct">Pour qui ?</p><p>{e(p["pour_qui"])}</p></div>')
        if badges or logos: blocs.append(f'<div class="badges">{badges}{logos}</div>')
        side_html = f'<div class="side" style="left:{sx0}mm;top:{sy0}mm;width:{sx1 - sx0}mm;height:{sy1 - sy0}mm">{"".join(blocs)}</div>'

    strip_html = ""
    if G["strip"]:
        lx0, ly0, lx1, ly1 = G["strip"]
        strip_html = (f'<p class="slogan" style="left:{(lx0 + lx1) / 2}mm;top:{(ly0 + ly1) / 2}mm;font-size:{min(7, (lx1 - lx0) * 1.2):.2f}pt">'
                      f'{e(p.get("slogan", "peau neuve, mine de rien"))} ✦</p>')

    trous_html = "".join(f'<div class="trou" style="left:{x0}mm;top:{y0}mm;width:{x1 - x0}mm;height:{y1 - y0}mm"></div>' for x0, y0, x1, y1 in G["trous"])

    guides_html = ""
    if guides:
        b, W, H = G["b"], G["W"], G["H"]
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
.fond {{ position: absolute; left: {bx0}mm; top: {by0}mm; width: {bx1 - bx0}mm; height: {by1 - by0}mm; overflow: hidden;
  background-color: {fond}; background-image: radial-gradient({dots} 0.42mm, transparent 0.5mm); background-size: 3.4mm 3.4mm; }}
.trou {{ position: absolute; background: #fff; border-radius: 2mm; }}
.sp {{ position: absolute; }}
.ring-big {{ position: absolute; width: {RB}mm; left: {RBX}mm; top: {RBY}mm; transform: rotate(-20deg); }}

/* ----- face avant ----- */
.front {{ position: absolute; left: {fx0}mm; top: {fy0}mm; width: {FW}mm; height: {FH}mm; display: flex; flex-direction: column; gap: {1.6 * u:.2f}mm; }}
.top {{ display: flex; align-items: center; justify-content: space-between; gap: {2 * u:.2f}mm; }}
.mark {{ font-family: Unbounded, sans-serif; font-weight: 900; letter-spacing: -.055em; line-height: .85; flex: 1; min-width: 0; white-space: nowrap; }}
.num {{ flex: none; width: {max(13.5, 12 * u):.2f}mm; height: {max(13.5, 12 * u):.2f}mm; border-radius: 50%; background: {C['aubergine'] if not fonce else C['creme']}; color: {C['creme'] if not fonce else C['aubergine']};
  display: grid; place-items: center; text-align: center; font-family: Unbounded, sans-serif; font-weight: 800; font-size: {pt(7.5)}; line-height: .9; transform: rotate(10deg); }}
.num small {{ display: block; font-family: "Bricolage Grotesque", sans-serif; font-weight: 700; font-size: {pt(4.2)}; letter-spacing: .02em; margin-top: .4mm; text-transform: uppercase; }}
.kick {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: {pt(5)}; letter-spacing: .22em; text-transform: uppercase; margin-top: -{.4 * u:.2f}mm; }}
.name {{ display: flex; flex-direction: column; }}
.ln {{ display: block; width: 100%; white-space: nowrap; font-family: Unbounded, sans-serif; font-weight: 900; line-height: .92; letter-spacing: -.045em; }}
.ln.em {{ color: {accent}; -webkit-text-stroke: {.55 * u:.2f}mm {C['aubergine']}; paint-order: stroke fill; }}
.sous {{ font-weight: 800; font-size: {pt(7)}; line-height: 1.15; margin-top: {1 * u:.2f}mm; }}
.art {{ position: relative; flex: 1; min-height: {16 * u:.2f}mm; container-type: size; }}
.arch {{ position: absolute; left: 50%; width: min(84%, 105cqh); transform: translateX(-50%); top: 6%; bottom: 0; background: {arche}; border: {.6 * u:.2f}mm solid {C['aubergine']};
  border-radius: 999mm 999mm {3 * u:.2f}mm {3 * u:.2f}mm; box-shadow: {1.1 * u:.2f}mm {1.1 * u:.2f}mm 0 {C['aubergine']}; overflow: hidden;
  background-image: radial-gradient(rgba(42,18,64,.08) .45mm, transparent .55mm); background-size: 3mm 3mm; }}
.ring-in {{ position: absolute; width: 90%; left: 30%; top: 22%; }}
.art .bouille {{ position: absolute; height: min(62%, 58cqw); max-width: 70%; aspect-ratio: 1; left: 50%; bottom: 7%; transform: translateX(-50%) rotate(8deg); }}
.bubble {{ position: absolute; left: max(0%, calc(50% - 52cqh - 4%)); top: 0; max-width: 60%; background: {C['creme'] if t['fond'] != 'creme' else C['citron']}; color: {C['aubergine']};
  border: {.5 * u:.2f}mm solid {C['aubergine']}; border-radius: {2.6 * u:.2f}mm; padding: {.9 * u:.2f}mm {1.8 * u:.2f}mm;
  font-family: Unbounded, sans-serif; font-weight: 800; font-size: {pt(5.6)}; line-height: 1.1; transform: rotate(-6deg); box-shadow: {.7 * u:.2f}mm {.7 * u:.2f}mm 0 {C['aubergine']}; z-index: 2; }}
.art .s1 {{ width: {6 * u:.2f}mm; right: 2%; top: 4%; z-index: 2; }}
.art .s2 {{ width: {4 * u:.2f}mm; left: 4%; bottom: 14%; z-index: 2; }}
.pills {{ display: flex; flex-wrap: wrap; justify-content: center; gap: {1.1 * u:.2f}mm {1.2 * u:.2f}mm; }}
.pill {{ background: var(--bg); color: var(--fg); border: {.45 * u:.2f}mm solid {C['aubergine']}; border-radius: 99mm; padding: {.6 * u:.2f}mm {1.9 * u:.2f}mm;
  font-family: Unbounded, sans-serif; font-weight: 700; font-size: {pt(5.4)}; white-space: nowrap; transform: rotate(var(--r)); box-shadow: {.55 * u:.2f}mm {.55 * u:.2f}mm 0 {C['aubergine']}; }}
.foot {{ display: flex; justify-content: space-between; align-items: baseline; gap: 2mm; border-top: {.4 * u:.2f}mm dashed currentColor; padding-top: {1.1 * u:.2f}mm; }}
.foot span {{ font-weight: 700; font-size: {pt(5.4)}; }}
.foot b {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: {pt(6.2)}; white-space: nowrap; }}

/* ----- côté ----- */
.side {{ position: absolute; display: flex; flex-direction: column; justify-content: space-between; gap: 2.4mm; }}
.card {{ background: {C['creme']}; color: {C['aubergine']}; border: .5mm solid {C['aubergine']}; border-radius: 3mm; padding: 2.2mm 2.6mm; box-shadow: 1mm 1mm 0 {C['aubergine']}; }}
.card.alt {{ transform: rotate(-1.2deg); }}
.ct {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 7.5pt; margin-bottom: 1.2mm; }}
.steps {{ list-style: none; display: grid; gap: 1mm; }}
.steps li {{ display: flex; align-items: center; gap: 1.6mm; font-weight: 700; font-size: 6.4pt; line-height: 1.15; }}
.steps b {{ flex: none; width: 4.4mm; height: 4.4mm; border-radius: 50%; background: {accent}; border: .35mm solid {C['aubergine']}; display: grid; place-items: center;
  font-family: Unbounded, sans-serif; font-size: 6pt; color: {C['aubergine']}; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 1mm; }}
.chip {{ border: .35mm solid {C['aubergine']}; border-radius: 99mm; padding: .35mm 1.6mm; font-weight: 700; font-size: 6.2pt; background: #fff; }}
.note {{ font-weight: 600; font-size: 6pt; margin-top: 1.2mm; }}
.pq p {{ font-weight: 600; font-size: 6.4pt; line-height: 1.3; }}
.pq .ct {{ margin-bottom: .6mm; }}
.badges {{ display: flex; align-items: center; gap: 2.4mm; }}
.badge {{ width: 15mm; height: 15mm; flex: none; border-radius: 50%; background: {C['creme']}; color: {C['aubergine']}; border: .5mm solid {C['aubergine']};
  box-shadow: .8mm .8mm 0 {C['aubergine']}; display: grid; place-items: center; text-align: center; font-family: Unbounded, sans-serif; font-weight: 800; font-size: 8pt; line-height: 1; transform: rotate(8deg); }}
.badge small {{ display: block; font-family: "Bricolage Grotesque", sans-serif; font-weight: 700; font-size: 5pt; margin-top: .5mm; }}
.logo {{ width: 12mm; height: 12mm; background: #fff; border-radius: 50%; flex: none; }}
.slogan {{ position: absolute; transform: translate(-50%, -50%) rotate(-90deg); white-space: nowrap; font-family: Unbounded, sans-serif; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; }}
.strip-sp {{ width: 5mm; }}

{EPURE_CSS if epure else ''}
/* ----- repères (aperçu seulement) ----- */
.gl {{ position: absolute; pointer-events: none; }}
.gz {{ position: absolute; border: .6mm dashed #FF6A2B; background: repeating-linear-gradient(45deg, rgba(255,106,43,.14) 0 2mm, transparent 2mm 4mm); display: grid; place-items: center; }}
.gz span, .gt {{ font: 700 5pt sans-serif; color: #c2410c; background: rgba(255,255,255,.9); padding: .4mm 1mm; text-align: center; }}
.gt {{ position: absolute; left: {G['b'] + 1}mm; bottom: .2mm; }}
</style></head><body>
<div class="fond">
  {anneau('ring-big', ring_a, ring_b) if G['strip'] and not epure else ''}
  {spark('', C['creme'] if t['fond'] != 'creme' else C['citron']).replace('class="sp "', f'class="sp" style="width:6mm;left:{(G["strip"][0] + G["strip"][2]) / 2 - bx0 - 3 if G["strip"] else 2}mm;top:{fy0 - by0 + 4}mm"') if G['strip'] and not epure else ''}
</div>
{trous_html}
{strip_html}
<div class="front">
  <div class="top"><p class="mark" data-fit data-max="{30 * u:.1f}">orane</p>{'<p class="kick-r">n°' + e(p['numero']) + ' · ' + e(p['univers']) + '</p>' if epure else '<p class="num">n°' + e(p['numero']) + '<small>' + e(p['univers']) + '</small></p>'}</div>
  <div class="name">{nom_html}{'<p class="sous">' + e(p['sous_titre']) + '</p>' if p.get('sous_titre') else ''}</div>
  <div class="art">
    {anneau('ring-solo', ring_a, ring_b) if epure else ''}
    <div class="arch">{anneau('ring-in', ring_a, ring_b)}</div>
    {BOUILLE}
    {'<p class="bubble">' + e(p['bulle']) + '</p>' if p.get('bulle') and not epure else ''}
    {spark('s1', C['citron'] if t['fond'] != 'citron' else C['creme'])}{spark('s2', C['rose'] if t['fond'] != 'rose' else C['creme'])}
  </div>
  <div class="pills">{pills_html}</div>
  <div class="foot"><span>{'' if epure else e(p.get('pied', ''))}</span><b>{e(p.get('volume', ''))}</b></div>
</div>
{side_html}
{guides_html}
<script>
// Ajuste chaque texte [data-fit] à la largeur disponible, puis réduit le nom si la face avant déborde
function fit(el, max) {{
  let lo = 4, hi = max;
  for (let i = 0; i < 18; i++) {{ const mid = (lo + hi) / 2; el.style.fontSize = mid + 'pt'; if (el.scrollWidth > el.clientWidth + .5) hi = mid; else lo = mid; }}
  el.style.fontSize = lo + 'pt';
}}
async function run() {{
  await document.fonts.ready;
  const front = document.querySelector('.front');
  let k = 1;
  for (let pass = 0; pass < 12; pass++) {{
    document.querySelectorAll('[data-fit]').forEach((el) => fit(el, parseFloat(el.dataset.max) * (el.classList.contains('ln') ? k : 1)));
    const art = document.querySelector('.art');
    if (front.scrollHeight <= front.clientHeight + .5 && art.getBoundingClientRect().height >= front.clientHeight * .24) break;
    k *= .9;
  }}
  const side = document.querySelector('.side');
  if (side) {{
    // le côté remplit sa hauteur : on cherche la plus grande échelle (0,6 à 1,6) où tout tient
    const H0 = side.clientHeight, W0 = side.clientWidth;
    side.style.justifyContent = 'flex-start';
    const apply = (z) => {{ side.style.transformOrigin = '0 0'; side.style.transform = `scale(${{z}})`; side.style.width = (W0 / z) + 'px'; side.style.height = (H0 / z) + 'px'; }};
    let lo = .6, hi = {1.12 if epure else 1.6};
    for (let i = 0; i < 16; i++) {{ const mid = (lo + hi) / 2; apply(mid); if (side.scrollHeight > side.clientHeight + .5) hi = mid; else lo = mid; }}
    apply(lo * .97);
    side.style.justifyContent = 'space-between';
  }}
  document.body.dataset.ready = '1';
}}
run();
</script>
</body></html>"""

def main(args):
    style = "epure" if "--epure" in args else "signature" if "--signature" in args else "v5" if "--v5" in args else "fiche" if "--fiche" in args else "simple" if "--simple" in args else "plein"
    dossier = {"epure": "sortie-epure", "signature": "sortie-signature", "v5": "sortie-v5", "fiche": "sortie-v6-fiche", "simple": "sortie-v7-simple"}.get(style, "sortie")
    args = [a for a in args if not a.startswith("--")]
    fichiers = sorted((ICI / "produits").glob("*.json"))
    if args:
        fichiers = [f for f in fichiers if any(a in f.stem for a in args)]
    jobs = []
    for f in fichiers:
        spec = json.loads(f.read_text(encoding="utf-8"))
        out = ICI / dossier / f.stem
        out.mkdir(parents=True, exist_ok=True)
        g = spec["gabarit"]
        px = g.get("px") or [round(g["largeur"] / 25.4 * 600), round(g["hauteur"] / 25.4 * 600)]
        for nom, guides in (("etiquette", False), ("apercu", True)):
            if style in ("fiche", "simple"):
                import fiche
                contenu = fiche.page(spec, guides, simple=style == "simple")
            elif style in ("signature", "v5"):
                import signature
                contenu = signature.page(spec, guides, leger=style == "v5")
            else:
                contenu = page(spec, guides, style)
            (out / f"{nom}.html").write_text(contenu, encoding="utf-8")
        jobs.append({"dir": str(out), "w": g["largeur"], "h": g["hauteur"], "px": px})
    jf = ICI / dossier / "jobs.json"
    jf.write_text(json.dumps(jobs), encoding="utf-8")
    subprocess.run(["node", str(ICI / "rendre.mjs"), str(jf)], check=True)

if __name__ == "__main__":
    main(sys.argv[1:])
