import requests
import datetime
import time
from requests_toolbelt import MultipartEncoder

addr = "https://test-admin-api.demeworld.cn"
login_url = r'/demeAdmin/manager/login'
api_url = r'/demeAdmin/collection/upLoadAir'
excel_path = r"D:\auto-test\YJ4X空投名单模板.xlsx"

header = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '1130',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'origin': 'https://test-admin.demeworld.cn',
    'referer': 'https://test-admin.demeworld.cn/',
}


# 登录后台
def con_manage():
    data = {"userName": "qgc1", "password": "/J+mraC7w/pcfK16djHSeQ=="}
    res = requests.post(url=addr+login_url, headers=header, json=data).json()['data']['token']
    print("登录成功！")
    return res

  # 上传空投excel
def add_collection(token):
    print('===============开始上传==============')
    data = MultipartEncoder({
        'file': ('YJ4X空投名单模板.xlsx', open(excel_path, 'rb'),
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
    })
    header['Content-Type'] = data.content_type
    header['token'] = token
    print(header)
    res = requests.post(url=addr+api_url, headers=header, data=data).json()
    print(res)
    time.sleep(1)
    # for i in res:
    #     print(i)


if __name__ == "__main__":
    # phone = input("请输入需要空投的用户手机号： ")
    # collections = input("请输入藏品code(英文逗号隔开)： ").split(",")
    token = con_manage()
    add_collection(token)