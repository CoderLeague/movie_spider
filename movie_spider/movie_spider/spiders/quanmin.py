# -*- coding: utf-8 -*-
import scrapy
from movie_spider.common import logger
from bs4 import BeautifulSoup
from movie_spider.items import QuanminItem

headers = {'User-Agent'      : 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
            'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer'        : 'http://www.anyunjun.cn/'}

class QuanminSpider(scrapy.Spider):
    name = 'quanmin'
    allowed_domains = ['www.anyunjun.cn']
    base_domain = 'http://www.anyunjun.cn'
    start_urls = [
#         'http://www.anyunjun.cn/list/c/dianying/cat/all/area/all/rank/createtime.html',  # 最新电影
        'http://www.anyunjun.cn/list/c/dianying/cat/all/area/all.html',                  # 全部电影
        ]

    def parse(self, response):
        #先，解析起始路径 start_urls
        logger.info(u'解析页面地址url:%s' % response.url)


        # 找出所有影片链接
        detail_link_list = response.xpath(
            '//html/body/section/div[3]/div/div[1]/div/div/ul[2]/li/a/@href').extract() # 获取当前页所有详情链接
        detail_list      = response.xpath(
            '//html/body/section/div[3]/div/div[1]/div/div/ul[2]/li/a').extract()         # 获取当前页所有详情信息
              
        for detail_link, detail in zip(detail_link_list, detail_list):
            yield scrapy.Request(url = detail_link,
                                 meta={'detail':detail},
                                 headers=headers,
                                 callback=self.item_parse)  # 解析单页页


#         if detail_link_list or len(detail_link_list) == 0:
#             # 下一页按钮一直会在, 但是可能只有广告, 这里针对电影数做个判断
#             return

        # 寻找下一页按钮
        next_page_list = response.xpath('//div[@class="paging"]').extract()
          
        for button_item in next_page_list:
            soup = BeautifulSoup(button_item, "lxml")
            link_list = soup.findAll('a')
              
            for tag_a in link_list:
                if u'下一页' in tag_a.text :
                    link = self.base_domain + tag_a['href']
                    logger.info(u"下一页链接: %s" % link)
                    yield scrapy.Request(url = link, headers=headers, callback=self.parse)


    def item_parse(self, response):
        # 解析影片介绍及播放页面

        detail     = response.meta['detail']  # 图片, 主演, 片名
        soup_meta  = BeautifulSoup(detail, "lxml")
        movie_tag  = soup_meta.find('a')
        title      = movie_tag['title']  # 片名
#         href       = movie_tag['href']   # 链接  直接调用response.url
        img_url    = soup_meta.find('img')['src']  # 封面图片地址
        year       = soup_meta.find('span', {'class' : 'hint'}).text   # 年份
        zhuyan     = soup_meta.find('p', {'class' : 'star'}).text   # 主演

        play_item = response.xpath('//p[@class="vspy"]/a').extract()
        video_src_list = len(play_item)  # 播放源数量

        tyyp   = response.xpath('/html/body/div[1]/section/div[1]/div/div[5]/div/h3[1]/span').extract()[0]
        tyyp   = BeautifulSoup(tyyp, "lxml").text.replace(' ', '')  # 影片分类
        
        desc  = response.xpath('//p[@class="item-desc js-close-wrap"]').extract()[0]
        desc  = BeautifulSoup(desc, "lxml").text.replace('\n', '')  # 简介
        
        cover_image = {
            "img"   : img_url,
            "width" : 0,
            "heigh" : 0
            }
        
        # 数视频源数量        
#         video_src_list = response.xpath('//p[@class="vspy"]').extract()
#         logger.info(video_src_list)

        item = QuanminItem()
        # 站内唯一标识
        item['item_id']       = response.url.split('/')[-1].split('.')[-2]
        # 影片标题
        item['title']         = title
        # 图片信息
        item['cover_images'].append(cover_image)
        # 播放页链接
        item['content_url']   = response.url
        # 介绍
        item['description']   = desc  # response.xpath('//*[@id="list3"]/div/div/text()').extract()[-1]
        # 播放地址数/片源数量
        item['video_src_cnt'] = video_src_list
        # 图片数量
        item['cover_img_cnt'] = len(item['cover_images'])
        # 主演
        item['actor_list']    = zhuyan.replace('/', ',').replace(' ', ',')
        # 上映年份
        item['show_year']     = year
        # 影片类型
        item['item_catagory'] = tyyp
        
        logger.info(u"成功解析: %s url: %s" % (item['title'], item['content_url']))

        yield item

