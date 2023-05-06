import os

def log_trade_to_file(file_name, trade_info):
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write('Timestamp,Operation,Price,Amount,Profit/Loss Percentage\n')

trade_info = "xxxxxxxxxxxxxxxxxxxxx"
print(trade_info)
log_trade_to_file('trades.csv', trade_info)
print(log_trade_to_file)
