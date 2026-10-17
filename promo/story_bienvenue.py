"""ORANE — story Instagram 1080x1920 : -10 % sur la première commande, code BIENVENUE10.
Les zones haute (~250 px) et basse (~300 px) restent libres pour l'interface de la story."""
import sys
from PIL import Image, ImageDraw
import render as R
from render import (W, H, MANDARINE, ROSE, CITRON, AUBERGINE, CREME,
                    UNB, BRI, BRI_SB, PANELS, sticker, blob, bouille, wordmark, text_size)
from render_humain import circle_photo

OUT = sys.argv[1] if len(sys.argv) > 1 else f"{R.HERE}/story_bienvenue10.png"
DONE = 99  # instant « tout est en place » pour les fonctions d'animation

def centered(d, txt, f, cy, color):
    tw, th, bx, by = text_size(f, txt)
    d.text((W / 2 - tw / 2 - bx, cy - th / 2 - by), txt, font=f, fill=color)

fr = Image.new("RGB", (W, H), MANDARINE)
blob(fr, ROSE, (1010, 330), 230, 0)
blob(fr, CITRON, (60, 1830), 260, 0, 1.0)
d = ImageDraw.Draw(fr)

# marque
bouille(fr, (540, 255), 52, DONE, 0)
wordmark(fr, (540, 385), 120, AUBERGINE, DONE, 0, pop=False)

# grosse pastille -10 %
cx, cy, r = 540, 780, 330
d.ellipse((cx - r + 22, cy - r + 22, cx + r + 22, cy + r + 22), fill=AUBERGINE)
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=CREME, outline=AUBERGINE, width=12)
centered(d, "-10 %", UNB(150), cy - 40, AUBERGINE)
centered(d, "rien que pour toi", BRI_SB(52), cy + 100, AUBERGINE)

# le pot, dans un rond qui déborde de la pastille
circle_photo(fr, Image.open(f"{R.HERE}/panels/shampooing_n02.png").convert("RGB"), (905, 1000), 150, DONE, 0, DONE, zoom=(1.0, 1.0))

d = ImageDraw.Draw(fr)
centered(d, "sur ta première commande", BRI_SB(62), 1225, AUBERGINE)
centered(d, "avec le code", BRI(50), 1320, AUBERGINE)
sticker(fr, "BIENVENUE10", (540, 1445), CITRON, AUBERGINE, 84, -2, DONE, 0, pad=(56, 34))

sticker(fr, "fais pas ta timide", (330, 1640), ROSE, AUBERGINE, 40, -6, DONE, 0)

fr.save(OUT)
print("ok", OUT)
