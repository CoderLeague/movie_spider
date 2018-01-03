# -*- coding: utf-8 -*-
import scrapy

from movie_spider.common import logger


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    def parse(self, response):
        logger.info(str(response.body))
        pass
