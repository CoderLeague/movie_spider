# -*- coding: utf-8 -*-

# Created on 2018年1月2日
# 全局配置信息
# @author: zhongliang


import os
import sys

# 项目全局根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# 默认图片文件存放根目录
IMAGE_ROOT = "/home/op/files/capture_ym"

# 线上数据库配置信息
ONLINE_MONGODB_SERVER     = "172.17.33.176"
ONLINE_MONGODB_PORT       = 30001
ONLINE_MONGODB_DB         = "feed"
ONLINE_MONGODB_COLLECTION = "capture_mysite_video"
ONLINE_MONGODB_USERNAME   = "liquid"
ONLINE_MONGODB_PASSWORD   = "n3tw0rk"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
   
# 测试数据库配置信息
ONLINE_MONGODB_SERVER     = "127.0.0.1"
ONLINE_MONGODB_PORT       = 27017
ONLINE_MONGODB_DB         = "local"
ONLINE_MONGODB_COLLECTION = "capture_mysite_video"
ONLINE_MONGODB_USERNAME   = None
ONLINE_MONGODB_PASSWORD   = None
       
# 测试图片文件存放根目录
IMAGE_ROOT = os.path.join(BASE_DIR, 'data', 'images')

