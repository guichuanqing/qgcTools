# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2022/12/19 14:52
# @File : main.py
# Description : 文件说明
"""
from locust import User, task, events, run_single_user, HttpUser
import time
from websocket import create_connection
import json
import websockets
import random

def success_call(name, recvText, total_time):
    events.request_success.fire(
        request_type="[Success]",
        name=name,
        response_time=total_time,
        response_length=len(recvText)
    )


def fail_call(name, total_time, e):
    events.request_failure.fire(
        request_type="[Fail]",
        name=name,
        response_time=total_time,
        response_length=0,
        exception=e,
    )

def get_seq():
    start_time = time.time()
    num = random.randint(100000, 999999)
    seq = str(int(round(start_time * 1000))) + "-" + str(num)
    return [seq, num]

class WebSocketClient(object):
    def __init__(self, host):
        self.host = host
        self.ws = None

    def connect(self, burl):
        self.ws = create_connection(burl)

    def recv(self):
        return self.ws.recv()

    def send(self, msg):
        self.ws.send(msg)

    def close(self):
        self.ws.close()


class WebsocketUser(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(WebsocketUser, self).__init__(*args, **kwargs)
        self.client = WebSocketClient(self.host)
        self.client._locust_environment = self.environment


class ApiUser(WebsocketUser):
    host = "ws://47.109.44.38:8089/acc"

    @task(1)
    def pft(self):
        # wss 地址
        self.url = 'ws://47.109.44.38:8089/acc'
        start_time = time.time()
        try:
            self.client.connect(self.url)
            print("连接订阅")
            # 发送的订阅请求
            msg = {"seq":"","cmd":"login","data":{"userId":"","appId":101}}
            msg['seq'] = get_seq()[0]
            msg['data']['userId'] = "deme"+str(get_seq()[1])
            msgstr = json.dumps(msg)

            self.client.send(msgstr)
            print(f"↑: {msgstr}")

            greeting = self.client.recv()
            print(f"↓: {greeting}")

        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            fail_call("Send", total_time, e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            success_call("Send", "success", total_time)
        heartbeat = {"seq":"","cmd":"heartbeat","data":{}}
        heartbeat['seq'] = get_seq()[0]
        msgstr = json.dumps(heartbeat)
        print('保持心跳')
        self.client.send(msgstr)
        print(f"↑: {msgstr}")

        greeting = self.client.recv()
        print(f"↓: {greeting}")
        # self.run_forever()

        self.stop()
        # self.environment.runner.quit()

    def on_start(self):
        print("连接开始")

    def on_stop(self):
        print("开始关闭")

# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(ApiUser)