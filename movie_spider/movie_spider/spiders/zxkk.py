# -*- coding: utf-8 -*-
import scrapy
from movie_spider.common import logger

headers = {'User-Agent'      : 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
            'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer'        : 'http://www.anyunjun.cn/'}


class ZxkkSpider(scrapy.Spider):
    name = 'zxkk'
    allowed_domains = ['zxkk5.com']
    base_domain = 'http://zxkk5.com'
    start_urls = [
        'http://zxkk5.com/list/?1.html'  # 全部电影第一页
        ]

    def parse(self, response):
        """
        解析电影列表页
        """
        logger.info(u'解析电影列表页:%s' % response.url)
        
        # 找出所有影片链接
        detail_link_list = response.xpath('//div[@class="index-area clearfix"]/ul/li/a/@href').extract() # 获取当前页所有详情链接
        detail_list      = response.xpath('//div[@class="index-area clearfix"]/ul/li/a').extract()       # 获取当前页所有详情信息
        
        for detail_link, detail in zip(detail_link_list, detail_list):
            yield scrapy.Request(url = detail_link,
                                 meta={'detail':detail},
                                 headers=headers,
                                 callback=self.item_parse)  # 解析单页页
        
        print detail_list

