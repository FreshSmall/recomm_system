'''
Author: yinchao
Date: 2025-04-02 05:55:01
LastEditors: Please set LastEditors
LastEditTime: 2025-07-16 23:25:09
Description: 
'''
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from repository.MongoDB import MongoDB

class SinaPipeline:
    def __init__(self):
        self.mongo_db= MongoDB('scrapy_data')
        self.mongo_collection = self.mongo_db.db_scrapy['content_ori']

    def process_item(self, item, spider):
        result_item = dict(item)
        print(self.mongo_collection)
        self.mongo_collection.insert_one(result_item)
        return item
