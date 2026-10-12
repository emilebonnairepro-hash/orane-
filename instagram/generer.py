"""ORANE — posts Instagram (1080 × 1350, portrait 4:5) dans l'univers de la marque.

Fond swirl des étiquettes, bouille, couleurs de la charte, polices Unbounded + Bricolage Grotesque.
Usage : python3 instagram/generer.py   → instagram/posts/*.png + instagram/grille.png
Les légendes et hashtags sont dans instagram/LEGENDES.md.
"""
import json, pathlib, subprocess, sys, base64, html as h
from urllib.parse import quote

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent / "etiquettes"))
from couleurs import C, _mix  # noqa: E402

A, CR = C["aubergine"], C["creme"]
SWIRL = (ICI.parent / "etiquettes" / "assets" / "swirl-modele.svg").read_text(encoding="utf-8")
BOUILLE = """<svg viewBox="0 0 120 120" class="{cls}"><circle cx="64" cy="64" r="52" fill="#2A1240"/>
<circle cx="58" cy="58" r="52" fill="#FF6A2B" stroke="#2A1240" stroke-width="5"/>
<ellipse cx="30" cy="70" rx="10" ry="7" fill="#FF5FA8"/><ellipse cx="86" cy="70" rx="10" ry="7" fill="#FF5FA8"/>
<circle cx="42" cy="48" r="7" fill="#2A1240"/>
<path d="M68 48 Q76 40 84 48" fill="none" stroke="#2A1240" stroke-width="5" stroke-linecap="round"/>
<path d="M36 66 Q58 98 82 66 Z" fill="#2A1240" stroke="#2A1240" stroke-width="4" stroke-linejoin="round"/>
<path d="M48 80 Q58 72 70 80 Q60 90 48 80 Z" fill="#FF5FA8"/></svg>"""


def bouille(cls="bouille"):
    return BOUILLE.format(cls=cls)


def spark(style, fill):
    return (f'<svg viewBox="0 0 40 40" class="sp" style="{style}"><path d="M20 2 C22 14 26 18 38 20 C26 22 22 26 20 38 C18 26 14 22 2 20 '
            f'C14 18 18 14 20 2 Z" fill="{fill}" stroke="{A}" stroke-width="2.5" stroke-linejoin="round"/></svg>')


def anneau(a, b, style):
    return (f'<svg viewBox="0 0 100 100" class="ring" style="{style}"><path d="M10 50 A40 40 0 0 1 90 50" fill="none" stroke="{a}" stroke-width="18"/>'
            f'<path d="M90 50 A40 40 0 0 1 10 50" fill="none" stroke="{b}" stroke-width="18"/>'
            f'<circle cx="78.3" cy="21.7" r="10" fill="{CR}" stroke="{A}" stroke-width="2"/></svg>')


def img(nom):
    p = ICI / "assets" / f"{nom}.png"
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


def fond(nom):
    """Fond : couleur pleine + swirl (pâle sur les fonds vifs, sombre sur violet/aubergine) — comme les étiquettes."""
    if nom in ("violet", "aubergine"):
        base, forme = _mix(C[nom], A, .55 if nom == "violet" else 0), (C["violet"] if nom == "aubergine" else C[nom])
        if nom == "violet":
            base, forme = _mix(C["violet"], A, .62), C["violet"]
        else:
            base, forme = A, _mix(A, C["violet"], .45)
    elif nom == "creme":
        base, forme = CR, _mix(C["rose"], CR, .35)
    else:
        base, forme = _mix(C[nom], CR, .82 if nom == "citron" else .5), C[nom]
    texte = CR if nom in ("violet", "aubergine") else A
    svg = SWIRL.replace("#B8ADFF", forme)
    return base, "data:image/svg+xml," + quote(svg), texte


def e(t):
    t = str(t)
    for c in "%?!:":
        t = t.replace(" " + c, " " + c)
    return h.escape(t).replace("\n", "<br>")


CSS = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1080px; height: 1350px; overflow: hidden; }}
body {{ position: relative; font-family: "Bricolage Grotesque", sans-serif; background: var(--base); color: var(--txt); }}
.bg {{ position: absolute; inset: 0; background-image: var(--swirl); background-size: cover; background-position: center; }}
.sp {{ position: absolute; }}
.ring {{ position: absolute; }}
.kicker {{ font-family: Unbounded, sans-serif; font-weight: 700; font-size: 26px; letter-spacing: .22em; text-transform: uppercase; }}
.title {{ font-family: Unbounded, sans-serif; font-weight: 900; letter-spacing: -.05em; line-height: .92; }}
.title em {{ font-style: normal; color: var(--acc); -webkit-text-stroke: 7px {A}; paint-order: stroke fill; }}
.sticker {{ display: inline-block; font-family: Unbounded, sans-serif; font-weight: 800; color: {A}; border: 5px solid {A}; border-radius: 999px;
  padding: 14px 30px; box-shadow: 7px 7px 0 {A}; white-space: nowrap; }}
