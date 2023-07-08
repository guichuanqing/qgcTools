import requests
import datetime
# from docx import Document
from random import choice
import csv
import pandas as pd


addr = "http://47.108.180.26:8088"  # 接口地址
login_url = r'/demeAdmin/manager/login'
phone_path = r"D:\deme-test-performance\paramData\phoneSet.csv"
login_token_path = r"D:\deme-test-performance\paramData\login_token.csv"

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'token': 'eyJhbGciOiJIUzI1NiJ9.eyJwaG9uZSI6IjE4OTA4MzM2MzM0IiwibWVzc2FnZSI6InVzZXJJZF85MSIsInVzZXJOYW1lIjoiNHlBQTlZM28iLCJ1c2VySWQiOjkxLCJleHAiOjE2NTUyNjI5NjZ9.B4TG76LjWNHrvNg844-6R_2o1DqzLuwYxuP7F338_TM',
    'Content-Length': '42081',
    'Origin': 'https://web.demeworld.cn',
    'Connection': 'keep-alive',
    'Referer': 'https://web.demeworld.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
}

# 读取CSV
def phone_read():
    with open(phone_path) as f:
        f_csv = csv.reader(f)
        uid_lit = []
        t_lit = []
        count = 0
        for row in f_csv:
            try:
                res = con_login(row[0])
                print(res)
                if not res:
                    continue
                uid_lit.append(res['user']['id'])
                t_lit.append(res['token'])
                count +=1
                print(f'保存第{count}条登录数据。。。', end='')
                if count%1000 == 0:
                    print(f'共{len(uid_lit)}数据获取完毕，开始写入！')
                    try:
                        pass
                        # token_write(uid_lit, t_lit)
                    except Exception as error:
                        print(error)
                    else:
                        uid_lit.clear()
                        t_lit.clear()
            except Exception as error:
                print(error)
        print(f'共{len(uid_lit)}数据获取完毕，开始写入！')
        token_write(uid_lit, t_lit)

# 登录
def con_login(phone):
    data1 = {"phone":phone}
    res1 = requests.post(url=addr + '/deme/ses/sendMessage', headers=header, json=data1)
    data2 = {"phone":phone,"code":"666666"}
    res2 = requests.post(url=addr + '/deme/user/phoneLogin', headers=header, json=data2).json()['data']    # ['token']
    # print("登录成功！")
    print('\r', end='', flush=True)
    return res2

# 写入CSV
def token_write(a, b):
    # with open(login_token_path, 'a', newline='') as f:
    #     # global if_head
    #     # if if_head:
    #     #     fieldnames = ['userId', 'token']  # 表头
    #     writer = csv.writer(f)
    #     #     writer.writeheader()
    #     #     if_head = False
    #     # writer = csv.writer(f)
    #     writer.writerow(every_dict)
    #     print('插入成功！')
    dataframe = pd.DataFrame({'userId': a, 'token': b})
    dataframe.to_csv(login_token_path, mode= 'a', index=False, sep=',',header=False)
    print("写入成功！")


if __name__ == "__main__":
    # num = int(input("请输入新增资讯个数：\n"))
    # token = con_login()
    phone_read()
    # for i in range(0, num):
        # add_collection(token)