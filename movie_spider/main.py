#!/usr/bin/env python

from scrapy.cmdline import execute
import rest_spider

# execute(['scrapy', 'crawl', 'vip1905'])

# execute(['scrapy', 'crawl', 'lili'])

execute(['scrapy', 'crawl', 'vipfree'])

# execute(['scrapy', 'crawl', 'quanmin'])



# 下载图片, 更新相对链接
rest_spider.images_loader.master_main()
