import requests
import datetime
from docx import Document
from random import choice


addr = "http://api.demeworld.cn"  # 线上地址
login_url = r'/demeAdmin/manager/login'
api_url = r'/deme/article/addArticle'    # 新增资讯
article_lis = ["article_01.docx", "article_02.docx", "article_03.docx", "article_04.docx"]
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


# 登录
def con_login():
    data1 = {"phone":"18908330000"}
    res1 = requests.post(url=addr + '/deme/ses/sendMessage', headers=header, json=data1)
    data2 = {"phone":"18908330000","code":"666666"}
    res2 = requests.post(url=addr + '/deme/user/phoneLogin', headers=header, json=data2).json()['data']['token']
    print("登录成功！")
    return res2


# 多次新增变更data数据
def data_format(data):
    content = docx_read()
    if type(data) is dict:
        for k, v in data.items():
            if k == "title":
                data[k] = content[0][3:-4]
            if k == "content":
                data[k] = ''.join(content)
    return data


# 读取docx文件
def docx_read():
    content = []
    path = 'D:\\deme-test-performance\\other\\' + choice(article_lis)
    print("读取文件：", path)
    document = Document(path)
    for parg in document.paragraphs:
        content.append("<p>" + parg.text + "</p>")
    return content


  # 新增资讯
def add_collection(token):
    data = {"authorId":26,
             "content":"关于去中心化前景的探讨和争论已经汗牛充栋，涵盖的问题形形色色，从它的重要性，到谁将操控互联网底层软件的这样的更大问题。这些问题都很关键,若资讯信息涉及侵犯知识产权，&nbsp;请及时来电或致函告之，本站将第一时间删除文章。",
             "image1":"https://deme3.oss-cn-chengdu.aliyuncs.com/image/U38C2.jpg",
             "image2":"https://deme3.oss-cn-chengdu.aliyuncs.com/image/TFDJ003.jpg",
             "image3":"https://deme3.oss-cn-chengdu.aliyuncs.com/image/ZQGG03.jpg",
             "image4":"",
             "label":24,
             "title":"Web3建设者的去中心化宝典",
             "introduction":"Web3建设者的去中心化宝典：准则、模式和方法\n作者 | Miles Jennings\n关于去中心化前景的探讨和争论已经汗牛充栋",
             "jumpTitle":"Web3建设者的去中心化宝典",
             "jumpIntroduction":"Web3建设者的去中心化宝典的简介",
             "jumpLink":"https://web.demeworld.cn",
             "jumpLogo":"https://deme3.oss-cn-chengdu.aliyuncs.com/image/GBUV00s4f4.jpg",
              }
    header['token'] = token
    data = data_format(data)
    print("开始新增资讯...")
    res = requests.post(url=addr+api_url, headers=header, json=data).json()
    print(res)
    # for i in res:
    #     print(i)


if __name__ == "__main__":
    num = int(input("请输入新增资讯个数：\n"))
    token = con_login()
    for i in range(0, num):
        add_collection(token)