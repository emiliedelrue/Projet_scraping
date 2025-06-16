import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
from itemloaders import ItemLoader
import re
 
 
    
def clean_text(value):
    if value:
        value = re.sub(r'<[^>]+>', '', value)
        value = re.sub(r'[\xa0\u00A0\u2000-\u200B\u2028\u2029]', ' ', value)
        value = re.sub(r'\s{2,}', ' ', value.strip())  
        return value if value else ''
    return ''
 
def extract_number(value):
    if value:
        match = re.search(r'(\d+)', str(value))
        return int(match.group(1)) if match else None
    return None
 
def clean_team_name(value):
    if value:
        value = re.sub(r'<[^>]+>', '', str(value))
        value = value.strip()
        value = re.sub(r'[\xa0\u00A0]', ' ', value)
        value = re.sub(r' {3,}', ' ', value)
        return value if value else ''
    return ''
 
 
def extract_height(value):
    if value:
        value = value.replace(',', '.')
        
        match = re.search(r'(\d+)[\.,]?(\d+)?m', value)
        if match:
            meters = int(match.group(1))
            cm = int(match.group(2)) if match.group(2) else 0
            return meters * 100 + cm
        
        match = re.search(r'(\d{3})', value)
        if match:
            return int(match.group(1))
            
    return None
 
def extract_weight(value):
    if value:
        match = re.search(r'(\d+)', value)
        return int(match.group(1)) if match else None
    return None
 
class PlayerItem(scrapy.Item):
    nom = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    prenom = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    nom_complet = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    numero_maillot = scrapy.Field(
        input_processor=MapCompose(extract_number),
        output_processor=TakeFirst()
    )
    
    date_naissance = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    age = scrapy.Field(
        input_processor=MapCompose(extract_number),
        output_processor=TakeFirst()
    )
    taille = scrapy.Field(
        input_processor=MapCompose(extract_height),
        output_processor=TakeFirst()
    )
    poids = scrapy.Field(
        input_processor=MapCompose(extract_weight),
        output_processor=TakeFirst()
    )
    
    poste = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    club_actuel = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    pays_club = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    
    selections = scrapy.Field(
        input_processor=MapCompose(extract_number),
        output_processor=TakeFirst()
    )
    palmares = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=Join(' | ')
    )
    
    equipe = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    categorie = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    url_source = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    photo_url = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    
    nationalite = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    lieu_naissance = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    formation = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
 
class TeamItem(scrapy.Item):
    nom_equipe = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    categorie = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    entraineur = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    staff_technique = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=Join(' | ')
    )
    nombre_joueurs = scrapy.Field(
        input_processor=MapCompose(extract_number),
        output_processor=TakeFirst()
    )
    url_source = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
 
class StaffItem(scrapy.Item):
    nom = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    prenom = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    fonction = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    equipe = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
    url_source = scrapy.Field(
        input_processor=MapCompose(clean_text),
        output_processor=TakeFirst()
    )
 
class DataItem(scrapy.Item):
    Année = scrapy.Field()
    Masculin = scrapy.Field()
    Feminin = scrapy.Field()
 
class ResultItem(scrapy.Item):
    Année = scrapy.Field()
    Masculin = scrapy.Field()
    Feminin = scrapy.Field()
    Type_Championnat = scrapy.Field()
 
class ResultItemLoader(ItemLoader):
    default_item_class = ResultItem
    
    Année_in = MapCompose(extract_number)
    Année_out = TakeFirst()
    
    Masculin_in = MapCompose(clean_team_name)
    Masculin_out = TakeFirst()
    
    Feminin_in = MapCompose(clean_team_name)  
    Feminin_out = TakeFirst()
    
    Type_Championnat_in = MapCompose(clean_text)
    Type_Championnat_out = TakeFirst()