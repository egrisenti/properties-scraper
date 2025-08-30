import scrapy
from properties.items import PropertiesItem
from properties.itemloaders import propertyLoader

class PropertiesspiderSpider(scrapy.Spider):
    name = "propertiesspider"
    allowed_domains = ["www.italianhousesforsale.com"]
    start_urls = ["https://www.italianhousesforsale.com/property-for-sale-in-italy/?sortby=d_date"]
    
    def parse(self, response):
        
        prop = response.css('div.item-wrap')

        for pro in prop:
            property_item = propertyLoader(item=PropertiesItem(), selector = pro)
            property_item.add_css('name', 'a h3::text'),
            property_item.add_css('price', 'div.ihs-price::text'),
            property_item.add_css('type', 'div.col span::text'),
            property_item.add_css('mq', 'li.h-area span.hz-figure::text'),
            property_item.add_css('bed', 'li.h-beds span.hz-figure::text'),
            property_item.add_css('bath', 'li.h-baths span.hz-figure::text'),
            property_item.add_css('url', 'a::attr(href)'),
            yield property_item.load_item()

#
#        next_page = response.css('ul.pagination li.page-item a::attr(href)').getall()
#
#        if next_page[-2] is not None:
#            next_page_url = next_page[-2]
#            yield response.follow(next_page_url, callback = self.parse)
