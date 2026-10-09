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
    # dosage par couleur pour garder un bon contraste entre le fond et les formes
    if fond in ("violet", "aubergine"):
        return _mix(C[fond], C["aubergine"], .68)   # violet : fond nettement plus sombre
    if fond == "citron":
        return _mix(C[fond], C["creme"], .82)       # citron : fond presque crème
    return _mix(C[fond], C["creme"], .5)


def motif_svg(couleur):
    """Rubans liquides façon « swirl » (d'après le modèle) : gros rubans aux bouts arrondis + vague basse.
    Tuile 140 × 110, dessinée 3 fois (décalée de ±140) pour se répéter sans couture."""
    W, H = 140, 110
    rubans = [
        # grande vague en S : entre à gauche, remonte, puis plonge vers le bas à droite
        (15, "M-12,58 C10,50 26,40 46,44 C66,48 70,30 86,30 C104,30 104,52 98,66 C92,80 104,96 120,104"),
        # forme du haut : goutte qui pend, puis bras vers la droite
        (14, "M58,-12 C54,8 60,22 70,20 C80,18 82,6 94,8 C112,10 116,30 132,34 C142,36 148,30 152,26"),
        # bras qui part de la grosse forme et descend au milieu
        (10, "M78,22 C70,40 58,54 60,70 C62,82 74,84 78,76"),
        # petit ruban en haut à gauche
        (9, "M-8,26 C4,22 12,14 14,4"),
    ]
    vague = "M-2,112 L-2,88 C14,78 26,96 40,92 C56,88 58,74 72,80 C84,85 84,100 96,98 C108,96 118,84 132,86 C138,87 140,88 142,88 L142,112 Z"
    g = "".join(f'<path d="{d}" fill="none" stroke="{couleur}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>' for w, d in rubans)
    g += f'<path d="{vague}" fill="{couleur}"/>'
    corps = "".join(f'<g transform="translate({dx},0)">{g}</g>' for dx in (-W, 0, W))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none">{corps}</svg>')
    from urllib.parse import quote
    return "data:image/svg+xml," + quote(svg)
