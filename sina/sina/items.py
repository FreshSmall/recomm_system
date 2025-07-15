# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # 定义新闻标题字段
    title = scrapy.Field()
    # 定义新闻时间字段  
    time = scrapy.Field()
