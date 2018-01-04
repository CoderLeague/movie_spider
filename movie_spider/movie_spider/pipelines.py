# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from movie_spider.common import logger


class MovieSpiderPipeline(object):
    def process_item(self, item, spider):
#         logger.info(str(item))
        return item



class MongoDBPipeline(object):
    def __init__(self):
        connection=pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
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
            log.msg('question added to mongodb database!',
                    level=log.DEBUG,spider=spider)
            
        logger.info(u'存入数据成功')
        return item


