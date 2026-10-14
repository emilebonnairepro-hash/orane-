"""Fiches produit ORANE (descriptions Shopify) : accroche, « Ce que tu vas aimer », utilisation, actifs, routine, extras.
Source : textes Selfnamed (INFO) et étiquettes ORANE. Pas d'allégation médicale (« aide à… »).
Usage : python3 shopify/produits/fiches.py  → fiches.json (titre, handle, collections, descriptionHtml)
"""
import json, html, pathlib

V, C, H, CH, FP = ("gid://shopify/Collection/684248793429", "gid://shopify/Collection/684248826197",
                   "gid://shopify/Collection/684248858965", "gid://shopify/Collection/684357124437",
                   "gid://shopify/Collection/684187582805")

def fiche(lead, intro, aimer, geste=None, actifs=None, routine=None, extras=()):
    e = lambda s: html.escape(s, quote=False)
    out = f"<p><strong>{e(lead)}</strong></p>\n<p>{e(intro)}</p>\n<h3>Ce que tu vas aimer</h3>\n<ul>\n" + "".join(f"<li>{e(x)}</li>\n" for x in aimer) + "</ul>\n"
    if geste:
        out += f"<h3>Comment l'utiliser</h3>\n<p>{e(geste)}</p>\n"
    if actifs:
        out += f"<h3>Les actifs</h3>\n<p>{e(actifs)}</p>\n"
    if routine:
        txt, nom, handle = routine
        out += f'<h3>Pour une routine complète</h3>\n<p>{e(txt)} <a href="/products/{handle}">{e(nom)}</a>.</p>\n'
    for titre, corps in extras:
        out += f"<h3>{e(titre)}</h3>\n<p>{e(corps)}</p>\n"
    return out.strip()

