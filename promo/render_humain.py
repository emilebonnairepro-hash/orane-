"""ORANE — masque kératine N°16, version « plus humaine ».
Même charte et mêmes outils que render.py, mais la photo du rituel est
déclinée en plusieurs plans (cheveux, profil, geste) répartis dans la vidéo."""
import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
import render as R
from render import (W, H, FPS, MANDARINE, ROSE, VIOLET, CITRON, PISCINE, AUBERGINE, CREME,
                    UNB, BRI, BRI_SB, PANELS, prog, clamp, ease_out, ease_in_out, back_out,
                    photo_card, sticker, headline, blob, bouille, wordmark, text_size)

HERE = sys.path[0]
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{HERE}/orane_masque_keratine_promo_humain.mp4"

def soften(img):
    """Les recadrages sont très agrandis : on lisse puis on remet un peu de piqué."""
    return img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))

P5 = PANELS[5]
HUMAN = {
    "cheveux": soften(P5.crop((0, 0, 260, 420))),      # longueurs, plan vertical
    "profil": soften(P5.crop((140, 10, 330, 260))),    # nuque et profil
    "reflets": soften(P5.crop((0, 150, 210, 420))),    # pointes brillantes
    "geste": P5,                                       # plan large du rituel
}

def circle_photo(frame, img, center, r, t_local, start, dur, zoom=(1.05, 1.15)):
    """Photo dans un rond, contour aubergine et ombre en aplat."""
    p = back_out(prog(t_local, start, 0.55), 1.8)
    if p <= 0: return
    rr = int(r * p)
    if rr < 4: return
    k = ease_in_out(t_local / dur)
    z = zoom[0] + (zoom[1] - zoom[0]) * k
    d = 2 * rr
    cover = max(d / img.width, d / img.height) * z
    im = img.resize((math.ceil(img.width * cover), math.ceil(img.height * cover)), Image.LANCZOS)
    ox, oy = (im.width - d) // 2, (im.height - d) // 2
    im = im.crop((ox, oy, ox + d, oy + d))
    S = 3
    def disc(size):
        m = Image.new("L", (size * S, size * S), 0)
        ImageDraw.Draw(m).ellipse((0, 0, size * S - 1, size * S - 1), fill=255)
        return m.resize((size, size), Image.LANCZOS)
    bw = 10
    cx, cy = int(center[0]), int(center[1])
    sh = Image.new("RGB", (d + 2 * bw, d + 2 * bw), AUBERGINE)
    frame.paste(sh, (cx - rr - bw + 18, cy - rr - bw + 18), disc(d + 2 * bw))
    frame.paste(sh, (cx - rr - bw, cy - rr - bw), disc(d + 2 * bw))
    frame.paste(im, (cx - rr, cy - rr), disc(d))

# Scènes
def s_accroche(fr, t, D):
    blob(fr, ROSE, (980, 1500), 260, t)
    photo_card(fr, HUMAN["cheveux"], t, D, (90, 140, 900, 1180), zoom=(1.05, 1.18), pan=(0, 0.6))
    headline(fr, ["tes cheveux", "font la tête ?"], 90, 1420, AUBERGINE, 92, t, 0.45)
    sticker(fr, "on s'en occupe.", (700, 1760), CITRON, AUBERGINE, 46, -5, t, 1.4)

def s_logo(fr, t, D):
    blob(fr, MANDARINE, (920, 330), 250, t)
    blob(fr, CITRON, (140, 1640), 190, t, 1.3)
    bouille(fr, (540, 660), 115, t, 0.05)
    wordmark(fr, (540, 940), 230, AUBERGINE, t, 0.2)
    headline(fr, ["peau neuve,", "mine de rien."], 540, 1160, AUBERGINE, 0, t, 0.6, align="center", f=BRI_SB(72))

