import requests
import csv
import math
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 发送请求并获取响应
url = "https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/home-page/query-list"
payload = {
    "pageNumber": 1,
    "pageSize": 20,
    "timeRange": "30D",
    "dataType": "ROI",
    "favoriteOnly": False,
    "hideFull": False,
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
    current_len = len(all_data)

    if payload["pageNumber"] >= math.ceil(total/payload["pageSize"]):
        break

    payload["pageNumber"] += 1

# 多线程获取每个交易员的交易开始时间
def get_start_time(trader):
    portfolio_id = trader["leadPortfolioId"]
    detail_url = f"https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/lead-portfolio/detail?portfolioId={portfolio_id}"
    detail_response = requests.get(detail_url)
    detail_data = detail_response.json().get("data")

    if detail_data and "startTime" in detail_data:
        start_time = detail_data["startTime"]
        trader["startTime"] = start_time
    else:
        trader["startTime"] = 0  # 设置默认值为 0

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(get_start_time, trader) for trader in all_data]
    for future in as_completed(futures):
        future.result()

# 计算每个交易员的交易天数
now = datetime.now().timestamp() * 1000  # 获取当前时间戳,并转换为毫秒
for trader in all_data:
    start_time = trader["startTime"]
    if start_time != 0:
        trading_days = (now - start_time) // (1000 * 60 * 60 * 24)
        trader["tradingDays"] = int(trading_days)
    else:
        trader["tradingDays"] = 0

# 打开CSV文件并写入标题行
with open("zz_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["nickname", "roi", "mdd", "sharpRatio", "winRate", "tradingDays"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # 遍历每个交易员的数据并写入CSV文件
    for trader in all_data:
        nickname = trader["nickname"]
        roi = trader["roi"]
        mdd = trader["mdd"]
        winRate = trader["winRate"]
        sharpRatio = trader["sharpRatio"]
        tradingDays = trader["tradingDays"]
        writer.writerow({"nickname": nickname, "roi": roi, "mdd": mdd, "sharpRatio": sharpRatio, "winRate": winRate, "tradingDays": tradingDays})