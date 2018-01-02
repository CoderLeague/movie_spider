# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieSpiderItem(scrapy.Item):
    """
    电影的基本信息
    """
    pass


class BaseMovieItem(MovieSpiderItem):
    """
    基本赚取
    """
    title        = scrapy.Field()  # 片名
    protagonist  = scrapy.Field()  # 主演
    type         = scrapy.Field()  # 类型
    director     = scrapy.Field()  # 导演
    description  = scrapy.Field()  # 简介
    show_year    = scrapy.Field()  # 年份
    region       = scrapy.Field()  # 地区
    lang         = scrapy.Field()  # 语言



class Liliyy123Item(BaseMovieItem):
    """
    莉莉影院
    """
    alias     = scrapy.Field()  # 别名
    cover_url = scrapy.Field()  # 封面链接
    play_url  = scrapy.Field()  # 页面链接


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