def s_hero(fr, t, D):
    blob(fr, MANDARINE, (980, 280), 300, t)
    headline(fr, ["N°16 · cheveux"], 90, 170, AUBERGINE, 0, t, 0.1, f=BRI_SB(46))
    headline(fr, ["masque", "kératine"], 90, 240, AUBERGINE, 104, t, 0.2)
    photo_card(fr, PANELS[1], t, D, (90, 600, 900, 1000), zoom=(1.05, 1.18), pan=(0.2, -0.1), appear=0.05)
    sticker(fr, "fais pas ta timide", (600, 1640), ROSE, AUBERGINE, 46, -4, t, 0.9)

def s_texture(fr, t, D):
    headline(fr, ["une texture", "qui fond."], 90, 170, CREME, 100, t, 0.1)
    photo_card(fr, PANELS[4], t, D, (90, 500, 760, 880), zoom=(1.0, 1.15), pan=(0.25, 0.1), appear=0.05)
    circle_photo(fr, HUMAN["profil"], (800, 1420), 220, t, 0.6, D)
    sticker(fr, "glow à la carte", (330, 1560), CITRON, AUBERGINE, 46, 5, t, 1.0)

def s_rituel(fr, t, D):
    blob(fr, PISCINE, (960, 230), 160, t)
    photo_card(fr, HUMAN["geste"], t, D, (90, 170, 900, 1080), zoom=(1.18, 1.0), pan=(0.35, 0.2))
    # les trois gestes arrivent un par un
    for i, mot in enumerate(["applique,", "patiente,", "rince."]):
        headline(fr, [mot], 90, 1350 + i * 110, AUBERGINE, 92, t, 0.5 + i * 0.55)
    sticker(fr, "bouille de star", (780, 1240), ROSE, AUBERGINE, 42, -6, t, 2.1)

def s_reflets(fr, t, D):
    blob(fr, CITRON, (130, 260), 200, t, 0.6)
    photo_card(fr, HUMAN["reflets"], t, D, (90, 140, 720, 1080), zoom=(1.05, 1.2), pan=(0, -0.5))
    photo_card(fr, PANELS[2], t, D, (560, 820, 430, 470), zoom=(1.0, 1.1), appear=0.5)
    headline(fr, ["souples,", "brillants,", "pas sages."], 90, 1380, AUBERGINE, 96, t, 0.7)

def s_naturel(fr, t, D):
    R.s_naturel(fr, t, D)

def s_campagne(fr, t, D):
    photo_card(fr, PANELS[6], t, D, (90, 170, 900, 1020), zoom=(1.18, 1.0))
    circle_photo(fr, HUMAN["cheveux"], (860, 1140), 150, t, 0.5, D)
    headline(fr, ["masque", "kératine"], 540, 1340, CREME, 110, t, 0.35, align="center")
    headline(fr, ["N°16 · 170 ml"], 540, 1600, CREME, 0, t, 0.6, align="center", f=BRI_SB(56))
    sticker(fr, "brillance", (540, 1760), CITRON, AUBERGINE, 50, -3, t, 0.95)

def s_outro(fr, t, D):
    R.s_outro(fr, t, D)

SCENES = [
    (3.0, MANDARINE, s_accroche),
    (2.3, ROSE, s_logo),
    (2.8, CREME, s_hero),
    (3.0, VIOLET, s_texture),
    (3.6, MANDARINE, s_rituel),
    (3.0, ROSE, s_reflets),
    (2.8, CREME, s_naturel),
    (3.2, AUBERGINE, s_campagne),
    (3.4, AUBERGINE, s_outro),
]
CORNERS = [(W, H), (0, 0), (W, 0), (0, H), (W, H), (0, 0), (W, 0), (W // 2, H), (W // 2, H // 2)]

if __name__ == "__main__":
    # même moteur que render.py : on lui passe nos scènes
    R.SCENES[:] = SCENES
    R.OUT = OUT
    if len(sys.argv) > 2 and sys.argv[2] == "stills":
        for i, (D, _, _) in enumerate(SCENES):
            R.render_scene(i, D * 0.8).save(f"{sys.argv[3]}/still_h{i}.png")
    else:
        R.CORNERS = CORNERS
        R.main()
