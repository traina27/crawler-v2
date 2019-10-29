# -*- coding: utf-8 -*-
import os
import scrapy
import re
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse

class MyImagesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        URL = request.meta["image_url"]
        TYPE = request.meta["type"]
        URL_SPLIT = re.split("\/.", URL)
        LEN = len(URL_SPLIT)
        return  """{0}/{1}""".format(TYPE, URL_SPLIT[LEN - 1])


    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'type': item['type'], 'image_url': image_url})

    def item_completed(self, results, item, info):
        print('lllll', results)
        return results

