
# 数据爬取

import requests
import json
import csv

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "content-type": "application/json",
    "cookieorigin": "https://you.ctrip.com",
    "origin": "https://you.ctrip.com",
    "priority": "u=1, i",
    "referer": "https://you.ctrip.com/",
    "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Microsoft Edge\";v=\"145\", \"Chromium\";v=\"145\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
    "x-ctx-ubt-pageid": "10650142842",
    "x-ctx-ubt-pvid": "5",
    "x-ctx-ubt-sid": "1",
    "x-ctx-ubt-vid": "1772589264504.2db8UkSyHbb7",
    "x-ctx-wclient-req": "17887c74e1529373a14bc15a39a3bd14"
}
cookies = {
    "GUID": "09031165415069615556",
    "UBT_VID": "1772589264504.2db8UkSyHbb7",
    "StartCity_Pkg": "PkgStartCity=2",
    "MKT_CKID": "1772589265944.208sp.pvzd",
    "_RGUID": "8e326a56-d3fa-4d11-b3a8-84881f1aa31d",
    "nfes_isSupportWebP": "1",
    "_bfa": "1.1772589264504.2db8UkSyHbb7.1.1772589720556.1772589731447.1.5.10650142842",
    "_jzqco": "%7C%7C%7C%7C1772589266141%7C1.427917455.1772589265947.1772589720970.1772589731726.1772589720970.1772589731726.undefined.0.0.5.5"
}
url = "https://m.ctrip.com/restapi/soa2/18109/json/getAttractionList"
params = {
    "_fxpcqlniredt": "09031165415069615556",
    "x-traceID": "09031165415069615556-1772589740479-7311122"
}

def get_json(k, v, page):
    data = {
        "head": {
            "cid": "09031165415069615556",
            "ctok": "",
            "cver": "1.0",
            "lang": "01",
            "sid": "8888",
            "syscode": "999",
            "auth": "",
            "xsid": "",
            "extension": []
        },
        "scene": "online",
        "districtId": v, # 城市（省份） id
        "index": page, # 爬该城市（省份）的第 page 页景点
        "sortType": 1,
        "count": 10,
        "filter": {
            "filterItems": [
                "0"
            ]
        },
        "coordinate": {
            "latitude": 39.23783380541338,
            "longitude": 117.05240225951094,
            "coordinateType": "WGS84"
        },
        "returnModuleType": "product"
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

    return response.json()

def get_data_info(resp, k):
    feeds = resp.get('attractionList', {}) # 获取该页景点列表，类型为字典
    rows = []
    with open('C:\\Users\\lenovo\\Desktop\\智能旅游推荐系统\\travel\\data\\data.csv', 'a', encoding = 'utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for feed in feeds:
            card = feed.get('card', {}) # 获取景点信息，类型为字典
            coordinate = card.get('coordinate', {}) # 获取景点坐标
            poiId = card.get('poiId', '') # 景点 id
            zoneName = card.get('zoneName', '') # 景点所在区域
            poiName = card.get('poiName', '') # 景点名称
            commentCount = card.get('commentCount', '') # 评论数量
            commentScore = card.get('commentScore', '') # 评分
            isAdvertisement = card.get('isAdvertisement', '') # 是否为广告内容
            isRecommend = card.get('isRecommend', '') # 是否为推荐内容
            districtName = card.get('districtName', '') # 城市名称
            coverImageUrl = card.get('coverImageUrl', '') # 景点封面图片链接
            distanceStr = card.get('distanceStr', '') # 到市中心的距离
            tagNameList = card.get('tagNameList', []) # 景点标签
            detailUrl = card.get('detailUrl', '') # 详情页链接
            marketPrice = card.get('marketPrice', '') # 市场价
            preferentialPrice = card.get('preferentialPrice', '') # 优惠价
            preferentialDesc = card.get('preferentialDesc', '') # 优惠描述
            price = card.get('price', '免费') # 价格
            priceType = card.get('priceType', '') # 价格类型
            priceTypeDesc = card.get('priceTypeDesc', '') # 价格类型描述
            isFree = card.get('isFree', '') # 是否免费
            latitude = coordinate.get('latitude') # 景点纬度
            longitude = coordinate.get('longitude') # 景点经度
            heatScore = card.get('heatScore', '') # 热度评分
            rows.append([poiId, zoneName, poiName, commentCount, commentScore, isAdvertisement, isRecommend, districtName, 
                         coverImageUrl, distanceStr, tagNameList, detailUrl, marketPrice, preferentialPrice, preferentialDesc, 
                         price, priceType, priceTypeDesc, isFree, latitude, longitude, heatScore, k])
        csvwriter.writerows(rows)

if __name__ == "__main__":
    cityDict = {
        '北京': 1,
        '上海': 2,
        '广东': 100051,
        '云南': 100007,
        '四川': 100009,
        '天津': 154,
        '河北': 100059,
        '陕西': 100057,
        '安徽': 100068,
        '湖北': 100067,
    }
    for k, v in cityDict.items():
        for page in range(1, 16):
            print(f'正在爬取{k}的第{page}页景点信息...')
            resp = get_json(k, v, page)
            get_data_info(resp, k)
