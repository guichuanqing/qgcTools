import pymysql
import redis


# mysql
db_config = {
    'host': '18.167.240.43',
    'port': 3306,
    'user': 'deme3.0',
    'passwd': 'fdFNbdJZTPxrYNGa',
    'db': 'deme3.0',
    'charset':'utf8'
}
conn = pymysql.connect(**db_config)
print(conn)
cursor=conn.cursor() #建立游标
row=cursor.execute('show databases') #execute()执行sql语句
print(row)
cursor.close()
conn.close()


# redis
redisArgs={
    'host':'119.23.73.197',
    'port':6379,
    'password':'123456',
}
re=redis.Redis(**redisArgs)
print(re)#Redis>>