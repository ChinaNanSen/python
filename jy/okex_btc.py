import os
import time
import ccxt
import numpy as np
import config
import math

def calculate_performance_metrics(file_name):
    trades = np.genfromtxt(file_name, delimiter=',', skip_header=1)
    if trades.shape[0] < 2:
        return 0, 0, 0
    profits = trades[:, 4] * trades[:, 2]
    total_profit = np.sum(profits)
    profit_factor = np.sum(profits[profits > 0]) / np.abs(np.sum(profits[profits < 0]))
    daily_returns = (trades[1:, 4] - trades[:-1, 4]) / trades[:-1, 4]
    sharpe_ratio = (np.mean(daily_returns) * 252) / (np.std(daily_returns) * math.sqrt(252))
    return total_profit, profit_factor, sharpe_ratio


def fetch_ohlcv():
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    return np.array(ohlcv)

def calculate_moving_average(data, length):
    return np.convolve(data[:, 4], np.ones(length) / length, mode='valid')

def fetch_order_fee(order_id, symbol):
    order_info = exchange.fetch_order(order_id, symbol)
    fee_currency = order_info['info']['feeCcy']
    fee_amount = abs(float(order_info['info']['fee']))
    return fee_currency, fee_amount

def log_trade_to_file(file_name, trade_info):
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write('Timestamp,Operation,Price,Amount,Fee,Fee in USDT,Total Profit,Profit Factor,Sharpe Ratio\n')
            print(f"Created file: {file_name}")

    with open(file_name, 'a') as f:
        total_profit, profit_factor, sharpe_ratio = calculate_performance_metrics(file_name)
        trade_info += f',{total_profit},{profit_factor},{sharpe_ratio}'
        f.write(trade_info + '\n')
        print(f"Logged trade: {trade_info}")

exchange = ccxt.okex({
    'apiKey': config.api_key,
    'secret': config.secret_key,
    'password': config.password,
    'enableRateLimit': True,
})

symbol = 'ETH/USDT'
timeframe = '1m'
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

        if last_operation != 'buy' and fast_ma[-1] > slow_ma[-1] and usdt_balance > 1:
            print("buy")
            amount = usdt_balance / data[-1, 4]
            if amount >= min_trade_amount:
                order = exchange.create_market_buy_order(symbol, amount)
                order_id = order['id']
                fee_currency, fee_amount = fetch_order_fee(order_id, symbol)

                last_operation = 'buy'

                fee_currency = order['info']['feeCcy']
                fee_amount = float(order['info']['fee'])
                if fee_currency != 'USDT':
                    fee_conversion_symbol = f"{fee_currency}/USDT"
                    fee_conversion_rate = exchange.fetch_ticker(fee_conversion_symbol)['close']
                    fee_in_usdt = fee_amount * fee_conversion_rate
                else:
                    fee_in_usdt = fee_amount

                trade_info = {'Timestamp': order['datetime'], 'Operation': 'Buy', 'Price': order['info']['fillPx'], 'Amount': order['amount'], 'Fee': fee_in_usdt}
                print(trade_info)
                log_trade_to_file('trades.json', trade_info)

        elif last_operation != 'sell' and fast_ma[-1] < slow_ma[-1] and eth_balance * data[-1, 4] > 1:
            print("sell")
            if eth_balance >= min_trade_amount:
                order = exchange.create_market_sell_order(symbol, eth_balance)
                order_id = order['id']
                fee_currency, fee_amount = fetch_order_fee(order_id,symbol)

                last_operation = 'sell'

                fee_currency = order['info']['feeCcy']
                fee_amount = float(order['info']['fee'])
                if fee_currency != 'USDT':
                    fee_conversion_symbol = f"{fee_currency}/USDT"
                    fee_conversion_rate = exchange.fetch_ticker(fee_conversion_symbol)['close']
                    fee_in_usdt = fee_amount * fee_conversion_rate
                else:
                    fee_in_usdt = fee_amount

                trade_info = {'Timestamp': order['datetime'], 'Operation': 'Sell', 'Price': order['info']['fillPx'], 'Amount': order['amount'], 'Fee': fee_in_usdt}
                print(trade_info)
                log_trade_to_file('trades.json', trade_info)

        time.sleep(60)
    except Exception as e:
        print(e)
        time.sleep(60)


