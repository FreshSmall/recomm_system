'''
Author: error: git config user.name & please set dead value or install git
Date: 2025-07-13 23:23:03
LastEditors: yinchao
LastEditTime: 2025-07-15 23:20:05
Description: 
'''
import sys
import os
from scrapy import cmdline

# 将项目根目录添加到Python路径中，这样就能找到repository模块
# sina/main.py -> 向上一级到项目根目录
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    cmdline.execute('scrapy crawl sina_spider -s LOG_FILE=spider.log'.split())