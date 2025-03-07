# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/5 17:43
# @File : http_client
# Description : 文件说明
"""
# services/http_client.py
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HttpClient:
    def __init__(self, base_url):
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 504]
        )
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.base_url = base_url

    def call_api(self, endpoint, method="GET", **kwargs):
        url = f"{self.base_url}/{endpoint}"
        return self.session.request(method, url, **kwargs)