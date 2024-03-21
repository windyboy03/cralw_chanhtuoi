# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import traceback
import pymongo
import json
from itemadapter import ItemAdapter
import os
from decouple import config

class ChanhtuoiPipeline:
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
    def __init__(self):
        url = config('url')
        client = pymongo.MongoClient(url)
        db = client["chanhtuoi"]
        self.db = db
        
    def process_item(self, item, spider):
        try:
            parseItem = ItemAdapter(item).asdict()
            existed_o = self.db.article_details_raw.find_one({ "url": parseItem["url"] }, {"url": 1})
            if not existed_o:
                self.db.article_details_raw.insert_one(parseItem)
            else:
                print('Existed url: {}'.format(parseItem["url"]))
        except Exception as e:
            print('Error: db.article_details_raw.insert_one', e)
            print(traceback.format_exc())
        return item
