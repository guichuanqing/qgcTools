import redis
import pandas as pd
from sshtunnel import SSHTunnelForwarder # ssh连接库


token_path = r".\login_token.csv"
# pool = redis.ConnectionPool(host='172.29.101.42', port=6379, db=0, password='QWE123456')
server = SSHTunnelForwarder(
        ssh_address_or_host= ('47.108.168.38',22),   # ssh地址
        ssh_username= "root", # ssh连接的用户名
        ssh_password=  "Deme112233!@#!@#" , # ssh连接的用户名
        remote_bind_address=('r-2vcinifo71556p3qin.redis.cn-chengdu.rds.aliyuncs.com', 6379))

def execute_sql():
    try:
        r = redis.Redis(host='127.0.0.1', port=server.local_bind_port, decode_responses=True, password='QWEqwe123!@#', db=0, encoding='gb18030')
        print("连接成功")
        keys = r.keys(pattern="*userId*")
        print(f"共找到{len(keys)}个数据")
        result = []
        for i in keys:
            try:
                result.append(r.get(i))
            except Exception as e:
                print("{}不存在".format(i))
                result = None
    except Exception as e:
        print(e)
    print(f"共保存{len(result)}个数据")
    return result


def token_write(a):
    dataframe = pd.DataFrame({'token': a})
    dataframe.to_csv(token_path, mode= 'a', index=False, sep=',',header=False)
    print("写入成功！")

if __name__ == "__main__":
    server.start()
    token = execute_sql()
    token_write(token)
    server.close()
