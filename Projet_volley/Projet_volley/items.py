# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayerItem(scrapy.Item):
    nom = scrapy.Field()
    prenom = scrapy.Field()
    poste = scrapy.Field()
    age = scrapy.Field()
    taille = scrapy.Field()
    poids = scrapy.Field()
    club = scrapy.Field()
    photo_url = scrapy.Field()
    biographie = scrapy.Field()
    position_nav = scrapy.Field()
    page_url = scrapy.Field()