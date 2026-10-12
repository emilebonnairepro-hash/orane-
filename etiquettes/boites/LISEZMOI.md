# ORANE — boîtes (emballages Selfnamed)

Même design que les étiquettes V1 (verrouillé) : fond swirl de la catégorie, la bouille, Unbounded + Bricolage Grotesque.
Ce dossier ne modifie aucun fichier verrouillé : il lit `etiquettes/couleurs.py` et `etiquettes/assets/swirl-modele.svg`.

| N° | Produit | Gabarit | Plan de travail | Fichier à téléverser |
|----|---------|---------|-----------------|----------------------|
| 08 | Crème solaire teintée SPF 30 | BOX30-001 | 174,96 × 212,05 mm · 4133 × 5009 px (600 dpi) | `08-creme-solaire-teintee-spf30/sortie/boite.png` |
| 10 | Crème anti-âge peptides AM/PM | BOX50-001 (manuel « ALTERNATIVE ») | 175,00 × 250,00 mm · 4133 × 5909 px (600 dpi) | `10-creme-peptides-am-pm/sortie/boite.png` |

**Règles appliquées (manuel Selfnamed) :**
- Le texte reste à au moins 3 mm des plis et de la coupe. C'est vérifié automatiquement : le rendu s'arrête si un texte dépasse.
- Aucun texte ne fait moins de 4,5 pt.
- Le fond va jusqu'au tracé du fond perdu.
- Les zones de mentions (dos, côté gauche et rabat du dessous) restent vides et transparentes, car Selfnamed les remplit.
- Export en PNG 600 dpi sur fond transparent, à la taille exacte en px.

**Comment c'est organisé :**
- `boite.py` : le moteur commun. Chaque dossier contient un `boite.json` (produit de `etiquettes/v1/produits`, gabarit, ligne sous le sticker, côté), et les textes viennent de l'étiquette.
- `gabarit/<gabarit>.json` : la découpe, le fond perdu, les fentes et les plis, en pt, relus dans le .ai avec `lire_boite_ai.py`.
- `gabarit/mentions-selfnamed.png` : ce que Selfnamed imprime, superposé sur `apercu.png` pour contrôle.
- Les sorties sont `boite.png` (600 dpi, transparent), `boite.pdf` (600 dpi, taille exacte), `boite-600dpi.tif` (sans perte), `apercu.png` (découpe, plis et mentions) et `maquette.png` (boîte montée).

**Lancer le rendu :** `python3 etiquettes/boites/boite.py` (toutes les boîtes) ou `python3 etiquettes/boites/boite.py 10`

**Pour une nouvelle boîte**, il faut le zip Selfnamed : le gabarit .ai de la boîte, le manuel et le SVG des mentions.
