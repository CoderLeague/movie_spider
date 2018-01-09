#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import rest_spider
from movie_spider.common import logger

# execute(['scrapy', 'crawl', 'vip1905'])

# execute(['scrapy', 'crawl', 'lili'])

# execute(['scrapy', 'crawl', 'vipfree'])

execute(['scrapy', 'crawl', 'quanmin'])



# 下载图片, 更新相对链接
# rest_spider.images_loader.master_main()


logger.info(u'全部任务执行完毕')
