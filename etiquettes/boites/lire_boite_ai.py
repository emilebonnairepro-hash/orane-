"""Extrait les tracés d'un gabarit Illustrator Selfnamed (données privées décompressées) en chemins SVG.
Usage : python3 lire_boite_ai.py <ai décompressé .txt> <x0> <y0> <sortie.json>   (x0, y0 = origine du plan de travail)
"""
import sys, re, json
L = open(sys.argv[1]).read().split('\n')
X0, Y0 = float(sys.argv[2]), float(sys.argv[3])
def P(x, y): return f"{float(x)-X0:.3f},{float(y)-Y0:.3f}"
layers = {}; cur_layer = None; d = []; out = []
color = None
for ln in L:
    s = ln.strip()
    m = re.match(r'^\((.*)\) Ln$', s)
    if m: cur_layer = m.group(1); layers[cur_layer] = []; continue
    if cur_layer is None or s.startswith('%'): continue
    t = s.split()
    if not t: continue
    op = t[-1]
    try:
        if op == 'm' and len(t) == 3: d.append('M' + P(t[0], t[1])); cp = (t[0], t[1])
        elif op in ('L', 'l') and len(t) == 3: d.append('L' + P(t[0], t[1])); cp = (t[0], t[1])
        elif op in ('C', 'c') and len(t) == 7: d.append('C' + ' '.join(P(t[i], t[i+1]) for i in (0, 2, 4))); cp = (t[4], t[5])
        elif op in ('V', 'v') and len(t) == 5: d.append('C' + P(*cp) + ' ' + P(t[0], t[1]) + ' ' + P(t[2], t[3])); cp = (t[2], t[3])
        elif op in ('Y', 'y') and len(t) == 5: d.append('C' + P(t[0], t[1]) + ' ' + P(t[2], t[3]) + ' ' + P(t[2], t[3])); cp = (t[2], t[3])
        elif op == 'XA' : color = t[:-1]
        elif re.match(r'^\(?[sSfFbBnN]\)?$', t[0]) or op in ('s','S','f','F','b','B','n','N'):
            if d:
                closed = t[0].strip('()') in ('s', 'f', 'b', 'F', 'B')
                layers[cur_layer].append({'d': ' '.join(d) + (' Z' if closed else ''), 'op': t[0].strip('()'), 'col': color})
            d = []
    except ValueError: pass
json.dump(layers, open(sys.argv[4], 'w'))
for k, v in layers.items(): print(k, len(v))
