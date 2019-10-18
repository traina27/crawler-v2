import scrapy
import database.storage as storage

class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['https://sachvui.com/']
    CONNECT = storage.connect()

    if CONNECT != False:
        def parse(self, response):
            LIST_CATEGORY = []
            SET_SELECTOR = '.cat-item.col-xs-12.col-md-4.col-sm-6'
            for brickset in response.css(SET_SELECTOR):

                NAME_SELECTOR = 'a ::text'
                URL_PAGE = 'a ::attr(href)'

                if not URL_PAGE in LIST_CATEGORY:
                    LIST_CATEGORY.append(url)
