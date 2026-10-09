# Le calque d'étiquette ORANE

Un seul design pour tous les soins, quelle que soit la taille de l'étiquette.
Le calque lit un fichier par produit dans `produits/` et calcule tout seul la mise en page :
face avant (le nom du soin remplit toute la largeur, l'arche avec la bouille, les pastilles),
panneau « côté » quand il y a la place (le geste, dedans, pour qui, pastilles, logo),
bande décorative sur la gauche, zones des mentions obligatoires laissées vides et transparentes.

## Générer
    python3 etiquettes/calque/calque.py            # tous les produits
    python3 etiquettes/calque/calque.py 07         # un seul
Résultats dans `sortie/<produit>/` : `etiquette.png` (à téléverser sur Selfnamed : 600 dpi, fond transparent,
taille exacte du gabarit), `etiquette.pdf`, `apercu.png` (avec les repères).

## Ajouter un produit
Copie `produits/07-gel-nettoyant-purifiant.json`, renomme-le, puis remplis :
- `gabarit` : d'après le manuel Selfnamed du produit (zip « Download template »)
  - `largeur`, `hauteur` : plan de travail en mm (fond perdu compris) ; `px` : taille en pixels indiquée par le manuel
  - `fond_perdu` (souvent 2 ou 3 mm), `marge` (3 mm)
  - `zones_vides` : le cadre orange des mentions obligatoires, en mm depuis le coin haut gauche
  - `face` (facultatif) : centre `cx` et `largeur` de la partie visible de face sur le flacon
- `produit` : numéro, univers, `lignes` du nom (une ou deux), sous-titre, bulle, pastilles, pied, volume,
  et pour le côté : `geste`, `dedans`, `parfum`, `pour_qui`, `badges`, `logos` (fichiers SVG dans `assets/`)
- `theme` : `fond`, `texte`, `accent`, `pastilles`, `anneau` parmi
  mandarine, rose, violet, citron, aubergine, creme (piscine en petite touche seulement)

Charte : pas de texte crème sur mandarine ou rose, 3 couleurs vives maximum par étiquette.
Textes : uniquement ce que dit la fiche du produit (pas de promesse médicale).

Les gabarits des produits 01 à 06 sont provisoires (66 × 96 mm et 96 × 66 mm) : à remplacer par les vrais.
