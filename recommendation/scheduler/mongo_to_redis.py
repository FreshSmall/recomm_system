import sys
import os

# 将项目根目录添加到Python路径中
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


from recommendation.dao.redis_db import RedisDB
from recommendation.dao.mongo_db import MongoDB


class mongo_to_redis_content(object):
    def __init__(self):
        self.redis_db = RedisDB()
        self.mongo_db_recommendation = MongoDB(db="recommendation")
        self.mongo_db_collection = self.mongo_db_recommendation.mongo_client[
            "recommendation"
        ]["content_label"]

    def get_data_from_mongodb(self):
        datas = self.mongo_db_collection.find()
        print(f"从数据库获取数据...")
        data_list = list(datas)
        print(f"获取到 {len(data_list)} 条数据")
        return data_list

    def write_to_redis(self):
        data_list = self.get_data_from_mongodb()
        for data in data_list:
            result = dict()
            result_title = dict()
            result["content_id"] = str(data["_id"])
            result["describe"] = str(data["describe"])
            result["type"] = str(data["type"])
            result["title"] = str(data["title"])
            result["news_date"] = str(data["news_date"])
            result["likes"] = data["likes"]
            result["read"] = data["read"]
            result_title["content_id"] = str(data["_id"])
            result_title["title"] = str(data["title"])
            self.redis_db.redis_client.set(
                "news_detail:" + str(data["_id"]), str(result)
            )

        print("写入redis完成")


if __name__ == "__main__":
    write_to_redis = mongo_to_redis_content()
    write_to_redis.write_to_redis()
