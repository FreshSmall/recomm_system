"""
author: yinchao
date: Do not edit
team: wuhan operational dev.
Description:
"""

from ast import main
import sys
import os

# 将项目根目录添加到Python路径中
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

import recommendation.dao.redis_db as redis_db
import recommendation.dao.mongo_db as mongo_db


class SimpleRecList(object):
    def __init__(self):
        self.redis_db = redis_db.RedisDB()
        self.mongo_db = mongo_db.MongoDB(db="recommendation")
        self.mongo_db_collection = self.mongo_db.mongo_client["recommendation"][
            "content_label"
        ]

    def add_data_to_redis(self):
        mongo_data = self.mongo_db_collection.find().sort("news_date", -1)
        count = 10000
        for data in mongo_data:
            self.redis_db.redis_client.zadd(
                "rec_list_by_time", {str(data["_id"]): count}
            )
            count -= 1


if __name__ == "__main__":
    simple_rec_list = SimpleRecList()
    simple_rec_list.add_data_to_redis()
