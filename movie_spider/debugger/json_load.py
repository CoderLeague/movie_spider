# -*- coding: utf-8 -*-

'''
Created on 2018年1月2日

@author: jiangzhongliang
'''
import json
import os, sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)


if __name__ == '__main__':
    
#     json_add = os.path.join(base_dir, 'data', 'movie_url.json')
    json_add = os.path.join(base_dir, 'data', 'sub_channel.json')
    print json_add
    
    with open(json_add) as f:
#         print f.read()
        
        j = json.load(f)
        print j