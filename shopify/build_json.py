import json
A, C, M, R, V, L = "#2a1240", "#fff3e3", "#ff6a2b", "#ff5fa8", "#6b2cf5", "#d4f23a"
def sch(bg, text, button, label, sec):
    return {"settings": {"background": bg, "background_gradient": "", "text": text, "button": button,
                         "button_label": label, "secondary_button_label": sec, "shadow": A}}
CREME, MAND, MENU = "scheme-a38ac93a-7224-4079-9c68-70762ddc148e", "scheme-b403d301-a3c4-4b45-a120-9ddc7de66256", "scheme-8c397c6a-afaa-4a34-8061-81677b1c9f81"

current = {
  "logo": "shopify://shop_images/orane-logo-horizontal-fond-clair.png", "logo_width": 240,
  "favicon": "shopify://shop_images/orane-bouille.png",
  "type_header_font": "unbounded_n8", "heading_scale": 120,
  "type_body_font": "bricolage_grotesque_n6", "body_scale": 120,
  "page_width": 1200, "spacing_sections": 0, "spacing_grid_horizontal": 28, "spacing_grid_vertical": 28,
  "animations_reveal_on_scroll": True, "animations_hover_elements": "3d-lift",
}
# Contours aubergine épais + ombres décalées nettes (charte) via les réglages natifs
def box(prefix, border, radius_key=None, radius=None, shadow=6, opacity=100):
    d = {f"{prefix}_border_thickness": border, f"{prefix}_border_opacity": 100,
         f"{prefix}_shadow_opacity": opacity, f"{prefix}_shadow_horizontal_offset": shadow,
         f"{prefix}_shadow_vertical_offset": shadow, f"{prefix}_shadow_blur": 0}
    if radius_key: d[radius_key] = radius
    return d
current.update(box("buttons", 3, "buttons_radius", 40, 4))
current.update(box("variant_pills", 2, "variant_pills_radius", 40, 4))
current.update(box("inputs", 3, "inputs_radius", 26, 4))
current.update({"card_style": "card", "card_image_padding": 16, "card_text_alignment": "left", "card_color_scheme": MAND})
current.update(box("card", 3, "card_corner_radius", 22, 6))
current.update({"collection_card_style": "card", "collection_card_image_padding": 16, "collection_card_text_alignment": "left", "collection_card_color_scheme": "scheme-2"})
current.update(box("collection_card", 3, "collection_card_corner_radius", 22, 6))
current.update({"blog_card_style": "card", "blog_card_image_padding": 16, "blog_card_text_alignment": "left", "blog_card_color_scheme": "scheme-1"})
current.update(box("blog_card", 3, "blog_card_corner_radius", 22, 6))
current.update(box("text_boxes", 3, "text_boxes_radius", 22, 6))
current.update(box("media", 3, "media_radius", 22, 6))
current.update(box("popup", 3, "popup_corner_radius", 22, 6))
current.update(box("drawer", 3, None, None, 0, 0))
current.update({
  "badge_position": "top left", "badge_corner_radius": 40,
  "sale_badge_color_scheme": "scheme-4", "sold_out_badge_color_scheme": "scheme-3",
  "brand_headline": "", "brand_description": "<p></p>", "brand_image_width": 100,
  **{f"social_{s}_link": "" for s in ["facebook","instagram","youtube","tiktok","twitter","snapchat","pinterest","tumblr","vimeo"]},
  "predictive_search_enabled": False, "predictive_search_show_vendor": False, "predictive_search_show_price": False,
  "currency_code_enabled": True, "cart_type": "drawer", "show_vendor": False, "show_cart_note": False,
  "cart_drawer_collection": "", "cart_color_scheme": CREME,
  "sections": {"main-password-header": {"type": "main-password-header", "settings": {"color_scheme": "scheme-3"}},
               "main-password-footer": {"type": "main-password-footer", "settings": {"color_scheme": "scheme-3"}}},
  "content_for_index": [],
  "blocks": {
    "2118589882331710876": {"type": "shopify://apps/essential-trust-badges/blocks/app-embed/0ff65b25-07e1-408e-950f-f54dd3d1751b", "disabled": False, "settings": {}},
    "15683396631634586217": {"type": "shopify://apps/inbox/blocks/chat/841fc607-4181-4ad1-842d-e24d7f8bad6b", "disabled": False, "settings": {
      "greeting_message": "", "show_featured_products": True, "featured_products": [],
      "background_color": "#FFF3E3", "font_color": "#2A1240", "agent_invert_activator_colors": True,
      "button_color": "#6B2CF5", "button_icon": "smiley_face", "button_text": "chat_with_us",
      "button_horizontal_position": "bottom_right", "button_vertical_position": "lowest",
      "agent_inherit_fonts": True, "agent_font": "system_ui_n4", "agent_font_size": 14,
      "agent_activator_font_size": 16, "agent_border_radius": 16}},
    "9388344762370057067": {"type": "shopify://apps/essential-cart-drawer/blocks/app-embed/824bb1f9-5f36-4608-a60c-1f2b6a6f8834", "disabled": False, "settings": {}},
    "3410014444582139945": {"type": "shopify://apps/amose-ai-store-builder/blocks/amose_embed/019b845c-fbba-74c5-9473-5c87b8849c1b", "disabled": False, "settings": {}},
  },
  # Les 7 couleurs de la charte ; jamais de crème sur mandarine ou sur rose
  "color_schemes": {
    "scheme-1": sch(C, A, M, A, A),          # crème
    "scheme-2": sch(R, A, C, A, A),          # rose bonbon
    "scheme-3": sch(A, C, L, A, C),          # aubergine
    "scheme-4": sch(V, C, L, A, C),          # violet électrique
    "scheme-5": sch(L, A, A, C, A),          # citron vert
    "scheme-f02800e5-53f8-4ea0-8da3-e0926506d380": sch(C, A, M, A, A),
    MAND: sch(M, A, C, A, A),                # mandarine
    CREME: sch(C, A, M, A, A),               # crème (fond principal)
    MENU: sch(M, A, C, A, A),                # mandarine (newsletter)
  },
})
HEADER = """/*
 * ------------------------------------------------------------
 * IMPORTANT: The contents of this file are auto-generated.
 *
 * This file may be updated by the Shopify admin theme editor
 * or related systems. Please exercise caution as any changes
 * made to this file may be overwritten.
 * ------------------------------------------------------------
 */
"""
import re
def fr(o):
    """Espaces insécables avant ? ! : ; (typographie française)."""
    if isinstance(o, dict): return {k: fr(v) for k, v in o.items()}
    if isinstance(o, list): return [fr(v) for v in o]
    if isinstance(o, str) and "{{" not in o: return re.sub(r" ([?!:;])", "\u00a0\\1", o)
    return o
