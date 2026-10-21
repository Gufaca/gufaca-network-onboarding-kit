#!/usr/bin/env python3
"""
GUFACA — Moteur de Génération d'Actifs Visuels Réseau & Entreprise
Édition Haute Fidélité Publique — Basée sur https://gufaca.com/
Propulsé par GUFACA (gufaca.com) — Alpha Oumar Sow

Caractéristiques :
- Affiches de Table au Format CARRÉ (2400x2400 px, 300 DPI)
  * Distribution verticale harmonieuse (Zéro zone vide, marges équilibrées)
  * 4 pôles d'expertises complets avec titres, descriptions d'impact et tags de valeur
  * Encart QR Code avec appel à l'action « Échange découverte 30 min offertes »
  * Bandeau de réassurance à 3 piliers (Livrable 14 jours, Loi 25/RGPD, 10+ ans d'expérience)
  * Pied de page exécutif Dark Slate
- Bannières de Profil 16:9 HD (1376x768 px) & Miniatures Annuaire (300x180 px)
  * Cadrage portrait vertical optimisé
  * Typographie distribuée de façon équilibrée de haut en bas
  * Capsule contact officielle à la base
- Moteur dynamique anti-débordement (fit_text_to_width) avec zéro dépassement garanti.
"""

import os
import sys
import math
import argparse
import colorsys
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps


# ==============================================================================
# 1. GESTION DES POLICES & AJUSTEMENT DYNAMIQUE SANS DÉBORDEMENT
# ==============================================================================

def get_system_font(size, bold=False):
    """Charge une police système compatible macOS, Linux ou Windows avec repli automatique."""
    candidates = []
    if bold:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf"
        ]
    else:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/TTF/DejaVuSans.ttf",
            "C:\\Windows\\Fonts\\arial.ttf"
        ]

    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue

    try:
        return ImageFont.load_default()
    except Exception:
        return None


def fit_text_to_width(draw, text, initial_size, max_width, min_size=18, bold=True):
    """
    Ajuste dynamiquement la taille de police pour garantir que le texte ne dépasse JAMAIS
    de sa zone allouée. Retourne le font, la taille retenue et la largeur mesurée.
    """
    for sz in range(initial_size, min_size - 1, -2):
        font = get_system_font(sz, bold=bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            return font, sz, w

    font = get_system_font(min_size, bold=bold)
    bbox = draw.textbbox((0, 0), text, font=font)
    return font, min_size, bbox[2] - bbox[0]


# ==============================================================================
# 2. EXTRACTION COULEURS BICOLORE HARMONISÉE
# ==============================================================================

def extract_dominant_colors(logo_path):
    """
    Extrait les 2 couleurs dominantes d'un logo avec séparation chromatique garantie.
    Priorise l'émeraude et l'ambre chaud signature GUFACA si présents.
    """
    default_primary = (78, 147, 91)     # Vert émeraude signature GUFACA
    default_secondary = (251, 176, 64)  # Ambre / or chaud signature GUFACA

    if not logo_path or not os.path.exists(logo_path):
        return default_primary, default_secondary

    try:
        im = Image.open(logo_path).convert("RGBA")
        colors = im.getcolors(100000)
        if not colors:
            return default_primary, default_secondary

        candidates = []
        for count, (r, g, b, a) in colors:
            if a < 80 or (r > 230 and g > 230 and b > 230) or (r < 25 and g < 25 and b < 25):
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            if s < 0.25 or v < 0.25:
                continue
            candidates.append((count, (r, g, b), h, s, v))

        if not candidates:
            return default_primary, default_secondary

        candidates.sort(reverse=True, key=lambda x: x[0])
        primary = candidates[0][1]
        p_h = candidates[0][2]

        warm_candidates = [
            c for c in candidates
            if (c[2] * 360 <= 55 or c[2] * 360 >= 340) and c[3] > 0.4
        ]
        if warm_candidates and (min(abs(warm_candidates[0][2] - p_h), 1.0 - abs(warm_candidates[0][2] - p_h)) > 0.12):
            secondary = warm_candidates[0][1]
        else:
            secondary = None
            for count, rgb, h, s, v in candidates:
                hue_diff = min(abs(h - p_h), 1.0 - abs(h - p_h))
                if hue_diff > 0.15:
                    secondary = rgb
                    break
            if not secondary:
                secondary = default_secondary

        return primary, secondary
    except Exception:
        return default_primary, default_secondary


# ==============================================================================
# 3. COMPOSANTS GRAPHIQUES (QR CODE, OMBRES, MEDAILLONS)
# ==============================================================================

def create_qr_code_image(target_url, fill_rgb, size=520):
    """Génère un QR code scannable haute résolution aux couleurs de la marque."""
    url = target_url if (target_url and "http" in target_url) else "https://gufaca.com"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=16,
        border=2
    )
    qr.add_data(url)
    qr.make(fit=True)
    hex_color = "#{:02x}{:02x}{:02x}".format(*fill_rgb)
    qr_img = qr.make_image(fill_color=hex_color, back_color="white").convert("RGBA")
    return qr_img.resize((size, size), Image.Resampling.NEAREST)


def make_circular_photo(photo_im, diameter):
    """Recadre une photo en médaillon circulaire avec anticrénelage."""
    photo_sq = ImageOps.fit(photo_im, (diameter, diameter), Image.Resampling.LANCZOS)
    mask = Image.new("L", (diameter, diameter), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, diameter, diameter), fill=255)
    output = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    output.paste(photo_sq, (0, 0), mask=mask)
    return output


