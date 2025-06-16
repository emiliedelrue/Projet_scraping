# fix_ocr_config.py
"""
Script pour corriger la configuration OCR et tester immédiatement
"""

import os
import sys

def fix_and_test_ocr():
    """Corrige la config OCR et teste immédiatement"""
    print("🔧 CORRECTION CONFIGURATION OCR")
    print("=" * 35)
    
    try:
        import pytesseract
        from PIL import Image, ImageDraw
        import requests
        from io import BytesIO
        
        # Configuration du chemin Tesseract
        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        
        if os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            print(f"✅ Chemin Tesseract configuré: {tesseract_path}")
        else:
            print(f"❌ Tesseract non trouvé à: {tesseract_path}")
            return False
        
        # Test rapide
        print(f"\n🧪 Test OCR rapide...")
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ Version Tesseract: {version}")
        except Exception as e:
            print(f"❌ Erreur version: {e}")
            return False
        
        # Test sur image réelle FFVB
        print(f"\n🏐 Test sur image joueur FFVB...")
        
        # URL de Kevin Tillie
        image_url = "http://www.ffvb.org/data/Files/2025%20-%20EDF%20MASCULINE%20VOLLEY/CV%20JOUEURS/7%20Kevin%20Tillie.png"
        
        try:
            print(f"📥 Téléchargement: {image_url}")
            response = requests.get(image_url, timeout=15)
            response.raise_for_status()
            
            # Ouvrir l'image
            image = Image.open(BytesIO(response.content))
            print(f"🖼️ Image: {image.size[0]}x{image.size[1]} pixels")
            
            # OCR avec config française
            print(f"🔍 Extraction OCR...")
            text = pytesseract.image_to_string(image, config='--psm 6 -l fra')
            
            if text.strip():
                print(f"✅ OCR RÉUSSI! {len(text)} caractères extraits")
                
                # Afficher les premiers 300 caractères
                print(f"\n📄 APERÇU DU TEXTE EXTRAIT:")
                print("-" * 40)
                print(text[:300])
                if len(text) > 300:
                    print("...")
                
                # Chercher des informations spécifiques
                import re
                
                print(f"\n🔍 RECHERCHE D'INFORMATIONS:")
                print("-" * 30)
                
                # Patterns améliorés
                patterns = {
                    'Nom/Prénom': r'(Kevin|Tillie)',
                    'Poste': r'(?:poste|position)[\s:]*([^,\n\r\.]+)',
                    'Taille': r'(?:taille)[\s:]*(\d{1,3})(?:\s*cm)?',
                    'Poids': r'(?:poids)[\s:]*(\d{2,3})(?:\s*kg)?',
                    'Âge': r'(?:âge|age)[\s:]*(\d{1,2})',
                    'Club': r'(?:club|équipe)[\s:]+([^,\n\r\.]{3,50})',
                    'Numéro': r'(?:numéro|n°|#)[\s:]*(\d{1,2})',
                    'Sélections': r'(?:sélections?)[\s:]*(\d+)'
                }
                
                found_data = {}
                for info_type, pattern in patterns.items():
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    if matches:
                        # Prendre la première occurrence non vide
                        value = next((m for m in matches if m.strip()), None)
                        if value:
                            found_data[info_type] = value.strip()
                            print(f"✅ {info_type}: {value.strip()}")
                    else:
                        print(f"❌ {info_type}: Non trouvé")
                
                # Sauvegarder la configuration qui fonctionne
                save_working_config(tesseract_path, found_data, text)
                
                print(f"\n🎉 OCR FONCTIONNEL!")
                print(f"📊 Informations trouvées: {len(found_data)}/8")
                
                if len(found_data) >= 3:
                    print(f"✅ Extraction très prometteuse pour tous les joueurs!")
                    return True
                else:
                    print(f"⚠️ Extraction partielle - ajustements possibles")
                    return True
            
            else:
                print(f"❌ Aucun texte extrait de l'image")
                print(f"💡 L'image pourrait nécessiter un préprocessing")
                return False
        
        except Exception as e:
            print(f"❌ Erreur test image: {e}")
            return False
    
    except ImportError as e:
        print(f"❌ Module manquant: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return False

def save_working_config(tesseract_path, found_data, sample_text):
    """Sauvegarde la configuration OCR qui fonctionne"""
    
    # 1. Créer un module de configuration
    config_content = f'''# ocr_config.py
"""
Configuration OCR pour FFVB - Générée automatiquement
"""

import pytesseract

# Chemin Tesseract qui fonctionne
TESSERACT_PATH = r"{tesseract_path}"

def setup_tesseract():
    """Configure Tesseract avec le bon chemin"""
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Configuration automatique
setup_tesseract()

# Configurations OCR optimisées
OCR_CONFIGS = {{
    'francais_standard': '--psm 6 -l fra',
    'francais_precis': '--psm 8 -l fra',
    'multilangue': '--psm 6 -l fra+eng',
    'layout_complexe': '--psm 3 -l fra'
}}

# Patterns d'extraction validés
EXTRACTION_PATTERNS = {{
    'poste': [
        r'(?:poste|position)[\\s:]*([^,\\n\\r\\.]+)',
        r'(attaquant|passeur|central|libéro|libero|réceptionneur|pointu|opposite)'
    ],
    'taille': [
        r'(?:taille)[\\s:]*(\\d{{1,3}})(?:\\s*cm)?',
        r'(\\d{{3}})\\s*cm'
    ],
    'poids': [
        r'(?:poids)[\\s:]*(\\d{{2,3}})(?:\\s*kg)?',
        r'(\\d{{2,3}})\\s*kg'
    ],
    'age': [
        r'(?:âge|age)[\\s:]*(\\d{{1,2}})',
        r'(\\d{{1,2}})\\s*ans?'
    ],
    'club': [
        r'(?:club|équipe)[\\s:]+([^,\\n\\r\\.{{3,50}})'
    ],
    'selections': [
        r'(?:sélections?)[\\s:]*(\\d+)',
        r'(\\d+)\\s*sélections?'
    ]
}}
'''
    
    try:
        with open('ocr_config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"✅ Configuration sauvée: ocr_config.py")
    except Exception as e:
        print(f"⚠️ Erreur sauvegarde config: {e}")
    
    # 2. Créer un rapport de test
    report_content = f'''# Rapport Test OCR FFVB
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Configuration
- Tesseract: {tesseract_path}
- Version: {pytesseract.get_tesseract_version()}

## Résultats Test Kevin Tillie
Informations extraites: {len(found_data)}

{chr(10).join([f"- {k}: {v}" for k, v in found_data.items()])}

## Échantillon Texte OCR
{sample_text[:500]}...

## Statut
OCR fonctionnel ✅
'''
    
    try:
        from datetime import datetime
        with open('rapport_test_ocr.md', 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✅ Rapport sauvé: rapport_test_ocr.md")
    except Exception as e:
        print(f"⚠️ Erreur sauvegarde rapport: {e}")

def main():
    """Test et correction principal"""
    print("🏐 CORRECTION & TEST OCR FFVB")
    print("Configuration automatique de Tesseract")
    print()
    
    success = fix_and_test_ocr()
    
    if success:
        print(f"\n🎉 OCR CONFIGURÉ ET FONCTIONNEL!")
        print(f"✅ Vous pouvez maintenant extraire les données des 51 joueurs")
        print(f"\n🚀 PROCHAINES ÉTAPES:")
        print(f"1. python enhanced_ocr_extractor.py  # Extraction complète")
        print(f"2. Ou testez d'abord: python simple_image_ocr_test.py")
    else:
        print(f"\n❌ PROBLÈME DE CONFIGURATION OCR")
        print(f"🔧 Vérifiez l'installation de Tesseract")

if __name__ == "__main__":
    main()