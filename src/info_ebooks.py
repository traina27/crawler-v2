import scrapy
import datetime
import database.handles.select as select
import database.handles.create as create
from src.Item import ImageItem
from scrapy.crawler import CrawlerProcess

class spider(scrapy.Spider):
   listEbook = select.all('ebooks')
   start_urls = []
   for i in listEbook:
       start_urls.append(i[2])
   name = "brickset_spider"
   STT = 0

   def parse(self, response):
        MAIN_URL = response.url
        spider.STT = spider.STT + 1
        print('Page: ', spider.STT, MAIN_URL)

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
        _DESCRIPTION_TEXT = DESCRIPTION_TEXT.replace('"', '\"')
        __DESCRIPTION_TEXT = _DESCRIPTION_TEXT.replace("'", "\'")
        ___DESCRIPTION_TEXT = __DESCRIPTION_TEXT.replace("“", "")
        ____DESCRIPTION_TEXT = ___DESCRIPTION_TEXT.replace("”", "")
        checkExistsInfo = select._one('id', MAIN_URL, 'url', 'info_ebooks')
        if checkExistsInfo == False:
           yield create.insertInfoBook(ID_EBOOK, MAIN_URL, NAME_EBOOK, ____DESCRIPTION_TEXT, NAME_AUTHOR)

        IDInfo = select._one('id', MAIN_URL, 'url', 'info_ebooks')
        if IDInfo:
            # GET URL FILE EBOOK
            FILE_EBOOK_SELECTOR = '.thong_tin_ebook .col-md-8 a'
            URL_DOWN_EPUB = ''
            URL_DOWN_MOBI = ''
            URL_DOWN_PDF = ''
            for __file in response.css(FILE_EBOOK_SELECTOR):
                URL_FILE = __file.css('::attr(href)').extract_first()
                if '/download/epub/' in URL_FILE:
                    URL_DOWN_EPUB = URL_FILE
                if '/download/mobi/' in URL_FILE:
                    URL_DOWN_MOBI = URL_FILE
                if '/download/pdf/' in URL_FILE:
                    URL_DOWN_PDF = URL_FILE

            # GET IMAGE URL
            URL_IMAGE = response.css('.img-thumbnail ::attr(src)').get()

            # GET LIST_CHAPTER
            yield scrapy.Request(
                MAIN_URL,
                callback=self.parse_chapter,
                cb_kwargs=dict(id_ebook=ID_EBOOK)
            )

            #DOWNLOAD IMAGE
            if URL_IMAGE:
                getURL = select._one('url_image', IDInfo, 'id', 'info_ebooks')
                if not getURL:
                    yield ImageItem(type='images', image_url=URL_IMAGE, id_info_ebook=IDInfo)

            # DOWNLOAD PDF
            if URL_DOWN_PDF:
                yield scrapy.Request(
                    URL_DOWN_PDF,
                    callback=self.parse_file,
                    cb_kwargs=dict(type='pdf',IDInfo=IDInfo)
                )

            # DOWNLOAD EPUB
            if URL_DOWN_EPUB:
                yield scrapy.Request(
                    URL_DOWN_EPUB,
                    callback=self.parse_file,
                    cb_kwargs=dict(type='epub',IDInfo=IDInfo)
                )

            # DOWNLOAD MOBI
            if URL_DOWN_MOBI:
                yield scrapy.Request(
                    URL_DOWN_MOBI,
                    callback=self.parse_file,
                    cb_kwargs=dict(type='mobi',IDInfo=IDInfo)
                )


   def parse_chapter(self, response, id_ebook):
        # GET LIST CHAPTER
        CHAPTER_SELECTOR = '#list-chapter > li a'
        for __chapter in response.css(CHAPTER_SELECTOR):
            URL_CHAPTER = __chapter.css('::attr(href)').get()
            NAME_CHAPTER = __chapter.css('::text').get()
            checkExistsChapter = select._one('id', URL_CHAPTER, 'url', 'chapters')
            if checkExistsChapter == False:
               create.insertChapter(NAME_CHAPTER, URL_CHAPTER, id_ebook)

        # NEXT PAGE
        NEXT_PAGE_SELECTOR = '.pagination.pagination-sm li a[rel="next"] ::attr(href)'
        URL_NEXT_PAGE = response.css(NEXT_PAGE_SELECTOR).get()
        if URL_NEXT_PAGE:
            yield scrapy.Request(
                URL_NEXT_PAGE,
                callback=self.parse_chapter,
                cb_kwargs=dict(id_ebook=id_ebook)
            )

   def parse_file(self, response, type, IDInfo):
        if response.url:
            getURL = select._one('url_dw_{0}'.format(type), IDInfo, 'id', 'info_ebooks')
            if not getURL:
                yield ImageItem(type=type, image_url=response.url, id_info_ebook=IDInfo)


process = CrawlerProcess(settings= {
    'LOG_ENABLED': False,
    'LOG_LEVEL': 'INFO',
    'DOWNLOAD_DELAY': 5,
    'ITEM_PIPELINES': {
        'src.pipelines.MyImagesPipeline': 1
    },
    'FILES_STORE': 'files/',
    'DOWNLOAD_MAXSIZE': 0,
    'DOWNLOAD_TIMEOUT': 1200
})

process.crawl(spider)
process.start()
