import pandas as pd
import datetime
import finta
import okx.MarketData as MarketData

marketDataAPI = MarketData.MarketAPI(flag="1")

# 获取历史数据
def get_historical_data(instId, bar):
    historical_data = marketDataAPI.get_history_candlesticks(
        instId=instId,
        # after='1698854399000',
        before='1696093200000',
        bar=bar
    )
    # print(historical_data)
    data = pd.DataFrame(historical_data["data"], columns=[
        "ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"])

    data['ts'] = pd.to_datetime(data['ts'],unit='ms')  # 转换为日期时间格式
    data['ts'] = data['ts'].dt.strftime('%Y-%m-%d %H:%M:%S')  # 格式化日期时间
    data.set_index('ts', inplace=True)

    return data

# 简单移动平均线策略
def simple_moving_average_strategy(data, short_period, long_period):
    signals = []
    position = None

    for i in range(long_period, len(data)):
        short_ma = data['close'].iloc[i - short_period:i].mean()
        long_ma = data['close'].iloc[i - long_period:i].mean()

        if short_ma > long_ma and position is None:
            signals.append("Buy")
            position = "Long"
        elif short_ma < long_ma and position == "Long":
            signals.append("Sell")
            position = None
        else:
            signals.append("Hold")

    return signals

# 示例使用
historical_data = get_historical_data("ETH-USDT", "1H")

print(historical_data)

short_period = 15
long_period = 150
signals = simple_moving_average_strategy(historical_data, short_period, long_period)
print(signals)

# 执行回测
balance = 1000  # 初始资金
position = None
shares = 0

for i in range(len(signals)):
    if signals[i] == "Buy" and position is None:
        # 执行买入逻辑
        position = "Long"
        price = historical_data['close'].iloc[i]
        shares = balance / price
        balance = 0
    elif signals[i] == "Sell" and position == "Long":
        # 执行卖出逻辑
        position = None
        price = historical_data['close'].iloc[i]
        balance = shares * price

# 输出最终资金
print("Final Balance:", balance)
