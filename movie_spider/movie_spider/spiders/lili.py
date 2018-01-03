# -*- coding: utf-8 -*-
import scrapy
from movie_spider.items import Liliyy123Item
from movie_spider.common import logger


headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36',
            'Accept'   : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer':'http://www.liliyy123.com/'}

class LiliSpider(scrapy.Spider):
    name = 'lili'
    allowed_domains = ['www.liliyy123.com']
    base_domain = "http://www.liliyy123.com"
    start_urls = [
        'http://www.liliyy123.com/fa/1.html',
        ]
    

    def parse(self, response):
        # 只执行一次，解析起始路径
        
        logger.info(u'开始解析')
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.sub_parse)

    def sub_parse(self, response):
        # 分页执行
        
        # 找出所有影片链接
        detail_link_list = response.xpath(".//div[@class='index-tj-l']/ul/li/a/@href").extract()
        for detail_link in detail_link_list:
            yield scrapy.Request(self.base_domain + detail_link, headers=headers, callback=self.item_parse)
            
        # 找下一页
        temp = response.xpath(".//a[@class='pagelink_a']/@href").extract()
        link = temp[-2]
        tar = link.split("-")[-1]
        tar = tar.split(".")[0]
        if (tar != "1"): # parse next page if exists
            yield scrapy.Request(self.base_domain + link, headers=headers, callback=self.sub_parse)

    def item_parse(self, response):
        # 解析影片介绍页面
        
        link_list   = response.xpath("(.//div[@class='videourl clearfix'])[1]/ul/li/a/@href").extract()
        title_list  = response.xpath("(.//div[@class='videourl clearfix'])[1]/ul/li/a/@title").extract() # 正片
        title       = response.xpath(".//dt[@class='name']/text()").extract()[0]
        protagonist = response.xpath(".//div[@class='ct-c']/dt[1]/text()").extract()
        mtype       = response.xpath(".//div[@class='ct-c']/dt[1]/text()").extract()
        director    = response.xpath(".//div[@class='ct-c']/dt[1]/text()").extract()
        description = response.xpath(".//div[@class='ct-c']/dt[1]/text()").extract()
        show_year   = response.xpath(".//div[@class='ct-c']/dt[1]/text()").extract()
        region      = response.xpath(".//div[@class='ct-c']/dt[1]/text()").extract()
        lang        = response.xpath(".//div[@class='ct-c']/dt[1]/text()").extract()
        cover_url   = response.xpath(".//div[@class='ct-c']/dt[1]/text()").extract()
#         play_url    = response.xpath(".//div[@class='ct-c']/dt[1]/text()").extract()
        
        
#         protagonist = response.xpath().extract()
        
        logger.info(protagonist)
        logger.info("titile %s, link %s " % (str(len(title_list)), str(len(link_list))))
        
        for i in range(len(title_list)):
            logger.info("title index %d" % (i,))
            logger.info("title value %s" % (title_list[i]))
            item = Liliyy123Item()
            
            item['title']       = title
            item['protagonist'] = protagonist
            item['type']        = mtype
            item['director']    = director
            item['description'] = description
            item['show_year']   = show_year
            item['region']      = region
            item['lang']        = lang
            item['cover_url']   = cover_url
            item['play_url']    = self.base_domain + link_list[i]
            
#             logger.info(item)
            yield item


