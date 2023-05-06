import os
import time
import ccxt
import numpy as np
import config

def fetch_ohlcv():
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    return np.array(ohlcv)


def calculate_moving_average(data, length):
    return np.convolve(data[:, 4], np.ones(length) / length, mode='valid')


#def calculate_moving_average(data, length):
    #return data[-length:, 4].mean()

def log_trade_to_file(file_name, trade_info):
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write('Timestamp,Operation,Price,Amount,Profit/Loss Percentage,Fee in USDT\n')

    with open(file_name, 'a') as f:
        f.write(trade_info + '\n')

exchange = ccxt.okex({
    'apiKey': config.api_key,
    'secret': config.secret_key,
    'password': config.password,
    'enableRateLimit': True,
})

symbol = 'ETH/USDT'
timeframe = '15m'
fast_ma_length = 5
slow_ma_length = 20
min_trade_amount = 0.0001

last_operation = None

while True:
    try:
        data = fetch_ohlcv()
        fast_ma = calculate_moving_average(data, fast_ma_length)
        slow_ma = calculate_moving_average(data, slow_ma_length)
        print(fast_ma[-1])
        print(slow_ma[-1])

        balance = exchange.fetch_balance()
        eth_balance = balance.get('ETH', {}).get('free', 0)
        usdt_balance = balance.get('USDT', {}).get('free', 0)
        print(eth_balance)
        print(usdt_balance)
    

        if last_operation != 'buy' and fast_ma[-1] > slow_ma[-1] and usdt_balance > 1:
            amount = usdt_balance / data[-1, 4]
            if amount >= min_trade_amount:
                order = exchange.create_market_buy_order(symbol, amount)
                print("order = ", order)

                last_operation = 'buy'
                print('已买入 ETH')

                fee_currency = order['info']['feeCcy']
                fee_amount = float(order['info']['fee'])
                if fee_currency != 'USDT':
                    fee_conversion_symbol = f"{fee_currency}/USDT"
                    fee_conversion_rate = exchange.fetch_ticker(fee_conversion_symbol)['close']
                    fee_in_usdt = fee_amount * fee_conversion_rate
                else:
                    fee_in_usdt = fee_amount

                trade_info = f"{order['info']['ts']},Buy,{order['info']['fillPx']},{order['info']['fillSz']},N/A,{fee_in_usdt}"
                print(trade_info)
                log_trade_to_file('./trades.csv', trade_info)

        elif last_operation != 'sell' and fast_ma[-1] < slow_ma[-1] and eth_balance * data[-1, 4] > 1:
            if eth_balance >= min_trade_amount:
                order = exchange.create_market_sell_order(symbol, eth_balance)
                print("sell order =  ",order)

                last_operation = 'sell'
                print('已售出 ETH')

                fee_currency = order['info']['feeCcy']
                fee_amount = float(order['info']['fee'])
                if fee_currency != 'USDT':
                    fee_conversion_symbol = f"{fee_currency}/USDT"
                    fee_conversion_rate = exchange.fetch_ticker(fee_conversion_symbol)['close']
                    fee_in_usdt = fee_amount * fee_conversion_rate
                else:
                    fee_in_usdt = fee_amount

                trade_info = f"{order['info']['ts']},Sell,{order['info']['fillPx']},{order['info']['fillSz']},N/A,{fee_in_usdt}"
                print(trade_info)
                log_trade_to_file('./trades.csv', trade_info)

        time.sleep(60 * 15)
    except Exception as e:
        print(e)
        time.sleep(60)

