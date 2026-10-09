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
