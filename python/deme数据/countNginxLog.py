import os,json
import pandas as pd
import datetime


'''
全局参数
'''

# 日志文件存放目录
logDir = r"C:\Users\qgc\Desktop"
# 源日志文件，3天汇总
logFile= r"C:\Users\qgc\Desktop\api.demeworld.cn.log"
# 清洗完的文件绝对路径
date = datetime.datetime.strftime(datetime.datetime.now(), '%H%M')
print(date)
resultName = logDir+"\\result-" + date +".xlsx"

print ('开始数据预处理')

# 定义过滤函数，过滤掉无效uri
filt = ['.js','css','images','static']
filt2 = ['/deme/']
def filter_invalid_str(s,filt):
    if s.isdigit() or s == '/' or s =='/null':
        return 0
    for i in filt:
        if i in s:
            return 0
    for j in filt2:
        if j not in s:
            return 0
    else:
        return 1

print('开始数据分析')


# 统计各个uri的访问量,算出日业务量，过滤掉请求次数为0的uri
def uri_statistics(time):
    result = {}
    count = 0
    with open(logFile, 'r', encoding="utf-8") as fr:
        for i in fr:
            line = i.split()
            if time in line[3]:
                k = line[6].split("?")[0]
                if filter_invalid_str(k,filt):
                    count+=1
                    if k not in result.keys():
                        result[k] = 1
                    elif k in result.keys():
                        result[k] += 1
                    else:
                        print("%s 存入字典时，key没有找到！"%k)
    print(f"共分析{count}条数据，找到{len(result)}接口数据")
    if len(result) >0:
        # 将清洗完的接口统计数据写入目标文件
        if os.path.exists(resultName):
            os.remove(resultName)
        pandas_to_excel(resultName, result)
    else:
        print("未生成txt数据")

def pandas_to_excel(f, data):
    file_path = pd.ExcelWriter(f)
    try:
        df = pd.DataFrame(pd.Series(data), columns=['total'])
        df = df.reset_index().rename(columns={'index': 'apiUri'})
        df.to_excel(file_path, encoding='utf-8')
        file_path.save()
    except Exception as e:
        print("Error:", e)
    print("excel处理数据成功")


if __name__ == '__main__':
    time = "13/Jul/2022:09"
    uri_statistics(time)