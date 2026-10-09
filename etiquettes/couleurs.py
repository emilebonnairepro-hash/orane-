"""ORANE — une couleur de fond verrouillée par catégorie de soin (comme les tuiles « univers » du site).

Toutes les étiquettes (V1 et calque) lisent ce fichier : changer une couleur ici la change partout.
Les accents sont choisis pour respecter la charte : jamais de texte crème sur mandarine ou rose,
3 couleurs vives maximum par étiquette, bleu piscine en petite touche seulement.
"""

C = {"mandarine": "#FF6A2B", "rose": "#FF5FA8", "violet": "#6B2CF5", "citron": "#D4F23A",
     "piscine": "#2CC8F5", "aubergine": "#2A1240", "creme": "#FFF3E3"}

# catégorie → couleur de fond
UNIVERS = {
    "visage": "rose",
    "corps": "citron",
    "cheveux": "mandarine",
    "homme": "violet",
}

# couleur de fond → accents qui vont avec
PALETTES = {
    "rose":      {"fond": "rose",      "texte": "aubergine", "accent": "citron",    "sticker": "violet", "anneau": ["violet", "citron"],    "etincelles": ["creme", "citron"]},
    "citron":    {"fond": "citron",    "texte": "aubergine", "accent": "mandarine", "sticker": "violet", "anneau": ["violet", "rose"],      "etincelles": ["creme", "rose"]},
    "mandarine": {"fond": "mandarine", "texte": "aubergine", "accent": "citron",    "sticker": "citron", "anneau": ["violet", "citron"],    "etincelles": ["creme", "citron"]},
    "violet":    {"fond": "violet",    "texte": "creme",     "accent": "citron",    "sticker": "citron", "anneau": ["citron", "rose"],      "etincelles": ["creme", "citron"]},
}


def palette(univers):
    """Palette (noms de couleurs) pour une catégorie : visage, corps, cheveux, homme."""
    return PALETTES[UNIVERS[univers.lower()]]


def texte_sur(nom):
    """Couleur de texte lisible sur un fond donné (charte : crème seulement sur les fonds foncés)."""
    return C["creme"] if nom in ("violet", "aubergine") else C["aubergine"]


def _mix(a, b, t):
    """Mélange deux couleurs hex : t = part de b (0 à 1)."""
    a, b = a.lstrip("#"), b.lstrip("#")
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ca, cb))


# Motif de fond (vagues) : ton sur ton, plus clair sur les fonds vifs, plus foncé sur le violet (texte crème lisible)
def couleur_motif(univers):
    fond = palette(univers)["fond"]
    if fond in ("violet", "aubergine"):
        return _mix(C[fond], C["aubergine"], .38)
    return _mix(C[fond], C["creme"], .42)


def motif_svg(couleur):
    """Tuile de vagues organiques, raccord horizontal (se répète sans couture), proportion 1,3 : 1."""
    import math
    W, H = 130.0, 100.0
    def courbe(y0, amp, ph, k=1):
        return [(W * i / 64, y0 + amp * math.sin(2 * math.pi * k * i / 64 + ph)) for i in range(65)]
    def bande(haut, bas):
        pts = haut + list(reversed(bas))
        return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"
    b1 = bande(courbe(8, 24, 0.4), courbe(48, 30, 1.2))
    b2 = bande(courbe(70, 22, 3.8), courbe(100, 16, 3.0))
    blob = ("M96,4 C112,0 128,10 124,26 C121,40 104,40 98,30 C93,22 82,14 96,4 Z "
            "M18,52 C28,46 42,52 40,62 C38,72 24,74 16,68 C9,62 10,56 18,52 Z")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" preserveAspectRatio="none">'
           f'<g fill="{couleur}"><path d="{b1}"/><path d="{b2}"/><path d="{blob}"/></g></svg>')
    from urllib.parse import quote
    return "data:image/svg+xml," + quote(svg)
