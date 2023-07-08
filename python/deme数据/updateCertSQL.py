import pymysql
import redis
import csv



phone_path = r"D:\deme-test-performance\paramData\phone.csv"
email_path = r"D:\deme-test-performance\paramData\email.csv"

# # 读取CSV
# def phone_read():
#     with open(phone_path) as f:
#         f_csv = csv.reader(f)
#         uid_lit = []
#         t_lit = []
#         count = 0
#         for row in f_csv:
#             row[0]

def execute_sql():
    # mysql
    db_config = {
        'host': '18.167',
        'port': 3306,
        'user': 'de',
        'passwd': 'fdFNbdJZTPxrYNGa',
        'db': 'de',
        'charset':'utf8'
    }
    conn = pymysql.connect(**db_config)
    print(conn)
    cursor=conn.cursor() #建立游标
    # sql = 'UPDATE t_user u set  u.authentication = 1,u.cert_no = '5110****4671',u.cert_name='卿**' WHERE u.phone = '18920823682' or u.email = 'oeoyzdqg0n@mail.hk.com''
    sql = r'UPDATE t_user u set  u.authentication = 1, u.cert_no = %s,u.cert_name="卿**" WHERE u.phone = %s or u.email = %s'

    # phone用户处理
    with open(phone_path) as f1:
        f_csv1 = csv.reader(f1)
        for row1 in f_csv1:
            try:
                cursor.execute(sql, ('5111****4671', row1[0], 'oeoyzdqg0n@mail.hk.com'))    #execute()执行sql语句, executemany(sql,[('小明',19,99.8),('小红',18,99.9),('晓丽',18,99.8),('小花',19,99.6)])
                conn.commit()
                print("修改成功")
            except Exception as e:
                print(e)
                conn.rollback()
                print("修改失败")
            finally:
                cursor.close()
                conn.close()
    # email用户处理
    with open(email_path) as f2:
        f_csv2 = csv.reader(f2)
        for row2 in f_csv2:
            try:
                cursor.execute(sql, ('5111****4671', row2[0], 'oeoyzdqg0n@mail.hk.com'))    #execute()执行sql语句, executemany(sql,[('小明',19,99.8),('小红',18,99.9),('晓丽',18,99.8),('小花',19,99.6)])
                conn.commit()
                print("修改成功")
            except Exception as e:
                print(e)
                conn.rollback()
                print("修改失败")
            finally:
                cursor.close()
                conn.close()



if __name__ == "__main__":
    execute_sql()
