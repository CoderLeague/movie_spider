# -*- coding: utf-8 -*-
import scrapy
from movie_spider.common import logger
from bs4 import BeautifulSoup
from movie_spider.items import XiaomaItem


headers = {'User-Agent'      : 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
            'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer'        : 'http://efx6.cn'}

MAX_PAGE_INDEX = 25

class XiaomaSpider(scrapy.Spider):
    name = 'xiaoma'
    allowed_domains = ['efx6.cn']
    base_domain     = 'http://efx6.cn'
    start_urls      = []

    def __init__(self):
        super(XiaomaSpider, self).__init__()
        
        # 初始化 start_urls, 生成电影的地址
        movie_root = u'http://efx6.cn/movie.php?m=http://www.360kan.com/dianying/list.php?cat=all%26pageno={pageno}'
        for i in range(MAX_PAGE_INDEX):
            url = movie_root.format(pageno = str(i+1))
            logger.info(u'初始化网页链接 %s' % url)
            self.start_urls.append(url)

            break

    def parse(self, response, headers=headers):
        #先，解析起始路径 start_urls
        logger.info(u'影片展示页url:%s' % response.url)

        # 找出所有影片链接
        detail_link_list = response.xpath(
            '//div[@class="s-tab-main"]/ul/li/a/@href').extract() # 获取当前页所有详情链接
        detail_list      = response.xpath(
            '//div[@class="s-tab-main"]/ul/li/a').extract()       # 获取当前页所有详情信息

        print(detail_link_list)

        for detail_link, detail in zip(detail_link_list, detail_list):
            url = self.base_domain + detail_link[1:]
            logger.info(u'影片播放页 传参 %s' % url)
            yield scrapy.Request(url = url,
                                 meta={'detail':detail},
                                 headers=headers,
                                 callback=self.item_parse)  # 解析播放页
            break

    def item_parse(self, response):
        # 解析影片介绍及播放页面
        
        url = response.url
        logger.info(u'影片播放页 url:%s' % url)

        detail     = response.meta['detail']  # 图片, 主演, 片名
        soup_meta  = BeautifulSoup(detail, "lxml")
        movie_tag  = soup_meta.find('a')
        title      = movie_tag['title']       # 片名
        img_url    = soup_meta.find('img')['src']                   # 封面图片地址
        score      = soup_meta.find('span', {'class' : 's2'}).text  # 评分
        zhuyan     = soup_meta.find('p', {'class' : 'star'}).text   # 主演

        desc  = response.xpath('//p[@class="item-desc js-close-wrap"]').extract()[0]
        desc  = BeautifulSoup(desc, "lxml").text.replace('\n', '')  # 简介
        
        cover_image = {
            "img"   : img_url,
            "width" : 0,
            "heigh" : 0
            }

        item = XiaomaItem()
        # 站内唯一标识
        item['item_id']       = response.url.split('/')[-1].split('.')[-2]
        # 影片标题
        item['title']         = title
        # 图片信息
        item['cover_images'].append(cover_image)
        # 播放页链接
        item['content_url']   = url
        # 介绍
        item['description']   = desc
        # 播放地址数/片源数量
        item['video_src_cnt'] = 1
        # 图片数量
        item['cover_img_cnt'] = len(item['cover_images'])
        # 主演
        item['actor_list']    = zhuyan.replace('/', ',').replace(' ', ',')
        # 评分
        item['score']         = score
        
        logger.info(u"成功解析: %s url: %s" % (item['title'], item['content_url']))

        yield item

