# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
# from scrapy import log
from movie_spider.common import logger
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


# class MovieSpiderPipeline(object):
#     def process_item(self, item, spider):
# #         logger.info(str(item))
#         return item



class MongoDBPipeline(object):
    def __init__(self):        
        connection=pymongo.MongoClient(
            host     = settings['MONGODB_SERVER'],
            port     = settings['MONGODB_PORT'],
            username = settings['MONGODB_USERNAME'],
            password = settings['MONGODB_PASSWORD']
        )
        db=connection[settings['MONGODB_DB']]
        self.collection=db[settings['MONGODB_COLLECTION']]


    def process_item(self,item,spider):
        valid=True
        for data in item:
            if not data:
                valid=False
                raise DropItem('Missing{0}!'.format(data))
        if valid:
            self.collection.insert(dict(item))
#             log.msg('question added to mongodb database!',
#                     level=log.DEBUG,spider=spider)
            
        logger.info(u'存入数据成功')
        return item


class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info): #下载图片
        for cover_image in item['cover_images']:
            yield Request(cover_image['img'],
                          meta={'cover_image':cover_image,
                                }
                          ) #添加meta是为了下面重命名文件名使用

    def file_path(self,request,response=None,info=None):
        item=request.meta['item']   #通过上面的meta传递过来item
        index=request.meta['index'] #通过上面的index传递过来列表中当前下载图片的下标

        #图片文件名，item['carname'][index]得到汽车名称，request.url.split('/')[-1].split('.')[-1]得到图片后缀jpg,png
        image_guid = item['carname'][index]+'.'+request.url.split('/')[-1].split('.')[-1]
        #图片下载目录 此处item['country']即需要前面item['country']=''.join()......,否则目录名会变成\u97e9\u56fd\u6c7d\u8f66\u6807\u5fd7\xxx.jpg
        filename = u'full/{0}/{1}'.format(item['country'], image_guid) 
        return filename


