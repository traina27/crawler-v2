import scrapy
import database.handles.select as select
import database.handles.create as create
from scrapy.crawler import CrawlerProcess

class spider(scrapy.Spider):
    listSite = select.all('sites')
    start_urls = []
    for i in listSite:
        start_urls.append(i[2])
    name = "brickset_spider"

    def parse(self, response):
        URL_SITE = response.url
        # GET ID SITE
        ID_SITE = select._one('id', URL_SITE, 'url', 'sites')

        SET_SELECTOR = '.cat-item.col-xs-12.col-md-4.col-sm-6'
        for brickset in response.css(SET_SELECTOR):

            NAME_CATEGORY = brickset.css('a ::text').extract_first()
            URL_CATEGORY = brickset.css('a ::attr(href)').extract_first()
            checkExistsCategory = select._one('id', URL_CATEGORY, 'url', 'categories')
            if checkExistsCategory == False:
                create.insertCategory(NAME_CATEGORY, URL_CATEGORY, ID_SITE)

process = CrawlerProcess(settings={
    'LOG_ENABLED': False,
    'LOG_LEVEL': 'ERROR'

})

process.crawl(spider)
process.start()
