# spiders/ffvb_simple_debug_spider.py
import scrapy
import csv
from datetime import datetime

class FFVBSimpleDebugSpider(scrapy.Spider):
    name = 'ffvb_debug'
    allowed_domains = ['ffvb.org', 'www.ffvb.org']
    start_urls = [
        'http://www.ffvb.org/index.php?lvlid=384&dsgtypid=37&artid=1217&pos=0',
    ]
    
    def __init__(self):
        # Fichier CSV simple
        self.csv_file = open('ffvb_debug_output.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['type', 'nom_joueur', 'numero', 'poste', 'info_supplementaire', 'url_source'])
        self.count = 0

    def closed(self, reason):
        self.csv_file.close()
        self.logger.info(f'🎉 Debug terminé! {self.count} éléments trouvés')

    def parse(self, response):
        """Parse avec debug maximum"""
        self.logger.info(f'🔍 DEBUGGING: {response.url}')
        
        # Sauvegarder la page pour inspection
        with open('debug_page_source.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        # 1. Chercher TOUT le texte contenant des noms de joueurs
        all_text = response.css('*::text').getall()
        player_patterns = []
        
        for text in all_text:
            text = text.strip()
            if text and len(text) > 2:
                # Chercher des patterns typiques de joueurs
                if any(word in text.lower() for word in ['joueur', 'attaquant', 'passeur', 'libero', 'central']):
                    player_patterns.append(text)
                # Chercher des noms propres (majuscules)
                elif text[0].isupper() and ' ' in text and len(text.split()) == 2:
                    player_patterns.append(text)
                # Chercher des numéros avec noms
                elif any(char.isdigit() for char in text) and any(char.isalpha() for char in text):
                    player_patterns.append(text)
        
        # 2. Chercher dans les tables
        tables = response.css('table')
        self.logger.info(f'📊 Tables trouvées: {len(tables)}')
        
        for i, table in enumerate(tables):
            rows = table.css('tr')
            self.logger.info(f'  Table {i+1}: {len(rows)} lignes')
            
            for j, row in enumerate(rows):
                cells = row.css('td::text, th::text').getall()
                if cells:
                    row_text = ' | '.join([cell.strip() for cell in cells if cell.strip()])
                    if row_text:
                        self.csv_writer.writerow(['table_row', row_text, '', '', f'Table {i+1} Row {j+1}', response.url])
                        self.count += 1

        # 3. Chercher des listes
        lists = response.css('ul, ol')
        self.logger.info(f'📋 Listes trouvées: {len(lists)}')
        
        for i, lst in enumerate(lists):
            items = lst.css('li')
            for j, item in enumerate(items):
                item_text = item.css('::text').get()
                if item_text and item_text.strip():
                    self.csv_writer.writerow(['list_item', item_text.strip(), '', '', f'Liste {i+1} Item {j+1}', response.url])
                    self.count += 1

        # 4. Chercher des divs avec du contenu intéressant
        divs = response.css('div')
        interesting_divs = []
        
        for div in divs:
            div_text = div.css('::text').get()
            if div_text and div_text.strip():
                text = div_text.strip()
                # Si ça ressemble à un nom de joueur ou info sportive
                if (len(text.split()) == 2 and text[0].isupper()) or \
                   any(word in text.lower() for word in ['n°', '#', 'cm', 'kg', 'ans']):
                    interesting_divs.append(text)

        for text in interesting_divs:
            self.csv_writer.writerow(['div_content', text, '', '', 'Contenu DIV intéressant', response.url])
            self.count += 1

        # 5. Extraire tous les liens pour voir la structure
        links = response.css('a::attr(href)').getall()
        valid_links = []
        
        for link in links:
            if link and not link.startswith('javascript:') and not link.startswith('#'):
                if 'collectif' in link.lower() or 'joueur' in link.lower() or 'equipe' in link.lower():
                    valid_links.append(link)
        
        self.logger.info(f'🔗 Liens intéressants trouvés: {len(valid_links)}')
        for link in valid_links[:5]:  # Limiter à 5
            self.csv_writer.writerow(['link_found', link, '', '', 'Lien intéressant', response.url])
            self.count += 1

        # 6. Log de debug des patterns trouvés
        self.logger.info(f'🎯 Patterns joueurs trouvés: {len(player_patterns)}')
        for pattern in player_patterns[:10]:  # Top 10
            self.csv_writer.writerow(['player_pattern', pattern, '', '', 'Pattern détecté', response.url])
            self.count += 1

        # 7. Chercher des images (photos de joueurs)
        images = response.css('img::attr(src)').getall()
        player_images = [img for img in images if any(word in img.lower() for word in ['player', 'joueur', 'photo'])]
        
        for img in player_images:
            self.csv_writer.writerow(['player_image', img, '', '', 'Photo joueur potentielle', response.url])
            self.count += 1

        # 8. Extraire le titre de la page
        title = response.css('title::text').get()
        if title:
            self.csv_writer.writerow(['page_title', title.strip(), '', '', 'Titre de la page', response.url])
            self.count += 1

        # 9. Chercher des éléments avec des classes spécifiques
        special_elements = response.css('[class*="player"], [class*="joueur"], [class*="team"], [class*="equipe"]')
        for elem in special_elements:
            elem_text = elem.css('::text').get()
            if elem_text and elem_text.strip():
                self.csv_writer.writerow(['special_element', elem_text.strip(), '', '', 'Élément spécialisé', response.url])
                self.count += 1

        self.logger.info(f'📈 Total éléments extraits: {self.count}')