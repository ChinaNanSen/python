import okx.Account as Account
import okx.Trade as Trade
import okx.MarketData as MarketData
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import logging
import json
import time
import finta
import configparser
import random
# from datetime import *


# API 初始化
# 从配置文件读取API初始化信息
config = configparser.ConfigParser()
config.read('config.ini')

apikey = config['OKX']['apikey']
secretkey = config['OKX']['secretkey']
passphrase = config['OKX']['passphrase']
flag = config['OKX']['flag']  # 实盘:0 , 模拟盘:1


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
    return result


def generate_order_id():
    # 生成一个新的随机订单号
    return random.randint(10000, 99999)


def tradedata():
    result = tradeAPI.get_orders_history(
        instType="SPOT",
        ordType="market,post_only,fok,ioc"
    )
    return result

def positions():
    result = accountAPI.get_positions(
        instType="SWAP",
        instId=bz
    )
    return result




# 配置日志
logging.basicConfig(filename='trading_test_btc.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',encoding='utf-8')

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



def jy():

    # 跟踪全局变量状态
    global position_opened
    global order_id  # 使用global关键字声明order_id是全局变量
    
    # print(getOrder('641999281087422464'))
    # exit(1006)
  

   # 获取当前时间的 Unix 时间戳
    timestamp = time.time()
    local_time = time.localtime(timestamp)
    nows = time.asctime(local_time)
    time_tuple = time.strptime(nows, "%a %b %d %H:%M:%S %Y")
    now = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)

        
    # 获取历史数据
    historical_data = marketDataAPI.get_candlesticks(
        instId=bz,
        # before="",
        bar="30m",
        limit="160"
    )
    time.sleep(0.1)
    data1 = pd.DataFrame(historical_data["data"], columns=[
        "ts", "open", "high", "low", "close", "vol", "volCcy", "volCcyQuote", "confirm"])

    data1['ts'] = data1['ts'].apply(
        lambda x: datetime.datetime.fromtimestamp(int(x) / 1000))
    data_frame['ts'] = data_frame['ts'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data_frame.set_index('ts', inplace=True)
    return data_frame

def trading_logic(data_frame, position_opened):
    
    # 交易逻辑
    ma15 = finta.TA.SMA(data_frame, 15)
    ma150 = finta.TA.SMA(data_frame, 150)
    bbands = finta.TA.BBANDS(data_frame)
    bu = bbands.iloc[-1]['BB_UPPER']
    bl = bbands.iloc[-1]['BB_LOWER']
    cn = data_frame['close'].iloc[0]
    hn = data_frame['high'].iloc[0]
    ln = data_frame['low'].iloc[0]
    print("\033[32mcn:%s\nbl:%s\n\033[0m" %(ln, bl))
    print("-------------")
    print("\033[31mcn:%s\nbu:%s\n\033[0m" %(hn, bu))

    if float(ln) < bl and  position_opened == False:
        print(position_opened)
        print("\033[32m开始买入\033[0m")
        print("-----")
        
        # 买入信号
        
        ye = account("USDT")
        

        ccb = ye["details"][0]["availBal"]
        cb = float(ccb) / 2
        # print(ye)
        print(position_opened)
        # exit(1023)
        print(cb)
        info = {}
        info['币种'] = dbz 
        info['date'] = now
        info['方向'] = "买"
        info['状态'] = position_opened
        info['订单ID'] = order_id
        info['支出'] = cb
        info['最低价'] = ln
        info['LB'] = bl
       
        # exit(1036)
        if float(cb) >= 100:

            result = tradeAPI.place_order(
                instId=bz,
                tdMode="cross",  # 保证金模式：isolated：逐仓 ；cross：全仓
                # ccy=dbz,
                # posSide="short",  # 选择 long 或 short
                # side="sell",
                posSide="long",  # 选择 long 或 short
                side="buy",
                clOrdId="buy"+str(order_id),
                ordType="market",  # market 市价单 ，limit 限价单
                # px="34430",
                sz="300"  # 买入100 USDT的BTC
            )
            print(result)
            # 更新持仓状态
            position_opened = True
            # 订单ID
            oid = result['data'][0]['clOrdId']
            # print(">>>>>>>>",oid)
            oidict = {}
            # 订单币币余额
            bye = getOrder(oid)['data'][0]['fillSz']
            # print(position_opened,"----------------",bye)
            # 订单币币余额消费
            bxf = getOrder(oid)['data'][0]['sz']
            # 成交价
            bcj = getOrder(oid)['data'][0]['fillPx']
            # 订单手续费
            bsx = getOrder(oid)['data'][0]['fee']
            
            info['oid'] = "buy"+str(order_id)
            info['成交价'] = bcj
            info['资金费'] = bsx
            dd.append(info)
            # print(dd)

            buy_signals[data1.index[15]] = data1['close'].iloc[15]
            print("\033[32m++++hit++buy\033[0m")
        else:
            print("\033[31mbuy操作忽略,USDT余额不足\033[0m")

    # elif ma15.iloc[15] < ma150.iloc[150] and position_opened == False:
    if float(hn) > bu and position_opened :
        print("\033[31m开始卖出\033[0m")
        print("++++++++++")
        print(order_id)
        info = {}
        info['币种'] = dbz
        info['date'] = now
        info['方向'] = "卖"
        info['状态'] = position_opened
        info['订单ID'] = order_id
        # info['支出'] = cb
        info['最高价'] = hn
        info['UB'] = bu
    
        # 卖出信号
        try:
            byex = getOrder("buy"+str(order_id))['data'][0]['fillSz']
        except Exception as es:
            print(f"\033[31m没有买入订单,忽略: {es} {byex}\033[0m")
            

        if float(byex) != 0:

            uresult = tradeAPI.close_positions(
                instId=bz,
                # ccy='BTC',
                clOrdId="sell"+str(order_id),
                posSide="long",
                mgnMode="cross"
            )
            print(uresult)

            position_opened = False
            uoid = uresult['data'][0]['clOrdId']
            print(uoid)
            # 订单币币余额
            uye = getOrder(uoid)['data'][0]['fillSz']
            # 订单币币收入
            uxf = getOrder(uoid)['data'][0]['sz']
            # 成交价
            ucj = getOrder(uoid)['data'][0]['fillPx']
            # 订单手续费
            usx = getOrder(uoid)['data'][0]['fee']
            
            info['uoid'] = "sell"+str(order_id)
            info['成交价'] = ucj
            info['资金费'] = usx
            dd.append(info)

            sell_signals[data1.index[15]] = data1['close'].iloc[15]
            print("\033[32m---hit-----sell\033[0m")

        else:
            print("\033[31msell操作忽略,BTC余额不足\033[0m")
    else:
        print("\033[33m###########miss\033[0m")


    if position_opened:
        print(position_opened)
        pos_data = positions()['data'][0]
        if float(pos_data['upl']) <= -9:
            print("\033[31m亏损超过11U,平仓\033[0m")
            print(order_id)
            print("==========")
            info = {}
            info['币种'] = dbz
            info['date'] = now
            info['方向'] = "平仓"
            info['状态'] = position_opened
            info['订单ID'] = order_id
            info['亏损'] = pos_data['upl']
            
            # 卖出信号
            try:
                byex = getOrder("buy"+str(order_id))['data'][0]['fillSz']
            except Exception as es:
                print(f"\033[31m没有买入订单,忽略: {es} {byex}\033[0m")
                

            if float(byex) != 0:

                uresult = tradeAPI.close_positions(
                    instId=bz,
                    # ccy='BTC',
                    clOrdId="sell"+str(order_id),
                    posSide="long",
                    mgnMode="cross"
                )
                print(uresult)
                
                position_opened = False
                
                
                uoid = uresult['data'][0]['clOrdId']
                print(uoid)
                # 订单币币余额
                uye = getOrder(uoid)['data'][0]['fillSz']
                # 订单币币收入
                uxf = getOrder(uoid)['data'][0]['sz']
                # 成交价
                ucj = getOrder(uoid)['data'][0]['fillPx']
                # 订单手续费
                usx = getOrder(uoid)['data'][0]['fee']
               
                info['id'] = "sell"+str(order_id)
                info['成交价'] = ucj
                info['资金费'] = usx
                dd.append(info)
               

                sell_signals[data1.index[15]] = data1['close'].iloc[15]
                print("\033[32m---hit-----sell\033[0m")

            else:
                print("\033[31msell操作忽略,BTC余额不足\033[0m")



if __name__ == "__main__":
    dd = []  
    position_opened = False
    while True:
        # print(dd)
        # 将交易记录输出到文件
        log_dictionary(dd)
        dd.clear()
        time.sleep(2)
        jy()
        print(position_opened)
        
        
        