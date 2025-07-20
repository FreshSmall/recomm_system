"""
author: yinchao
date: Do not edit
team: wuhan operational dev.
Description:
"""

from flask import Flask, request, jsonify
import json
from page_utils import page_utils

page_query = page_utils()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/hello_rec", methods=["POST"])
def hello_recommendation():
    if request.method == "POST":
        req_json = request.get_data()
        rec_obj = json.loads(req_json)
        user_id = rec_obj["user_id"]
        return jsonify({"code": 0, "msg": "请求成功", "data": "hello " + user_id})
    else:
        return jsonify({"code": 2001, "msg": "Method not allowed"})


@app.route("/recommendation/get_rec_list", methods=["POST"])
def get_rec_list():
    if request.method == "POST":
        rec_obj = request.get_json()
        page_num = rec_obj["page_num"]
        page_size = rec_obj["page_size"]

        try:
            data = page_query.get_page_data(page_num, page_size)
            return jsonify({"code": 0, "msg": "请求成功", "data": data})
        except Exception as e:
            print(str(e))
            return jsonify({"code": 2000, "msg": "error"})
    else:
        return jsonify({"code": 2001, "msg": "Method not allowed"})


if __name__ == "__main__":
    app.run(port=10086)
