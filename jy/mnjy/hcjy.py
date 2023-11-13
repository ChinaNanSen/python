import okx.MarketData as MarketData
import configparser
import pandas as pd
import time
from datetime import datetime

# 初始化API
config = configparser.ConfigParser()
config.read('config.ini')
flag = config['OKX']['flag']
marketDataAPI = MarketData.MarketAPI(flag=flag)


def get_monthly_historical_data(instId, year, month, bar):
    # 计算月份的开始和结束时间戳
    start_date = datetime(year, month, 1)
    end_date = datetime(
        year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
    start_ts = int(start_date.timestamp()) * 1000
    end_ts = int(end_date.timestamp()) * 1000

    print(start_date,end_date)

    all_data = []
    last_ts = end_ts

    while True:
        result = marketDataAPI.get_history_candlesticks(
            instId=instId,
            bar=bar,
            before=str(start_ts),
            # after="1699852860000",
            after=str(last_ts),
            limit="100"
        )
        print(last_ts,start_ts)

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
datas = get_monthly_historical_data("BTC-USDT", 2023, 5, "15m")
datas['ts'] = pd.to_datetime(datas['ts'], unit='ms')
datas['ts'] = datas['ts'].dt.strftime('%Y-%m-%d %H:%M:%S')
datas.set_index('ts', inplace=True)
csv_file_name = 'historical_data_2023_05.csv'
datas.to_csv(csv_file_name)
print("数据写入成功！！！")
