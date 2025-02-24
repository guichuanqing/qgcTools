# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/2/24 18:19
# @File : set_data.py
# Description : 文件说明
"""
import requests
import json

# 配置信息
MOCK_SERVER_URL = "http://localhost:5000/set_mock"  # Mock 服务的地址
MOCK_JSON_FILE = "mock_data.json"                  # 你的 JSON 文件路径

def set_mock_data():
    try:
        # 1. 读取 JSON 文件
        with open(MOCK_JSON_FILE, "r", encoding="utf-8") as f:
            mock_config = json.load(f)  # 自动解析 JSON

        mock_config = {"response": mock_config, "status_code": 200}
        # 2. 发送 POST 请求
        response = requests.post(
            MOCK_SERVER_URL,
            json=mock_config,  # 自动设置 Content-Type 为 application/json
            timeout=5          # 超时时间（秒）
        )

        # 3. 检查响应
        if response.status_code == 200:
            print("Mock 数据设置成功！响应内容:", response.json())
        else:
            print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")

    except FileNotFoundError:
        print(f"错误：文件 {MOCK_JSON_FILE} 不存在！")
    except json.JSONDecodeError:
        print(f"错误：文件 {MOCK_JSON_FILE} 不是有效的 JSON 格式！")
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {str(e)}")

if __name__ == "__main__":
    set_mock_data()