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

## Deux styles
- plein (v2) : `python3 etiquettes/calque/calque.py` → `sortie/`
- épuré (v3) : `python3 etiquettes/calque/calque.py --epure` → `sortie-epure/`
  (une seule pastille, pas de bulle ni de motif à pois, la bouille dans l'anneau, côté en texte simple)

- signature (v4) : `python3 etiquettes/calque/calque.py --signature` → `sortie-signature/`
  (fenêtre crème où la bouille déborde dans un médaillon à texte circulaire, deux pastilles, accroche ;
  côté : grands chiffres du geste, pastilles des actifs, séparateurs). Sur les petits formats, l'accroche
  puis la 2e pastille disparaissent avant que le nom ne rapetisse. Champs en plus : `accroche`, `cercle` (facultatif).

- v5 équilibrée : `python3 etiquettes/calque/calque.py --v5` → `sortie-v5/`
  (la structure de la signature sans le texte circulaire, une seule pastille, côté sans « pour qui » ni pastilles d'actifs)

- v6 fiche : `python3 etiquettes/calque/calque.py --fiche` → `sortie-v6-fiche/`
  (pas d'illustration au centre : identité en tête, puis toutes les infos essentielles en lignes qui remplissent la hauteur.
  Champs : `fiche` = [[intitulé, texte], …] (« Ce qu'il fait » en bandeau), `geste`, `plus`)

- v7 simple : `python3 etiquettes/calque/calque.py --simple` → `sortie-v7-simple/`
  (le plus simple pour le client : marque, nom, ce qu'il fait en une grande phrase, pour qui, volume ;
  côté : le geste en 3 étapes et les pastilles)

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
