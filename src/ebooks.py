import scrapy
import database.handles.select as select
import database.handles.create as create
from scrapy.crawler import CrawlerProcess

class spider(scrapy.Spider):
   listCategories = select.all('categories')
   start_urls = []
   for i in listCategories:
       start_urls.append(i[2])
   name = "brickset_spider"
   STT = 0
   STT_EBOOK = 0

   def parse(self, response, url_category = False):
       MAIN_URL = response.url
       if not MAIN_URL in self.start_urls:
            MAIN_URL = url_category
       spider.STT = spider.STT + 1
#        print('Ebook ', spider.STT, MAIN_URL)
       # GET ID SITE
       ID_CATEGORY = select._one('id', MAIN_URL, 'url', 'categories')

       SET_SELECTOR = '.col-xs-6.col-md-3.col-sm-3.ebook'
       for brickset in response.css(SET_SELECTOR):
           URL_EBOOK = brickset.css('a ::attr(href)').extract_first()
           checkExistsEbook = select._one('id', URL_EBOOK, 'url', 'ebooks')
           spider.STT_EBOOK = spider.STT_EBOOK + 1
           print('Ebook ', spider.STT_EBOOK, URL_EBOOK)
           if checkExistsEbook == False:
               create.insertEbook(ID_CATEGORY, URL_EBOOK)

       NEXT_PAGE_SELECTOR = '.pagination.pagination-sm li a[rel="next"] ::attr(href)'
       URL_NEXT_PAGE = response.css(NEXT_PAGE_SELECTOR).extract_first()
       if URL_NEXT_PAGE:
           yield scrapy.Request(
               response.urljoin(URL_NEXT_PAGE),
               callback=self.parse,
               cb_kwargs=dict(url_category=MAIN_URL)
           )

process = CrawlerProcess(settings= {
    'LOG_ENABLED': False,
    'LOG_LEVEL': 'ERROR',
    'DOWNLOAD_DELAY': 0.5,
    'DOWNLOAD_FAIL_ON_DATALOSS': False

})

process.crawl(spider)
process.start()
