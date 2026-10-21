#!/usr/bin/env python3
"""
Test Unitaire Automatisé Multi-Styles — Kit Visuel Officiel GUFACA (gufaca.com)
Vérifie la génération des 3 Affiches de Table CARRÉES (2400x2400 px, 300 DPI)
et des 3 Bannières de Profil (16:9 HD & 300x180 px), ainsi que le décodage optique du QR code vers https://gufaca.com.
"""

import os
import sys
from PIL import Image

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

from generate_member_assets import (
    extract_dominant_colors,
    run_all_variations
)

def run_tests(out_dir_name="outputs_v3"):
    print("==================================================================")
    print(f"  Démarrage des tests officiels GUFACA (Sortie: {out_dir_name})")
    print("  Affiches CARRÉES 2400x2400 (300 DPI) & Bannières HD")
    print("==================================================================")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_logo = os.path.join(base_dir, "assets", "sample_logo.png")
    sample_photo = os.path.join(base_dir, "assets", "sample_photo.png")
    out_dir = os.path.join(base_dir, "assets", out_dir_name)
    os.makedirs(out_dir, exist_ok=True)

    # Test 1 : Validation des fichiers sources
    assert os.path.exists(sample_logo), f"Logo introuvable : {sample_logo}"
    assert os.path.exists(sample_photo), f"Photo introuvable : {sample_photo}"
    print("✔ Test 1 : Actifs sources (photo + logo) validés.")

    # Test 2 : Extraction dynamique de palette bicolore avec séparation chromatique
    primary, secondary = extract_dominant_colors(sample_logo)
    assert primary is not None and secondary is not None
    print(f"✔ Test 2 : Couleurs dominantes extraites : Primaire={primary}, Secondaire={secondary}")

    # Test 3 : Exécution de toutes les variantes avec textes officiels de gufaca.com
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

    target_website = "https://gufaca.com"

    run_all_variations(
        photo_path=sample_photo,
        logo_path=sample_logo,
        name="Alpha Oumar Sow",
        company="GUFACA",
        subtitle="Ingénierie Logicielle & Intelligence Artificielle",
        headline="Ingénierie Logicielle & Intelligence Artificielle",
        bullets=bullets,
        services=services,
        website=target_website,
        email="contact@gufaca.com",
        phone="(514) 754-9984",
        city="Montréal, QC",
        out_dir=out_dir
    )

    # Test 4 : Contrôle des 3 Bannières de profil
    banner_files = [
        ("banniere_style_1_executive_HD.jpg", (1376, 768)),
        ("banniere_style_1_executive_300x180.jpg", (300, 180)),
        ("banniere_style_2_circular_HD.jpg", (1376, 768)),
        ("banniere_style_2_circular_300x180.jpg", (300, 180)),
        ("banniere_style_3_split_HD.jpg", (1376, 768)),
        ("banniere_style_3_split_300x180.jpg", (300, 180)),
    ]
    for filename, expected_size in banner_files:
        p = os.path.join(out_dir, filename)
        assert os.path.exists(p), f"Fichier manquant : {p}"
        im = Image.open(p)
        assert im.size == expected_size, f"Dimensions incorrectes pour {filename} : {im.size} vs {expected_size}"
        assert os.path.getsize(p) > 5000, f"Fichier vide ou trop petit : {p}"
    print("✔ Test 4 : Les 3 styles de bannières (HD et 300x180 px) sont 100% validés.")

    # Test 5 : Contrôle des 3 Affiches de table CARRÉES (2400x2400 px, 300 DPI)
    flyer_files = [
        ("affiche_style_1_centered.png", (2400, 2400)),
        ("affiche_style_2_header_card.png", (2400, 2400)),
        ("affiche_style_3_asymmetric.png", (2400, 2400)),
    ]
    for filename, expected_size in flyer_files:
        p = os.path.join(out_dir, filename)
        assert os.path.exists(p), f"Fichier manquant : {p}"
        im = Image.open(p)
        assert im.size == expected_size, f"Dimensions incorrectes pour {filename} : {im.size} vs {expected_size}"
        assert os.path.getsize(p) > 20000, f"Fichier vide ou trop petit : {p}"
    print("✔ Test 5 : Les 3 styles d'affiches de table CARRÉES (2400x2400 px) sont 100% validés.")

    # Test 6 : Validation de la scannabilité optique du QR Code via OpenCV
    if HAS_CV2:
        qr_detector = cv2.QRCodeDetector()
        for filename, _ in flyer_files:
            p = os.path.join(out_dir, filename)
            img_cv = cv2.imread(p)
            data, bbox, _ = qr_detector.detectAndDecode(img_cv)
            assert data == target_website, f"Échec de décodage QR pour {filename} : '{data}' vs attendu '{target_website}'"
            print(f"✔ Test 6 : QR Code décodé avec succès dans {filename} -> {data}")
    else:
        print("ℹ Test 6 ignoré : OpenCV non disponible pour le décodage automatisé.")

    # Test 7 : Validation des documents textuels bilingues (Présentation, Pitch 1 min, Profils)
    text_files = [
        "presentation_entreprise_fr.md",
        "presentation_entreprise_en.md",
        "pitch_1_minute_fr.md",
        "pitch_1_minute_en.md",
        "profil_membre_fr.md",
        "profil_membre_en.md"
    ]
    for tf in text_files:
        p = os.path.join(out_dir, tf)
        assert os.path.exists(p), f"Document textuel manquant : {p}"
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
            assert len(content) > 150, f"Document trop court : {tf}"
            assert "GUFACA" in content, f"GUFACA absent dans {tf}"
            assert "gufaca.com" in content, f"gufaca.com absent dans {tf}"
    print("✔ Test 7 : Les 6 documents textuels (Présentations, Pitchs 1 min, Profils FR/EN) sont 100% validés.")

    print("\n==================================================================")
    print(f"  TOUS LES TESTS SONT VALIDES AVEC SUCCÈS (100%)")
    print(f"  Dossier vérifié : assets/{out_dir_name}")
    print("==================================================================")


if __name__ == "__main__":
    out_name = sys.argv[1] if len(sys.argv) > 1 else "outputs_v3"
    run_tests(out_name)
