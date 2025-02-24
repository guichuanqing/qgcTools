# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/2/24 17:34
# @File : mock_server.py.py
# Description : 文件说明
"""
from flask import Flask, request, jsonify
from flask_cors import CORS

# 设置mock数据 curl
#  curl -X POST http://localhost:5000/set_mock -H "Content-Type: application/json" -d "{\"response\": {\"user\": {\"id\": 1, \"name\": \"测试用户\"}}, \"status_code\": 200}"

# # 通过 GET 获取
# curl http://localhost:5000/get_mock
# # 通过 POST 获取（不需要传 Body）
# curl -X POST http://localhost:5000/get_mock

app = Flask(__name__)
CORS(app)

mock_data ={
    "response": {"message": "default value"},   # 自定义的返回内容
    "status_code": 200                          # 自定义的 HTTP 状态码
}

# ----------------------
# 设置 Mock 的接口 (只允许 POST)
# ----------------------
@app.route('/set_mock', methods=['POST'])
def set_mock():
    data = request.json
    # 更新 Mock 数据
    mock_data["response"] = data.get("response", mock_data["response"])
    mock_data["status_code"] = data.get("status_code", 200)
    return jsonify({"status": "success"})

# ----------------------
# 获取 Mock 的接口 (支持 GET/POST)
# ----------------------
@app.route('/get_mock', methods=['GET', 'POST'])
def get_mock():
    # 无论 GET 还是 POST，都返回相同的 Mock 数据
    return jsonify(mock_data["response"]), mock_data["status_code"]

if __name__ == '__main__':
    app.run(port=5000, debug=True)