INCI = {
 "solaire": "Zinc Oxide, Aqua/Water, Dicaprylyl Carbonate, Isoamyl Laurate, Squalane, Caprylic/Capric Triglyceride, Glycerin, CI 77891 (Titanium Dioxide)***, Polyglyceryl-3 Polyricinoleate, Sorbitan Oleate, Lecithin, Hydrated Silica, Cera Alba (Beeswax), Polyglyceryl-6 Stearate, Sodium Chloride, Hectorite, Jojoba Esters, Sorbitan Caprylate, Parfum/Fragrance, Polyhydroxystearic Acid, Hippophae Rhamnoides (Sea Buckthorn) Fruit Extract*, Citric Acid, Polyglyceryl-6 Behenate, Propanediol, Caprylyl Glycol, Benzoic Acid, Sodium Phytate, Isostearic Acid, Hydrolyzed Hyaluronic Acid, Sodium Hyaluronate, [CI 77491, CI 77492, CI 77499 (Iron Oxides)]*, Limonene**, Citrus Aurantium Peel Oil, Linalool**, Citrus Limon Peel Oil, Pinene**, Vanillin, Citral**. *Ingrédients issus de l'agriculture biologique. **Issus d'huiles essentielles naturelles. ***Pigments minéraux purs.",
 "argile": "Aloe Barbadensis Leaf Juice*, Kaolin, Glycerin, Montmorillonite, Diatomaceous Earth, Butylene Glycol, Aqua/Water, Sodium PCA, Lactic Acid, Sodium Levulinate, Olea Europaea (Olive) Fruit Oil*, Tocopherol, Xanthan Gum, Propanediol, Sodium Anisate, Glyceryl Caprylate, Charcoal Powder, Camellia Sinensis (Black Tea) Leaf Extract*, Cucumis Sativus (Cucumber) Fruit Extract*, Salvia Officinalis (Sage) Leaf Extract*, [CI 77491, CI 77492, CI 77499 (Iron Oxides)]**, Rhamnose, Glycolipids, Glucose, Glucuronic Acid. *Ingrédients issus de l'agriculture biologique. **Pigments minéraux purs.",
 "peptides": "Aqua/Water, Simmondsia Chinensis (Jojoba) Seed Oil*, Glycerin, Pentylene Glycol, Polyglyceryl-6 Stearate, Cetearyl Alcohol, Sodium PCA, Dipalmitoyl Hydroxyproline, Propanediol, Aroma/Fragrance, Dicaprylyl Carbonate, Polyglyceryl-6 Behenate, Mangifera Indica (Mango) Seed Butter*, Caprylic/Capric Triglyceride, Coco-Caprylate, Fragaria Ananassa (Strawberry) Seed Oil, Vaccinium Myrtillus (Blueberry) Seed Oil*, Xanthan Gum, Hexapeptide-11, Phytosterols, Octyldodecanol, Palmitic Acid, Stearic Acid, Tocopherol, Ascorbyl Palmitate, Hydrolyzed Hyaluronic Acid, Sodium Hyaluronate, Sodium Phytate, Potassium Hydroxide, Leuconostoc/Radish Root Ferment Filtrate, Ginkgo Biloba (Ginkgo) Leaf Extract*, Citric Acid, Sodium Benzoate, Potassium Sorbate, CI 77491 (Iron Oxides)***, Linalyl Acetate**, Geranyl Acetate**, Linalool**, Geraniol**, Citronellol**. *Ingrédients issus de l'agriculture biologique. **Issus d'huiles essentielles naturelles. ***Pigments minéraux purs.",
 "ha": "Aloe Barbadensis (Aloe) Leaf Juice*, Pentylene Glycol, Butylene Glycol, Glycerin**, Sodium PCA, Aqua/Water, Propanediol, Cellulose Gum, Parfum/Fragrance, Algin, Camellia Sinensis (White Tea) Leaf Extract*, Salvia Officinalis (Sage) Leaf Extract*, Hydrolyzed Hyaluronic Acid, Lactic Acid, Sodium Hyaluronate, Sodium Phytate, Rhamnose, Glucose, Glucuronic Acid. *Ingrédients issus de l'agriculture biologique. **Fabriqué à partir d'ingrédients biologiques.",
 "uree": "Aqua, Helianthus Annuus (Sunflower) Seed Oil*, Glycerin, Hydroxyethyl Urea, Polyglyceryl-6 Stearate, Cetearyl Alcohol, Panthenol, Caprylic/Capric Triglyceride, Caprylic/Capric/Myristic/Stearic Triglyceride, Dicaprylyl Carbonate, Sodium PCA, Parfum, Triethyl Citrate, Polyglyceryl-6 Behenate, Benzyl Alcohol, Xanthan Gum, Sodium Benzoate, Palmitic Acid, Stearic Acid, Lactic Acid, Potassium Sorbate, Ascorbyl Palmitate, Sodium Hyaluronate, Sodium Phytate, Tocopherol, Benzyl Salicylate, Limonene, Citrus Aurantium Bergamia Peel Oil, Citrus Aurantium Peel Oil, Citral, Linalool, Linalyl Acetate, Pinene, Cananga Odorata Oil/Extract. *Ingrédients issus de l'agriculture biologique.",
 "patchouli": "Aqua/Water, Sodium Coco-Sulfate, Sodium Cocoamphoacetate, Cocamidopropyl Betaine, Betaine, Coco-Glucoside, Citric Acid, Parfum/Fragrance, Sodium Chloride, Benzyl Alcohol, Pyrus Cydonia (Quince) Fruit Extract*, Sodium Benzoate, Potassium Sorbate. *Ingrédients issus de l'agriculture biologique.",
 "serum": "Aqua, Coconut Alkanes, Pentylene Glycol, Cetearyl Alcohol, Glycerin, Glyceryl Stearate Citrate, Betaine, Caprylic/Capric Triglyceride, Dicaprylyl Carbonate, Simmondsia Chinensis Seed Oil, Sodium PCA, Helianthus Annuus Seed Oil, Parfum, Undecane, Tridecane, Xanthan Gum, Cellulose, Ascorbyl Palmitate, Tocopherol, Rosa Canina Fruit Oil, Sodium Phytate, Nasturtium Officinale Flower/Leaf Extract, Potassium Hydroxide, Sodium Hyaluronate, Ginkgo Biloba Leaf Extract, Citric Acid, Sodium Benzoate, Potassium Sorbate, Vanillin, Linalyl Acetate, Pogostemon Cablin Oil, Linalool, Coumarin, Cedrus Atlantica Oil/Extract.",
 "keratine": "Aqua/Water, Cantharellus Cibarius (Chanterelle) Extract*, Cetearyl Alcohol, Distearoylethyl Dimonium Chloride, Glycerin**, Brassica Alcohol, PCA Glyceryl Oleate, Sodium PCA, Brassicyl Isoleucinate Esylate, Lactic Acid, Parfum/Fragrance, Cocos Nucifera (Coconut) Oil*, Xylitylglucoside, Butylene Glycol, Guar Hydroxypropyltrimonium Chloride, Benzyl Alcohol, Anhydroxylitol, Persea Gratissima (Avocado) Oil*, Hydrolyzed Wheat Protein, Sodium Benzoate, Xylitol, Hydrolyzed Keratin, Potassium Sorbate, Ascorbyl Palmitate, Butyrospermum Parkii (Shea) Butter*, Oenothera Biennis (Evening Primrose) Oil*, Prunus Amygdalus Dulcis (Sweet Almond) Oil*, Tocopherol, Crambe Maritima (Sea Kale) Leaf Extract, Leuconostoc/Radish Root Ferment Filtrate, Linalool***, Limonene***, Citrus Aurantium Peel Oil, Juniperus Virginiana Oil, Benzyl Salicylate***. *Ingrédients issus de l'agriculture biologique. **Fabriqué à partir d'ingrédients biologiques. ***Issus d'huiles essentielles naturelles.",
 "sec": "Alcohol denat., Aqua (Water), Distarch Phosphate, Propanediol, Glycerin, Parfum (Fragrance), Sarcosine, Panthenol, Maltodextrin, Echinacea Purpurea Extract, Rhodiola Rosea Extract.",
}
ing = lambda k: ("Ingrédients", INCI[k])

