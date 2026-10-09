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
