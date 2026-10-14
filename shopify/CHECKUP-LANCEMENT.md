# ORANE : check-up avant lancement (14 octobre 2026)

Le check-up a été fait sur la boutique Shopify (API d'administration) et sur le thème publié **ORANE – v5**.
L'accès direct au site depuis l'environnement de travail est bloqué : les pages ont donc été vérifiées
avec l'aperçu local du thème (vrai code Liquid).

## ✅ Fait pendant ce check-up

**Fiches produit (12 nouveaux produits).** Elles sont réécrites au format ORANE, comme les 6 premières :
- une accroche ;
- « Ce que tu vas aimer » ;
- le mode d'emploi ;
- les actifs ;
- un duo routine (avec lien) ;
- « Bon à savoir » si besoin ;
- la liste INCI quand Selfnamed la fournit.

Sources : textes Selfnamed et étiquettes ORANE, sans allégation médicale. Le texte brut (balises en vrac, INCI non mis en forme) a disparu.

**Titres corrigés :**
- « COPY OF Crème Peptide… » → « Crème anti-âge aux peptides, jour et nuit » ;
- « Moisturising Conditioner » → « Après-shampooing hydratant » ;
- « Hand & Body Wash, Patchouli & Amber Vanilla » → « Gel lavant mains & corps, patchouli & vanille ambrée » ;
- « CARDAMONE & GINGEMBRE » → « cardamome & gingembre » ;
- « Nettoyant… contre l'acné » → « Gel nettoyant purifiant, peaux à imperfections » (le terme « acné » relève du médical) ;
- « Démaquillant BiPhasic » → « Démaquillant biphasé » ;
- le double espace dans « Gel lavant mains & corps, pamplemousse ».

**Adresses (URL) propres, avec redirection automatique depuis l'ancienne :**

| Ancienne adresse | Nouvelle adresse |
|---|---|
| copy-of-creme-peptide-ageless-jour-et-nuit | creme-anti-age-peptides-jour-et-nuit |
| moisturising-conditioner | apres-shampooing-hydratant |
| hand-body-wash-patchouli-amber-vanilla | gel-lavant-mains-corps-patchouli-vanille-ambree |
| gel-lavant-mains-corps-cardamone-gingembre | gel-lavant-mains-corps-cardamome-gingembre |
| nettoyant-purifiant-pour-le-visage-contre-lacne | gel-nettoyant-purifiant-visage |

**Collections.** Les 12 produits n'étaient dans aucune collection. Ils sont maintenant rangés ainsi :

| Collection | Nombre de produits |
|---|---|
| Visage | 9 |
| Corps | 5 |
| Cheveux | 4 |
| Homme | 2 |

La collection « Soin du cuir chevelu » s'appelle désormais « Soin des cheveux », avec le même lien. Les descriptions des collections ont été mises à jour pour toute la gamme, et le menu principal aussi.

**Liens.** Les 18 liens « routine complète » pointent vers des produits existants. Les produits et collections cités par le thème existent tous.

**Rendu.** Les nouvelles fiches s'affichent correctement, sans erreur JavaScript : accroche, stickers, mode d'emploi, actifs, duo avec bouton d'ajout au panier, ingrédients.

**Toujours en ordre :**
- les 18 produits sont actifs et publiés sur la boutique en ligne, avec 2 à 4 photos chacun ;
- le fournisseur « Selfnamed » est masqué sur le site.

## 🔴 Bloquant pour le lancement

**1. La livraison offerte n'existe pas en vrai.** Le site annonce « livraison offerte dès 50 € » à 13 endroits : bandeau, fiches, panier, FAQ, contact. Or les 18 produits sont dans le profil de livraison « Selfnamed », où la France coûte 7,48 € quel que soit le montant. Le profil général (offert dès 65 €) ne s'applique à aucun produit.
→ Décision à prendre : ajouter un tarif « Livraison offerte » à 0 € dès 50 € pour la France dans le profil Selfnamed, ou retirer la promesse du thème.

**2. Trois politiques manquent :** Livraison, Retours et CGV. Leurs liens dans le pied de page mènent à une page introuvable. Les mentions légales, obligatoires en France, manquent aussi. Des brouillons sont prêts dans `shopify/politiques/`. Il faut les compléter avec les informations de la société (raison sociale, SIRET, adresse, médiateur de la consommation) avant de les publier.

**3. Les paiements ne sont pas vérifiables d'ici.** L'API ne m'autorise pas à lire Shopify Payments. À vérifier dans **Paramètres → Paiements** : un moyen de paiement doit être activé, et une commande test doit être passée.

## 🟠 À corriger avant ou juste après le lancement

**4. La politique de confidentialité a un trou :** « veuillez nous appeler au , nous envoyer un e-mail à l'adresseemilebonnairepro@gmail.com ». Il manque le numéro et une espace. À corriger dans Paramètres → Politiques.

**5. Les prix sont incohérents.** Les 6 premiers produits valent de 6,30 € à 13,40 €. Le même gel lavant de 490 ml coûte 8,30 € en pamplemousse et 16,90 € en cardamome. On dirait des prix d'achat Selfnamed : à vérifier.

**6. Le délai « Livré en 2 à 5 jours »** est annoncé partout. Les produits partent de chez Selfnamed, en Lettonie : à confirmer avec leurs délais réels.

**7. L'UE n'est pas ouverte à la vente.** Seul le marché France est actif. Les tarifs prévus pour l'UE et l'international ne servent pas tant que les marchés correspondants ne sont pas activés.

**8. Le texte d'accueil est incomplet.** « Gel lavant, shampooing, patchs… » ne cite que les 6 premiers produits. À mettre à jour dans l'éditeur de thème : le thème publié ne peut pas être modifié par l'API.

**9. Le domaine.** Le site est encore sur 9p6hke-1p.myshopify.com. Il faut brancher un nom de domaine (ex. orane.fr) avant le lancement.

**10. Le menu « Footer menu »** contient « Search », en anglais. Le pied de page utilise « Besoin d'aide », donc c'est sans effet visible.
