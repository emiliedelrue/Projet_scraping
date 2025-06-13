# pipelines.py
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
# pipelines.py - Version alternative
# pipelines.py
from itemadapter import ItemAdapter
import csv
import re
import os
import requests
from urllib.parse import unquote
import pytesseract
from PIL import Image
from io import BytesIO

class CSVVolleyPipeline:
    def open_spider(self, spider):
        self.file = open('joueurs_ffvb.csv', 'w', newline='', encoding='utf-8')
        self.fieldnames = [
            'nom', 
            'prenom', 
            'poste', 
            'age', 
            'taille', 
            'poids', 
            'club', 
            'ville_naissance',
            'photo_url',
            'biographie'
        ]
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()
        print(f"Fichier CSV sauvegardé : joueurs_ffvb.csv")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Filtrer les pages qui ne sont pas des joueurs
        nom = adapter.get('nom', '').lower()
        if any(word in nom for word in ['journées', 'sélections', 'pôles', 'staff', 'de ']):
            spider.logger.info(f"Page ignorée (pas un joueur): {adapter.get('nom')} {adapter.get('prenom')}")
            return None
        
        # Nettoyer les données
        for field in ['nom', 'prenom', 'poste', 'club', 'ville_naissance']:
            if adapter.get(field):
                adapter[field] = str(adapter[field]).strip()
        
        # Nettoyer la biographie (enlever les retours à la ligne)
        if adapter.get('biographie'):
            bio = str(adapter['biographie'])
            bio = re.sub(r'\s+', ' ', bio)  # Normaliser les espaces
            bio = bio.replace('\n', ' ').replace('\r', '')  # Enlever les retours à la ligne
            adapter['biographie'] = bio.strip()
        
        # Créer un dictionnaire avec seulement les champs voulus
        filtered_item = {field: adapter.get(field, '') for field in self.fieldnames}
        
        self.writer.writerow(filtered_item)
        return item

