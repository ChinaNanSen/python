import okx.MarketData as MarketData
import configparser
import pandas as pd
import time
from datetime import datetime
import finta
import ccxt

# 初始化API
config = configparser.ConfigParser()
config.read('config.ini')
flag = config['OKX']['flag']
marketDataAPI = MarketData.MarketAPI(flag=flag)


# def get_monthly_historical_data(instId, year, month, bar):
def get_monthly_historical_data():
    # # 计算月份的开始和结束时间戳
    # start_date = datetime(year, month, 1)
    # end_date = datetime(
    #     year, month + 2, 28) if month < 12 else datetime(year + 1, 1, 1)
    # start_ts = int(start_date.timestamp()) * 1000
    # end_ts = int(end_date.timestamp()) * 1000

    # print(start_date, end_date)

    # all_data = []
    # last_ts = end_ts

  

    
    # 获取历史数据
    # ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

    # 转换为 DataFrame
    # df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    # df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    # return pd.DataFrame(all_ohlcv, columns=["ts", "open", "high", "low", "close", "vol"])

    # 显示数据
    # print(df)
    # exit(33)

    # while True:
        # 创建交易所实例
    exchange = ccxt.okx()

    # 设置交易对和时间框架
    symbol = 'BTC/USDT'  # 比特币与USDT的交易对
    timeframe = '30m'  # 时间框架为1小时

    # 设定开始和结束时间（示例）
    start_str = '2023-11-28 00:00:00'
    end_str = '2023-12-10 00:00:00'

    # 将字符串日期转换为毫秒时间戳
    start_ts = int(datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
    end_ts = int(datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)

    # 获取历史数据
    all_ohlcv = []
    while start_ts < end_ts:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=start_ts)
        # ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
        # print(ohlcv)
        # exit(11)
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

    # print(all_ohlcv)
    # exit(13)
    return pd.DataFrame(all_ohlcv, columns=["ts", "open", "high", "low", "close", "vol"])
    
        # result = marketDataAPI.get_history_candlesticks(
        #     # result = marketDataAPI.get_candlesticks(
        #     instId=instId,
        #     bar=bar,
        #     before=str(start_ts),
        #     # after="1699852860000",
        #     after=str(last_ts),
        #     limit="100"
        # )
        # print(last_ts, start_ts)

    
        # result = ccxt_historical_data()

    #     if 'data' in result and len(result['data']) > 0:
    #         batch_data = result['data']
    #         first_ts = int(batch_data[0][0])

    #         if first_ts < start_ts:
    #             # 过滤掉开始时间之前的数据
    #             batch_data = [x for x in batch_data if int(x[0]) >= start_ts]
    #             all_data.extend(batch_data)
    #             break
    #         else:
    #             all_data.extend(batch_data)
    #             last_ts = batch_data[-1][0]  # 更新时间戳为最后一条数据的时间戳

    #         time.sleep(0.1)  # 遵守API的限速规则
    #     else:
    #         break  # 如果没有数据返回，则停止循环

    # return pd.DataFrame(all_data, columns=[
    #     "ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"])
    


# 示例用法
# 获取2023年5月的BTC-USDT历史数据
# datas = get_monthly_historical_data("BTC-USDT", 2023, 10, "5m")

# datas = get_monthly_historical_data()
# datas['ts'] = pd.to_datetime(datas['ts'], unit='ms')
# datas['ts'] = datas['ts'].dt.strftime('%Y-%m-%d %H:%M:%S')
# datas.set_index('ts', inplace=True)
csv_file_name = 'historical_data_2023_05.csv'
# datas.to_csv(csv_file_name)
print("数据写入成功！！！")


# 假设data1是您的历史数据DataFrame
data1 = pd.read_csv(csv_file_name)
# data1 = data1.iloc[::-1]

# print(data1)
# data1['mas'] = finta.TA.EMA(data1,15)
# print(data1['mas'])
# print(data1['ts'].iloc[0],"   ",data1['mas'].iloc[0])
# bbands = finta.TA.BBANDS(data1)
# # print(bbands)
# print(data1['ts'].iloc[19],"   ",bbands['BB_UPPER'].iloc[19])

# data1 = data1.sort_values(by='ts')
# print(data1)
data1.set_index('ts', inplace=True)

# 计算移动平均
# data1['mas'] = finta.TA.EMA(data1,15)
# print(data1['mas'])
# print(data1['ts'].iloc[-1],"   ",data1['mas'].iloc[-1])
# print(data1['mas'].iloc[13] )
# print(data1)
mal = finta.TA.SMA(data1, 150)
mas = finta.TA.SMA(data1, 15)
ma = finta.TA.SMA(data1, 60)

data1['mal'] = mal.iloc[-1]
data1['mas'] = mas.iloc[-1]
data1['ma'] = ma.iloc[-1]

