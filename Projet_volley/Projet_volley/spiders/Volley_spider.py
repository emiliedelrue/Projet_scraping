import scrapy
from urllib.parse import urljoin, urlparse, parse_qs
import re
from Projet_volley.items import DataItem
from itemloaders import ItemLoader


class FFVBChampionsSpider(scrapy.Spider):
    name = 'ffvb_champions'
    
    start_urls = [
        'http://www.ffvb.org/index.php?lvlid=220&dsgtypid=37&artid=291&pos=0'
    ]

    def parse(self, response):
        for row in response.css("tr"):
            if row.css("th[scope='row']") and len(row.css("td")) >= 2:
                loader = ItemLoader(item=DataItem(), selector=row)  
                loader.add_css("Année", "th[scope='row']::text")  
                loader.add_css("Masculin", "td:nth-child(2)::text")  
                loader.add_css("Feminin", "td:nth-child(3)::text")   
                yield loader.load_item()

class FFVBChampionsFranceSpider(scrapy.Spider):
    name = 'ffvb_champions_France'
    
    start_urls = [
        'http://www.ffvb.org/index.php?lvlid=220&dsgtypid=37&artid=290&pos=1'
    ]

    def parse(self, response):
        for row in response.css("tr"):
            if row.css("th[scope='row']") and len(row.css("td")) >= 2:
                loader = ItemLoader(item=DataItem(), selector=row)  
                loader.add_css("Année", "th[scope='row']::text")  
                loader.add_css("Masculin", "td:nth-child(2)::text")  
                loader.add_css("Feminin", "td:nth-child(3)::text")   
                yield loader.load_item()

class FFVBChampionsFederalSpider(scrapy.Spider):
    name = 'ffvb_champions_France_Federal'
    
    start_urls = [
        'http://www.ffvb.org/index.php?lvlid=220&dsgtypid=37&artid=539&pos=2'
    ]

    def parse(self, response):
        for row in response.css("tr"):
            if row.css("th[scope='row']") and len(row.css("td")) >= 2:
                loader = ItemLoader(item=DataItem(), selector=row)  
                loader.add_css("Année", "th[scope='row']::text")  
                loader.add_css("Masculin", "td:nth-child(2)::text")  
                loader.add_css("Feminin", "td:nth-child(3)::text")   
                yield loader.load_item()

