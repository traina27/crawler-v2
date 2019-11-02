import scrapy
import database.handles.select as select
import database.handles.create as create
from scrapy.crawler import CrawlerProcess

class spider(scrapy.Spider):
    listChapter = select.all('chapters')
    start_urls = []
    for i in listChapter:
        start_urls.append(i[2])
    name = "brickset_spider"
    STT = 0

    def parse(self, response):
        URL_SITE = response.url
        spider.STT = spider.STT + 1
        print('Page content ', spider.STT, URL_SITE)
        # GET ID SITE
        ID_CHAPTER = select._one('id', URL_SITE, 'url', 'chapters')

        SET_SELECTOR = '.doc-online p'
        CONTENT = ''
        for brickset in response.css(SET_SELECTOR):
            TEXT = brickset.css('::text').getall()
            _TEXT = ' '.join(str(e) for e in TEXT)
            __TEXT = str(_TEXT).replace('"', '\"')
            ____TEXT= __TEXT.replace("'", "")
            _______TEXT = ____TEXT.replace("“", "")
            ___________TEXT = _______TEXT.replace("”", "")
            CONTENT = '{0} <p>{1}</p>'.format(CONTENT, ___________TEXT)

        checkExistsContent = select._one('id', ID_CHAPTER, 'chapter_id', 'contents')
        if checkExistsContent == False:
            create.insertContent(ID_CHAPTER, CONTENT)

process = CrawlerProcess(settings={
    'LOG_ENABLED': False,
    'LOG_LEVEL': 'ERROR',
    'DOWNLOAD_FAIL_ON_DATALOSS': False,
    'DOWNLOAD_DELAY': 0.5,

})

process.crawl(spider)
process.start()
