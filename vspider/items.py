# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    image_url = scrapy.Field()
    page_url = scrapy.Field()
    iframe_url = scrapy.Field()
    m3u8_url = scrapy.Field()


class S1482Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    image_url = scrapy.Field()
    page_url = scrapy.Field()
    iframe_url = scrapy.Field()
    m3u8_url = scrapy.Field()