.card {{ background: {CR}; color: {A}; border: 5px solid {A}; border-radius: 40px; box-shadow: 12px 12px 0 {A}; }}
.foot {{ position: absolute; left: 70px; right: 70px; bottom: 54px; display: flex; justify-content: space-between; align-items: center;
  font-family: Unbounded, sans-serif; font-weight: 700; font-size: 22px; letter-spacing: .14em; text-transform: uppercase; }}
.foot b {{ font-weight: 900; font-size: 40px; letter-spacing: -.04em; text-transform: none; }}
.bottle {{ position: absolute; filter: drop-shadow(0 0 0 transparent); }}
"""

FOOT = '<div class="foot"><b>orane</b><span>peau neuve, mine de rien ✦</span></div>'


def page(fond_nom, corps, acc=None):
    base, sw, txt = fond(fond_nom)
    acc = acc or (C["citron"] if fond_nom in ("violet", "aubergine", "rose", "mandarine") else C["mandarine"])
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Unbounded:wght@700;800;900&display=block" rel="stylesheet">
<style>:root {{ --base: {base}; --swirl: url("{sw}"); --txt: {txt}; --acc: {acc}; }}{CSS}</style></head>
<body><div class="bg"></div>{corps}{FOOT}
<script>document.fonts.ready.then(() => document.body.dataset.ready = '1');</script></body></html>"""


# ------------------------------------------------------------------ les 9 posts
P = []

# 01 — Bienvenue dans la bande
P.append(("01-bienvenue", page("violet", f"""
<p class="kicker" style="position:absolute;left:70px;top:80px">bienvenue dans la bande ✦</p>
{anneau(C['mandarine'], C['rose'], 'width:620px;right:-150px;top:150px;transform:rotate(-18deg)')}
{bouille('bouille" style="position:absolute;width:420px;right:110px;top:270px;transform:rotate(10deg)')}
{spark('width:90px;left:120px;top:250px', C['citron'])}{spark('width:60px;left:560px;top:170px', C['rose'])}
<p class="title" style="position:absolute;left:58px;top:720px;font-size:250px;color:{CR}">orane</p>
<p class="sticker" style="position:absolute;left:70px;top:1010px;font-size:40px;background:{C['citron']};transform:rotate(-4deg)">peau neuve, mine de rien.</p>
<p style="position:absolute;left:74px;top:1130px;font-weight:700;font-size:34px">soins visage · corps · cheveux · homme</p>
""")))

# 02 — Crème corps 5 % d'urée
P.append(("02-creme-corps-uree", page("citron", f"""
<p class="kicker" style="position:absolute;left:70px;top:80px">n°12 · corps</p>
<p class="title" style="position:absolute;left:66px;top:150px;font-size:118px">Peau qui<br>tiraille&nbsp;?<br><em>On gère.</em></p>
<img class="bottle" src="{img('12-creme-corps-uree')}" style="height:700px;right:110px;top:470px;transform:rotate(6deg)">
<p class="sticker" style="position:absolute;left:70px;top:620px;font-size:46px;background:{C['violet']};color:{CR};transform:rotate(-5deg)">5&nbsp;% d'urée</p>
<p class="sticker" style="position:absolute;left:90px;top:760px;font-size:36px;background:{CR};transform:rotate(3deg)">non grasse</p>
<p class="sticker" style="position:absolute;left:70px;top:880px;font-size:36px;background:{C['rose']};transform:rotate(-2deg)">peaux sèches &amp; rugueuses</p>
{spark('width:80px;left:470px;top:1010px', C['rose'])}
""")))

# 03 — Quiz
opts = [("A", "fatiguée du regard"), ("B", "assoiffée mais sans gras"), ("C", "qui tiraille de partout"), ("D", "cheveux en mode botte de foin")]
pills = "".join(f'<li class="sticker" style="font-size:38px;background:{[C["citron"], CR, C["mandarine"], C["violet"]][i]};'
                f'{"color:" + CR + ";" if i == 3 else ""}transform:rotate({[-3, 2, -1, 3][i]}deg)"><b style="margin-right:18px">{k}</b>{e(v)}</li>'
                for i, (k, v) in enumerate(opts))
