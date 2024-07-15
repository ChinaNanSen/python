import pandas as pd
import ccxt
from datetime import datetime
import numpy as np
import okx.Account as Account
import okx.Trade as Trade
import okx.MarketData as MarketData
import time
import finta
import sys



# 初始化交易所
exchange = ccxt.okx()

def get_historical_data(symbol, start_date, end_date, timeframe):
    """
    从交易所获取指定时间段的历史 K 线数据
    """
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

    return pd.DataFrame(all_ohlcv, columns=["ts", "open", "high", "low", "close", "volume"])


# def calculate_atr(data, period):
#     """
#     计算平均真实波动范围（ATR）
#     """
#     tr_list = []
#     for i in range(1, len(data)):
#         high = data['high'].iloc[i]
#         low = data['low'].iloc[i]
#         close_prev = data['close'].iloc[i - 1]
#         tr = max(high - low, abs(high - close_prev), abs(low - close_prev))
#         tr_list.append(tr)
#     # 计算ATR
#     atr = int(np.floor(np.mean(tr_list[-period:])))
#     return atr

# def calculate_ema(data, span, column_name):
#     """
#     计算指数移动平均线（EMA）
#     """
#     # EMA公式：EMA = (Close × (Span - 1) / (Span)) + (Previous EMA × (Span - 1) / Span))
#     data[column_name] = data['close'].ewm(span=span, adjust=False).mean()
#     return data

def backtest(symbol, start_date, end_date, timeframe, initial_balance):
    """
    执行回测，使用双均线策略（EMA5和EMA20）
    """

    # 创建或打开输出文件
    output_file = open('backtest_results.txt', 'w', encoding='utf-8')
    
    # # 重定向标准输出到文件
    original_stdout = sys.stdout
    sys.stdout = output_file

    data = get_historical_data(symbol, start_date, end_date, timeframe)
    data['ts'] = pd.to_datetime(data['ts'], unit='ms')
    # 如果数据已经是UTC时间，那么首先将其本地化到UTC
    data['ts'] = data['ts'].dt.tz_localize('UTC')

    # 然后将其转换到您的本地时区，例如'Asia/Shanghai'（东八区）
    data['ts'] = data['ts'].dt.tz_convert('Asia/Shanghai')

    #计算 MACD
    # print(data)
    data['sma10'] = finta.TA.EMA(data,10)
    data['sma20'] = finta.TA.EMA(data,20)
    data['ema10'] = finta.TA.SMA(data,10)
    data['ema5'] = finta.TA.SMA(data,5)
    data['ema20'] = finta.TA.SMA(data,20)
    data['ema30'] = finta.TA.SMA(data,30)
    data['ema150'] = finta.TA.SMA(data,170)
    # print(data['ts'].iloc[149],data['ema20'].iloc[149])
    # print(data['ts'].iloc[14],data['ema10'].iloc[14])
    # exit(1)
    data['rsi14'] = finta.TA.RSI(data)
    mac = finta.TA.MACD(data,13,34)
    # mac = finta.TA.MACD(data,12,26)
    data = data.join(mac)
    # data = data.join(data['ema10'])
    # data = data.join(data['ema20'])
    # print(data.iloc[-1])
    # print(data.iloc[-2])
    # print(data )

    # # 计算EMA5和EMA20
    # data['EMA5'] = finta.TA.EMA(data, 15)
    # data['EMA20'] = finta.TA.EMA(data, 150)
    # print( data['timestamp'],data['EMA5'])
    # exit(1)
    

    # exit(1)
    # 回测逻辑
    balance = initial_balance
    totee = 0
    position = 0  # 持仓数量
    position_open_index = None  # 开仓时的索引

    for index, row in data.iterrows():
        # print(row['macd'])
        # print(index)
        # print(data['macd'].iloc[index - 1])
        # print(row['macd'])
        # exit(1)
        # 检查是否需要开多头仓位
        if position == 0 and balance > 100 and data['macd'].iloc[index - 1] < 0 and  row['macd'] > 0 and row['sma20'] > row['sma10'] :
        # if position == 0 and balance > 100 and row['macd'] > 0 and row['ema5'] > row['ema20'] :
        # if position == 0 and balance > 100  and row['ema20'] < row['ema10'] :
            amount = balance * 0.5
            position = amount / row['close']  # 计算开多仓的数量
            position_open_index = index  # 记录开仓的索引
            stee = row['close'] * position * 0.002
            balance -= stee
            totee += stee
            # print(row)
            print(f"Date: {row['ts']}, Position start : {position}, Balance: {balance}, Price: {row['close']}, stee: {stee}")

        # 检查是否需要平多头仓位
        # if position > 0  and row['macd'] < 0 and row['ema5'] < row['ema20']:
        if position > 0 and data['macd'].iloc[index - 1] > 0 and row['macd'] < 0 and row['sma20'] < row['sma10']:
        # if position > 0 and row['ema20'] > row['ema10']:

            # 计算平仓后的收益
            etee = row['close'] * position * 0.002
            position_pnl = (row['close'] - data.iloc[position_open_index]['close']) * position * 20 - etee
            balance += position_pnl  # 更新余额
            totee += etee
            position = 0  # 重置持仓
            print(f"Date: {row['ts']}, Position Closed: {position}, Balance: {balance}, PnL: {position_pnl}, Price: {row['close']}, etee: {etee}")

        # 打印当前持仓和余额
        #print(f"Date: {row['ts']}, Position: {position}, Balance: {balance}, Price: {row['close']}")

    # 回测结束
    final_balance = balance
    print(f"Initial Balance: {initial_balance}, Final Balance: {final_balance}, Total Tee: {totee}")

    # 恢复标准输出并关闭文件
    sys.stdout = original_stdout
    output_file.close()

    print(f"Backtest results have been saved to 'backtest_results.txt'")


# 运行回测
if __name__ == "__main__":
    symbol = "BTC-USDT-SWAP"  # 交易对
    start_date = "2022-11-14 00:00:00"
    end_date = "2024-11-21 23:59:59"
    timeframe = "6h"  # 时间框架，这里使用1天
    initial_balance = 5000  # 初始资金

    backtest(symbol, start_date, end_date, timeframe, initial_balance)

  

   
