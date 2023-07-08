import pymysql
import redis
import csv
import pandas as pd
from sshtunnel import SSHTunnelForwarder # ssh连接库
import base64



orderCode_path = r"D:/deme-test-performance/paramData/t_order.csv"
pool = redis.ConnectionPool(host='172.29.101.42', port=6379, db=0, password='QWE123456')

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
            print(f'执行查询语句：{sql}  参数：{args}')
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

def execute_sql(sql):
    try:
        result = []
        datas = mysql_ssh(sql)
        if datas[-1]:
            print(f"共找到{len(datas[0])}个数据")
            result = list(datas[0])
            try:
                datas_write(result)
            except Exception as error:
                print(error)
            else:
                result.clear()
        else:
            print('数据查询失败')
    except Exception as e:
        print(e)


def datas_write(a):
    # dataframe = pd.MultiIndex.from_tuples(a, name=["orderCode","userId"])
    dataframe = pd.DataFrame(a)
    dataframe.to_csv(orderCode_path, mode= 'w', index=False, sep=',',header=["orderCode", "userId"])
    print("写入成功！")

if __name__ == "__main__":
    sql = r"SELECT order_code,user_id FROM `t_order`;"      # 导出所有的订单code
    # sql = r"SELECT order_code,user_id FROM `t_order` WHERE order_state = 1;"    # 导出支付状态的订单code
    execute_sql(sql)

