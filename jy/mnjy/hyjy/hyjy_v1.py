import okx.Account as Account
import okx.Trade as Trade
import okx.MarketData as MarketData
import pandas as pd
import datetime
import logging
import json
import time
import finta
import configparser
import random

# 配置文件读取
config = configparser.ConfigParser()
config.read('config.ini')

apikey = config['OKX']['apikey']
secretkey = config['OKX']['secretkey']
passphrase = config['OKX']['passphrase']
flag = config['OKX']['flag']

accountAPI = Account.AccountAPI(apikey, secretkey, passphrase, False, flag)
tradeAPI = Trade.TradeAPI(apikey, secretkey, passphrase, False, flag)
marketDataAPI = MarketData.MarketAPI(flag=flag)
bz = "BTC-USDT-SWAP"
dbz = "BTC"


def getOrder(oid):
    result = tradeAPI.get_order(
        instId=bz,
        # ordId=oid,
        clOrdId=oid
    )
    time.sleep(0.1)
    return result


def generate_order_id():
    # 生成一个新的随机订单号
    return random.randint(10000, 99999)


def tradedata():
    result = tradeAPI.get_orders_history(
        instType="SPOT",
        ordType="market,post_only,fok,ioc"
    )
    time.sleep(0.1)
    return result

def positions():
    result = accountAPI.get_positions(
        instType="SWAP",
        instId=bz
    )
    time.sleep(0.1)
    return result




# 配置日志
logging.basicConfig(filename='trading_btc.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',encoding='utf-8')

def log_dictionary(dict_data):
    """
    记录字典内容到日志文件中，确保中文字符可读
    """
    try:
        # 将字典转换为 JSON 字符串，并确保中文字符被正确解码
        dict_as_string = json.dumps(dict_data, indent=4, ensure_ascii=False)
        # 将字符串写入日志
        logging.info(dict_as_string)
    except Exception as e:
        logging.error(f"Error logging dictionary: {e}")


def account(cb):
    for attempt in range(3):  # 尝试次数
        try:
            result = accountAPI.get_account_balance(
                ccy=cb
            )
            time.sleep(0.1)
            return result["data"][0]
        except Exception as e:
            print(f"Error: {e}")
            if attempt < 2:  # 如果这不是最后一次尝试，等待2秒然后再次尝试
                time.sleep(2)
            else:
                print("Failed to get account balance after 3 attempts.")
                return None  # 或者返回一个错误值/异常，让调用者知道请求失败


# # 获取历史数据
# historical_data = marketDataAPI.get_candlesticks(
#     instId="BTC-USDT",
#     # bar="5m"
# )
"""
bar	String	否	时间粒度，默认值1m
如 [1m/3m/5m/15m/30m/1H/2H/4H]
香港时间开盘价k线：[6H/12H/1D/2D/3D/1W/1M/3M]
UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc]
"""

# 转换数据到 DataFrame

"""
ts	String	开始时间，Unix时间戳的毫秒数格式，如 1597026383085
o	String	开盘价格
h	String	最高价格
l	String	最低价格
c	String	收盘价格
vol	String	交易量，以张为单位
如果是衍生品合约，数值为合约的张数。
如果是币币/币币杠杆，数值为交易货币的数量。
volCcy	String	交易量，以币为单位
如果是衍生品合约，数值为交易货币的数量。
如果是币币/币币杠杆，数值为计价货币的数量。
volCcyQuote	String	交易量，以计价货币为单位
如：BTC-USDT 和 BTC-USDT-SWAP, 单位均是 USDT；
BTC-USD-SWAP 单位是 USD
confirm	String	K线状态
0 代表 K 线未完结，1 代表 K 线已完结。

"""


print("\033[34m~~~~~starting jy %s\033[0m" % dbz)


# 新增函数：计算EMA
def calculate_ema(data, period):
    return finta.TA.EMA(data, period)

# 新增函数：执行交易
def execute_trade(order_side, size, order_id):
    try:
        if order_side == 'buy':
            result = tradeAPI.place_order(
                instId=bz,
                tdMode="cross",
                posSide="long",
                side=order_side,
                clOrdId=order_id,
                ordType="market",
                sz=size
            )
        else:
            result = tradeAPI.place_order(
                instId=bz,
                tdMode="cross",
                posSide="short",
                side=order_side,
                clOrdId=order_id,
                ordType="market",
                sz=size
            )
        return result
    except Exception as e:
        logging.error(f"Error placing order: {e}")
        return None

# 新增函数：检查EMA交叉点
def check_ema_cross(data, short_period, long_period):
    short_ema = calculate_ema(data, short_period)
    long_ema = calculate_ema(data, long_period)
    
    if len(data) < 3:
        return None
    
    # 检查上拐点
    if (data['close'].iloc[-1] > short_ema.iloc[-1]) and (data['close'].iloc[-2] < short_ema.iloc[-2]) and (short_ema.iloc[-1] > long_ema.iloc[-1]):
        return 'buy'
    # 检查下拐点
    elif (data['close'].iloc[-1] < short_ema.iloc[-1]) and (data['close'].iloc[-2] > short_ema.iloc[-2]) and (short_ema.iloc[-1] < long_ema.iloc[-1]):
        return 'sell'
    return None

# 核心交易逻辑函数
def jy():
    global position_opened
    global order_id
    
    # 获取5分钟历史数据
    historical_data = marketDataAPI.get_candlesticks(
        instId=bz,
        bar="5m",
        limit="120"
    )
    data1 = pd.DataFrame(historical_data["data"], columns=[
        "ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"])
    
    # 转换时间戳
    data1['ts'] = pd.to_datetime(data1['ts'], unit='ms')
    data1.set_index('ts', inplace=True)
    
    # 计算EMA
    ema_10 = calculate_ema(data1, 10)
    ema_60 = calculate_ema(data1, 60)
    
    # 确定交易信号
    signal = check_ema_cross(data1, 10, 60)
    
    # 执行买入或卖出操作
    if signal == 'buy' and not position_opened:
        order_id = generate_order_id()
        result = execute_trade('buy', 1, order_id)
        if result:
            position_opened = True
            logging.info(f"Buy order placed. Order ID: {order_id}")
        else:
            logging.error("Failed to place buy order.")
    
    elif signal == 'sell' and position_opened:
        # 执行卖出操作，此处假设您已经持有多头仓位
        order_id = generate_order_id()
        result = execute_trade('sell', 1, order_id)
        if result:
            position_opened = False
            logging.info(f"Sell order placed. Order ID: {order_id}")
        else:
            logging.error("Failed to place sell order.")
    
    # 检查持仓并执行止损
    if position_opened:
        pos_data = positions()['data'][0]
        # 此处应根据实际的持仓数据结构来获取止损价格
        stop_loss_price = pos_data['entryPx'] * 0.98  # 假设止损价格为入场价格的98%
        current_price = data1['close'].iloc[-1]
        if current_price <= stop_loss_price:
            # 执行止损操作
            order_id = generate_order_id()
            result = execute_trade('sell', 1, order_id)
            if result:
                position_opened = False
                logging.info(f"Stop loss triggered. Order ID: {order_id}")
            else:
                logging.error("Failed to execute stop loss.")

# 主循环
if __name__ == "__main__":
    logging.basicConfig(filename='trading_btc.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
    dd = []
    position_opened = False
    order_id = None
    
    while True:
        try:
            jy()
            # 记录交易日志
            log_dictionary(dd)
            dd.clear()
            time.sleep(300)  # 每5分钟执行一次
        except Exception as e:
            logging.error(f"Error in trading loop: {e}")
            time.sleep(10)  # 短暂等待后重试