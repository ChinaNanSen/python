import requests
import csv

# 发送请求并获取响应
url = "https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/home-page/query-list"
payload = {
    "pageNumber": 1,
    "pageSize": 18,  # 设置为最大值以获取尽可能多的数据
    "timeRange": "90D",
    "dataType": "ROI",
    "favoriteOnly": False,
    "hideFull": True,
    "nickname": "",
    "order": "DESC",
    "userAsset": 0
}
headers = {
    "Content-Type": "application/json"
}

all_data = []

while True:
    response = requests.request("POST", url, headers=headers, json=payload)
    data = response.json()["data"]["list"]
    all_data.extend(data)

    total = response.json()["data"]["total"]
    #print(total)
    #print(all_data[0])
    current_len = len(all_data)
    
    #print(current_len)
    if payload["pageNumber"] >= 323:
        break

    payload["pageNumber"] += 1

# 打开CSV文件并写入标题行
with open("copy_trade_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["nickname", "roi", "mdd", "sharpRatio", "winRate"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # 遍历每个交易员的数据并写入CSV文件
    for trader in all_data:
        nickname = trader["nickname"]
        roi = trader["roi"]
        mdd = trader["mdd"]
        winRate = trader["winRate"]
        sharpRatio = trader["sharpRatio"]
        writer.writerow({"nickname": nickname, "roi": roi, "mdd": mdd, "sharpRatio": sharpRatio, "winRate": winRate})