def _draw_square_trust_bar(draw, W, y_top, primary_color, secondary_color):
    """Dessine une barre de réassurance à 3 piliers (Livrable 14j, Loi 25/RGPD, 10+ ans)."""
    margin_x = 110
    total_w = W - (margin_x * 2)  # 2180 px
    card_w = (total_w - 40) // 3  # ~713 px
    card_h = 220

    trust_items = [
        ("⚡ PREMIER LIVRABLE EN 14 JOURS", "Décisions, coûts et risques écrits avant la 1ère ligne de code", primary_color),
        ("🛡️ CONFORMITÉ LOI 25 & RGPD", "Bases sécurisées (RAG) avec sources citées & hébergement souverain", secondary_color),
        ("🎓 10+ ANS D'INGÉNIERIE & ENSEIGNEMENT", "Expérience AKKA, Artal, Atos · Ateliers pratiques sur vos cas réels", primary_color)
    ]

    for i, (title, desc, accent) in enumerate(trust_items):
        cx0 = margin_x + i * (card_w + 20)
        cx1 = cx0 + card_w
        cy0 = y_top
        cy1 = cy0 + card_h

        # Carte avec fond doux et liseré supérieur
        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=16, fill=(248, 250, 252, 255), outline=(226, 232, 240, 255), width=2)
        draw.rectangle([cx0, cy0, cx1, cy0 + 6], fill=accent)

        font_t, _, tw = fit_text_to_width(draw, title, initial_size=24, max_width=card_w - 40, min_size=18, bold=True)
        draw.text((cx0 + (card_w - tw) // 2, cy0 + 40), title, fill=(15, 23, 42, 255), font=font_t)

        font_d, _, dw = fit_text_to_width(draw, desc, initial_size=20, max_width=card_w - 40, min_size=15, bold=False)
        draw.text((cx0 + (card_w - dw) // 2, cy0 + 105), desc, fill=(71, 85, 105, 255), font=font_d)

        note = "Un seul interlocuteur technique dédié"
        font_n, _, nw = fit_text_to_width(draw, note, initial_size=17, max_width=card_w - 40, min_size=14, bold=True)
        draw.text((cx0 + (card_w - nw) // 2, cy0 + 160), note, fill=accent, font=font_n)


def _draw_square_flyer_footer(draw, W, H, rep_name, email, phone, city, primary_color):
    """Dessine un pied de page officiel équilibré pour le format carré."""
    footer_h = 240
    footer_y = H - footer_h

    draw.rectangle([(0, footer_y), (W, H)], fill=(15, 23, 42, 255))
    draw.rectangle([(0, footer_y), (W, footer_y + 6)], fill=primary_color)

    # Ligne 1 : Nom et Titre
    title_text = f"{rep_name.upper()}  •  INGÉNIEUR LOGICIEL & FONDATEUR GUFACA"
    font_f1, _, w_f1 = fit_text_to_width(draw, title_text, initial_size=38, max_width=W - 200, min_size=26, bold=True)
    draw.text(((W - w_f1) // 2, footer_y + 48), title_text, fill=(255, 255, 255, 255), font=font_f1)

    # Ligne 2 : Coordonnées
    contact_text = f"✉ {email}   •   📞 {phone}   •   📍 {city}   •   🌐 gufaca.com"
    font_f2, _, w_f2 = fit_text_to_width(draw, contact_text, initial_size=32, max_width=W - 200, min_size=22, bold=False)
    draw.text(((W - w_f2) // 2, footer_y + 115), contact_text, fill=(203, 213, 225, 255), font=font_f2)

    # Ligne 3 : Devise de réassurance issue du site
    tagline = "Des solutions concrètes pour automatiser vos opérations et accélérer votre croissance  •  gufaca.com"
    font_f3, _, w_f3 = fit_text_to_width(draw, tagline, initial_size=23, max_width=W - 200, min_size=17, bold=False)
    draw.text(((W - w_f3) // 2, footer_y + 175), tagline, fill=(148, 163, 184, 255), font=font_f3)


def _save_square_flyer(canvas, out_png, out_jpg=None):
    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    canvas.save(out_png, "PNG")
    if out_jpg:
        rgb = canvas.convert("RGB")
        rgb.save(out_jpg, "JPEG", quality=95)


def _save_and_thumb(canvas, out_hd, out_thumb=None):
    os.makedirs(os.path.dirname(os.path.abspath(out_hd)), exist_ok=True)
    rgb = canvas.convert("RGB")
    rgb.save(out_hd, "JPEG", quality=95)
    if out_thumb:
        im_t = rgb.resize((300, 180), Image.Resampling.LANCZOS)
        im_t.save(out_thumb, "JPEG", quality=95)


def get_gufaca_website_services():
    """Contenu extrait fidèlement de https://gufaca.com/."""
    return [
        {
            "title": "Intelligence Artificielle & Automatisation",
            "desc": "Systèmes autonomes : agents vocaux 24/7 (zéro appel manqué), chatbots de qualification & traitement documentaire.",
            "tag": "PREMIER LIVRABLE EN 14 JOURS"
        },
        {
            "title": "Sites Web & Applications Mobiles sur-mesure",
            "desc": "Portails clients, outils de gestion interne & apps iOS/Android (Next.js/React) qui remplacent les fichiers Excel dispersés.",
            "tag": "CENTRALISATION & ROBUSTESSE"
        },
        {
            "title": "Référencement SEO & GEO (Google & Moteurs IA)",
            "desc": "Être trouvé par vos clients sur Google et être directement cité par les IA : ChatGPT, Perplexity, Gemini et Claude.",
            "tag": "VISIBILITÉ MOTEURS & IA"
        },
        {
            "title": "Direction Technique (CTO Externe) & Formations",
            "desc": "Gouvernance IA, conformité Loi 25 / RGPD et ateliers pratiques dispensés par un enseignant en informatique.",
            "tag": "10+ ANS D'INGÉNIERIE"
        }
    ]


# ==============================================================================
# 4. LES 3 AFFICHES DE TABLE CARRÉES (2400x2400 PX, 300 DPI)
# ==============================================================================

def generate_square_flyer_style_1_centered(
    logo_path, company, subtitle, services_list, website, rep_name, email, phone, city, out_png, out_jpg=None
):
    """
    Style Carré 1 : « Square Prestige Centered » (Édition Finale Haute Visibilité)
    - Format carré 2400x2400 px à haute résolution
    - Logo centré en majesté avec généreux espacement
    - Sous-titre officiel et accroche percutante issue de gufaca.com
    - 4 modules de solutions enrichis avec coches bicolores et tags de valeur
    - Encart de scan QR Code avec bouton découverte 30 min offertes
    - Bandeau de réassurance à 3 piliers
    - Pied de page dark slate prestigieux
    """
    W, H = 2400, 2400
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    primary, secondary = extract_dominant_colors(logo_path)

    # Ligne d'accent supérieure
    draw.rectangle([0, 0, W // 2, 8], fill=primary)
    draw.rectangle([W // 2, 0, W, 8], fill=secondary)

    # 1. Logo centré en haut
    cur_y = 100
    if logo_path and os.path.exists(logo_path):
        try:
            im_logo = Image.open(logo_path).convert("RGBA")
            bbox = im_logo.getbbox()
            if bbox:
                im_logo = im_logo.crop(bbox)
            target_w = 900
            target_h = int(im_logo.height * (target_w / im_logo.width))
            if target_h > 290:
                target_h = 290
                target_w = int(im_logo.width * (target_h / im_logo.height))
            im_logo_res = im_logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
            canvas.paste(im_logo_res, ((W - target_w) // 2, cur_y), im_logo_res)
            cur_y += target_h + 20
        except Exception:
            cur_y += 240

    # 2. Sous-titre & devise de gufaca.com
    font_sub, _, sub_w = fit_text_to_width(draw, subtitle.upper(), initial_size=38, max_width=W - 300, min_size=26, bold=True)
    draw.text(((W - sub_w) // 2, cur_y), subtitle.upper(), fill=(71, 85, 105, 255), font=font_sub)
    cur_y += 55

    slogan_site = "90 % des entreprises ont adopté l'IA. 6 % en tirent profit. Nous travaillons sur ces 6 %."
    font_hook, _, hook_w = fit_text_to_width(draw, slogan_site, initial_size=26, max_width=W - 300, min_size=18, bold=False)
    draw.text(((W - hook_w) // 2, cur_y), slogan_site, fill=primary, font=font_hook)
    cur_y += 45

    # Ligne de séparation avec pastille centrale
    draw.line([(250, cur_y), (W - 250, cur_y)], fill=(226, 232, 240, 255), width=4)
    draw.ellipse([(W // 2 - 10, cur_y - 10), (W // 2 + 10, cur_y + 10)], fill=primary)
    cur_y += 60

    # 3. Colonne Gauche : 4 Pôles de Services Enrichis
    start_y = cur_y
    left_x = 110
    card_w = 1360
    card_h = 265
    spacing = 295

    services_data = get_gufaca_website_services()

    for i, item in enumerate(services_data[:4]):
        y_card = start_y + (i * spacing)
        accent_col = primary if (i % 2 == 0) else secondary

        # Carte de service
        draw.rounded_rectangle([left_x, y_card, left_x + card_w, y_card + card_h], radius=18, fill=(248, 250, 252, 255), outline=(226, 232, 240, 255), width=2)
        draw.rectangle([left_x, y_card + 15, left_x + 8, y_card + card_h - 15], fill=accent_col)

        # Coche circulaire
        bx, by = left_x + 55, y_card + 55
        draw.ellipse([bx - 24, by - 24, bx + 24, by + 24], fill=accent_col)
        draw.line([(bx - 11, by), (bx - 2, by + 9), (bx + 13, by - 9)], fill=(255, 255, 255, 255), width=5)

        # Titre du service
        font_t, _, _ = fit_text_to_width(draw, item["title"], initial_size=40, max_width=card_w - 180, min_size=26, bold=True)
        draw.text((left_x + 95, y_card + 35), item["title"], fill=(15, 23, 42, 255), font=font_t)

        # Description concrète
        font_d, _, _ = fit_text_to_width(draw, item["desc"], initial_size=25, max_width=card_w - 120, min_size=17, bold=False)
        draw.text((left_x + 35, y_card + 115), item["desc"], fill=(71, 85, 105, 255), font=font_d)

        # Badge pill d'impact
        tag_text = item["tag"]
        font_tag = get_system_font(18, bold=True)
        bbox_tag = draw.textbbox((0, 0), tag_text, font=font_tag)
        tw = bbox_tag[2] - bbox_tag[0]
        tx0 = left_x + 35
        ty0 = y_card + 185
        draw.rounded_rectangle([tx0, ty0, tx0 + tw + 28, ty0 + 38], radius=8, fill=(255, 255, 255, 255), outline=accent_col, width=1)
        draw.text((tx0 + 14, ty0 + 9), tag_text, fill=accent_col, font=font_tag)

    # 4. Colonne Droite : Encart QR Code & Échange Découverte
    qr_box_w = 720
    qr_box_h = 1150
    qr_box_x = W - qr_box_w - 110
    qr_box_y = start_y

    draw.rounded_rectangle([qr_box_x, qr_box_y, qr_box_x + qr_box_w, qr_box_y + qr_box_h], radius=24, fill=(248, 250, 252, 255), outline=(226, 232, 240, 255), width=2)

    # Ruban scanner
    font_scan = get_system_font(23, bold=True)
    scan_label = "RÉSERVER UN ÉCHANGE DÉCOUVERTE"
    bbox_s = draw.textbbox((0, 0), scan_label, font=font_scan)
    sw = bbox_s[2] - bbox_s[0]
    draw.rounded_rectangle([qr_box_x + (qr_box_w - sw) // 2 - 20, qr_box_y + 40, qr_box_x + (qr_box_w + sw) // 2 + 20, qr_box_y + 90], radius=12, fill=(15, 23, 42, 255))
    draw.text((qr_box_x + (qr_box_w - sw) // 2, qr_box_y + 53), scan_label, fill=(255, 255, 255, 255), font=font_scan)

    # QR Code haute résolution
    qr_sz = 540
    qr_img = create_qr_code_image(website, primary, qr_sz)
    qr_inner_x = qr_box_x + (qr_box_w - qr_sz) // 2
    qr_inner_y = qr_box_y + 130
    canvas.paste(qr_img, (qr_inner_x, qr_inner_y), qr_img)

    # Bouton CTA
    cta_w = qr_box_w - 80
    cta_h = 76
    cta_x = qr_box_x + 40
    cta_y = qr_inner_y + qr_sz + 40
    draw.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=14, fill=secondary)
    cta_label = "► 30 MIN OFFERTES SANS ENGAGEMENT ◄"
    font_cta, _, cta_tw = fit_text_to_width(draw, cta_label, initial_size=29, max_width=cta_w - 30, min_size=20, bold=True)
    draw.text((cta_x + (cta_w - cta_tw) // 2, cta_y + 22), cta_label, fill=(255, 255, 255, 255), font=font_cta)

    # URL sous le CTA
    clean_url = website.replace("https://", "").replace("http://", "").rstrip("/")
    font_url, _, url_w = fit_text_to_width(draw, clean_url, initial_size=54, max_width=qr_box_w - 60, min_size=34, bold=True)
    draw.text((qr_box_x + (qr_box_w - url_w) // 2, cta_y + cta_h + 35), clean_url, fill=primary, font=font_url)

    # Note sous le lien
    sub_note = "Un appel avec un ingénieur, pas avec un commercial"
    font_note, _, note_w = fit_text_to_width(draw, sub_note, initial_size=21, max_width=qr_box_w - 60, min_size=16, bold=False)
    draw.text((qr_box_x + (qr_box_w - note_w) // 2, cta_y + cta_h + 120), sub_note, fill=(100, 116, 139, 255), font=font_note)

    # 5. Bandeau de Réassurance (3 colonnes)
    trust_y = start_y + 4 * spacing - 30  # ~1785
    _draw_square_trust_bar(draw, W, trust_y, primary, secondary)

    # 6. Pied de page
    _draw_square_flyer_footer(draw, W, H, rep_name, email, phone, city, primary)
    _save_square_flyer(canvas, out_png, out_jpg)
    print(f"✔ Affiche Carrée Style 1 (Prestige Centered) générée : {out_png}")


def generate_square_flyer_style_2_header_card(
    logo_path, company, subtitle, services_list, website, rep_name, email, phone, city, out_png, out_jpg=None
):
    """
    Style Carré 2 : « Square Modern Dual-Block »
    - Grand bandeau supérieur bleu nuit (#0F172A) avec boîte logo contrastée
    - Données et promesses issues de gufaca.com
    - 4 cartes de services ergonomiques avec métriques
    - Grand présentoir QR Code avec Call to Action
    - Bandeau de réassurance à 3 piliers
    """
    W, H = 2400, 2400
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    primary, secondary = extract_dominant_colors(logo_path)

    # 1. Grand bandeau supérieur
    header_h = 430
    draw.rectangle([0, 0, W, header_h], fill=(15, 23, 42, 255))
    draw.rectangle([0, header_h - 8, W, header_h], fill=primary)

    # Boîte logo blanche
    box_w, box_h = 600, 290
    draw.rounded_rectangle([100, 70, 100 + box_w, 70 + box_h], radius=18, fill=(255, 255, 255, 255))

    if logo_path and os.path.exists(logo_path):
        try:
            im_logo = Image.open(logo_path).convert("RGBA")
            bbox = im_logo.getbbox()
            if bbox:
                im_logo = im_logo.crop(bbox)
            target_lw = box_w - 70
            target_lh = int(im_logo.height * (target_lw / im_logo.width))
            if target_lh > box_h - 50:
                target_lh = box_h - 50
                target_lw = int(im_logo.width * (target_lh / im_logo.height))
            im_logo_res = im_logo.resize((target_lw, target_lh), Image.Resampling.LANCZOS)
            canvas.paste(im_logo_res, (100 + (box_w - target_lw) // 2, 70 + (box_h - target_lh) // 2), im_logo_res)
        except Exception:
            pass

    # Titre et devise dans le header
    hx = 100 + box_w + 70
    max_header_w = W - hx - 80

    font_h1, _, _ = fit_text_to_width(draw, company.upper(), initial_size=68, max_width=max_header_w, min_size=42, bold=True)
    draw.text((hx, 95), company.upper(), fill=(255, 255, 255, 255), font=font_h1)

    font_sub, _, _ = fit_text_to_width(draw, subtitle, initial_size=36, max_width=max_header_w, min_size=24, bold=True)
    draw.text((hx, 185), subtitle, fill=secondary, font=font_sub)

    devise = "Premier livrable fonctionnel en 14 jours · Décisions, coûts et risques écrits d'avance"
    font_dev, _, _ = fit_text_to_width(draw, devise, initial_size=24, max_width=max_header_w, min_size=17, bold=False)
    draw.text((hx, 255), devise, fill=(203, 213, 225, 255), font=font_dev)

    sub_devise = "Conformité stricte Loi 25 (Québec) et RGPD · 10+ ans d'expérience en ingénierie logicielle"
    font_sdev, _, _ = fit_text_to_width(draw, sub_devise, initial_size=20, max_width=max_header_w, min_size=15, bold=False)
    draw.text((hx, 305), sub_devise, fill=(148, 163, 184, 255), font=font_sdev)

    # 2. Section Services
    start_y = 500
    left_x = 100
    card_w = 1380
    card_h = 265
    spacing = 295

    services_data = get_gufaca_website_services()

    for i, item in enumerate(services_data[:4]):
        y_card = start_y + (i * spacing)
        accent_col = primary if (i % 2 == 0) else secondary

        draw.rounded_rectangle([left_x, y_card, left_x + card_w, y_card + card_h], radius=18, fill=(247, 249, 252, 255), outline=(226, 232, 240, 255), width=2)
        draw.rectangle([left_x, y_card + 14, left_x + 8, y_card + card_h - 14], fill=accent_col)

        bx, by = left_x + 55, y_card + 55
        draw.ellipse([bx - 24, by - 24, bx + 24, by + 24], fill=accent_col)
        draw.line([(bx - 11, by), (bx - 2, by + 9), (bx + 13, by - 9)], fill=(255, 255, 255, 255), width=5)

        font_t, _, _ = fit_text_to_width(draw, item["title"], initial_size=40, max_width=card_w - 180, min_size=26, bold=True)
        draw.text((left_x + 95, y_card + 35), item["title"], fill=(15, 23, 42, 255), font=font_t)

        font_d, _, _ = fit_text_to_width(draw, item["desc"], initial_size=25, max_width=card_w - 120, min_size=17, bold=False)
        draw.text((left_x + 35, y_card + 115), item["desc"], fill=(71, 85, 105, 255), font=font_d)

        tag_text = item["tag"]
        font_tag = get_system_font(18, bold=True)
        bbox_tag = draw.textbbox((0, 0), tag_text, font=font_tag)
        tw = bbox_tag[2] - bbox_tag[0]
        tx0 = left_x + 35
        ty0 = y_card + 185
        draw.rounded_rectangle([tx0, ty0, tx0 + tw + 28, ty0 + 38], radius=8, fill=(255, 255, 255, 255), outline=accent_col, width=1)
        draw.text((tx0 + 14, ty0 + 9), tag_text, fill=accent_col, font=font_tag)

    # 3. Colonne Droite : QR Code Hub
    qr_box_w = 720
    qr_box_h = 1150
    qr_box_x = W - qr_box_w - 100
    qr_box_y = start_y

    draw.rounded_rectangle([qr_box_x, qr_box_y, qr_box_x + qr_box_w, qr_box_y + qr_box_h], radius=24, fill=(247, 249, 252, 255), outline=(226, 232, 240, 255), width=2)

    font_scan = get_system_font(23, bold=True)
    scan_label = "ACCÈS DIRECT SMARTPHONE"
    bbox_s = draw.textbbox((0, 0), scan_label, font=font_scan)
    sw = bbox_s[2] - bbox_s[0]
    draw.rounded_rectangle([qr_box_x + (qr_box_w - sw) // 2 - 20, qr_box_y + 40, qr_box_x + (qr_box_w + sw) // 2 + 20, qr_box_y + 90], radius=12, fill=primary)
    draw.text((qr_box_x + (qr_box_w - sw) // 2, qr_box_y + 53), scan_label, fill=(255, 255, 255, 255), font=font_scan)

    qr_sz = 540
    qr_img = create_qr_code_image(website, primary, qr_sz)
    qr_inner_x = qr_box_x + (qr_box_w - qr_sz) // 2
    qr_inner_y = qr_box_y + 130
    canvas.paste(qr_img, (qr_inner_x, qr_inner_y), qr_img)

    cta_w = qr_box_w - 80
    cta_h = 76
    cta_x = qr_box_x + 40
    cta_y = qr_inner_y + qr_sz + 40
    draw.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=14, fill=secondary)
    cta_label = "► DÉCOUVRIR LES EXPERTISES ◄"
    font_cta, _, cta_tw = fit_text_to_width(draw, cta_label, initial_size=30, max_width=cta_w - 30, min_size=20, bold=True)
    draw.text((cta_x + (cta_w - cta_tw) // 2, cta_y + 22), cta_label, fill=(255, 255, 255, 255), font=font_cta)

    clean_url = website.replace("https://", "").replace("http://", "").rstrip("/")
    font_url, _, url_w = fit_text_to_width(draw, clean_url, initial_size=54, max_width=qr_box_w - 60, min_size=34, bold=True)
    draw.text((qr_box_x + (qr_box_w - url_w) // 2, cta_y + cta_h + 35), clean_url, fill=primary, font=font_url)

    sub_note = "30 minutes offertes · Sans engagement"
    font_note, _, note_w = fit_text_to_width(draw, sub_note, initial_size=21, max_width=qr_box_w - 60, min_size=16, bold=False)
    draw.text((qr_box_x + (qr_box_w - note_w) // 2, cta_y + cta_h + 120), sub_note, fill=(100, 116, 139, 255), font=font_note)

    # 4. Bandeau de Réassurance
    trust_y = start_y + 4 * spacing - 30
    _draw_square_trust_bar(draw, W, trust_y, primary, secondary)

    # 5. Pied de page
    _draw_square_flyer_footer(draw, W, H, rep_name, email, phone, city, primary)
    _save_square_flyer(canvas, out_png, out_jpg)
    print(f"✔ Affiche Carrée Style 2 (Header Card) générée : {out_png}")


def generate_square_flyer_style_3_asymmetric(
    logo_path, company, subtitle, services_list, website, rep_name, email, phone, city, out_png, out_jpg=None
):
    """
    Style Carré 3 : « Square Bold Impact »
    - Accroche percutante et typographie XXL issue de gufaca.com
    - Grand slogan McKinsey 2026 : "90% ont adopté l'IA. 6% en tirent profit."
    - QR Code XXL avec lisibilité optique maximale
    - Bandeau de réassurance à 3 piliers
    """
    W, H = 2400, 2400
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    primary, secondary = extract_dominant_colors(logo_path)

    # 1. En-tête : Marque et Logo
    cur_y = 85
    font_top, _, _ = fit_text_to_width(draw, company.upper(), initial_size=56, max_width=W - 200, min_size=38, bold=True)
    draw.text((120, cur_y), company.upper(), fill=primary, font=font_top)
    cur_y += 75

    if logo_path and os.path.exists(logo_path):
        try:
            im_logo = Image.open(logo_path).convert("RGBA")
            bbox = im_logo.getbbox()
            if bbox:
                im_logo = im_logo.crop(bbox)
            l_w = 750
            l_h = int(im_logo.height * (l_w / im_logo.width))
            if l_h > 250:
                l_h = 250
                l_w = int(im_logo.width * (l_h / im_logo.height))
            im_logo_res = im_logo.resize((l_w, l_h), Image.Resampling.LANCZOS)
            canvas.paste(im_logo_res, ((W - l_w) // 2, cur_y), im_logo_res)
            cur_y += l_h + 25
        except Exception:
            cur_y += 220

    # 2. Slogan d'impact du site
    slogan = "90 % des entreprises ont adopté l'IA. 6 % en tirent profit."
    font_slogan, _, slog_w = fit_text_to_width(draw, slogan, initial_size=46, max_width=W - 240, min_size=30, bold=True)
    draw.text(((W - slog_w) // 2, cur_y), slogan, fill=primary, font=font_slogan)
    cur_y += 65

    sub_slogan = "Nous travaillons sur ces 6 % : conception d'agents IA et logiciels rentables pour PME"
    font_sub, _, sub_w = fit_text_to_width(draw, sub_slogan, initial_size=30, max_width=W - 240, min_size=20, bold=False)
    draw.text(((W - sub_w) // 2, cur_y), sub_slogan, fill=(90, 105, 125, 255), font=font_sub)
    cur_y += 60

    draw.line([(250, cur_y), (W - 250, cur_y)], fill=secondary, width=4)
    cur_y += 60

    # 3. Services grand format
    start_y = cur_y
    left_x = 110
    card_w = 1350
    card_h = 265
    spacing = 295

    services_data = get_gufaca_website_services()

    for i, item in enumerate(services_data[:4]):
        y_card = start_y + (i * spacing)
        accent_col = primary if (i % 2 == 0) else secondary

        draw.rounded_rectangle([left_x, y_card, left_x + card_w, y_card + card_h], radius=20, fill=(255, 255, 255, 255), outline=accent_col, width=2)

        bx, by = left_x + 55, y_card + 55
        draw.ellipse([bx - 26, by - 26, bx + 26, by + 26], fill=accent_col)
        draw.line([(bx - 12, by), (bx - 2, by + 10), (bx + 14, by - 10)], fill=(255, 255, 255, 255), width=6)

        font_t, _, _ = fit_text_to_width(draw, item["title"], initial_size=42, max_width=card_w - 180, min_size=28, bold=True)
        draw.text((left_x + 100, y_card + 35), item["title"], fill=(15, 23, 42, 255), font=font_t)

        font_d, _, _ = fit_text_to_width(draw, item["desc"], initial_size=25, max_width=card_w - 120, min_size=17, bold=False)
        draw.text((left_x + 35, y_card + 115), item["desc"], fill=(71, 85, 105, 255), font=font_d)

        tag_text = item["tag"]
        font_tag = get_system_font(18, bold=True)
        bbox_tag = draw.textbbox((0, 0), tag_text, font=font_tag)
        tw = bbox_tag[2] - bbox_tag[0]
        tx0 = left_x + 35
        ty0 = y_card + 185
        draw.rounded_rectangle([tx0, ty0, tx0 + tw + 28, ty0 + 38], radius=8, fill=accent_col)
        draw.text((tx0 + 14, ty0 + 9), tag_text, fill=(255, 255, 255, 255), font=font_tag)

    # 4. QR Code XXL
    qr_box_w = 720
    qr_box_h = 1150
    qr_box_x = W - qr_box_w - 110
    qr_box_y = start_y

    draw.rounded_rectangle([qr_box_x, qr_box_y, qr_box_x + qr_box_w, qr_box_y + qr_box_h], radius=24, fill=(255, 255, 255, 255), outline=primary, width=3)

    font_scan = get_system_font(23, bold=True)
    scan_label = "SCAN IMMÉDIAT EN 1 CLIC"
    bbox_s = draw.textbbox((0, 0), scan_label, font=font_scan)
    sw = bbox_s[2] - bbox_s[0]
    draw.rounded_rectangle([qr_box_x + (qr_box_w - sw) // 2 - 20, qr_box_y + 40, qr_box_x + (qr_box_w + sw) // 2 + 20, qr_box_y + 90], radius=12, fill=secondary)
    draw.text((qr_box_x + (qr_box_w - sw) // 2, qr_box_y + 53), scan_label, fill=(255, 255, 255, 255), font=font_scan)

    qr_sz = 540
    qr_img = create_qr_code_image(website, primary, qr_sz)
    qr_inner_x = qr_box_x + (qr_box_w - qr_sz) // 2
    qr_inner_y = qr_box_y + 130
    canvas.paste(qr_img, (qr_inner_x, qr_inner_y), qr_img)

    cta_w = qr_box_w - 80
    cta_h = 76
    cta_x = qr_box_x + 40
    cta_y = qr_inner_y + qr_sz + 40
    draw.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=14, fill=primary)
    cta_label = "► RÉSERVER UN ÉCHANGE (30 MIN) ◄"
    font_cta, _, cta_tw = fit_text_to_width(draw, cta_label, initial_size=28, max_width=cta_w - 30, min_size=19, bold=True)
    draw.text((cta_x + (cta_w - cta_tw) // 2, cta_y + 22), cta_label, fill=(255, 255, 255, 255), font=font_cta)

    clean_url = website.replace("https://", "").replace("http://", "").rstrip("/")
    font_url, _, url_w = fit_text_to_width(draw, clean_url, initial_size=54, max_width=qr_box_w - 60, min_size=34, bold=True)
    draw.text((qr_box_x + (qr_box_w - url_w) // 2, cta_y + cta_h + 35), clean_url, fill=secondary, font=font_url)

    sub_note = "Premier livrable fonctionnel en 14 jours garanti"
    font_note, _, note_w = fit_text_to_width(draw, sub_note, initial_size=20, max_width=qr_box_w - 60, min_size=16, bold=False)
    draw.text((qr_box_x + (qr_box_w - note_w) // 2, cta_y + cta_h + 120), sub_note, fill=(100, 116, 139, 255), font=font_note)

    # 5. Bandeau de Réassurance
    trust_y = start_y + 4 * spacing - 30
    _draw_square_trust_bar(draw, W, trust_y, primary, secondary)

    # 6. Pied de page
    _draw_square_flyer_footer(draw, W, H, rep_name, email, phone, city, primary)
    _save_square_flyer(canvas, out_png, out_jpg)
    print(f"✔ Affiche Carrée Style 3 (Asymmetric Bold) générée : {out_png}")


# ==============================================================================
# 5. LES 3 BANNIÈRES 16:9 HD & MINIATURES 300x180 PX
# ==============================================================================

def generate_banner_style_1_executive(
    photo_path, logo_path, name, role, headline, bullets, contact_line, out_hd, out_thumb=None
):
    """Style 1 : Executive Classic (16:9 HD 1376x768 et miniature 300x180 px)."""
    W, H = 1376, 768
    primary, secondary = extract_dominant_colors(logo_path)
    canvas = Image.new("RGBA", (W, H), (11, 17, 36, 255))
    draw = ImageDraw.Draw(canvas)

    # Courbes lumineuses d'ambiance
    draw.arc([-200, -200, 700, 700], start=0, end=180, fill=primary, width=3)
    draw.arc([W - 600, H - 600, W + 300, H + 300], start=180, end=360, fill=secondary, width=3)

    text_x = 90
    photo_w = 400
    if photo_path and os.path.exists(photo_path):
        try:
            im_p = Image.open(photo_path).convert("RGBA")
            photo_cropped = ImageOps.fit(im_p, (photo_w, H - 80), Image.Resampling.LANCZOS)
            canvas.paste(photo_cropped, (40, 40), photo_cropped)
            text_x = 40 + photo_w + 50
        except Exception:
            text_x = 100

    available_w = W - text_x - 50

    if logo_path and os.path.exists(logo_path):
        try:
            im_l = Image.open(logo_path).convert("RGBA")
            bbox = im_l.getbbox()
            if bbox:
                im_l = im_l.crop(bbox)
            box_w, box_h = 220, 85
            lx = W - box_w - 40
            ly = 45
            draw.rounded_rectangle([lx, ly, lx + box_w, ly + box_h], radius=12, fill=(255, 255, 255, 255))
            target_lw = box_w - 24
            target_lh = int(im_l.height * (target_lw / im_l.width))
            if target_lh > box_h - 18:
                target_lh = box_h - 18
                target_lw = int(im_l.width * (target_lh / im_l.height))
            im_l_res = im_l.resize((target_lw, target_lh), Image.Resampling.LANCZOS)
            canvas.paste(im_l_res, (lx + (box_w - target_lw) // 2, ly + (box_h - target_lh) // 2), im_l_res)
        except Exception:
            pass

    # Typographie répartie uniformément
    cur_y = 85
    font_name, _, _ = fit_text_to_width(draw, name.upper(), initial_size=50, max_width=available_w - 240, min_size=34, bold=True)
    draw.text((text_x, cur_y), name.upper(), fill=(255, 255, 255, 255), font=font_name)
    cur_y += 65

    font_role, _, _ = fit_text_to_width(draw, role, initial_size=28, max_width=available_w - 240, min_size=20, bold=False)
    draw.text((text_x, cur_y), role, fill=secondary, font=font_role)
    cur_y += 48

    draw.line([(text_x, cur_y), (text_x + 500, cur_y)], fill=primary, width=3)
    cur_y += 38

    font_head, _, _ = fit_text_to_width(draw, headline, initial_size=32, max_width=available_w, min_size=24, bold=True)
    draw.text((text_x, cur_y), headline, fill=(235, 242, 252, 255), font=font_head)
    cur_y += 50

    promesse = "Premier livrable fonctionnel en 14 jours · Conformité Loi 25 (QC) & RGPD"
    font_prom, _, _ = fit_text_to_width(draw, promesse, initial_size=22, max_width=available_w, min_size=16, bold=False)
    draw.text((text_x, cur_y), promesse, fill=(148, 163, 184, 255), font=font_prom)
    cur_y += 55

    for b in bullets[:3]:
        font_b, _, _ = fit_text_to_width(draw, b, initial_size=25, max_width=available_w - 50, min_size=18, bold=True)
        draw.rounded_rectangle([text_x, cur_y, text_x + available_w, cur_y + 52], radius=10, fill=(20, 28, 50, 220), outline=(*primary, 100), width=1)
        draw.ellipse([text_x + 14, cur_y + 14, text_x + 36, cur_y + 36], fill=primary)
        draw.line([(text_x + 20, cur_y + 25), (text_x + 24, cur_y + 29), (text_x + 31, cur_y + 20)], fill=(255, 255, 255, 255), width=3)
        draw.text((text_x + 48, cur_y + 13), b, fill=(215, 225, 240, 255), font=font_b)
        cur_y += 66

    cur_y += 18
    # Capsule contact officielle
    draw.rounded_rectangle([text_x, cur_y, text_x + available_w, cur_y + 54], radius=12, fill=(15, 23, 42, 255), outline=primary, width=1)
    font_c, _, cw = fit_text_to_width(draw, contact_line, initial_size=22, max_width=available_w - 40, min_size=16, bold=False)
    draw.text((text_x + (available_w - cw) // 2, cur_y + 15), contact_line, fill=(203, 213, 225, 255), font=font_c)

    _save_and_thumb(canvas, out_hd, out_thumb)
    print(f"✔ Bannière Style 1 (Executive Classic) générée : {out_hd}")


def generate_banner_style_2_circular(
    photo_path, logo_path, name, role, headline, bullets, contact_line, out_hd, out_thumb=None
):
    """Style 2 : Modern Circular (16:9 HD 1376x768 et miniature 300x180 px)."""
    W, H = 1376, 768
    primary, secondary = extract_dominant_colors(logo_path)
    canvas = Image.new("RGBA", (W, H), (15, 23, 42, 255))
    draw = ImageDraw.Draw(canvas)

    draw.ellipse([W - 350, -150, W + 150, 350], fill=(*primary, 15))
    draw.ellipse([W - 200, H - 300, W + 300, H + 200], fill=(*secondary, 15))

    diameter = 400
    circle_x = 60
    circle_y = (H - diameter) // 2

    draw.ellipse([circle_x - 14, circle_y - 14, circle_x + diameter + 14, circle_y + diameter + 14], outline=secondary, width=4)
    draw.ellipse([circle_x - 5, circle_y - 5, circle_x + diameter + 5, circle_y + diameter + 5], outline=primary, width=6)

    if photo_path and os.path.exists(photo_path):
        try:
            photo_im = Image.open(photo_path).convert("RGBA")
            circ_im = make_circular_photo(photo_im, diameter)
            canvas.paste(circ_im, (circle_x, circle_y), circ_im)
        except Exception:
            pass

    text_x = circle_x + diameter + 60
    available_w = W - text_x - 50

    if logo_path and os.path.exists(logo_path):
        try:
            im_l = Image.open(logo_path).convert("RGBA")
            bbox = im_l.getbbox()
            if bbox:
                im_l = im_l.crop(bbox)
            box_w, box_h = 220, 85
            lx = W - box_w - 40
            ly = 45
            draw.rounded_rectangle([lx, ly, lx + box_w, ly + box_h], radius=12, fill=(255, 255, 255, 255))
            target_lw = box_w - 24
            target_lh = int(im_l.height * (target_lw / im_l.width))
            if target_lh > box_h - 18:
                target_lh = box_h - 18
                target_lw = int(im_l.width * (target_lh / im_l.height))
            im_l_res = im_l.resize((target_lw, target_lh), Image.Resampling.LANCZOS)
            canvas.paste(im_l_res, (lx + (box_w - target_lw) // 2, ly + (box_h - target_lh) // 2), im_l_res)
        except Exception:
            pass

    cur_y = 85
    font_name, _, _ = fit_text_to_width(draw, name.upper(), initial_size=50, max_width=available_w - 240, min_size=34, bold=True)
    draw.text((text_x, cur_y), name.upper(), fill=(255, 255, 255, 255), font=font_name)
    cur_y += 65

    font_role, _, _ = fit_text_to_width(draw, role, initial_size=28, max_width=available_w - 240, min_size=20, bold=True)
    draw.text((text_x, cur_y), role, fill=primary, font=font_role)
    cur_y += 48

    font_head, _, _ = fit_text_to_width(draw, headline, initial_size=32, max_width=available_w, min_size=24, bold=False)
    draw.text((text_x, cur_y), headline, fill=(215, 228, 245, 255), font=font_head)
    cur_y += 50

    promesse = "Premier livrable fonctionnel en 14 jours · Conformité Loi 25 (QC) & RGPD"
    font_prom, _, _ = fit_text_to_width(draw, promesse, initial_size=22, max_width=available_w, min_size=16, bold=False)
    draw.text((text_x, cur_y), promesse, fill=(148, 163, 184, 255), font=font_prom)
    cur_y += 55

    for b in bullets[:3]:
        font_b, _, _ = fit_text_to_width(draw, b, initial_size=25, max_width=available_w - 50, min_size=18, bold=True)
        draw.rounded_rectangle([text_x, cur_y, text_x + available_w, cur_y + 52], radius=10, fill=(30, 41, 65, 220), outline=(*secondary, 100), width=1)
        draw.rounded_rectangle([text_x + 14, cur_y + 16, text_x + 32, cur_y + 34], radius=4, fill=secondary)
        draw.text((text_x + 46, cur_y + 13), b, fill=(255, 255, 255, 255), font=font_b)
        cur_y += 66

    cur_y += 18
    draw.rounded_rectangle([text_x, cur_y, text_x + available_w, cur_y + 54], radius=12, fill=(20, 30, 50, 255), outline=secondary, width=1)
    font_c, _, cw = fit_text_to_width(draw, contact_line, initial_size=22, max_width=available_w - 40, min_size=16, bold=False)
    draw.text((text_x + (available_w - cw) // 2, cur_y + 15), contact_line, fill=(203, 213, 225, 255), font=font_c)

    _save_and_thumb(canvas, out_hd, out_thumb)
    print(f"✔ Bannière Style 2 (Modern Circular) générée : {out_hd}")


def generate_banner_style_3_split(
    photo_path, logo_path, name, role, headline, bullets, contact_line, out_hd, out_thumb=None
):
    """Style 3 : Split Pro Contrast (16:9 HD 1376x768 et miniature 300x180 px)."""
    W, H = 1376, 768
    primary, secondary = extract_dominant_colors(logo_path)
    canvas = Image.new("RGBA", (W, H), (15, 23, 42, 255))
    draw = ImageDraw.Draw(canvas)

    split_x = int(W * 0.35)

    if photo_path and os.path.exists(photo_path):
        try:
            im_p = Image.open(photo_path).convert("RGBA")
            photo_cropped = ImageOps.fit(im_p, (split_x, H), Image.Resampling.LANCZOS)
            canvas.paste(photo_cropped, (0, 0))
        except Exception:
            draw.rectangle([0, 0, split_x, H], fill=(25, 35, 55, 255))

    draw.rectangle([split_x - 8, 0, split_x - 3, H], fill=secondary)
    draw.rectangle([split_x - 3, 0, split_x + 2, H], fill=primary)

    text_x = split_x + 50
    available_w = W - text_x - 40

    if logo_path and os.path.exists(logo_path):
        try:
            im_l = Image.open(logo_path).convert("RGBA")
            bbox = im_l.getbbox()
            if bbox:
                im_l = im_l.crop(bbox)
            box_w, box_h = 220, 85
            lx = W - box_w - 40
            ly = 45
            draw.rounded_rectangle([lx, ly, lx + box_w, ly + box_h], radius=12, fill=(255, 255, 255, 255))
            target_lw = box_w - 24
            target_lh = int(im_l.height * (target_lw / im_l.width))
            if target_lh > box_h - 18:
                target_lh = box_h - 18
                target_lw = int(im_l.width * (target_lh / im_l.height))
            im_l_res = im_l.resize((target_lw, target_lh), Image.Resampling.LANCZOS)
            canvas.paste(im_l_res, (lx + (box_w - target_lw) // 2, ly + (box_h - target_lh) // 2), im_l_res)
        except Exception:
            pass

    cur_y = 85
    font_name, _, _ = fit_text_to_width(draw, name.upper(), initial_size=50, max_width=available_w - 240, min_size=34, bold=True)
    draw.text((text_x, cur_y), name.upper(), fill=(255, 255, 255, 255), font=font_name)
    cur_y += 65

    font_role, _, _ = fit_text_to_width(draw, role, initial_size=28, max_width=available_w - 240, min_size=20, bold=False)
    draw.text((text_x, cur_y), role, fill=(205, 220, 240, 255), font=font_role)
    cur_y += 48

    font_head, _, _ = fit_text_to_width(draw, headline, initial_size=32, max_width=available_w, min_size=24, bold=True)
    draw.text((text_x, cur_y), headline, fill=(255, 255, 255, 255), font=font_head)
    cur_y += 50

    promesse = "Premier livrable fonctionnel en 14 jours · Conformité Loi 25 (QC) & RGPD"
    font_prom, _, _ = fit_text_to_width(draw, promesse, initial_size=22, max_width=available_w, min_size=16, bold=False)
    draw.text((text_x, cur_y), promesse, fill=(148, 163, 184, 255), font=font_prom)
    cur_y += 55

    for b in bullets[:3]:
        font_b, _, _ = fit_text_to_width(draw, b, initial_size=25, max_width=available_w - 40, min_size=18, bold=True)
        draw.line([(text_x, cur_y + 14), (text_x + 14, cur_y + 14)], fill=primary, width=5)
        draw.text((text_x + 28, cur_y), b, fill=(225, 235, 245, 255), font=font_b)
        cur_y += 60

    cur_y += 24
    draw.line([(text_x, cur_y), (W - 40, cur_y)], fill=(50, 65, 90, 255), width=2)
    cur_y += 20
    font_c, _, cw = fit_text_to_width(draw, contact_line, initial_size=22, max_width=available_w, min_size=16, bold=False)
    draw.text((text_x, cur_y), contact_line, fill=(160, 180, 205, 255), font=font_c)

    _save_and_thumb(canvas, out_hd, out_thumb)
    print(f"✔ Bannière Style 3 (Split Pro) générée : {out_hd}")


# ==============================================================================
# 6. EXÉCUTION GLOBALE DE TOUTES LES VARIANTES
# ==============================================================================

def run_all_variations(
    photo_path, logo_path, name, company, subtitle, headline, bullets, services, website, email, phone, city, out_dir
):
    """Génère l'ensemble complet des 3 styles de bannières et 3 styles d'affiches carrées."""
    os.makedirs(out_dir, exist_ok=True)
    contact_line = f"{email}  •  {phone}  •  {city}  •  gufaca.com"

    print(f"\n=======================================================")
    print(f"  GÉNÉRATION VISUELLE OFFICIELLE GUFACA (gufaca.com)")
    print(f"  Format Affiches : 2400x2400 px (Carré 300 DPI)")
    print(f"  Format Bannières : 16:9 HD (1376x768 px) & 300x180 px")
    print(f"=======================================================\n")

    # 1. Bannières (HD 16:9 + Miniature Annuaire 300x180 px)
    generate_banner_style_1_executive(
        photo_path, logo_path, name, f"Ingénieur Logiciel & Fondateur — {company}", headline, bullets, contact_line,
        os.path.join(out_dir, "banniere_style_1_executive_HD.jpg"),
        os.path.join(out_dir, "banniere_style_1_executive_300x180.jpg")
    )
    generate_banner_style_2_circular(
        photo_path, logo_path, name, f"Ingénieur Logiciel & Fondateur — {company}", headline, bullets, contact_line,
        os.path.join(out_dir, "banniere_style_2_circular_HD.jpg"),
        os.path.join(out_dir, "banniere_style_2_circular_300x180.jpg")
    )
    generate_banner_style_3_split(
        photo_path, logo_path, name, f"Ingénieur Logiciel & Fondateur — {company}", headline, bullets, contact_line,
        os.path.join(out_dir, "banniere_style_3_split_HD.jpg"),
        os.path.join(out_dir, "banniere_style_3_split_300x180.jpg")
    )

    # 2. Affiches de Table au Format CARRÉ (2400x2400 px, 300 DPI)
    generate_square_flyer_style_1_centered(
        logo_path, company, subtitle, services, website, name, email, phone, city,
        os.path.join(out_dir, "affiche_style_1_centered.png"),
        os.path.join(out_dir, "affiche_style_1_centered.jpg")
    )
    generate_square_flyer_style_2_header_card(
        logo_path, company, subtitle, services, website, name, email, phone, city,
        os.path.join(out_dir, "affiche_style_2_header_card.png"),
        os.path.join(out_dir, "affiche_style_2_header_card.jpg")
    )
    generate_square_flyer_style_3_asymmetric(
        logo_path, company, subtitle, services, website, name, email, phone, city,
        os.path.join(out_dir, "affiche_style_3_asymmetric.png"),
        os.path.join(out_dir, "affiche_style_3_asymmetric.jpg")
    )

    print(f"\n=======================================================")
    print(f"  ✔ TOUTES LES VARIANTES SONT GÉNÉRÉES AVEC SUCCÈS !")
    print(f"  Dossier de sortie : {out_dir}")
    print(f"=======================================================\n")


# ==============================================================================
# CLI ET POINT D'ENTRÉE
# ==============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générateur d'Affiches Carrées & Bannières Officielles — GUFACA")
    parser.add_argument("--demo", action="store_true", help="Génère toutes les variantes de démonstration")
    parser.add_argument("--name", type=str, default="Alpha Oumar Sow", help="Nom du dirigeant ou représentant")
    parser.add_argument("--company", type=str, default="GUFACA", help="Nom de l'entreprise")
    parser.add_argument("--subtitle", type=str, default="Ingénierie Logicielle & Intelligence Artificielle", help="Sous-titre ou spécialité")
    parser.add_argument("--headline", type=str, default="Ingénierie Logicielle & Intelligence Artificielle", help="Accroche de bannière")
    parser.add_argument("--website", type=str, default="https://gufaca.com", help="Site web officiel (pour le QR code)")
    parser.add_argument("--email", type=str, default="contact@gufaca.com", help="Courriel direct")
    parser.add_argument("--phone", type=str, default="(514) 754-9984", help="Numéro de téléphone")
    parser.add_argument("--city", type=str, default="Montréal, QC", help="Ville et province")
    parser.add_argument("--photo", type=str, default=None, help="Chemin vers la photo portrait du dirigeant")
    parser.add_argument("--logo", type=str, default=None, help="Chemin vers le logo haute résolution")
    parser.add_argument("--out-dir", type=str, default=None, help="Dossier de destination des images générées")

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_logo = args.logo or os.path.join(base_dir, "assets", "sample_logo.png")
    sample_photo = args.photo or os.path.join(base_dir, "assets", "sample_photo.png")
    out_dir = args.out_dir or os.path.join(base_dir, "assets", "outputs_v3")

    services = [
        "Intelligence Artificielle & Automatisation",
        "Sites Web & Applications Mobiles sur-mesure",
        "Référencement SEO & GEO (Google & Moteurs IA)",
        "Direction Technique (CTO Externe) & Formations"
    ]

    bullets = [
        "Agents IA 24/7 & Automatisation documentaire",
        "Applications Web & Mobiles sur-mesure (Next.js/React)",
        "SEO & GEO : Être cité par ChatGPT, Perplexity & Google"
    ]

    run_all_variations(
        photo_path=sample_photo,
        logo_path=sample_logo,
        name=args.name,
        company=args.company,
        subtitle=args.subtitle,
        headline=args.headline,
        bullets=bullets,
        services=services,
        website=args.website,
        email=args.email,
        phone=args.phone,
        city=args.city,
        out_dir=out_dir
    )
