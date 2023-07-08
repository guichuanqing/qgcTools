import pymysql
import random
import datetime
import requests
from sshtunnel import SSHTunnelForwarder # ssh连接库

addr = "http://47.108.180.26:8088"  # 接口地址   3561807
login_url = r'/demeAdmin/manager/login'
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

# 生成随机phone
def create_random_phone():
    phone = "1" + random.choice(['3', '5', '7', '8', '9'])
    # phone = "1" + random.choice(['2', '4', '6', '0'])
    for i in range(0, 9):
        num = random.randint(0, 9)
        phone += str(num)
    return phone

# 登录
def con_login(phone):
    data1 = {"phone":phone}
    res1 = requests.post(url=addr + '/deme/ses/sendMessage', headers=header, json=data1)
    data2 = {"phone":phone,"code":"666666"}
    res2 = requests.post(url=addr + '/deme/user/phoneLogin', headers=header, json=data2).json()['data']    # ['token']
    if res2:
        print("登录成功：", res2)
    print('\r', end='', flush=True)
    return res2

# 数据库插入
def mysql_ssh(sql,args=None):
    with SSHTunnelForwarder(
            ('47.108.168.38', 22),
            ssh_password='Deme112233!@#!@#',
            ssh_username='root',
            local_bind_address=('127.0.0.1', 22),
            remote_bind_address=('rm-2vctoz47r43qrelfm.mysql.cn-chengdu.rds.aliyuncs.com', 3306)) as server:
        print('SSH连接成功')
        conn = pymysql.connect(host='127.0.0.1',
                               port=22,
                               user='deme3',
                               password='7tEp8N283SkLYRAi',
                               database='deme3',
                               charset='utf8')
        print('mysql数据库连接成功')
        cursor = conn.cursor()
        print('游标获取成功')
        try:
            print(f'执行语句：{sql}  参数：{args}')
            cursor.execute(sql,args)
            print('数据查询成功')
            conn.commit()
            print('事务提交成功')
            datas = cursor.fetchall()
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

# 查询多个用户的sql
def select_sql(userName):
    print('----------', userName)
    if len(userName)>1:
        value = tuple(userName)
        sql = f'SELECT id FROM t_user WHERE `user_name` in {value};'
    else:
        sql = f'SELECT id FROM t_user WHERE `user_name` = "{userName[0]}";'
    result = execute_sql(sql)
    print(result)
    user = []
    for i in result:
        user.append(i[0])
    return user

# 添加多个用户的sql
def insert_sql(superior, user):
    time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    print(time)
    value =""
    for i in user:
        tmp = superior + "," + str(i) + "," + "1," + time
        value_tuple = tuple(tmp.split(","))
        value += str(value_tuple) +","
    if value[-1]==",":
        value = value[:-1]
    sql = f'INSERT INTO t_invitation_relationship(superior,subordinate,status,invitation_time) VALUES {value};'
    execute_sql(sql)

if __name__ == "__main__":
    superior = input("请输入邀请主用户id： ")
    times = int(input("请输入被邀请人数： "))
    userName = []
    for i in range(times):
        phone = create_random_phone()
        data = con_login(phone)
        if data['user']['userName']:
            userName.append(data['user']['userName'])
    userId = select_sql(userName)
    insert_sql(superior,userId)

