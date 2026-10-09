"""ORANE — étiquettes avant pour Selfnamed.

Génère, pour chaque soin :
  - export/<n>-<slug>.png       : fichier à téléverser sur Selfnamed (600 dpi, 3 mm de fond perdu)
  - export/<n>-<slug>.pdf       : la même chose en PDF vectoriel (pour un imprimeur ou un contrôle)
  - apercu/<n>-<slug>.png       : épreuve avec les repères (coupe, zone de sécurité, zone des mentions obligatoires)

Les tailles réelles viennent des gabarits Selfnamed de chaque produit : remplace LARGEUR / HAUTEUR
(en mm, format fini sans fond perdu) dans PRODUITS, puis relance :  python3 etiquettes/generer.py
La mise en page s'adapte toute seule (portrait ou paysage).
"""
import json, pathlib, subprocess, sys

ICI = pathlib.Path(__file__).resolve().parent
FOND_PERDU = 3      # mm, demandé par Selfnamed
MARGE = 3           # mm, zone de sécurité à l'intérieur de la coupe
ZONE_MENTIONS = 0.24  # part de la hauteur laissée vide en bas pour les mentions obligatoires (ajoutées par Selfnamed)

C = {"mandarine": "#FF6A2B", "rose": "#FF5FA8", "violet": "#6B2CF5", "citron": "#D4F23A",
     "piscine": "#2CC8F5", "aubergine": "#2A1240", "creme": "#FFF3E3"}

# Charte : jamais de texte crème sur mandarine ou rose ; 3 couleurs vives maximum par étiquette.
PRODUITS = [
  {"n": "01", "slug": "gel-lavant", "univers": "corps", "nom": "gel lavant", "sous": "mains & corps",
   "sticker": "pamplemousse", "fond": "citron", "texte": "aubergine", "accent": "mandarine", "sticker_fond": "mandarine",
   "largeur": 60, "hauteur": 90},
  {"n": "02", "slug": "shampooing", "univers": "cheveux", "nom": "shampooing", "sous": "cuir chevelu sensible",
   "sticker": "tout doux", "fond": "rose", "texte": "aubergine", "accent": "citron", "sticker_fond": "citron",
   "largeur": 60, "hauteur": 90},
  {"n": "03", "slug": "huile-a-barbe", "univers": "homme", "nom": "huile à barbe", "sous": "adoucissante",
   "sticker": "non grasse", "fond": "aubergine", "texte": "creme", "accent": "mandarine", "sticker_fond": "citron",
   "largeur": 60, "hauteur": 90},
  {"n": "04", "slug": "demaquillant", "univers": "visage", "nom": "démaquillant", "sous": "biphasé",
   "sticker": "sans parfum", "fond": "violet", "texte": "creme", "accent": "citron", "sticker_fond": "citron",
   "largeur": 60, "hauteur": 90},
  {"n": "05", "slug": "gel-visage-zinc", "univers": "homme", "nom": "gel visage", "sous": "au zinc, sans huile",
   "sticker": "zéro effet gras", "fond": "mandarine", "texte": "aubergine", "accent": "citron", "sticker_fond": "creme",
   "largeur": 60, "hauteur": 90},
  {"n": "06", "slug": "patchs-yeux", "univers": "visage", "nom": "patchs yeux", "sous": "caféine & vitamine C",
   "sticker": "7 paires", "fond": "creme", "texte": "aubergine", "accent": "rose", "sticker_fond": "mandarine",
   "largeur": 90, "hauteur": 60},
]

BOUILLE = """<svg viewBox="0 0 120 120" class="bouille"><circle cx="64" cy="64" r="52" fill="#2A1240"/>
<circle cx="58" cy="58" r="52" fill="#FF6A2B" stroke="#2A1240" stroke-width="5"/>
<ellipse cx="30" cy="70" rx="10" ry="7" fill="#FF5FA8"/><ellipse cx="86" cy="70" rx="10" ry="7" fill="#FF5FA8"/>
<circle cx="42" cy="48" r="7" fill="#2A1240"/>
<path d="M68 48 Q76 40 84 48" fill="none" stroke="#2A1240" stroke-width="5" stroke-linecap="round"/>
<path d="M36 66 Q58 98 82 66 Z" fill="#2A1240" stroke="#2A1240" stroke-width="4" stroke-linejoin="round"/>
<path d="M48 80 Q58 72 70 80 Q60 90 48 80 Z" fill="#FF5FA8"/></svg>"""

