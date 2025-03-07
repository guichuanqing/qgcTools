# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/6 10:05
# @File : test_account
# Description : 文件说明
"""
from web3_test_framework.services.http_client import HttpClient
from web3_test_framework.core.account.wallet import Wallet

class CCat(HttpClient):

    def __init__(self):
        super().__init__()
        self.user: Wallet = None

    def login(self):
        # 用户进行登录
        endpoint = "/login"
        method = "POST"
        rsp = self.call_api(endpoint, method)

    def logout(self):
        # 用户退出登录
        pass

    def ask(self, kol_user):
        # 用户对某个KOL进行提问
        pass

    def answer(self, ask_id):
        # KOL用户对某个问题进行回答
        pass

    def spectate(self, ask_id):
        # 普通用户对某个已回答问题进行围观
        pass

    def like_q(self, ask_id):
        # 围观用户对某个已回答问题进行点赞
        pass

    def dislike_q(self, ask_id):
        # 围观用户对某个已回答问题进行点踩
        pass

    def get_rewards(self):
        # 获取奖励列表
        pass



if __name__ == "__main__":
    # 使用pytest运行测试
    # pytest.main(['-v', '--tb=short', __file__])
    pass