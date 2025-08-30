# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PropertiesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = scrapy.Field()
    price = scrapy.Field()
    type = scrapy.Field()
    mq = scrapy.Field()
    bed = scrapy.Field()
    bath = scrapy.Field()
    url = scrapy.Field()
    region = scrapy.Field()
    province = scrapy.Field()
    town = scrapy.Field()
    town2 = scrapy.Field()
    pool = scrapy.Field()
    garden = scrapy.Field()
    parking = scrapy.Field()