P.append(("03-quiz", page("rose", f"""
<p class="kicker" style="position:absolute;left:70px;top:80px">le quiz qui dure 2 secondes</p>
<p class="title" style="position:absolute;left:66px;top:150px;font-size:112px">Ta peau,<br>là, <em>maintenant</em>&nbsp;?</p>
<ul style="position:absolute;left:70px;top:560px;list-style:none;display:grid;gap:34px;justify-items:start">{pills}</ul>
{bouille('bouille" style="position:absolute;width:200px;right:90px;top:130px;transform:rotate(-8deg)')}
<p class="card" style="position:absolute;left:70px;top:1060px;padding:22px 34px;font-weight:800;font-size:34px;transform:rotate(-1.5deg)">Réponds en commentaire, on te trouve ton match ✦</p>
""")))

# 04 — Routine cheveux
steps = [("1", "on lave", "shampooing n°02", "02-shampooing-cuir-chevelu-sensible"),
         ("2", "on démêle", "après-shampooing n°17", "17-apres-shampooing-hydratant"),
         ("3", "on chouchoute", "masque kératine n°16 · 1×/sem", "16-masque-capillaire-keratine")]
cols = "".join(f'''<div style="position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;gap:14px">
  <p class="title" style="font-size:150px;color:transparent;-webkit-text-stroke:5px {A}">{n}</p>
  <div style="height:330px;display:flex;align-items:flex-end"><img src="{img(f)}" style="max-height:330px;max-width:290px"></div>
  <p style="font-family:Unbounded;font-weight:900;font-size:38px">{e(t)}</p><p style="font-weight:700;font-size:25px">{e(s)}</p></div>'''
               for n, t, s, f in steps)
P.append(("04-routine-cheveux", page("mandarine", f"""
<p class="kicker" style="position:absolute;left:70px;top:80px">la routine cheveux</p>
<p class="title" style="position:absolute;left:66px;top:150px;font-size:104px">3 gestes,<br><em>zéro prise</em><br>de tête.</p>
<div style="position:absolute;left:40px;right:40px;top:560px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px">{cols}</div>
""")))

# 05 — Ce qu'on ne fera jamais
nev = ["Te promettre des miracles", "Te noyer sous le jargon", "Chuchoter en nude", "Se prendre au sérieux"]
lis = "".join(f'<li style="display:flex;gap:26px;align-items:baseline"><span class="sticker" style="font-size:26px;padding:6px 18px;background:{C["citron"]};box-shadow:4px 4px 0 {C["violet"]}">0{i + 1}</span>'
              f'<span style="font-family:Unbounded;font-weight:900;font-size:48px;line-height:1.08;letter-spacing:-.03em;white-space:nowrap;background:linear-gradient({C["mandarine"]},{C["mandarine"]}) no-repeat 0 60%/100% .26em">{e(t)}</span></li>' for i, t in enumerate(nev))
P.append(("05-jamais", page("aubergine", f"""
<p class="kicker" style="position:absolute;left:70px;top:80px;color:{C['citron']}">promis, juré</p>
<p class="title" style="position:absolute;left:66px;top:150px;font-size:118px">Ce qu'on<br>ne fera <em>jamais</em>.</p>
<ul style="position:absolute;left:70px;right:70px;top:540px;list-style:none;display:grid;gap:44px">{lis}</ul>
{bouille('bouille" style="position:absolute;width:200px;right:70px;top:1000px;transform:rotate(12deg)')}
""", acc=C["mandarine"])))

# 06 — SPF 30
P.append(("06-spf30", page("creme", f"""
<p class="kicker" style="position:absolute;left:70px;top:80px">n°08 · visage</p>
<p class="title" style="position:absolute;left:66px;top:150px;font-size:100px">Le soleil,<br>oui. Les traces<br><em>blanches</em>, non.</p>
<img class="bottle" src="{img('08-creme-solaire-teintee-spf30')}" style="height:680px;right:110px;top:500px;transform:rotate(-5deg)">
<p class="sticker" style="position:absolute;left:70px;top:640px;font-size:96px;background:{C['citron']};transform:rotate(-6deg)">SPF 30</p>
<p class="sticker" style="position:absolute;left:80px;top:860px;font-size:36px;background:{C['rose']};transform:rotate(3deg)">teintée · fini naturel</p>
<p class="sticker" style="position:absolute;left:70px;top:980px;font-size:36px;background:{CR};transform:rotate(-2deg)">filtre minéral</p>
""", acc=C["rose"])))

