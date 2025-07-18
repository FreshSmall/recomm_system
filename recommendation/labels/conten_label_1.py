'''
author: yinchao
date: Do not edit
team: wuhan operational dev.
Description: 
'''
import sys
import os

# 将项目根目录添加到Python路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from recommendation.dao.mongo_db import MongoDB
from recommendation.model.test_keywords import Model

class ContentLabel(object):
    def __init__(self):
        self.mongo_recommendation = MongoDB(db='recommendation')
        self.content_label_collection = self.mongo_recommendation.db_recommendation['content_label']
    
    def get_data_from_mongodb(self):
        datas = self.content_label_collection.find()
        print(f"从数据库获取数据...")
        data_list = list(datas)
        print(f"获取到 {len(data_list)} 条数据")
        return data_list
    
    def make_content_labels(self):
        datas = self.get_data_from_mongodb()
        if not datas:
            print("没有找到数据")
            return
        
        model = Model()
        for data in datas:
            desc = data.get('describe', '')
            words_list = model.process_text(desc)
            tfidf_keyword = model.get_keyword(words_list, 'tfidf')
            textrank_keyword = model.get_keyword(words_list, 'textrank')
            keywords = model.keyword_interact(tfidf_keyword, textrank_keyword)
            print(keywords)
            data['keywords'] = keywords
            self.content_label_collection.update_one({'_id': data['_id']}, {'$set': {'keywords': keywords}})
            
    def main(self):
        self.make_content_labels()

if __name__ == '__main__':
    content_label = ContentLabel()
    content_label.main()