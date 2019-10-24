import scrapy

class MagazineCover(scrapy.Item):
    title = scrapy.Field()
    pubDate = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    image_urls=scrapy.Field()
    images=scrapy.Field()

    def file_path(self, request, response=None, info=None):
        print('>>>>> FILISSS')
        image_guid = request.meta['model'][0]
        log.msg(image_guid, level=log.DEBUG)
        return 'full/%s' % (image_guid)
