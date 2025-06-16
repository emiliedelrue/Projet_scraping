# clean_duplicates.py
"""
Script pour nettoyer et déduplicater les données des joueurs FFVB
"""

import csv
import os
from collections import defaultdict

def analyze_and_clean_players():
    """Analyse et nettoie les données des joueurs"""
    print("🧹 NETTOYAGE ET DÉDUPLICATION DES JOUEURS")
    print("=" * 50)
    
    if not os.path.exists('ffvb_players_complete.csv'):
        print(" Fichier ffvb_players_complete.csv non trouvé")
        return
    
    # Charger les données
    players = load_players_data()
    print(f" Total lignes dans le fichier: {len(players)}")
    
    # Analyser les doublons
    duplicates_analysis = analyze_duplicates(players)
    
    # Nettoyer les doublons
    unique_players = deduplicate_players(players)
    
    # Sauvegarder les données nettoyées
    save_clean_data(unique_players)
    
    # Afficher le résumé
    print_cleaning_summary(len(players), len(unique_players), duplicates_analysis)

def load_players_data():
    """Charge les données des joueurs"""
    players = []
    
    try:
        with open('ffvb_players_complete.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            players = list(reader)
    except Exception as e:
        print(f" Erreur lecture fichier: {e}")
    
    return players

def analyze_duplicates(players):
    """Analyse les types de doublons"""
    print(f"\n ANALYSE DES DOUBLONS:")
    print("-" * 30)
    
    # Grouper par nom
    by_name = defaultdict(list)
    # Grouper par numéro
    by_number = defaultdict(list)
    # Grouper par URL d'image
    by_image = defaultdict(list)
    
    for i, player in enumerate(players):
        name = player.get('nom_joueur', '').strip()
        numero = player.get('numero', '').strip()
        image_url = player.get('url_cv_image', '').strip()
        
        if name:
            by_name[name].append((i, player))
        if numero:
            by_number[numero].append((i, player))
        if image_url:
            by_image[image_url].append((i, player))
    
    # Analyser les doublons
    name_duplicates = {name: indices for name, indices in by_name.items() if len(indices) > 1}
    number_duplicates = {num: indices for num, indices in by_number.items() if len(indices) > 1}
    image_duplicates = {img: indices for img, indices in by_image.items() if len(indices) > 1}
    
    print(f" Doublons par nom: {len(name_duplicates)}")
    print(f" Doublons par numéro: {len(number_duplicates)}")
    print(f" Doublons par image: {len(image_duplicates)}")
    
    # Afficher quelques exemples
    if name_duplicates:
        print(f"\n Exemples doublons par nom:")
        for name, occurrences in list(name_duplicates.items())[:3]:
            print(f"   {name}: {len(occurrences)} occurrences")
            for idx, player in occurrences[:2]:  # Max 2 exemples
                url = player.get('url_page_principale', 'N/A')
                print(f"     - Ligne {idx+1}: {url}")
    
    return {
        'by_name': name_duplicates,
        'by_number': number_duplicates,
        'by_image': image_duplicates
    }

def deduplicate_players(players):
    """Déduplique les joueurs en gardant la meilleure version"""
    print(f"\n DÉDUPLICATION EN COURS...")
    
    # Créer un dictionnaire pour identifier les joueurs uniques
    unique_players = {}
    
    for player in players:
        # Créer une clé unique basée sur nom + numéro
        name = player.get('nom_joueur', '').strip()
        numero = player.get('numero', '').strip()
        
        if not name:
            continue  # Ignorer les lignes sans nom
        
        # Clé unique
        player_key = f"{name}_{numero}" if numero else name
        
        if player_key not in unique_players:
            # Premier joueur avec cette clé
            unique_players[player_key] = player
        else:
            # Joueur déjà existant - garder le meilleur
            existing = unique_players[player_key]
            better_player = choose_better_player(existing, player)
            unique_players[player_key] = better_player
    
    # Convertir en liste
    unique_list = list(unique_players.values())
    
    # Trier par numéro si possible
    def sort_key(p):
        try:
            return int(p.get('numero', 999))
        except:
            return 999
    
    unique_list.sort(key=sort_key)
    
    print(f" Déduplication terminée")
    print(f" Joueurs uniques: {len(unique_list)}")
    
    return unique_list

def choose_better_player(player1, player2):
    """Choisit le meilleur joueur entre deux doublons"""
    
    # Critères de qualité (par ordre de priorité)
    def calculate_quality_score(player):
        score = 0
        
        # +10 si a une image CV
        if player.get('url_cv_image', '').strip():
            score += 10
        
        # +5 si a une URL de page
        if player.get('url_page_principale', '').strip():
            score += 5
        
        # +1 pour chaque champ non vide
        important_fields = ['nom_joueur', 'numero', 'poste', 'taille', 'poids', 'age', 'club_actuel']
        for field in important_fields:
            if player.get(field, '').strip():
                score += 1
        
        # +2 si a une date d'extraction récente
        if player.get('date_extraction', '').strip():
            score += 2
        
        return score
    
    score1 = calculate_quality_score(player1)
    score2 = calculate_quality_score(player2)
    
    # Retourner le joueur avec le meilleur score
    return player1 if score1 >= score2 else player2

def save_clean_data(unique_players):
    """Sauvegarde les données nettoyées"""
    output_file = 'ffvb_players_clean.csv'
    
    if not unique_players:
        print(" Aucune donnée à sauvegarder")
        return
    
    try:
        # Obtenir tous les champs possibles
        all_fields = set()
        for player in unique_players:
            all_fields.update(player.keys())
        
        # Ordonner les champs importants en premier
        priority_fields = [
            'nom_joueur', 'numero', 'poste', 'taille', 'poids', 'age',
            'club_actuel', 'selections', 'url_cv_image', 'url_page_principale',
            'date_extraction'
        ]
        
        # Champs restants
        remaining_fields = sorted(all_fields - set(priority_fields))
        final_fields = priority_fields + remaining_fields
        
        # Écrire le fichier CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=final_fields)
            writer.writeheader()
            writer.writerows(unique_players)
        
        print(f" Données nettoyées sauvées: {output_file}")
        
    except Exception as e:
        print(f" Erreur sauvegarde: {e}")

def print_cleaning_summary(original_count, clean_count, duplicates_analysis):
    """Affiche le résumé du nettoyage"""
    print(f"\n RÉSUMÉ DU NETTOYAGE:")
    print("=" * 30)
    print(f" Lignes originales: {original_count}")
    print(f" Joueurs uniques: {clean_count}")
    print(f" Doublons supprimés: {original_count - clean_count}")
    
    if original_count > 0:
        reduction_pct = ((original_count - clean_count) / original_count) * 100
        print(f" Réduction: {reduction_pct:.1f}%")
    
    # Détail des types de doublons
    name_dups = len(duplicates_analysis['by_name'])
    if name_dups > 0:
        print(f" Joueurs avec doublons de nom: {name_dups}")
    
    print(f"\n Fichier nettoyé: ffvb_players_clean.csv")
    print(f" Prêt pour l'extraction OCR!")

def preview_clean_data():
    """Affiche un aperçu des données nettoyées"""
    if not os.path.exists('ffvb_players_clean.csv'):
        print(" Fichier ffvb_players_clean.csv non trouvé")
        return
    
    print(f"\n APERÇU DES DONNÉES NETTOYÉES:")
    print("-" * 40)
    
    try:
        with open('ffvb_players_clean.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            players = list(reader)
        
        print(f" Total joueurs uniques: {len(players)}")
        
        # Afficher les 10 premiers
        print(f"\n👥 PREMIERS JOUEURS:")
        for i, player in enumerate(players[:10], 1):
            name = player.get('nom_joueur', 'N/A')
            numero = player.get('numero', 'N/A')
            has_image = "🖼️" if player.get('url_cv_image') else "❌"
            print(f"   {i:2d}. #{numero:>2} - {name:<20} {has_image}")
        
        if len(players) > 10:
            print(f"   ... et {len(players) - 10} autres joueurs")
        
        # Statistiques
        with_images = sum(1 for p in players if p.get('url_cv_image', '').strip())
        print(f"\n STATISTIQUES:")
        print(f"   Images CV disponibles: {with_images}/{len(players)} ({(with_images/len(players)*100):.1f}%)")
        
    except Exception as e:
        print(f" Erreur lecture aperçu: {e}")

def main():
    """Fonction principale"""
    print("🧹 NETTOYAGE DONNÉES FFVB")
    print("Suppression des doublons avant extraction OCR")
    print()
    
    # Nettoyer les données
    analyze_and_clean_players()
    
    # Afficher un aperçu
    preview_clean_data()
    
    print(f"\n PROCHAINES ÉTAPES:")
    print(f"1. Vérifiez ffvb_players_clean.csv")
    print(f"2. Lancez: python final_ocr_extractor.py")
    print(f"   (modifiez le nom du fichier d'entrée)")

if __name__ == "__main__":
    main()