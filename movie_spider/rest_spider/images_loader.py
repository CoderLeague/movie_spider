# -*- coding: utf-8 -*-

# Created on 2018年1月8日
# 主要功能: 将网络URL图片下载到本地, 并计算好长宽.
# @author: codenewman

# 步骤一: 获取图片url
# 步骤二: 下载图片
# 步骤三: 计算长宽
# 步骤四: 保存(json和mongoDB)

import logging
import os
import sys
import urllib
import traceback

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from dao.mongo_dao import MongoDao
from PIL import Image
from toolkit import logkit
from configure.setting import IMAGE_ROOT, ONLINE_MONGODB_SERVER,\
    ONLINE_MONGODB_PORT, ONLINE_MONGODB_USERNAME, ONLINE_MONGODB_PASSWORD,\
    ONLINE_MONGODB_COLLECTION, ONLINE_WECHAT_COLLECTION

# 引入多线程日志
logger = logkit.get_logger('images_loader', log_level=logging.INFO, print_level=logging.ERROR)

class ImageDownloader(object):
    """
    M站图片下载器
    """
    
    _cache_collect = None
    
    
    def __init__(self,
                host     = ONLINE_MONGODB_SERVER,
                port     = ONLINE_MONGODB_PORT,
                username = ONLINE_MONGODB_USERNAME,
                password = ONLINE_MONGODB_PASSWORD,
                collection_name =  ONLINE_MONGODB_COLLECTION
                ):
        mongo_client = MongoDao(
                host     = host,
                port     = port,
                username = username,
                password = password
        )
        self._cache_collect = mongo_client.get_collection(collection_name)

    
    def get_images_info(self):
        """
        获取数据库中图片的信息
        可迭代,字典元素
        """
        images_result = self._cache_collect.find()
        print self._cache_collect.count()
        return images_result

    
    def get_file_path(self, db_image_info, file_name):
        """
        构造路径
        """
        relative_path = os.path.join(
            db_image_info[u'source'],
            db_image_info[u'sub_source'],
            db_image_info[u'channel'],
            db_image_info[u'sub_channel'],
            )
        save_path = os.path.join(
            IMAGE_ROOT,
            relative_path,
            )
    
        if not os.path.exists(save_path):
            os.makedirs(save_path)
    
        relative_path = os.path.join(relative_path, file_name)
        save_path     = os.path.join(IMAGE_ROOT, relative_path)
    
        return save_path, relative_path
    
    
    def pull_image(self, url, save_path):
        """
        下载图片
        """
        logger.info (u'正在下载文件:%s' % (url))
        content = urllib.urlopen(url).read()
        with file(save_path, u'wb') as f:
            f.write(content)
    
    def get_web_images(self, db_image_doc):
        """
        获取web图片, 保存至本地, 更细mongo
        """
        image_list = db_image_doc[u'cover_images']
        count = 1
        result = []
        
        for img in image_list:
            logger.info(img[u'img'])
            if img[u'img'].startswith('http') == False :
                result.append(img)
                continue

            file_name = u'.'.join((
                db_image_doc[u'item_id'] + u'_' + str(count),
                img[u'img'].replace(' ','').split(u'.')[-1],
                ))
            save_path, relative_path = self.get_file_path(db_image_doc, file_name)

            try:
                # 下载图片
                self.pull_image(img[u'img'], save_path)
                logger.info(save_path)
                
                # 获取图片尺寸
                f_img  = Image.open(save_path)
                width  = f_img.size[0]
                height = f_img.size[1]
            
                # 将本地URL更新至mongo缓存
                img[u'img']    = relative_path
                img[u'width']  = width
                img[u'height'] = height
                
                result.append(img)
            except:
                logger.error(u'处理图片时出现错误, 跳过当前图片')
                logger.error(img[u'img'])
                logger.error(traceback.format_exc())

        db_image_doc[u'cover_images'] = result
        return db_image_doc
    
    
    def update_mongo(self, update_image_doc):
        """
        更新数据库
        """
        logger.info(u'正在保存图片数据')
        
        self._cache_collect.update({u'_id' : update_image_doc[u'_id']}, 
                       update_image_doc,
                       )
    
    
    def master_main(self):
        """
        程序入口, 主调度
        """
        images_info_list = self.get_images_info()
        
        for image_info in images_info_list:
            update_image_doc = self.get_web_images(image_info)

            self.update_mongo(update_image_doc)

        logger.info(u'图片下载和更新链接, 完成.')


class WechatImageDownloader(ImageDownloader):
    """
    微信图片下载器
    """

    def get_web_images(self, db_image_info):
        """
        获取web图片, 保存至本地, 更细mongo
        """
        count = 1
        result = []

        for img in db_image_info[u'cover_images']:

            logger.info(img[u'img'])


            if img[u'img'].startswith('http') == False:
                continue
            
            file_name = u'.'.join((
                db_image_info[u'item_id'] + u'_' + str(count),
                img[u'img'].replace(' ','').split(u'.')[-1],
                ))
            save_path, relative_path = self.get_file_path(db_image_info, file_name)
            
            # 下载图片
            self.pull_image(img[u'img'], save_path)
            logger.info(save_path)
            
            try:
                # 获取图片尺寸
                f_img  = Image.open(save_path)
                width  = f_img.size[0]
                height = f_img.size[1]
            
                # 将本地URL更新至mongo缓存
                img[u'img']    = relative_path
                img[u'width']  = width
                img[u'height'] = height
                
                result.append(img)
            except:
                logger.error(traceback.format_exc())

        return result


if __name__ == '__main__':
     image_worker = ImageDownloader()  # M站图片下载
     image_worker.master_main()

#    wechat_image_worker = WechatImageDownloader(collection_name=ONLINE_WECHAT_COLLECTION)  # 微信图片下载
#    wechat_image_worker.master_main()
