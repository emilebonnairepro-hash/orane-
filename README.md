# ORANE — site vitrine

Site one-page construit à partir de la charte graphique « ORANE — Identité décalée » (PDF à la racine).

- `index.html` : la page (accueil, esprit, soins, rituel, club, pied de page)
- `style.css` : les 7 couleurs de la charte, typos Unbounded + Bricolage Grotesque (Google Fonts), contours aubergine et ombres décalées
- `script.js` : menu mobile, apparitions au défilement, panier et inscription de démonstration (aucune donnée envoyée)
- `assets/favicon.svg` : l'anneau ORANE

Pour le voir : ouvrir `index.html` dans un navigateur. Pour le mettre en ligne gratuitement : GitHub Pages (Settings → Pages → branche, dossier `/`).

## Thème Shopify

Le dossier `shopify/` contient tout ce qui a été ajouté ou modifié dans le thème
« ORANE – version 2, plus loin (brouillon) ».

Sections (toutes modifiables dans l'éditeur de thème) :

- `orane-hero` : bannière avec le nom en géant, l'anneau, la bouille et des stickers qu'on peut décoller
- `orane-ticker` : deux rubans de phrases qui se croisent
- `orane-manifeste` : le manifeste qui s'allume mot après mot (`[mot]` = surligné, `#bouille` / `#anneau` = icônes)
- `orane-etagere` : les produits en cartes penchées, ajout au panier sans quitter la page
- `orane-quiz` : « Ta peau, là, maintenant ? », une humeur = un produit
- `orane-rituel` : trois gestes, trois chiffres géants, chacun relié à un produit
- `orane-outro` : le mot de la fin
- `orane-page-hero` : en-tête des collections, du panier, du contact, des pages et de la 404
- `orane-promesses` : livraison, retours… en gros stickers ronds
- `orane-faq` : questions qui s'ouvrent

Panier en tiroir : `snippets/cart-drawer.liquid` appelle `orane-cart-drawer` (le tiroir de Dawn, mêmes
identifiants) avec la piste de livraison offerte, le coup de pouce et « va très bien avec »
(`orane-drawer-bonus`, `orane-drawer-row`). Il s'ouvre à chaque ajout depuis les cartes ORANE.
L'appli Essential Cart Drawer est coupée dans ce thème (Personnaliser → Intégrations d'applications pour la remettre).

Autres fichiers : `snippets/` (anneau, bouille, étincelle en SVG), `assets/orane-brand.css`
(toute l'identité, y compris les pages Dawn : produit, collection, panier, tiroir, contact),
`assets/orane.js` (interactions), `templates/*.json` et `config/settings_data.json`
(générés par `build_json.py`).

### Aperçu local

`index.html` à la racine est la page d'accueil rendue à partir du vrai Liquid :

```sh
npm i liquidjs@10 && node shopify/preview/render.mjs              # page d'accueil → index.html
node shopify/preview/render.mjs cart /tmp/panier.html               # autre modèle
```
