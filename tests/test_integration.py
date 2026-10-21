#!/usr/bin/env python3
"""
Tests d'Intégration — Kit d'Onboarding GUFACA
Valide le pipeline complet de bout en bout (End-to-End) :
- Génération des 3 styles de bannières HD (1376x768) et miniatures (300x180)
- Génération des 3 styles d'affiches de table CARRÉES (2400x2400, 300 DPI)
- Génération des 6 documents textuels (Présentations, Pitchs 1 min, Profils bilingues)
- Décodage optique des QR codes générés avec OpenCV
"""

import os
import sys
import unittest
import tempfile
import shutil
from PIL import Image

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BASE_DIR)

from generate_member_assets import run_all_variations

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False


class TestIntegrationEndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.sample_logo = os.path.join(BASE_DIR, "assets", "sample_logo.png")
        cls.sample_photo = os.path.join(BASE_DIR, "assets", "sample_photo.png")
        cls.website = "https://gufaca.com"

        services = [
            "Intelligence Artificielle & Automatisation 24/7",
            "Sites Web & Applications Mobiles sur-mesure",
            "Référencement SEO & GEO (Google & Moteurs IA)",
            "Direction Technique (CTO Externe) & Formations"
        ]
        bullets = [
            "Agents IA 24/7 & Automatisation documentaire",
            "Applications Web & Mobiles sur-mesure (Next.js/React)",
            "SEO & GEO : Être cité par ChatGPT, Perplexity & Google"
        ]

        # Exécution du pipeline complet
        run_all_variations(
            photo_path=cls.sample_photo,
            logo_path=cls.sample_logo,
            name="Alpha Oumar Sow",
            company="GUFACA",
            subtitle="Ingénierie Logicielle & Intelligence Artificielle",
            headline="Ingénierie Logicielle & Intelligence Artificielle",
            bullets=bullets,
            services=services,
            website=cls.website,
            email="contact@gufaca.com",
            phone="(514) 754-9984",
            city="Montréal, QC",
            out_dir=cls.temp_dir
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_01_banners_dimensions_and_files(self):
        """Vérifie la présence et les dimensions exactes des 3 styles de bannières HD et miniatures."""
        banner_styles = [
            ("banniere_style_1_executive_HD.jpg", "banniere_style_1_executive_300x180.jpg"),
            ("banniere_style_2_circular_HD.jpg", "banniere_style_2_circular_300x180.jpg"),
            ("banniere_style_3_split_HD.jpg", "banniere_style_3_split_300x180.jpg")
        ]

        for hd_name, thumb_name in banner_styles:
            hd_path = os.path.join(self.temp_dir, hd_name)
            thumb_path = os.path.join(self.temp_dir, thumb_name)

            self.assertTrue(os.path.exists(hd_path), f"Fichier HD manquant : {hd_name}")
            self.assertTrue(os.path.exists(thumb_path), f"Miniature manquante : {thumb_name}")

            with Image.open(hd_path) as im:
                self.assertEqual(im.size, (1376, 768), f"Dimension HD incorrecte pour {hd_name}")

            with Image.open(thumb_path) as im:
                self.assertEqual(im.size, (300, 180), f"Dimension miniature incorrecte pour {thumb_name}")

    def test_02_square_flyers_dimensions_and_files(self):
        """Vérifie la présence et les dimensions carrées exactes (2400x2400) des 3 styles d'affiches."""
        flyer_styles = [
            ("affiche_style_1_centered.png", "affiche_style_1_centered.jpg"),
            ("affiche_style_2_header_card.png", "affiche_style_2_header_card.jpg"),
            ("affiche_style_3_asymmetric.png", "affiche_style_3_asymmetric.jpg")
        ]

        for png_name, jpg_name in flyer_styles:
            png_path = os.path.join(self.temp_dir, png_name)
            jpg_path = os.path.join(self.temp_dir, jpg_name)

            self.assertTrue(os.path.exists(png_path), f"Fichier PNG manquant : {png_name}")
            self.assertTrue(os.path.exists(jpg_path), f"Fichier JPG manquant : {jpg_name}")

            with Image.open(png_path) as im:
                self.assertEqual(im.size, (2400, 2400), f"Dimension carrée incorrecte pour {png_name}")

            with Image.open(jpg_path) as im:
                self.assertEqual(im.size, (2400, 2400), f"Dimension carrée incorrecte pour {jpg_name}")

    def test_03_text_deliverables_created(self):
        """Vérifie que les 6 documents textuels bilingues sont créés et non vides."""
        text_files = [
            "presentation_entreprise_fr.md",
            "presentation_entreprise_en.md",
            "pitch_1_minute_fr.md",
            "pitch_1_minute_en.md",
            "profil_membre_fr.md",
            "profil_membre_en.md"
        ]

        for tf in text_files:
            path = os.path.join(self.temp_dir, tf)
            self.assertTrue(os.path.exists(path), f"Document textuel manquant : {tf}")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertGreater(len(content), 200, f"Le document {tf} semble trop court")
                self.assertIn("GUFACA", content)
                self.assertIn("gufaca.com", content)

    def test_04_optical_qr_decoding(self):
        """Vérifie que le QR code intégré sur chaque affiche se décode optiquement vers l'URL officielle."""
        if not OPENCV_AVAILABLE:
            self.skipTest("OpenCV non installé — test de décodage optique ignoré")

        detector = cv2.QRCodeDetector()
        flyers = [
            "affiche_style_1_centered.png",
            "affiche_style_2_header_card.png",
            "affiche_style_3_asymmetric.png"
        ]

        for fname in flyers:
            fpath = os.path.join(self.temp_dir, fname)
            img = cv2.imread(fpath)
            self.assertIsNotNone(img, f"Échec de lecture de l'image OpenCV : {fname}")
            data, bbox, _ = detector.detectAndDecode(img)
            self.assertEqual(
                data,
                self.website,
                f"Le QR Code dans {fname} a décodé '{data}' au lieu de '{self.website}'"
            )


if __name__ == "__main__":
    unittest.main()
