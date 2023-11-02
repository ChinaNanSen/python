import openai_secret_manager
import pandas as pd

credentials = openai_secret_manager.get_secret("okx")

import okex.v5 as okex

client = okex.Client(
    api_key=credentials["api_key"],
    api_secret=credentials["api_secret"],
    passphrase=credentials["passphrase"]
)




# 获取历史数据
historical_data = client.futures_historical_data(instrument_id='BTC-USD-210625', start='', end='', granularity=60)

# 将数据转换为DataFrame
df = pd.DataFrame(historical_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'currency_volume'])

# 计算均线
df['short_ma'] = df['close'].rolling(window=10).mean()
df['long_ma'] = df['close'].rolling(window=50).mean()

for i in range(len(df)):
    # 仅在有足够的数据时检查均线交叉
    if i >= 50:
        # 当短期均线上穿长期均线时买入
        if df['short_ma'][i] > df['long_ma'][i] and df['short_ma'][i-1] <= df['long_ma'][i-1]:
            client.futures_trade(instrument_id='BTC-USD-210625', type='open_long', price='', size='1', match_price='1', leverage='10')
        # 当短期均线下穿长期均线时卖出
        elif df['short_ma'][i] < df['long_ma'][i] and df['short_ma'][i-1] >= df['long_ma'][i-1]:
            client.futures_trade(instrument_id='BTC-USD-210625', type='close_long', price='', size='1', match_price='1', leverage='10')
