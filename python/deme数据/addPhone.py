import random
import csv

# 生成随机phone
def create_random_phone():
    phone = "1" + random.choice(['3', '5', '7', '8', '9'])
    # phone = "1" + random.choice(['2', '4', '6', '0'])
    for i in range(0, 9):
        num = random.randint(0, 9)
        phone += str(num)
    return phone

# 生成随机email
def create_random_email():
    #用数字0-9 和字母a-z 生成随机邮箱。
    list_sum = [i for i in range(10)] + ["a", "b", "c", "d", "e", "f", "g", "h", 'i', "j", "k",
                                         "l", "M", "n", "o", "p", "q", "r", "s", "t", "u", "v",
                                         "w", "x", "y", "z"]
    email_str = ""
    email_suffix = ["@163.com", "@qq.com", "@gmail.com", "@mail.hk.com", "@foxmail.com", "@mail.com"]
    for i in range(10):
        a = str(random.choice(list_sum))
        email_str = email_str + a
    return email_str + random.choice(email_suffix)


# 生成指定数目的数据，非重复
def write_data(i, type):
    arry = []
    print("开始生成数据")
    while (i):
        i -= 1
        if ('phone' == type):
            arry.append(create_random_phone())
        elif ('email' == type):
            arry.append(create_random_email())
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
    type = input("请输入phone/email后继续...\n")
    # type = 'email'  # phone, email
    file_name = 'D:\\deme-test-performance\\paramData\\' + type + '.csv'
    data = write_data(2000000, type)
    print(f"共生成{len(data)}个元素")
    data_csv(file_name, data, type)
