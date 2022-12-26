# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2022/12/20 17:27
# @File : chat.py
# Description : 文件说明
"""
from locust import User, task, events, constant, run_single_user
import time
import websocket
import ssl
import json
import jsonpath
import random


def eventType_success(eventType, recvText, total_time):
    events.request_success.fire(request_type="[RECV]",
                                name=eventType,
                                response_time=total_time,
                                response_length=len(recvText))

def get_seq():
    start_time = time.time()
    num = random.randint(100000, 999999)
    seq = str(int(round(start_time * 1000))) + "-" + str(num)
    return [seq, num]

class WebSocketClient(object):
    _locust_environment = None

    def __init__(self, host):
        self.host = host
        # 针对 WSS 关闭 SSL 校验警报
        self.ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

    def connect(self, burl):
        start_time = time.time()
        try:
            self.conn = self.ws.connect(url=burl)
        except websocket.WebSocketConnectionClosedException as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="[Connect]", name='Connection is already closed', response_time=total_time, exception=e)
        except websocket.WebSocketTimeoutException as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="[Connect]", name='TimeOut', response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(
                request_type="[Connect]", name='WebSocket', response_time=total_time, response_length=0)
        return self.conn

    def recv(self):
        return self.ws.recv()

    def send(self, msg):
        self.ws.send(msg)


class WebsocketUser(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(WebsocketUser, self).__init__(*args, **kwargs)
        self.client = WebSocketClient(self.host)
        self.client._locust_environment = self.environment


class ApiUser(WebsocketUser):
    host = "ws://47.109.44.38:8089/acc"
    wait_time = constant(0)


    @task(1)
    def pft(self):
        # wss 地址
        self.url = 'ws://47.109.44.38:8089/acc'
        self.data = {}
        self.client.connect(self.url)
        run_time = time.time()

        # 发送的订阅请求
        msg = {"seq": "", "cmd": "login", "data": {"userId": "", "appId": 101}}
        msg['seq'] = get_seq()[0]
        msg['data']['userId'] = "deme" + str(get_seq()[1])
        msgstr = json.dumps(msg)
        self.client.send(msgstr)

        while True:
            # 消息接收计时
            start_time = time.time()
            recv = self.client.recv()
            total_time = int((time.time() - start_time) * 1000)
            if int(start_time - run_time) > 30:
                heartbeat = {"seq": "", "cmd": "heartbeat", "data": {}}
                heartbeat['seq'] = get_seq()[0]
                msgstr = json.dumps(heartbeat)
                print('保持心跳')
                self.client.send(msgstr)
                print(f"↑: {msgstr}")

            # 为每个推送过来的事件进行归类和独立计算性能指标
            try:
                recv_j = json.loads(recv)
                eventType_s = jsonpath.jsonpath(recv_j, expr='$.eventType')
                eventType_success(eventType_s[0], recv, total_time)
            except websocket.WebSocketConnectionClosedException as e:
                events.request_failure.fire(request_type="[ERROR] WebSocketConnectionClosedException",
                                            name='Connection is already closed.',
                                            response_time=total_time,
                                            exception=e)
            except:
                print(recv)
                # 正常 OK 响应，或者其它心跳响应加入进来避免当作异常处理
                if 'ok' in recv:
                    eventType_success('ok', 'ok', total_time)

# if launched directly, e.g. "python3 debugging.py", not "locust -f debugging.py"
if __name__ == "__main__":
    run_single_user(ApiUser)