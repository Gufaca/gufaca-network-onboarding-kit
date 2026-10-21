# 🚀 GUFACA — Kit d'Onboarding Réseau GR International

> **Générateur Multi-Styles d'Actifs Visuels Haute Définition & Profils Bilingues pour Membres de Réseaux d'Affaires**  
> *Conçu et propulsé par GUFACA ([gufaca.com](https://gufaca.com)) — Alpha Oumar Sow*

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-1E824C.svg)](https://www.python.org/downloads/)
[![Network: GR International](https://img.shields.io/badge/Réseau-GR%20International-D97706.svg)](https://www.grinternational.ca/)
[![Design: Agency Grade](https://img.shields.io/badge/Design-Agency--Grade-0F172A.svg)]()
[![Status: Production Ready](https://img.shields.io/badge/Statut-Production--Ready-22C55E.svg)]()
[![License: MIT](https://img.shields.io/badge/Licence-MIT-blue.svg)](LICENSE)

---

## 📋 Contexte : Optimisé pour GR International

Ce dépôt contient l'infrastructure logicielle et la compétence d'agent IA conçues pour propulser la visibilité des membres du réseau d'affaires **GR International** (ainsi que tout club d'entrepreneurs ou chambre de commerce).

Il permet à tout nouveau membre ou dirigeant de générer en quelques secondes un **kit de visibilité 360° complet** :
* 3 variantes graphiques d'affiches de table avec logo et QR code pour les déjeuners et rencontres d'affaires.
* 3 variantes graphiques de bannières de profil en haute définition (16:9) et au format miniature officiel de l'annuaire GR (300×180 px).
* Des profils d'annuaire bilingues (français et anglais) rédigés sur un ton humain, direct et sans jargon.
* Des formules de pitchs oraux percutants (pitch éclair 30s, pitch 60s, demande de recommandation ciblée).

---

## 🎨 Les Actifs Visuels Produits (Qualité Studio Graphique)

Le moteur extrait automatiquement la palette chromatique bicolore du logo du membre (couleur primaire et accent chaud/complémentaire) et applique un rendu d'agence : cartes avec ombres portées ambiantes (*ambient occlusion*), badges circulaires avec coches blanches `✓`, encarts de scan interactifs et rubans d'adhésion officiels.

### 1. 🖼️ 3 Styles de Bannières de Profil (16:9 HD 1376×768 & Miniature 300×180 px)

| Style | Nom | Description & Esthétique | Usage Recommandé |
| :--- | :--- | :--- | :--- |
| **Style 1** | **Executive Classic** | Fond sombre prestige (`#0B1124`), halo lumineux bicolore, photo portrait détourée à gauche (ratio 3:5), capsule logo blanche et typographie nette sans débordement. | Annuaire GR International, LinkedIn, En-têtes de proposition |
| **Style 2** | **Modern Circular** | Médaillon circulaire avec double anneau dynamique aux couleurs de marque, logo contrasté et puces stylisées. | Présentations d'équipe, signatures courriel, profils conférencier |
| **Style 3** | **Split Pro Contrast** | Découpage vertical asymétrique (35% portrait à gauche avec liseré bicolore, 65% contenu à droite sur fond ultra sombre). | Affichage mobile, bannières d'annuaires compacts |

#### Aperçu Visuel des 3 Styles de Bannières :

##### Style 1 — Executive Classic (16:9 HD) :
![Bannière Style 1 Executive Classic](assets/examples/banniere_style_1_executive_HD.jpg)

##### Style 2 — Modern Circular (16:9 HD) :
![Bannière Style 2 Modern Circular](assets/examples/banniere_style_2_circular_HD.jpg)

##### Style 3 — Split Pro Contrast (16:9 HD) :
![Bannière Style 3 Split Pro](assets/examples/banniere_style_3_split_HD.jpg)

---

### 2. 📄 3 Styles d'Affiches de Table au Format CARRÉ (2400×2400 px, 300 DPI)

Conçues spécialement au **format carré 1:1** haute définition (300 DPI), avec distribution aérée sur deux colonnes, barre de réassurance à 3 piliers (Livrable 14j, Loi 25 & RGPD, 10+ ans d'expérience) et grand QR Code scannable à distance :

| Style | Nom | Caractéristiques Visuelles & Contenu | Point Fort |
| :--- | :--- | :--- | :--- |
| **Style 1** | **Square Prestige Centered** *(Modèle Holistik Carré)* | Format carré 2400×2400, logo centré en majesté, sous-titre officiel, 4 modules de services complets (titre + description concrète + badge d'impact), encart QR code avec Call to Action et pied de page dark slate. | Équilibre parfait, clarté et prestige institutionnel épuré |
| **Style 2** | **Square Modern Dual-Block** | Grand bandeau supérieur bleu nuit (`#0F172A`) avec logo en boîte blanche en relief, 4 cartes d'expertises ergonomiques avec puces d'impact et grand module QR Code interactif. | Impact visuel fort, look moderne orienté tech et conseil |
| **Style 3** | **Square Bold Impact** *(Modèle Mamie Carré)* | Typographie extra large pour une lisibilité optimale à 3 mètres de distance, grand slogan de croissance, médaillons circulaires pleins et QR Code XXL. | Visibilité maximale à travers la salle lors du tour de table |

#### Aperçu Visuel des 3 Styles d'Affiches Carrées :

<div align="center">

##### Style 1 — Square Prestige Centered (2400×2400 px, 300 DPI)
<img src="assets/examples/affiche_style_1_centered.jpg" alt="Affiche Carrée Style 1 Prestige Centered" width="600"/>

##### Style 2 — Square Modern Dual-Block (2400×2400 px, 300 DPI)
<img src="assets/examples/affiche_style_2_header_card.jpg" alt="Affiche Carrée Style 2 Modern Dual-Block" width="600"/>

##### Style 3 — Square Bold Impact (2400×2400 px, 300 DPI)
<img src="assets/examples/affiche_style_3_asymmetric.jpg" alt="Affiche Carrée Style 3 Bold Impact" width="600"/>

</div>

---

## 🛠️ Guide d'Installation Pas-à-Pas

### 1. Prérequis Système
* **Python 3.9** ou supérieur installé ([python.org](https://www.python.org/downloads/)).
* Git installé sur votre poste.

### 2. Cloner le Dépôt
```bash
git clone https://github.com/Gufaca/gufaca-network-onboarding-kit.git
cd gufaca-network-onboarding-kit
```

### 3. Créer et Activer un Environnement Virtuel (Recommandé)

**Sur macOS et Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Sur Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Installer les Dépendances
```bash
pip install -r requirements.txt
```

*(Optionnel pour les tests automatisés de décodage optique : `pip install opencv-python`)*

---

## 🧪 Comment Tester le Projet Immédiatement

Le projet intègre une suite de validation automatisée qui teste l'extraction de palette, génère l'ensemble des 6 fichiers et vérifie la scannabilité optique des QR codes :

```bash
python3 test_kit.py
```

**Sortie attendue :**
```text
==================================================================
  Démarrage des tests multi-styles GUFACA × GR International
==================================================================
✔ Test 1 : Actifs sources (photo + logo) validés.
✔ Test 2 : Couleurs dominantes extraites : Primaire=(78, 147, 91), Secondaire=(251, 176, 64)

=======================================================
  GÉNÉRATION COMPLÈTE GUFACA × GR INTERNATIONAL
  3 Variantes de Bannières + 3 Variantes d'Affiches
=======================================================

✔ Bannière Style 1 (Executive Classic) générée : .../banniere_style_1_executive_HD.jpg
✔ Bannière Style 2 (Modern Circular) générée : .../banniere_style_2_circular_HD.jpg
✔ Bannière Style 3 (Split Pro) générée : .../banniere_style_3_split_HD.jpg
✔ Affiche Style 1 (Classic Centered) générée : .../affiche_style_1_centered.png
✔ Affiche Style 2 (Header Card) générée : .../affiche_style_2_header_card.png
✔ Affiche Style 3 (Asymmetric Bold) générée : .../affiche_style_3_asymmetric.png

✔ Test 4 : Les 3 styles de bannières (HD et 300x180 px) sont 100% validés.
✔ Test 5 : Les 3 styles d'affiches de table CARRÉES (2400x2400 px) sont 100% validés.
✔ Test 6 : QR Code décodé avec succès dans affiche_style_1_centered.png -> https://gufaca.com
✔ Test 6 : QR Code décodé avec succès dans affiche_style_2_header_card.png -> https://gufaca.com
✔ Test 6 : QR Code décodé avec succès dans affiche_style_3_asymmetric.png -> https://gufaca.com

==================================================================
  TOUS LES TESTS MULTI-STYLES SONT VALIDES AVEC SUCCÈS (100%)
==================================================================
```

Les images produites se trouvent dans `assets/outputs/`.

---

## 🚀 Guide d'Utilisation : Générer Vos Propres Actifs

### Mode Démonstration Rapide
Génère tous les visuels avec les éléments graphiques et coordonnées par défaut de GUFACA :
```bash
python3 generate_member_assets.py --demo
```

### Personnalisation Complète pour un Membre ou une Entreprise
Vous pouvez passer l'ensemble de vos paramètres en ligne de commande :

```bash
python3 generate_member_assets.py \
  --name "Jean-François Tremblay" \
  --company "Tremblay Solutions" \
  --subtitle "Comptabilité Stratégique & Conseil PME" \
  --headline "Optimisation Fiscale & Conseil PME" \
  --website "https://gufaca.com" \
  --email "jf@tremblaysolutions.ca" \
  --phone "(514) 555-0199" \
  --city "Montréal, QC" \
  --network "GR INTERNATIONAL" \
  --logo "chemin/vers/mon_logo.png" \
  --photo "chemin/vers/ma_photo.png" \
  --out-dir "mes_visuels"
```

### Tableau des Options CLI

| Paramètre | Description | Valeur par défaut |
| :--- | :--- | :--- |
| `--name` | Nom complet du dirigeant ou représentant | `Alpha Oumar Sow` |
| `--company` | Nom de l'entreprise ou marque | `GUFACA` |
| `--subtitle` | Spécialité ou sous-titre officiel | `Ingénierie Technologique & Intelligence Artificielle` |
| `--headline` | Accroche concise pour les bannières | `Ingénierie Technologique & IA` |
| `--website` | URL officielle vers laquelle pointe le QR Code | `https://gufaca.com` |
| `--email` | Courriel professionnel affiché en pied de page | `alpha@gufaca.com` |
| `--phone` | Numéro de téléphone direct | `(514) 754-9984` |
| `--city` | Ville et province d'opération | `Montréal, QC` |
| `--network` | Nom du réseau d'affaires partenaire | `GR INTERNATIONAL` |
| `--logo` | Chemin vers le logo haute résolution (PNG transparent recommandé) | `assets/sample_logo.png` |
| `--photo` | Chemin vers la photo portrait professionnelle | `assets/sample_photo.png` |
| `--out-dir` | Dossier de sortie des fichiers générés | `assets/outputs/` |

---

## 🖨️ Conseils d'Impression & d'Affichage

1. **Affiches de table au format CARRÉ (Chevalets 2400×2400 px, 300 DPI) :**
   * Format carré 1:1 optimisé pour tirage photo 8×8 pouces ou 20×20 cm en haute définition.
   * Imprimer sur papier couché mat ou semi-brillant (minimum 200 g/m²).
   * Insérer dans un cadre ou présentoir de table carré en acrylique transparent (chevalet en T ou en L).
2. **Miniatures Annuaire (300×180 px) :**
   * Dimension exacte exigée par la plateforme d'annuaire des membres de GR International.
3. **Bannières 16:9 HD (1376×768 px) :**
   * Parfaites pour LinkedIn, signatures HTML, fiches de présentation client et diapositives.

---

## 🌐 Membres Sans Site Web : Accompagnement GUFACA

Pour les nouveaux membres ne disposant pas encore d'un site internet moderne ou dont le site actuel n'est pas optimisé mobile :
* Ils bénéficient d'un **tarif préférentiel exclusif** auprès de **GUFACA** ([gufaca.com](https://gufaca.com)) pour la conception de leur vitrine moderne, portail métier ou application mobile.
* En attendant la mise en ligne, le QR code de leurs affiches peut être directement relié à leur profil professionnel LinkedIn ou à leur fiche contact vCard.

---

## 📁 Architecture du Dépôt

```text
gufaca-network-onboarding-kit/
├── README.md                      # Documentation complète (Installation, Usage, Architecture)
├── SKILL.md                       # Spécification de la compétence Antigravity AI Agent
├── requirements.txt               # Dépendances Python (pillow, qrcode)
├── .gitignore                     # Fichiers exclus du suivi git
├── generate_member_assets.py      # Moteur graphique multi-styles (PIL)
├── test_kit.py                    # Suite unitaire automatisée avec validation optique QR
├── templates/
│   ├── profile_template_fr.md     # Modèle de profil d'annuaire en français
│   ├── profile_template_en.md     # Modèle de profil d'annuaire en anglais
│   └── pitch_templates.md         # Pitchs oraux 30s, 60s et demandes de recommandations
└── assets/
    ├── sample_logo.png            # Logo de démonstration GUFACA
    ├── sample_photo.png           # Photo de démonstration du dirigeant
    └── outputs/                   # Les 6 actifs générés (3 bannières + 3 affiches)
```

---

## 🆘 Support Direct & Assistance Personnalisée

Pour toute assistance technique, adaptation de gabarits ou intégration sur-mesure dans votre écosystème d'entreprise :

* 👤 **Alpha Oumar Sow** — Fondateur & Ingénieur IA, GUFACA
* 📞 Téléphone : **(514) 754-9984**
* ✉️ Courriel : **alpha@gufaca.com**
* 📍 Bureau : **Montréal (Québec), Canada**
* 🌐 Site web officiel : **[gufaca.com](https://gufaca.com)**

---

## 📄 Licence
Ce projet est distribué sous licence libre **MIT**. Vous êtes libre de l'utiliser, l'adapter et le redistribuer pour vos membres et vos projets clients.
