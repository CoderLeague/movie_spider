# -*- coding: utf-8 -*-

'''
Created on 2018.01.02

@author: codenewman
'''
from configure.setting import ONLINE_MONGODB_SERVER, ONLINE_MONGODB_PORT,\
    ONLINE_MONGODB_DB, ONLINE_MONGODB_COLLECTION, ONLINE_MONGODB_USERNAME,\
    ONLINE_MONGODB_PASSWORD
from pymongo.mongo_client import MongoClient
from toolkit import logkit
import logging


# 设置多线程日志
logger = logkit.get_logger(logger_name='mongo_dao', log_level=logging.DEBUG, print_level=logging.DEBUG)

# 设置mongo单例链接对象
BASE_MONGO_CLIENT = None

def get_mongo():
    """
    获取mongo操作对象
    """
    global BASE_MONGO_CLIENT
    
    if BASE_MONGO_CLIENT == None:
        BASE_MONGO_CLIENT = MongoDao()

    return BASE_MONGO_CLIENT

class MongoDao(MongoClient):
    '''
    [重写] MongoDB
    设置为单例
    '''

    def __init__(self):
        '''
        初始化
        '''
        logger.info (u'初始化mongo单例')
        self.init_connection()

    def init_connection(self):
        """
        初始化连接
        """
        super(MongoDao, self).__init__(
                host     = ONLINE_MONGODB_SERVER,
                port     = ONLINE_MONGODB_PORT,
                username = ONLINE_MONGODB_USERNAME,
                password = ONLINE_MONGODB_PASSWORD
            )
        self.static_mongo = self


    def get_mongo(self):
        """
        获取数据库操作对象
        """
        return self.static_mongo


    def get_mongo_collection(self, collection_name):
        """
        获取一个表
        """
        return self.getCollentcion(collection_name)


    def get_database(self, name=None, codec_options=None, read_preference=None, 
        write_concern=None, read_concern=None):
        """
        [重写]获取db操作对象
        增加默认数据库
        """
        name = name if name != None else ONLINE_MONGODB_DB
        return super(MongoDao, self).get_database(name=name, codec_options=codec_options, read_preference=read_preference, write_concern=write_concern, read_concern=read_concern)


    def get_collection(self, collection_name=ONLINE_MONGODB_COLLECTION, db_name = None):
        """
        获取默认
        """
        return self.get_database(db_name)[collection_name]


    def server_info(self, session=None):
        """
        打印已存在的数据库名称
        """
        info = super(MongoDao, self).server_info(session)
        logger.info (u'数据库连接信息: %s' % (info))
        return info


    def info(self, session=None):
        """
        获取基本信息
        """
        return self.server_info(session)
