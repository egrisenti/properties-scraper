from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

def clean_name(value):
    return value.strip()

def clean_price(value):
    return value.replace("€", "").replace(",", "").strip()

class propertyLoader(ItemLoader):

    default_output_processor = TakeFirst()
    price_in = MapCompose(clean_price)
    name_in = MapCompose(clean_name)