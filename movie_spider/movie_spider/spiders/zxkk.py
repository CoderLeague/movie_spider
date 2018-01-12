# -*- coding: utf-8 -*-
import scrapy
from movie_spider.common import logger
from movie_spider.items import ZxkkItem
from bs4 import BeautifulSoup

headers = {'User-Agent'      : 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
            'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer'        : 'http://zxkk5.com/'}


class ZxkkSpider(scrapy.Spider):
    name = 'zxkk'
    allowed_domains = ['zxkk5.com']
    base_domain = 'http://zxkk5.com'
    start_urls = [
        'http://zxkk5.com/list/?1.html'  # 全部电影的第一页
        ]

    def __init__(self):
        """
        重写初始化, 引入headers
        """
        super(ZxkkSpider, self).__init__()
    
    
    def parse(self, response):
        """
        解析电影列表页
        """
        logger.info(u'解析电影列表页:%s' % response.url)
        
        # 找出所有影片链接
        detail_link_list = response.xpath('//div[@class="index-area clearfix"]/ul/li/a/@href').extract() # 获取当前页所有详情链接
        detail_list      = response.xpath('//div[@class="index-area clearfix"]/ul/li/a').extract()       # 获取当前页所有详情信息
         
        for detail_link, detail in zip(detail_link_list, detail_list):
            yield scrapy.Request(url = self.base_domain + detail_link,
                                 headers=headers,
                                 meta={'detail':detail},
                                 callback=self.item_parse)  # 解析单页页
            break
        
        # 超出下一页按钮
        next_page_list = response.xpath('//div[@class="page mb clearfix"]/a').extract() # 获取当前页所有详情链接
          
        for button_item in next_page_list:
            soup = BeautifulSoup(button_item, "lxml")
            link_list = soup.findAll('a')
  
            for tag_a in link_list:
                if u'>' == tag_a.text :
                    link = self.base_domain + tag_a['href']
                    logger.info(u"下一页链接: %s" % link)
                    yield scrapy.Request(url = link,
                                         callback=self.parse)


    def item_parse(self, response):
        """
        解析影片播放详情页
        """
        logger.info(u'解析影片播放详情页: %s' % response.url)

        # 解析影片介绍页面
        logger.info(u'解析影片介绍页面: %s' % response.url)

        detail     = response.meta['detail']  # 图片, 片名
        soup_meta  = BeautifulSoup(detail, "lxml")
        title      = soup_meta.find('p', {'class' : 'name'}).text      #片名
        img_url    = soup_meta.find('img')['data-original']            # 封面图片地址
        
        actors     = soup_meta.findAll('p', {'class' : 'actor'})
        actor_list    = actors[0].text     # 演员表
        item_catagory = actors[1].text     # 影片类型
        show_year     = actors[2].text.split('/')[0]     # 上映年份
        region        = actors[2].text.split('/')[1]     # 所属地区

# -------------------------------------------------- #

        director   = response.xpath('//div[@class="ct-c"]/dl/dd[1]/a/text()').extract()  # 导演
        if len(director) == 0:
            director = ''
        else:
            director = director[0]

        lang   = response.xpath('//div[@class="ct-c"]/dl/dd[4]/text()').extract()        # 影片语言
        if len(lang) == 0:
            lang = ''
        else:
            lang = lang[0]

        play_item  = response.xpath('//div[@class="playfrom tab8 clearfix"]/ul/li').extract()
        video_src_list = len(play_item)  # 播放源数量
        
        desc  = response.xpath('////div[@name="ee"]').extract()[0]
        desc  = BeautifulSoup(desc, "lxml").text.replace('\n', '')  # 简介
        
        cover_image = {
            "img"   : img_url,
            "width" : 0,
            "heigh" : 0
            }

        item = ZxkkItem()
        # 站内唯一标识
        item['item_id']       = response.url.split('?')[-1].split('.')[-2]
        # 影片标题
        item['title']         = title
        # 图片信息
        item['cover_images'].append(cover_image)
        # 播放页链接
        item['content_url']   = response.url
        # 介绍
        item['description']   = desc
        # 播放地址数/片源数量
        item['video_src_cnt'] = video_src_list
        # 图片数量
        item['cover_img_cnt'] = len(item['cover_images'])
        # 导员
        item['director']      = director
        # 演员表
        item['actor_list']    = actor_list
        # 上映年份
        item['show_year']     = show_year
        # 影片类型
        item['item_catagory'] = item_catagory
        # 影片类型
        item['sub_channel']   = item_catagory
        # 上映年份
        item['region']        = region
        
        logger.info(u"成功解析: %s url: %s" % (item['title'], item['content_url']))

        yield item