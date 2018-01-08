# -*- coding: utf-8 -*-
'''
@author: codenewman
'''
from dao.mongo_dao import get_mongo

mongo = get_mongo()
mongo = get_mongo()
mongo = get_mongo()
mongo = get_mongo()

mongo.server_info()

collect = mongo.get_collection()
cursorRegex = collect.find()

count = 0

for document in cursorRegex:
    count += 1
    print(document[u'_id'])
#     print("Regex document: {}".format(document))

print count