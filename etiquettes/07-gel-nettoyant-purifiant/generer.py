"""ORANE n°07 — Gel nettoyant purifiant (Selfnamed « Blemish Purifying Face Wash », 140 ml, réf. 150-004).

Gabarit Selfnamed (TEMPLATE_Label 150-004.ai + manuel) :
  - plan de travail 142,5 × 109 mm (3367 × 2575 px à 600 dpi), fond perdu 2 mm → étiquette coupée 138,5 × 105 mm
  - zone des mentions obligatoires (cadre orange) : de x = 107 mm jusqu'au bord droit → laissée vide et transparente
  - face avant visible sur le flacon : centrée vers x ≈ 37–45 mm
  - texte ≥ 4,5 pt, marge de 3 mm entre le design et la coupe, export PNG 600 dpi fond transparent, < 20 Mo

Usage : python3 etiquettes/07-gel-nettoyant-purifiant/generer.py
Sorties : etiquette.png (à téléverser), etiquette.pdf, apercu.png (avec repères), apercu-flacon.png
"""
import pathlib, subprocess, re

ICI = pathlib.Path(__file__).resolve().parent
W, H = 142.5, 109.0          # plan de travail (mm)
BLEED = 2.0
SAFE = BLEED + 3.0           # 3 mm entre design et coupe
INFO_X = 107.0               # début de la zone des mentions obligatoires
FRONT_CX = 39.0              # centre de la face avant
FRONT_W = 32.0

C = {"mandarine": "#FF6A2B", "rose": "#FF5FA8", "violet": "#6B2CF5", "citron": "#D4F23A",
     "aubergine": "#2A1240", "creme": "#FFF3E3"}

BOUILLE = """<svg viewBox="0 0 120 120" class="bouille"><circle cx="64" cy="64" r="52" fill="#2A1240"/>
<circle cx="58" cy="58" r="52" fill="#FF6A2B" stroke="#2A1240" stroke-width="5"/>
<ellipse cx="30" cy="70" rx="10" ry="7" fill="#FF5FA8"/><ellipse cx="86" cy="70" rx="10" ry="7" fill="#FF5FA8"/>
<circle cx="42" cy="48" r="7" fill="#2A1240"/>
<path d="M68 48 Q76 40 84 48" fill="none" stroke="#2A1240" stroke-width="5" stroke-linecap="round"/>
<path d="M36 66 Q58 98 82 66 Z" fill="#2A1240" stroke="#2A1240" stroke-width="4" stroke-linejoin="round"/>
<path d="M48 80 Q58 72 70 80 Q60 90 48 80 Z" fill="#FF5FA8"/></svg>"""
ANNEAU = f"""<svg viewBox="0 0 100 100" class="anneau"><path d="M10 50 A40 40 0 0 1 90 50" fill="none" stroke="{C['violet']}" stroke-width="18"/>
<path d="M90 50 A40 40 0 0 1 10 50" fill="none" stroke="{C['rose']}" stroke-width="18"/><circle cx="78.3" cy="21.7" r="10" fill="{C['creme']}" stroke="#2A1240" stroke-width="2"/></svg>"""
def spark(cls, fill):
    return f"""<svg viewBox="0 0 40 40" class="sp {cls}"><path d="M20 2 C22 14 26 18 38 20 C26 22 22 26 20 38 C18 26 14 22 2 20 C14 18 18 14 20 2 Z" fill="{fill}" stroke="#2A1240" stroke-width="2.5" stroke-linejoin="round"/></svg>"""

def ecocert():
    s = (ICI / "ecocert-cosmos-natural.svg").read_text(encoding="utf-8")
    s = re.sub(r"<\?xml.*?\?>|<!--.*?-->|<!DOCTYPE.*?\]>", "", s, flags=re.S)
    return s.replace("<svg ", '<svg class="eco" ', 1)