F = [
 dict(id="gid://shopify/Product/11694984823125", title="Gel nettoyant purifiant, peaux à imperfections", handle="gel-nettoyant-purifiant-visage", col=[V],
  html=fiche("Le nettoyage doux qui fait du bien aux peaux à imperfections.",
   "Un gel nettoyant au pH équilibré, sans tensioactifs agressifs : il élimine les impuretés et l'excès de sébum tout en respectant l'hydratation naturelle de la peau. Résultat : un teint frais, doux et confortable, avec un parfum frais de thé vert.",
   ["Nettoie et purifie sans agresser la peau", "pH équilibré, sans tensioactifs agressifs", "Aide à éliminer l'excès de sébum", "Parfum frais de thé vert", "Formule végétalienne, sans gluten, sans noix"],
   "Une petite noisette sur peau humide, masse doucement, puis rince abondamment. Parfait en première étape de ta routine.",
   "Extraits de feuille de maté, de mousse d'Islande et de cals de genévrier, aux propriétés apaisantes et purifiantes, pour un teint plus lisse et plus net.",
   ("Une fois par semaine, ajoute notre", "masque à l'argile", "masque-a-largile-pour-les-pores-et-les-points-noirs"))),
 dict(id="gid://shopify/Product/11695076376917", title="Crème solaire teintée SPF 30", handle=None, col=[V],
  html=fiche("Le soleil, oui. Les traces blanches, non.",
   "Une crème solaire teintée à filtre minéral, SPF 30 (protection élevée). Sa formule légère s'étale facilement, sans laisser de traces blanches, et aide à uniformiser le teint pour un fini naturel et lumineux.",
   ["SPF 30, protection élevée, à filtre minéral (oxyde de zinc)", "Une teinte légère qui aide à uniformiser le teint", "Facile à étaler, sans traces blanches", "Formule hydratante", "Testée dermatologiquement"],
   "Applique généreusement avant l'exposition au soleil et renouvelle souvent, surtout après la baignade.",
   "Argousier riche en oméga et acide hyaluronique, pour aider la peau à rester hydratée et confortable toute la journée.",
   ("Le matin, commence par notre", "gel double hydratation", "gel-double-hydratation-boost-ha-1"),
   [("Bon à savoir", "Ce produit ne garantit pas une protection à 100 % contre les rayons UVA/UVB. Une exposition prolongée au soleil présente un risque sérieux pour la santé : évite-la, même avec une crème solaire."), ing("solaire")])),
 dict(id="gid://shopify/Product/11695080472917", title="Masque à l'argile pour les pores et les points noirs", handle=None, col=[V],
  html=fiche("10 minutes de pause, des pores qui respirent.",
   "Un masque purifiant à l'argile blanche et verte : il absorbe l'excès de sébum et les impuretés, exfolie en douceur et aide à affiner l'apparence des pores et des points noirs, sans dessécher. Peau propre, lisse et fraîche.",
   ["Argiles blanche et verte, riches en minéraux", "Absorbe l'excès de sébum et les impuretés", "Exfolie en douceur", "Texture crémeuse qui ne dessèche pas", "Sans parfum, végétalien, sans gluten, sans noix"],
   "Sur peau propre, laisse poser 5 à 10 minutes, puis rince abondamment.",
   "Argile blanche, argile verte, algues aquatiques, complexe biominéral et jus d'aloe vera, avec des extraits bio de thé noir, de sauge et de concombre.",
   ("Avant le masque, nettoie ta peau avec notre", "gel nettoyant purifiant", "gel-nettoyant-purifiant-visage"),
   [ing("argile")])),
 dict(id="gid://shopify/Product/11695140929877", title="Crème anti-âge aux peptides, jour et nuit", handle="creme-anti-age-peptides-jour-et-nuit", col=[V],
  html=fiche("Une seule crème, matin et soir.",
   "Une crème raffermissante au complexe de peptides qui aide à améliorer l'élasticité de la peau et à atténuer l'apparence des ridules et des rides. Hydratation équilibrée et effet repulpant, dans une texture légère qui pénètre facilement.",
   ["Un complexe de peptides de qualité", "Aide à améliorer l'élasticité et à atténuer l'apparence des ridules", "Hydrate et repulpe", "Texture légère, vite absorbée", "Pensée pour les peaux matures", "Formule végétalienne, sans gluten, sans noix"],
   "Matin et soir, sur peau propre.",
   "Peptides, acide hyaluronique, vitamines C et E et PCA de sodium.",
   ("Le matin, protège ta peau avec notre", "crème solaire teintée SPF 30", "creme-solaire-teintee-spf30"),
   [ing("peptides")])),
 dict(id="gid://shopify/Product/11695167078741", title="Gel double hydratation à l'acide hyaluronique", handle=None, col=[V],
  html=fiche("De l'eau, et elle reste.",
   "Un gel léger qui associe un acide hyaluronique de plusieurs poids moléculaires et du PCA de sodium : il aide la peau à former une barrière hydratante, à limiter la perte d'eau et à garder sa fermeté et son élasticité. Peau fraîche, douce, et ridules atténuées.",
   ["Double hydratation : PCA de sodium et acide hyaluronique", "Aide à limiter la perte d'hydratation", "Atténue l'apparence des ridules", "Frais et léger", "Pour les peaux normales, matures ou déshydratées"],
   "Sur peau propre.",
   "Acide hyaluronique, PCA de sodium, jus de feuille d'aloe vera, extraits bio de sauge et de thé blanc.",
   ("Termine par notre", "crème anti-âge aux peptides", "creme-anti-age-peptides-jour-et-nuit"),
   [ing("ha")])),
 dict(id="gid://shopify/Product/11698062524757", title="Crème corps 5 % d'urée + 2 % de panthénol", handle=None, col=[C],
  html=fiche("Peau qui tiraille ? On gère.",
   "Une crème pour le corps à 5 % d'hydroxyéthylurée, avec de l'acide hyaluronique et du panthénol : elle apaise et adoucit la peau sèche et rugueuse et l'hydrate en profondeur, toute la journée. Texture nourrissante et non grasse.",
   ["5 % d'hydroxyéthylurée pour une hydratation en profondeur", "Acide hyaluronique pour retenir l'hydratation", "Panthénol pour un soin apaisant", "Texture nourrissante, non grasse", "Testée dermatologiquement", "Pour tous les types de peau"],
   "Applique-la sur une peau propre, en massant jusqu'à ce qu'elle pénètre.",
   "Urée (hydroxyéthylurée), panthénol, acide hyaluronique et PCA de sodium.",
   ("À appliquer juste après la douche avec notre", "gel lavant cardamome et gingembre", "gel-lavant-mains-corps-cardamome-gingembre"),
   [ing("uree")])),
 dict(id="gid://shopify/Product/11698063737173", title="Gel lavant mains & corps, cardamome & gingembre", handle="gel-lavant-mains-corps-cardamome-gingembre", col=[C],
  html=fiche("Une douche qui réveille.",
   "Un gel lavant pour les mains et le corps qui nettoie sans dessécher et laisse la peau fraîche et douce, avec un parfum chaud et épicé de cardamome et de gingembre.",
   ["Nettoie mains et corps sans déshydrater", "Hydratant et léger", "Parfum de cardamome et de gingembre", "Certifié naturel", "Formule végétalienne, sans gluten, sans noix", "Pour tous les types de peau"],
   "Applique-le sur la peau humide, fais mousser, puis rince abondamment.",
   "Bétaïne hydratante et extrait de coing bio.",
   ("Après la douche, hydrate avec notre", "crème corps à l'urée", "creme-pour-le-corps-a-5-dhydroxyethyluree-2-de-panthenol"))),
 dict(id="gid://shopify/Product/11698066063701", title="Gel lavant mains & corps, patchouli & vanille ambrée", handle="gel-lavant-mains-corps-patchouli-vanille-ambree", col=[C],
  html=fiche("La douceur, en version cocooning.",
   "Un gel lavant pour les mains et le corps qui nettoie sans dessécher et laisse la peau fraîche, douce et délicatement parfumée, avec des notes chaudes de patchouli et de vanille ambrée.",
   ["Nettoie mains et corps sans déshydrater", "Hydratant et léger", "Parfum patchouli et vanille ambrée", "Certifié naturel", "Formule végétalienne, sans gluten, sans noix", "Pour tous les types de peau"],
   "Applique-le sur la peau humide, fais mousser, puis rince abondamment.",
   "Bétaïne hydratante et extrait de coing bio.",
   ("Prolonge le cocooning avec notre", "sérum corporel Silk Skin", "serum-corporel-silk-skin-ambre-boise-et-cuir"),
   [ing("patchouli")])),
 dict(id="gid://shopify/Product/11698068062549", title="Sérum corporel Silk Skin, ambre boisé et cuir", handle=None, col=[C],
  html=fiche("Une peau de soie, en quelques secondes.",
   "Un sérum pour le corps léger et vite absorbé, qui hydrate intensément et laisse la peau incroyablement douce et lisse. Son mélange d'huiles nourrissantes, dont le jojoba et la rose musquée, aide à améliorer la texture et l'élasticité de la peau.",
   ["Formule légère à absorption rapide", "Hydratation en profondeur", "Huiles de jojoba et de rose musquée", "Apaise et hydrate", "Parfum ambre boisé et cuir", "Certifié naturel"],
   "Applique-le sur une peau propre, en massant jusqu'à ce qu'il pénètre.",
   "PCA de sodium, huile de jojoba, acide hyaluronique, bétaïne et extraits de plantes.",
   ("Commence par notre", "gel lavant patchouli et vanille ambrée", "gel-lavant-mains-corps-patchouli-vanille-ambree"),
   [ing("serum")])),
 dict(id="gid://shopify/Product/11698070290773", title="Masque capillaire réparateur intensif à la kératine", handle=None, col=[CH],
  html=fiche("Des longueurs qui retrouvent leur souplesse.",
   "Un masque riche et onctueux qui nourrit et renforce les cheveux en profondeur. Il cible les cassures, les pointes fourchues et le manque d'éclat : des cheveux plus doux, plus brillants et faciles à coiffer.",
   ["Kératine hydrolysée, protéines de blé et peptides pour renforcer la fibre", "Aide à réduire les cassures et les pointes fourchues", "Vitamine E et beurre de karité pour nourrir", "Cheveux brillants et soyeux", "Certifié naturel"],
   "Sur cheveux propres et humides, applique généreusement en insistant sur les longueurs et les pointes. Laisse agir 5 à 10 minutes, puis rince abondamment.",
   "Kératine, protéines de blé, peptides, complexe biominéral, vitamine E, beurre de karité et PCA de sodium.",
   ("Pour démêler au quotidien, associe-le à notre", "après-shampooing hydratant", "apres-shampooing-hydratant"),
   [ing("keratine")])),
 dict(id="gid://shopify/Product/11698075861333", title="Après-shampooing hydratant", handle="apres-shampooing-hydratant", col=[CH],
  html=fiche("Démêlé, lisse, et zéro prise de tête.",
   "Un après-shampooing qui nourrit les cheveux et les laisse lisses et faciles à coiffer. Infusé d'huile d'argan et de protéines de blé, il aide à nourrir les pointes sèches et à améliorer la texture des cheveux.",
   ["Huile d'argan et protéines de blé", "Aide à nourrir les pointes sèches", "Cheveux lisses et faciles à coiffer", "Avec du jus d'aloe vera", "Certifié naturel, sans noix"],
   "Après le shampooing, applique-le sur les longueurs et les pointes, laisse agir 2 à 5 minutes, puis rince.",
   "Huile d'argan, protéines de blé et jus d'aloe vera.",
   ("Le duo parfait avec notre", "shampooing pour cuir chevelu sensible", "shampooing-pour-cuir-chevelu-sensible"))),
 dict(id="gid://shopify/Product/11698078450005", title="Shampooing sec en spray Quick Refresh", handle=None, col=[CH],
  html=fiche("Cheveux frais, sans passer sous l'eau.",
   "Un shampooing sec sans gaz, diffusé en brume fine : ses agents naturels absorbent l'excès de sébum aux racines et redonnent instantanément aux cheveux un aspect propre et du volume. Sans résidus blancs, pour espacer les lavages.",
   ["Sans gaz, en brume fine et légère", "Aide à absorber l'excès de sébum aux racines", "Aspect propre et volume instantanés", "Ne laisse pas de résidus blancs", "Formule végétalienne, sans noix", "Pour tous les types de cheveux"],
   "Agite bien. Vaporise sur cheveux secs, en insistant sur les racines, puis masse délicatement du bout des doigts. Ne rince pas. Un petit dépôt de poudre au fond du flacon, c'est normal.",
   "Amidon de riz, sarcosine, panthénol et extraits botaniques (échinacée, rhodiola).",
   ("Le jour du lavage, offre une pause à tes longueurs avec notre", "masque à la kératine", "masque-capillaire-reparateur-intensif-a-la-keratine"),
   [("Bon à savoir", "Contient de l'alcool : tiens-le à l'écart de la chaleur et des flammes. Pour cette raison, il est expédié uniquement en livraison standard."), ing("sec")])),
]
pathlib.Path(__file__).with_name("fiches.json").write_text(json.dumps(F, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(F), "fiches")
