import sys
import os

# 将项目根目录添加到Python路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from recommendation.dao.mongo_db import MongoDB
from datetime import datetime
from datetime import timezone

class ContentLabel(object):
   def __init__(self):
       self.mongo_scrapy = MongoDB(db='scrapy_data')
       self.mongo_recommendation = MongoDB(db='recommendation')
       self.scrapy_collection = self.mongo_scrapy.db_scrapy_data['scrapy_data.content_ori']
       self.content_label_collection = self.mongo_recommendation.db_recommendation['content_label']

   def get_data_from_mongodb(self):
       datas = self.scrapy_collection.find()
       print(f"从数据库获取数据...")
       data_list = list(datas)
       print(f"获取到 {len(data_list)} 条数据")
       return data_list
   
   def make_content_labels(self):
       datas = self.get_data_from_mongodb()
       
       if not datas:
           print("没有找到数据")
           return
           
       for i, data in enumerate(datas):
           print(f"处理第 {i+1} 条数据: {data}")
           
           content_collection = dict()
           # 适配实际的数据字段结构
           content_collection['describe'] = data.get('desc', '')  # 可能为空
           content_collection['type'] = data.get('type', 'news')  # 默认为news
           content_collection['title'] = data.get('title', '')
           content_collection['news_date'] = data.get('time', '')  # 使用time字段而不是times
           content_collection['hot_heat'] = 10000
           content_collection['likes'] = 0
           content_collection['read'] = 0
           content_collection['collections'] = 0
           content_collection['create_time'] = datetime.now(timezone.utc)
           
           print(f"处理后的数据: {content_collection}")
           
           # 插入到recommendation数据库
           try:
               self.content_label_collection.insert_one(content_collection)
               print(f"成功插入第 {i+1} 条数据到content_label集合")
           except Exception as e:
               print(f"插入数据时出错: {e}")

if __name__ == '__main__':
    content_label = ContentLabel()
    content_label.make_content_labels()