def html(guides=False):
    fl, fr = FRONT_CX - FRONT_W / 2, FRONT_CX + FRONT_W / 2
    g = ""
    if guides:
        g = f"""
<div class="g" style="inset:{BLEED}mm; border:.3mm solid #2a6cff"></div>
<div class="g" style="inset:{SAFE}mm; border:.25mm dashed #2a6cff; opacity:.6"></div>
<div class="g" style="left:{INFO_X}mm; top:{BLEED}mm; right:{BLEED}mm; bottom:{BLEED}mm; border:.6mm dashed #FF6A2B;
  background: repeating-linear-gradient(45deg, rgba(255,106,43,.12) 0 2mm, transparent 2mm 4mm);"></div>
<div class="g lab" style="left:{INFO_X + 3}mm; top:48mm; width:28mm">zone des mentions obligatoires<br>(ajoutées par Selfnamed)</div>
<div class="g" style="left:{fl - 2.5}mm; width:{FRONT_W + 5}mm; top:0; bottom:0; border-left:.3mm solid #888; border-right:.3mm solid #888"></div>
<div class="g lab" style="left:{fl - 2.5}mm; top:.3mm; width:{FRONT_W + 5}mm; text-align:center">FACE AVANT</div>
<div class="g lab" style="left:{BLEED + 1}mm; bottom:.2mm">bleu : coupe · pointillés : marge 3 mm · fond perdu 2 mm</div>"""
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Unbounded:wght@700;800&display=block" rel="stylesheet">
<style>
@page {{ size: {W}mm {H}mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {W}mm; height: {H}mm; overflow: hidden; background: transparent; }}
body {{ position: relative; color: {C['aubergine']}; font-family: "Bricolage Grotesque", sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.fond {{ position: absolute; left: 0; top: 0; bottom: 0; width: {INFO_X - 1.2}mm; background: {C['citron']}; overflow: hidden; }}
.fond::after {{ content: ""; position: absolute; right: 0; top: {SAFE}mm; bottom: {SAFE}mm; border-right: .5mm dashed rgba(42,18,64,.35); }}
.anneau {{ position: absolute; width: 44mm; left: -22mm; top: 78mm; transform: rotate(-24deg); }}
.sp {{ position: absolute; }}
.s1 {{ width: 7mm; left: 9mm; top: 14mm; }} .s2 {{ width: 4.5mm; left: 86mm; top: 96mm; }} .s3 {{ width: 5mm; left: 98mm; top: 9mm; }}
.slogan {{ position: absolute; left: 7.5mm; top: 50mm; transform: translate(-50%, -50%) rotate(-90deg); white-space: nowrap;
  font-family: Unbounded, sans-serif; font-weight: 700; font-size: 6.5pt; letter-spacing: .2em; text-transform: uppercase; }}

.front {{ position: absolute; left: {fl}mm; width: {FRONT_W}mm; top: {SAFE + 2}mm; bottom: {SAFE + 1}mm; display: flex; flex-direction: column; align-items: center; text-align: center; }}
.kicker {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: 6pt; letter-spacing: .24em; text-transform: uppercase; }}
.marque {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 25pt; letter-spacing: -.05em; line-height: .9; margin-top: 2.2mm; }}
.bouille {{ width: 21mm; margin: 5mm 0 0 4mm; transform: rotate(8deg); }}
.nom {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 12.5pt; line-height: 1; letter-spacing: -.03em; margin-top: auto; }}
.sous {{ font-weight: 700; font-size: 7pt; margin-top: 1.6mm; line-height: 1.2; }}
.sticker {{ margin-top: 2.6mm; background: {C['violet']}; color: {C['creme']}; border: .55mm solid {C['aubergine']}; border-radius: 99mm;
  padding: .9mm 3mm; font-family: Unbounded, sans-serif; font-weight: 700; font-size: 7pt; box-shadow: .8mm .8mm 0 {C['aubergine']}; transform: rotate(-4deg); }}
.volume {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: 6.5pt; margin-top: 4mm; }}

.side {{ position: absolute; left: 62mm; width: 39mm; top: {SAFE + 2}mm; display: flex; flex-direction: column; gap: 3.2mm; }}
.side h3 {{ font-family: Unbounded, sans-serif; font-weight: 800; font-size: 8pt; letter-spacing: -.01em; margin-bottom: .8mm; }}
.side p {{ font-size: 6.6pt; line-height: 1.3; font-weight: 600; }}
.pastille {{ align-self: flex-start; display: grid; place-items: center; text-align: center; width: 17mm; height: 17mm; border-radius: 50%;
  background: {C['creme']}; border: .55mm solid {C['aubergine']}; box-shadow: .8mm .8mm 0 {C['aubergine']};
  font-family: Unbounded, sans-serif; font-weight: 800; font-size: 9pt; line-height: 1; transform: rotate(8deg); }}
.pastille small {{ display: block; font-family: "Bricolage Grotesque", sans-serif; font-weight: 700; font-size: 5.4pt; margin-top: .6mm; }}
.bas {{ display: flex; align-items: center; gap: 3mm; margin-top: 1mm; }}
.eco {{ width: 13mm; height: 13mm; background: #fff; border-radius: 50%; }}
.g {{ position: absolute; pointer-events: none; }}
.lab {{ font: 700 5pt sans-serif; color: #c2410c; background: rgba(255,255,255,.85); padding: .3mm .8mm; }}
</style></head><body>
<div class="fond">
  {ANNEAU}
  {spark('s1', C['creme'])}{spark('s2', C['rose'])}{spark('s3', C['creme'])}
  <p class="slogan">peau neuve, mine de rien ✦</p>
  <div class="front">
    <p class="kicker">n°07 · visage</p>
    <p class="marque">orane</p>
    {BOUILLE}
    <p class="nom">gel<br>nettoyant</p>
    <p class="sous">purifiant · peaux à imperfections</p>
    <p class="sticker">thé vert</p>
    <p class="volume">140 ml ℮</p>
  </div>
  <div class="side">
    <div><h3>Le geste</h3><p>Une petite noisette sur peau humide. On masse tout doucement, on rince bien. C'est tout, et c'est frais.</p></div>
    <div><h3>Pour qui ?</h3><p>Les peaux à imperfections qui veulent un nettoyage doux, sans tensioactifs agressifs. pH équilibré.</p></div>
    <div><h3>Dedans</h3><p>Maté bio · mousse d'Islande · cals de genévrier. Parfum frais de thé vert.</p></div>
    <div class="bas">
      <p class="pastille"><span>98 %<small>d'origine naturelle</small></span></p>
      {ecocert()}
    </div>
  </div>
</div>
{"" if not guides else g}
</body></html>"""

def main():
    (ICI / "etiquette.html").write_text(html(False), encoding="utf-8")
    (ICI / "apercu.html").write_text(html(True), encoding="utf-8")
    subprocess.run(["node", str(ICI / "rendre.mjs"), str(ICI)], check=True)

if __name__ == "__main__":
    main()
