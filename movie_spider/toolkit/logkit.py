# -*- coding: utf-8 -*-

# @File    : logkit.py
# @Brief   :
# @Author  : jiangzhongliang@liquidnetwork.com
# @Time    : 2017/8/30 下午5:35

import os
import logging
from cloghandler import ConcurrentRotatingFileHandler

logger_dict = {}

def get_logger(logger_name, log_level=logging.WARNING, print_level=logging.WARNING):
    """
    获取日志操作对象
    """
    if logger_name in logger_dict:
        return logger_dict[logger_name]

    # 修改为可以多进程写入的日志系统
    logger = create_concurrent_logger(logger_name, log_level, print_level)
    logger_dict[logger_name] = logger

    return logger


def create_concurrent_logger(logger_name, log_level=logging.WARNING, print_level=logging.WARNING):
    """
    创建一个多进程使用的日志
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(base_dir, "logs")
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    logfile = os.path.join(log_path, logger_name + ".log")
    filesize = 800 * 1024 * 1024
    log = logging.getLogger(logger_name)

    # 将日志写入日志文件中
    rotate_handler = ConcurrentRotatingFileHandler(logfile, "a", filesize, 5, encoding="utf-8")
    rotate_handler.setLevel(log_level)
    fmt = "[%(asctime)-15s %(levelname)-8s %(filename)s:%(lineno)3d] [%(process)s] %(message)s"
    datefmt = "%a, %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)
    rotate_handler.setFormatter(formatter)
    log.addHandler(rotate_handler)
    log.setLevel(log_level)

    # 定义一个StreamHandler，将WARNING级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
    console = logging.StreamHandler()
    console.setLevel(print_level)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    return log
