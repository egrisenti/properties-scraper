import scrapy
from properties.items import PropertiesItem
from properties.itemloaders import propertyLoader

class PropertiesspiderSpider(scrapy.Spider):
    name = "propertiesspider"
    allowed_domains = ["www.italianhousesforsale.com"]
    start_urls = ["https://www.italianhousesforsale.com/property-for-sale-in-italy/?sortby=d_date"]

    # custom counter
    page_count = 0
    max_pages = 50

    def parse(self, response):

        # increase counter
        self.page_count += 1
        self.logger.info(f"Parsing page {self.page_count}")

        # stop if we reached max pages
        if self.page_count > self.max_pages:
            self.logger.info("Reached max page limit, stopping crawl.")
            return

        prop = response.css('div.item-wrap')

        for pro in prop:
            property_item = propertyLoader(item=PropertiesItem(), selector = pro)
            property_item.add_css('url', 'a::attr(href)')
            property_item.add_css('name', 'a h3::text'),
            property_item.add_css('price', 'div.ihs-price::text'),
            property_item.add_css('type', 'div.col span::text'),
            property_item.add_css('mq', 'li.h-area span.hz-figure::text'),
            property_item.add_css('bed', 'li.h-beds span.hz-figure::text'),
            property_item.add_css('bath', 'li.h-baths span.hz-figure::text'),
            
            item = property_item.load_item()
            detail_url = pro.css('a::attr(href)').get()
            if detail_url:
                yield response.follow(
                    detail_url, 
                    callback = self.parse_detail, 
                    meta={'item': item}
                )

        next_page = response.css('ul.pagination li.page-item a::attr(href)').getall()
        if next_page and len(next_page) > 2:
            next_page_url = next_page[-2]
            yield response.follow(next_page_url, callback = self.parse)



    def parse_detail(self, response):

        item = response.meta['item']
        property_item = propertyLoader(item=item, selector=response)
        
        property_item.add_value('url', response.url)
        property_item.add_css('region', 'li.detail-state span::text')
        property_item.add_css('province', 'li.detail-city span::text')
        property_item.add_css('town', 'li.detail-address span::text')
        property_item.add_css('town2', 'li.detail-area span::text')
        features = response.css('div.block-content-wrap li a::text').getall()
        for feat in features:
            if "Pool" in feat:
                property_item.add_value('pool', 1)
            if "Graden" in feat:
                property_item.add_value('garden', 1)
            if "Parking" in feat:
                property_item.add_value('parking', 1)

        yield property_item.load_item()


