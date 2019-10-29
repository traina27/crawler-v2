import scrapy
from scrapy.item import Item, Field

class ImageItem(Item):
    type = Field()
    image_urls = Field()
    images = Field()
