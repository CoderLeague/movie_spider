# -*- coding: utf-8 -*-
import os
import json

# 设置电影类型 单例对象
SUB_CHANNEL = None

# 设置网站信息 单例对象
MOVIE_URL   = None

def sub_channel_format(fuzzy_str):
    global SUB_CHANNEL
    
    if SUB_CHANNEL == None:
        sub_channel_file = os.path.join('data', 'sub_channel.json')
        
        with open(sub_channel_file) as f:
            SUB_CHANNEL = json.load(f)
    
#     for v in SUB_CHANNEL.values:
#         if v 

    print SUB_CHANNEL



if __name__ == '__main__':
    sub_channel_format('')