# test_tesseract_install.py
"""
Script pour tester et configurer l'installation de Tesseract
"""

import os
import sys

def test_tesseract_installation():
    """Teste l'installation de Tesseract"""
    print("🔧 TEST INSTALLATION TESSERACT")
    print("=" * 35)
    
    # Test 1: Import des modules Python
    print("📦 Test des modules Python:")
    
    modules = ['pytesseract', 'PIL', 'cv2']
    missing_modules = []
    
    for module in modules:
        try:
            if module == 'PIL':
                import PIL
            elif module == 'cv2':
                import cv2
            else:
                import pytesseract
            print(f"   ✅ {module}: OK")
        except ImportError:
            print(f"   ❌ {module}: MANQUANT")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n📥 Installation requise:")
        if 'pytesseract' in missing_modules:
            print("   pip install pytesseract")
        if 'PIL' in missing_modules:
            print("   pip install pillow")
        if 'cv2' in missing_modules:
            print("   pip install opencv-python")
        return False
    
    # Test 2: Tesseract système
    print(f"\n🔍 Test Tesseract système:")
    
    try:
        import pytesseract
        
        # Chemins possibles sur Windows
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME', '')),
            "tesseract"  # Si dans PATH
        ]
        
        tesseract_found = False
        working_path = None
        
        for path in possible_paths:
            try:
                if path != "tesseract" and not os.path.exists(path):
                    continue
                
                pytesseract.pytesseract.tesseract_cmd = path
                version = pytesseract.get_tesseract_version()
                print(f"   ✅ Tesseract trouvé: {path}")
                print(f"   ✅ Version: {version}")
                tesseract_found = True
                working_path = path
                break
                
            except Exception as e:
                continue
        
        if not tesseract_found:
            print("   ❌ Tesseract non trouvé")
            print("   📥 Installation requise:")
            print("      https://github.com/UB-Mannheim/tesseract/wiki")
            return False
        
        # Test 3: OCR fonctionnel
        print(f"\n🧪 Test OCR fonctionnel:")
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            import io
            
            # Créer une image de test simple
            img = Image.new('RGB', (200, 50), color='white')
            draw = ImageDraw.Draw(img)
            draw.text((10, 15), "Test OCR 123", fill='black')
            
            # Test OCR
            text = pytesseract.image_to_string(img, config='--psm 8')
            
            if "test" in text.lower() or "123" in text:
                print("   ✅ OCR fonctionne!")
                print(f"   ✅ Texte détecté: '{text.strip()}'")
                
                # Sauvegarder la config qui fonctionne
                save_tesseract_config(working_path)
                return True
            else:
                print(f"   ⚠️ OCR partiellement fonctionnel")
                print(f"   ⚠️ Texte détecté: '{text.strip()}'")
                return True
                
        except Exception as e:
            print(f"   ❌ Erreur test OCR: {e}")
            return False
    
    except Exception as e:
        print(f"   ❌ Erreur Tesseract: {e}")
        return False

def save_tesseract_config(tesseract_path):
    """Sauvegarde la configuration Tesseract qui fonctionne"""
    config_content = f'''# tesseract_config.py
"""
Configuration Tesseract pour le projet FFVB
Généré automatiquement par test_tesseract_install.py
"""

import pytesseract

# Chemin vers Tesseract qui fonctionne
TESSERACT_PATH = r"{tesseract_path}"

def configure_tesseract():
    """Configure Tesseract avec le bon chemin"""
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Configuration automatique à l'import
configure_tesseract()
'''
    
    try:
        with open('tesseract_config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"   ✅ Configuration sauvée: tesseract_config.py")
    except Exception as e:
        print(f"   ⚠️ Erreur sauvegarde config: {e}")

def install_tesseract_guide():
    """Guide d'installation Tesseract"""
    print("\n📦 GUIDE INSTALLATION TESSERACT")
    print("=" * 35)
    
    print("1. 🌐 Aller sur: https://github.com/UB-Mannheim/tesseract/wiki")
    print("2. 📥 Télécharger: tesseract-ocr-w64-setup-5.3.x.exe")
    print("3. 🚀 Lancer l'installateur")
    print("4. ✅ Garder le chemin par défaut")
    print("5. 🔄 Relancer ce test")
    
    print(f"\n💡 CHEMINS TYPIQUES:")
    print(f"   C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
    print(f"   C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe")

def main():
    """Test principal"""
    print("🏐 TEST INSTALLATION OCR POUR FFVB")
    print("Vérification de Tesseract pour extraction images CV")
    print()
    
    success = test_tesseract_installation()
    
    if success:
        print(f"\n🎉 INSTALLATION OCR RÉUSSIE!")
        print(f"✅ Vous pouvez maintenant extraire les données des images CV")
        print(f"🚀 Prochaine étape: python simple_image_ocr_test.py")
    else:
        print(f"\n❌ INSTALLATION OCR INCOMPLÈTE")
        install_tesseract_guide()
        
        print(f"\n🔧 APRÈS INSTALLATION:")
        print(f"   python test_tesseract_install.py")

if __name__ == "__main__":
    main()