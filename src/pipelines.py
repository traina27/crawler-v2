# -*- coding: utf-8 -*-
import os
import scrapy
import re
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
import database.handles.update as update

class MyImagesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        URL = request.meta["image_url"]
        TYPE = request.meta["type"]
        URL_SPLIT = re.split("\/.", URL)
        LEN = len(URL_SPLIT)
        return  """{0}/{1}""".format(TYPE, URL_SPLIT[LEN - 1])


    def get_media_requests(self, item, info):
        image_url = item['image_url']
        yield scrapy.Request(image_url, meta={'type': item['type'], 'image_url': image_url})

    def item_completed(self, results, item, info):
        URL_PATH = results[0][1]['path']
        ID = item['id_info_ebook']
        FIELD = 'url_image'
        if item['type'] == 'pdf':
            FIELD = 'url_dw_pdf'
        elif item['type'] == 'epub':
            FIELD = 'url_dw_epub'
        elif item['type'] == 'mobi':
            FIELD = 'url_dw_mobi'
        update.updateInfoEbook(FIELD, URL_PATH, ID)
        return

