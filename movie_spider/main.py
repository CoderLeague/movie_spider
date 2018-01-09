#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import rest_spider
from movie_spider.common import logger

# 莉莉影视
# execute(['scrapy', 'crawl', 'lili'])

# 唯爱痞电影网
# execute(['scrapy', 'crawl', 'vipfree'])

# 全民影院
# execute(['scrapy', 'crawl', 'quanmin'])

# 小马影院
execute(['scrapy', 'crawl', 'xiaoma'])



# 下载图片, 更新相对链接
rest_spider.images_loader.master_main()

logger.info(u'全部任务执行完毕')
