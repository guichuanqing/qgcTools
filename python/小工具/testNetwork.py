# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2023/7/7 14:49
# @File : testNetwork.py
# Description : 文件说明
"""

# Internet Speed tester
# pip install speedtest-cli
import speedtest as st

# Set Best Server
server = st.Speedtest()
server.get_best_server()

# Test Download Speed
down = server.download()
down = down / 1000000
print(f"Download Speed: {down} Mb/s")

# Test Upload Speed
up = server.upload()
up = up / 1000000
print(f"Upload Speed: {up} Mb/s")

# Test Ping
ping = server.results.ping
print(f"Ping Speed: {ping}")
