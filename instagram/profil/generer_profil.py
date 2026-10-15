"""ORANE — photos de profil Instagram (1080 × 1080, fond blanc, pensées pour le recadrage rond)."""
import json, pathlib
D = pathlib.Path(__file__).resolve().parent
A, MAN, ROSE, CIT = "#2A1240", "#FF6A2B", "#FF5FA8", "#D4F23A"
ANNEAU = (f'<svg viewBox="0 0 100 100" class="ring"><path d="M10 50 A40 40 0 0 1 90 50" fill="none" stroke="{MAN}" stroke-width="18"/>'
          f'<path d="M90 50 A40 40 0 0 1 10 50" fill="none" stroke="{ROSE}" stroke-width="18"/><circle cx="78.3" cy="21.7" r="10" fill="{CIT}"/></svg>')
HEAD = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@800;900&display=block" rel="stylesheet">
<style>* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:1080px; height:1080px; overflow:hidden; background:#fff; }
body { display:grid; place-items:center; font-family:Unbounded,sans-serif; color:%s; }
.word { font-weight:900; letter-spacing:-.05em; line-height:.9; }
.ring { display:block; }
</style></head><body>""" % A
END = "<script>document.fonts.ready.then(()=>document.body.dataset.ready='1')</script></body></html>"
V = {
 "profil-1-symbole": f'<div style="width:620px">{ANNEAU.replace("class=\"ring\"", "class=\"ring\" width=\"620\"")}</div>',
 "profil-2-nom": f'<div style="text-align:center"><p class="word" style="font-size:250px">orane</p></div>',
 "profil-3-symbole-et-nom": f'<div style="display:flex;flex-direction:column;align-items:center;gap:40px">'
     f'{ANNEAU.replace("class=\"ring\"", "class=\"ring\" width=\"400\"")}<p class="word" style="font-size:170px">orane</p></div>',
}
jobs = []
for n, body in V.items():
    (D / f"{n}.html").write_text(HEAD + body + END)
    jobs.append({"html": str(D / f"{n}.html"), "png": str(D / f"{n}.png")})
(D / "jobs.json").write_text(json.dumps(jobs))
