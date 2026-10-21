#!/usr/bin/env python3
"""
Tests Unitaires — Kit d'Onboarding GUFACA
Valide les fonctions atomiques : palette, typographie, QR code et documents textuels bilingues.
"""

import os
import sys
import unittest
import tempfile
import shutil
from PIL import Image, ImageDraw

# Ajout du dossier parent au path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BASE_DIR)

from generate_member_assets import (
    extract_dominant_colors,
    fit_text_to_width,
    create_qr_code_image,
    make_circular_photo,
    generate_text_deliverables,
    get_system_font
)


class TestUnitAssets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_logo = os.path.join(BASE_DIR, "assets", "sample_logo.png")
        cls.sample_photo = os.path.join(BASE_DIR, "assets", "sample_photo.png")

    def test_01_assets_exist(self):
        """Vérifie la présence des fichiers sources de référence."""
        self.assertTrue(os.path.exists(self.sample_logo), "Le logo sample_logo.png doit exister.")
        self.assertTrue(os.path.exists(self.sample_photo), "La photo sample_photo.png doit exister.")

    def test_02_extract_dominant_colors(self):
        """Vérifie l'extraction des couleurs dominantes (primaire et secondaire)."""
        primary, secondary = extract_dominant_colors(self.sample_logo)
        self.assertIsInstance(primary, tuple)
        self.assertIsInstance(secondary, tuple)
        self.assertEqual(len(primary), 3)
        self.assertEqual(len(secondary), 3)
        for val in primary + secondary:
            self.assertTrue(0 <= val <= 255)

    def test_03_fit_text_to_width(self):
        """Vérifie que fit_text_to_width ajuste la taille pour respecter max_width."""
        im = Image.new("RGB", (1000, 200), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        text = "Ingénierie Logicielle & Intelligence Artificielle"
        max_w = 550
        font, final_size, w = fit_text_to_width(draw, text, initial_size=60, max_width=max_w, min_size=16)
        self.assertLessEqual(w, max_w)
        self.assertLess(final_size, 60)

    def test_04_create_qr_code_image(self):
        """Vérifie la génération d'un QR code PIL Image."""
        url = "https://gufaca.com"
        qr_img = create_qr_code_image(url, (15, 23, 42), size=400)
        self.assertIsInstance(qr_img, Image.Image)
        self.assertEqual(qr_img.size, (400, 400))
        self.assertEqual(qr_img.mode, "RGBA")

    def test_05_make_circular_photo(self):
        """Vérifie le découpage d'un portrait circulaire en mode RGBA."""
        base_im = Image.new("RGB", (300, 300), (100, 150, 200))
        circ_im = make_circular_photo(base_im, diameter=150)
        self.assertEqual(circ_im.size, (150, 150))
        self.assertEqual(circ_im.mode, "RGBA")


class TestUnitTextDeliverables(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_06_generate_text_deliverables(self):
        """Vérifie la génération des 6 fichiers markdown de présentation et pitchs."""
        name = "Alpha Oumar Sow"
        company = "GUFACA"
        subtitle = "Ingénierie Logicielle & Intelligence Artificielle"
        website = "https://gufaca.com"
        email = "contact@gufaca.com"
        phone = "(514) 754-9984"
        city = "Montréal, QC"

        generate_text_deliverables(
            name=name,
            company=company,
            subtitle=subtitle,
            website=website,
            email=email,
            phone=phone,
            city=city,
            out_dir=self.temp_dir
        )

        expected_files = [
            "presentation_entreprise_fr.md",
            "presentation_entreprise_en.md",
            "pitch_1_minute_fr.md",
            "pitch_1_minute_en.md",
            "profil_membre_fr.md",
            "profil_membre_en.md"
        ]

        for fname in expected_files:
            file_path = os.path.join(self.temp_dir, fname)
            self.assertTrue(os.path.exists(file_path), f"Le fichier {fname} doit être créé.")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn(company, content, f"{company} doit figurer dans {fname}")
                self.assertIn(website, content, f"{website} doit figurer dans {fname}")
                self.assertGreater(len(content), 100, f"Le fichier {fname} doit être substantiel.")


if __name__ == "__main__":
    unittest.main()
