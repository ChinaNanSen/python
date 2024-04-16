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
    # print(response.json())
    data = response.json()["data"]["list"]
    all_data.extend(data)

    total = response.json()["data"]["total"]
    current_len = len(all_data)
    

    if payload["pageNumber"] >= math.ceil(total/payload["pageSize"]):
    # if payload["pageNumber"] >= 1:
        break

    payload["pageNumber"] += 1

# 多线程获取每个交易员的交易开始时间
def get_start_time(trader):
    portfolio_id = trader["leadPortfolioId"]
    print(portfolio_id)
    detail_url = f"https://www.binance.com/bapi/futures/v1/friendly/future/copy-trade/lead-portfolio/detail?portfolioId={portfolio_id}"
    detail_response = requests.get(detail_url)
    detail_data = detail_response.json().get("data")
    # print(detail_data)

    if detail_data and "startTime" in detail_data:
        start_time = detail_data["startTime"]
        trader["startTime"] = start_time
        
    else:
        trader["startTime"] = 0  # 设置默认值为 0

    if detail_data and "marginBalance" in detail_data:
        marginBalance = detail_data["marginBalance"]
        trader["marginBalance"] = marginBalance
        
    else:
        trader["marginBalance"] = 0  # 设置默认值为 0

    
    if detail_data and "copierPnl" in detail_data:
        marginBalance = detail_data["copierPnl"]
        trader["copierPnl"] = marginBalance
        
    else:
        trader["copierPnl"] = 0  # 设置默认值为 0

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(get_start_time, trader) for trader in all_data]
    for future in as_completed(futures):
        future.result()

# 定义计算交易天数的函数
def calculate_trading_days(trader):
    now = datetime.now().timestamp() * 1000  # 获取当前时间戳，并转换为毫秒
    start_time = trader.get("startTime", 0)
    if start_time:
        trading_days = (now - start_time) // (1000 * 60 * 60 * 24)
        trader["tradingDays"] = int(trading_days)
    else:
        trader["tradingDays"] = 0

# 定义写入CSV文件的函数
def write_to_csv(trader, csvfile, writer):
    trader_data = {
        "nickname": trader["nickname"],
        "roi": trader["roi"],
        "mdd": trader["mdd"],
        "apiKeyTag": trader["apiKeyTag"],#api标签
        "winRate": trader["winRate"],
        "pnl": trader["pnl"],#盈亏
        "aum": trader["aum"],#资产规模
        "marginBalance": trader["marginBalance"],#保证金余额
        "sharpRatio": trader["sharpRatio"],
        "copierPnl": trader["copierPnl"], #跟单者盈亏
        "tradingDays": trader["tradingDays"]
    }
    writer.writerow(trader_data)

# 使用多线程计算交易天数和写入CSV文件
with ThreadPoolExecutor(max_workers=10) as executor:
    # 计算交易天数
    trading_days_futures = [executor.submit(calculate_trading_days, trader) for trader in all_data]
    
    # 等待计算交易天数的任务完成
    for future in as_completed(trading_days_futures):
        future.result()  # 获取结果，确保每个交易员的交易天数都已计算

    # 打开CSV文件准备写入
    with open("newj30_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["nickname", "roi", "mdd", "winRate", "tradingDays", "sharpRatio", "pnl", "copierPnl", "aum", "marginBalance", "apiKeyTag"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # 写入CSV文件
        write_futures = [executor.submit(write_to_csv, trader, csvfile, writer) for trader in all_data]
        
        # 等待写入CSV文件的任务完成
        for future in as_completed(write_futures):
            future.result()  # 确保所有数据都已写入文件