def anneau(a, b):
    return f"""<svg viewBox="0 0 100 100" class="anneau"><path d="M10 50 A40 40 0 0 1 90 50" fill="none" stroke="{a}" stroke-width="18"/>
<path d="M90 50 A40 40 0 0 1 10 50" fill="none" stroke="{b}" stroke-width="18"/><circle cx="78.3" cy="21.7" r="10" fill="#D4F23A"/></svg>"""

ETINCELLE = """<svg viewBox="0 0 40 40" class="etincelle"><path d="M20 2 C22 14 26 18 38 20 C26 22 22 26 20 38 C18 26 14 22 2 20 C14 18 18 14 20 2 Z" fill="FILL" stroke="#2A1240" stroke-width="2.5" stroke-linejoin="round"/></svg>"""

def page(p, apercu):
    W, H = p["largeur"], p["hauteur"]
    TW, TH = W + 2 * FOND_PERDU, H + 2 * FOND_PERDU
    paysage = W > H
    u = min(W, H) / 60  # unité d'échelle : 1 pour une étiquette de 60 mm de petit côté
    fond, texte, accent = C[p["fond"]], C[p["texte"]], C[p["accent"]]
    sfond = C[p["sticker_fond"]]
    stexte = C["aubergine"]
    trait = C["aubergine"] if p["fond"] not in ("aubergine", "violet") else C["creme"]
    # anneau : moitié haute = accent, moitié basse = une seconde couleur vive tant qu'on reste à 3 vives
    vives = {p["fond"], p["accent"], p["sticker_fond"]} - {"aubergine", "creme"}
    seconde = next((k for k in ["rose", "mandarine", "citron", "violet"] if k in vives and k != p["accent"]), p["accent"])
    ring = anneau(accent, C[seconde])
    spark = ETINCELLE.replace("FILL", C["creme"] if p["fond"] != "creme" else C["citron"])
    zone_h = H * ZONE_MENTIONS
    guides = ""
    if apercu:
        guides = f"""
<div class="g coupe"></div><div class="g securite"></div>
<div class="g mentions"><span>zone laissée vide : mentions obligatoires ajoutées par Selfnamed</span></div>
<div class="g legende">— coupe · - - sécurité 3 mm · fond perdu 3 mm autour</div>"""
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Unbounded:wght@700;800&display=block" rel="stylesheet">
<style>
@page {{ size: {TW}mm {TH}mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {TW}mm; height: {TH}mm; overflow: hidden; }}
body {{ position: relative; background: {fond}; color: {texte}; font-family: "Bricolage Grotesque", sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.anneau {{ position: absolute; width: {38*u}mm; {'right' if not paysage else 'left'}: {-14*u}mm; top: {-12*u}mm; transform: rotate(-18deg); }}
.etincelle {{ position: absolute; width: {7*u}mm; }}
.e1 {{ left: {FOND_PERDU + MARGE + (W*0.12 if not paysage else W*0.72)}mm; top: {FOND_PERDU + H*(0.33 if not paysage else 0.12)}mm; }}
.e2 {{ right: {FOND_PERDU + MARGE + 2*u}mm; top: {FOND_PERDU + H*(1-ZONE_MENTIONS) - 12*u}mm; width: {4.5*u}mm; }}
.contenu {{ position: absolute; left: {FOND_PERDU + MARGE}mm; right: {FOND_PERDU + MARGE}mm; top: {FOND_PERDU + MARGE}mm;
  height: {H - 2*MARGE - zone_h}mm; display: flex; flex-direction: column; {'padding-left: ' + str(round(30*u,2)) + 'mm;' if paysage else ''} }}
.kicker {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: {5.2*u}pt; letter-spacing: .22em; text-transform: uppercase; }}
.marque {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: {(27 if not paysage else 19)*u}pt; letter-spacing: -.05em; line-height: .9; margin-top: {1.6*u}mm; }}
.nom {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: {(13 if not paysage else 12)*u}pt; line-height: .98; letter-spacing: -.03em; margin-top: auto; }}
.sous {{ font-weight: 700; font-size: {7*u}pt; margin-top: {1.4*u}mm; }}
.sticker {{ display: inline-block; align-self: flex-start; margin-top: {2.4*u}mm; background: {sfond}; color: {stexte}; border: {0.5*u}mm solid {C['aubergine']};
  border-radius: 99mm; padding: {0.9*u}mm {2.6*u}mm; font-family: Unbounded, sans-serif; font-weight: 700; font-size: {6*u}pt;
  box-shadow: {0.8*u}mm {0.8*u}mm 0 {C['aubergine']}; transform: rotate(-4deg); }}