class FFVBPlayerSpider(scrapy.Spider):
    name = 'ffvb_players'
    allowed_domains = ['ffvb.org']
    start_urls = ['http://www.ffvb.org/index.php?lvlid=384&dsgtypid=37&artid=1217&pos=0']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'DOWNLOAD_DELAY': 2,
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """Parse chaque page de joueur"""
        
        # Extraire les informations du joueur actuel
        player_data = self.extract_player_info(response)
        
        if player_data:
            yield player_data
        
        # Chercher le lien vers le joueur suivant
        next_link = response.css('a:contains(">>")::attr(href)').get()
        
        # Alternative si le sélecteur ci-dessus ne fonctionne pas
        if not next_link:
            next_link = response.css('a[href*="pos="]:contains("GREBENNIKOV"), a[href*="pos="]:contains(">>")::attr(href)').get()
        
        # Autre alternative : chercher tous les liens avec pos= et prendre le suivant
        if not next_link:
            all_nav_links = response.css('a[href*="pos="]::attr(href)').getall()
            current_pos = self.get_position_from_url(response.url)
            
            for link in all_nav_links:
                link_pos = self.get_position_from_url(link)
                if link_pos == current_pos + 1:
                    next_link = link
                    break
        
        # Si on a trouvé un lien suivant, continuer
        if next_link:
            next_url = urljoin(response.url, next_link)
            self.logger.info(f"Navigation vers: {next_url}")
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                dont_filter=True
            )
        else:
            self.logger.info("Fin de la navigation - plus de joueurs")

    def extract_player_info(self, response):
        """Extrait les informations du joueur depuis la page"""
        
        # Récupérer le nom du joueur depuis le lien de navigation ou le titre
        player_name = ""
        
        # Méthode 1: depuis le lien de navigation actuel
        nav_links = response.css('a[href*="pos="]')
        current_pos = self.get_position_from_url(response.url)
        
        for link in nav_links:
            link_pos = self.get_position_from_url(link.css('::attr(href)').get())
            if link_pos == current_pos:
                player_name = link.css('::text').get()
                if player_name:
                    player_name = player_name.replace('>>>', '').strip()
                break
        
        # Méthode 2: depuis l'URL de l'image CV
        cv_image = response.css('div.articleTexte img::attr(src)').get()
        cv_image_alt = response.css('div.articleTexte img::attr(alt)').get()
        
        # Extraire le nom depuis le nom du fichier image si pas trouvé
        if not player_name and cv_image:
            filename = cv_image.split('/')[-1]
            # Format exemple: "1%20Barth%C3%A9l%C3%A9my%20Chinenyeze.png"
            name_from_file = filename.replace('.png', '').replace('.jpg', '')
            # Décoder les caractères URL
            import urllib.parse
            name_from_file = urllib.parse.unquote(name_from_file)
            # Supprimer le numéro au début
            name_from_file = re.sub(r'^\d+\s*', '', name_from_file)
            player_name = name_from_file
        
        if not player_name:
            return None
        
        # Séparer nom et prénom
        name_parts = player_name.split()
        if len(name_parts) >= 2:
            nom = name_parts[0]
            prenom = ' '.join(name_parts[1:])
        else:
            nom = player_name
            prenom = ""
        
        # URL complète de l'image CV
        full_cv_url = urljoin(response.url, cv_image) if cv_image else ""
        
        player_data = {
            'nom': nom,
            'prenom': prenom,
            'poste': '',  # À remplir manuellement ou par OCR de l'image
            'age': '',
            'taille': '',
            'poids': '',
            'club': '',
            'photo_url': full_cv_url,
            'biographie': '',
            'position_nav': current_pos,
            'page_url': response.url
        }
        
        self.logger.info(f"Joueur trouvé: {nom} {prenom}")
        return player_data
    
    def get_position_from_url(self, url):
        """Extrait la position depuis l'URL"""
        if not url:
            return 0
        
        try:
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            pos = query_params.get('pos', ['0'])[0]
            return int(pos)
        except:
            return 0

# Version alternative pour extraire TOUS les liens de navigation d'abord
class FFVBPlayerSpiderV2(scrapy.Spider):
    name = 'ffvb_players_v2'
    allowed_domains = ['ffvb.org']
    start_urls = ['http://www.ffvb.org/index.php?lvlid=384&dsgtypid=37&artid=1217&pos=0']
    
    def parse(self, response):
        """Parse la première page et trouve tous les liens de navigation"""
        
        # Extraire tous les liens de navigation des joueurs
        nav_links = []
        
        # Chercher dans la navigation (si elle existe sur la page)
        player_links = response.css('a[href*="pos="]::attr(href)').getall()
        
        # Si pas de navigation visible, créer les URLs manuellement
        if not player_links:
            # Essayer de déterminer le nombre total de joueurs
            # En général, les équipes nationales ont entre 12-20 joueurs
            base_url = "http://www.ffvb.org/index.php?lvlid=384&dsgtypid=37&artid={}&pos={}"
            
            # Commencer avec les IDs d'articles probables
            for artid in range(1217, 1240):  # Ajuster selon le besoin
                for pos in range(0, 25):  # Maximum 25 joueurs
                    url = base_url.format(artid, pos)
                    nav_links.append(url)
        else:
            nav_links = [urljoin(response.url, link) for link in player_links]
        
        # Visiter chaque lien
        for url in nav_links:
            yield scrapy.Request(
                url=url,
                callback=self.parse_player,
                dont_filter=True
            )
    
    def parse_player(self, response):
        """Parse une page de joueur spécifique"""
        
        # Vérifier si la page existe (pas d'erreur 404)
        if response.status != 200:
            return
        
        # Vérifier s'il y a bien un CV/image
        cv_image = response.css('div.articleTexte img::attr(src)').get()
        if not cv_image:
            return
        
        # Extraire les informations comme dans la version précédente
        spider_v1 = FFVBPlayerSpider()
        player_data = spider_v1.extract_player_info(response)
        
        if player_data:
            yield player_data
