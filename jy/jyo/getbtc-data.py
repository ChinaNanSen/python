import os
import time
import ccxt
import numpy as np
import config

exchange = ccxt.okex({
    'apiKey': config.api_key,
    'secret': config.secret_key,
    'password': config.password,
    'enableRateLimit': True,
})

def log_trade_to_file(file_name, trade_info):
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write('Timestamp,Operation,Price,Amount,Fee,Fee in USDT\n')
            print(f"Created file: {file_name}")

    with open(file_name, 'a') as f:
        f.write(trade_info + '\n')
        print(f"Logged trade: {trade_info}")

def fetch_order_fee(order_id, symbol):
    order_info = exchange.fetch_order(order_id, symbol)
    print(f"Order info: {order_info}")  # 添加此行以查看'order_info'内容
    fee_currency = order_info['info']['feeCcy']  # 修改此行
    fee_amount = abs(float(order_info['info']['fee']))  # 修改此行
    return fee_currency, fee_amount


# order_id = '575409374068699136'  # 请替换为您的实际订单ID
# symbol = 'ETH/USDT'

# order = fetch_order_fee(order_id, symbol)
# # print(order)
# # print(order['info']['ordId'])
# trade_info = "%s,%s"%(order[0],order[1])
# log_trade_to_file('.\\test.csv',trade_info)

file_path = 'file.json'  # 文件路径
file_mode = 'w'  # 打开文件的模式，'w'表示写入模式

with open(file_path, file_mode) as file:
    # 写入内容
    file.write('Hello, world!\n')
    file.write('This is a test file.\n')
    file.write('Writing some text.\n')