# 07 — Ça ou ça ?
P.append(("07-ca-ou-ca", page("citron", f"""
<p class="kicker" style="position:absolute;left:70px;top:80px">le grand duel</p>
<p class="title" style="position:absolute;left:0;right:0;top:150px;text-align:center;font-size:132px">Ça ou <em>ça</em>&nbsp;?</p>
<img class="bottle" src="{img('13-gel-douche-cardamome')}" style="height:580px;left:120px;top:390px;transform:rotate(-6deg)">
<img class="bottle" src="{img('14-gel-douche-vanille-ambree')}" style="height:580px;right:120px;top:390px;transform:rotate(6deg)">
<p class="sticker" style="position:absolute;left:455px;top:620px;font-size:56px;background:{C['violet']};color:{CR};transform:rotate(-8deg)">VS</p>
<p class="sticker" style="position:absolute;left:70px;top:1010px;font-size:34px;background:{C['mandarine']};transform:rotate(-3deg)">🌶 cardamome &amp; gingembre</p>
<p class="sticker" style="position:absolute;right:70px;top:1110px;font-size:34px;background:{CR};transform:rotate(3deg)">vanille ambrée 🍦</p>
""")))

# 08 — L'actif décrypté : acide hyaluronique
P.append(("08-actif-hyaluronique", page("rose", f"""
<p class="kicker" style="position:absolute;left:70px;top:80px">l'actif décrypté</p>
<p class="title" style="position:absolute;left:66px;top:150px;font-size:100px">L'acide<br><em>hyaluronique</em>,<br>en vrai&nbsp;?</p>
<div class="card" style="position:absolute;left:70px;right:70px;top:610px;padding:50px 56px;transform:rotate(-1.5deg)">
  <p style="font-family:Unbounded;font-weight:900;font-size:58px;line-height:1.05;letter-spacing:-.03em">Il retient l'eau<br>comme une éponge.</p>
  <p style="font-weight:700;font-size:34px;margin-top:24px;line-height:1.3">Résultat : la peau a l'air plus rebondie et reste hydratée plus longtemps.</p>
</div>
<p class="sticker" style="position:absolute;left:70px;top:1060px;font-size:30px;background:{C['citron']};transform:rotate(-3deg)">dans nos n°08 · n°10 · n°11</p>
{bouille('bouille" style="position:absolute;width:190px;right:80px;top:1010px;transform:rotate(10deg)')}
""", acc=C["citron"])))

# 09 — La bouille (humour)
P.append(("09-moi-apres-masque", page("violet", f"""
<p class="kicker" style="position:absolute;left:70px;top:80px;color:{C['citron']}">mood du dimanche soir</p>
<p class="title" style="position:absolute;left:66px;top:150px;font-size:96px;color:{CR}">Moi après<br>10 minutes de<br><em>masque à l'argile</em></p>
{anneau(C['citron'], C['rose'], 'width:600px;left:240px;top:580px;transform:rotate(-12deg)')}
{bouille('bouille" style="position:absolute;width:440px;left:320px;top:660px;transform:rotate(-6deg)')}
<p class="sticker" style="position:absolute;left:70px;top:620px;font-size:34px;background:{C['citron']};transform:rotate(-6deg)">pores : 0</p>
<p class="sticker" style="position:absolute;right:70px;top:1080px;font-size:34px;background:{C['rose']};transform:rotate(4deg)">moi : 1</p>
{spark('width:80px;left:150px;top:900px', C['citron'])}{spark('width:56px;right:150px;top:640px', C['rose'])}
""", acc=C["rose"])))


def main():
    out = ICI / "posts"; out.mkdir(exist_ok=True)
    src = ICI / "source"; src.mkdir(exist_ok=True)
    jobs = []
    for nom, html in P:
        f = src / f"{nom}.html"; f.write_text(html, encoding="utf-8")
        jobs.append({"html": str(f), "png": str(out / f"{nom}.png")})
    (src / "jobs.json").write_text(json.dumps(jobs))
    subprocess.run(["node", str(ICI / "rendre.mjs"), str(src / "jobs.json")], check=True)
    (src / "jobs.json").unlink()
    # aperçu de la grille du profil (le post le plus récent s'affiche en haut à gauche)
    from PIL import Image
    ims = [Image.open(j["png"]).convert("RGB").resize((360, 450)) for j in reversed(jobs)]
    g = Image.new("RGB", (360 * 3 + 8, 450 * 3 + 8), "white")
    for i, im in enumerate(ims):
        g.paste(im, ((i % 3) * 364, (i // 3) * 454))
    g.save(ICI / "grille.png")


if __name__ == "__main__":
    main()
