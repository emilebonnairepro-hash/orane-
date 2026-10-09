# ✅ DESIGN VERROUILLÉ — à utiliser pour toutes les étiquettes ORANE

Style V1 + fond « swirl » (formes exactes du modèle, `etiquettes/assets/swirl-modele.svg`)
en **couleurs de catégorie** : visage rose · corps citron · cheveux mandarine · homme violet
(fond pâle de la couleur, formes dans la couleur pleine — `etiquettes/couleurs.py`).
Ne pas utiliser les anciens essais (`etiquettes/calque/`, `etiquettes/07-gel-nettoyant-purifiant/`) : archives seulement.

🔒 **Verrou** : `VERROU.json` garde l'empreinte des fichiers du design (mise en page, couleurs, formes du fond,
bouille, rendu). Si l'un d'eux change, `v1.py` refuse de générer. Images de référence : `reference/`.
Déverrouiller (changement voulu uniquement) : `python3 etiquettes/v1/v1.py --deverrouiller`, puis recalculer VERROU.json.
Ce qui reste libre pour chaque produit : les textes et le gabarit (fichier dans `produits/`).

Nouvelle étiquette : zip Selfnamed + description → un fichier dans `produits/` → `python3 etiquettes/v1/v1.py`.

# Style V1 (retenu) — moteur pour tous les produits

`python3 etiquettes/v1/v1.py` (ou `… v1.py 08` pour un seul produit) → `sortie/<produit>/` :
`etiquette.png` (à téléverser sur Selfnamed : 600 dpi, fond transparent, taille exacte du gabarit), `etiquette.pdf`, `apercu.png` (repères).

Un fichier par produit dans `produits/` : le gabarit (lu dans le zip Selfnamed : dimensions, fond perdu, cadre orange
des mentions, face avant) + les textes. La couleur de fond suit la catégorie (`etiquettes/couleurs.py`).
Fond : couleur de la catégorie + motif de vagues ton sur ton (`couleurs.py` → `motif_svg`, aperçu : `motif-par-categorie.png`).
Les tailles s'ajustent toutes seules au format (texte jamais sous 4,6 pt).

- 07 Gel nettoyant purifiant — gabarit 150-004 (140 ml) — rose (visage)
- 08 Crème solaire teintée SPF 30 — gabarit UZL30-002 (30 ml, 100 × 46 mm) — rose (visage)
- 09 Masque à l'argile — gabarit 100-004 (90 ml, 249,5 × 46 mm, deux zones de mentions, face au centre) — rose (visage)
- 10 Crème peptides AM/PM — gabarit UZL50-001 (50 ml, 96 × 113 mm) — rose (visage)
- 11 Gel double hydratation — gabarit LABEL_30-002 (30 ml, 100 × 46 mm, identique à la crème solaire) — rose (visage)
