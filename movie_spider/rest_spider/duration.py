# -*- coding: utf-8 -*-
# 采用selenium获取ajax数据
# 主要获取视频流的时间
#
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

url = 'http://www.efx6.cn/play.php?play=aHR0cDovL3d3dy4zNjBrYW4uY29tL20vZjZ2bVloSDJRMFQ3VGguaHRtbA=='

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# driver = webdriver.Firefox( executable_path='/home/codenewman/workspace/github/movie_spider/movie_spider/selenium_driver/geckodriver')

firefox_binary  = FirefoxBinary(r'/usr/lib/firefox/firefox')
executable_path = os.path.join(base_dir, 'drivers', 'geckodriver')
driver = webdriver.Firefox( firefox_binary  = firefox_binary,
                            executable_path = executable_path
                           )
driver.get(url)
assert u'铁拳' in driver.title
# elem = driver.find_element_by_name('wd')
elem = driver.find_element_by_xpath('//*[@id="dianshijuid"]/div/div/a')
print elem
# elem.clear()
# elem.send_keys(u'网络爬虫')
elem.click()
time.sleep(10)
elem = driver.find_element_by_xpath('/html/body/div[1]/section/div[1]/div/div[5]/div/div[2]/button[3]')
print elem
elem.click()
time.sleep(10)

# driver.close()