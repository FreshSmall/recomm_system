'''
Author: error: git config user.name & please set dead value or install git
Date: 2025-07-13 23:23:03
LastEditors: yinchao
LastEditTime: 2025-07-14 17:01:22
Description: 
'''
from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute('scrapy crawl sina_spider -s LOG_FILE=sipder.log'.split())