def dump(path, obj):
    obj = fr(obj)
    open(path, "w").write(HEADER + json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

dump("config/settings_data.json", {"current": current})

# ---------- En-tête : feuille de style ORANE chargée sur toutes les pages ----------
dump("sections/header-group.json", {
  "name": "t:sections.header.name", "type": "header",
  "sections": {
    "orane-brand": {"type": "custom-liquid", "settings": {
      "custom_liquid": "{{ 'orane-brand.css' | asset_url | stylesheet_tag }}<script src=\"{{ 'orane.js' | asset_url }}\" defer></script>",
      "color_scheme": CREME, "padding_top": 0, "padding_bottom": 0}},
    "announcement-bar": {"type": "announcement-bar",
      "blocks": {
        "announcement-bar-0": {"type": "announcement", "settings": {"text": "Livraison offerte dès 50€ d'achat", "link": ""}},
        "announcement-bar-1": {"type": "announcement", "settings": {"text": "peau neuve, mine de rien ✦", "link": ""}}},
      "block_order": ["announcement-bar-0", "announcement-bar-1"],
      "settings": {"auto_rotate": True, "change_slides_speed": 5, "color_scheme": "scheme-4",
                   "show_line_separator": False, "show_social": False,
                   "enable_country_selector": False, "enable_language_selector": False}},
    "header": {"type": "header", "settings": {
      "logo_position": "middle-left", "mobile_logo_position": "center", "menu": "main-menu",
      "menu_type_desktop": "dropdown", "sticky_header_type": "on-scroll-up", "show_line_separator": False,
      "color_scheme": CREME, "menu_color_scheme": CREME,
      "enable_country_selector": True, "enable_language_selector": True,
      "margin_bottom": 0, "padding_top": 0, "padding_bottom": 0}}},
  "order": ["orane-brand", "announcement-bar", "header"]})

# ---------- Pied de page ----------
dump("sections/footer-group.json", {
  "name": "t:sections.footer.name", "type": "footer",
  "sections": {
    "newsletter": {"type": "newsletter",
      "blocks": {
        "heading": {"type": "heading", "settings": {"heading": "Rejoins la bande", "heading_size": "h1"}},
        "paragraph": {"type": "paragraph", "settings": {"text": "<p>Les nouveautés ORANE et les bons plans, avant tout le monde. Pas de spam, juste du pep's.</p>"}},
        "email-form": {"type": "email_form", "settings": {}}},
      "block_order": ["heading", "paragraph", "email-form"],
      "settings": {"color_scheme": "scheme-4", "full_width": True, "padding_top": 56, "padding_bottom": 56}},
    "footer": {"type": "footer",
      "blocks": {
        "about": {"type": "text", "settings": {"heading": "orane", "subtext": "<p>peau neuve, mine de rien. Des soins doux et un ton léger : visage, corps, cheveux, homme.</p>"}},
        "explore": {"type": "link_list", "settings": {"heading": "Explorer", "menu": "main-menu"}},
        "help": {"type": "link_list", "settings": {"heading": "Besoin d'aide", "menu": "ova-footer-2"}}},
      "block_order": ["about", "explore", "help"],
      "settings": {"color_scheme": "scheme-3", "newsletter_enable": False, "newsletter_heading": "",
                   "enable_follow_on_shop": True, "show_social": True, "enable_country_selector": False,
                   "enable_language_selector": False, "payment_enable": True, "show_policy": True,
                   "margin_top": 0, "padding_top": 44, "padding_bottom": 60}}},
  "order": ["newsletter", "footer"]})

# ---------- Page d'accueil : nouveau + existant ----------
def fc(collection, n, title, cols, scheme=CREME):
    return {"type": "featured-collection", "settings": {
      "collection": collection, "products_to_show": n, "title": title, "heading_size": "h1",
      "description": "", "show_description": False, "description_style": "body",
      "columns_desktop": cols, "enable_desktop_slider": False, "full_width": False,
      "show_view_all": True, "view_all_style": "solid", "color_scheme": scheme,
      "image_ratio": "portrait", "image_shape": "default", "show_secondary_image": True,
      "show_vendor": False, "show_rating": True, "quick_add": "standard",
      "columns_mobile": "2", "swipe_on_mobile": False, "padding_top": 56, "padding_bottom": 56}}

P_PATCHS = "patchs-hydrogel-energisants-pour-les-yeux-a-la-cafeine-et-a-la-vitamine-c"
P_DEMAQ = "demaquillant-biphasic-sans-parfum-1"
P_GEL = "gel-visage-au-zinc-sans-huile-pour-hommes"
P_BARBE = "huile-a-barbe-adoucissante"
P_SHAMP = "shampooing-pour-cuir-chevelu-sensible"
P_CORPS = "gel-lavant-mains-corps-pamplemousse"

def blocks(prefix, items):
    return {f"{prefix}{i}": it for i, it in enumerate(items)}, [f"{prefix}{i}" for i in range(len(items))]

hero_b, hero_o = blocks("s", [
  {"type": "sticker", "settings": {"text": "peau neuve, mine de rien.", "small": "", "round": False, "color": "citron", "x": 0, "y": 64, "rotate": -6}},
  {"type": "sticker", "settings": {"text": "zéro filtre", "small": "100 % pep's", "round": True, "color": "rose", "x": 36, "y": 38, "rotate": 10}},
  {"type": "sticker", "settings": {"text": "fais pas ta timide", "small": "", "round": False, "color": "creme", "x": 22, "y": 74, "rotate": 4}},
])
tape_b, tape_o = blocks("t", [{"type": "phrase", "settings": {"text": t}} for t in
  ["fais pas ta timide", "zéro filtre", "glow à la carte", "bouille de star", "100 % pep's"]])
quiz_b, quiz_o = blocks("m", [
  {"type": "mood", "settings": {"mood": "fatiguée du regard", "product": P_PATCHS, "why": "Caféine et vitamine C, le temps d'un café. Ton regard dit merci."}},
  {"type": "mood", "settings": {"mood": "maquillée jusqu'aux oreilles", "product": P_DEMAQ, "why": "Une phase huile, une phase eau : tout part en un geste, sans frotter."}},
  {"type": "mood", "settings": {"mood": "assoiffée mais sans gras", "product": P_GEL, "why": "Une hydratation express, texture légère, zéro effet brillant."}},
  {"type": "mood", "settings": {"mood": "barbe rebelle", "product": P_BARBE, "why": "Quelques gouttes et la barbe se fait douce, sans effet gras."}},
  {"type": "mood", "settings": {"mood": "cuir chevelu chatouilleux", "product": P_SHAMP, "why": "La douceur qu'il faut aux cuirs chevelus sensibles."}},
  {"type": "mood", "settings": {"mood": "envie de fraîcheur", "product": P_CORPS, "why": "Mains et corps, parfum pamplemousse. Ça pétille sans dessécher."}},
])
rit_b, rit_o = blocks("r", [
  {"type": "step", "settings": {"title": "Tu démaquilles", "text": "<p>On secoue, on imbibe un coton, on glisse. Le maquillage s'en va, ta bonne humeur reste.</p>", "product": P_DEMAQ}},
  {"type": "step", "settings": {"title": "Tu réveilles ton regard", "text": "<p>Une paire de patchs sous les yeux, le temps d'un café. Fais pas ta timide.</p>", "product": P_PATCHS}},
  {"type": "step", "settings": {"title": "Tu hydrates", "text": "<p>Une noisette de gel léger, sans effet gras. C'est bouclé : sourire obligatoire.</p>", "product": P_GEL}},
])

index = {"sections": {
  "orane-hero": {"type": "orane-hero", "blocks": hero_b, "block_order": hero_o, "settings": {
    "kicker_left": "N°01 — soins pour bouilles qui rigolent", "kicker_right": "visage · corps · cheveux",
    "lead": "<p>Le secteur chuchote en nude. Nous, on parle fort, en couleurs, avec des <strong>formules toutes douces</strong> pour ta peau.</p>",
    "cta_label": "voir les soins", "cta_link": "shopify://collections/all", "word": "orane",
    "hint": "psst : les stickers se décollent ✦"}},
  "orane-ticker": {"type": "orane-ticker", "blocks": tape_b, "block_order": tape_o},
  "orane-manifeste": {"type": "orane-manifeste", "settings": {
    "kicker": "Pourquoi ORANE ne ressemble à personne",
    "text": "Le secteur chuchote en nude. Nous, on parle [fort]. Des couleurs qui crient #anneau des formes [rondes] partout et des formules [douces] pour ta peau. Le premier degré est interdit, le clin d'œil obligatoire #bouille",
    "sign": "— la bande ORANE"}},
  "orane-etagere": {"type": "orane-etagere", "settings": {
    "kicker": "La boutique", "title": "Tout ORANE,", "title_em": "en vrac.", "collection": "all", "limit": 8,
    "add_label": "Dans mon panier", "soldout_label": "Voir le produit", "all_label": "Tout voir"}},
  "multicolumn_garanties": {"type": "multicolumn",
    "blocks": {
      "g1": {"type": "column", "settings": {"title": "", "text": "<h3>Livré en 2 à 5 jours</h3><p>Ta commande arrive vite.</p>", "link_label": "", "link": ""}},
      "g2": {"type": "column", "settings": {"title": "", "text": "<h3>Livraison offerte dès 50 €</h3><p>En dessous, les frais s'affichent avant de payer.</p>", "link_label": "", "link": ""}},
      "g3": {"type": "column", "settings": {"title": "", "text": "<h3>14 jours pour changer d'avis</h3><p>Un retour simple, depuis la page Contact.</p>", "link_label": "", "link": ""}}},
    "block_order": ["g1", "g2", "g3"],
    "settings": {"title": "", "heading_size": "h2", "image_width": "third", "image_ratio": "adapt",
      "button_label": "", "button_link": "", "columns_desktop": 3, "column_alignment": "center",
      "background_style": "none", "color_scheme": CREME, "columns_mobile": "1", "swipe_on_mobile": False,
      "padding_top": 12, "padding_bottom": 72}},
  "orane-quiz": {"type": "orane-quiz", "blocks": quiz_b, "block_order": quiz_o, "settings": {
    "kicker": "Le quiz qui dure 2 secondes", "title": "Ta peau, là, maintenant\u00a0?",
    "idle": "Choisis une humeur, je m'occupe du reste.", "match_label": "Ton match", "cta_label": "Je le veux"}},
  "collection-list": {"type": "collection-list",
    "blocks": {f"c{i+1}": {"type": "featured_collection", "settings": {"collection": h}} for i, h in enumerate(
      ["soin-du-visage", "soin-du-corps", "soin-du-cuit-chevelu", "homme"])},
    "block_order": ["c1", "c2", "c3", "c4"],
    "settings": {"title": "Choisis ton univers", "heading_size": "h1", "image_ratio": "square",
      "columns_desktop": 4, "show_view_all": False, "color_scheme": "scheme-4",
      "columns_mobile": "2", "swipe_on_mobile": False, "padding_top": 72, "padding_bottom": 80}},
  "produit-vedette": {"type": "featured-product",
    "blocks": {"title": {"type": "title", "settings": {"heading_size": "h1"}}, "price": {"type": "price", "settings": {}},
      "intro": {"type": "text", "settings": {"text": "7 paires de patchs hydrogel, à la caféine et à la vitamine C, pour le contour des yeux. Le petit coup de frais du matin.", "text_style": "body"}},
      "buy_buttons": {"type": "buy_buttons", "settings": {"show_dynamic_checkout": False, "show_gift_card_recipient": True}}},
    "block_order": ["title", "price", "intro", "buy_buttons"],
    "settings": {"product": P_PATCHS, "secondary_background": False, "media_size": "large", "color_scheme": "scheme-2",
      "constrain_to_viewport": True, "media_fit": "contain", "media_position": "left", "image_zoom": "lightbox",
      "hide_variants": False, "enable_video_looping": False, "padding_top": 72, "padding_bottom": 72}},
  "orane-rituel": {"type": "orane-rituel", "blocks": rit_b, "block_order": rit_o, "settings": {
    "kicker": "Le rituel", "title": "Trois gestes,", "title_em": "mine de rien.", "sticker": "glow à la carte"}},
  "orane-outro": {"type": "orane-outro", "settings": {"line": "À toute, bouille de star ✦", "word": "orane"}},
}, "order": ["orane-hero", "orane-ticker", "orane-manifeste", "orane-etagere", "multicolumn_garanties",
             "orane-quiz", "collection-list", "produit-vedette", "orane-rituel", "orane-outro"]}
dump("templates/index.json", index)
print("ok")

# =================== Les autres pages ===================
NB = " "
def hero(**kw):
    base = {"kicker": "", "title": "", "text": "", "show_description": True, "show_count": True,
            "sticker": "zéro filtre", "button_label": "", "button_link": "", "color": "auto"}
    base.update(kw)
    return {"type": "orane-page-hero", "settings": base}

def promesses(color="creme", title=""):
    b, o = blocks("p", [
      {"type": "promise", "settings": {"big": "2 à 5 jours", "small": "et c'est chez toi", "color": "citron"}},
      {"type": "promise", "settings": {"big": "offerte dès 50 €", "small": "la livraison", "color": "rose"}},
      {"type": "promise", "settings": {"big": "14 jours", "small": "pour changer d'avis", "color": "mandarine"}},
    ])
    return {"type": "orane-promesses", "blocks": b, "block_order": o, "settings": {"title": title, "color": color}}

def tapes():
    return {"type": "orane-ticker", "blocks": tape_b, "block_order": tape_o}

def shelf(title, em, kicker="", limit=8):
    return {"type": "orane-etagere", "settings": {"kicker": kicker, "title": title, "title_em": em, "collection": "all",
            "limit": limit, "add_label": "Dans mon panier", "soldout_label": "Voir le produit", "all_label": "Tout voir"}}

# Accueil : les garanties passent en gros stickers
index["sections"]["multicolumn_garanties"] = promesses("creme", "Les promesses ORANE")
dump("templates/index.json", index)

# Fiche produit : on garde la fiche et les suggestions, on ajoute rubans et promesses
TONE_CSS = ("{%- assign tones = 'mandarine,rose,citron' | split: ',' -%}{%- assign i = product.id | modulo: 3 -%}"
            "<style>:root { --o-tone: var(--o-{{ tones[i] }}); }</style>{{ 'orane-product.css' | asset_url | stylesheet_tag }}")
product = {"sections": {
  "orane-style": {"type": "custom-liquid", "settings": {"custom_liquid": TONE_CSS,
    "color_scheme": CREME, "padding_top": 0, "padding_bottom": 0}},
  "main": {"type": "main-product",
    "blocks": {
      "title": {"type": "title", "settings": {}}, "rating": {"type": "rating", "settings": {}},
      "price": {"type": "price", "settings": {}},
      "orane_bonus": {"type": "custom_liquid", "settings": {"custom_liquid": "{% render 'orane-buybox', product: product, threshold: 5000 %}"}},
      "variant_picker": {"type": "variant_picker", "settings": {"picker_type": "button", "swatch_shape": "none"}},
      "quantity_selector": {"type": "quantity_selector", "settings": {}},
      "buy_buttons": {"type": "buy_buttons", "settings": {"show_dynamic_checkout": True, "show_gift_card_recipient": True}},
      "livraison": {"type": "collapsible_tab", "settings": {"heading": "Livraison", "icon": "truck",
        "content": "<p>Livré en 2 à 5 jours. Livraison offerte dès 50 € d'achat ; en dessous, les frais s'affichent avant le paiement.</p>", "page": ""}},
      "retours": {"type": "collapsible_tab", "settings": {"heading": "Retours", "icon": "return",
        "content": "<p>Tu as 14 jours pour changer d'avis. Écris-nous depuis la page Contact avec ton numéro de commande.</p>", "page": ""}},
      "share": {"type": "share", "settings": {"share_label": "Partager"}}},
    "block_order": ["title", "rating", "price", "orane_bonus", "variant_picker", "quantity_selector", "buy_buttons", "livraison", "retours", "share"],
    "settings": {"enable_sticky_info": True, "color_scheme": CREME, "media_size": "medium", "constrain_to_viewport": True,
      "media_fit": "contain", "gallery_layout": "thumbnail_slider", "mobile_thumbnails": "show", "media_position": "left",
      "image_zoom": "lightbox", "hide_variants": True, "enable_video_looping": False, "padding_top": 40, "padding_bottom": 80}},
  "histoire": {"type": "orane-produit-histoire", "settings": {
    "lead_kicker": "En deux mots", "loves_title": "Ce que tu", "loves_em": "vas adorer.",
    "howto_kicker": "Mode d'emploi", "howto_stamp": "facile !", "actives_kicker": "Ce qu'il y a dedans",
    "for_kicker": "Pensé pour", "duo_title": "Le duo", "duo_em": "qui va bien.",
    "duo_here": "tu es ici ✦", "duo_add": "Je l'ajoute aussi"}},
  "orane-tapes": tapes(),
  "orane-promesses": promesses("creme"),
  "related-products": {"type": "related-products", "settings": {
    "heading": "Complète ta routine", "heading_size": "h1", "products_to_show": 4, "columns_desktop": 4, "columns_mobile": "2",
    "color_scheme": CREME, "image_ratio": "portrait", "image_shape": "default", "show_secondary_image": True,
    "show_vendor": False, "show_rating": True, "padding_top": 24, "padding_bottom": 100}},
  "sticky": {"type": "orane-sticky-atc", "settings": {"label": "Dans mon panier ✦", "soldout": "Bientôt de retour"}},
}, "order": ["orane-style", "main", "histoire", "orane-tapes", "orane-promesses", "related-products", "sticky"]}
dump("templates/product.json", product)

# Collections
dump("templates/collection.json", {"sections": {
  "hero": hero(kicker="", sticker="zéro filtre"),
  "tapes": tapes(),
  "product-grid": {"type": "main-collection-product-grid", "settings": {
    "products_per_page": 24, "columns_desktop": 3, "columns_mobile": "2", "color_scheme": CREME,
    "image_ratio": "portrait", "image_shape": "default", "show_secondary_image": True, "show_vendor": False,
    "show_rating": False, "quick_add": "standard", "enable_filtering": True, "filter_type": "horizontal",
    "enable_sorting": True, "padding_top": 24, "padding_bottom": 72}},
  "promesses": promesses("aubergine"),
}, "order": ["hero", "tapes", "product-grid", "promesses"]})

dump("templates/list-collections.json", {"sections": {
  "hero": hero(kicker="Les collections", title="tous les univers", sticker="choisis ton camp", color="violet", show_count=False,
               text="<p>Visage, corps, cheveux, homme : quatre façons de prendre soin de toi, toutes avec le sourire.</p>"),
  "main": {"type": "main-list-collections", "settings": {"title": "", "sort": "alphabetical", "image_ratio": "square",
    "columns_desktop": 4, "columns_mobile": "2"}},
  "promesses": promesses("creme"),
}, "order": ["hero", "main", "promesses"]})

# Panier
dump("templates/cart.json", {"sections": {
  "hero": hero(kicker="Le panier", title="presque" + NB + "à toi.", sticker="bon choix ✦", color="rose", show_count=False),
  "cart-items": {"type": "main-cart-items", "settings": {"color_scheme": CREME, "padding_top": 36, "padding_bottom": 24}},
  "cart-footer": {"type": "main-cart-footer",
    "blocks": {"subtotal": {"type": "subtotal", "settings": {}}, "buttons": {"type": "buttons", "settings": {}}},
    "block_order": ["subtotal", "buttons"],
    "settings": {"color_scheme": CREME, "padding_top": 12, "padding_bottom": 48}},
  "promesses": promesses("aubergine"),
  "shelf": shelf("Un petit dernier", "pour la route ?", "Avant de filer", 6),
}, "order": ["hero", "cart-items", "cart-footer", "promesses", "shelf"]})

# Contact
faq_b, faq_o = blocks("q", [
  {"type": "question", "settings": {"question": "En combien de temps je reçois ma commande" + NB + "?",
    "answer": "<p>En 2 à 5 jours. Tu peux souffler, c'est bientôt chez toi.</p>"}},
  {"type": "question", "settings": {"question": "La livraison, elle coûte combien" + NB + "?",
    "answer": "<p>Elle est offerte dès 50 € d'achat. En dessous, les frais s'affichent avant le paiement, pas de surprise.</p>"}},
  {"type": "question", "settings": {"question": "Je peux changer d'avis" + NB + "?",
    "answer": "<p>Oui : tu as 14 jours. Écris-nous via le formulaire avec ton numéro de commande et on s'occupe du reste.</p>"}},
  {"type": "question", "settings": {"question": "Comment je choisis le bon soin" + NB + "?",
    "answer": "<p>Chaque fiche produit indique les types de peau et les principes actifs. Tu peux aussi faire le quiz de la page d'accueil, ou nous écrire : on adore conseiller.</p>"}},
])
dump("templates/page.contact.json", {"sections": {
  "hero": hero(kicker="Contact", title="on papote" + NB + "?", sticker="réponse rapide", color="violet", show_count=False,
               text="<p>Une question sur un soin, une commande, ou juste envie de dire coucou ? Écris-nous, on répond vite (et gentiment).</p>"),
  "main": {"type": "main-page", "settings": {"padding_top": 36, "padding_bottom": 0}},
  "form": {"type": "contact-form", "settings": {"heading": "", "heading_size": "h1", "color_scheme": CREME,
    "padding_top": 24, "padding_bottom": 72}},
  "faq": {"type": "orane-faq", "blocks": faq_b, "block_order": faq_o, "settings": {
    "kicker": "Avant de nous écrire", "title": "Les questions", "title_em": "qu'on adore.", "show_contact": False,
    "contact_text": "Pas trouvé ta réponse ? Écris-nous, on répond vite (et gentiment)."}},
}, "order": ["hero", "main", "form", "faq"]})

# Pages simples
dump("templates/page.json", {"sections": {
  "hero": hero(sticker="peau neuve, mine de rien", color="violet", show_count=False),
  "main": {"type": "main-page", "settings": {"padding_top": 48, "padding_bottom": 72}},
  "promesses": promesses("creme"),
}, "order": ["hero", "main", "promesses"]})

# 404
dump("templates/404.json", {"sections": {
  "hero": hero(kicker="Erreur 404", title="oups.", sticker="pas de panique", color="aubergine", show_count=False,
               text="<p>Cette page fait sa timide : elle n'existe pas, ou plus. Mais les soins, eux, sont bien là.</p>",
               button_label="Retour aux soins", button_link="shopify://collections/all"),
  "shelf": shelf("Tant qu'on", "y est…", "Petite consolation", 6),
}, "order": ["hero", "shelf"]})

# Recherche : la section principale était désactivée, on la réactive
dump("templates/search.json", {"sections": {
  "main": {"type": "main-search", "settings": {
    "columns_desktop": 3, "columns_mobile": "2", "image_ratio": "portrait", "image_shape": "default",
    "show_secondary_image": True, "show_vendor": False, "show_rating": False, "enable_filtering": False,
    "filter_type": "horizontal", "enable_sorting": True, "article_show_date": True, "article_show_author": False,
    "padding_top": 60, "padding_bottom": 60}},
  "shelf": shelf("Et sinon,", "en vrac.", "Toute la boutique", 8),
}, "order": ["main", "shelf"]})
print("pages ok")
