"""ORANE — masque kératine N°16 : vidéo promo verticale 1080x1920, 30 i/s.
Rendu image par image avec PIL, envoyé à ffmpeg sur stdin."""
import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = sys.path[0]
W, H, FPS = 1080, 1920, 30
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{HERE}/orane_masque_keratine_promo.mp4"

# Charte
MANDARINE = (255, 106, 43)
ROSE = (255, 95, 168)
VIOLET = (107, 44, 245)
CITRON = (212, 242, 58)
PISCINE = (44, 200, 245)
AUBERGINE = (42, 18, 64)
CREME = (255, 243, 227)

def font(name, size):
    return ImageFont.truetype(f"{HERE}/fonts/{name}.ttf", size)

UNB = lambda s: font("Unbounded-ExtraBold", s)
BRI = lambda s: font("Bricolage-Regular", s)
BRI_SB = lambda s: font("Bricolage-SemiBold", s)

PANELS = {i: Image.open(f"{HERE}/panels/p{i}.png").convert("RGB") for i in range(1, 7)}

# Easing
def clamp(x): return max(0.0, min(1.0, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_in_out(x): x = clamp(x); return x * x * (3 - 2 * x)
def back_out(x, s=1.9):
    x = clamp(x); x -= 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2
def prog(t, start, dur): return clamp((t - start) / dur)

# Éléments graphiques
def rounded_mask(size, r, scale=3):
    w, h = size
    m = Image.new("L", (w * scale, h * scale), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * scale - 1, h * scale - 1), r * scale, fill=255)
    return m.resize(size, Image.LANCZOS)

def photo_card(frame, panel, t_local, dur, box, zoom=(1.0, 1.12), pan=(0, 0), appear=0.0):
    """Photo dans une carte arrondie, contour aubergine épais, ombre portée pleine (aplat)."""
    x, y, w, h = box
    p = ease_out(prog(t_local, appear, 0.55))
    if p <= 0: return
    # entrée : montée + léger rebond d'échelle
    sc = 0.9 + 0.1 * back_out(prog(t_local, appear, 0.6))
    y_off = int((1 - p) * 140)
    cw, ch = int(w * sc), int(h * sc)
    cx, cy = x + (w - cw) // 2, y + (h - ch) // 2 + y_off
    # Ken Burns
    k = ease_in_out(t_local / dur)
    z = zoom[0] + (zoom[1] - zoom[0]) * k
    pw, ph = panel.size
    cover = max(cw / pw, ch / ph) * z
    img = panel.resize((math.ceil(pw * cover), math.ceil(ph * cover)), Image.LANCZOS)
    ox = (img.width - cw) / 2 + pan[0] * k * (img.width - cw) / 2
    oy = (img.height - ch) / 2 + pan[1] * k * (img.height - ch) / 2
    img = img.crop((int(ox), int(oy), int(ox) + cw, int(oy) + ch))
    r, bw = 56, 10
    # ombre en aplat aubergine décalée
    sh = Image.new("RGB", (cw + 2 * bw, ch + 2 * bw), AUBERGINE)
    frame.paste(sh, (cx - bw + 22, cy - bw + 22), rounded_mask(sh.size, r + bw))
    frame.paste(sh, (cx - bw, cy - bw), rounded_mask(sh.size, r + bw))
    frame.paste(img, (cx, cy), rounded_mask((cw, ch), r))

def text_size(f, s):
    b = f.getbbox(s); return b[2] - b[0], b[3] - b[1], b[0], b[1]

def sticker(frame, text, center, fill, ink, size, angle, t_local, start, pad=(44, 26), f=None):
    """Pastille arrondie, contour aubergine, qui « tamponne » en place."""
    p = prog(t_local, start, 0.45)
    if p <= 0: return
    s = back_out(p, 2.6)
    f = f or UNB(size)
    tw, th, bx, by = text_size(f, text)
    w, h = tw + 2 * pad[0], th + 2 * pad[1]
    bw = 7
    S = 2
    im = Image.new("RGBA", ((w + 2 * bw + 16) * S, (h + 2 * bw + 16) * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((8 * S + 10 * S, 8 * S + 10 * S, (8 + w + 2 * bw) * S, (8 + h + 2 * bw) * S), (h // 2 + bw) * S, fill=AUBERGINE)
    d.rounded_rectangle((8 * S, 8 * S, (8 + w + 2 * bw - 10) * S, (8 + h + 2 * bw - 10) * S), (h // 2 + bw) * S, fill=AUBERGINE)
    d.rounded_rectangle(((8 + bw) * S, (8 + bw) * S, (8 + w + bw - 10) * S, (8 + h + bw - 10) * S), (h // 2) * S, fill=fill)
    fS = font(f.path.rsplit("/", 1)[1][:-4], f.size * S)
    d.text(((8 + bw + pad[0] - 5) * S - bx * S, (8 + bw + pad[1] - 5) * S - by * S), text, font=fS, fill=ink)
    im = im.resize((max(1, int(im.width / S * s)), max(1, int(im.height / S * s))), Image.LANCZOS)
    im = im.rotate(angle * (1 - 0.35 * (1 - clamp(p * 1.5))), resample=Image.BICUBIC, expand=True)
    frame.paste(im, (int(center[0] - im.width / 2), int(center[1] - im.height / 2)), im)

def headline(frame, lines, x, y, color, size, t_local, start, align="left", lh=1.12, f=None, stagger=0.09):
    """Lignes de titre qui montent, une à une, derrière un masque."""
    f = f or UNB(size)
    d = ImageDraw.Draw(frame)
    yy = y
    for i, line in enumerate(lines):
        p = ease_out(prog(t_local, start + i * stagger, 0.5))
        tw, th, bx, by = text_size(f, line)
        lh_px = int(f.size * lh)
        if p > 0:
            layer = Image.new("RGBA", (tw + 40, lh_px + 40), (0, 0, 0, 0))
            ImageDraw.Draw(layer).text((20 - bx, 20 + int((1 - p) * lh_px)), line, font=f, fill=color)
            lx = x if align == "left" else (x - tw // 2 if align == "center" else x - tw)
            frame.paste(layer, (lx - 20, yy - 20), layer)
        yy += lh_px

def blob(frame, color, center, radius, t, phase=0.0):
    """Rond qui respire doucement en fond (rond partout)."""
    r = radius * (1 + 0.04 * math.sin(t * 2.2 + phase))
    d = ImageDraw.Draw(frame)
    d.ellipse((center[0] - r, center[1] - r, center[0] + r, center[1] + r), fill=color)

def bouille(frame, center, r, t_local, start, color=AUBERGINE, wink=False):
    """La bouille : anneau + yeux + sourire, comme sur le label."""
    p = back_out(prog(t_local, start, 0.5), 2.2)
    if p <= 0: return
    S = 3
    R = int(r * p)
    if R < 2: return
    im = Image.new("RGBA", (2 * R * S + 8, 2 * R * S + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = R * S + 4
    lw = max(2, int(R * S * 0.13))
    d.ellipse((c - R * S + lw // 2, c - R * S + lw // 2, c + R * S - lw // 2, c + R * S - lw // 2), outline=color, width=lw)
    er = R * S * 0.11
    for ex in (-0.33, 0.33):
        exx, eyy = c + ex * R * S, c - 0.18 * R * S
        if wink and ex > 0:
            d.line((exx - er, eyy, exx + er, eyy), fill=color, width=int(er * 0.9))
        else:
            d.ellipse((exx - er, eyy - er, exx + er, eyy + er), fill=color)
    sr = R * S * 0.42
    d.arc((c - sr, c - sr * 0.55, c + sr, c + sr * 1.05), 25, 155, fill=color, width=lw)
    im = im.resize((im.width // S, im.height // S), Image.LANCZOS)
    frame.paste(im, (int(center[0] - im.width / 2), int(center[1] - im.height / 2)), im)

def wordmark(frame, center, size, color, t_local, start, pop=True):
    f = UNB(size)
    tw, th, bx, by = text_size(f, "orane")
    p = back_out(prog(t_local, start, 0.6), 2.0) if pop else 1
    if p <= 0: return
    layer = Image.new("RGBA", (tw + 80, th + 80), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((40 - bx, 40 - by), "orane", font=f, fill=color)
    layer = layer.resize((max(1, int(layer.width * p)), max(1, int(layer.height * p))), Image.LANCZOS)
    frame.paste(layer, (int(center[0] - layer.width / 2), int(center[1] - layer.height / 2)), layer)

# Scènes : (durée, couleur de fond, fonction de dessin)
def s_intro(fr, t, D):
    blob(fr, ROSE, (900, 330), 260, t)
    blob(fr, CITRON, (150, 1650), 200, t, 1.3)
    bouille(fr, (540, 640), 120, t, 0.15)
    wordmark(fr, (540, 930), 230, AUBERGINE, t, 0.35)
    headline(fr, ["peau neuve,", "mine de rien."], 540, 1160, AUBERGINE, 0, t, 0.85, align="center", f=BRI_SB(72))
    sticker(fr, "nouveau !", (800, 1430), CITRON, AUBERGINE, 52, -8, t, 1.4)

def s_hero(fr, t, D):
    blob(fr, MANDARINE, (980, 280), 300, t)
    headline(fr, ["N°16 · cheveux"], 90, 170, AUBERGINE, 0, t, 0.1, f=BRI_SB(46))
    headline(fr, ["masque", "kératine"], 90, 240, AUBERGINE, 104, t, 0.2)
    photo_card(fr, PANELS[1], t, D, (90, 600, 900, 1000), zoom=(1.05, 1.18), pan=(0.2, -0.1), appear=0.05)
    sticker(fr, "fais pas ta timide", (600, 1640), ROSE, AUBERGINE, 46, -4, t, 1.0)

def s_detail(fr, t, D):
    blob(fr, CITRON, (120, 1720), 240, t, 0.7)
    photo_card(fr, PANELS[2], t, D, (90, 170, 900, 1060), zoom=(1.0, 1.22), pan=(-0.3, -0.2))
    headline(fr, ["réparateur", "intensif."], 90, 1350, AUBERGINE, 100, t, 0.45)
    headline(fr, ["Kératine hydrolysée, complexe", "biomimétique et karité."], 92, 1625, AUBERGINE, 0, t, 0.8, f=BRI(44), lh=1.4, stagger=0.06)

def s_texture(fr, t, D):
    blob(fr, ROSE, (1000, 1650), 260, t)
    headline(fr, ["une texture", "qui fond."], 90, 170, CREME, 100, t, 0.1)
    photo_card(fr, PANELS[4], t, D, (90, 500, 900, 1080), zoom=(1.0, 1.15), pan=(0.25, 0.1), appear=0.05)
    sticker(fr, "glow à la carte", (560, 1700), CITRON, AUBERGINE, 50, 5, t, 0.9)

def s_rituel(fr, t, D):
    blob(fr, PISCINE, (960, 260), 170, t)
    photo_card(fr, PANELS[5], t, D, (90, 170, 900, 1120), zoom=(1.0, 1.12), pan=(-0.15, 0.1))
    headline(fr, ["souples,", "brillants,", "pas sages."], 90, 1390, AUBERGINE, 96, t, 0.4)
    sticker(fr, "bouille de star", (790, 1270), ROSE, AUBERGINE, 42, -6, t, 1.1)

def s_naturel(fr, t, D):
    blob(fr, MANDARINE, (110, 330), 220, t, 0.4)
    photo_card(fr, PANELS[3], t, D, (90, 640, 900, 1060), zoom=(1.0, 1.14), pan=(0.0, 0.25), appear=0.05)
    # gros chiffre dans un rond
    p = back_out(prog(t, 0.35, 0.55), 2.0)
    if p > 0:
        r = int(220 * p)
        d = ImageDraw.Draw(fr)
        d.ellipse((760 - r + 12, 450 - r + 12, 760 + r + 12, 450 + r + 12), fill=AUBERGINE)
        d.ellipse((760 - r, 450 - r, 760 + r, 450 + r), fill=CREME, outline=AUBERGINE, width=max(1, int(10 * p)))
        if p > 0.6:
            f1, f2 = UNB(int(118 * p)), BRI_SB(int(40 * p))
            for txt, f, dy in (("98 %", f1, -40), ("d'origine", f2, 50), ("naturelle", f2, 95)):
                tw, th, bx, by = text_size(f, txt)
                d.text((760 - tw / 2 - bx, 450 + dy * p - th / 2 - by), txt, font=f, fill=AUBERGINE)
    headline(fr, ["zéro", "filtre,"], 90, 210, AUBERGINE, 96, t, 0.1)
    headline(fr, ["juste du bon."], 92, 470, AUBERGINE, 0, t, 0.3, f=BRI_SB(52))

def s_campagne(fr, t, D):
    photo_card(fr, PANELS[6], t, D, (90, 170, 900, 1020), zoom=(1.18, 1.0))
    headline(fr, ["masque", "kératine"], 540, 1300, CREME, 110, t, 0.35, align="center")
    headline(fr, ["N°16 · 170 ml"], 540, 1560, CREME, 0, t, 0.6, align="center", f=BRI_SB(56))
    sticker(fr, "brillance", (540, 1720), CITRON, AUBERGINE, 50, -3, t, 0.95)

def s_outro(fr, t, D):
    blob(fr, VIOLET, (540, 960), 640, t)
    bouille(fr, (540, 640), 110, t, 0.1, color=CREME, wink=t > 1.3 and t < 1.6)
    wordmark(fr, (540, 920), 230, CREME, t, 0.25)
    headline(fr, ["peau neuve, mine de rien."], 540, 1130, CREME, 0, t, 0.7, align="center", f=BRI_SB(58))
    sticker(fr, "100 % pep's", (540, 1430), CITRON, AUBERGINE, 50, 4, t, 1.15)

SCENES = [
    (2.8, MANDARINE, s_intro),
    (3.2, CREME, s_hero),
    (3.0, ROSE, s_detail),
    (3.0, VIOLET, s_texture),
    (3.2, MANDARINE, s_rituel),
    (3.0, CREME, s_naturel),
    (3.2, AUBERGINE, s_campagne),
    (3.4, AUBERGINE, s_outro),
]
TRANS = 0.42  # transition : rond qui s'ouvre depuis un coin

def render_scene(i, t_local):
    D, bg, fn = SCENES[i]
    fr = Image.new("RGB", (W, H), bg)
    fn(fr, t_local, D)
    return fr

def main():
    starts, acc = [], 0.0
    for D, _, _ in SCENES:
        starts.append(acc); acc += D
    total = acc
    n = int(round(total * FPS))
    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    corners = [(W, H), (0, 0), (W, 0), (0, H), (W, H), (0, 0), (W // 2, H), (W // 2, H // 2)]
    for k in range(n):
        t = k / FPS
        i = max(j for j in range(len(SCENES)) if starts[j] <= t + 1e-9)
        tl = t - starts[i]
        fr = render_scene(i, tl)
        if i > 0 and tl < TRANS:
            # la scène précédente reste visible, la nouvelle s'ouvre en cercle par-dessus
            prev = render_scene(i - 1, SCENES[i - 1][0] + tl)
            p = ease_in_out(tl / TRANS)
            cx, cy = corners[i]
            rmax = math.hypot(max(cx, W - cx), max(cy, H - cy))
            m = Image.new("L", (W, H), 0)
            r = rmax * p
            ImageDraw.Draw(m).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
            prev.paste(fr, (0, 0), m)
            fr = prev
        # fondu de sortie final
        if t > total - 0.35:
            fr = Image.blend(fr, Image.new("RGB", (W, H), AUBERGINE), clamp((t - (total - 0.35)) / 0.35))
        ff.stdin.write(fr.tobytes())
        if k % 60 == 0: print(f"{k}/{n}", flush=True)
    ff.stdin.close(); ff.wait()
    print("ok", OUT, f"{total:.1f}s")

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "stills":
        # aperçus : une image au milieu de chaque scène
        for i, (D, _, _) in enumerate(SCENES):
            render_scene(i, D * 0.75).save(f"{HERE}/still_{i}.png")
    else:
        main()
