# -*- coding: utf-8 -*-
# 
# Created on 2018年1月8日
# 
# @author: codenewman
# 
import urllib
from PIL import Image


save_path =  "../data/t01174c0d7a97728b1a.webp"

def test_save():

    url = "http://p0.qhimg.com/t01174c0d7a97728b1a.webp"
    
    content = urllib.urlopen(url).read()
    with file(save_path, u'wb') as f:
        f.write(content)


def text_open():
    # 获取图片尺寸
    f_img  = Image.open(save_path)
    width  = f_img.size[0]
    height = f_img.size[1]
    print f_img


if __name__ == "__main__":
#     test_save()
    text_open()


