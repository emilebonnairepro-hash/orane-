# Livraison offerte dès 65 € : les textes du thème publié à mettre à jour

Le tarif « Livraison offerte » (0 € dès 65 € d'achat, France) est **déjà actif dans Shopify**, dans le profil de livraison Selfnamed.
Le thème publié (ORANE – v5) annonce encore « dès 50 € ». L'API ne permet pas de modifier le thème publié :
il faut faire le changement dans **Boutique en ligne → Thèmes → Personnaliser**, ou dans **Modifier le code**.

**Le plus rapide.** Dans Thèmes, ouvre « … → Modifier le code ». Pour chacun des 8 fichiers ci-dessous, remplace le contenu par celui du fichier du même nom dans ce dossier. Ce sont les fichiers du thème publié, où seuls les 50 € deviennent 65 €.

| Fichier du thème | Ce qui change |
|---|---|
| sections/header-group.json | Bandeau : « Livraison offerte dès 65 € d'achat » |
| templates/index.json | Ticker et bloc promesses de l'accueil |
| templates/product.json | Jauge de la fiche (`threshold: 6500`), onglet Livraison, FAQ, promesse |
| templates/cart.json | Jauge du panier et coach (`threshold: 65`), promesse |
| templates/collection.json | Promesse |
| templates/list-collections.json | Promesse |
| templates/page.json | Promesse |
| templates/page.contact.json | Promesse et réponse de la FAQ livraison |

Les jauges « Plus que … pour la livraison offerte », sur la fiche produit et dans le panier, utilisent ces réglages : sans eux, elles se trompent de 15 €.
