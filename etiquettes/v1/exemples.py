"""Un exemple d'étiquette par catégorie (sur le gabarit du gel nettoyant) → etiquettes/v1/exemples/4-categories.png"""
import sys, json, copy, subprocess, pathlib
ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI)); import v1
base = json.load(open(ICI / "produits/07-gel-nettoyant-purifiant.json"))
ex = {
 "visage": base["produit"],
 "corps": {"numero": "01", "univers": "corps", "nom": ["gel", "lavant"], "sous_titre": "mains & corps · tous types de peau", "sticker": "pamplemousse",
   "cote": [["Le geste", "Sur peau humide, fais mousser, puis rince abondamment."], ["Ce qu'on aime", "Nettoie mains et corps sans dessécher. Parfum frais de pamplemousse."], ["Dedans", "Bétaïne et ingrédients hydratants. Formule végétalienne."]]},
 "cheveux": {"numero": "02", "univers": "cheveux", "nom": ["shampooing"], "sous_titre": "cuir chevelu sensible", "sticker": "tout doux",
   "cote": [["Pour qui ?", "Les cuirs chevelus délicats ou facilement irrités."], ["Ce qu'on aime", "Lave en douceur, pour un cuir chevelu confortable. Testé dermatologiquement."], ["Dedans", "Bétaïne et protéines de blé. Délicatement parfumé."]],
   "logos": ["ecocert-cosmos-natural.svg"]},
 "homme": {"numero": "03", "univers": "homme", "nom": ["huile", "à barbe"], "sous_titre": "adoucissante · non grasse", "sticker": "barbe douce",
   "cote": [["Le geste", "Quelques gouttes dans les paumes, puis sur la barbe."], ["Ce qu'on aime", "Adoucit la barbe et facilite le coiffage. Absorbée rapidement."], ["Dedans", "Mélange d'huiles naturelles et 1 % de CBD."]]},
}
D = ICI / "exemples"; jobs = []
for u, p in ex.items():
    sp = copy.deepcopy(base); sp["produit"] = p; out = D / u; out.mkdir(parents=True, exist_ok=True)
    (out / "etiquette.html").write_text(v1.page(sp, False)); (out / "apercu.html").write_text(v1.page(sp, False))
    jobs.append({"dir": str(out), "w": 142.5, "h": 109, "px": [1600, 1224]})
(D / "jobs.json").write_text(json.dumps(jobs))
subprocess.run(["node", str(ICI.parent / "calque/rendre.mjs"), str(D / "jobs.json")], check=True); (D / "jobs.json").unlink()
from PIL import Image, ImageDraw, ImageFont
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
ims = []
for u in ex:
    i = Image.open(D / u / "etiquette.png").convert("RGBA"); w, h = i.size; i = i.crop((0, 0, int(w * .755), h))
    bg = Image.new("RGB", i.size, "white"); bg.paste(i, mask=i.split()[3]); bg = bg.resize((bg.size[0] // 2, bg.size[1] // 2)); ims.append((u, bg))
cw, ch = ims[0][1].size
s = Image.new("RGB", (cw * 2 + 30, (ch + 50) * 2 + 10), "#FFF3E3"); d = ImageDraw.Draw(s)
for k, (u, i) in enumerate(ims):
    x = (k % 2) * (cw + 30); y = (k // 2) * (ch + 50)
    d.text((x + 6, y + 8), u.upper(), fill="#2A1240", font=f); s.paste(i, (x, y + 48))
s.save(D / "4-categories.png")
