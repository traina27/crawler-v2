import scrapy
import database.storage as storage

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['https://sachvui.com/']

    def parse(self, response):
        LIST_CATEGORY = []
        SET_SELECTOR = '.cat-item.col-xs-12.col-md-4.col-sm-6'
        for brickset in response.css(SET_SELECTOR):

            NAME_SELECTOR = 'a ::text'
            URL_CATEGORY = brickset.css('a ::attr(href)').extract_first()
            print('URL ', URL_CATEGORY)
