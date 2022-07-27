import random
import csv

# 生成随机phone
def create_random_phone():
    phone_virtual = ["1700","1701","1702","162","1703","1705","1706","165","1704","1707","1708","1709","171","167",
                     "1349","174","140","141","144","146","148"]
    phone_lit = []
    for i in phone_virtual:
        phone = i
        for j in range(0, 11 - len(i)):
            num = random.randint(0, 9)
            phone += str(num)
        phone_lit.append(phone)
    return phone_lit


# 生成指定数目的数据，非重复
def write_data(i):
    arry = []
    print("开始生成数据")
    while (i):
        i -= 1
        arry.extend(create_random_phone())
    print("生成数据完毕！")
    return list(set(arry))


# 打开文件流写入并保存
def data_csv(file_name, datas, type):
    print("开始写入数据到：", file_name)
    with open(file_name, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([type])
        for i in range(len(datas)):
            writer.writerow([datas[i]])
    print("插入并保存完毕！")


if __name__ == "__main__":
    type = 'virtualPhone'  # phone
    file_name = 'D:\\qgcTools\\虚拟手机号\\' + type + '.csv'
    data = write_data(10)
    print(f"共生成{len(data)}个元素")
    data_csv(file_name, data, type)
