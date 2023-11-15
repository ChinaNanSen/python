import okx.MarketData as MarketData
import configparser
import pandas as pd
import time
from datetime import datetime
import finta

# 初始化API
config = configparser.ConfigParser()
config.read('config.ini')
flag = config['OKX']['flag']
marketDataAPI = MarketData.MarketAPI(flag=flag)


def get_monthly_historical_data(instId, year, month, bar):
    # 计算月份的开始和结束时间戳
    start_date = datetime(year, month, 1)
    end_date = datetime(
        year, month + 2, 1) if month < 12 else datetime(year + 1, 1, 1)
    start_ts = int(start_date.timestamp()) * 1000
    end_ts = int(end_date.timestamp()) * 1000

    print(start_date, end_date)

    all_data = []
    last_ts = end_ts

    while True:
        result = marketDataAPI.get_history_candlesticks(
        # result = marketDataAPI.get_candlesticks(
            instId=instId,
            bar=bar,
            before=str(start_ts),
            # after="1699852860000",
            after=str(last_ts),
            limit="100"
        )
        print(last_ts, start_ts)

        if 'data' in result and len(result['data']) > 0:
            batch_data = result['data']
            first_ts = int(batch_data[0][0])

            if first_ts < start_ts:
                # 过滤掉开始时间之前的数据
                batch_data = [x for x in batch_data if int(x[0]) >= start_ts]
                all_data.extend(batch_data)
                break
            else:
                all_data.extend(batch_data)
                last_ts = batch_data[-1][0]  # 更新时间戳为最后一条数据的时间戳

            time.sleep(0.1)  # 遵守API的限速规则
        else:
            break  # 如果没有数据返回，则停止循环

    return pd.DataFrame(all_data, columns=[
        "ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"])


# 示例用法
# 获取2023年5月的BTC-USDT历史数据
# datas = get_monthly_historical_data("LTC-USDT", 2023, 9, "15m")
# datas['ts'] = pd.to_datetime(datas['ts'], unit='ms')
# datas['ts'] = datas['ts'].dt.strftime('%Y-%m-%d %H:%M:%S')
# datas.set_index('ts', inplace=True)
csv_file_name = 'historical_data_2023_05.csv'
# datas.to_csv(csv_file_name)
print("数据写入成功！！！")


# 假设data1是您的历史数据DataFrame
data1 = pd.read_csv(csv_file_name)
data1 = data1.sort_values(by='ts')
# data1.set_index('ts', inplace=True)


# 计算移动平均
data1['mas'] = finta.TA.SMA(data1,  15)
data1['mal'] = finta.TA.SMA(data1, 150)
data1['emas'] = finta.TA.EMA(data1, 15)
data1['emal'] = finta.TA.EMA(data1, 157)


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

# 回测逻辑
for index, row in data1.iterrows():
    # print(row['ts'])
    if pd.isna(row['emas']) or pd.isna(row['emal']):  # 跳过还未生成MA的行
        continue

    price = row['close'] * (1 + slippage)  # 模拟实际成交价格（包括滑点）

    # 检查买入信号
    # print(row)
    # if row['mas'] > row['mal'] and balance > 0:
    if row['emas'] > row['emal'] and balance > 0:
        amount = balance / price
        fee = amount * price * commission_rate
        balance -= amount * price + fee
        position += amount
        total_commission += fee  # 累加手续费
        trades.append({'type': 'buy', 'price': price,
                      'amount': amount, 'fee': fee, 'timestamp': row['ts']})

    # 检查卖出信号

    # elif row['mas'] < row['mal'] and position > 0:
    elif row['emas'] < row['emal'] and position > 0:
        fee = position * price * commission_rate
        balance += position * price - fee
        position = 0
        trades.append({'type': 'sell', 'price': price,
                      'amount': position, 'fee': fee, 'timestamp': row['ts']})

# 性能评估
final_balance = balance + position * data1['close'].iloc[-1]
performance = final_balance - initial_balance

# 将交易记录输出到文件
trades_df = pd.DataFrame(trades)
trades_df.to_csv('trading_record.csv', index=False)

# 打印结果
print(
    f"Initial Balance: {initial_balance}, Final Balance: {final_balance}, Performance: {performance}, Total Commission Paid: {total_commission}")
