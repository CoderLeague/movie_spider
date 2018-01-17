# -*- coding: utf-8 -*-
# Created on 2018年1月8日
# 主要功能: 导出所有影片的信息
# @author: codenewman

import os
import sys
import csv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from rest_spider.images_loader import get_images_info

def save_data_name(images_info_list, file_name = 'move_name_from_db.txt'):
    os_path = os.path.join(base_dir, 'data', file_name)
    
    file_out = file(os_path, 'wb+')
    writer   = csv.writer(file_out)

    try:
        for image_info in images_info_list:
            # try:
            row_data = image_info['title']

            writer.writerow(row_data)
            # except:
            #     print ('error %s' % image_info['title'])
            #     pass
    finally:
        file_out.close()


def master_main():
    images_info_list = get_images_info()
    save_data_name(images_info_list)

if __name__ == '__main__':
    master_main()