class PDFVolleyPipeline:
    """Pipeline pour télécharger les images des CV"""
    
    def __init__(self):
        self.images_dir = "images_joueurs"
        os.makedirs(self.images_dir, exist_ok=True)
    
    def process_item(self, item, spider):
        if item.get('photo_url'):
            # Télécharger l'image du CV
            self.download_image(item['photo_url'], item['nom'], item['prenom'])
        
        return item
    
    def download_image(self, url, nom, prenom):
        try:
            # Décoder l'URL (pour les caractères spéciaux)
            clean_url = unquote(url)
            
            # Créer un nom de fichier propre
            clean_nom = "".join(c for c in nom if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_prenom = "".join(c for c in prenom if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{clean_nom}_{clean_prenom}.png"
            filepath = os.path.join(self.images_dir, filename)
            
            # Télécharger l'image
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Image téléchargée: {filename}")
            
        except Exception as e:
            print(f"❌ Erreur téléchargement {nom} {prenom}: {e}")

class OCRVolleyPipeline:
    """Pipeline pour extraire les données depuis les images CV"""
    
    def process_item(self, item, spider):
        if item.get('photo_url'):
            # Extraire les données depuis l'image
            extracted_data = self.extract_data_from_cv(item['photo_url'], item['nom'], item['prenom'])
            
            # Mettre à jour l'item avec les données extraites
            if extracted_data:
                item.update(extracted_data)
                spider.logger.info(f"Données extraites pour {item['nom']} {item['prenom']}: {extracted_data}")
        
        return item
    
    def extract_data_from_cv(self, url, nom, prenom):
        """Extraire les informations depuis l'image du CV"""
        try:
            # Télécharger l'image
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Ouvrir l'image avec PIL
            image = Image.open(BytesIO(response.content))
            
            # Améliorer l'image pour l'OCR
            image = image.convert('RGB')
            
            # Extraire le texte avec Tesseract
            text = pytesseract.image_to_string(image, lang='fra')
            
            # Parser le texte pour extraire les informations
            return self.parse_cv_text(text, nom, prenom)
            
        except Exception as e:
            print(f"❌ Erreur OCR pour {nom} {prenom}: {e}")
            return {}
    
    def parse_cv_text(self, text, nom, prenom):
        """Parser le texte extrait pour récupérer les informations structurées"""
        data = {}
        
        # Nettoyer le texte (enlever les caractères parasites)
        text = re.sub(r'\n+', ' ', text)  # Remplacer les retours à la ligne par des espaces
        text = re.sub(r'\s+', ' ', text)  # Normaliser les espaces multiples
        
        # Debug : afficher le texte nettoyé
        print(f"\n=== TEXTE NETTOYÉ POUR {nom} {prenom} ===")
        print(text[:500] + "..." if len(text) > 500 else text)
        print("=" * 50)
        
        # Extraire l'âge avec plusieurs méthodes
        age_patterns = [
            r'NAISSANCE\s+(\d{2}/\d{2}/\d{4})',
            r'(\d{2}/\d{2}/\d{4})',
            r'NAISSANCE.*?(\d{4})',
            r'(\d{4})\s+(?:Grenoble|Paris|Lyon|Marseille|Bordeaux|Toulouse|Nantes)'
        ]
        
        for pattern in age_patterns:
            match = re.search(pattern, text)
            if match:
                if '/' in match.group(1):
                    annee = int(match.group(1).split('/')[2])
                else:
                    annee = int(match.group(1))
                if 1980 <= annee <= 2005:  # Années plausibles
                    data['age'] = str(2025 - annee)
                    break
        
        # Extraire la taille
        taille_match = re.search(r'TAILLE\s+(\d{3})\s*cm', text)
        if taille_match:
            data['taille'] = taille_match.group(1) + ' cm'
        
        # Extraire le poids
        poids_match = re.search(r'POIDS\s+(\d{2,3})\s*kg', text)
        if poids_match:
            data['poids'] = poids_match.group(1) + ' kg'
        
        # Extraire le poste
        poste_patterns = [
            r'(CENTRAL)',
            r'(LIBERO|LIBÉRO)',
            r'(PASSEUR)',
            r'(RÉCEPTIONNEUR|RECEPTIONNEUR)',
            r'(ATTAQUANT)',
            r'(POINTU)'
        ]
        
        for pattern in poste_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['poste'] = match.group(1).replace('É', 'é').title()
                break
        
        # Extraire la ville de naissance (corrigé)
        ville_patterns = [
            r'NAISSANCE\s+\d{2}/\d{2}/\d{4}\s+([A-Za-zÀ-ÿ\s-]+?)\s*$ ',            r'Originaire de ([A-Za-zÀ-ÿ\s-]+),',            r'([A-Za-zÀ-ÿ]+)\s+\(\d{2} $ ',
            r'débute sa carrière à.*?([A-Za-zÀ-ÿ]+)'
        ]
        
        for pattern in ville_patterns:
            match = re.search(pattern, text)
            if match:
                ville = match.group(1).strip()
                # Filtrer les mots parasites
                mots_parasites = ['TAILLE', 'POIDS', 'NAISSANCE', 'HAUTEUR', 'BLOCK', 'ATTAQUE', 'France', 'FRANCE']
                if ville not in mots_parasites and len(ville) > 2:
                    data['ville_naissance'] = ville
                    break
        
        # Extraire le club actuel
        club_patterns = [
            r'2024\s*[—-]\s*([A-Za-zÀ-ÿ\s]+?)(?:\s+2023|\s+2022|\s+$)',
            r'2023\s*[—-]\s*2024\s*([A-Za-zÀ-ÿ\s]+\w+)',
            r'([\w\s]+(?:Volley|VB|Volleyball)[\w\s]*)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+\s+VB)'
        ]
        
        for pattern in club_patterns:
            match = re.search(pattern, text)
            if match:
                club = match.group(1).strip()
                club = re.sub(r'\s+', ' ', club)
                
                # Filtrer les faux clubs
                faux_clubs = ['CNVB', 'FIVB', 'Médaille de bronze Volley', 'Francevolley', 'Vainqueur']
                if club not in faux_clubs and len(club) > 3:
                    data['club'] = club
                    break
        
        # Extraire une biographie propre
        bio_patterns = [
            r'Originaire de [^.]+\.',
            r'[^.]*débute sa carrière[^.]*\.',
            r'[^.]*équipe de France[^.]*\.',
            r'[^.]*expérience[^.]*\.'
        ]
        
        for pattern in bio_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                bio = match.group(0).strip()
                bio = re.sub(r'\s+', ' ', bio)
                if 20 <= len(bio) <= 200:
                    data['biographie'] = bio
                    break
        
        return data
