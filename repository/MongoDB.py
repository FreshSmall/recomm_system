"""
Author: yinchao
Date: 2025-07-15 22:52:20
LastEditors: Please set LastEditors
LastEditTime: 2025-07-16 23:11:37
Description:
"""

import pymongo


class MongoDB:
    def __init__(self, db):
        mongo_client = self._connect("127.0.0.1", 27017, "", "", db)
        self.db_scrapy = mongo_client[db]

    def _connect(self, host, port, username, password, db):
        mongo_info = self._splicing(host, port, username, password, db)
        mongo_client = pymongo.MongoClient(
            mongo_info, connectTimeoutMS=12000, connect=False
        )
        return mongo_client

    @staticmethod
    def _splicing(host, port, user, pwd, db):
        client = "mongodb://" + host + ":" + str(port) + "/"
        if user != "":
            client = (
                "mongodb://" + user + ":" + pwd + "@" + host + ":" + str(port) + "/"
            )
        if db != "":
            client += db
        return client
