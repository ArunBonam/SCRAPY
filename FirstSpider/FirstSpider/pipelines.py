# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class FirstspiderPipeline(object):
    #def process_item(self, item, spider):
        #return item

###This pipeline gets the yielded items in First Spider and writes to MongoDB hosted on compose############

import ssl
import pymongo
import traceback
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from pymongo import MongoClient

class MongoDBPipeline(object):
    # connection parameters will be fetched settings.py
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_URL'],ssl=True
            #settings['MONGODB_SERVER'],
            #settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        print("connecting to==>",connection)
        print("connecting to the db==>",db)
        self.collection = db[settings['MONGODB_COLLECTION']]
        
    def process_item(self, item, spider):
        valid = True
        for data in item:
            print("in mongodb",data)
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            try:
                self.collection.insert(item)
                log.msg("Articles added to MongoDB database!",level=log.DEBUG,spider=spider)
            except Exception as e:
                print(e)
                traceback.print_exc()    
        return item

