import ccxt
import time
import numpy as np
import config

# 初始化交易所
exchange = ccxt.okex({
    'apiKey': config.api_key,
    'secret': config.secret_key,
    'enableRateLimit': True,
})

symbol = 'ETH/USDT'  # 选择交易对
timeframe = '1m'  # 设定K线周期
fast_ma_length = 5  # 快速均线长度
slow_ma_length = 20  # 慢速均线长度

def fetch_ohlcv():
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    return np.array(ohlcv)

def calculate_moving_average(data, length):
    return data[-length:, 4].mean()

last_operation = None
while True:
    try:
        data = fetch_ohlcv()
        fast_ma = calculate_moving_average(data, fast_ma_length)
        slow_ma = calculate_moving_average(data, slow_ma_length)

        balance = exchange.fetch_balance()
        btc_balance = balance['ETH']['free']
        usdt_balance = balance['USDT']['free']

        if last_operation != 'sell' and fast_ma > slow_ma and btc_balance * data[-1, 4] > 10:
            order = exchange.create_market_sell_order(symbol, btc_balance)
            print('已卖出', order)
            last_operation = 'sell'

        elif last_operation != 'buy' and fast_ma < slow_ma and usdt_balance > 10:
            buy_amount = usdt_balance / data[-1, 4]
            order = exchange.create_market_buy_order(symbol, buy_amount)
            print('已买入', order)
            last_operation = 'buy'

        time.sleep(60)
    except Exception as e:
        print(e)
        time.sleep(60)
