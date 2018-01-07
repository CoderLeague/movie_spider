# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import time


class CollectipsIpItem(scrapy.Item):
    """
    系统自动生成
    """
    IP              = scrapy.Field()
    PORT            = scrapy.Field()
    POSITION        = scrapy.Field()
    TYPE            = scrapy.Field()
    SPEED           = scrapy.Field()
    LAST_CHECK_TIME = scrapy.Field()


class BaseMovieItem(scrapy.Item):
    """
    基本抓取
    """
    source           = scrapy.Field()  #     一级抓取分类
    sub_source       = scrapy.Field()  #     二级抓取分类
    site_url         = scrapy.Field()  #     网站域名
    director         = scrapy.Field()  #     导演
    actor_list       = scrapy.Field()  #     演员表
    show_year        = scrapy.Field()  #     上映年份
    item_catagory    = scrapy.Field()  #     影片类型
    duration         = scrapy.Field()  #     影片时长
    item_id          = scrapy.Field()  #     站内唯一ID
    eposide_num      = scrapy.Field()  #     连戏剧更新集数
    free_tag         = scrapy.Field()  #     是否免费
    title            = scrapy.Field()  #     标题
    description      = scrapy.Field()  #     描述(正文)
    cover_images     = scrapy.Field()  #     图片
    cover_img_cnt    = scrapy.Field()  #     图片数目
    sub_title        = scrapy.Field()  #     单集简介
    publish_date     = scrapy.Field()  #     上传时间
    last_update_time = scrapy.Field()  #     抓取时间
    video_src_cnt    = scrapy.Field()  #     片源数量
    score            = scrapy.Field()  #     电影评分
    content_url      = scrapy.Field()  #     播放页链接
    lang             = scrapy.Field()  #     语言语种
    region           = scrapy.Field()  #     所属地区
    type             = scrapy.Field()  #     一级形式分类
    sub_type         = scrapy.Field()  #     二级形式分类
    channel          = scrapy.Field()  #     一级内容业务分类
    sub_channel      = scrapy.Field()  #     二级内容业务分类
    
    def __init__(self):
        super(BaseMovieItem, self).__init__()
        
        self['source']        =      "c.l.a.webview.msite.video"
        self['sub_source']    =      ""
        self['site_url']      =      ""
        self['director']      =      ""
        self['actor_list']    =      ""
        self['show_year']     =      0
        self['item_catagory'] =      ""
        self['duration']      =      ""
        self['item_id']       =      ""
        self['eposide_num']   =      ""
        self['free_tag']      =      "付费"      
        self['title']         =      ""
        self['description']   =      ""
        self['cover_images']  =      []
        self['cover_img_cnt'] =      ""
        self['sub_title']     =      ""
        self['publish_date']  =      0
        self['last_update_time']  =  0
        self['video_src_cnt'] =      ""
        self['score']         =      ""
        self['content_url']   =      ""
        self['lang']          =      ""
        self['region']        =      ""
        self['type']          =      ""
        self['sub_type']      =      "video"
        self['channel']       =      "movie"
        self['sub_channel']   =      ""


class VipfreeItem(BaseMovieItem):
    """
    唯爱痞电影网
    """

    def __init__(self):
        super(VipfreeItem, self).__init__()
        self['sub_source']    =      "weiaipidianyingwang"
        self['site_url']      =      'vip-free.com'
        self['free_tag']      =      "免费"
        self['last_update_time']  =  int(time.time())


class QuanminItem(BaseMovieItem):
    """
    全民影院
    """
    def __init__(self):
        super(VipfreeItem, self).__init__()
        self['sub_source']    =      "quanminyingyuan"
        self['site_url']      =      'www.anyunjun.cn'
        self['free_tag']      =      "免费"
        self['last_update_time']  =  int(time.time())


class Liliyy123Item(BaseMovieItem):
    """
    莉莉影院
    """
    def __init__(self):
        super(VipfreeItem, self).__init__()
        self['sub_source']    =      "liliyingshi"
        self['site_url']      =      'liliyy123.com'
        self['free_tag']      =      "免费"
        self['last_update_time']  =  int(time.time())


class Vip1905Item(scrapy.Item):
    name = scrapy.Field()  # 名字
    data_id = scrapy.Field()  # 数据ID
    score = scrapy.Field()  # 评分
    url = scrapy.Field()  # 播放链接
    intro = scrapy.Field()  # 介绍
    tag_hover = scrapy.Field()  # 标签
    protagonist = scrapy.Field()  # 主演
    plot = scrapy.Field()  # 剧情
