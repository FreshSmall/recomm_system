"""
author: yinchao
date: Do not edit
team: wuhan operational dev.
Description:
"""

import sys
import os

# 将项目根目录添加到Python路径中
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from recommendation.dao.mongo_db import MongoDB
from recommendation.model.test_keywords import Model
from datetime import datetime
from datetime import timezone
from sklearn.feature_extraction.text import TfidfVectorizer


class ContentLabel(object):
    def __init__(self):
        self.mongo_scrapy = MongoDB(db="scrapy_data")
        self.mongo_recommendation = MongoDB(db="recommendation")
        self.scrapy_collection = self.mongo_scrapy.mongo_client["scrapy_data"][
            "content_ori"
        ]
        self.content_label_collection = self.mongo_recommendation.mongo_client[
            "recommendation"
        ]["content_label"]

    def get_data_from_mongodb(self):
        datas = self.scrapy_collection.find()
        print(f"从数据库获取数据...")
        data_list = list(datas)
        print(f"获取到 {len(data_list)} 条数据")
        return data_list

    def extract_keywords_mixed(self, desc_list, top_k=5):
        model = Model()
        keywords_list = []
        for desc in desc_list:
            words_list = model.process_text(desc)
            textrank_keyword = model.get_keyword(words_list, "textrank")
            tfidf_keyword = model.get_keyword(words_list, "tfidf")
            keywords = model.keyword_interact(tfidf_keyword, textrank_keyword)
            keywords_list.append(keywords)
        return keywords_list

    def make_content_labels(self):
        datas = self.get_data_from_mongodb()
        if not datas:
            print("没有找到数据")
            return

        desc_list = [data.get("desc", "") for data in datas]
        keywords_list = self.extract_keywords_mixed(desc_list, top_k=5)

        for i, (data, keywords) in enumerate(zip(datas, keywords_list)):
            print(f"处理第 {i+1} 条数据: {data}")
            content_collection = dict()
            # 适配实际的数据字段结构
            content_collection["describe"] = data.get("desc", "")  # 可能为空
            content_collection["type"] = data.get("type", "news")  # 默认为news
            content_collection["title"] = data.get("title", "")
            content_collection["news_date"] = data.get(
                "time", ""
            )  # 使用time字段而不是times
            content_collection["hot_heat"] = 10000
            content_collection["likes"] = 0
            content_collection["read"] = 0
            content_collection["collections"] = 0
            content_collection["create_time"] = datetime.now(timezone.utc)
            content_collection["keywords"] = keywords

            print(f"处理后的数据: {content_collection}")
            # 插入到recommendation数据库
            try:
                self.content_label_collection.insert_one(content_collection)
                print(f"成功插入第 {i+1} 条数据到content_label集合")
            except Exception as e:
                print(f"插入数据时出错: {e}")


if __name__ == "__main__":
    content_label = ContentLabel()
    content_label.make_content_labels()
