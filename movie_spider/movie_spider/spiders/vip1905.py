# -*- coding: utf-8 -*-
import scrapy

from movie_spider.common import logger


class Vip1905Spider(scrapy.Spider):
    name = 'vip1905'
    allowed_domains = ['vip.1905.com']
    start_urls = ['http://vip.1905.com/']

    def parse(self, response):
        logger.info(str(str(response.url)))
        print('DEBUG DEBUG DEBUG:',str(response.body))
        pass
