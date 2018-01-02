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


class Vip1905Item(scrapy.Item):
    name = scrapy.Field()  # 名字
    data_id = scrapy.Field()  # 数据ID
    score = scrapy.Field()  # 评分
    url = scrapy.Field()  # 播放链接
    intro = scrapy.Field()  # 介绍
    tag_hover = scrapy.Field()  # 标签
    protagonist = scrapy.Field()  # 主演
    plot = scrapy.Field()  # 剧情
