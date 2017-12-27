# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CollectipsIpItem(scrapy.Item):
    IP              = scrapy.Field()
    PORT            = scrapy.Field()
    POSITION        = scrapy.Field()
    TYPE            = scrapy.Field()
    SPEED           = scrapy.Field()
    LAST_CHECK_TIME = scrapy.Field()