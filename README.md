# Projet FFVB Scraper

Ce projet permet d'extraire et de traiter les données de la Fédération Française de Volley-Ball (FFVB) en utilisant Scrapy et des techniques d'OCR.

## Structure du projet

```
Projet_scraping/
├── .venv/                          # Environnement virtuel Python
├── ffvb_scraper/                   # Dossier principal du projet Scrapy
│   ├── .scrapy/                    # Cache Scrapy
│   ├── ffvb_scraper/              # Package principal
│   │   ├── spiders/               # Spiders Scrapy
│   │   │   ├── __init__.py
│   │   │   ├── ffvb_working_spider.py
│   │   │   └── resultat_spider.py
│   │   ├── __init__.py
│   │   ├── middlewares.py         # Middlewares Scrapy
│   │   ├── pipelines.py           # Pipelines de traitement
│   │   └── settings.py            # Configuration Scrapy
│   ├── check_and_run_scraper.py   # Script de vérification et lancement
│   ├── clean_duplicates.py        # Script de nettoyage des doublons
│   ├── final_ocr_extractor.py     # Extracteur OCR final
│   ├── ffvb_players_complete.csv  # Données des joueurs
│   ├── requirements.txt           # Dépendances Python
│   └── scrapy.cfg                 # Configuration Scrapy
└── README.md                       # Ce fichier
```

## 🚀 Installation

### Prérequis
- Python 3.7+
- pip

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone https://github.com/emiliedelrue/Projet_scraping.git
cd Projet_scraping
```

2. **Créer et activer l'environnement virtuel**
```bash
python -m venv .venv

# Sur Windows
.venv\Scripts\activate

# Sur Linux/Mac
source .venv/bin/activate
```

3. **Installer les dépendances**
```bash
cd ffvb_scraper
pip install -r requirements.txt
```

## Utilisation

### Extraction des données avec les spiders Scrapy

Pour extraire les différents types de données FFVB, utilisez les commandes suivantes dans le dossier `ffvb_scraper/` :

```bash
# Champions nationaux
scrapy crawl ffvb_champions

# Champions de France
scrapy crawl ffvb_champions_France

# Champions de France Fédéral
scrapy crawl ffvb_champions_France_Federal

# Champions de France Beach Volley
scrapy crawl ffvb_champions_France_beach_volley

# Résultats tous championnats confondus
scrapy crawl ffvb_resultats
```

### Traitement des données avec OCR

Pour obtenir le fichier de sortie final sur les joueurs hommes avec extraction OCR, suivez cette séquence **dans l'ordre** :

1. **Vérification et lancement du scraper**
```bash
python check_and_run_scraper.py
```

2. **Nettoyage des doublons**
```bash
python clean_duplicates.py
```

3. **Extraction OCR finale**
```bash
python final_ocr_extractor.py
```

**Important** : Respectez cet ordre d'exécution pour obtenir des résultats corrects.

## Fichiers de sortie

- **CSV des spiders** : Les commandes `scrapy crawl` génèrent des fichiers CSV avec les données extraites
- **ffvb_players_complete.csv** : Données complètes des joueurs après traitement
- **Fichier OCR final** : Généré par `final_ocr_extractor.py` après la séquence complète

## Configuration

- **settings.py** : Configuration principale de Scrapy (délais, user-agent, etc.)
- **pipelines.py** : Pipelines de traitement des données extraites
- **middlewares.py** : Middlewares pour le traitement des requêtes/réponses

## Scripts utilitaires

- **check_and_run_scraper.py** : Vérifie l'environnement et lance le scraping
- **clean_duplicates.py** : Supprime les entrées dupliquées dans les données
- **final_ocr_extractor.py** : Applique l'OCR pour extraire du texte depuis les images

