import scrapy
from ffvb_scraper.items import DataItem, ResultItem
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

class FFVBAllChampionsSpider(scrapy.Spider):
    name = 'ffvb_resultats'
    
    start_urls = [
        'http://www.ffvb.org/index.php?lvlid=220&dsgtypid=37&artid=291&pos=0',  
        'http://www.ffvb.org/index.php?lvlid=220&dsgtypid=37&artid=290&pos=1',  
        'http://www.ffvb.org/index.php?lvlid=220&dsgtypid=37&artid=539&pos=2'   
    ]

    def parse(self, response):
        if 'artid=291' in response.url:
            championship_type = 'Champions de France'
        elif 'artid=290' in response.url:
            championship_type = 'Coupe de France Volley-ball'
        elif 'artid=539' in response.url:
            championship_type = 'Coupe de France Federal'
        else:
            championship_type = 'Unknown'

        for row in response.css("tr"):
            if row.css("th[scope='row']") and len(row.css("td")) >= 2:
                loader = ItemLoader(item=ResultItem(), selector=row)  
                loader.add_css("Année", "th[scope='row']::text")  
                loader.add_css("Masculin", "td:nth-child(2)::text")  
                loader.add_css("Feminin", "td:nth-child(3)::text")
                loader.add_value("Type_Championnat", championship_type)  
                yield loader.load_item()


class FFVBChampionsFranceBeachSpider(scrapy.Spider):
    name = 'ffvb_champions_France_beach_volley'
    
    start_urls = [
        'http://www.ffvb.org/index.php?lvlid=230&dsgtypid=37&artid=308&pos=0'
    ]

    def parse(self, response):
        for row in response.css("tr"):
            if row.css("th[scope='row']") and len(row.css("td")) >= 2:
                loader = ItemLoader(item=DataItem(), selector=row)  
                loader.add_css("Année", "th[scope='row']::text")  
                loader.add_css("Masculin", "td:nth-child(2)::text")  
                loader.add_css("Feminin", "td:nth-child(3)::text")   
                yield loader.load_item()