.slogan {{ font-weight: 600; font-size: {5.4*u}pt; margin-top: {2.2*u}mm; opacity: .9; }}
.bouille {{ position: absolute; width: {(15 if not paysage else 22)*u}mm; {'right' if not paysage else 'left'}: {FOND_PERDU + MARGE + (2*u if not paysage else 3*u)}mm;
  top: {FOND_PERDU + (H*0.27 if not paysage else H*0.26)}mm; transform: rotate(8deg); }}
.trait {{ position: absolute; left: {FOND_PERDU + MARGE}mm; right: {FOND_PERDU + MARGE}mm; top: {FOND_PERDU + H - MARGE - zone_h + 1.2*u}mm; border-top: {0.45*u}mm dashed {trait}; opacity: .55; }}
.g {{ position: absolute; pointer-events: none; }}
.coupe {{ inset: {FOND_PERDU}mm; border: .25mm solid #000; }}
.securite {{ inset: {FOND_PERDU + MARGE}mm; border: .25mm dashed #000; opacity: .6; }}
.mentions {{ left: {FOND_PERDU + MARGE}mm; right: {FOND_PERDU + MARGE}mm; bottom: {FOND_PERDU + MARGE}mm; height: {zone_h - 2*u}mm;
  border: .5mm dashed #FF6A2B; background: rgba(255,255,255,.55); display: grid; place-items: center; text-align: center; padding: 1mm;
  font: 600 {4.4*u}pt "Bricolage Grotesque", sans-serif; color: #2A1240; }}
.legende {{ left: {FOND_PERDU}mm; bottom: .6mm; font: 600 3.6pt sans-serif; color: #000; background: rgba(255,255,255,.8); padding: 0 1mm; }}
</style></head><body>
{ring}
{spark.replace('class="etincelle"', 'class="etincelle e1"')}
{spark.replace('class="etincelle"', 'class="etincelle e2"')}
{BOUILLE}
<div class="contenu">
  <p class="kicker">n°{p['n']} · {p['univers']}</p>
  <p class="marque">orane</p>
  <p class="nom">{p['nom']}</p>
  <p class="sous">{p['sous']}</p>
  <p class="sticker">{p['sticker']}</p>
  <p class="slogan">peau neuve, mine de rien.</p>
</div>
<div class="trait"></div>
{guides}
</body></html>"""

def main():
    (ICI / "source").mkdir(exist_ok=True)
    jobs = []
    for p in PRODUITS:
        for apercu in (False, True):
            nom = f"{p['n']}-{p['slug']}"
            f = ICI / "source" / f"{nom}{'-apercu' if apercu else ''}.html"
            f.write_text(page(p, apercu), encoding="utf-8")
            jobs.append({"html": str(f), "nom": nom, "apercu": apercu,
                         "w": p["largeur"] + 2 * FOND_PERDU, "h": p["hauteur"] + 2 * FOND_PERDU})
    (ICI / "source" / "jobs.json").write_text(json.dumps(jobs), encoding="utf-8")
    subprocess.run(["node", str(ICI / "rendre.mjs"), str(ICI)], check=True)

if __name__ == "__main__":
    sys.exit(main())
