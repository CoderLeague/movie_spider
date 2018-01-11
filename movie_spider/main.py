#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from scrapy.cmdline import execute
from movie_spider.common import logger
from rest_spider import images_loader

# 莉莉影视
# execute(['scrapy', 'crawl', 'lili'])

# 唯爱痞电影网
# execute(['scrapy', 'crawl', 'vipfree'])

# 全民影院
# execute(['scrapy', 'crawl', 'quanmin'])

# 小马影院
# execute(['scrapy', 'crawl', 'xiaoma'])

# 在线看看
execute(['scrapy', 'crawl', 'zxkk'])

# 下载图片, 更新相对链接
images_loader.master_main()
 
logger.info(u'全部任务执行完毕')
