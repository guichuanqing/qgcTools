import pymysql
import random
import datetime
import requests
from sshtunnel import SSHTunnelForwarder # ssh连接库
import json

addr = "https://test-admin-api.demeworld.cn"  # 接口地址   3561807
login_url = r'/demeAdmin/manager/login'
collection_send_url = r'/demeAdmin/collection/send'
orderCode_path = r"D:/deme-test-performance/paramData/t_order.csv"
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



# 数据库插入
def mysql_ssh(sql,args=None):
    with SSHTunnelForwarder(
            ('xxxx', 22),
            ssh_password='Deme112233!@#!@#',
            ssh_username='root',
            local_bind_address=('127.0.0.1', 22),
            remote_bind_address=('xxxxx', 3306)) as server:
        print('SSH连接成功')
        conn = pymysql.connect(host='127.0.0.1',
                               port=22,
                               user='dem',
                               password='7tEp',
                               database='deme3',
                               charset='utf8')
        print('mysql数据库连接成功')
        cursor = conn.cursor()
        print('游标获取成功')
        try:
            print(f'执行语句：{sql}  参数：{args}')
            cursor.execute(sql,args)
            print('数据查询成功')
            if sql.count("INSERT"):
                datas=conn.insert_id()
                conn.commit()
                print('事务提交成功')
            else:
                datas = cursor.fetchall()
                conn.commit()
                print('事务提交成功')
            success = True
        except:
            print('数据查询失败')
            datas = None
            success = False
        print('正在关闭数据库连接')
        cursor.close()
        conn.close()
    return datas, success

# 执行sql
def execute_sql(sql):
    try:
        datas = mysql_ssh(sql)
        if datas[-1]:
            print(f"数据执行成功")
            return datas[0]
    except Exception as e:
        print(e)

# 查询用户的id,name
def select_sql(phone):
    print('----------查询用户信息')
    sql = f'SELECT id,user_name,phone FROM t_user WHERE `phone` in ({phone});'
    result = execute_sql(sql)
    print(result)
    user = []
    for i in result[0]:
        user.append(i)
    return user

# 添加空投需求
def insert_sql(collections, user):
    print('----------插入空投需求')
    result =[]
    time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    user_id = user[0]
    user_name = user[1]
    user_phone = user[2]
    for collection_code in collections:
        value =f"'34', 'qgc', '{time}', '{collection_code}', {user_id}, '{user_name}', '{user_phone}', 1, '1'"
        sql = f'INSERT INTO t_collection_airdrop(create_by,create_name,create_time,collection_code,user_id,user_name,user_phone,status,quantity) VALUES ({value});'
        print(sql)
        result.append(execute_sql(sql))
    return result
# 发放空投
def con_manage(ids):
    data = {"userName": "qgc1", "password": "/J+mraC7w/pcfK16djHSeQ=="}
    token = requests.post(url=addr+login_url, headers=header, json=data).json()['data']['token']
    header['token'] = token
    data1 = {}
    data1["ids"] = ids
    res = requests.post(url=addr + collection_send_url, headers=header, data=json.dumps(data1)).json()
    print("空投发送结果：", res)

if __name__ == "__main__":
    # 发送空投
    phone = input("请输入需要空投的用户手机号： ")
    collections = input("请输入藏品code(英文逗号隔开)： ").split(",")
    user = select_sql(phone)
    result = insert_sql(collections, user)
    con_manage(result)




