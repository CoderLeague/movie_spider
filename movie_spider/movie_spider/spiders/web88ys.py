# -*- coding: utf-8 -*-
import scrapy


class movie88ysSpider(scrapy.Spider):
    name = '88ys'
    allowed_domains = ['www.88ys.tv']
    start_urls = ['http://www.88ys.tv/']

    def parse(self, response):
        print response.url
        pass
