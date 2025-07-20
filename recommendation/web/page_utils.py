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

import recommendation.dao.redis_db as redis_db


class page_utils(object):
    def __init__(self):
        self.redis_db = redis_db.RedisDB()

    def get_page_data(self, page_num, page_size):
        start = (page_num - 1) * page_size
        end = page_num * page_size-1
        list_data = self.redis_db.redis_client.zrevrange("rec_list_by_time", start, end)
        lst = []
        for data in list_data:  # type: ignore
            data = self.redis_db.redis_client.get(f"news_detail:{data}")
            lst.append(data)
        return lst


if __name__ == "__main__":
    pageUtils = page_utils()
    lst = pageUtils.get_page_data(1, 10)
    print(lst)
