import okx.Account as Account
import okx.Trade as Trade
import okx.MarketData as MarketData
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import time
import finta
import configparser

#测试

# API 初始化
# 从配置文件读取API初始化信息
config = configparser.ConfigParser()
config.read('config.ini')

apikey = config['OKX']['apikey']
secretkey = config['OKX']['secretkey']
passphrase = config['OKX']['passphrase']
flag = config['OKX']['flag']  # 实盘:0 , 模拟盘:1

accountAPI = Account.AccountAPI(apikey, secretkey, passphrase, False, flag)
tradeAPI = Trade.TradeAPI(apikey, secretkey, passphrase, False, flag)
marketDataAPI = MarketData.MarketAPI(flag=flag)
bz = "ETH-USDT"
dbz = "ETH"

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

def get_historical_data(inst_id, limit=160):
    for attempt in range(3):  # 尝试次数
        try:
            historical_data = marketDataAPI.get_candlesticks(
                instId=inst_id,
                limit=str(limit)
            )
            return historical_data
        except Exception as e:
            print(f"Error: {e}")
            if attempt < 2:  # 如果这不是最后一次尝试，等待2秒然后再次尝试
                time.sleep(2)
            else:
                print("Failed to get historical data after 3 attempts.")
                return None

def process_data(historical_data):
    data = pd.DataFrame(historical_data["data"], columns=[
        "ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"])
    data['ts'] = data['ts'].apply(
        lambda x: datetime.datetime.fromtimestamp(int(x) / 1000))
    data['ts'] = data['ts'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data.set_index('ts', inplace=True)
    return data

def calculate_ma(data, window):
    return finta.TA.SMA(data, window)

def get_account_balance(currency):
    for attempt in range(3):  # 尝试次数
        try:
            result = accountAPI.get_account_balance(ccy=currency)
            return result["data"][0]
        except Exception as e:
            print(f"Error: {e}")
            if attempt < 2:  # 如果这不是最后一次尝试，等待2秒然后再次尝试
                time.sleep(2)
            else:
                print("Failed to get account balance after 3 attempts.")
                return None  # 或者返回一个错误值/异常，让调用者知道请求失败

def execute_trade(data, ma15, ma150):
    for attempt in range(3):  # 尝试次数
        try:
            # 获取历史数据
            historical_data = marketDataAPI.get_candlesticks(
                instId=bz,
                limit="160"
            )
            data = pd.DataFrame(historical_data["data"], columns=[
                "ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"])
            data['ts'] = data['ts'].apply(lambda x: datetime.datetime.fromtimestamp(int(x) / 1000))
            data['ts'] = data['ts'].dt.strftime('%Y-%m-%d %H:%M:%S')
            data.set_index('ts', inplace=True)

            ma15 = finta.TA.SMA(data, 15)
            ma150 = finta.TA.SMA(data, 150)

            # 检查交叉点并执行交易逻辑
            if ma15.iloc[15] > ma150.iloc[150]:
                # 买入信号
                account_info = get_account_balance("USDT")
                if account_info:
                    cash_balance = account_info["details"][0]["cashBal"]
                    if float(cash_balance) > 10:
                        result = tradeAPI.place_order(
                            instId=bz,
                            tdMode="cash",
                            ccy="USDT",
                            side="buy",
                            ordType="market",
                            sz=cash_balance
                        )
                        print("Buy order executed.")
                    else:
                        print("Buy operation ignored, insufficient USDT balance.")
                else:
                    print("Failed to get account balance for USDT.")

            elif ma15.iloc[15] < ma150.iloc[150]:
                # 卖出信号
                account_info = get_account_balance(dbz)
                if account_info:
                    asset_balance = account_info["details"][0]["cashBal"]
                    if float(asset_balance) > 0:
                        result = tradeAPI.place_order(
                            instId=bz,
                            tdMode="cash",
                            ccy=dbz,
                            side="sell",
                            ordType="market",
                            sz=asset_balance
                        )
                        print("Sell order executed.")
                    else:
                        print("Sell operation ignored, insufficient asset balance.")
                else:
                    print(f"Failed to get account balance for {dbz}.")

            else:
                print("No trading signal.")
            # 如果代码运行成功，跳出循环
            break
        except Exception as e:
            print(f"Error: {e}")
            if attempt < 2:  # 如果这不是最后一次尝试，等待2秒然后再次尝试
                time.sleep(2)
            else:
                print("Failed to execute trading logic after 3 attempts.")

def jy():
    for attempt in range(3):  # 尝试次数
        try:
            historical_data = get_historical_data(bz)
            if historical_data is None:
                raise ValueError("Failed to get historical data")

            data = process_data(historical_data)
            ma15 = calculate_ma(data, 15)
            ma150 = calculate_ma(data, 150)
            
            buy_signals, sell_signals = execute_trade(data, ma15, ma150)
            
            # ... other logic ...
            # 画图功能
            # plot_data(data, ma15, ma150, buy_signals, sell_signals)

            break  # 如果代码运行成功，跳出循环
        except Exception as e:
            print(f"Error: {e}")
            if attempt < 2:  # 如果这不是最后一次尝试，等待2秒然后再次尝试
                time.sleep(2)
            else:
                print("Failed to execute trading logic after 3 attempts.")

if __name__ == "__main__":
    while True:
        time.sleep(3)
        jy()
