# ORANE — site vitrine

Site one-page construit à partir de la charte graphique « ORANE — Identité décalée » (PDF à la racine).

- `index.html` : la page (accueil, esprit, soins, rituel, club, pied de page)
- `style.css` : les 7 couleurs de la charte, typos Unbounded + Bricolage Grotesque (Google Fonts), contours aubergine et ombres décalées
- `script.js` : menu mobile, apparitions au défilement, panier et inscription de démonstration (aucune donnée envoyée)
- `assets/favicon.svg` : l'anneau ORANE

Pour le voir : ouvrir `index.html` dans un navigateur. Pour le mettre en ligne gratuitement : GitHub Pages (Settings → Pages → branche, dossier `/`).

## Thème Shopify

Le dossier `shopify/` contient les fichiers ajoutés ou modifiés dans le thème
« ORANE – identité décalée (brouillon) », copie du thème en ligne :

- `sections/orane-hero|orane-ticker|orane-esprit|orane-rituel.liquid` : sections ORANE, modifiables dans l'éditeur de thème
- `snippets/orane-ring|orane-bouille|orane-spark.liquid` : l'anneau, la bouille et l'étincelle en SVG
- `assets/orane-brand.css` : la couche de marque, chargée sur toutes les pages
- `templates/index.json`, `sections/header-group.json`, `sections/footer-group.json`, `config/settings_data.json` : accueil, en-tête, pied de page et réglages (couleurs de la charte, contours et ombres)
- `build_json.py` : génère les fichiers JSON ci-dessus
