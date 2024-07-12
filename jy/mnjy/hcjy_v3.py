import pandas as pd
import finta
import ccxt
from datetime import datetime
import time

def get_historical_data(symbol, start_date, end_date, timeframe):
    """
    从 CCXT 获取指定时间段的历史 K 线数据
    """
    exchange = ccxt.okx()

    # 将字符串日期转换为毫秒时间戳
    start_ts = int(datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    end_ts = int(datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)

    # 获取历史数据
    all_ohlcv = []
    while start_ts < end_ts:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=start_ts)
        if not ohlcv:
            break
        # 过滤并处理数据
        for row in ohlcv:
            if row[0] < end_ts:
                all_ohlcv.append(row)
            else:
                # 一旦发现数据超出结束时间，立即停止添加
                break
        
        # 更新开始时间戳为最后一条数据的时间加上时间框架
        start_ts = ohlcv[-1][0] + exchange.parse_timeframe(timeframe) * 1000
        time.sleep(exchange.rateLimit / 1000)

    return pd.DataFrame(all_ohlcv, columns=["ts", "open", "high", "low", "close", "vol"])


def backtest(symbol, start_date, end_date, timeframe, initial_balance):

    data = get_historical_data(symbol, start_date, end_date, timeframe)
    print(data["close"])
    # exit(1)
    
    # 假设策略逻辑：这里我们使用一个非常简单的移动平均线交叉策略作为示例
    position_size = initial_balance / data['close'].iloc[0]  # 购买的BTC数量
    position_opened = False  # 初始化持仓状态

    for index, row in data.iterrows():
        # 计算两个不同周期的EMA
        ema_short = finta.TA.EMA(data.iloc[:index+1], 10)
        ema_long = finta.TA.EMA(data.iloc[:index+1], 240)

        # 检查是否需要开仓
        if not position_opened:
            if ema_short.iloc[-1] > ema_long.iloc[-1] and row['close'] > ema_short.iloc[-1]:  # 多头信号
                position_opened = True
                position_size = initial_balance / row['close']  # 更新持仓BTC数量
            elif ema_short.iloc[-1] < ema_long.iloc[-1] and row['close'] < ema_short.iloc[-1]:  # 空头信号
                position_opened = True
                position_size = -initial_balance / row['close']  # 更新持仓BTC数量（做空）

        # 检查是否需要平仓
        elif position_opened:
            if (ema_short.iloc[-1] < ema_long.iloc[-1] and position_size > 0) or \
               (ema_short.iloc[-1] > ema_long.iloc[-1] and position_size < 0):
                position_opened = False
                position_size = 0  # 重置持仓状态

        # 记录交易结果
        balance = initial_balance + position_size * row['close']
        print(f"Date: {row['ts']}, Position: {position_size}, Balance: {balance}")

    # 回测结束
    final_balance = initial_balance + position_size * data['close'].iloc[-1]
    print(f"Initial Balance: {initial_balance}, Final Balance: {final_balance}")

# 运行回测
if __name__ == "__main__":
    symbol = "BTC-USDT-SWAP"
    start_date = "2024-05-01 00:00:00"
    end_date = "2024-05-06 23:59:59"
    timeframe = "5m"
    initial_balance = 1000  # 初始资金

    backtest(symbol, start_date, end_date, timeframe, initial_balance)