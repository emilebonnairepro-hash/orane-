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
def dump(path, obj):
    open(path, "w").write(HEADER + json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

dump("config/settings_data.json", {"current": current})

# ---------- En-tête : feuille de style ORANE chargée sur toutes les pages ----------
dump("sections/header-group.json", {
  "name": "t:sections.header.name", "type": "header",
  "sections": {
    "orane-brand": {"type": "custom-liquid", "settings": {
      "custom_liquid": "{{ 'orane-brand.css' | asset_url | stylesheet_tag }}",
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

index = {"sections": {
  "orane-hero": {"type": "orane-hero", "settings": {
    "eyebrow": "Visage · corps · cheveux · homme", "title": "orane", "sticker": "peau neuve, mine de rien.",
    "text": "<p>Le secteur chuchote en nude. Nous, on parle fort, en couleurs, avec des formules toutes douces pour ta peau.</p>",
    "button_label": "Découvrir les soins", "button_link": "shopify://collections/all",
    "button2_label": "C'est quoi, ce délire ?", "button2_link": "#esprit"}},
  "orane-ticker": {"type": "orane-ticker",
    "blocks": {f"t{i}": {"type": "phrase", "settings": {"text": t}} for i, t in enumerate(
      ["fais pas ta timide", "zéro filtre", "glow à la carte", "bouille de star", "100 % pep's"])},
    "block_order": [f"t{i}" for i in range(5)]},
  "multicolumn_garanties": {"type": "multicolumn",
    "blocks": {
      "g1": {"type": "column", "settings": {"title": "", "text": "<h3>Livré en 2 à 5 jours</h3><p>Ta commande arrive vite.</p>", "link_label": "", "link": ""}},
      "g2": {"type": "column", "settings": {"title": "", "text": "<h3>Livraison offerte dès 50 €</h3><p>En dessous, les frais s'affichent avant de payer.</p>", "link_label": "", "link": ""}},
      "g3": {"type": "column", "settings": {"title": "", "text": "<h3>14 jours pour changer d'avis</h3><p>Un retour simple, depuis la page Contact.</p>", "link_label": "", "link": ""}}},
    "block_order": ["g1", "g2", "g3"],
    "settings": {"title": "", "heading_size": "h2", "image_width": "third", "image_ratio": "adapt",
      "button_label": "", "button_link": "", "columns_desktop": 3, "column_alignment": "center",
      "background_style": "none", "color_scheme": CREME, "columns_mobile": "1", "swipe_on_mobile": False,
      "padding_top": 48, "padding_bottom": 28}},
  "featured-collection-0": fc("all", 6, "Nos soins", 3),
  "collection-list": {"type": "collection-list",
    "blocks": {f"c{i+1}": {"type": "featured_collection", "settings": {"collection": h}} for i, h in enumerate(
      ["soin-du-visage", "soin-du-corps", "soin-du-cuit-chevelu", "homme"])},
    "block_order": ["c1", "c2", "c3", "c4"],
    "settings": {"title": "Choisis ton univers", "heading_size": "h1", "image_ratio": "square",
      "columns_desktop": 4, "show_view_all": False, "color_scheme": "scheme-1",
      "columns_mobile": "2", "swipe_on_mobile": False, "padding_top": 56, "padding_bottom": 56}},
  "orane-esprit": {"type": "orane-esprit",
    "blocks": {
      "e1": {"type": "card", "settings": {"color": "mandarine", "title": "Doux avant tout", "text": "<p>Chaque soin est pensé pour nettoyer, hydrater ou apaiser sans agresser la peau. Rien de coupant, ni dans la forme ni dans la formule.</p>"}},
      "e2": {"type": "card", "settings": {"color": "rose", "title": "Des actifs qui servent", "text": "<p>Acide hyaluronique, aloe vera, caféine, vitamine C, zinc : des ingrédients connus, choisis pour leur rôle. Zéro jargon.</p>"}},
      "e3": {"type": "card", "settings": {"color": "citron", "title": "Premier degré interdit", "text": "<p>On parle de beauté sans se prendre au sérieux. Quatre univers, des associations évidentes et un dernier geste : sourire.</p>"}}},
    "block_order": ["e1", "e2", "e3"],
    "settings": {"eyebrow": "L'esprit ORANE", "title": "Le soin, version sourire", "background": "aubergine",
      "intro": "<p>Le secteur mise sur le nude, le minimal et le chuchoté. ORANE fait l'inverse : de la couleur qui crie, des formes rondes et un clin d'œil.</p>"}},
  "produit-vedette": {"type": "featured-product",
    "blocks": {"title": {"type": "title", "settings": {}}, "price": {"type": "price", "settings": {}},
      "intro": {"type": "text", "settings": {"text": "7 paires de patchs hydrogel, à la caféine et à la vitamine C, pour le contour des yeux. Le petit coup de frais du matin.", "text_style": "body"}},
      "buy_buttons": {"type": "buy_buttons", "settings": {"show_dynamic_checkout": False}}},
    "block_order": ["title", "price", "intro", "buy_buttons"],
    "settings": {"product": "patchs-hydrogel-energisants-pour-les-yeux-a-la-cafeine-et-a-la-vitamine-c",
      "secondary_background": False, "media_size": "large", "color_scheme": "scheme-2",
      "padding_top": 56, "padding_bottom": 56}},
  "orane-rituel": {"type": "orane-rituel",
    "blocks": {
      "r1": {"type": "step", "settings": {"title": "Tu démaquilles", "text": "<p>On secoue, on imbibe un coton, on glisse. Maquillage et impuretés s'en vont, ta bonne humeur reste.</p>", "product": "demaquillant-biphasic-sans-parfum-1"}},
      "r2": {"type": "step", "settings": {"title": "Tu réveilles ton regard", "text": "<p>Une paire de patchs sous les yeux, le temps d'un café. Fais pas ta timide, ça se voit à peine.</p>", "product": "patchs-hydrogel-energisants-pour-les-yeux-a-la-cafeine-et-a-la-vitamine-c"}},
      "r3": {"type": "step", "settings": {"title": "Tu hydrates", "text": "<p>Une noisette de gel léger, sans effet gras. C'est bouclé : sourire obligatoire.</p>", "product": "gel-visage-au-zinc-sans-huile-pour-hommes"}}},
    "block_order": ["r1", "r2", "r3"],
    "settings": {"eyebrow": "Le rituel", "title": "Trois gestes, mine de rien", "sticker": "glow à la carte"}},
  "featured-collection-homme": fc("homme", 2, "Pour lui", 2),
}, "order": ["orane-hero", "orane-ticker", "multicolumn_garanties", "featured-collection-0", "collection-list",
             "orane-esprit", "produit-vedette", "orane-rituel", "featured-collection-homme"]}
dump("templates/index.json", index)
print("ok")
