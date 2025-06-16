import scrapy
from ffvb_scraper.items import DataItem, ResultItemLoader
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
 
        self.logger.info(f"Parsing {championship_type} depuis {response.url}")
 
        for row in response.css("tr"):
            if row.css("th[scope='row']") and len(row.css("td")) >= 2:
                
                year_raw = row.css("th[scope='row']::text").get()
                male_raw = row.css("td:nth-child(2)::text").get()
                female_raw = row.css("td:nth-child(3)::text").get()
                
                year_all = ''.join(row.css("th[scope='row']::text").getall())
                male_all = ''.join(row.css("td:nth-child(2)::text").getall())
                female_all = ''.join(row.css("td:nth-child(3)::text").getall())
                
                self.logger.info(f"DEBUG RAW - Année: {repr(year_raw)} | Masculin: {repr(male_raw)} | Féminin: {repr(female_raw)}")
                self.logger.info(f"DEBUG ALL - Année: {repr(year_all)} | Masculin: {repr(male_all)} | Féminin: {repr(female_all)}")
                
                loader = ResultItemLoader(selector=row)
                
                loader.add_css("Année", "th[scope='row']::text")
                loader.add_css("Année", "th[scope='row'] *::text")  
                
                loader.add_css("Masculin", "td:nth-child(2)::text")
                loader.add_css("Masculin", "td:nth-child(2) *::text")  
                
                loader.add_css("Feminin", "td:nth-child(3)::text")
                loader.add_css("Feminin", "td:nth-child(3) *::text")  
                
                loader.add_value("Type_Championnat", championship_type)
                
                item = loader.load_item()
                
                self.logger.info(f"DEBUG ITEM: {dict(item)}")
                
                if item.get('Année') and (item.get('Masculin') or item.get('Feminin')):
                    yield item
                else:
                    self.logger.warning(f"Item incomplet ignoré: {dict(item)}")
                    
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

