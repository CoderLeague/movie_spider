# -*- coding: utf-8 -*-
import scrapy
from movie_spider.common import logger
from bs4 import BeautifulSoup
from movie_spider.items import QuanminItem

headers = {'User-Agent'      : 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36',
            'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer'        : 'http://www.anyunjun.cn/'}

class QuanminSpider(scrapy.Spider):
    name = 'quanmin'
    allowed_domains = ['www.anyunjun.cn']
    base_domain = 'http://www.anyunjun.cn'
    start_urls = [
        'http://www.anyunjun.cn/'
        ]

    def parse(self, response):
        # 只执行一次，解析起始路径 start_urls
        
        logger.info(u'开始解析全民影院的视频信息')
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.sub_parse)

    def sub_parse(self, response):
        
        # 分页执行

        # 找出所有影片链接
        detail_link_list = response.xpath('//div[@class="item"]/ul/div/a/@href').extract() # 获取当前页所有详情链接
        detail_list      = response.xpath('//div[@class="item"]/ul/div/a').extract()       # 获取当前页所有详情信息
             
        for detail_link, detail in zip(detail_link_list, detail_list):
            yield scrapy.Request(url = self.base_domain + detail_link[1:],
                                 meta={'detail':detail},
                                 headers=headers,
                                 callback=self.item_parse)  # 解析单页页面

        # 寻找下一页按钮
        next_page_list = response.xpath('/html/body/div[2]/div/div[3]/div[3]/ul/li/a').extract()

        for button_item in next_page_list:
            if u'下一页' in button_item :
                logger.info(u'------------正在翻页------------')
                soup = BeautifulSoup(button_item, "lxml")
                link = soup.find('a')['href']
                link = self.base_domain + '/' + link
                logger.info(link)
                yield scrapy.Request(url = link, headers=headers, callback=self.sub_parse)


    def item_parse(self, response):
        # 解析影片介绍及播放页面
        
        detail = response.meta['detail']
        soup = BeautifulSoup(detail, "lxml")
        values = soup.find('a')
        cover_image = {
            "img"   : values['src'],
            "width" : 0,
            "heigh" : 0
            }
        video_src_list = response.xpath('//*[@id="playlist1"]/ul/li').extract()
        
        item = QuanminItem()
        # 站内唯一标识
        item['item_id']       = response.url.split('/')[-1].split('.')[-2]
        # 影片标题
        item['title']         = values['title']
        # 图片信息
        item['cover_images'].append(cover_image)
        # 播放页链接
        item['content_url']   = response.url
        # 介绍
        item['description']   = response.xpath('//*[@id="list3"]/div/div/text()').extract()[-1]
        # 播放地址数
        item['video_src_cnt'] = len(video_src_list)
        # 图片数量
        item['cover_img_cnt'] = 1

        logger.info(item['title'])
        logger.info(item['description'])
        
        yield item

