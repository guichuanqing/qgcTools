import requests
import datetime
import time


addr = "https://test-admin-api.demeworld.cn"
login_url = r'/demeAdmin/manager/login'
api_url = r'/demeAdmin/collection/addCollectionAndUp'
header = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '1130',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'origin': 'https://test-admin.demeworld.cn',
    'referer': 'https://test-admin.demeworld.cn/',
}
dataChain = {"activityDays": None,
        "blindboxContentList":[],
        "collectionCode":"xxxccc",
        "collectionContent":"https://image.demeworld.cn/image/W2GE2.jpg",
        "collectionDescribe":"这是藏品描述哈哈哈哈哈哈哈哈哈哈或或或或或或或或或或",
        "collectionLabel":"藏品标签上链",
        "collectionName":"qgc的上链藏品09",
        "collectionPrice":"0.01",
        "collectionType":2,
        "coverPhoto":"https://image.demeworld.cn/image/LXBL006.jpg",
        "createBy":34,
        "createName":"qgc",
        "downloadFile":"https://image.demeworld.cn/image/BM4C7a7da2f25acf4179f11273c63d5b442a.gif",
        "groundState":"009",
        "isSetupHot":"Y",
        "isWhitelist":1,
        "limitNumber":100,
        "pictureFile":"https://image.demeworld.cn/image/FMCF9bd8fa6c7968522b24dcaee30da67ab0.gif",
        "preSalePhoto":"https://image.demeworld.cn/image/CBZ5003.jpg",
        "reserveNumber":50,
        "reserveUseNumber":50,
        "saleNumber":50,
        "saleTime":"2022-10-05 19:26:56",
        "saleUseNumber":50,
        "whitelistNumber":0,
        "whitelistUseNumber":0,
        "buyProtocol":"<p>这是购买协议 哈哈哈哈哈哈哈哈哈哈或或或或或或或或或或或或或或或或或或或或或或或或或或或或或或或或或或或</p>",
        "giveDaysRequired1":"0",
        "giveDaysRequired2":"0",
        "whitelistGainConditionsList":[],
        "whitelistMedalExchangeList":[],
        "whitelistExchangeLimit":"",
        "whitelistRedeemed":0,
        "whitelistOffer":0,
        "whitelistConditions":"这是白名单条件 是 试试",
        "advancePayTime":0,
        "reserveTime":0,
        "maxPurchaseQuantity":"20",
        "properties":{"properties":[{"trait_type":"base","value":"starf"}]},
        "rankings":{"rankings":[{"trait_type":"level","value":5}]},
        "stats":{"stats":[{"trait_type":"generation","value":2,"display_type":"number"}]},
        "contractCode":"13TAIBAO",
        "componentPhoto":"https://image.demeworld.cn/file/ZV5YEwB3R9mmv6.png"
        }

# 登录后台
def con_manage():
    data = {"userName": "qgc1", "password": "/J+mraC7w/pcfK16djHSeQ=="}
    res = requests.post(url=addr+login_url, headers=header, json=data).json()['data']['token']
    print("登录成功！")
    return res


# 多次新增变更data数据
def data_format(data, i):
    if type(data) is dict:
        time_str = datetime.datetime.strftime(datetime.datetime.now(), '%m%d%H%M')
        for k, v in data.items():
            if k == "collectionCode":
                data[k] = "qgcx1234567890" + time_str + str(i)
            if k == 'collectionName':
                data[k] = "qgc的上链藏品正确属性" + time_str + '-' + str(i)
            if k == 'saleTime':
                # data[k] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')     # 单独设置出售时间
                data[k] = "2022-07-25 15:39:28"  # 单独设置出售时间
    return data

  # 新增藏品
def add_collection(token, i):
    data = {
             "activityDays": None,
             "advancePayTime":0,
             "auditionFile": "",
             "blindboxContentList": [],
              "collectionCode": "qgc0725001",
              "collectionContent": "https://deme3.oss-cn-chengdu.aliyuncs.com/image/XNP5详情图-Ferry P 签名衣服_02.png,https://deme3.oss-cn-chengdu.aliyuncs.com/image/WHCV详情图-Ferry P 签名衣服_03.png,https://deme3.oss-cn-chengdu.aliyuncs.com/image/A9NM详情图-Ferry P 签名衣服_04.png,https://deme3.oss-cn-chengdu.aliyuncs.com/image/74QX详情图-Ferry P 签名衣服_05.png",
              "collectionDescribe": "商品：\n大甩卖！！！清仓跳楼价！！！\n买不了吃亏，买不了上当。包开包甜，不甜不要钱。",
              "collectionLabel": "衣服",
              "collectionName": "qgc的藏品",
              "collectionPrice": "0.01",
              "collectionType": 2,
              "coverPhoto": "https://deme3.oss-cn-chengdu.aliyuncs.com/image/G3JW封面图-Ferry P 签名衣服.jpg",
              "createBy": "34",
              "createName": "qgc",
              "downloadFile": "https://deme3.oss-cn-chengdu.aliyuncs.com/image/B9HF封面图-Ferry P 签名衣服.jpg",
              "groundState": "009",
              "isSetupHot": "Y",
              "isWhitelist": 1,
              "limitNumber": 50,
              "maxPurchaseQuantity": "10000",
              "pictureFile": "https://deme3.oss-cn-chengdu.aliyuncs.com/image/G8VP详情图-Ferry P 签名衣服_01.png,https://deme3.oss-cn-chengdu.aliyuncs.com/image/D3L2封面图-Ferry P 签名衣服.jpg",
              "preSalePhoto": "https://deme3.oss-cn-chengdu.aliyuncs.com/image/3QYS封面图-Ferry P 签名衣服.jpg",
              "reserveNumber": 50,
              "reserveTime": 0,
              "reserveUseNumber": 50,
              "saleNumber": 0,
              "saleTime": "2022-07-25 17:00:00",
              "saleUseNumber": 0,
              "whitelistConditions": None,
              "whitelistNumber": 0,
              "whitelistUseNumber": 0,
              "whitelistOffer": "0",
              "buyProtocol": "<p>这是购买协议哈哈哈哈哈哈</p>",
              "giveDaysRequired1": "0",
              "giveDaysRequired2": "0"
              }
    header['token'] = token
    data = data_format(dataChain, i)
    print("开始新增藏品...")
    res = requests.post(url=addr+api_url, headers=header, json=data).json()
    time.sleep(1)
    print(res)
    # for i in res:
    #     print(i)


if __name__ == "__main__":
    num = int(input("请输入新增藏品个数：\n"))
    token = con_manage()
    for i in range(0, num):
        add_collection(token, i)