sar = finta.TA.SAR(data1)
# print(sar.iloc[0])
# exit(112)
data1['emal'] = finta.TA.EMA(data1, 150)
data1['emas'] = finta.TA.EMA(data1, 15)
# data1['rsi'] = finta.TA.RSI(data1)
macd = finta.TA.MACD(data1)
# data1['macd'] = macd.iloc[-1]['MACD']
# data1['sig'] = macd.iloc[-1]['SIGNAL']
# bbands = finta.TA.BBANDS(data1,30,3)
bbands = finta.TA.BBANDS(data1)
print(bbands['BB_UPPER'])
data1['bu'] = bbands.iloc[-27]['BB_UPPER']
# print(data1['bu'])
data1['bm'] = bbands.iloc[-27]['BB_MIDDLE']
data1['bl'] = bbands.iloc[-27]['BB_LOWER']
cn = data1['close'].iloc[0]
hn = data1['high'].iloc[0]
ln = data1['low'].iloc[0]
print(data1)
ich = finta.TA.ICHIMOKU(data1)
data1['ic'] = ich.iloc[-27]['CHIKOU']

# # print(ich)
# print(data1['ic'])
# # print(data1['ic'])
# # print(data1['bu'])
# print(bbands)
# print(data1['bl'])
# # print(data1)
# # print(ln)
# # print(hn)
# exit(111)
# print(bbands )

# print(data1['ts'].iloc[-1],"   ",bbands['BB_UPPER'].iloc[-1])
# print(bbands['BB_LOWER'])
# exit(1)
# print(data1['bl'])
# print(data1['mas'])

# exit(103)
# atr = finta.TA.ATR(data1)
# stop_loss = data1['close'] - atr * multiplier


# 定义手续费和滑点
commission_rate = 0.001
# slippage = 0
slippage = 0.0005

# 初始化账户余额和持仓
initial_balance = 2000
balance = initial_balance
position = 0
total_commission = 0  # 总手续费

# 记录交易
trades = []
# print(data1)
exit(112)

# 回测逻辑
for index, row in data1.iterrows():
    # print(row['ts'])
    if pd.isna(row['emas']) or pd.isna(row['emal']) or pd.isna(row['bu']) or pd.isna(row['bl'] ):  # 跳过还未生成MA的行
        continue

   
    lprice = row['low'] * (1 + slippage)  # 模拟实际成交价格（包括滑点）
    hprice = row['high'] * (1 + slippage)  # 模拟实际成交价格（包括滑点）
    price = row['close'] * (1 + slippage)  # 模拟实际成交价格（包括滑点）

    # 检查买入信号
    
    print(row)
    # exit(1)
    # print(row['ic'])
    # print(row['bl'])

    if row['mas'] > row['mal'] and balance > 0:
    # if row['emas'] > row['emal'] and balance > 0:
    # if row['close'] < row['bl'] and balance > 0:
    # if row['close'] > row['ma'] and balance > 0:
    # if row['low'] < row['bl'] and balance > 0:
    # if row['emal'] < row['close'] and row['low'] < row['bl'] and balance > 0:
        amount = balance / lprice
        # amount = balance / price
        fee = amount * lprice * commission_rate
        # fee = amount * price * commission_rate
        balance -= amount * lprice + fee
        # balance -= amount * price + fee
        position += amount
        total_commission += fee  # 累加手续费
        trades.append({'type': 'buy', 'price': lprice,
        # trades.append({'type': 'buy', 'price': price,
                      'amount': amount, 'fee': fee, 'timestamp': row.name})

    # 检查卖出信号

    elif row['mas'] < row['mal'] and position > 0:
    # elif row['emas'] < row['emal'] and position > 0:
    # elif row['close'] > row['bu'] and position > 0:
    # elif row['close'] < row['ma'] and position > 0:
    # elif row['high'] > row['bu'] and position > 0:
    # elif  row['high'] > row['bu'] and balance > 0:
        fee = position * hprice * commission_rate
        # fee = position * price * commission_rate
        trade_amount = position  # 保存当前持仓量用于交易记录
        balance += position * hprice - fee
        # balance += position * price - fee
        position = 0
        trades.append({'type': 'sell', 'price': hprice,
        # trades.append({'type': 'sell', 'price': price,
                      'amount': trade_amount, 'fee': fee, 'timestamp': row.name})

# 性能评估
# final_balance = balance + position * data1['high'].iloc[-1]
final_balance = balance + position * data1['close'].iloc[-1]
performance = final_balance - initial_balance

# 将交易记录输出到文件
trades_df = pd.DataFrame(trades)
trades_df.to_csv('trading_record.csv', index=False)

# 打印结果
print(
    f"Initial Balance: {initial_balance}, Final Balance: {final_balance}, Performance: {performance}, Total Commission Paid: {total_commission}")
