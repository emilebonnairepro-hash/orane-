# ORANE — boîtes (emballages Selfnamed)

Même design que les étiquettes V1 (verrouillé) : fond swirl de la catégorie, la bouille, Unbounded + Bricolage Grotesque.
Ce dossier ne modifie aucun fichier verrouillé : il lit `etiquettes/couleurs.py` et `etiquettes/assets/swirl-modele.svg`.

| N° | Produit | Gabarit | Plan de travail | Fichier à téléverser |
|----|---------|---------|-----------------|----------------------|
| 08 | Crème solaire teintée SPF 30 | BOX30-001 | 174,96 × 212,05 mm · 4133 × 5009 px (600 dpi) | `08-creme-solaire-teintee-spf30/sortie/boite.png` |
| 11 | Gel double hydratation | BOX30-001 (version du zip n°11) | 175,00 × 212,00 mm · 4133 × 5008 px (600 dpi) | `11-gel-double-hydratation/sortie/boite.png` |
| 19 | Démaquillant biphasé | BiPhasic Make-up Remover 100 ml (fond perdu reconstruit depuis les pointillés) | 170,00 × 236,00 mm · 4016 × 5575 px (600 dpi) | `19-demaquillant-biphase/sortie/boite.png` |
| 20 | Patchs yeux caféine (étui plat) | BOX001-001 (disposition « etui_plat » : textes en bandeau sous la face, tranche verticale) | 233,19 × 196,50 mm · 5508 × 4642 px (600 dpi) | `20-patchs-yeux-cafeine/sortie/boite.png` |
| 22 | Gel visage zinc homme | 50 ml (même découpe que BOX50-001 ; côté gauche libre, mentions = PAO seulement) | 175,00 × 250,00 mm · 4133 × 5909 px (600 dpi) | `22-gel-visage-zinc-homme/sortie/boite.png` |
| 23 | Huile à barbe | BOX20-001 (face étroite : textes mis à l'échelle de la largeur) | 140,00 × 200,45 mm · 3307 × 4735 px (600 dpi) | `23-huile-barbe/sortie/boite.png` |
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
