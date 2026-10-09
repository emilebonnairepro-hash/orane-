# Étiquettes ORANE pour Selfnamed

- `export/` : les fichiers à téléverser sur Selfnamed (PNG 600 dpi, 3 mm de fond perdu) + la même chose en PDF.
- `apercu/` : les épreuves avec les repères (coupe, zone de sécurité 3 mm, zone laissée vide pour les mentions obligatoires).
- `generer.py` : la source. Pour changer une taille, un texte ou une couleur, modifie la liste `PRODUITS`
  puis lance `python3 etiquettes/generer.py` (il faut Node et Playwright).

Tailles actuelles : 60 × 90 mm (portrait) et 90 × 60 mm pour les patchs. Ce sont des tailles provisoires :
remplace-les par celles des gabarits Selfnamed de chaque produit (bouton « Download template » dans le Design Studio).

Règles Selfnamed respectées : PNG, 600 dpi minimum, moins de 10 Mo, ~3 mm de fond perdu,
zone des mentions obligatoires laissée vide (Selfnamed les ajoute).
Charte : 7 couleurs, pas de texte crème sur mandarine ou rose, 3 couleurs vives maximum.

## n°07 — Gel nettoyant purifiant (gabarit Selfnamed 150-004, 140 ml) — ✅ VERSION RETENUE (V1)

Dossier `07-gel-nettoyant-purifiant/`, fait d'après le vrai gabarit Selfnamed :
plan de travail 142,5 × 109 mm (3367 × 2575 px à 600 dpi), fond perdu 2 mm, marge 3 mm,
zone des mentions obligatoires (x ≥ 107 mm) laissée vide et transparente.
- `etiquette.png` : à téléverser (PNG 600 dpi, fond transparent) · `etiquette.pdf` : même chose en PDF
- `apercu.png` : avec les repères · `apercu-flacon.png` : maquette approximative sur le flacon
- `generer.py` : la source (relancer : `python3 etiquettes/07-gel-nettoyant-purifiant/generer.py`)
