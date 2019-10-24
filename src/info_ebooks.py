import scrapy
import datetime
import database.handles.select as select
import database.handles.create as create
from src.MagazineCover import MagazineCover
from scrapy.crawler import CrawlerProcess
from scrapy.pipelines.images import ImagesPipeline

class spider(scrapy.Spider):
#    listEbook = select.all('ebooks')
   start_urls = ['https://sachvui.com/ebook/doi-ngan-dung-ngu-dai-robin-sharma.3020.html']
#    for i in listEbook:
#        start_urls.append(i[2])
   name = "brickset_spider"

   def parse(self, response):
        MAIN_URL = response.url
        #if not MAIN_URL in self.start_urls:
        #MAIN_URL = url_category
        # GET ID SITE
        ID_EBOOK = select._one('id', MAIN_URL, 'url', 'ebooks')

        # GET NAME EBOOK
        NAME_EBOOK = response.css('h1.ebook_title.text-primary::text').get()

        # GET NAME AUTHOR
        NAME_AUTHOR_SELECTOR = '.thong_tin_ebook h5'
        NAME_AUTHOR = ''
        for _author in response.css(NAME_AUTHOR_SELECTOR):
            TEXT__AUTHOR = _author.css('::text').get()
            if 'Tác giả : ' in TEXT__AUTHOR:
                NAME_AUTHOR = TEXT__AUTHOR.replace('Tác giả : ', '')

        # GET DESCRIPTION EBOOK
        DESCRIPTION_TEXT_LIST = response.css('.gioi_thieu_sach.text-justify *').getall()
        DESCRIPTION_TEXT = ' '.join(str(e) for e in DESCRIPTION_TEXT_LIST)

        # GET URL FILE EBOOK
        FILE_EBOOK_SELECTOR = '.thong_tin_ebook .col-md-8 a'
        URL_DOWN_EPUD = ''
        URL_DOWN_MOBI = ''
        URL_DOWN_PDF = ''
        for __file in response.css(FILE_EBOOK_SELECTOR):
            URL_FILE = __file.css('::attr(href)').extract_first()
            if '/download/epub/' in URL_FILE:
                URL_DOWN_EPUD = URL_FILE
            if '/download/mobi/' in URL_FILE:
                URL_DOWN_MOBI = URL_FILE
            if '/download/pdf/' in URL_FILE:
                URL_DOWN_PDF = URL_FILE

        # GET IMAGE URL
        URL_IMAGE = response.css('.img-thumbnail ::attr(src)').get()

        # GET LIST_CHAPTER
#         yield scrapy.Request(
#             MAIN_URL,
#             callback=self.parse_chapter,
#             cb_kwargs=dict(id_ebook=ID_EBOOK)
#         )

        # DOWNLOAD IMAGE
        pub = datetime.datetime.now()
        print('URL ', URL_IMAGE)
        if URL_IMAGE:
            yield MagazineCover(title=NAME_EBOOK, pubDate=pub, file_urls=[URL_IMAGE])


   def parse_chapter(self, response, id_ebook):
        print('Self ', response.url)

        # GET LIST CHAPTER
        CHAPTER_SELECTOR = '#list-chapter > li a'
        for __chapter in response.css(CHAPTER_SELECTOR):
            URL_CHAPTER = __chapter.css('::attr(href)').get()
            NAME_CHAPTER = __chapter.css('::text').get()
            print('URL_CHAPTER',  URL_CHAPTER, NAME_CHAPTER)
            checkExistsChapter = select._one('id', URL_CHAPTER, 'url', 'chapters')
            if checkExistsChapter == False:
               create.insertChapter(NAME_CHAPTER, URL_CHAPTER, id_ebook)

        # NEXT PAGE
        NEXT_PAGE_SELECTOR = '.pagination.pagination-sm li a[rel="next"] ::attr(href)'
        URL_NEXT_PAGE = response.css(NEXT_PAGE_SELECTOR).get()
        if URL_NEXT_PAGE:
            print('Nexxxt >> ', URL_NEXT_PAGE)
            yield scrapy.Request(
                URL_NEXT_PAGE,
                callback=self.parse_chapter,
                cb_kwargs=dict(id_ebook=id_ebook)
            )


process = CrawlerProcess(settings= {
    'LOG_ENABLED': False,
    'LOG_LEVEL': 'ERROR',
    'DOWNLOAD_DELAY': 0.5,
    'ITEM_PIPELINES': {
        'scrapy.pipelines.files.FilesPipeline': 1
    },
    'FILES_STORE': 'files/images/'
})

process.crawl(spider)
process.start()
