import pandas as pd
import finta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib

# 设置 Matplotlib 使用中文字体
matplotlib.rcParams['font.family'] = 'SimHei'  # 例如使用 "SimHei" 字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 读取交易记录和历史数据
data1 = pd.read_csv('historical_data_2023_05.csv')
trades_df = pd.read_csv('trading_record.csv')



# # 准备买卖信号标记
buy_signals = trades_df[trades_df['type'] == 'buy']
sell_signals = trades_df[trades_df['type'] == 'sell']
data1['emas'] = finta.TA.EMA(data1, 15)
data1['emal'] = finta.TA.EMA(data1, 150)





# 假设 data1, buy_signals, sell_signals 已经准备好
data1['date'] = pd.to_datetime(data1['ts'])
fig, ax = plt.subplots(figsize=(12, 6))


# 绘制 K 线图
ax.plot(data1['date'], data1['close'], label='LTC-收盘价')

# print(buy_signals.columns)

# 绘制买卖信号
ax.scatter(buy_signals['timestamp'], buy_signals['price'], color='green', marker='^', label='买入信号')
ax.scatter(sell_signals['timestamp'], sell_signals['price'], color='red', marker='v', label='卖出信号')

# 设置 X 轴为日期格式
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# 显示图例
ax.legend()

plt.show()
