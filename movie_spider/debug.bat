@echo 创建项目
@echo scrapy startproject movie_spider

@echo 创建应用
@echo scrapy genspider vip1905 vip.1905.com

@echo 执行爬虫
scrapy crawl vip1905
