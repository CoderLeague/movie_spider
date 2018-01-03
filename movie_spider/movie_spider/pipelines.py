# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from movie_spider.common import logger


class MovieSpiderPipeline(object):
    def process_item(self, item, spider):
        logger.info(str(item))

        return item
