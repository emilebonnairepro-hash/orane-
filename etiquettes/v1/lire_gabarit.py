"""Lit les repères d'un gabarit Illustrator Selfnamed (.ai) : calques, lignes verticales, étendue des zones à éviter (en mm)."""
import sys, pypdf, zlib
try: import zstandard
except ImportError: zstandard = None
r = pypdf.PdfReader(sys.argv[1]); pg = r.pages[0]
priv = pg['/PieceInfo']['/Illustrator'].get_object()['/Private']
keys = sorted([k for k in priv.keys() if k.startswith('/AIPrivateData')], key=lambda k: int(k[len('/AIPrivateData'):]))
raw = b''.join(priv[k].get_object().get_data() for k in keys)
out = raw
for m in (b'%AI24_ZStandard_Data', b'%AI12_CompressedData'):
    i = raw.find(m)
    if i >= 0:
        i += len(m)
        out = zstandard.ZstdDecompressor().decompressobj().decompress(raw[i:]) if b'ZStandard' in m else zlib.decompressobj().decompress(raw[i:])
        break
L = out.replace(b'\r', b'\n').decode('latin1').split('\n')
W = float(pg.mediabox.width); H = float(pg.mediabox.height); PT = 25.4 / 72
print('page mm', round(W * PT, 2), round(H * PT, 2))
lay = [(i, l) for i, l in enumerate(L) if l.endswith(') Ln') or l.startswith('%AI5_EndLayer')]
def num(x):
    try: return float(x)
    except: return None
pts_all = {}
for (a, name), (b, _) in zip(lay[::2], lay[1::2]):
    segs = []; cur = []
    for ln in L[a:b]:
        if ln.startswith('%'): continue
        t = ln.strip().split()
        if len(t) == 3 and t[-1] == 'm' and num(t[0]) is not None: cur = [(num(t[0]), num(t[1]))]
        elif len(t) == 3 and t[-1] in ('L', 'l') and cur and num(t[0]) is not None: cur.append((num(t[0]), num(t[1])))
        elif t and t[-1] in ('c', 'C', 'v', 'V', 'y', 'Y'): cur = []
        elif t and (ln.strip().endswith('*') or t[-1] in ('S', 's', 'f', 'F', 'N', 'n')):
            if len(cur) >= 2: segs.append(cur)
            cur = []
    pts_all[name] = segs
avoid = [s for n, s in pts_all.items() if 'void' in n]
avoid = avoid[0] if avoid else []
if avoid:
    xs = [p[0] for c in avoid for p in c]; ys = [p[1] for c in avoid for p in c]
    X1, Ytop = max(xs), max(ys)
    X0 = X1 - W   # bord droit des hachures = bord droit du plan de travail
    print('avoid x mm', round((min(xs) - X0) * PT, 1), round((max(xs) - X0) * PT, 1))
    for n, segs in pts_all.items():
        v = sorted({round((c[0][0] - X0) * PT, 1) for c in segs if len(c) == 2 and abs(c[0][0] - c[1][0]) < .2 and abs(c[0][1] - c[1][1]) > 40})
        print(n, 'verticales mm', v)
